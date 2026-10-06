import json
import asyncio
import os
from ast import literal_eval #解析数据（eg.字符串->列表、字典等）
from fastapi import APIRouter,UploadFile,Form
from fastapi.responses import StreamingResponse
from tools.tools_select import tools
from typing import List,AsyncIterable
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #message模版
from langchain.agents import create_react_agent,AgentExecutor#ReAct框架
from langchain.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate
from configs.prompt import PROMPT_TEMPLATES
from configs.setting import chat_model_name, api_key, base_url, TIME_OUT, TEMP_FILE_STORAGE_DIR
from utils.callback import CustomAsyncIteratorCallbackHandler #SSE流式输出
from db_server.base import session
from db_server.knowledge_base_repository import list_kb_from_db #结果转换成列表格式
from tools.code_interpreter import code_interpreter #链路清洗+返回图片
from utils.load_docs import get_file_content #读取不同类型文件内容

chat_router = APIRouter(prefix="/chat",tags=["Chat 对话"])

def files_rag(files,uuid):
    kb_file_storage_path = os .path.join(TEMP_FILE_STORAGE_DIR,uuid)
    result = []
    #确保目录存在
    os.makedirs(kb_file_storage_path,exist_ok=True)
    if files:
        for file in files:
             file_path = os.path.join(kb_file_storage_path,file.filename)

             with open(file_path,"wb") as f:
                 f.write(file.file.read())
    #遍历读取文件内容
    for filename in  os.listdir(kb_file_storage_path):
        file_path = os.path.join(kb_file_storage_path,filename)
        if os.path.isfile(file_path):
            file_content = get_file_content(file_path)

            result.append(f"document:.{file_path}\ncontent:{file_content}\n")
    return "".join(result)

#实例化对象，设置历史对话
@chat_router.post("/agent_chat")
async def agent_chat(
        files: List[UploadFile] = None,
        query: str = Form(...,description="用户输入"),
        sys_prompt: str = Form("You are a heapful assistant.",description="系统提示"),
        history_len: int = Form(-1,description="保留历史消息的数量"),
        history: List[str] = Form([],description="历史对话"),
        temperature: float = Form(0.5,description="LLM采样温度"),
        max_tokens: int = Form(1024,description="LLM最大token数配置"),
        session_id: str = Form(None,description="会话标识"),

):   
    documents = files_rag(files,session_id)
    history = [literal_eval(item) for item in history]
    histories = ""
    if history_len >0:
        history = history[-2*history_len:]

    for msg in history:
        role = msg.get('role')
        content = msg.get('content')
        histories += f"{role}:{content}\n\n"

    async def agent_chat_iterator() -> AsyncIterable[str]:
        #使用自己定义的迭代器函数
        callback = CustomAsyncIteratorCallbackHandler()
        callbacks = [callback]

        chat_model = ChatOpenAI(
            model = chat_model_name,
            api_key = api_key,
            base_url = base_url,
            temperature = temperature,
            max_tokens = max_tokens,
            streaming = True,
            callbacks = callbacks
        )

        system_prompt = SystemMessagePromptTemplate.from_template(
            sys_prompt
        )
        human_prompt = HumanMessagePromptTemplate.from_template(
            PROMPT_TEMPLATES["agent"]
        )
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt,human_prompt])

        #创建代理
        agent = create_react_agent(chat_model,tools,chat_prompt,stop_sequence=["\nObserv"])
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose= True,
        )

        #列出所有知识库,并整理成字符串
        knowledgebases = list_kb_from_db(session)
        kbs = "".join([f"{kb['kb_name']} - {kb['kb_info']}\n" for kb in knowledgebases])
        code_interpreter.output_files,code_interpreter.output_codes = "",""

        #开启异步执行agent
        task = asyncio.create_task(
            agent_executor.acall(
                inputs={"input":query,"history":histories,"knowledgebases":kbs,"documents":documents}
            )
        )

        async for token in callback.aiter():
            response_data = {
                "answer":token,
            }
            yield json.dumps(response_data).encode('utf-8')

        await asyncio.wait_for(task,TIME_OUT)
        output_files,output_codes = code_interpreter.get_outputs()

        if output_files:
            yield json.dumps({"answer":f'\n\n{output_codes}\n\n![](http://localhost:6605{output_files})'}).encode('utf-8')
        else:
            yield json.dumps({"answer":f'\n\n{output_codes}'}).encode('utf-8')

    return StreamingResponse(agent_chat_iterator(),media_type="application/json")
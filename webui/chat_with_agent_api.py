# 定义后台 API 的 URL
import json
import requests
from contextlib import ExitStack

chat_with_agent_url = "http://127.0.0.1:6605/chat/agent_chat"
chat_url = "http://127.0.0.1:6605/chat/chat"


def chat_with_agent(prompt, history, sys_prompt, history_len, temperature, max_tokens, stream, session_id):
    # 构建文件和表单数据
    with ExitStack() as stack:
        files = []
        for f in prompt.get("files", []):
            file_handle = stack.enter_context(open(f["path"], 'rb'))
            files.append(('files', (f["path"], file_handle)))
    
        query = prompt["text"]
        if prompt.get("files"):
            query += "\n" + "".join([f["path"] for f in prompt["files"]])
            
        data = {
            "query": query,
            "sys_prompt": sys_prompt,
            "history_len": history_len,
            "history": [str(h) for h in history],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "session_id": session_id,
        }

        # 添加用户消息到历史
        history.append({"role": "user", "content": query})
        # 初始化助手消息（用于流式更新）
        history.append({"role": "assistant", "content": ""})
        
        try:
            response = requests.post(chat_with_agent_url, files=files, data=data, stream=True)
            if response.status_code == 200:
                chunks = ""
                if stream:
                    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            d = json.loads(chunk)
                            chunks += d.get('answer', '')
                            history[-1]["content"] = chunks
                            yield history # 流式返回整个 history
                else:
                    # 非流式逻辑类似
                    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                        d = json.loads(chunk)
                        chunks += d.get('answer', '')
                    history[-1]["content"] = chunks
                    yield history
            else:
                history[-1]["content"] = "请求失败，请检查后台服务器是否正常运行。"
                yield history
        except Exception as e:
            history[-1]["content"] = f"发生错误：{e}"
            yield history

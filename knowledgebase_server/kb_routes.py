import os
import shutil
from typing import List
import jieba
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from .loader.loader import data_loader
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import HTTPException, APIRouter, Body, UploadFile, File, Form
from db_server.base import session
from db_server.knowledge_base_repository import add_kb_to_db, del_kb_from_db
from configs.setting import KB_DIR, FILE_STORAGE_DIR, embedding_model_path

kb_router = APIRouter(prefix="/knowledgebase", tags=["knowledge Bases Management"])

if not os.path.exists(KB_DIR):
    os.makedirs(KB_DIR)

class CustomEmbeddingModel(Embeddings):
    def __init__(self,model,model_name):
        self.model = model
        self.model_name = model_name

# 文档文本向量化
    def embed_documents(self, texts):
        return [self.model.client.create(model=self.model_name,input=text).data[0].embedding for text in texts]
# 用户问题向量化
    def embed_query(self, text):
        return self.model.client.create(model=self.model_name, input=text).data[0].embedding
embedding = OpenAIEmbeddings(
    api_key = "sk-yjjxzctudycwysxmbgsrtnalelpudblbdwrmjusvneaayzvc",
    base_url="https://api.siliconflow.cn/v1",
)
embedding_model = CustomEmbeddingModel(embedding,"BAAI/bge-large-zh-v1.5")

#创建新知识库
@kb_router.post("/create_kb")
async def create_kb(
    kb_name: str = Body(...,description="知识库名称"),
    kb_info: str = Body("",description="知识库内容简介（用于Agent选知识库）"),
):
    kb_path = os.path.join(KB_DIR,f"{kb_name}.faiss")

    if os.path.exists(kb_path):
        raise HTTPException(status_code=400,detail="知识库已存在")

    # 创建一个临时向量数据库
    doc = Document(page_content="init",metadata={})
    vector_store = FAISS.from_documents([doc],embedding_model,normalize_L2=True) # 向量归一化处理，并计算余弦相似度
    ids = list(vector_store.docstore._dict.keys())
    vector_store.delete(ids)

    vector_store.save_local(kb_path)

    add_kb_to_db(session,kb_name,kb_info)
    return {"message":f"知识库'{kb_name}'创建成功！"}

# 删除知识库
@kb_router.delete("/delete_kb")
async def delete_kb(kb_name: str):
    kb_path = os.path.join(KB_DIR,f"{kb_name}.faiss")
    kb_files_path = os.path.join(FILE_STORAGE_DIR,kb_name)

    if not os.path.exists(kb_path):
        raise HTTPException(status_code=404,detail="Database not found")

    shutil.rmtree(kb_path)
    if os.path.exists(kb_files_path):
        shutil.rmtree(kb_files_path)

    del_kb_from_db(session,kb_name)

    return {"message":f"Database '{kb_name}' deleted successfully"}

# 列出所有知识库的API
@kb_router.get("/list_kbs")
async def list_kbs():
    kb_files = [f for f in os.listdir(KB_DIR) if f.endswith(".faiss")]
    return {"knowledgebases": kb_files}

# 对知识库内的文件进行修改
@kb_router.post("/upload_docs")
async def upload_docs(
    files: List[UploadFile] = File(...),
    kb_name: str = Form(..., description="知识库名称"),
    chunk_size: int = Form(128, description="知识库中单段文本最大长度"),
    chunk_overlap: int = Form(20, description="知识库中相邻文本重合长度"),
):
    kb_path = os.path.join(KB_DIR,f"{kb_name}.faiss")
    kb_file_storage_path = os.path.join(FILE_STORAGE_DIR,kb_name)

    if not os.path.exists(kb_path):
        raise HTTPException(status_code=404,detail="Database not found")

    os.makedirs(kb_file_storage_path,exist_ok=True)
    updated_file = []
    for file in files:
        file_path = os.path.join(kb_file_storage_path,file.filename)
        file_content = file.file.read()
        with open(file_path,"wb") as f:
            f.write(file_content)

        loader = data_loader().get_loader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,separators=[
            "\n\n",
            "\n",
            " ",
            "."
            ","
            "。",
            "，",
            ""
        ],)
        chunks = text_splitter.split_documents(docs)
        vectorstore = FAISS.load_local(kb_path,embedding_model,allow_dangerous_deserialization=True)
        vectorstore.add_documents(chunks)
        vectorstore.save_local(kb_path)
        updated_file.append(file.filename)
    return {"message": f"File '{updated_file}' added to database '{kb_name}' successfully"}

@kb_router.post("/delete_docs")
async def delete_docs(
        file_names: List[str] = Body(..., examples=[["test.txt"]]),
        kb_name: str = Body(..., description="知识库名称"),
):
    kb_path = os.path.join(KB_DIR, f"{kb_name}.faiss")
    kb_file_storage_path = os.path.join(FILE_STORAGE_DIR, kb_name)

    # 检查知识库是否存在
    if not os.path.exists(kb_path):
        raise HTTPException(status_code=404, detail=f"知识库 {kb_name} 不存在")

    # 加载知识库
    vector_store = FAISS.load_local(kb_path, embedding_model,
                                    allow_dangerous_deserialization=True)

    failed_files = {}
    success_files = []
    for file_name in file_names:
        file_path = os.path.join(kb_file_storage_path, file_name)
        # 检查文件是否存在
        if not os.path.exists(file_path):
            failed_files[file_name] = f"未找到文件 {file_name}"
            continue

        # 尝试删除文件
        try:
            os.remove(file_path)
            ids = [
                k
                for k, v in vector_store.docstore._dict.items()
                if v.metadata.get("source").lower() == file_path.lower()
            ]
            if len(ids) > 0:
                vector_store.delete(ids)
                success_files.append(file_name)
            else:
                failed_files[file_name] = f"文件 {file_name} 在向量存储中找不到"
        except Exception as e:
            failed_files[file_name] = str(e)

    # 保存更新后的向量存储
    try:
        vector_store.save_local(kb_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存向量存储时出错: {str(e)}")

    response = {
        "success": success_files,
        "failed": failed_files
    }

    return response


@kb_router.post("/search_kb")
async def search_kb(
        kb_name: str = Body(..., description="知识库名称"),
        query: str = Body(..., description="问题")

):
    kb_path = os.path.join(KB_DIR, f"{kb_name}.faiss")

    if not os.path.exists(kb_path):
        raise HTTPException(status_code=404, detail="Database not found")

    # 加载知识库
    vector_store = FAISS.load_local(kb_path, embedding_model,
                                    allow_dangerous_deserialization=True)

    # 使用 FAISS 进行相似度检索
    faiss_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    docs = list(vector_store.docstore._dict.values())

    bm25_retriever = BM25Retriever.from_documents(
        docs,
        preprocess_func=jieba.lcut_for_search,
    )
    bm25_retriever.k = 2  # 设置 BM25 检索器返回的文档数量

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
    )

    contexts = ensemble_retriever.invoke(query)

    contexts = {
        "results": [{"sources": context.metadata.get("source", ""), "page_contents": context.page_content} for context
                    in contexts],
    }
    return contexts
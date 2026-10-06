# uvicorn + FastAPI 连接前端与后端
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #获取前端许可
from chat.chat_routes import chat_router #chatAPI(各种功能的接口)
from knowledgebase_server.kb_routes import kb_router #RAG：向量化+向量数据库+混合检索
from fastapi.staticfiles import StaticFiles #上传文件、图片等本地路径（静态路由）
from configs.setting import MEDIA_DIR #获取图像路径

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#挂载路由
app.include_router(chat_router)
app.include_router(kb_router)

app.mount("/media",StaticFiles(directory=MEDIA_DIR),name="media")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=6605,log_level="info") #仅允许本机访问，打印日志信息

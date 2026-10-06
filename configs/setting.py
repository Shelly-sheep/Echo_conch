chat_model_name = "Qwen/Qwen2.5-7B-Instruct"
api_key = "sk-yjjxzctudycwysxmbgsrtnalelpudblbdwrmjusvneaayzvc"
base_url = "https://api.siliconflow.cn/v1"

embedding_model_path = "./models/AI-ModelScope/bge-large-zh-v1___5"

#保存数据库的路径
KB_DIR = "./knowledgebases"
TEMP_KB_DIR = "./temp/knowledgebases"

# 存储文件的路径
FILE_STORAGE_DIR = "./data"
TEMP_FILE_STORAGE_DIR = "./temp/data"

# 知识库信息数据库的路径
SQLALCHEMY_DATABASE = "./db_server/data/"
# 知识库信息数据库的URI
SQLALCHEMY_DATABASE_URI = "sqlite:///./db_server/data/info.db"

# 设置超时
TIME_OUT = 60

# 媒体文件保存路径
MEDIA_DIR = "./temp/medias"
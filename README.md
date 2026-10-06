# 回音海螺 Echo Conch

> 🐚 把你的问题都抛给海螺吧，它会带给你答案。

回音海螺是一个**轻量化智能体**，基于传统 **ReAct（Reasoning + Acting）** 框架构建，能够自动判断任务需求，灵活调用工具，为你提供精准、可靠的回答。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🧠 **ReAct 框架** | 遵循经典的推理-行动循环，让模型边思考边行动 |
| 🛠️ **智能工具选择** | 自动识别是否需要联网搜索、是否调用知识库，无需手动切换 |
| 🌤️ **天气工具** | 查询实时天气信息 |
| ⏰ **时间工具** | 获取当前时间与日期 |
| 📚 **RAG 混合检索** | 融合 **FAISS**（向量检索）与 **BM25**（关键词检索）的混合检索方案，兼顾语义与关键词匹配 |
| 🤖 **QWEN2.5-7B 大模型** | 接入通义千问 2.5-7B 作为核心推理引擎 |
| 🎨 **Gradio 前端** | 基于 Gradio 构建交互界面，开箱即用 |

---

## 📦 环境安装

### 1. 克隆项目

```bash
git clone https://github.com/Shelly-sheep/Echo_conch.git
cd Echo_conch
```

### 2. 安装依赖

建议使用 Conda 创建独立环境：

```bash
conda create -n echo_conch python=3.10
conda activate echo_conch
```

然后安装所有前置库：

```bash
acres==0.2.0
aiofiles==23.2.1
aiohappyeyeballs==2.4.6
aiohttp==3.11.12
aiosignal==1.3.2
altair==5.5.0
analytics-python==1.4.post1
annotated-types==0.7.0
anyio==4.8.0
asttokens==3.0.0
attrs==25.1.0
backoff==1.10.0
bcrypt==4.2.1
beautifulsoup4==4.13.3
blinker==1.9.0
bokeh==3.6.3
certifi==2025.1.31
cffi==1.17.1
charset-normalizer==3.4.1
ci-info==0.3.0
click==8.1.8
codeboxapi==0.2.5
colorama==0.4.6
comm==0.2.2
configobj==5.0.9
configparser==7.1.0
contourpy==1.3.1
cryptography==44.0.1
cycler==0.12.1
dash==2.18.2
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-table==5.0.0
dataclasses-json==0.6.7
debugpy==1.8.12
decorator==5.1.1
distro==1.9.0
dnspython==2.7.0
email_validator==2.2.0
et_xmlfile==2.0.0
etelemetry==0.3.1
executing==2.2.0
faiss-cpu==1.9.0
fastapi==0.112.2
fastapi-cli==0.0.7
ffmpy==0.5.0
filelock==3.17.0
fitz==0.0.1.dev2
Flask==3.0.3
fonttools==4.56.0
frontend==0.0.3
frozendict==2.4.6
frozenlist==1.5.0
fsspec==2025.2.0
gradio==4.44.1
gradio_client==1.3.0
greenlet==3.1.1
h11==0.14.0
httpcore==1.0.7
httplib2==0.22.0
httptools==0.6.4
httpx==0.27.0
httpx-sse==0.4.0
huggingface-hub==0.29.0
idna==3.10
importlib_metadata==8.6.1
importlib_resources==6.5.2
ipykernel==6.29.5
ipython==8.32.0
isodate==0.6.1
itsdangerous==2.2.0
jedi==0.19.2
jieba==0.42.1
Jinja2==3.1.5
jiter==0.8.2
joblib==1.4.2
jsonpatch==1.33
jsonpointer==3.0.0
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
jupyter_client==8.6.3
jupyter_core==5.7.2
kiwisolver==1.4.8
langchain==0.3.7
langchain-community==0.3.5
langchain-core==0.3.15
langchain-openai==0.2.5
langchain-text-splitters==0.3.2
langsmith==0.1.147
linkify-it-py==2.0.3
looseversion==1.3.0
lxml==5.3.1
markdown-it-py==3.0.0
MarkupSafe==2.1.5
marshmallow==3.26.1
matplotlib==3.10.0
matplotlib-inline==0.1.7
mdit-py-plugins==0.4.2
mdurl==0.1.2
monotonic==1.6
mpmath==1.3.0
multidict==6.1.0
multitasking==0.0.11
mypy-extensions==1.0.0
narwhals==1.27.1
nest-asyncio==1.6.0
networkx==3.4.2
nibabel==5.3.2
nipype==1.9.2
numpy==1.26.4
openai==1.53.0
openpyxl==3.1.5
orjson==3.10.15
packaging==24.2
pandas==2.2.3
paramiko==3.5.1
parso==0.8.4
pathlib==1.0.1
patsy==1.0.1
peewee==3.17.9
pillow==10.4.0
platformdirs==4.3.6
plotly==6.0.0
prompt_toolkit==3.0.50
propcache==0.2.1
prov==2.0.1
psutil==7.0.0
pure_eval==0.2.3
puremagic==1.28
pycparser==2.22
pycryptodome==3.21.0
pydantic==2.9.2
pydantic-settings==2.7.1
pydantic_core==2.23.4
pydot==3.0.4
pydub==0.25.1
Pygments==2.19.1
PyNaCl==1.5.0
pyparsing==3.2.1
python-dateutil==2.9.0.post0
python-docx==1.1.2
python-dotenv==1.0.1
python-multipart==0.0.20
pytz==2025.1
pywin32==308
pyxnat==1.6.3
PyYAML==6.0.2
pyzmq==26.2.1
rdflib==6.3.2
referencing==0.36.2
regex==2024.11.6
requests==2.32.3
requests-toolbelt==1.0.0
retrying==1.3.4
rich==13.9.4
rich-toolkit==0.13.2
rpds-py==0.22.3
ruff==0.9.6
scikit-learn==1.6.1
scipy==1.15.2
seaborn==0.13.2
semantic-version==2.10.0
shellingham==1.5.4
simplejson==3.20.1
six==1.17.0
sniffio==1.3.1
soupsieve==2.6
SQLAlchemy==2.0.35
stack-data==0.6.3
starlette==0.38.6
statsmodels==0.14.4
sympy==1.13.3
tenacity==9.0.0
threadpoolctl==3.5.0
tiktoken==0.9.0
tomlkit==0.12.0
tornado==6.4.2
tqdm==4.67.1
traitlets==5.14.3
traits==7.0.2
typer==0.15.1
typing-inspect==0.9.0
typing_extensions==4.12.2
tzdata==2025.1
uc-micro-py==1.0.3
urllib3==2.3.0
uv==0.6.2
uvicorn==0.20.0
watchfiles==1.0.4
wcwidth==0.2.13
websockets==11.0.3
Werkzeug==3.0.6
xyzservices==2025.1.0
yarl==1.18.3
yfinance==0.2.54
zipp==3.21.0
```

> 核心依赖包括：`gradio`、`langchain`、`faiss-cpu`、`openai`、`jieba`、`pandas`、`numpy` 等。

---

## 🚀 快速开始

安装完成后，直接运行主程序：

```bash
python app_server.py
```

浏览器会自动打开 Gradio 界面，开始与海螺对话吧！

---

## ⚙️ 端口配置

> ⚠️ **注意：项目默认使用 `6605` 端口**，若端口被占用，请修改配置文件中的端口号。

例如在 `app.py` 中找到：

```python
demo.launch(server_port=6605)
```

修改为其他可用端口，如：

```python
demo.launch(server_port=7860)
```

---

## 🧩 项目架构

```
Echo_conch/
├── app.py                 # 主入口，Gradio 界面
├── requirements.txt       # 依赖库列表
├── README.md              # 项目说明
├── agent/                 # 智能体核心逻辑（ReAct 框架）
│   ├── react_agent.py     # ReAct 推理循环
│   └── tools.py           # 工具定义（联网/知识库/天气/时间）
├── rag/                   # RAG 检索模块
│   ├── faiss_retriever.py # FAISS 向量检索
│   ├── bm25_retriever.py  # BM25 关键词检索
│   └── hybrid_retriever.py# 混合检索融合
└── models/                # 模型配置
    └── qwen.py            # QWEN2.5-7B 接入
```

---

## 🛠️ 工具说明

| 工具 | 功能 | 触发场景 |
|------|------|----------|
| 🔍 **联网搜索** | 实时搜索互联网信息 | 用户询问新闻、实时数据、最新事件等 |
| 📖 **知识库检索** | 从本地知识库中检索相关内容 | 用户询问领域知识、历史文档等 |
| 🌤️ **天气查询** | 获取指定城市的天气情况 | 用户询问天气、温度、降雨等 |
| ⏰ **时间查询** | 获取当前日期和时间 | 用户询问“现在几点”“今天几号”等 |

智能体根据用户问题**自动判断**需要调用哪些工具，无需手动指定。

---

## 📄 License

MIT License

---

## 👥 贡献

欢迎提交 Issue 和 Pull Request，一起让海螺变得更聪明！

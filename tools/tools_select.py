from langchain_core.tools import Tool,StructuredTool
from tools.code_interpreter import code_interpreter
from tools.weather_check import weather_check
from tools.web_search import web_search
from tools.knowledge_search import knowledgebas_search
from tools.get_time import get_time

tools = [
    Tool(
        name = "weather check",
        func = weather_check.run,
        description = "获取当前地点或指定城市的实时天气信息，包括温度、天气状况等。"
    ),

    Tool(
        name="web search",
        func=web_search.run,
        description="通过网络搜索获取最新资讯、回答问题或查找特定主题的相关内容。"
    ),

    Tool(
        name="knowledge search",
        func=knowledgebas_search.run,
        description="搜索本地知识库，获取与特定主题相关的内容。此工具的输入应是一个由 ',' 分隔的两个字符串，第一个字符串表示您需要查询的知识库，第二个字符串表示您需要查询的问题。例如，您想要在 '人工智能' 知识库查询关于 '人工智能学习方法' ，输入应为 '人工智能,人工智能学习方法' 。"
    ),

    Tool(
        name="get time",
        func=get_time.run,
        description="获取当前时间。输入应始终为空字符串"
    ),

    Tool(
        name="code interpreter",
        func=code_interpreter.run,
        description="一个Python shell。使用它来执行python代码。输入应该是一个有效的python代码字符串。在与开头引号相同的行开始编写代码。不要以换行开始你的代码。"
    ),
]
import requests
from pydantic import Field
from configs.setting import TIME_OUT

class WebSearch:
    query: str = Field(description="需要联网查找的内容")

    def __init__(self,api_key):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
        
    def run (self,query):
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "baidu",
            "rn": 5
        }

        try:
            # 发送请求到网络搜索API
            resp = requests.get(self.base_url, params=params, timeout=TIME_OUT)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return f"联网搜索请求失败：{e}"

        # 优先用 ai_overview 百度页面开头的AI摘要
        blocks = []
        for block in data.get("ai_overview", {}).get("text_blocks", []):
            if block.get("snippet"):
                blocks.append(block["snippet"])

        # organic_results
        lines = []
        for r in data.get("organic_results", []):
            title = r.get("title", "")
            link = r.get("link", "")
            snippet = r.get("snippet") or r.get("desc") or ""

            # 过滤百度和 serpapi 内部链接
            if "baidu.com/link" in link or "serpapi.com" in link:
                continue

            lines.append(f"标题：{title}\n链接：{link}\n摘要：{snippet}")

        text = "\n\n".join(lines)

        if blocks:
            text = "【AI 概览】\n" + "\n".join(blocks) + "\n\n【搜索结果】\n" + text

        return text if text.strip() else "没有找到有效网页结果"

web_search = WebSearch("e63e7106b83e89b540cd719e471ca039dde7f14416881933b47cc6f855f24922")
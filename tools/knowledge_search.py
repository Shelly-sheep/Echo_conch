import json
import requests
from pydantic import Field
from configs.setting import TIME_OUT

class KnowledgeBaseSearch:
    input:str = Field(description="包含知识库名称和需要查询问题的字符串")

    def run(self,inputs):
        kb_name , query = inputs.split(",")
        url = "http://127.0.0.1:6605/knowledgebase/search_kb"

        data = {
            "kb_name": kb_name,
            "query": query
        }

        json_data = json.dumps(data)
        headers = {
            'Content-Type':'application/json'
        }
        response = requests.post(url,data=json_data,headers=headers,timeout=TIME_OUT)

        if response.status_code == 200:
            data = response.json()
            res = "".join([f"source:\n{d['sources']} \ncontext:\n{d['page_contents']}\n" for d in data['results']])
            return res
        else:
            return f"无法获取和{query}有关信息"

knowledgebas_search = KnowledgeBaseSearch()
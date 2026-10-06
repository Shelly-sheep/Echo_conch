from datetime import datetime

class Get_time:
    def run(self,text:str):
        # 获取当前时间，格式为 年-月-日 小时:分钟:秒
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_time

get_time = Get_time()
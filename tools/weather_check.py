import requests
from pydantic import Field
from configs.setting import TIME_OUT

class WeatherCheck:
    city:str = Field(description="City name,include city and county")

    def __init__(self,api_key):
        self.api_key = api_key

    def run(self,city):
        city = city.split('\n')[0]
        url = f"https://api.seniverse.com/v3/weather/now.json?key={self.api_key}&location={city}&language=zh-Hans&unit=c"
        response = requests.get(url,timeout=TIME_OUT)

        if response.status_code == 200:
            data =response.json()
            weather = data['results'][0]['now']['text']
            temperature = data['results'][0]['now']['temperature']
            return f"{city}的天气是{weather}，温度为摄氏度{temperature}"
        else:
            return f"错误码:{response.status_code},无法获取{city}的天气信息"

weather_check = WeatherCheck("SiVObz9XPg4pFO4rL")
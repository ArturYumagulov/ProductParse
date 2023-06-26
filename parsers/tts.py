import requests
from environs import Env

from config.config_data import TTS_CONF

headers = {
    "Accept": "application/json",
    "Content-type": "application/json"
}

env = Env()
Env().read_env()

url = f"{TTS_CONF['url']}/search/articles/?" \
      f"userlogin={env('TTS_LOGIN')}&" \
      f"userpsw={env('TTS_PASSWORD')}&" \
      f"number=w914/2&" \
      f"brand=MANN-FILTER"


r = requests.get(url, headers)

result_list = r.json()
for item in result_list:
    if item['brand'] == "MANN-FILTER":
        print(item)


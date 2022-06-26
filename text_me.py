import requests
import json

with open ("kakao_code.json", "r") as f:
    token_data = json.load(f)

url = "https://kapi.kakao.com/v2/api/talk/memo/send"

headers = {
    "Authorization": "Bearer " + token_data['access_token']
    }


data = {
    "template_id" : 78766
}

response = requests.post(url, headers=headers, data=data)
if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
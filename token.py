import requests
import json

import config

client_id = config.kakao["rest_api_key"]
redirect_uri = config.kakao["redirect_uri"]
code = config.kakao["code"]

with open("token.json", 'r') as kakao:
    token_data = json.load(kakao)

def get_token():
    # 카카오톡 메시지 API
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "authorization_code",
        "client_id" : client_id,
        "redirect_url" : redirect_uri,
        "code" : code
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

    # token.json 파일 저장
    with open("token.json", "w") as kakao:
        json.dump(tokens, kakao)

def print_token_info():
    url = "https://kapi.kakao.com/v1/user/access_token_info"

    headers = {
        "Authorization": "Bearer " + token_data['access_token']
    }
    response = requests.get(url, headers=headers)
    token_info = response.json()
    print(token_info)

def refresh_token():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "refresh_token",
        "client_id" : client_id,
        "refresh_token" : token_data['refresh_token']
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("token_refreshed.json", "w") as kakao:
        json.dump(tokens, kakao)
        
if __name__ == "__main__":
    # print_token_info()
    refresh_token()
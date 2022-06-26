import requests
import json

import config

# 카카오톡 메시지 API
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : config.kakao["rest_api_key"],
    "redirect_url" : "https://localhost:3000",
    "code" : "2XiKhxXXumwjT4VR5447-ZFCQik_R-wW3AXZlAqTKkwX-ZN9Dt4RswQZVHct_feXOzIPqwo9dRoAAAGBnoTgVg"
}
response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# kakao_code.json 파일 저장
with open("kakao_code.json", "w") as fp:
    json.dump(tokens, fp)
import requests
import json
import time

def send_msg(data):
    with open ("token.json", "r") as kakao:
        token_data = json.load(kakao)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + token_data['access_token']
        }

    response = requests.post(url, headers=headers, data={'template_object': json.dumps(data)})
    now = time.localtime()
    time_msg = "%04d/%02d/%02d %02d:%02d:%02d - " % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    if response.json().get('result_code') == 0:
        print(time_msg + '메시지를 성공적으로 보냈습니다.')
    else:
        print(time_msg + '메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

# title, description(time), web_url
def send_msg_top3(data_list, num) :   # data_list : [title, url, time]
    contents = []
    header_title = "공지사항" if num == 1 else "소식"
    for i in range(3):
        contents.append({
            "title": data_list[0][i],
            "description": data_list[2][i],
            "image_url": "",
            "link" : {
                "web_url" : data_list[1][i],
                "mobile_web_url": data_list[1][i],
                "android_execution_params": data_list[1][i],
                "ios_execution_params": data_list[1][i]
            }
        }
    )
    data = {
       "object_type": "list",
        "header_title": "KHU sw사업단 " + header_title,
        "header_link": {
            "web_url": "http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01",
            "mobile_web_url": "http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01",
            "android_execution_params": "main",
            "ios_execution_params": "main"
        },
        "contents": contents,
        "buttons": [
            {
                "title": "사업단 홈페이지로 이동",
                "link": {
                    "web_url": "http://swedu.khu.ac.kr",
                    "mobile_web_url": "http://swedu.khu.ac.kr"
                }
            },
        ]
    }
    send_msg(data)

# send recent notice or news
def send_msg_new(recent_data, num):
    text = "공지사항" if num == 1 else "사업단 소식"
    data = {
        "object_type": "text",
        "text": "새로운 " + text + "이 올라왔어요!\n" + "\'{}\'".format(recent_data['title']),
        "link": {
            "web_url": recent_data['url'],
            "mobile_web_url": recent_data['url']
        },
        "button_title": "바로 확인"
    }
    send_msg(data)

if __name__ == "__main__":
    data = {
        "object_type": "text",
        "text": "kakao talk message test",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    send_msg(data)
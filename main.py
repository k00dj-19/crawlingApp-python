import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from bs4 import BeautifulSoup
import schedule
import time
import requests
import json

import config

'''
    매일 특정시간에 실행하여 공지사항에 변경사항이 있을 경우 카톡으로 알림을 보낸다.
'''
### kakao login ###

client_id = config.kakao["rest_api_key"]
redirect_uri = config.kakao["redirect_uri"]
code = config.kakao["code"]

def kakao_auth():
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
    return tokens["refresh_token"]

def kakao_auth_refresh(r_token):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "refresh_token",
        "client_id" : client_id,
        "refresh_token" : r_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    
    with open("token.json", "w") as kakao:
        json.dump(tokens, kakao)

    return tokens["access_token"]

def print_token_info():
    with open("token.json", 'r') as kakao:
        token_data = json.load(kakao)

    url = "https://kapi.kakao.com/v1/user/access_token_info"

    headers = {
        "Authorization": "Bearer " + token_data['access_token']
    }
    response = requests.get(url, headers=headers)
    token_info = response.json()
    print(token_info)


### crawling ###    

recent_notice = {
    'title' : "",
    'url' : ""
}

recent_news = {
    'title' : "",
    'url' : ""
}

# url을 html 형식으로 반환
def download(url):
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print("Download error", e.reason)
        html = None
    return html

# 상위 3개 글 제목과 url, time 리스트 반환
def find_top3(html):
    soup = BeautifulSoup(html, "html.parser")
    url_list, title_list, time_list = [], [], []
    # crawling title and url
    target = soup.select(".bo_tit > a")
    for i in target[:3]:
        url_list.append(i["href"])
        title_list.append(i.string.strip())

    # crwling time
    target = soup.select(".td_datetime")
    time_list = [t.string for t in target[:3]]
    data_list = [title_list, url_list, time_list]
    return data_list

# 맨 첫번째 글 제목과 url 반환
def find_first(html):
    soup = BeautifulSoup(html, "html.parser")
    target = soup.find(class_="bo_tit").find("a")
    url = target["href"]
    title = target.string.strip()
    return title, url

# 가장 상위의 공지사항이 변경되었는지 확인
# 변경 되었으면 카톡 메시지로 알림
def check_recent_notice(url):
    global recent_notice
    title, url = find_first(download(url))
    #print(recent_notice)
    if recent_notice['title'] != title:
        recent_notice['title'], recent_notice['url'] = title, url
        send_msg_new(recent_notice,1)

# 가장 상위의 사업단 소식이 변경되었는지 확인
def check_recent_news(url):
    global recent_news
    title, url = find_first(download(url))
    #print(recent_news)
    if recent_news['title'] != title:
        recent_news['title'], recent_news['url'] = title, url
        send_msg_new(recent_news,2)

def send_notice(data_list):
    send_msg_top3(data_list,1)

def send_news(data_list):
    send_msg_top3(data_list,2)



### send messgage ###

def send_msg(data, msg):
    with open("token.json", 'r') as kakao:
        token_data = json.load(kakao)
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + token_data["access_token"]
    }
    response = requests.post(url, headers=headers, data={'template_object': json.dumps(data)})
    now = time.localtime()
    time_msg = "%04d/%02d/%02d %02d:%02d:%02d - " % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    if response.json().get('result_code') == 0:
        print(time_msg + msg + '메시지를 성공적으로 보냈습니다.')
    else:
        print(time_msg + '메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

# title, description(time), web_url
def send_msg_top3(data_list, num) :   # data_list : [title, url, time]
    contents = []
    header_title = "공지사항" if num == 1 else "소식"

    for i in range(len(data_list[0])):
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
    send_msg(data, header_title)

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
    send_msg(data, "new" + text)

def send_msg_test():
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


if __name__ == "__main__":
    url_notice = 'http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01'
    url_news = 'http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_03'
    notice_data_list = find_top3(download(url_notice))
    news_data_list = find_top3(download(url_news))

    r_token = kakao_auth()
    a_token = schedule.every(6).hours.do(kakao_auth_refresh, r_token)
    schedule.every(1).hours.do(send_notice, notice_data_list)
    schedule.every(1).hours.do(send_news, news_data_list)
    schedule.every(1).hours.do(check_recent_notice, url_notice)
    schedule.every(1).hours.do(check_recent_news, url_news)

    #schedule.every().day.at("15:30:00").do(send_notice, url_notice)
    #schedule.every().day.at("15:32:00").do(send_notice, url_notice)
    while True:
        schedule.run_pending()
        time.sleep(1)
from turtle import done, down
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from bs4 import BeautifulSoup
import schedule
import time

import message

'''
    매일 12시, 18시에 실행하여 공지사항에 변경사항이 있을 경우 카톡으로 알림을 보낸다.
'''
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
    print(recent_notice)
    if recent_notice['title'] != title:
        recent_notice['title'], recent_notice['url'] = title, url
        message.send_msg_new(recent_notice,1)

# 가장 상위의 사업단 소식이 변경되었는지 확인
def check_recent_news(url):
    global recent_news
    title, url = find_first(download(url))
    print(recent_news)
    if recent_news['title'] != title:
        recent_news['title'], recent_news['url'] = title, url
        message.send_msg_new(recent_news,2)

def send_notice(url):
    data_list = find_top3(url)
    message.send_msg_top3(data_list,1)

def send_news(url):
    data_list = find_top3(url)
    message.send_msg_top3(data_list,2)

if __name__ == "__main__":
    url_notice = 'http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01'
    url_news = 'http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_03'
    # schedule.every(2).minutes.do(send_notice, notice_data)
    schedule.every().day.at("12:00:00").do(check_recent_notice, url_notice)
    schedule.every().day.at("18:00:00").do(check_recent_notice, url_notice)
    schedule.every().day.at("12:00:00").do(check_recent_news, url_news)
    schedule.every().day.at("09:00:00").do(send_notice, url_notice)
    schedule.every().day.at("12:00:00").do(send_notice, url_notice)
    schedule.every().day.at("15:00:00").do(send_notice, url_notice)
    schedule.every().day.at("18:00:00").do(send_notice, url_notice)
    while True:
        schedule.run_pending()
        time.sleep(1)
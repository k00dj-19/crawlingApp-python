import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import requests
from bs4 import BeautifulSoup

def download(url):
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print("Download error", e.reason)
        html = None
    return html

page = download('http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01&page=1')
soup = BeautifulSoup(page)
target_url = soup.find(class_="bo_tit").find("a")["href"]

print(target_url)
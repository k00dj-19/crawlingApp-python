import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import requests
import bs4

def download(url):
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print("Download error", e.reason)
        html = None
    return html

print(download('https://www.google.com'))
print("hello world")
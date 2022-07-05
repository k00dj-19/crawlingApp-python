from flask import Flask

app = Flask(__name__)

# 스킬 종류
# 공지사항 리스트 출력
# 사업단 소식 리스트 출력
# 새로운 공지사항/사업단 소식 올라오면 알림
@app.route("/ping", methods=['GET'])
def ping():
    return "pong"
# flask 패키지에서 Flask 클래스와 jsonify 함수를 가져온다
from flask import Flask, jsonify

# __name__ 이란 현재 실행되고 있는 모듈의 이름
# Flask 객체를 생성한다
app = Flask(__name__)

# 경로를 설정하고, 각 경로에 접근시 호출할 함수를 정의한다
#디폴트 경로로 접근시 문자열 'Welcome!' 을 반환한다.
@app.route('/')
def index():
    return 'Welcome!'

#/menu 경로로 접근시 HTML 소스를 반환한다.
@app.route('/menu') 
def menu():
    return '<h1>This page is menu</h1><button>버튼</button><p>paragraph</p>'

#/board 경로로 접근시 json 형식 데이터를 반환한다.
@app.route('/board')
def board():
    return jsonify(msg="This page is board", format="json")

#동적 URL
@app.route('/board/<idx>')
def board_idx(idx):
    return idx + "번째 게시글"

# 메인으로 실행되는 부분 
if __name__ == '__main__':
    app.run(port = 5000)

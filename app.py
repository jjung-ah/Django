# -*- coding: utf-8 -*

from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # register 주소에서 POST 요청이 들어왔을경우
    if request.method == 'POST':
        # form 태그에서 POST 방식으로 보낸 데이터는 request.form 으로 전달받는다
        data = request.form
        # print(data)

        if "cancel" in data:
            return redirect(url_for('index'))

        if (data['password'] != data['c_password']):
            # 템플릿의 notice_text 변수에 문자열 삽입 
            return render_template('register.html', notice_text = "비밀번호를 확인해주세요.")
        else:
            return redirect(url_for('index'))
    
    # register 주소에서 GET 요청이 들어왔을경우
    else:
        # GET 방식으로 보낸 데이터는 URL 자체에서 가져온다
        # data = request.args.get
        return render_template('register.html', notice_text = "")



@app.route('/deepbot', methods=['GET', 'POST'])
def deepbot():
    user = request.form['user']
    # pwd = request.form['p']
    return render_template('deepbot.html',user=user)
     

@app.route('/message', methods=['GET', 'POST'])
def chatting():
    # request
    message = request.json['message']
    return jsonify({'message' : message})


if __name__ == '__main__':
    app.run(port=5000)

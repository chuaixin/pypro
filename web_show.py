#!/usr/bin/python3
# filename  web_show.py

from flask import Flask,request,url_for,Response

#创建一个Flask对象
app = Flask(__name__)

@app.route('/login/')
def login():
    return Response('login ok')
@app.route('/')
def hello_world():
 return url_for('login', next='/')
    # /login/?next=/
    # 会自动的将/编码，不需要手动去处理。
    # url=/login/?next=%2F

if __name__ == '__main__':
    #默认为5000端口
    app.run(debug = True)
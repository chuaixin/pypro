#从flask包中导入Flask类
from flask import Flask,render_template

app = Flask(__name__)
@app.route('/')
def index():
   return "根目录"

@app.route('/pro/')
def indexpro():   
   return render_template('index.html',user = 'chuai')

#启动这个WEB服务
if __name__ == '__main__':
    #默认为5000端口
    app.run(debug=True)  


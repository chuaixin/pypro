#从flask包中导入Flask类
from flask import Flask,render_template,request

app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
   pwd = request.values.get('pwd')
   my_name = '测试一下cehnggong'+pwd
   return render_template('index.html', myname=my_name)

@app.route('/bootstrap-examples/album/')
def boot():
   return render_template('/bootstrap-examples/index.html')
   print("test ok")

#启动这个WEB服务
if __name__ == '__main__':
    #默认为5000端口
    app.run(debug=True)  


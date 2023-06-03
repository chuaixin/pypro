#!/usr/bin/python3
# filename  web_show.py

from flask import Flask,request,url_for,Response
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='007928',
    database='world',
    charset='utf8')
try:
    cur=conn.cursor()
    cur.execute('select * from country limit 10')
    res=cur.fetchall()
    for item in res:
        code
except Exception as ex:
    print(ex)
finally:
    cur.close()
    conn.close()

print()

response = item
#创建一个Flask对象
app = Flask(__name__)

@app.route('/login/')
def login():
    return "test"


if __name__ == '__main__':
    app.run(debug = True)


#!/usr/bin/python3
# filename  hello.py

#from PyMySQL import *
import pymysql

conn = connect(host='localhost',user='root',password='cx007928',database='hellodb',charset='utf8')

try:
    cur=conn.cursor()
    # insertsql=insert into TestModel_test(id,name) values ('','jimbo')

    cur.execute('select * from TestModel_test')
    # conn.commit()
    res=cur.fetchall()
    for item in res:
        print('ID;{0} name{1}'.format(item[1],item[3]))
    print(res)
    #print('sucess')
except Exception as ex:
    print(ex)
finally:
    cur.close()
    conn.close()

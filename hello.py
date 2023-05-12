#!/usr/bin/python3
# filename  hello.py
#from PyMySQL import

import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='cx007928',
    database='hellodb',
    charset='utf8')

try:
    cur=conn.cursor()
    # insertsql=insert into TestModel_test(id,name) values ('','jimbo')
    createsql = '''
        CREATE TABLE `entries` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `title` varchar(12) NOT NULL,
            `text` varchar(12) NOT NULL DEFAULT '请输入',
            PRIMARY KEY (`id`)
        );'''

    cur.execute( createsql )
    # conn.commit()

    print ("create ok")
    #print('sucess')
except Exception as ex:
    print(ex)
finally:
    cur.close()
    conn.close()

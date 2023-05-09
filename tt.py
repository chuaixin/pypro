#!/usr/bin/python3
# filename  hello.py

import pymysql
 
# 连接数据库，创建连接对象connection
# 连接对象作用是：连接数据库、发送数据库信息、处理回滚操作（查询中断时，数据库回到最初状态）、创建新的光标对象
 
conn = pymysql.connect(
    host='192.168.95.170',
    user='khan2_pro',
    password='khan2_pro',
    database='khan2_pro',
    charset='utf8')
 
# 执行完毕返回的结果集默认以元组显示 
sql = "select * from kh_project limit 10"

# 执行SQL语句
# 查询语句
try:
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for data in result:
        print(data)
except Exception:
    print("查询失败")

# 关闭光标对象
cursor.close()
 
# 关闭数据库连接
conn.close()
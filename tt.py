 
import pymysql
 
# 连接数据库，创建连接对象connection
# 连接对象作用是：连接数据库、发送数据库信息、处理回滚操作（查询中断时，数据库回到最初状态）、创建新的光标对象
 
conn = pymysql.connect(host='127.0.0.1',  # host属性
                       port=3306,  # 端口号
                       user='root',  # 用户名
                       password='007928',  # 此处填登录数据库的密码
                       db='world' , # 数据库名
                       charset="utf8"
                       )
 
# 执行完毕返回的结果集默认以元组显示 
sql = "select * from country limit 10"

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
#!/usr/bin/python3
# coding=utf-8
# filename  hello.py

import sys
print(sys.version)
import pymysql
 
# 连接数据库，创建连接对象connection
# 连接对象作用是：连接数据库、发送数据库信息、处理回滚操作（查询中断时，数据库回到最初状态）、创建新的光标对象
conn = pymysql.connect(
    host='192.168.95.170',
    user='khan2_pro',
    password='khan2_pro',
    database='khan2_pro',
    charset='utf8')

#部门信息配置
dept = ('数字化运营事业部','智能运营事业部','云网运营事业部','技术中台支撑部','通信运营事业部','短信业务支撑部')

# 按部门查询系统项目数 
# sql = "select dept_name,count(*) from kh_project where category=1 GROUP BY dept_name"

# 按部门查询系统项目数
# sql = "select dept_name,count(*) from kh_project where category=2 GROUP BY dept_name"

# 执行SQL语句
# try:
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     for data in result:
#         print(data)
# except Exception:
#     print("查询失败")
# ====================================
# 查询产品代码库入库量
'''
for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=2 and dept_name='%s'" %dept_rep 
    dept_rep_y = 0
    dept_rep_n = 0
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        for data in result:
            sql_sc_repository_id = "select count(repository_id) from kh_project__repository where project_id=%s" % data[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchone()
            if(result_repository[0]):
                dept_rep_y += 1
            else:
                dept_rep_n += 1  
            #print(data[0],result_repository[0])
    except Exception:
        print("查询失败")
    print(data[0],"代码库项目数",dept_rep_y,"无代码库项目数",dept_rep_n)
'''
# ====================================
# 查询系统代码库入库量
'''
for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=1 and dept_name='%s'" %dept_rep 
    dept_rep_y = 0
    dept_rep_n = 0
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        for data in result:
            sql_sc_repository_id = "select count(repository_id) from kh_project__repository where project_id=%s" % data[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchone()
            if(result_repository[0]):
                dept_rep_y += 1
            else:
                dept_rep_n += 1  
            # print(data[0],result_repository[0])
    except Exception:
        print("查询失败")
    print(data[0],"代码库项目数",dept_rep_y,"无代码库项目数",dept_rep_n)
'''
# ====================================
# 查询系统是否已做关联产品
# for dept_rep in dept:
#     sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=1 and dept_name='%s'" %dept_rep 
#     dept_rep_y = 0
#     dept_rep_n = 0
#     # 执行SQL语句
#     try:
#         cursor = conn.cursor()
#         cursor.execute(sql_sc_project_id)
#         result = cursor.fetchall()
#         for data in result:
#             sql_sc_repository_id = "select count(depend_project_id) from kh_project_dependency where project_id=%s" % data[2]
#             cursor.execute(sql_sc_repository_id)
#             result_repository = cursor.fetchone()
#             if(result_repository[0]):
#                 dept_rep_y += 1
#             else:
#                 dept_rep_n += 1  
#             # print(data[0],result_repository[0])
#     except Exception:
#         print("查询失败")
#     print(data[0],"已关联产品系统数",dept_rep_y,"未关联产品系统数",dept_rep_n)


# ====================================
# 查询各项目任务创建数
'''
for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=1 and dept_name='%s'" %dept_rep #系统项目
    # sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=2 and dept_name='%s'" %dept_rep #产品项目
    dept_rep_y = 0
    dept_rep_n = 0
    sum_job = 0
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        for data in result:
            sql_sc_repository_id = "select count(*) FROM kh_project_function where project_id=%s AND create_time>'2023-04-01'" % data[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchone()
            if(result_repository[0]):
                dept_rep_y += 1
                sum_job += result_repository[0]
            else:
                dept_rep_n += 1  
            # print(data[0],data[1],result_repository[0])
    except Exception:
        print("查询失败")
    print(data[0],"有任务系统数",dept_rep_y,"未发任务系统数",dept_rep_n,"任务数总量",sum_job)
'''

# ====================================
# 查询各项目代码提交数据

for dept_rep in dept:
    # sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=1 and dept_name='%s'" %dept_rep #系统项目
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=2 and dept_name='%s'" %dept_rep #产品项目
    dept_rep_y = 0 #部门项目有效计数器
    dept_rep_n = 0 #部门项目无效计数器
    commit_pro = 0
    commit_pro_no = 0
    project_sum_commit = 0
    sum_commit = 0 #提交总数计数器
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        #通过project_id查询项目的代码库id
        for data in result:
            sql_sc_repository_id = "select repository_id from kh_project__repository where project_id = %s" % data[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchall()
            #通过代码库id查询提交代码次数
            for reps_id in result_repository:
                sql_sc_repository_commit = "select count(*) from kh_gitlab_statistical_commits where repository_id=%s AND committer_time>'2023-04-01'" % reps_id[0]
                cursor.execute(sql_sc_repository_commit)
                result_commit = cursor.fetchone()
                project_sum_commit+=result_commit[0]
            if(project_sum_commit):
                commit_pro+=1
            else:
                commit_pro_no+=1
            #按项目计数清零，累加到部门总提交量    
            sum_commit += project_sum_commit

            project_sum_commit = 0
            dept_rep_y += commit_pro
            dept_rep_n += commit_pro_no
            commit_pro = 0
            commit_pro_no = 0

        print(dept_rep,"提交项目数",dept_rep_y,'未提交项目数',dept_rep_n,'总代码提交次数',sum_commit)

    except Exception:
        print("查询失败")



# 关闭光标对象
cursor.close()
 
# 关闭数据库连接
conn.close()
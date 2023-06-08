#!/usr/bin/python3
# coding=utf-8
# filename  effective_stat.py

import pymysql
import sys
 
# 连接数据库，创建连接对象connection
conn = pymysql.connect(
    host='192.168.95.170',
    user='khan2_pro',
    password='khan2_pro',
    database='khan2_pro',
    charset='utf8')

#部门信息配置
dept = ('数字化运营事业部','智能运营事业部','云网运营事业部','技术中台支撑部','通信运营事业部','短信业务支撑部')

#部门信息配置
deptdict = {'数字化运营事业部':'szhyy','智能运营事业部':'znyy','云网运营事业部':'ywyy','技术中台支撑部':'jszt','通信运营事业部':'txyy','短信业务支撑部':'dxyw'}

# 按部门查询系统项目数 
print("\n【按部门查询系统项目数】：\n==============================================")
sql_sys = "select dept_name,count(*) from kh_project where category=1 and (status=1 or status=2) GROUP BY dept_name"
try:
    cursor = conn.cursor()
    cursor.execute(sql_sys)
    result = cursor.fetchall()
    for data in result:
        print("部门:",data[0],"系统项目数：",data[1])
except Exception:
    print("查询失败")

# 按部门查询系统项目数
print("\n【按部门查询产品项目数】：\n ==============================================")
sql_pro = "select dept_name,count(*) from kh_project where category=2 and (status=1 or status=2) GROUP BY dept_name"
try:
    cursor = conn.cursor()
    cursor.execute(sql_pro)
    result = cursor.fetchall()
    for data in result:
        print("部门:",data[0],"产品项目数：",data[1])
except Exception:
    print("查询失败")


# ====================================
#待迁移项目
print("\n【查询所有待迁移代码库项目明细】：\n ==============================================")
removelist = (1083,1028,461,1160,997,1033,996,858,1024,793,1037,1014,1013,994,1045,985,839,1017,1003,1100,1097,1103,1110,1108,1106,316,1093,296)
for removdata in removelist:
    sql_sc_project_id = "select dept_name,name,project_key,id,liable_user_name from kh_project where id ='%s'" %removdata
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchone()
        print (result[0],"\t",result[1],"\t",result[2],"\t",result[3],"\t",result[4])
    except Exception as ex:
        print(ex)


# ====================================
# 查询新产品代码库入库量
newproduct = {
    "Ultra-CMP":"混合多云管理平台",
    "Ultra-CNBP":"算网大脑平台",
    "Ultra-Leopard":"猎豹智云平台",
    "Ultra-Matrix":"配置管理矩阵",
    "Ultra-BI":"数析展示工具",
    "Ultra-CNB":"集约化综合网管",
    "Ultra-BPC":"流程引擎能力中台",
    "Ultra-AutoOpsCenter":"自动化运维能力中台",
    "Ultra-UC":"用户管理中心系统",
    "Ultra-IPDIW":"IP运维工作台",
    "Ultra-CDNDIW":"CDN运维工作台",
    "Ultra-SDNC":"SDN控制器",
    "Ultra-CNMP":"核心网运维工作台",
    "Ultra-AIEngine":"智能运维引擎",
    "Ultra-Khan":"一站式研发效能平台",
    }

newproduct_bydept = {
    '数字化运营事业部':["Ultra-CMP","Ultra-CNBP","Ultra-Leopard","Ultra-Matrix","Ultra-BI","Ultra-CNB"],
    '智能运营事业部':["Ultra-BPC","Ultra-AutoOpsCenter","Ultra-UC"],
    '云网运营事业部':["Ultra-IPDIW","Ultra-CDNDIW","Ultra-SDNC","Ultra-CNMP","Ultra-AIEngine"],
    '技术中台支撑部':["Ultra-Khan"],
    }


# ====================================
# 查询新产品代码库入库量
print("\n【按部门查询新产品无代码库明细】：\n ==============================================")

for deptname,productlist in newproduct_bydept.items():
    nocode = 0
    for newpd in productlist:
        sql_sc_project_id = "select dept_name,project_key,id,liable_user_name from kh_project where project_key='%s' and (status=1 or status=2)" %newpd #产品项目
        # 执行SQL语句
        try:
            cursor = conn.cursor()
            cursor.execute(sql_sc_project_id)
            result = cursor.fetchone()
            sql_sc_repository_id = "select project_id,count(repository_id) from kh_project__repository where project_id=%s" % result[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchone()
            if(result_repository[1] == 0):
                print("项目英文名：",result[1],"\t 项目ID:",result[2])
                nocode += 1
        except Exception as e:
            print(e)
    print(deptname,"新产品无代码库项目数",nocode,"\n")

# ====================================
# 查询部门总产品项目数
print("\n【按部门查询维护状态产品项目总数】：\n ==============================================")
for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=2 and dept_name='%s' and  (status=1 or status=2) " %dept_rep
    nocode = 0
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        for data in result:
            if(data[1] in newproduct):
                continue
            print("项目英文名：",data[1],"\t 项目ID:",data[2])
            nocode += 1
            
    except Exception:
        print("查询失败")
    print(data[0],"部门产品项目数",nocode,"\n")


# ====================================
# 查询维护状态产品代码库入库量
print("\n【按部门查询维护状态产品无代码库明细】：\n ==============================================")

for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=2 and dept_name='%s' and  (status=1 or status=2) " %dept_rep
    print(dept_rep,"维护产品无代码库：")
    nocode = 0
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        for data in result:
            if(data[1] in newproduct):
                continue
            sql_sc_repository_id = "select project_id,count(repository_id) from kh_project__repository where project_id=%s" % data[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchone()
            if(result_repository[1] == 0):
                print("项目英文名：",data[1],"\t 项目ID:",data[2])
                nocode += 1
            
    except Exception:
        print("查询失败")
    print(data[0],"无代码库产品项目数",nocode,"\n")




# ====================================
# 查询系统代码库入库量
print("\n【按部门查询系统项目无代码库明细】：\n ==============================================")
for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id,name,liable_user_name from kh_project where category=1 and dept_name='%s' and (status=1 or status=2)" %dept_rep 
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
                print(data[3],"\t",data[1],"\t",data[2],"\t",data[4])
            # print(data[0],result_repository[0])
    except Exception:
        print("查询失败")
    print(data[0],"代码库项目数",dept_rep_y,"无代码库项目数",dept_rep_n,"\n")

# ====================================
# 查询系统是否已做关联产品
print("\n【按部门查询系统项目未关联产品的明细】：\n ==============================================")
for dept_rep in dept:
    sql_sc_project_id = "select dept_name,project_key,id,name,liable_user_name from kh_project where category=1 and dept_name='%s' and (status=1 or status=2)" %dept_rep 
    dept_rep_y = 0
    dept_rep_n = 0
    # 执行SQL语句
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sc_project_id)
        result = cursor.fetchall()
        for data in result:
            sql_sc_repository_id = "select count(depend_project_id) from kh_project_dependency where project_id=%s" % data[2]
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchone()
            if(result_repository[0]):
                dept_rep_y += 1
            else:
                dept_rep_n += 1  
                print(data[3],"\t",data[1],"\t",data[2],"\t",data[4])
    except Exception:
        print("查询失败")
    print(data[0],"已关联产品系统数",dept_rep_y,"未关联产品系统数",dept_rep_n,"\n")



# ====================================
# 查询新产品项目任务创建数

print("\n【按部门新产品项目任务创建数据】：\n ==============================================")
for deptname,productlist in newproduct_bydept.items():
    sum_job = 0
    sum_project = 0
    for newpd in productlist:
        sql_sc_project_id = "select dept_name,project_key,id from kh_project where project_key='%s' and category=2 and (status=1 or status=2)" %newpd #产品项目
        # 执行SQL语句
        try:
            cursor = conn.cursor()
            cursor.execute(sql_sc_project_id)
            result = cursor.fetchall()
            for data in result:
                sql_sc_repository_id = "select count(*) FROM kh_project_function where project_id=%s AND create_time>'2023-04-15'" % data[2]
                cursor.execute(sql_sc_repository_id)
                result_repository = cursor.fetchone()
                if result_repository[0]:
                    sum_project += 1
                    sum_job += result_repository[0]
                print(data[0],data[1],result_repository[0])

        except Exception as e:
            print(e)
    print(deptname,'总项目数:',sum_project,'总任务数:',sum_job,"\n")





# ====================================
# 查询各项目任务创建数
print("\n【按部门维护状态产品项目未关联产品的明细】：\n ==============================================")
for dept_rep in dept:
    # sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=1 and dept_name='%s' and (status=1 or status=2)" %dept_rep #系统项目
    sql_sc_project_id = "select dept_name,project_key,id from kh_project where category=2 and dept_name='%s' and (status=1 or status=2)" %dept_rep #产品项目
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




# ====================================
# 查询新产品项目代码提交数据
print("\n【按部门查询新产品项目代码提交数据】：\n ==============================================")
for deptname,productlist in newproduct_bydept.items():
    pro_commit = {}
    project_sum_commit = 0
    sum_commit = 0 #提交总数计数器
    for newpd in productlist:
        sql_sc_project_id = "select dept_name,project_key,id from kh_project where project_key='%s' and category=2 and (status=1 or status=2)" %newpd #产品项目
        
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
                    sql_sc_repository_commit = "select count(*) from kh_gitlab_statistical_commits where repository_id=%s AND committer_time>'2023-04-15'" % reps_id[0]
                    cursor.execute(sql_sc_repository_commit)
                    result_commit = cursor.fetchone()
                    project_sum_commit+=result_commit[0] #项目代码库提交累加数
                pro_commit[data[1]] = project_sum_commit
                project_sum_commit = 0
        except Exception as e:
            print(e)
    print(deptname,pro_commit)
    print(deptname,"总提交次数",sum(list(pro_commit.values())),"\n")


# ====================================
# 查询各项目代码提交数据
'''
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
            if(data[1] in newproduct):
                continue
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

'''


# 关闭光标对象
cursor.close()
 
# 关闭数据库连接
conn.close()
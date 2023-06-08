#!/usr/bin/python3
# filename  web_show.py

from flask import Flask,render_template,request,url_for,Response
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
dept = {'数字化运营事业部':'szhyy','智能运营事业部':'znyy','云网运营事业部':'ywyy','技术中台支撑部':'jszt','通信运营事业部':'txyy','短信业务支撑部':'dxyw'}

#dept_sys_list字典内按部门列出项目清单
dept_sys_list = {}
for deptname,depkey in dept.items():
    # 按部门查询系统项目列表

    dept_temp_list = []
    sql_sys_list = "select dept_name,id,project_key,name from kh_project where category=1 and dept_name='%s'" %deptname
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sys_list)
        result = cursor.fetchall()
        for data in result:
            dept_temp_list.append(data)
    except Exception:
        print(Exception)
    dept_sys_list.update({depkey:dept_temp_list})    #按部门统计系统项目总数
    #dept_sys_list项目清单end

#未做产品关联的项目数
# ====================================
# 查询系统是否已做关联产品
for dname,sys_list in dept_sys_list.items():
    plink = {}
    dept_rep_y = 0 #有关联+1
    dept_rep_n = 0 #无关联+1
    for sys_info in sys_list:
        sql_depend_id = "SELECT kp.id,kp.name,kp.project_key,kd.depend_project_id,kd.project_id, kd.depend_version_id from kh_project as kp, kh_project_dependency as kd where kd.project_id=%s and kp.id=kd.depend_project_id" % sys_info[1]
        # print(sql_depend_id)
        cursor.execute(sql_depend_id)
        result_depend = cursor.fetchall()
        if (len(result_depend)==0):
            dept_rep_n+=1
        for depend_data in result_depend:
            pass
            # print(depend_data)
    plink.update({dname:dept_rep_n})



#系统项目相关数据展示
#各部门系统项目总数 dep_sys_sum
dep_sys_sum = {}
for dp_name,sys_sum in dept_sys_list.items():
    dep_sys_sum.update({dp_name:len(sys_sum)})


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#dept_product_list字典内按部门列出产品清单
dept_product_list = {}
for deptname,depkey in dept.items():
    # 按部门查询系统项目列表

    dept_temp_list = []
    sql_sys_list = "select dept_name,id,project_key,name from kh_project where category=2 and dept_name='%s'" %deptname
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sys_list)
        result = cursor.fetchall()
        for data in result:
            dept_temp_list.append(data)
    except Exception:
        print(Exception)
    dept_product_list.update({depkey:dept_temp_list})    #按部门统计系统项目总数
#dept_product_list项目清单end

#系统项目相关数据展示
#各部门系统项目总数 dep_product_sum
dep_product_sum = {}
for dp_name,sys_sum in dept_product_list.items():
    dep_product_sum.update({dp_name:len(sys_sum)})


# 关闭光标对象
cursor.close()
 
# 关闭数据库连接
conn.close()

#创建一个Flask对象
app = Flask(__name__)

@app.route('/all/')
def list_all():
    return render_template('index.html',
        sys_total=dep_sys_sum,
        product_total=dep_product_sum,
        sys_detail=dept_sys_list,
        sys_plink=plink)

if __name__ == '__main__':
    #默认为5100端口
    app.run(debug = True,port = 8000)
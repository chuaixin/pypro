#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-01 16:24:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pymysql
import sys
import json
from khan_config import *

# ====================================
# 按部门查询系统和产品项目信息
def get_project_by_dept(ptype, deptname=''):
    conn = pymysql.connect(**conn_khan)
    sys_list = []
    projecttype = {"系统项目":1, "产品项目":2, "历史项目":4, "其他项目":3}

    if deptname:
        sql_sys = "select id,dept_name,project_key,name,liable_user_name,progress_status from kh_project where category={0} and (status=1 or status=2) and dept_name='{1}'".format(projecttype[ptype],deptname)
    else:
        sql_sys = "select id,dept_name,project_key,name,liable_user_name,progress_status from kh_project where category={0} and (status=1 or status=2) order BY dept_name".format(projecttype[ptype])
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sys)
        result = cursor.fetchall()
        for data in result:
            # print (data)
            sys_list.append(data)
    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return sys_list
# ====================================
# 按部门查询系统和产品是否已有代码库 pytype-项目类型，deptname-部门名称，producttype-产品类型（新产品或维护中产品）
def get_project_repository_by_dept(ptype, deptname, producttype=''):
    productlist = get_project_by_dept(ptype, deptname)
    conn = pymysql.connect(**conn_khan)
    cursor = conn.cursor()
    newplist=[]
    
    for pdata in productlist:
        sql_sc_repository_id = "select project_id,count(repository_id) from kh_project__repository where project_id=%s" % pdata[2]
        #根据项目英文名查询代码库数量
        try:
            cursor.execute(sql_sc_repository_id)
            count_repository = cursor.fetchone()
        except Exception as e:
            print(e)
        pdatalist = (pdata[1],pdata[2],pdata[3],pdata[4],count_repository[1])
        if ptype=='产品项目' and producttype=='new': #产品项目判断
            if pdata[1] in newproduct:
                newplist.append(pdatalist) #新产品
        elif ptype=='产品项目' and producttype=='old':
            if not (pdata[1] in newproduct):
                newplist.append(pdatalist) #新产品
        else:
            newplist.append(pdatalist)
    return newplist

# ====================================
# 按部门查询系统和产品管理产品数 pytype-项目类型，deptname-部门名称，producttype-产品类型（新产品或维护中产品）
def get_project_relate_by_dept(ptype, deptname):
    productlist = get_project_by_dept(ptype, deptname)
    conn = pymysql.connect(**conn_khan)
    cursor = conn.cursor()
    newplist =[]

    for pdata in productlist:
        sql_sc_repository_id = "select count(depend_project_id) from kh_project_dependency where project_id=%s" % pdata[2]
        try:
            cursor.execute(sql_sc_repository_id)
            count_depend = cursor.fetchone()
        except Exception as e:
            print(e)
        pdatalist = (pdata[1],pdata[2],pdata[3],pdata[4],count_depend[0])
        newplist.append(pdatalist)

    return newplist


# ====================================
# 按部门查询系统和产品任务创建数据
def get_project_job_by_dept(ptype, deptname):
    productlist = get_project_by_dept(ptype, deptname)
    conn = pymysql.connect(**conn_khan)
    cursor = conn.cursor()
    newplist =[]

    for pdata in productlist:
        sql_sc_repository_id = "select count(*) FROM kh_project_function where project_id=%s AND create_time>'2023-06-01'" % pdata[2]
        try:
            cursor.execute(sql_sc_repository_id)
            count_job = cursor.fetchone()
        except Exception as e:
            print(e)
        pdatalist = (pdata[1],pdata[2],pdata[3],pdata[4],count_job[0])
        newplist.append(pdatalist)

    return newplist

# ====================================
# 按部门查询系统和产品代码提交次数 pytype-项目类型，deptname-部门名称，producttype-产品类型（新产品或维护中产品）
def get_project_codecommit_by_dept(ptype, deptname, producttype=''):
    productlist = get_project_by_dept(ptype, deptname)
    conn = pymysql.connect(**conn_khan)
    cursor = conn.cursor()
    newplist=[]
    pro_commit = {}
    project_sum_commit = 0
    sum_commit = 0 #提交总数计数器
    for pdata in productlist:
        sql_sc_repository_id = "select repository_id from kh_project__repository where project_id=%s" % pdata[2]
        #根据项目英文名查询代码库数量
        try:
            cursor.execute(sql_sc_repository_id)
            result_repository = cursor.fetchall()
        except Exception as e:
            print(e)
        #通过代码库id查询提交代码次数
        for reps_id in result_repository:
            sql_sc_repository_commit = "select count(*) from kh_gitlab_statistical_commits where repository_id=%s AND committer_time>'2023-06-01'" % reps_id[0]
            cursor.execute(sql_sc_repository_commit)
            result_commit = cursor.fetchone()
            project_sum_commit+=result_commit[0] #项目代码库提交累加数

        pdatalist = (pdata[1],pdata[2],pdata[3],pdata[4],project_sum_commit)
        project_sum_commit = 0
        if ptype=='产品项目' and producttype=='new': #产品项目判断
            if pdata[1] in newproduct:
                newplist.append(pdatalist) #新产品
        elif ptype=='产品项目' and producttype=='old':
            if not (pdata[1] in newproduct):
                newplist.append(pdatalist) #新产品
        else:
            newplist.append(pdatalist)
    return newplist

def get_project_info(projectID):
    conn = pymysql.connect(**conn_khan)
    project_info = {}
    project_commit_times =0
    project_commit_count =0
    sql_sys = "select id,name,project_key,category,status,liable_user_name,progress_status from kh_project where id={0}".format(projectID)
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sys)
        result = cursor.fetchone()
        project_info = {'项目名称':result[1],'项目标识':result[2],'项目ID':result[0],'项目类型':project_type[result[3]],'项目状态':project_status[result[4]],'项目经理':result[5],'项目执行状态':progress_status[result[6]]}

        #读取该项目的项目成员
        sql_members = "select ACCOUNT_,NAME_,DIC.`name` from kh_project_member AS PROJ JOIN kh_dict AS DIC ON PROJ.project_id=%s AND PROJ.`STATUS_`=1 AND PROJ.ROLE_ID = DIC.id" % projectID
        cursor.execute(sql_members)
        member_list = {}
        result = cursor.fetchall()
        for member in result:
            if not (member[0] in ignore_member):
                member_list[member[0]]=member[2]
            
        project_info['团队成员'] = member_list

        #读取该项目的产品及版本依赖
        sql_depend_id = "select depend_project_id,depend_version_id from kh_project_dependency where project_id=%s" % projectID
        cursor.execute(sql_depend_id)
        result = cursor.fetchall()
        depend_list = []
        for depend_id,version_id in result:
            if version_id:
                sql_version = "select v.name,v.project_id ,v.id ,p.project_key from kh_version as v, kh_project as p where v.id={0} and v.project_id={1} and p.id={2}".format(version_id,depend_id,depend_id)
                cursor.execute(sql_version)
                result_version = cursor.fetchone()
                depend_list.append([result_version[3],result_version[0]])
            else:
                sql_version = "select project_key from kh_project where id={0}".format(depend_id)
                cursor.execute(sql_version)
                result_version = cursor.fetchone()
                depend_list.append([result_version[0]])
        project_info['产品依赖'] = depend_list

        #读取该项目的代码库
        sql_repository_id = "select repository_id from kh_project__repository where project_id=%s" % projectID
        cursor.execute(sql_repository_id)
        result = cursor.fetchall()
        repo_list = []
        for repo_id in result:
            #通过代码库id查询提交代码次数
            sql_sc_repository_commit = "select repository_id,count(total),CAST(SUM(total) AS SIGNED) from kh_gitlab_statistical_commits where repository_id=%s AND committer_time>'2023-06-01'" % repo_id[0]
            cursor.execute(sql_sc_repository_commit)
            result_commit = cursor.fetchone()
            project_commit_times = project_commit_times+result_commit[1] #项目代码库提交累加数
            if result_commit[2] is not None:
                project_commit_count = project_commit_count+result_commit[2] #项目代码行数提交累加数
            repo_list.append(repo_id[0])

        project_info['repository_list'] = repo_list
        project_info['repository_commit_times'] = project_commit_times
        project_info['repository_commit_total'] = project_commit_count


        #读取该项目的任务创建
        sql_job = "select count(*) FROM kh_project_function where project_id=%s AND create_time>'2023-06-01'" % projectID
        cursor.execute(sql_job)
        result_job = cursor.fetchone()
        project_info['job_count'] = result_job[0]

    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return project_info

#项目团队成员及角色信息
def get_project_memeber(projectID):
    conn = pymysql.connect(**conn_khan)
    member_list = {}
    sql_members = "select ACCOUNT_,NAME_,DIC.`name` from kh_project_member AS PROJ JOIN kh_dict AS DIC ON PROJ.project_id=%s AND PROJ.`STATUS_`=1 AND PROJ.ROLE_ID = DIC.id" % projectID
    try:
        cursor = conn.cursor()
        #读取该项目的项目成员
        cursor.execute(sql_members)

        result = cursor.fetchall()
        for member in result:
            if not (member[0] in ignore_member):
                member_list[member[0]]=member[2]
        
    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return member_list

# 获取项目版本及版本产品依赖信息
def get_project_related(projectID):
    conn = pymysql.connect(**conn_khan)
    project_info = {}

    try:
        cursor = conn.cursor()
        #读取该项目的版本数据
        sql_depend_id = "select kv.`name`,kv.`id`,kdic.`name` from kh_project_version AS kv JOIN kh_dict as kdic where project_id=%s AND kv.version_type=kdic.id" % projectID
        cursor.execute(sql_depend_id)
        result = cursor.fetchall()
        vers_list = {}
        for version_info in result:
            sql_version = "select pv.project_version_id,khpro.name,khpro.project_key,pv.depend_project_id,pv.official_version,pv.upgrade_pack,pv.patch_pack FROM kh_project_version_dependency AS pv join kh_project AS khpro ON pv.project_version_id={0} AND khpro.id=pv.depend_project_id".format(version_info[1])
            print(sql_version)
            cursor.execute(sql_version)
            result_version = cursor.fetchall()
            if len(result_version)==0:
                vers_list[version_info[0]]='' #将为空的版本信息加入字典
            else:
                vers_depend_list = []
                # 根据版本数据统计该版本下依赖的版本
                for vers_depend in result_version:
                    
                    # 添加主版本
                    if vers_depend[4] is not None:
                        print("official",vers_depend[4])
                        vers_depend_list.append(vers_depend[4])
                    # 添加升级包版本
                    if vers_depend[5] is not None:
                        vers_upgrade = vers_depend[5].split(";&")
                        vers_upgrade = list(filter(None, vers_upgrade))
                        print("upgrade".vers_upgrade)
                        vers_depend_list.extend(vers_upgrade)
                    # 添加补丁包版本
                    if vers_depend[6] is not None:
                        vers_patch = vers_depend[6].split(";&")
                        vers_patch = list(filter(None, vers_patch))
                        vers_depend_list.extend(vers_patch)
                print(vers_depend_list)
                
                vers_list[version_info[0]]=vers_depend_list
                # vers_depend_list.clear()


                    # print(vers_depend)  

        project_info['产品依赖'] = vers_list

    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return project_info

# print(json.dumps(get_project_info(1010),indent=4,ensure_ascii=False))


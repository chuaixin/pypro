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
        sql_sys = "select dept_name,project_key,id,name,liable_user_name from kh_project where category={0} and (status=1 or status=2) and dept_name='{1}'".format(projecttype[ptype],deptname)
    else:
        sql_sys = "select dept_name,project_key,id,name,liable_user_name from kh_project where category={0} and (status=1 or status=2) order BY dept_name".format(projecttype[ptype])
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
        sql_sc_repository_id = "select count(*) FROM kh_project_function where project_id=%s AND create_time>'2023-04-15'" % pdata[2]
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
            sql_sc_repository_commit = "select count(*) from kh_gitlab_statistical_commits where repository_id=%s AND committer_time>'2023-04-15'" % reps_id[0]
            cursor.execute(sql_sc_repository_commit)
            result_commit = cursor.fetchone()
            project_sum_commit+=result_commit[0] #项目代码库提交累加数

        pdatalist = (pdata[1],pdata[2],pdata[3],pdata[4],project_sum_commit)
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
    sql_sys = "select id,name,project_key,category,status,liable_user_name from kh_project where id={0}".format(projectID)
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sys)
        result = cursor.fetchone()
        project_info = {'id':result[0],'name':result[1],'project_key':result[2],'category':project_type[result[3]],'status':project_status[result[4]],'liable_user_name':result[5]}

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
        project_info['depend_list'] = depend_list

        #读取该项目的代码库
        sql_repository_id = "select repository_id from kh_project__repository where project_id=%s" % projectID
        cursor.execute(sql_repository_id)
        result = cursor.fetchall()
        repo_list = []
        for repo_id in result:
            #通过代码库id查询提交代码次数
            sql_sc_repository_commit = "select repository_id,count(total),CAST(SUM(total) AS SIGNED) from kh_gitlab_statistical_commits where repository_id=%s AND committer_time>'2023-04-15'" % repo_id[0]
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
        sql_job = "select count(*) FROM kh_project_function where project_id=%s AND create_time>'2023-05-15'" % projectID
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




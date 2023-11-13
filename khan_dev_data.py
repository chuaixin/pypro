#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-01 16:24:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pymysql
import sys
import datetime
import json
from prettytable import PrettyTable
import re
from khan_config import *
import pandas as pd

# 设置 Pandas 显示选项
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.width', None)  # 自动调整列宽
pd.set_option('display.max_colwidth', None)  # 显示所有单元格的内容
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# ====================================
# 按部门查询系统和产品项目信息
def get_project_by_dept(ptype, deptname=''):
    conn = pymysql.connect(**conn_khan)
    sys_list = []
    projecttype = {"系统项目":1, "产品项目":2, "历史项目":4, "其他项目":3}

    if deptname:
        sql_sys = "select dept_name,id,project_key,name,liable_user_name,progress_status,province,trade,customer_abbreviated from kh_project where category={0} and (status=1 or status=2) and dept_name='{1}'".format(projecttype[ptype],deptname)
    else:
        sql_sys = "select dept_name,id,project_key,name,liable_user_name,progress_status,province,trade,customer_abbreviated from kh_project where category={0} and (status=1 or status=2) order BY dept_name".format(projecttype[ptype])
    try:
        cursor = conn.cursor()
        cursor.execute(sql_sys)
        result = cursor.fetchall()
        for data in result:
            sys_info = (data[0],data[1],data[2],data[3],data[4],progress_status[data[5]],data[6],data[7],data[8])
            sys_list.append(sys_info)
    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return sys_list

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
    project_info = {}
    member_list = {}
    sql_members = "select ACCOUNT_,NAME_,DIC.`name` from kh_project_member AS PROJ JOIN kh_dict AS DIC ON PROJ.project_id=%s AND PROJ.`STATUS_`=1 AND PROJ.ROLE_ID = DIC.id  ORDER BY DIC.name" % projectID
    try:
        cursor = conn.cursor()
        #读取该项目的项目成员
        cursor.execute(sql_members)

        result = cursor.fetchall()
        for member in result:
            if not (member[2] in ignore_member):
                member_list[member[0]]=member[2] 
    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接 
    conn.close()
    project_info['membercount'] = len(member_list)
    project_info['memberlist'] = member_list

    return project_info

# 获取项目版本及版本产品依赖信息
def get_project_related(projectID):
    conn = pymysql.connect(**conn_khan)
    project_info = {}

    try:
        cursor = conn.cursor()
        #读取该项目的版本数据
        # 版本名称、版本ID 从kh_project_version获取
        sql_depend_id = "select kv.`name`,kv.`id`,kdic.`name` from kh_project_version AS kv JOIN kh_dict as kdic where project_id=%s AND kv.version_type=kdic.id" % projectID
        
        cursor.execute(sql_depend_id)
        result = cursor.fetchall()
        vers_list = {}
        for version_info in result:
            # 读取版本下的依赖产品配置
            # 读取项目版本ID、项目名称、项目英文名、项目版本依赖ID以及正式、补丁和升级包版本数据，从kh_project_version_dependency,和 kh_project

            sql_version = "select pv.project_version_id,khpro.name,khpro.project_key,pv.depend_project_id,pv.official_version,pv.upgrade_pack,pv.patch_pack FROM kh_project_version_dependency AS pv join kh_project AS khpro ON pv.project_version_id={0} AND khpro.id=pv.depend_project_id".format(version_info[1])
            cursor.execute(sql_version)
            result_version = cursor.fetchall()
            if len(result_version)==0:
                vers_list[version_info[0]]='' #将为空的版本信息加入字典
            else:
                vers_depend_key=[]
                # 根据版本数据统计该版本下依赖的版本
                for vers_depend in result_version:
                    vers_depend_list = []
                    # 添加主版本
                    if vers_depend[4] is not None:
                        vers_depend_list.append(vers_depend[4])

                    # 添加升级包版本
                    if vers_depend[5] is not None:
                        vers_upgrade = vers_depend[5].split(";&")
                        vers_upgrade = list(filter(None, vers_upgrade))
                        vers_depend_list.extend(vers_upgrade)
                    # 添加补丁包版本
                    if vers_depend[6] is not None:
                        vers_patch = vers_depend[6].split(";&")
                        vers_patch = list(filter(None, vers_patch))
                        vers_depend_list.extend(vers_patch)


                    # 对查询到的版本ID查询具体版本名称
                    for vers_key in vers_depend_list:
                        sql_verskey = "SELECT `name`,`link_url` FROM `khan2_pro`.`kh_project_version` WHERE `project_id` = {0} AND id = {1}".format(vers_depend[3],vers_key)
                        cursor.execute(sql_verskey)
                        result_version_key = cursor.fetchone()
                        if result_version_key is not None:
                            # 处理是否有介质判断

                            linktag = ''
                            if result_version_key[1] is not None and re.match(r"http://192.168.106.56:57880/svn", result_version_key[1]):
                                linktag = 'SVN存管'
                            else:
                                linktag = '无'
                            vers_temp_key = (vers_depend[2],vers_depend[1],result_version_key[0],linktag)
                            vers_depend_key.append(vers_temp_key)
                            
                vers_list[version_info[0]]=vers_depend_key

        project_info['verscount'] = len(vers_list)
        project_info['relatelist'] = vers_list


    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return project_info


def get_project_repository(projectID):
    conn = pymysql.connect(**conn_khan)
    project_info = {}

    try:
        cursor = conn.cursor()
        #读取该项目的代码库
        sql_repository_id = "select * from kh_project__repository AS pr JOIN kh_gitlab_repository AS gr where pr.project_id=%s AND pr.repository_id=gr.id ORDER BY gr.last_activity_at DESC" % projectID
        cursor.execute(sql_repository_id)
        result = cursor.fetchall()
        repo_list = []
        if len(result)>0:
            for result_repo in result:
                #通过代码库id查询提交代码次数
                repo_info = [result_repo[2],result_repo[8],result_repo[6],str(result_repo[13])]
                repo_list.append(repo_info)

        project_info['repository_count'] = len(repo_list)
        project_info['repository_list'] = repo_list

    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return project_info


# 按部门查询系统和产品代码提交次数 pytype-项目类型，deptname-部门名称，producttype-产品类型（新产品或维护中产品）
def get_project_codecommit(projectID):
    conn = pymysql.connect(**conn_khan)
    project_info = {}

    try:
        cursor = conn.cursor()
        #读取该项目的代码库
        sql_repository_id = "select pr.repository_id,gr.http_url_to_repo from kh_project__repository AS pr JOIN kh_gitlab_repository AS gr where pr.project_id=%s AND pr.repository_id=gr.id and gr.last_activity_at >'2023-01-01 00:00:00' ORDER BY gr.last_activity_at DESC" % projectID
        cursor.execute(sql_repository_id)
        repoid_list = cursor.fetchall()
        repo_list = []
        if len(repoid_list)>0:
            for repoid,repourl in repoid_list:
                #通过代码库id查询提交代码次数
                sql_repo_commit = "SELECT repository_id, committer_name,COUNT(commit_id),sum(total) FROM `khan2_pro`.`kh_gitlab_statistical_commits` WHERE `repository_id` = {0} and DATE_FORMAT(committer_time,'%Y') in ('2023') GROUP BY committer_name".format(repoid)
                cursor.execute(sql_repo_commit)
                result_repo_commit = cursor.fetchall()
                if len(result_repo_commit)>0:
                    for repo_by_member in result_repo_commit:
                        repo_commit_enumerate = [repo_by_member[0],repourl,repo_by_member[1],repo_by_member[2],str(repo_by_member[3])]
                        repo_list.append(repo_commit_enumerate)

        project_info['repository_count'] = len(repo_list)
        project_info['repository_list'] = repo_list

    except Exception as e:
        print(e)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return project_info

# print(json.dumps(get_project_info(1010),indent=4,ensure_ascii=False))


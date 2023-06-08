#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-02 17:38:43
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import pymysql
import sys
from khan_dev_data import *

# 按部门查询系统项目数 
print("\n【按部门查询系统项目数】：\n==============================================")
for dname in dept:
    
    print("【",dname,"相关统计】：\n")
    print("系统项目数：", len(get_project_by_dept("系统项目", dname)))
    print("明细：", get_project_by_dept("系统项目", dname))

    print("产品项目数：", len(get_project_by_dept("产品项目", dname)))
    print("明细：", get_project_by_dept("产品项目", dname))
    print("\n")

    repo_dept_new = get_project_repository_by_dept("产品项目", dname, 'new')
    repo_dept_old = get_project_repository_by_dept("产品项目", dname, 'old')
    repcount = 0
    for repdata in repo_dept_new:
        if repdata[-1]==0:
            repcount +=1
    print("新产品代码入库项目数：", len(repo_dept_new), "无代码库的项目数量", repcount)
    print("明细：", repo_dept_new)
    print("\n")

    repcount = 0
    for repdata in repo_dept_old:
        if repdata[-1]==0:
            repcount +=1
    print("维护中产品代码入库项目数：", len(repo_dept_old), "无代码库的项目数量", repcount)
    print("明细：", repo_dept_old)
    print("\n")


    repo_sys = get_project_repository_by_dept("系统项目", dname)
    repcount = 0
    replist = []
    for repdata in repo_sys:
        if repdata[-1]==0:
            repcount +=1
            replist.append(repdata)
    print("系统项目数：", len(repo_sys), "无代码库的项目数量", repcount)
    print("明细：",replist)
    print("\n")

    depend_sys = get_project_relate_by_dept("系统项目", dname)
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in depend_sys:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
    print("系统已绑定产品项目数：", repcount_yes, "未绑定产品的项目数", repcount_no)
    print("未绑定产品的系统项目明细：",nodepend_list)
    print("\n")

    depend_product = get_project_relate_by_dept("产品项目", dname)
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in depend_product:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
    print("产品项目已绑定产品项目数：", repcount_yes, "未绑定产品的项目数", repcount_no)
    print("未绑定产品的产品项目明细：",nodepend_list)
    print("\n")

    job_product = get_project_job_by_dept("产品项目", dname)
    sum_job = 0
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in job_product:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
            sum_job += repdata[4]
    print("产品项目已创建任务产品项目数：", repcount_yes, "未创建任务的产品项目数", repcount_no)
    print("未创建任务的产品项目明细：",nodepend_list)
    print("任务创建总数：",sum_job)
    print("\n")

    job_sys = get_project_job_by_dept("系统项目", dname)
    sum_job = 0
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in job_sys:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
            sum_job += repdata[4]
    print("系统项目已创建任务产品项目数：", repcount_yes, "未创建任务的系统项目数", repcount_no)
    print("未创建任务的系统项目明细：",nodepend_list)
    print("任务创建总数：",sum_job)
    print("\n")


    newproduct_commit = get_project_codecommit_by_dept("产品项目", dname, "new")
    sum_job = 0
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in newproduct_commit:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
            sum_job += repdata[4]
    print("新产品代码提交正常项目数：", repcount_yes, "新产品无代码提交项目数：", repcount_no)
    print("新产品无代码提交项目明细：",nodepend_list)
    print("代码提交总数：",sum_job)
    print("\n")


    oldproduct_commit = get_project_codecommit_by_dept("产品项目", dname, "old")
    sum_job = 0
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in oldproduct_commit:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
            sum_job += repdata[4]
    print("维护中产品代码提交正常项目数：", repcount_yes, "维护中产品无代码提交项目数：", repcount_no)
    print("维护中产品无代码提交项目明细：",nodepend_list)
    print("代码提交总数：",sum_job)
    print("\n")


    sys_commit = get_project_codecommit_by_dept("系统项目", dname,)
    sum_job = 0
    repcount_no = 0
    repcount_yes = 0
    nodepend_list = []
    for repdata in sys_commit:
        if not repdata[4]:
            repcount_no += 1
            nodepend_list.append(repdata)
        else:
            repcount_yes += 1
            sum_job += repdata[4]
    print("系统项目代码提交正常项目数：", repcount_yes, "系统项目无代码提交项目数：", repcount_no)
    print("系统项目无代码提交项目明细：",nodepend_list)
    print("代码提交总数：",sum_job)
    print("\n")




    break


			
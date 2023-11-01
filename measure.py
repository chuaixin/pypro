#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-07-04 16:14:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


from khan_dev_data import *

dname = '云网运营事业部'
pro_type = 1   #1为系统项目，2为产品项目
print("【项目明细】：\n")
project_list = get_project_by_dept(project_type[pro_type],dname)
print("项目数：", len(project_list))

#项目信息表
tb = PrettyTable()

for project_info in project_list:
	# print(project_info)
	# print("项目版本及依赖：",json.dumps(get_project_related(project_info[0]),indent=4,ensure_ascii=False))
	# print("代码库：",json.dumps(get_project_repository(project_info[0]),indent=4,ensure_ascii=False))
	# print("项目成员：",json.dumps(get_project_memeber(project_info[0]),indent=4,ensure_ascii=False))
	# break

	#添加表头
	if pro_type==1:
		tb.field_names = ['项目ID', '部门名称', '项目英文名', '项目中文名', '项目经理', '项目执行状态', '省分', '客户', '简称', '项目成员数', '版本数', '代码库数量']
		pinfo = list(project_info)
		pinfo[3] = pinfo[3][0:10]
	else:
		tb.field_names = ['项目ID', '部门名称', '项目英文名', '项目中文名', '项目经理', '项目执行状态', '项目成员数', '版本数', '代码库数量']
		pinfo = list(project_info)
		del pinfo[-1]
		del pinfo[-1]
		del pinfo[-1]
		pinfo[3] = pinfo[3][0:10]
		print(pinfo)
	project_group = get_project_memeber(project_info[0])
	pinfo.append(project_group['membercount'])
	project_vers = get_project_related(project_info[0])
	pinfo.append(project_vers['verscount'])
	project_repo = get_project_repository(project_info[0])
	pinfo.append(project_repo['repository_count'])
		
	#添加行
	tb.add_row(pinfo)
	#设置对齐方式align: l,r,c
	tb.align = 'c'

print(tb)



print("结束\n")

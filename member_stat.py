#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-11-03 10:14:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from khan_dev_data import *


dname = '技术中台支撑部'

pro_type = (2,1)   #1为系统项目，2为产品项目

for ptype in pro_type:
	pd_data = []
	print(project_type[ptype],":")
	project_list = get_project_by_dept(project_type[ptype],dname)

	for project_info in project_list:
		print("项目信息",project_info)

		p_codecommit = get_project_codecommit(project_info[1])
		print("查询结果：",json.dumps(p_codecommit,indent=4,ensure_ascii=False))



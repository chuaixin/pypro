#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-07-04 16:14:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


import pymysql
import sys
import json
from khan_dev_data import *

dname = '数字化运营事业部'
print("【项目明细】：\n")
project_list = get_project_by_dept("产品项目", dname)
print("项目数：", len(project_list))
# print("明细：", project_list)
for project_info in project_list:
	print(project_info)

	print("项目成员：",json.dumps(get_project_memeber(project_info[0]),indent=4,ensure_ascii=False))
	print("项目版本及依赖：",json.dumps(get_project_related(project_info[0]),indent=4,ensure_ascii=False))
	print("项目代码库：",json.dumps(get_project_repository(project_info[0]),indent=4,ensure_ascii=False))
	break
print("结束\n")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-07 16:30:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from khan_dev_data import *
import json

# confirmlist={
#  'U-GZYD-SJGXPT':'992',
#  'U-GXYD-SCREEN':'1017',
#  'U-GXYD-IQA':'1023',
#  'U-YNYD-JZXN':'1042',
#  'U-NMDX-SJGXPT':'1071',
#  'U-LNYD-JZXN':'1073',
#  'U-DXJT-ZNWG':'1076',
#  'U-HBYD-IPMAN':'1084',
#  'U-HIYD-IPMAN':'1085',
#  'U-GXYD-IPMAN':'1086',
#  'U-HNYD-IPDIW':'1155',
# 	}
# try:
# 	for x in confirmlist.values():
# 		projectinfo = get_project_info(x)
# 		if projectinfo['repository_list']:
# 			print("已有代码库,提交行数",projectinfo['repository_commit_total'])
# 		else:
# 			print("无代码库")
# except Exception as e:
# 	print(e)

sort_code_dict = {}
sort_commit_dict = {}
sort_job_dict = {}
deptlist = get_project_by_dept("产品项目", '数字化运营事业部','new')
for pdata in deptlist:
	pinfo = get_project_info(pdata[2])
	sort_code_dict[pinfo['project_key']] = pinfo['repository_commit_total'] 
	sort_commit_dict[pinfo['project_key']] = pinfo['repository_commit_times'] 
	sort_job_dict[pinfo['project_key']] = pinfo['job_count'] 

temp_commit_key = []
temp_commit_value = []
sorted_commit_dict = sorted(sort_commit_dict.items(),key=lambda x:x[1],reverse=True)
for std_commit in sorted_commit_dict:
	temp_commit_key.append(std_commit[0])
	temp_commit_value.append(std_commit[1])
print(temp_commit_key,temp_commit_value)

temp_commit_key = []
temp_commit_value = []
sorted_job_dict = sorted(sort_job_dict.items(),key=lambda x:x[1],reverse=True)
for std_commit in sorted_job_dict:
	temp_commit_key.append(std_commit[0])
	temp_commit_value.append(std_commit[1])
print(temp_commit_key,temp_commit_value)

temp_commit_key = []
temp_commit_value = []
sorted_code_dict = sorted(sort_code_dict.items(),key=lambda x:x[1],reverse=True)
for std_commit in sorted_code_dict:
	temp_commit_key.append(std_commit[0])
	temp_commit_value.append(std_commit[1])

print(temp_commit_key,temp_commit_value)

# print(sorted_commit_dict.keys(),sorted_commit_dict.values())
# print(sorted_job_dict.keys(),sorted_job_dict.values())
# print(sorted_code_dict.keys(),sorted_code_dict.values())


# print(json.dumps(sort_code_dict,indent=4,ensure_ascii=False))




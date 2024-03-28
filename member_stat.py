# -*- coding: utf-8 -*-
# @Date    : 2023-11-03 10:14:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from khan_dev_data import *

dname = '智能运营事业部'

pro_type = (2,1)   #1为系统项目，2为产品项目
#!/usr/bin/env python
pd_data = []
for ptype in pro_type:

	print(project_type[ptype],":")
	project_list = get_project_by_dept(project_type[ptype],dname)

	for project_info in project_list:
		project_commit=[]
		print("项目信息",project_info)
		p_codecommit = get_project_codecommit(project_info[1])
		print(p_codecommit['repository_count'])
		if p_codecommit['repository_count']>0:
			for commiter in p_codecommit['repository_list']:
				commit_s = [project_info[0],project_info[1],project_info[2],project_info[3]]
				commit_s.extend(commiter)
				project_commit.append(commit_s
				)
				commit_s =''
		sort_pd_data = sorted(project_commit,key= lambda x: x[4])

		pd_data.extend(sort_pd_data)
field_names = ['部门','项目ID','项目英文名','项目中文名','人员账号','代码库ID','代码库地址','提交次数','提交行数']
dframe_commmit = pd.DataFrame(pd_data,columns=field_names,dtype='string')

#新建文件名
'''
time = datetime.datetime.now()
timestamp = time.strftime("%Y%m%d_%H%M%S")
doc_name = "./static/"+'codecommit_'+timestamp+'.xlsx'

with pd.ExcelWriter(doc_name) as writer:
    dframe_commmit.to_excel(writer, sheet_name=dname, index=False)
'''
print(dframe_commmit)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-11-21 17:49:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from khan_dev_data import *
# pdb.set_trace()  # 设置断点
dname = '云网运营事业部'

pro_type = (2,1)   #1为系统项目，2为产品项目
pd_data = []
for ptype in pro_type:

	print(project_type[ptype],":")
	project_list = get_project_by_dept(project_type[ptype],dname)

	for project_info in project_list:
		project_commit=[]
		print("项目信息",project_info)
		p_perform = get_project_performance(project_info[1])
		print(p_perform['perform_count'])
		if p_perform['perform_count']>0:
			for performinfo in p_perform['perform_list']:
				commit_s = [project_info[0],project_info[1],project_info[2],project_info[3],project_info[4],project_info[6],project_info[7],project_info[8]]
				commit_s.extend(performinfo)
				project_commit.append(commit_s)
				commit_s =''

		pd_data.extend(project_commit)
field_names = ['部门','项目ID','项目英文名','项目中文名','项目经理','省分','客户','简称','合同项目编号','合同名称','23年新签毛利额','23年确认毛利额','合同总额']
dframe_performance = pd.DataFrame(pd_data,columns=field_names,dtype='string')

#新建文件名
time = datetime.datetime.now()
timestamp = time.strftime("%Y%m%d_%H%M%S")
doc_name = "./static/"+'业绩统计分析_'+dname+timestamp+'.xlsx'

with pd.ExcelWriter(doc_name) as writer:
    dframe_performance.to_excel(writer, sheet_name=dname, index=False)

print(dframe_performance)

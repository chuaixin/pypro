#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-07-04 16:14:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import pandas as pd
from khan_dev_data import *

# 设置 Pandas 显示选项
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.width', None)  # 自动调整列宽
pd.set_option('display.max_colwidth', None)  # 显示所有单元格的内容
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# dname = '技术中台支撑部'
dname = '数字化运营事业部'

pro_type = (2,1)   #1为系统项目，2为产品项目

for ptype in pro_type:
	pd_data = []
	if ptype == 1:#系统项目显示省分、客户和简称信息
		field_names = ['项目ID', '部门名称', '项目英文名', '项目中文名', '项目经理', '项目执行状态', '省分', '客户', '简称']
	else:
		field_names = ['项目ID', '部门名称', '项目英文名', '项目中文名', '项目经理', '项目执行状态']

	for dname in dept:
		print("\n")
		project_list = get_project_by_dept(project_type[ptype],dname)
		# project_list = [['107',"技术中台支撑部","Ultra-LDCP","一站式研发","杜勇","未开始",33,33,11]]

		print(dname,project_type[ptype],"项目数：", len(project_list))

		for project_info in project_list:
			# print("项目版本及依赖：",json.dumps(get_project_related(project_info[0]),indent=4,ensure_ascii=False))
			# 基础项目信息数据
			pinfo = list(project_info)

			if ptype==2:
				del pinfo[-1]
				del pinfo[-1]
				del pinfo[-1]
			pinfo[3] = pinfo[3][0:10]

			project_group = get_project_memeber(project_info[0])
			pinfo.append(project_group['membercount'])
			project_vers = get_project_related(project_info[0])
			pinfo.append(project_vers['verscount'])
			project_repo = get_project_repository(project_info[0])
			pinfo.append(project_repo['repository_count'])

			temp_pinfo=pinfo.copy()
			result_pinfo = []
			# 添加版本和依赖数据
			verslist = get_project_related(project_info[0])
			if verslist['verscount']>0:
				for vers,relatevalue in verslist['relatelist'].items():
					versdata = [vers]
					if len(relatevalue)>0:
						for relate in relatevalue:
							versdata.extend(relate)
							temp_pinfo.extend(versdata)
							result_pinfo.append(temp_pinfo) #组合内容加入列表

							temp_pinfo=pinfo.copy()	#清空临时文件
							versdata = [vers] #清空临时文件
					else:
						temp_pinfo.extend([vers,'','','',''])
						result_pinfo.append(temp_pinfo)

						temp_pinfo=pinfo.copy()	#清空临时文件
						versdata = [vers] #清空临时文件
			else:
				temp_pinfo.extend(['','','','',''])	
				result_pinfo.append(temp_pinfo)

			#添加项目信息数据
			pd_data.extend(result_pinfo)


	field_names.extend(['项目成员数','版本数','代码库数','版本','依赖产品英文','依赖产品名称','是否有介质','依赖产品版本'])
	if ptype==1:
		dframe_sys = pd.DataFrame(pd_data,columns=field_names,dtype='string')
		print(dframe_sys)
	else:
		dframe_project = pd.DataFrame(pd_data,columns=field_names,dtype='string')
		print(dframe_project)


#新建文件名
time = datetime.datetime.now()
timestamp = time.strftime("%Y%m%d_%H%M%S")
doc_name = "./static/"+'basedata_'+timestamp+'.xlsx'

# newdoc = pd.ExcelWriter(doc_name,mode='a')
# dframe_sys.to_excel(newdoc, sheet_name="系统项目清单" ,index=False)
# dframe_project.to_excel(newdoc, sheet_name="产品项目清单" ,index=False)

with pd.ExcelWriter(doc_name) as writer:
    dframe_sys.to_excel(writer, sheet_name='系统项目清单', index=False)
    dframe_project.to_excel(writer, sheet_name='产品项目清单', index=False)


	# print("代码库：",json.dumps(get_project_repository(project_info[0]),indent=4,ensure_ascii=False))
	# print("项目成员：",json.dumps(get_project_memeber(project_info[0]),indent=4,ensure_ascii=False))


print("结束\n")

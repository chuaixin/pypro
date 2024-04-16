#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-01 16:30:54
# @Author  : chuaixin
# @Link    : http://example.org
# @Version : $Id$

# 连接数据库，创建连接对象connection

conn_khan = {    
	'host':'192.168.95.170',
    'port':22306,
    'user':'khan3_pro',
    'password':'fT6_Yasgh4U1d',
    'database':'khan3_pro',
    'charset':'utf8'
    }

# 连接本地数据库，创建连接对象connection
conn_local = {    
    'host':'localhost',
    'user':'root',
    'password':'cx007928',
    'database':'stock',
    'charset':'utf8'
    }


#部门信息配置
dept = ('数字化运营事业部','智能运营事业部','云网运营事业部','技术中台支撑部','通信运营事业部','短信业务支撑部')

#部门信息配置
deptdict = {'数字化运营事业部':'szhyy','智能运营事业部':'znyy','云网运营事业部':'ywyy','技术中台支撑部':'jszt','通信运营事业部':'txyy','短信业务支撑部':'dxyw'}

#项目类型
project_type = {1:"系统项目", 2:"产品项目", 3:"其他项目",4:"历史项目",5:"解决方案项目"}
project_status = {0:"删除", 1:"正常", 2:"归档之后取消",3:"归档"}
progress_status = {1:"未开始", 2:"进行中", 3:"维保阶段",4:"已完成",5:"挂起"}
code_store = {1:"代码库纳管", 2:"代码库不纳管"}

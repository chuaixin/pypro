#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-01 16:30:54
# @Author  : chuaixin
# @Link    : http://example.org
# @Version : $Id$

# 连接数据库，创建连接对象connection
conn_khan = {    
	'host':'192.168.95.170',
    'user':'khan2_pro',
    'password':'khan2_pro',
    'database':'khan2_pro',
    'charset':'utf8'}


#部门信息配置
# dept = ('数字化运营事业部','智能运营事业部','云网运营事业部','技术中台支撑部','通信运营事业部','短信业务支撑部')
dept = ('数字化运营事业部','技术中台支撑部')

#部门信息配置
deptdict = {'数字化运营事业部':'szhyy','智能运营事业部':'znyy','云网运营事业部':'ywyy','技术中台支撑部':'jszt','通信运营事业部':'txyy','短信业务支撑部':'dxyw'}

#项目类型
project_type = {1:"系统项目", 2:"产品项目", 3:"其他项目",4:"历史项目"}
project_status = {0:"删除", 1:"正常", 2:"归档之后取消",3:"归档"}
progress_status = {1:"未开始", 2:"进行中", 3:"维保阶段",4:"已完成",5:"挂起"}
ignore_member = ["wangxiaojun", "zhangkai", "liupeng","chuaixin","xiaokunpeng","zhangwanting","zhaowei4"]

# ====================================
# 查询新产品代码库入库量
newproduct = {
    "Ultra-CMP":"混合多云管理平台",
    "Ultra-CNBP":"算网大脑平台",
    "Ultra-Leopard":"猎豹智云平台",
    "Ultra-Matrix":"配置管理矩阵",
    "Ultra-BI":"数析展示工具",
    "Ultra-CNB":"集约化综合网管",
    "Ultra-BPC":"流程引擎能力中台",
    "Ultra-AutoOpsCenter":"自动化运维能力中台",
    "Ultra-UC":"用户管理中心系统",
    "Ultra-IPDIW":"IP运维工作台",
    "Ultra-CDNDIW":"CDN运维工作台",
    "Ultra-SDNC":"SDN控制器",
    "Ultra-CNMP":"核心网运维工作台",
    "Ultra-AIEngine":"智能运维引擎",
    "Ultra-Khan":"一站式研发效能平台",
    }

newproduct_bydept = {
    '数字化运营事业部':["Ultra-CMP","Ultra-CNBP","Ultra-Leopard","Ultra-Matrix","Ultra-BI","Ultra-CNB"],
    '智能运营事业部':["Ultra-BPC","Ultra-AutoOpsCenter","Ultra-UC"],
    '云网运营事业部':["Ultra-IPDIW","Ultra-CDNDIW","Ultra-SDNC","Ultra-CNMP","Ultra-AIEngine"],
    '技术中台支撑部':["Ultra-Khan"],
    }


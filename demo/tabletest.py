#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-10-29 17:02:07
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from prettytable import PrettyTable
import pandas as pd



#创建Prettytable实例
tb = PrettyTable()
#添加表头
tb.field_names = ['userId', 'name', 'sex', 'age', 'job']
#添加行
tb.add_row(['123', '张三', '男', '25', 'softtest'])
tb.add_row(['124', '李四', '男', '25', 'Java'])
#添加列
tb.add_column('address', ['深圳', '北京'])
#设置对齐方式align: l,r,c
tb.align = 'l'
#自定义边框样式
print("默认边框:")
print(tb)
tb.horizontal_char = '*'  #横边框
tb.vertical_char = '|'    #竖边框
tb.junction_char = '|'    #边框连接符
print("自定义边框:")
print(tb)



# 数据
data = {'姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '性别': ['男', '女', '男']}

# 创建DataFrame
df = pd.DataFrame(data)
print(df)
# 生成报表
# df.to_excel('report.xlsx', index=False)

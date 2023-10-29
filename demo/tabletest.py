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
tb.field_names = ['项目ID', '负责人', '项目名称', '英文名', '依赖产品']
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




# 创建数据
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'arlie'],
    'Age': [25, 30, 22, 22],
    'City': ['New York', 'London', 'Paris', 'London']
}

df = pd.DataFrame(data)

# 导出到 Excel 文件
resultPath= "C:/py_gitwork/pypro/demo/output.xlsx"
df.to_excel(resultPath,sheet_name="sheet1",index = False,na_rep = 0,inf_rep = 0)#生成名为数据表1的excel文件

# df.to_excel('C:/py_gitwork/pypro/demo/output.xlsx', index=False)


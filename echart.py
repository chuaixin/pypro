#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-06-30 18:08:44
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

# from pyecharts import charts

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker

Faker.choose() #随机抽取x值
Faker.values() #随机抽取y值


bar = (
    Bar()
    .add_xaxis(Faker.choose())
    .add_yaxis("系列1", Faker.values())
    .add_yaxis("系列2", Faker.values())
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    #title_opts标题
)
bar.render()
#在Jupyter Notebook显示
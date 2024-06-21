import pandas as pd
# 创建一个示例Series
data = pd.Series(['United States', 'Canada', 'Mexico', 'Brazil', 'Argentina'])
# 定义一个映射关系字典
continent_mapping = {
    'United States': 'North America',
    'Canada': 'North America',
    'Mexico': 'North America',
    'Argentina': 'South America'
}
fill_defalt = 'Unknown' 
print(continent_mapping)
# 使用map方法进行映射
data_mapped = data.map(continent_mapping).fillna(fill_defalt)   # 更正：添加缺失值填充  
# 显示映射后的结果
print(data_mapped)

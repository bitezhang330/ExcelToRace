import pandas as pd

# 创建示例数据
data = {
    'year': [2020, 2020, 2020, 2021, 2021, 2021, 2022, 2022, 2022],
    'country': ['中国', '美国', '日本', '中国', '美国', '日本', '中国', '美国', '日本'],
    'gdp': [14723, 20937, 5065, 17734, 23315, 4937, 18100, 25035, 4231]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为Excel文件
df.to_excel('example_data.xlsx', index=False) 
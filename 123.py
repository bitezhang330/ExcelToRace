import pandas as pd
import bar_chart_race as bcr
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
data = []
years = [2005, 2010, 2015, 2020, 2024]

# 2005年数据
countries_2005 = ["美国", "日本", "德国", "英国", "中国", "法国", "意大利", "加拿大", "西班牙", "韩国"]
gdp_2005 = [13094, 4756, 2866, 2511, 2309, 2207, 1856, 1169, 1159, 898]
for country, gdp in zip(countries_2005, gdp_2005):
    data.append({"country": country, "year": 2005, "gdp": gdp})

# 2010年数据
countries_2010 = ["美国", "中国", "日本", "德国", "法国", "英国", "巴西", "意大利", "印度", "俄罗斯"]
gdp_2010 = [14964, 5812, 5793, 3310, 2560, 2246, 2088, 2051, 1729, 1638]
for country, gdp in zip(countries_2010, gdp_2010):
    data.append({"country": country, "year": 2010, "gdp": gdp})

# 2015年数据
countries_2015 = ["美国", "中国", "日本", "德国", "英国", "法国", "印度", "意大利", "巴西", "加拿大"]
gdp_2015 = [18037, 11226, 4382, 3365, 2863, 2420, 2088, 1826, 1801, 1553]
for country, gdp in zip(countries_2015, gdp_2015):
    data.append({"country": country, "year": 2015, "gdp": gdp})

# 2020年数据
countries_2020 = ["美国", "中国", "日本", "德国", "英国", "印度", "法国", "意大利", "加拿大", "韩国"]
gdp_2020 = [21323, 14688, 5056, 3888, 2698, 2675, 2647, 1897, 1656, 1644]
for country, gdp in zip(countries_2020, gdp_2020):
    data.append({"country": country, "year": 2020, "gdp": gdp})

# 2024年数据
countries_2024 = ["美国", "中国", "德国", "日本", "印度", "英国", "法国", "意大利", "巴西", "加拿大"]
gdp_2024 = [28780, 18530, 4590, 4110, 3940, 3500, 3130, 2330, 2330, 2240]
for country, gdp in zip(countries_2024, gdp_2024):
    data.append({"country": country, "year": 2024, "gdp": gdp})

# 创建DataFrame并重新组织数据格式
df = pd.DataFrame(data)
df_pivot = df.pivot(index='year', columns='country', values='gdp')

# 设置matplotlib使用微软雅黑字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置图形大小
plt.figure(figsize=(12, 8), dpi=144)

# 使用bar_chart_race生成动画
bcr.bar_chart_race(
    df=df_pivot,
    filename='global_gdp_ranking.gif',
    orientation='h',
    sort='desc',
    n_bars=10,
    title='全球GDP前十国家排名变化 (2005-2024)',
    period_length=1000
)

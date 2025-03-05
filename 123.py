import matplotlib
matplotlib.use('Agg')  # 使用Agg后端，不需要GUI
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pynimate as nim
from matplotlib.font_manager import FontProperties

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

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

# 创建DataFrame
df = pd.DataFrame(data)

try:
    # 尝试创建动画
    # 数据预处理，为pynimate创建正确格式的数据
    df_pivot = df.pivot(index='year', columns='country', values='gdp').fillna(0)

    # 创建Canvas和BarDatafier对象
    cnv = nim.Canvas(figsize=(15, 8))
    datafier = nim.BarDatafier(
        df_pivot,
        time_format="%Y",
        ip_freq="YE"
    )

    # 创建Barhplot对象
    bar = nim.Barhplot(datafier)

    # 修复时间标签回调函数 - 正确处理Timestamp对象
    bar.set_time(callback=lambda i, datafier: f"{datafier.data.index[i].year}年")

    # 设置标题
    bar.set_title('全球GDP前十国家排名')

    # 设置标签格式
    def format_label(val):
        return f'{val:,.0f}亿美元'

    bar.set_xlabel('GDP (亿美元)')

    # 添加到Canvas并创建动画
    cnv.add_plot(bar)
    cnv.animate()

    # 保存动画
    cnv.save('global_gdp_ranking.gif', fps=2)  # 降低帧率使动画更容易观看
    print("动画创建成功！")

except Exception as e:
    print(f"创建动画失败，错误: {e}")
    print("改用备选方案：创建静态图表...")
    
    # 为每一年创建一个条形图
    fig, axes = plt.subplots(len(years), 1, figsize=(12, 20))
    fig.suptitle('全球GDP前十国家变化 (2005-2024)', fontsize=16)
    
    for i, year in enumerate(years):
        # 筛选当年数据并排序
        year_data = df[df['year'] == year].sort_values('gdp', ascending=False).head(10)
        
        # 创建水平条形图
        bars = axes[i].barh(year_data['country'][::-1], year_data['gdp'][::-1])
        
        # 添加数值标签
        for bar in bars:
            width = bar.get_width()
            axes[i].text(width + 200, bar.get_y() + bar.get_height()/2, 
                         f'{width:,.0f}', ha='left', va='center')
        
        # 设置标题和标签
        axes[i].set_title(f'{year}年', fontsize=14)
        axes[i].set_xlabel('GDP (亿美元)', fontsize=12)
        
        # 设置坐标轴范围，确保所有图表使用相同的比例
        axes[i].set_xlim(0, 30000)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('global_gdp_ranking_static.png')
    print("静态图表已保存为 'global_gdp_ranking_static.png'")

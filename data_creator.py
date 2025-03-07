import pandas as pd
import os

# 准备数据
data = []
years = [2005, 2010, 2015, 2020, 2024]

# 2005年数据
countries_2005 = ["美国", "日本", "德国", "英国", "中国", "法国", "意大利", "加拿大", "西班牙", "韩国"]
gdp_2005 = [13094, 4756, 2866, 2511, 2309, 2207, 1856, 1169, 1159, 898]
for country, gdp in zip(countries_2005, gdp_2005):
    data.append({"year": 2005, "country": country, "gdp": gdp})

# 2010年数据
countries_2010 = ["美国", "中国", "日本", "德国", "法国", "英国", "巴西", "意大利", "印度", "俄罗斯"]
gdp_2010 = [14964, 5812, 5793, 3310, 2560, 2246, 2088, 2051, 1729, 1638]
for country, gdp in zip(countries_2010, gdp_2010):
    data.append({"year": 2010, "country": country, "gdp": gdp})

# 2015年数据
countries_2015 = ["美国", "中国", "日本", "德国", "英国", "法国", "印度", "意大利", "巴西", "加拿大"]
gdp_2015 = [18037, 11226, 4382, 3365, 2863, 2420, 2088, 1826, 1801, 1553]
for country, gdp in zip(countries_2015, gdp_2015):
    data.append({"year": 2015, "country": country, "gdp": gdp})

# 2020年数据
countries_2020 = ["美国", "中国", "日本", "德国", "英国", "印度", "法国", "意大利", "加拿大", "韩国"]
gdp_2020 = [21323, 14688, 5056, 3888, 2698, 2675, 2647, 1897, 1656, 1644]
for country, gdp in zip(countries_2020, gdp_2020):
    data.append({"year": 2020, "country": country, "gdp": gdp})

# 2024年数据
countries_2024 = ["美国", "中国", "德国", "日本", "印度", "英国", "法国", "意大利", "巴西", "加拿大"]
gdp_2024 = [28780, 18530, 4590, 4110, 3940, 3500, 3130, 2330, 2330, 2240]
for country, gdp in zip(countries_2024, gdp_2024):
    data.append({"year": 2024, "country": country, "gdp": gdp})

# 创建DataFrame
df = pd.DataFrame(data)

# 将数据保存为Excel文件
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_data.xlsx')
df.to_excel(output_path, index=False)

print(f"示例数据已保存为: {output_path}")
print(f"数据包含 {len(years)} 个年份，每个年份包含前10个国家的GDP数据")
print(f"共 {len(data)} 条数据记录")
print("数据格式: 第一列(year)年份，第二列(country)国家，第三列(gdp)GDP数值(亿美元)")

# 创建某些国家的GDP变化趋势数据
print("\n创建某些主要国家的趋势数据...")
main_countries = ["美国", "中国", "日本", "德国", "英国", "印度"]
trend_data = []

for country in main_countries:
    country_data = []
    for year in years:
        # 查找该国家在该年份的GDP数据
        found = False
        for entry in data:
            if entry["year"] == year and entry["country"] == country:
                country_data.append(entry["gdp"])
                found = True
                break
        if not found:
            country_data.append(None)  # 缺失数据
    
    trend_data.append({
        "国家": country,
        "2005": country_data[0],
        "2010": country_data[1],
        "2015": country_data[2],
        "2020": country_data[3],
        "2024": country_data[4]
    })

# 创建趋势DataFrame
trend_df = pd.DataFrame(trend_data)

# 保存趋势数据
trend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trend_data.xlsx')
trend_df.to_excel(trend_path, index=False)
print(f"趋势数据已保存为: {trend_path}")
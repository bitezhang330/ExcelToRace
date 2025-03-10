# ExcelToRace - 一键将Excel数据转为炫酷赛跑动图

这是一个基于PyQt5的数据可视化神器，可以一键将Excel数据转换为动态条形图赛跑动画。不仅限于GDP数据，任何时间序列排名数据都可以使用此工具进行可视化。**全部由Cursor AI开发，无需手动编写一行代码！**

## 功能特点

- 一键导入Excel和CSV文件
- 直观的可视化界面操作
- 自定义动画标题和样式
- 灵活调整显示实体数量
- 自由设置动画帧率和速度
- 一键导出高清GIF动画
- 支持生成静态图表快照
- 丰富的自定义颜色和样式选项
- 智能调整动画速度和平滑度
- 适用于各类排名数据可视化（不限于GDP）

## 项目结构

```
.
├── README.md                           # 项目说明文档
├── requirements.txt                    # 项目依赖
├── excel_to_race.py                    # 主程序GUI界面
├── excel_to_race_pro.py                # 专业版GUI界面（通用版）
├── demo_data.xlsx                      # 示例数据
├── trend_demo_data.xlsx                # 趋势数据示例
├── data_generator.py                   # 示例数据生成脚本
├── data_creator.py                     # 高级数据创建脚本
├── demo_gdp_race.gif                   # 生成的动画示例
├── demo_ranking_race.gif               # 另一个动画示例
├── output_animation.gif                # 最新生成的动画
├── output_static_chart.png             # 静态图表输出
└── static_charts/                      # 静态图表目录
```

## 安装

1. 确保已安装Python 3.7+
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序：
```bash
python excel_to_race.py
```
或使用专业版（适用于任何排名数据）：
```bash
python excel_to_race_pro.py
```

2. 点击"导入Excel"按钮选择数据文件
3. 设置列类型（实体名称、时间、数值）
4. 调整动画参数
5. 点击"生成GIF"按钮生成动画
6. 可选择"生成静态图表"功能

## 数据格式要求

Excel文件需包含以下列：
- 实体名称列（国家、公司、产品等）
- 时间列（年份、月份、季度等）
- 数值列（GDP、销售额、人口等任何可比较的数值）

## 核心功能

- 一键生成：只需几次点击，即可将枯燥数据转为生动动画
- 静态图表生成：可以生成特定时间点的静态条形图
- 自定义颜色：支持为不同实体设置不同颜色
- 动画平滑度调整：可以调整动画的平滑程度
- 专业UI界面：直观易用的操作界面
- 通用数据支持：`excel_to_race_pro.py`支持任何类型的排名数据

## 可视化类型

目前支持的可视化类型：
- 动态条形图（柱状图）赛跑动画
- 静态条形图

未来计划添加的可视化类型：
- 折线图动画
- 散点图动画
- 面积图动画
- 饼图动画

## 应用场景

本工具可用于多种场景：
- 国家/地区GDP、人口、军费等排名变化
- 公司市值、收入、利润等排名变化
- 产品销量、市场份额等排名变化
- 运动员/球队成绩排名变化
- 学校/机构排名变化
- 任何其他需要展示排名随时间变化的数据

## 项目亮点

- **零代码开发**：整个项目由Cursor AI智能助手开发，无需手动编写代码
- **高度定制**：满足各种数据可视化需求
- **简单易用**：即使没有编程经验也能轻松上手
- **专业效果**：生成的动画效果专业，适合演示和分享

## 如何贡献

欢迎贡献代码或提出建议！以下是一些可以改进的方向：
1. 添加更多可视化类型
2. 优化动画渲染性能
3. 增强数据处理能力
4. 改进用户界面
5. 添加更多自定义选项

## 获取支持

如果您觉得这个工具有用，请考虑：
- 在GitHub上给项目点星⭐
- 分享给可能需要的朋友或同事
- 提交问题或建议
- 贡献代码或文档

## 注意事项

- 确保数据格式正确
- 生成动画可能需要一定时间，请耐心等待
- 建议使用1000-2000毫秒的帧率以获得最佳观看效果
- 对于大型数据集，建议先生成静态图表预览
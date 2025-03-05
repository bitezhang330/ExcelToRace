# GDP排名动态可视化工具

这是一个基于PyQt5的GDP排名动态可视化工具，可以将Excel数据转换为动态条形图赛跑动画。

## 功能特点

- 支持Excel和CSV文件导入
- 可视化界面操作
- 自定义动画标题
- 可调整显示国家数量
- 可设置动画帧率
- 输出GIF动画文件

## 项目结构

```
.
├── README.md               # 项目说明文档
├── requirements.txt        # 项目依赖
├── gdp_ranking_ui.py      # 主程序GUI界面
├── example_data.xlsx      # 示例数据
├── example_data.py        # 示例数据生成脚本
└── global_gdp_ranking.gif # 生成的动画示例
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
python gdp_ranking_ui.py
```

2. 点击"导入Excel"按钮选择数据文件
3. 设置列类型（国家、年份、数值）
4. 调整动画参数
5. 点击"生成GIF"按钮生成动画

## 数据格式要求

Excel文件需包含以下列：
- 国家名称列
- 年份列
- 数值列（如GDP值）

## 注意事项

- 确保数据格式正确
- 生成动画可能需要一定时间，请耐心等待
- 建议使用1000-2000毫秒的帧率以获得最佳观看效果 
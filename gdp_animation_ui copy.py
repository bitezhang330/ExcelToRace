import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os
from PIL import Image, ImageTk
import pynimate as nim
import platform
from matplotlib.font_manager import FontProperties
import imageio
import gc
import datetime
from matplotlib.ticker import FuncFormatter

class GDPAnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP排名动画生成器")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f7")
        
        self.excel_path = None
        self.output_path = "output_animation.gif"
        self.static_output_path = "output_static.png"
        
        # 设置中文字体
        self.setup_fonts()
        
        # 创建应用UI
        self.create_widgets()
        
    def setup_fonts(self):
        """设置适合当前操作系统的中文字体"""
        system = platform.system()
        
        if system == 'Windows':
            font_names = ['Microsoft YaHei', 'SimHei', 'SimSun', 'Source Han Sans CN']
        elif system == 'Darwin':  # macOS
            font_names = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS', 'Source Han Sans CN']
        else:  # Linux and others
            font_names = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Droid Sans Fallback', 'Source Han Sans CN']
        
        # 设置matplotlib全局字体
        for font_name in font_names:
            try:
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                matplotlib.rcParams['font.family'] = 'sans-serif'
                matplotlib.rcParams['axes.unicode_minus'] = False
                matplotlib.rcParams['font.size'] = 12
                matplotlib.rcParams['text.antialiased'] = True
                
                # 测试字体是否支持中文
                fig, ax = plt.subplots()
                ax.set_title("测试")
                plt.close(fig)
                print(f"使用字体: {font_name}")
                return
            except:
                continue
        
        print("警告: 未找到支持中文的字体，可能导致图表中文显示为乱码")
        
    def create_widgets(self):
        # 设置适合显示中文的字体
        default_font = ('Microsoft YaHei', 10)  # 使用微软雅黑作为默认字体
        title_font = ('Microsoft YaHei', 22, 'bold')  # 标题字体
        
        # 创建全局样式
        style = ttk.Style()
        style.configure('TButton', font=default_font)
        style.configure('TLabel', font=default_font, background="#f5f5f7")
        style.configure('TFrame', background="#f5f5f7")
        style.configure('TLabelframe', background="#f5f5f7")
        style.configure('TLabelframe.Label', font=('Microsoft YaHei', 12, 'bold'), background="#f5f5f7")
        
        # 标题
        header_frame = tk.Frame(self.root, bg="#f5f5f7", pady=15)
        header_frame.pack(fill=tk.X)
        
        header = tk.Label(header_frame, text="GDP排名动画生成器", font=title_font, bg="#f5f5f7", fg="#1a1a1a")
        header.pack()
        
        subheader = tk.Label(header_frame, text="创建专业级数据可视化动画", font=('Microsoft YaHei', 12), 
                             bg="#f5f5f7", fg="#666666")
        subheader.pack(pady=5)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg="#f5f5f7")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # 左侧设置面板
        settings_frame = tk.Frame(main_frame, bg="#f5f5f7", width=350)
        settings_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        settings_frame.pack_propagate(False)
        
        # 文件选择部分
        file_frame = ttk.LabelFrame(settings_frame, text="数据文件")
        file_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        self.file_label = tk.Label(file_frame, text="未选择文件", font=default_font, bg="#f0f0f0", 
                                  fg="#555555", width=25, anchor="w", padx=10, pady=8)
        self.file_label.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        browse_button = tk.Button(file_frame, text="选择Excel文件", command=self.browse_file, 
                                bg="#0078d7", fg="white", font=default_font, padx=10, pady=5,
                                relief=tk.FLAT, bd=0, activebackground="#005a9e")
        browse_button.pack(fill=tk.X, padx=10, pady=10)
        
        # 基础设置
        basic_frame = ttk.LabelFrame(settings_frame, text="基础设置")
        basic_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        # 标题设置
        tk.Label(basic_frame, text="图表标题:", font=default_font, bg="#f5f5f7").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_var = tk.StringVar(value="全球GDP排名变化")
        tk.Entry(basic_frame, textvariable=self.title_var, width=25, font=default_font).grid(row=0, column=1, padx=10, pady=10, sticky='we')
        
        # 子标题设置
        tk.Label(basic_frame, text="子标题:", font=default_font, bg="#f5f5f7").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.subtitle_var = tk.StringVar(value="数据来源: World Bank")
        tk.Entry(basic_frame, textvariable=self.subtitle_var, width=25, font=default_font).grid(row=1, column=1, padx=10, pady=10, sticky='we')
        
        # 数值单位
        tk.Label(basic_frame, text="数值单位:", font=default_font, bg="#f5f5f7").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.unit_var = tk.StringVar(value="亿美元")
        tk.Entry(basic_frame, textvariable=self.unit_var, width=25, font=default_font).grid(row=2, column=1, padx=10, pady=10, sticky='we')
        
        # 显示数量设置
        tk.Label(basic_frame, text="显示数量:", font=default_font, bg="#f5f5f7").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.top_n_var = tk.IntVar(value=10)
        tk.Spinbox(basic_frame, from_=5, to=20, textvariable=self.top_n_var, width=5, font=default_font).grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        # 动画设置
        animation_frame = ttk.LabelFrame(settings_frame, text="动画设置")
        animation_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        # 帧率设置
        tk.Label(animation_frame, text="动画帧率:", font=default_font, bg="#f5f5f7").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.fps_var = tk.IntVar(value=10)  # 提高默认帧率
        tk.Spinbox(animation_frame, from_=1, to=30, textvariable=self.fps_var, width=5, font=default_font).grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # 过渡效果
        tk.Label(animation_frame, text="过渡效果:", font=default_font, bg="#f5f5f7").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.transition_var = tk.StringVar(value="ease_in_out_cubic")
        ttk.Combobox(animation_frame, textvariable=self.transition_var, width=15, font=default_font,
                     values=["linear", "ease_in_out_cubic", "ease_in_out_sine", "ease_in_cubic", "ease_out_cubic"]).grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # 色彩方案
        tk.Label(animation_frame, text="色彩方案:", font=default_font, bg="#f5f5f7").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.colormap_var = tk.StringVar(value="viridis")
        ttk.Combobox(animation_frame, textvariable=self.colormap_var, width=15, font=default_font,
                     values=["viridis", "plasma", "inferno", "magma", "cividis", "tab10", "tab20"]).grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # 显示数值
        self.show_values_var = tk.BooleanVar(value=True)
        tk.Checkbutton(animation_frame, text="显示数值", variable=self.show_values_var, 
                      font=default_font, bg="#f5f5f7").grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # 显示网格线
        self.show_grid_var = tk.BooleanVar(value=True)
        tk.Checkbutton(animation_frame, text="显示网格线", variable=self.show_grid_var, 
                      font=default_font, bg="#f5f5f7").grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # 显示变化指示器
        self.show_changes_var = tk.BooleanVar(value=True)
        tk.Checkbutton(animation_frame, text="显示变化指示器", variable=self.show_changes_var, 
                      font=default_font, bg="#f5f5f7").grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # 导出设置
        export_frame = ttk.LabelFrame(settings_frame, text="导出设置")
        export_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        # 输出文件名设置
        tk.Label(export_frame, text="输出文件名:", font=default_font, bg="#f5f5f7").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.output_var = tk.StringVar(value="gdp_ranking_animation")
        tk.Entry(export_frame, textvariable=self.output_var, width=25, font=default_font).grid(row=0, column=1, padx=10, pady=10, sticky='we')
        
        # 导出格式
        tk.Label(export_frame, text="导出格式:", font=default_font, bg="#f5f5f7").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.format_var = tk.StringVar(value="GIF")
        ttk.Combobox(export_frame, textvariable=self.format_var, width=15, font=default_font,
                     values=["GIF", "MP4", "PNG序列"]).grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # 分辨率设置
        tk.Label(export_frame, text="分辨率:", font=default_font, bg="#f5f5f7").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.dpi_var = tk.IntVar(value=100)
        tk.Spinbox(export_frame, from_=72, to=300, textvariable=self.dpi_var, width=5, font=default_font).grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # 操作按钮
        button_frame = tk.Frame(settings_frame, bg="#f5f5f7")
        button_frame.pack(fill=tk.X, pady=20)
        
        generate_button = tk.Button(button_frame, text="生成动画", command=self.generate_animation, 
                                   bg="#05a84c", fg="white", font=('Microsoft YaHei', 12, 'bold'),
                                   padx=15, pady=10, relief=tk.FLAT, bd=0, activebackground="#048d40")
        generate_button.pack(fill=tk.X, pady=5)
        
        # 右侧预览和状态面板
        preview_frame = tk.Frame(main_frame, bg="#f5f5f7")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 预览标签
        preview_label = tk.Label(preview_frame, text="预览", font=('Microsoft YaHei', 12, 'bold'), 
                               bg="#f5f5f7", fg="#333333")
        preview_label.pack(anchor="w", pady=(0, 10))
        
        # 预览图像框
        self.preview_container = tk.Frame(preview_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.preview_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.preview_label = tk.Label(self.preview_container, bg="#ffffff")
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # 状态面板
        status_frame = ttk.LabelFrame(preview_frame, text="状态")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="准备就绪. 请选择Excel数据文件...")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, 
                                    font=default_font, bg="#f5f5f7", fg="#333333", 
                                    justify=tk.LEFT, wraplength=400, anchor="w")
        self.status_label.pack(padx=10, pady=10, fill=tk.X)
        
        # 进度条
        progress_frame = tk.Frame(preview_frame, bg="#f5f5f7")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", 
                                       length=100, mode="determinate")
        self.progress.pack(fill=tk.X, pady=5)
        
        # 版权信息
        footer = tk.Label(self.root, text="© " + str(datetime.datetime.now().year) + " GDP排名动画生成器 | 版本 2.0", 
                        font=('Microsoft YaHei', 8), bg="#f5f5f7", fg="#999999")
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
    def browse_file(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.excel_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.status_var.set(f"已选择文件: {os.path.basename(file_path)}")
            self.validate_excel()
            
    def validate_excel(self):
        """验证Excel文件格式是否正确"""
        try:
            df = pd.read_excel(self.excel_path)
            
            # 检查列数
            if len(df.columns) < 3:
                self.status_var.set("错误: Excel文件应至少包含3列 (年份、国家/地区、数值)")
                return False
                
            # 尝试识别列名
            self.status_var.set(f"文件有效。列名: {', '.join(df.columns[:3])}")
            
            # 尝试创建静态预览
            self.create_preview(df)
            
            return True
            
        except Exception as e:
            self.status_var.set(f"验证Excel时出错: {str(e)}")
            return False
    
    def create_preview(self, df):
        """创建静态预览图"""
        try:
            # 确保列名正确
            if len(df.columns) >= 3:
                # 重命名前三列为标准名称
                column_names = list(df.columns)
                df_preview = df.rename(columns={
                    column_names[0]: "year",
                    column_names[1]: "country",
                    column_names[2]: "gdp"
                })
            
            # 预处理数据
            df_preview['gdp'] = pd.to_numeric(df_preview['gdp'], errors='coerce')
            df_preview['year'] = pd.to_numeric(df_preview['year'], errors='coerce')
            df_preview = df_preview.dropna(subset=['gdp', 'year'])
            
            # 获取最新年份
            latest_year = df_preview['year'].max()
            
            # 筛选最新年份数据并获取前N名
            year_data = df_preview[df_preview['year'] == latest_year].sort_values('gdp', ascending=False).head(10)
            
            # 创建预览图
            plt.figure(figsize=(8, 6), dpi=100)
            
            # 使用自定义颜色
            colors = plt.cm.get_cmap(self.colormap_var.get())(np.linspace(0, 0.8, len(year_data)))
            
            bars = plt.barh(year_data['country'][::-1], year_data['gdp'][::-1], color=colors)
            
            # 添加数值标签
            for bar in bars:
                width = bar.get_width()
                plt.text(width + (width*0.02), bar.get_y() + bar.get_height()/2, 
                         f'{width:,.0f}', ha='left', va='center')
            
            # 设置标题
            plt.title(f"{self.title_var.get()} - {int(latest_year)}年", fontsize=14)
            plt.xlabel(f"GDP ({self.unit_var.get()})", fontsize=12)
            
            # 设置网格
            if self.show_grid_var.get():
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                
            plt.tight_layout()
            
            # 保存预览图
            preview_path = "temp_preview.png"
            plt.savefig(preview_path, dpi=100)
            plt.close()
            
            # 显示预览
            self.show_preview(preview_path)
            
            # 删除临时文件
            try:
                os.remove(preview_path)
            except:
                pass
                
        except Exception as e:
            self.status_var.set(f"创建预览时出错: {str(e)}")
    
    def generate_animation(self):
        """生成动画"""
        if not self.excel_path:
            messagebox.showerror("错误", "请先选择Excel文件")
            return
            
        try:
            self.status_var.set("正在读取Excel数据...")
            self.progress["value"] = 10
            self.root.update()
            
            # 读取Excel
            df = pd.read_excel(self.excel_path)
            
            # 确保列名正确
            if len(df.columns) >= 3:
                # 重命名前三列为标准名称
                column_names = list(df.columns)
                df = df.rename(columns={
                    column_names[0]: "year",
                    column_names[1]: "country",
                    column_names[2]: "gdp"
                })
            else:
                raise ValueError("Excel文件格式不正确，需要至少3列数据")
                
            self.status_var.set("正在预处理数据...")
            self.progress["value"] = 20
            self.root.update()
            
            # 预处理数据
            df = self.preprocess_data(df)
            
            self.status_var.set("正在创建动画...")
            self.progress["value"] = 30
            self.root.update()
            
            output_filename = self.output_var.get()
            
            try:
                # 尝试使用pynimate创建动画
                self.create_animation_with_pynimate(df, output_filename)
            except Exception as e:
                self.status_var.set(f"创建动画失败，正在创建静态图表: {str(e)}")
                self.progress["value"] = 70
                self.root.update()
                
                # 备选方案：创建静态图表
                self.create_static_charts(df, output_filename)
                
        except Exception as e:
            self.status_var.set(f"处理过程中出错: {str(e)}")
            messagebox.showerror("错误", f"生成动画失败: {str(e)}")
            self.progress["value"] = 0
    
    def preprocess_data(self, df):
        """预处理数据，处理缺失值和异常值"""
        # 确保年份和GDP是数字类型
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['gdp'] = pd.to_numeric(df['gdp'], errors='coerce')
        
        # 删除缺失值
        df = df.dropna(subset=['year', 'gdp'])
        
        # 确保年份是整数
        df['year'] = df['year'].astype(int)
        
        # 获取TOP-N国家/地区（基于最新年份）
        top_n = self.top_n_var.get()
        latest_year = df['year'].max()
        
        # 获取最新年份排名前N的国家/地区
        top_countries = df[df['year'] == latest_year].nlargest(top_n, 'gdp')['country'].unique()
        
        # 只保留这些国家/地区的数据
        df_filtered = df[df['country'].isin(top_countries)]
        
        # 检测异常值
        for country in df_filtered['country'].unique():
            country_data = df_filtered[df_filtered['country'] == country]
            
            # 如果数据点超过3个，检测异常值
            if len(country_data) > 3:
                mean = country_data['gdp'].mean()
                std = country_data['gdp'].std()
                
                # 标记异常值（超过3个标准差）
                outliers = abs(country_data['gdp'] - mean) > 3*std
                
                if outliers.any():
                    # 获取异常值索引
                    outlier_indices = country_data[outliers].index
                    
                    # 对异常值进行线性插值替换
                    for idx in outlier_indices:
                        year = df.loc[idx, 'year']
                        
                        # 获取前后年份的值
                        prev_data = df_filtered[(df_filtered['country'] == country) & (df_filtered['year'] < year)].sort_values('year', ascending=False)
                        next_data = df_filtered[(df_filtered['country'] == country) & (df_filtered['year'] > year)].sort_values('year')
                        
                        if not prev_data.empty and not next_data.empty:
                            prev_year = prev_data.iloc[0]['year']
                            prev_gdp = prev_data.iloc[0]['gdp']
                            next_year = next_data.iloc[0]['year']
                            next_gdp = next_data.iloc[0]['gdp']
                            
                            # 线性插值
                            df.loc[idx, 'gdp'] = prev_gdp + (next_gdp - prev_gdp) * (year - prev_year) / (next_year - prev_year)
        
        return df
    
    def create_animation_with_pynimate(self, df, output_filename):
        """使用pynimate创建动态条形图"""
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun'] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 数据预处理
        # 将数据透视为宽格式
        df_pivot = df.pivot(index='year', columns='country', values='gdp').fillna(0)
        
        # 创建Canvas，设置合适的宽高比例
        cnv = nim.Canvas(figsize=(16, 9), dpi=self.dpi_var.get())
        
        # 创建BarDatafier对象
        datafier = nim.BarDatafier(
            df_pivot,
            time_format="%Y",
            ip_freq="YE"
        )
        
        # 创建Barhplot对象
        bar = nim.Barhplot(datafier)
        
        # 设置颜色方案
        colormap = plt.cm.get_cmap(self.colormap_var.get())
        colors = colormap(np.linspace(0, 0.8, len(df['country'].unique())))
        bar.set_colors(colors)
        
        # 设置时间标签回调函数
        bar.set_time(callback=lambda i, datafier: f"{datafier.data.index[i].year}年")
        
        # 设置标题和子标题
        bar.set_title(self.title_var.get(), fontsize=20, fontweight='bold')
        bar.set_subtitle(self.subtitle_var.get(), fontsize=14, color='#666666')
        
        # 设置标签
        unit = self.unit_var.get()
        bar.set_xlabel(f'GDP ({unit})', fontsize=14)
        
        # 设置过渡效果
        bar.set_transition(self.transition_var.get())
        
        # 自定义数字格式化函数
        def format_number(x, pos):
            return f'{x:,.0f}'
        
        # 获取轴对象并设置格式化器
        ax = bar.ax
        ax.xaxis.set_major_formatter(FuncFormatter(format_number))
        
        # 设置网格线
        if self.show_grid_var.get():
            ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # 添加数值标签
        if self.show_values_var.get():
            bar.add_value_texts(fmt="{x:,.0f}", fontsize=12, padding=5)
        
        # 添加变化指示器
        if self.show_changes_var.get():
            bar.add_rank_indicator(enable_arrow=True, arrow_size=25)
        
        # 添加水印/署名
        ax.text(0.98, 0.02, f"制作: GDP排名动画生成器", 
                transform=ax.transAxes, ha='right', va='bottom', 
                fontsize=10, color='#999999', alpha=0.7)
        
        # 增加一些边距，避免文字被裁剪
        bar.set_margins(left=0.25, right=0.85, top=0.85, bottom=0.15)
        
        # 添加到Canvas并创建动画
        cnv.add_plot(bar)
        cnv.animate()
        
        # 根据选择的格式保存动画
        format_option = self.format_var.get()
        
        if format_option == "GIF":
            # 保存为GIF
            gif_path = f"{output_filename}.gif"
            cnv.save(gif_path, fps=self.fps_var.get())
            self.output_path = gif_path
            self.status_var.set(f"动画已创建并保存为 {gif_path}")
            
        elif format_option == "MP4":
            # 保存为MP4
            mp4_path = f"{output_filename}.mp4"
            cnv.save(mp4_path, fps=self.fps_var.get())
            self.output_path = mp4_path
            self.status_var.set(f"动画已创建并保存为 {mp4_path}")
            
        elif format_option == "PNG序列":
            # 创建文件夹
            folder_path = f"{output_filename}_frames"
            os.makedirs(folder_path, exist_ok=True)
            
            # 保存为PNG序列
            cnv.save(f"{folder_path}/frame_%04d.png")
            self.output_path = folder_path
            self.status_var.set(f"PNG序列已保存至 {folder_path} 文件夹")
        
        self.progress["value"] = 100
        
        # 显示成功消息
        messagebox.showinfo("成功", f"动画已成功创建!\n保存位置: {self.output_path}")
        
        # 预览第一帧
        self.show_preview(self.output_path)
        
        # 清理内存
        plt.close('all')
        gc.collect()
        
    def create_static_charts(self, df, output_filename):
        """创建静态图表作为备选方案"""
        # 重新设置字体以确保中文显示正确
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 12
        
        # 获取所有不同的年份
        years = sorted(df['year'].unique())
        
        # 创建文件夹保存图表
        folder_path = f"{output_filename}_static_charts"
        os.makedirs(folder_path, exist_ok=True)
        
        # 创建颜色映射
        colormap = plt.cm.get_cmap(self.colormap_var.get())
        
        # 获取顶级国家(基于最新年份)
        latest_year = max(years)
        top_countries = df[df['year'] == latest_year].sort_values('gdp', ascending=False)['country'].unique()[:self.top_n_var.get()]
        
        # 为每一年创建一个条形图
        for i, year in enumerate(years):
            # 更新进度
            progress_value = 50 + (i / len(years) * 50)  # 进度从50%到100%
            self.progress["value"] = progress_value
            self.status_var.set(f"正在生成 {year}年 图表...")
            self.root.update()
            
            # 筛选当年数据并排序
            year_data = df[df['year'] == year]
            
            # 只保留顶级国家
            year_data = year_data[year_data['country'].isin(top_countries)]
            
            # 按GDP值排序
            year_data = year_data.sort_values('gdp', ascending=False)
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(16, 9), dpi=self.dpi_var.get())
            
            # 生成颜色
            colors = [colormap(i/len(top_countries)) for i in range(len(top_countries))]
            
            # 创建水平条形图
            bars = ax.barh(year_data['country'][::-1], year_data['gdp'][::-1], color=colors)
            
            # 添加数值标签
            if self.show_values_var.get():
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + (width*0.02), bar.get_y() + bar.get_height()/2, 
                            f'{width:,.0f}', ha='left', va='center', fontsize=12)
            
            # 设置标题和标签
            ax.set_title(f"{self.title_var.get()} - {int(year)}年", fontsize=20, fontweight='bold')
            ax.set_xlabel(f'GDP ({self.unit_var.get()})', fontsize=14)
            
            # 添加子标题
            ax.text(0.5, 0.97, self.subtitle_var.get(), 
                    transform=ax.transAxes, ha='center', fontsize=14, color='#666666')
            
            # 添加网格线
            if self.show_grid_var.get():
                ax.grid(axis='x', linestyle='--', alpha=0.7)
            
            # 格式化x轴标签
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:,.0f}'))
            
            # 添加水印/署名
            ax.text(0.98, 0.02, f"制作: GDP排名动画生成器", 
                    transform=ax.transAxes, ha='right', va='bottom', 
                    fontsize=10, color='#999999', alpha=0.7)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图表
            chart_path = f"{folder_path}/{year}.png"
            plt.savefig(chart_path)
            plt.close()
        
        # 尝试创建GIF
        try:
            # 收集所有图像
            images = []
            for year in years:
                image_path = f"{folder_path}/{year}.png"
                images.append(imageio.imread(image_path))
                
            # 创建GIF
            gif_path = f"{output_filename}.gif"
            imageio.mimsave(gif_path, images, fps=self.fps_var.get())
            
            self.status_var.set(f"静态图表已转换为GIF: {gif_path}")
            self.output_path = gif_path
            
            # 显示成功消息
            messagebox.showinfo("成功", f"静态图表已转换为GIF!\n保存位置: {gif_path}")
            
            # 预览GIF
            self.show_preview(gif_path)
            
        except Exception as e:
            self.status_var.set(f"无法创建GIF，静态图表已保存至文件夹: {folder_path}\n错误: {str(e)}")
            messagebox.showinfo("完成", f"静态图表已保存至文件夹: {folder_path}")
            
            # 预览第一张图
            first_image = f"{folder_path}/{years[0]}.png"
            self.show_preview(first_image)
        
        self.progress["value"] = 100
    
    def show_preview(self, image_path):
        """在UI中显示图像预览"""
        try:
            # 判断是文件还是文件夹
            if os.path.isdir(image_path):
                # 如果是文件夹，寻找第一个图像文件
                files = [f for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                if files:
                    files.sort()
                    image_path = os.path.join(image_path, files[0])
                else:
                    raise FileNotFoundError("文件夹中没有找到图像文件")
            
            # 打开图像
            img = Image.open(image_path)
            
            # 获取预览容器的尺寸
            container_width = self.preview_container.winfo_width()
            container_height = self.preview_container.winfo_height()
            
            # 如果容器尺寸为0（可能是因为窗口还未完全渲染），使用默认尺寸
            if container_width <= 1:
                container_width = 400
            if container_height <= 1:
                container_height = 300
            
            # 调整大小以适应容器，保持宽高比
            img_width, img_height = img.size
            ratio = min(container_width / img_width, container_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # 调整图像大小
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 显示图像
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # 保持引用，防止被垃圾回收
            
        except Exception as e:
            self.status_var.set(f"无法预览图像: {str(e)}")
            # 清除预览
            self.preview_label.config(image=None)
            self.preview_label.image = None

if __name__ == "__main__":
    root = tk.Tk()
    app = GDPAnimationApp(root)
    root.mainloop()



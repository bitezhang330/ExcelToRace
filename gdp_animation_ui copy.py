import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用Agg后端，不需要GUI
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageTk
import pynimate as nim
import platform
from matplotlib.font_manager import FontProperties

class GDPAnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP排名动画生成器")
        self.root.geometry("900x700")  # 稍微增大窗口尺寸
        self.root.configure(bg="#f5f5f5")
        
        # 设置窗口图标（如果有的话）
        # self.root.iconbitmap("icon.ico")  # 如果有图标可以取消注释此行
        
        # 初始化路径变量
        self.excel_path = None
        self.output_path = "output_animation.gif"
        self.static_output_path = "output_static.png"
        
        # 设置中文字体
        self.setup_fonts()
        
        # 设置应用主题颜色
        self.theme_color = "#3498db"  # 蓝色主题
        self.bg_color = "#f5f5f5"
        
        # 设置ttk样式
        self.setup_styles()
        
        # 创建UI组件
        self.create_widgets()
        
    def setup_fonts(self):
        """设置适合当前操作系统的中文字体"""
        system = platform.system()
        
        if system == 'Windows':
            font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']
        elif system == 'Darwin':  # macOS
            font_names = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS']
        else:  # Linux and others
            font_names = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Droid Sans Fallback']
        
        # 设置matplotlib全局字体
        for font_name in font_names:
            try:
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                matplotlib.rcParams['font.family'] = 'sans-serif'
                matplotlib.rcParams['axes.unicode_minus'] = False
                # 测试字体是否支持中文
                fig, ax = plt.subplots()
                ax.set_title("测试")
                plt.close(fig)
                print(f"使用字体: {font_name}")
                return
            except:
                continue
        
        print("警告: 未找到支持中文的字体，可能导致图表中文显示为乱码")
        
    def setup_styles(self):
        """设置ttk控件的样式"""
        style = ttk.Style()
        
        # 设置按钮样式
        style.configure('TButton', font=('Microsoft YaHei', 10))
        style.configure('Generate.TButton', font=('Microsoft YaHei', 12, 'bold'))
        
        # 设置进度条样式
        style.configure("Horizontal.TProgressbar", 
                       background=self.theme_color,
                       troughcolor="#e0e0e0",
                       borderwidth=0,
                       thickness=10)
        
    def create_widgets(self):
        # 设置适合显示中文的字体
        default_font = ('Microsoft YaHei', 10)  # 使用微软雅黑作为默认字体
        title_font = ('Microsoft YaHei', 22, 'bold')  # 使用微软雅黑作为标题字体
        
        # 设置主题色
        accent_color = "#3498db"  # 蓝色主题
        button_color = "#2980b9"
        success_color = "#27ae60"
        
        self.root.configure(bg=self.bg_color)
        
        # 标题
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=15)
        header_frame.pack(fill=tk.X)
        
        header = tk.Label(header_frame, text="GDP排名动画生成器", font=title_font, bg=self.bg_color, fg=self.theme_color)
        header.pack()
        
        subtitle = tk.Label(header_frame, text="可视化全球经济数据变化趋势", font=('Microsoft YaHei', 12), bg=self.bg_color, fg="#555")
        subtitle.pack(pady=5)
        
        # 创建主体框架
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # 文件选择部分
        file_frame = tk.LabelFrame(main_frame, text="数据文件", font=('Microsoft YaHei', 12, 'bold'), 
                                 bg=self.bg_color, fg=self.theme_color, padx=15, pady=15)
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_label = tk.Label(file_frame, text="未选择文件", font=default_font, 
                                  bg=self.bg_color, fg="#555555", width=50)
        self.file_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        style = ttk.Style()
        style.configure('Browse.TButton', font=('Microsoft YaHei', 10))
        
        browse_button = ttk.Button(file_frame, text="浏览...", 
                                 command=self.browse_file,
                                 style='Browse.TButton')
        browse_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # 设置部分
        settings_frame = tk.LabelFrame(main_frame, text="配置选项", font=('Microsoft YaHei', 12, 'bold'), 
                                     bg=self.bg_color, fg=self.theme_color, padx=15, pady=15)
        settings_frame.pack(fill=tk.X, pady=10)
        
        # 创建两列设置
        left_settings = tk.Frame(settings_frame, bg=self.bg_color)
        left_settings.grid(row=0, column=0, padx=10, sticky='w')
        
        right_settings = tk.Frame(settings_frame, bg=self.bg_color)
        right_settings.grid(row=0, column=1, padx=10, sticky='w')
        
        # 标题设置
        tk.Label(left_settings, text="图表标题:", font=default_font, bg=self.bg_color).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_var = tk.StringVar(value="全球GDP排名变化")
        title_entry = ttk.Entry(left_settings, textvariable=self.title_var, width=30, font=default_font)
        title_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # 帧率设置
        tk.Label(left_settings, text="动画帧率:", font=default_font, bg=self.bg_color).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.fps_var = tk.IntVar(value=2)
        fps_spinbox = ttk.Spinbox(left_settings, from_=1, to=10, textvariable=self.fps_var, width=5, font=default_font)
        fps_spinbox.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # 输出文件名设置
        tk.Label(right_settings, text="输出文件名:", font=default_font, bg=self.bg_color).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.output_var = tk.StringVar(value="output_animation")
        output_entry = ttk.Entry(right_settings, textvariable=self.output_var, width=30, font=default_font)
        output_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # 提示说明
        tip_label = tk.Label(settings_frame, text="提示: 确保Excel文件第一列为年份，第二列为国家/地区名称，第三列为GDP值",
                            font=('Microsoft YaHei', 9), bg=self.bg_color, fg="#888")
        tip_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='w')
        
        # 操作按钮
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=15)
        
        # 配置生成按钮样式
        style.configure('Generate.TButton', 
                       font=('Microsoft YaHei', 12, 'bold'))
        
        generate_button = ttk.Button(button_frame, text="生成动画", 
                                   command=self.generate_animation,
                                   style='Generate.TButton')
        generate_button.pack(pady=10)
        
        # 状态显示区域
        status_frame = tk.LabelFrame(main_frame, text="执行状态", font=('Microsoft YaHei', 12, 'bold'), 
                                    bg=self.bg_color, fg=self.theme_color, padx=15, pady=15)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="等待操作...")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, 
                                    font=default_font, bg=self.bg_color, fg="#333333", 
                                    justify=tk.LEFT, wraplength=700)
        self.status_label.pack(padx=10, pady=10, fill=tk.X)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", 
                                       length=100, mode="determinate")
        self.progress.pack(fill=tk.X, padx=20, pady=10)
        
        # 预览图像框
        preview_frame = tk.LabelFrame(main_frame, text="预览", font=('Microsoft YaHei', 12, 'bold'), 
                                     bg=self.bg_color, fg=self.theme_color, padx=15, pady=15)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        self.preview_label = tk.Label(preview_frame, bg="#e5e5e5", height=10)
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 版权信息
        footer = tk.Label(self.root, text="© 2023 GDP排名动画生成器", 
                        font=('Microsoft YaHei', 8), bg=self.bg_color, fg="#999")
        footer.pack(side=tk.BOTTOM, pady=5)
        
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
                self.status_var.set("错误: Excel文件应至少包含3列 (年份、国家/类别、数值)")
                return False
                
            # 尝试识别列名
            self.status_var.set(f"文件有效。列名: {', '.join(df.columns[:3])}")
            return True
            
        except Exception as e:
            self.status_var.set(f"验证Excel时出错: {str(e)}")
            return False
    
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
                
            self.status_var.set("正在处理数据...")
            self.progress["value"] = 30
            self.root.update()
            
            # 确保年份是数字类型
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            df = df.dropna(subset=['year'])
            df['year'] = df['year'].astype(int)
            
            # 确保GDP是数字
            df['gdp'] = pd.to_numeric(df['gdp'], errors='coerce')
            df = df.dropna(subset=['gdp'])
            
            # 为动画重新整理数据
            self.status_var.set("正在准备动画数据...")
            self.progress["value"] = 50
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
            
    def create_animation_with_pynimate(self, df, output_filename):
        """使用pynimate创建动态条形图"""
        # 数据预处理
        df_pivot = df.pivot(index='year', columns='country', values='gdp').fillna(0)
        
        # 创建Canvas和BarDatafier对象
        cnv = nim.Canvas(figsize=(15, 8))  # 使用与原始文件相同的图表尺寸
        
        # 确保图表使用正确的中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun'] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        datafier = nim.BarDatafier(
            df_pivot,
            time_format="%Y",
            ip_freq="YE"
        )
        
        # 创建Barhplot对象
        bar = nim.Barhplot(datafier)
        
        # 设置时间标签回调函数
        bar.set_time(callback=lambda i, datafier: f"{datafier.data.index[i].year}年")
        
        # 设置标题
        bar.set_title(self.title_var.get())
        
        # 设置标签
        bar.set_xlabel('数值')
        
        # 添加到Canvas并创建动画
        cnv.add_plot(bar)
        cnv.animate()
        
        # 保存动画
        gif_path = f"{output_filename}.gif"
        cnv.save(gif_path, fps=self.fps_var.get())
        
        # 为每一年创建静态PNG图表
        years = sorted(df['year'].unique())
        png_paths = []
        
        for year in years:
            # 筛选当年数据并排序
            year_data = df[df['year'] == year].sort_values('gdp', ascending=False).head(15)
            
            # 创建新的图表
            plt.figure(figsize=(15, 8))
            
            # 创建水平条形图
            bars = plt.barh(year_data['country'][::-1], year_data['gdp'][::-1])
            
            # 添加数值标签
            for bar in bars:
                width = bar.get_width()
                plt.text(width + (width*0.01), bar.get_y() + bar.get_height()/2, 
                        f'{width:,.0f}', ha='left', va='center')
            
            # 设置标题和标签
            plt.title(f'{self.title_var.get()} - {int(year)}年')
            plt.xlabel('GDP (单位: 亿美元)')
            
            # 保存当年的PNG
            year_png_path = f"{output_filename}_{year}.png"
            plt.savefig(year_png_path)
            plt.close()
            
            png_paths.append(year_png_path)
        
        # 更新状态信息
        png_files_str = "\n".join([os.path.basename(path) for path in png_paths])
        status_message = f"已生成：\n动画文件：{os.path.basename(gif_path)}\n静态图表：\n{png_files_str}"
        self.status_var.set(status_message)
        self.progress["value"] = 100
        
        # 显示成功消息
        messagebox.showinfo("成功", f"动画已保存为 {gif_path}\n已为每年生成单独的PNG文件")
        
        # 预览第一帧
        self.show_preview(gif_path)
        
    def create_static_charts(self, df, output_filename):
        """创建静态图表作为备选方案"""
        # 获取所有不同的年份
        years = sorted(df['year'].unique())
        
        # 重新设置字体以确保中文显示正确
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置美观的风格
        plt.style.use('seaborn-v0_8-pastel')
        
        # 为每一年创建一个条形图
        fig, axes = plt.subplots(len(years), 1, figsize=(16, 5*len(years)), dpi=120)
        fig.patch.set_facecolor('#f8f8f8')  # 设置图表背景色
        fig.suptitle(self.title_var.get(), fontsize=24, fontweight='bold')
        
        # 颜色映射，使图表更美观
        cmap = plt.cm.viridis
        
        # 如果只有一年数据，确保axes是可迭代的
        if len(years) == 1:
            axes = [axes]
        
        for i, year in enumerate(years):
            # 筛选当年数据并排序
            year_data = df[df['year'] == year].sort_values('gdp', ascending=False).head(15)
            
            # 创建水平条形图
            bars = axes[i].barh(year_data['country'][::-1], year_data['gdp'][::-1], 
                                color=[cmap(j/15) for j in range(len(year_data))],
                                edgecolor='white', alpha=0.9, height=0.7)
            
            # 添加数值标签
            for bar in bars:
                width = bar.get_width()
                axes[i].text(width + (width*0.01), bar.get_y() + bar.get_height()/2, 
                           f'{width:,.0f}', ha='left', va='center', fontsize=12, 
                           fontweight='bold')
            
            # 设置标题和标签
            axes[i].set_title(f'{int(year)}年', fontsize=20, pad=20)
            axes[i].set_xlabel('GDP (单位: 亿美元)', fontsize=14)
            
            # 去掉顶部和右侧边框
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            
            # 设置背景颜色
            axes[i].set_facecolor('#f8f8f8')
            
            # 添加网格线
            axes[i].grid(axis='x', linestyle='--', alpha=0.3)
            
            # 设置y轴标签字体
            for label in axes[i].get_yticklabels():
                label.set_fontsize(12)
                
            # 设置x轴刻度格式
            axes[i].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        
        # 添加水印
        fig.text(0.95, 0.05, '数据来源: Excel导入', 
                fontsize=12, color='gray', alpha=0.5,
                ha='right', va='bottom')
            
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        static_path = f"{output_filename}_static.png"
        plt.savefig(static_path, dpi=120, bbox_inches='tight')
        plt.close()
        
        self.status_var.set(f"静态图表已保存为 {static_path}")
        self.progress["value"] = 100
        
        # 显示成功消息
        messagebox.showinfo("成功", f"静态图表已保存为 {static_path}")
        
        # 预览图表
        self.show_preview(static_path)
    
    def show_preview(self, image_path):
        """在UI中显示图像预览"""
        try:
            # 打开图像
            img = Image.open(image_path)
            
            # 调整大小以适应预览区域
            width = 700
            ratio = width / img.width
            height = int(img.height * ratio)
            
            img = img.resize((width, height), Image.LANCZOS)
            
            # 显示图像
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # 保持引用，防止被垃圾回收
            
        except Exception as e:
            self.status_var.set(f"无法预览图像: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GDPAnimationApp(root)
    root.mainloop()

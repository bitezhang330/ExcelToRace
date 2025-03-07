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
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.excel_path = None
        self.output_path = "output_animation.gif"
        self.static_output_path = "output_static.png"
        
        # 设置中文字体
        self.setup_fonts()
        
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
        
    def create_widgets(self):
        # 设置适合显示中文的字体
        default_font = ('SimSun', 10)  # 使用宋体作为默认字体
        title_font = ('SimHei', 20, 'bold')  # 使用黑体作为标题字体
        
        # 标题
        header = tk.Label(self.root, text="GDP排名动画生成器", font=title_font, bg="#f0f0f0")
        header.pack(pady=20)
        
        # 框架容器
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 文件选择部分
        file_frame = tk.LabelFrame(main_frame, text="数据文件", font=('SimHei', 12), bg="#f0f0f0")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_label = tk.Label(file_frame, text="未选择文件", font=default_font, bg="#f0f0f0", fg="#555555", width=50)
        self.file_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        browse_button = tk.Button(file_frame, text="浏览...", 
                                 command=self.browse_file, 
                                 bg="#4CAF50", fg="white",
                                 width=10, font=('SimHei', 10))
        browse_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # 设置部分
        settings_frame = tk.LabelFrame(main_frame, text="设置", font=('SimHei', 12), bg="#f0f0f0")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # 标题设置
        tk.Label(settings_frame, text="图表标题:", font=default_font, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_var = tk.StringVar(value="全球GDP排名变化")
        tk.Entry(settings_frame, textvariable=self.title_var, width=30, font=default_font).grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # 帧率设置
        tk.Label(settings_frame, text="动画帧率:", font=default_font, bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.fps_var = tk.IntVar(value=2)
        tk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.fps_var, width=5, font=default_font).grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # 输出文件名设置
        tk.Label(settings_frame, text="输出文件名:", font=default_font, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.output_var = tk.StringVar(value="output_animation")
        tk.Entry(settings_frame, textvariable=self.output_var, width=30, font=default_font).grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # 操作按钮
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=20)
        
        generate_button = tk.Button(button_frame, text="生成动画", 
                                   command=self.generate_animation, 
                                   bg="#2196F3", fg="white",
                                   width=15, height=2, font=('SimHei', 12))
        generate_button.pack(pady=10)
        
        # 状态显示
        status_frame = tk.LabelFrame(main_frame, text="状态", font=('SimHei', 12), bg="#f0f0f0")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="等待操作...")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, 
                                    font=default_font, bg="#f0f0f0", fg="#333333", 
                                    justify=tk.LEFT, wraplength=700)
        self.status_label.pack(padx=10, pady=10, fill=tk.X)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", 
                                       length=100, mode="determinate")
        self.progress.pack(fill=tk.X, padx=20, pady=10)
        
        # 预览图像框
        self.preview_label = tk.Label(main_frame, bg="#e0e0e0", height=10)
        self.preview_label.pack(fill=tk.X, padx=20, pady=10)
        
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
        cnv = nim.Canvas(figsize=(15, 8))
        
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
        
        self.status_var.set(f"动画已创建并保存为 {gif_path}")
        self.progress["value"] = 100
        
        # 显示成功消息
        messagebox.showinfo("成功", f"动画已保存为 {gif_path}")
        
        # 预览第一帧
        self.show_preview(gif_path)
        
    def create_static_charts(self, df, output_filename):
        """创建静态图表作为备选方案"""
        # 获取所有不同的年份
        years = sorted(df['year'].unique())
        
        # 重新设置字体以确保中文显示正确
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 为每一年创建一个条形图
        fig, axes = plt.subplots(len(years), 1, figsize=(12, 5*len(years)))
        fig.suptitle(self.title_var.get(), fontsize=16)
        
        # 如果只有一年数据，确保axes是可迭代的
        if len(years) == 1:
            axes = [axes]
        
        for i, year in enumerate(years):
            # 筛选当年数据并排序
            year_data = df[df['year'] == year].sort_values('gdp', ascending=False).head(10)
            
            # 创建水平条形图
            bars = axes[i].barh(year_data['country'][::-1], year_data['gdp'][::-1])
            
            # 添加数值标签
            for bar in bars:
                width = bar.get_width()
                axes[i].text(width + (width*0.02), bar.get_y() + bar.get_height()/2, 
                            f'{width:,.0f}', ha='left', va='center')
            
            # 设置标题和标签
            axes[i].set_title(f'{int(year)}年', fontsize=14)
            axes[i].set_xlabel('数值', fontsize=12)
            
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        static_path = f"{output_filename}_static.png"
        plt.savefig(static_path)
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

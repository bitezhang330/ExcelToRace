import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QComboBox, QWidget, 
                            QTableView, QHeaderView, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QAbstractTableModel
import pandas as pd
import bar_chart_race as bcr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# 创建一个表格模型来显示Excel数据
class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.column_types = ['未设置'] * len(data.columns)

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self._data.columns[section])
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(self._data.index[section])
        return None
    
    def setColumnType(self, column, type_name):
        if 0 <= column < len(self.column_types):
            self.column_types[column] = type_name
            
    def getColumnType(self, column):
        if 0 <= column < len(self.column_types):
            return self.column_types[column]
        return '未设置'

# 主窗口类
class BarChartRaceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("条形图赛跑动画生成器")
        self.setGeometry(100, 100, 1000, 600)
        self.df = None
        self.model = None
        
        self.initUI()
        
    def initUI(self):
        # 创建主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # 创建顶部按钮布局
        top_layout = QHBoxLayout()
        
        # 添加导入Excel按钮
        self.import_btn = QPushButton("导入Excel")
        self.import_btn.clicked.connect(self.importExcel)
        top_layout.addWidget(self.import_btn)
        
        # 添加生成GIF按钮
        self.generate_btn = QPushButton("生成GIF")
        self.generate_btn.clicked.connect(self.generateGIF)
        self.generate_btn.setEnabled(False)
        top_layout.addWidget(self.generate_btn)
        
        # 将顶部布局添加到主布局
        main_layout.addLayout(top_layout)
        
        # 添加表格视图
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(QLabel("数据预览:"))
        main_layout.addWidget(self.table_view)
        
        # 添加列类型设置区域
        column_layout = QHBoxLayout()
        column_layout.addWidget(QLabel("选择列:"))
        
        self.column_selector = QComboBox()
        self.column_selector.currentIndexChanged.connect(self.updateTypeSelector)
        column_layout.addWidget(self.column_selector)
        
        column_layout.addWidget(QLabel("设置类型:"))
        self.type_selector = QComboBox()
        self.type_selector.addItems(['未设置', '国家', '年份', '数值'])
        self.type_selector.currentTextChanged.connect(self.setColumnType)
        column_layout.addWidget(self.type_selector)
        
        main_layout.addLayout(column_layout)
        
        # 添加动画参数设置
        param_layout = QHBoxLayout()
        
        param_layout.addWidget(QLabel("动画标题:"))
        self.title_input = QLabel("全球GDP前十国家排名变化")
        param_layout.addWidget(self.title_input)
        
        param_layout.addWidget(QLabel("显示数量:"))
        self.bars_selector = QComboBox()
        self.bars_selector.addItems(['5', '10', '15', '20'])
        self.bars_selector.setCurrentText('10')
        param_layout.addWidget(self.bars_selector)
        
        param_layout.addWidget(QLabel("每帧时长(毫秒):"))
        self.period_selector = QComboBox()
        self.period_selector.addItems(['500', '1000', '1500', '2000'])
        self.period_selector.setCurrentText('1000')
        param_layout.addWidget(self.period_selector)
        
        main_layout.addLayout(param_layout)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        self.setCentralWidget(main_widget)
    
    def importExcel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls);;CSV Files (*.csv)")
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.df = pd.read_csv(file_path)
                else:
                    self.df = pd.read_excel(file_path)
                
                self.model = PandasModel(self.df)
                self.table_view.setModel(self.model)
                
                # 更新列选择器
                self.column_selector.clear()
                self.column_selector.addItems([str(col) for col in self.df.columns])
                
                self.generate_btn.setEnabled(True)
                
                QMessageBox.information(self, "成功", f"已成功导入数据，共{len(self.df)}行，{len(self.df.columns)}列")
            
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入文件时出错:\n{str(e)}")
    
    def updateTypeSelector(self, index):
        if self.model and 0 <= index < len(self.model.column_types):
            current_type = self.model.getColumnType(index)
            self.type_selector.setCurrentText(current_type)
    
    def setColumnType(self, type_name):
        if self.model:
            current_column = self.column_selector.currentIndex()
            if current_column >= 0:
                self.model.setColumnType(current_column, type_name)
    
    def generateGIF(self):
        if self.df is None or self.model is None:
            QMessageBox.warning(self, "警告", "请先导入数据")
            return
        
        # 获取列类型映射
        country_col = None
        year_col = None
        value_col = None
        
        for i, col in enumerate(self.df.columns):
            col_type = self.model.getColumnType(i)
            if col_type == '国家':
                country_col = col
            elif col_type == '年份':
                year_col = col
            elif col_type == '数值':
                value_col = col
        
        if country_col is None or year_col is None or value_col is None:
            QMessageBox.warning(self, "警告", "请设置正确的列类型（国家、年份、数值）")
            return
        
        try:
            # 准备数据
            self.progress_bar.setValue(10)
            
            # 透视表转换
            df_pivot = self.df.pivot(index=year_col, columns=country_col, values=value_col)
            
            self.progress_bar.setValue(40)
            
            # 设置matplotlib使用微软雅黑字体
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 设置图形大小
            plt.figure(figsize=(12, 8), dpi=144)
            
            output_file, _ = QFileDialog.getSaveFileName(self, "保存GIF文件", "", "GIF Files (*.gif)")
            if not output_file:
                return
            
            if not output_file.lower().endswith('.gif'):
                output_file += '.gif'
                
            self.progress_bar.setValue(60)
            
            # 使用bar_chart_race生成动画
            bcr.bar_chart_race(
                df=df_pivot,
                filename=output_file,
                orientation='h',
                sort='desc',
                n_bars=int(self.bars_selector.currentText()),
                title=self.title_input.text(),
                period_length=int(self.period_selector.currentText())
            )
            
            self.progress_bar.setValue(100)
            
            QMessageBox.information(self, "成功", f"GIF动画已成功生成并保存到:\n{output_file}")
            
        except Exception as e:
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "错误", f"生成GIF时发生错误:\n{str(e)}")


# 添加可编辑的标题
class BarChartRaceApp(BarChartRaceApp):
    def initUI(self):
        super().initUI()
        
        # 修改标题为可编辑的文本框
        param_layout = self.findChild(QHBoxLayout)
        if param_layout:
            # 删除原有标题标签
            for i in range(param_layout.count()):
                item = param_layout.itemAt(i)
                if isinstance(item.widget(), QLabel) and item.widget().text() == "全球GDP前十国家排名变化":
                    item.widget().deleteLater()
                    break
            
            # 替换为文本框
            from PyQt5.QtWidgets import QLineEdit
            self.title_input = QLineEdit("全球GDP前十国家排名变化")
            # 找到"动画标题:"标签后的位置
            for i in range(param_layout.count()):
                item = param_layout.itemAt(i)
                if isinstance(item.widget(), QLabel) and item.widget().text() == "动画标题:":
                    param_layout.insertWidget(i+1, self.title_input)
                    break

    def generateGIF(self):
        # 修正generateGIF方法中的标题获取
        if hasattr(self, 'title_input'):
            title = self.title_input.text()
        else:
            title = "全球GDP前十国家排名变化"
        
        # 其余代码保持不变
        super().generateGIF()


# 启动应用
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarChartRaceApp()
    window.show()
    sys.exit(app.exec_())

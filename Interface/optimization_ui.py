"""
系统优化界面
提供图形化的系统优化和监控界面
"""
import sys
import time
from datetime import datetime
from typing import Dict, List
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                            QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                            QSystemTrayIcon, QMenu, QStyle, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtChart import QChart, QChartView, QLineSeries

from Core.task_scheduler import TaskScheduler
from Tools.system_optimizer import SystemOptimizer
from Tools.system_tools import SystemTools

class OptimizationWorker(QThread):
    """优化工作线程"""
    finished = pyqtSignal(list)
    progress = pyqtSignal(int, str)
    
    def __init__(self, optimizer, optimization_type):
        super().__init__()
        self.optimizer = optimizer
        self.optimization_type = optimization_type
        
    def run(self):
        try:
            total_steps = 5
            results = []
            
            if self.optimization_type == 'all' or self.optimization_type == 'services':
                self.progress.emit(20, "正在优化系统服务...")
                results.extend(self.optimizer.optimize_services())
                
            if self.optimization_type == 'all' or self.optimization_type == 'power':
                self.progress.emit(40, "正在优化电源设置...")
                results.extend(self.optimizer.optimize_power_plan())
                
            if self.optimization_type == 'all' or self.optimization_type == 'network':
                self.progress.emit(60, "正在优化网络设置...")
                results.extend(self.optimizer.optimize_network())
                
            if self.optimization_type == 'all' or self.optimization_type == 'performance':
                self.progress.emit(80, "正在优化系统性能...")
                results.extend(self.optimizer.optimize_system_performance())
                
            if self.optimization_type == 'all' or self.optimization_type == 'privacy':
                self.progress.emit(90, "正在优化隐私设置...")
                results.extend(self.optimizer.optimize_privacy())
                
            self.progress.emit(100, "优化完成")
            self.finished.emit(results)
            
        except Exception as e:
            self.progress.emit(0, f"优化失败: {str(e)}")
            self.finished.emit([f"错误: {str(e)}"])

class SystemMonitorChart(QChartView):
    """系统监控图表"""
    def __init__(self, title=""):
        super().__init__()
        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        
        self.chart.createDefaultAxes()
        self.chart.axes(Qt.Horizontal)[0].setRange(0, 60)
        self.chart.axes(Qt.Vertical)[0].setRange(0, 100)
        
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        
    def update_data(self, value):
        """更新数据"""
        points = self.series.pointsVector()
        if len(points) > 60:
            points = points[1:]
        points.append(QPointF(len(points), value))
        self.series.replace(points)

class OptimizationUI(QMainWindow):
    """系统优化主界面"""
    def __init__(self):
        super().__init__()
        self.optimizer = SystemOptimizer()
        self.system_tools = SystemTools()
        self.task_scheduler = TaskScheduler()
        
        self.init_ui()
        self.init_system_tray()
        self.init_monitoring()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle('系统优化工具')
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建选项卡
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # 优化选项卡
        optimization_tab = QWidget()
        optimization_layout = QVBoxLayout(optimization_tab)
        
        # 优化按钮
        buttons_layout = QHBoxLayout()
        optimization_layout.addLayout(buttons_layout)
        
        optimize_all_btn = QPushButton('一键优化')
        optimize_all_btn.clicked.connect(lambda: self.start_optimization('all'))
        buttons_layout.addWidget(optimize_all_btn)
        
        optimize_services_btn = QPushButton('优化服务')
        optimize_services_btn.clicked.connect(lambda: self.start_optimization('services'))
        buttons_layout.addWidget(optimize_services_btn)
        
        optimize_power_btn = QPushButton('优化电源')
        optimize_power_btn.clicked.connect(lambda: self.start_optimization('power'))
        buttons_layout.addWidget(optimize_power_btn)
        
        optimize_network_btn = QPushButton('优化网络')
        optimize_network_btn.clicked.connect(lambda: self.start_optimization('network'))
        buttons_layout.addWidget(optimize_network_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        optimization_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel()
        optimization_layout.addWidget(self.status_label)
        
        # 结果表格
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(['时间', '优化结果'])
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        optimization_layout.addWidget(self.results_table)
        
        tabs.addTab(optimization_tab, '系统优化')
        
        # 监控选项卡
        monitoring_tab = QWidget()
        monitoring_layout = QVBoxLayout(monitoring_tab)
        
        # CPU使用率图表
        self.cpu_chart = SystemMonitorChart("CPU使用率")
        monitoring_layout.addWidget(self.cpu_chart)
        
        # 内存使用率图表
        self.memory_chart = SystemMonitorChart("内存使用率")
        monitoring_layout.addWidget(self.memory_chart)
        
        tabs.addTab(monitoring_tab, '系统监控')
        
        # 任务调度选项卡
        schedule_tab = QWidget()
        schedule_layout = QVBoxLayout(schedule_tab)
        
        # 任务列表
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(['任务名称', '状态', '上次运行', '下次运行'])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        schedule_layout.addWidget(self.task_table)
        
        tabs.addTab(schedule_tab, '任务调度')
        
        # 设置深色主题
        self.set_dark_theme()
        
    def init_system_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction('显示主窗口')
        show_action.triggered.connect(self.show)
        
        optimize_action = tray_menu.addAction('一键优化')
        optimize_action.triggered.connect(lambda: self.start_optimization('all'))
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction('退出')
        quit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def init_monitoring(self):
        """初始化系统监控"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring)
        self.monitor_timer.start(1000)  # 每秒更新一次
        
        self.schedule_timer = QTimer()
        self.schedule_timer.timeout.connect(self.update_task_schedule)
        self.schedule_timer.start(60000)  # 每分钟更新一次
        
    def set_dark_theme(self):
        """设置深色主题"""
        dark_palette = QPalette()
        
        # 设置颜色
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
        
    def start_optimization(self, optimization_type):
        """开始优化"""
        self.worker = OptimizationWorker(self.optimizer, optimization_type)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.optimization_finished)
        self.worker.start()
        
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        
    def optimization_finished(self, results):
        """优化完成"""
        # 添加结果到表格
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        time_item = QTableWidgetItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.results_table.setItem(row, 0, time_item)
        
        results_text = '\n'.join(results)
        results_item = QTableWidgetItem(results_text)
        self.results_table.setItem(row, 1, results_item)
        
        # 显示通知
        self.tray_icon.showMessage(
            '系统优化',
            f'优化完成，共{len(results)}项优化',
            QSystemTrayIcon.Information,
            3000
        )
        
    def update_monitoring(self):
        """更新监控数据"""
        # 更新CPU使用率
        cpu_percent = psutil.cpu_percent()
        self.cpu_chart.update_data(cpu_percent)
        
        # 更新内存使用率
        memory = psutil.virtual_memory()
        self.memory_chart.update_data(memory.percent)
        
    def update_task_schedule(self):
        """更新任务调度信息"""
        self.task_table.setRowCount(0)
        
        tasks = self.task_scheduler.get_task_status()
        for task in tasks:
            row = self.task_table.rowCount()
            self.task_table.insertRow(row)
            
            self.task_table.setItem(row, 0, QTableWidgetItem(task['name']))
            self.task_table.setItem(row, 1, QTableWidgetItem(
                '启用' if task['enabled'] else '禁用'))
            self.task_table.setItem(row, 2, QTableWidgetItem(
                task['last_run'] or '从未运行'))
            self.task_table.setItem(row, 3, QTableWidgetItem(
                task['next_run'] or '未计划'))
                
    def closeEvent(self, event):
        """关闭事件处理"""
        if self.tray_icon.isVisible():
            QMessageBox.information(self, '系统优化工具',
                                  '程序将继续在系统托盘运行。')
            self.hide()
            event.ignore()

def main():
    app = QApplication(sys.argv)
    ui = OptimizationUI()
    ui.show()
    sys.exit(app.exec_())

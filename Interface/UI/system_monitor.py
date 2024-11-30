"""
系统监控模块
显示详细的系统性能监控信息
"""
import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QTabWidget, QFrame, QTableWidget, QTableWidgetItem,
                            QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis

class PerformanceChart(QWidget):
    """性能图表组件"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        
        layout = QVBoxLayout(self)
        
        # 创建图表
        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # 创建数据系列
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        
        # 创建坐标轴
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, 60)  # 显示60秒的数据
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setTitleText("Time (s)")
        
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, 100)
        self.axis_y.setLabelFormat("%d")
        self.axis_y.setTitleText("Usage (%)")
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        
        # 创建图表视图
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout.addWidget(chart_view)
        
        self.data_points = []
        
    def add_data_point(self, value):
        """添加数据点"""
        self.data_points.append(value)
        if len(self.data_points) > 60:
            self.data_points = self.data_points[-60:]
            
        # 更新数据系列
        self.series.clear()
        for i, point in enumerate(self.data_points):
            self.series.append(i, point)

class ProcessTable(QTableWidget):
    """进程表格组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_table()
        
    def _init_table(self):
        """初始化表格"""
        # 设置列
        columns = ['PID', 'Name', 'CPU %', 'Memory %', 'Disk I/O', 'Network']
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        
        # 设置列宽
        header = self.horizontalHeader()
        for i in range(len(columns)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
            
        # 设置样式
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        
    def update_processes(self, processes):
        """更新进程列表"""
        self.setRowCount(len(processes))
        for row, process in enumerate(processes):
            self.setItem(row, 0, QTableWidgetItem(str(process['pid'])))
            self.setItem(row, 1, QTableWidgetItem(process['name']))
            self.setItem(row, 2, QTableWidgetItem(f"{process['cpu_percent']}%"))
            self.setItem(row, 3, QTableWidgetItem(f"{process['memory_percent']}%"))
            self.setItem(row, 4, QTableWidgetItem(process['disk_io']))
            self.setItem(row, 5, QTableWidgetItem(process['network']))

class SystemMonitor(QWidget):
    """系统监控类"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._init_ui()
        
    def _init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # CPU标签页
        cpu_tab = QWidget()
        cpu_layout = QVBoxLayout(cpu_tab)
        self.cpu_chart = PerformanceChart('CPU Usage')
        cpu_layout.addWidget(self.cpu_chart)
        tab_widget.addTab(cpu_tab, 'CPU')
        
        # 内存标签页
        memory_tab = QWidget()
        memory_layout = QVBoxLayout(memory_tab)
        self.memory_chart = PerformanceChart('Memory Usage')
        memory_layout.addWidget(self.memory_chart)
        tab_widget.addTab(memory_tab, 'Memory')
        
        # 磁盘标签页
        disk_tab = QWidget()
        disk_layout = QVBoxLayout(disk_tab)
        self.disk_chart = PerformanceChart('Disk Usage')
        disk_layout.addWidget(self.disk_chart)
        tab_widget.addTab(disk_tab, 'Disk')
        
        # 网络标签页
        network_tab = QWidget()
        network_layout = QVBoxLayout(network_tab)
        self.network_chart = PerformanceChart('Network Usage')
        network_layout.addWidget(self.network_chart)
        tab_widget.addTab(network_tab, 'Network')
        
        # 进程标签页
        process_tab = QWidget()
        process_layout = QVBoxLayout(process_tab)
        self.process_table = ProcessTable()
        process_layout.addWidget(self.process_table)
        tab_widget.addTab(process_tab, 'Processes')
        
        layout.addWidget(tab_widget)
        
        # 设置更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_monitor)
        self.update_timer.start(1000)  # 每秒更新一次
        
    def _update_monitor(self):
        """更新监控数据"""
        # TODO: 从系统获取实际数据
        # 这里使用示例数据
        
        # 更新图表
        self.cpu_chart.add_data_point(30)
        self.memory_chart.add_data_point(45)
        self.disk_chart.add_data_point(60)
        self.network_chart.add_data_point(25)
        
        # 更新进程表格
        example_processes = [
            {
                'pid': 1234,
                'name': 'example.exe',
                'cpu_percent': 5.2,
                'memory_percent': 3.1,
                'disk_io': '1.2 MB/s',
                'network': '0.5 MB/s'
            },
            # 添加更多示例进程...
        ]
        self.process_table.update_processes(example_processes)

"""
仪表板模块
显示系统概览和关键指标
"""
import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QFrame, QProgressBar, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QColor

class SystemMetricWidget(QFrame):
    """系统指标组件"""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(title_label)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setTextVisible(True)
        layout.addWidget(self.progress)
        
        # 详细信息
        self.detail_label = QLabel()
        layout.addWidget(self.detail_label)
        
    def update_value(self, value, detail_text=""):
        """更新显示值"""
        self.progress.setValue(int(value))
        self.detail_label.setText(detail_text)

class CircularProgressWidget(QWidget):
    """圆形进度指示器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setMinimumSize(100, 100)
        
    def setValue(self, value):
        """设置值"""
        self.value = value
        self.update()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景圆
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 200, 200))
        painter.drawEllipse(10, 10, 80, 80)
        
        # 绘制进度圆弧
        painter.setBrush(QColor(0, 150, 255))
        span_angle = -self.value * 360 / 100
        painter.drawPie(10, 10, 80, 80, 90 * 16, span_angle * 16)
        
        # 绘制文本
        painter.setPen(Qt.black)
        painter.setFont(QFont('Arial', 16))
        painter.drawText(0, 0, 100, 100, Qt.AlignCenter, f"{self.value}%")

class Dashboard(QWidget):
    """仪表板类"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._init_ui()
        
    def _init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 系统概览部分
        overview_frame = QFrame()
        overview_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        overview_layout = QHBoxLayout(overview_frame)
        
        # CPU使用率
        self.cpu_widget = CircularProgressWidget()
        cpu_container = QWidget()
        cpu_layout = QVBoxLayout(cpu_container)
        cpu_layout.addWidget(QLabel('CPU Usage'))
        cpu_layout.addWidget(self.cpu_widget)
        overview_layout.addWidget(cpu_container)
        
        # 内存使用率
        self.memory_widget = CircularProgressWidget()
        memory_container = QWidget()
        memory_layout = QVBoxLayout(memory_container)
        memory_layout.addWidget(QLabel('Memory Usage'))
        memory_layout.addWidget(self.memory_widget)
        overview_layout.addWidget(memory_container)
        
        # 磁盘使用率
        self.disk_widget = CircularProgressWidget()
        disk_container = QWidget()
        disk_layout = QVBoxLayout(disk_container)
        disk_layout.addWidget(QLabel('Disk Usage'))
        disk_layout.addWidget(self.disk_widget)
        overview_layout.addWidget(disk_container)
        
        layout.addWidget(overview_frame)
        
        # 详细指标网格
        metrics_grid = QGridLayout()
        
        # CPU详细信息
        self.cpu_metric = SystemMetricWidget('CPU Details')
        metrics_grid.addWidget(self.cpu_metric, 0, 0)
        
        # 内存详细信息
        self.memory_metric = SystemMetricWidget('Memory Details')
        metrics_grid.addWidget(self.memory_metric, 0, 1)
        
        # 磁盘详细信息
        self.disk_metric = SystemMetricWidget('Disk Details')
        metrics_grid.addWidget(self.disk_metric, 1, 0)
        
        # 网络详细信息
        self.network_metric = SystemMetricWidget('Network Details')
        metrics_grid.addWidget(self.network_metric, 1, 1)
        
        layout.addLayout(metrics_grid)
        
        # 设置更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_metrics)
        self.update_timer.start(1000)  # 每秒更新一次
        
    def _update_metrics(self):
        """更新指标显示"""
        # TODO: 从系统获取实际数据
        # 这里使用示例数据
        
        # 更新圆形进度指示器
        self.cpu_widget.setValue(30)
        self.memory_widget.setValue(45)
        self.disk_widget.setValue(60)
        
        # 更新详细指标
        self.cpu_metric.update_value(30, "Temperature: 45°C\nProcesses: 120")
        self.memory_metric.update_value(45, "Used: 4.5GB\nAvailable: 11.5GB")
        self.disk_metric.update_value(60, "Used: 120GB\nFree: 80GB")
        self.network_metric.update_value(25, "Upload: 1.2MB/s\nDownload: 2.5MB/s")

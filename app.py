import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTabWidget, QPushButton, QLabel, 
                           QSystemTrayIcon, QMenu, QProgressBar, QTableWidget,
                           QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtChart import QChart, QChartView, QLineSeries

from Core.base_system import BaseSystem
from Core.task_scheduler import TaskScheduler
from Core.ai_system import AISystem
from Tools.system_tools import SystemTools
from Tools.system_optimizer import SystemOptimizer
from Interface.optimization_ui import MonitorPanel, TaskManager, OptimizerPanel

class OSAI_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_system = BaseSystem()
        self.task_scheduler = TaskScheduler()
        self.ai_system = AISystem()
        self.system_tools = SystemTools()
        self.system_optimizer = SystemOptimizer()
        
        self.init_ui()
        self.init_system_tray()
        self.init_monitoring()
        self.apply_theme()
        
    def init_ui(self):
        """初始化主界面"""
        self.setWindowTitle('OS_AI 系统管理器')
        self.setMinimumSize(1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建顶部状态栏
        self.status_bar = self.create_status_bar()
        layout.addWidget(self.status_bar)
        
        # 创建选项卡
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # 添加功能选项卡
        self.monitor_panel = MonitorPanel()
        tabs.addTab(self.monitor_panel, '系统监控')
        
        self.optimizer_panel = OptimizerPanel()
        tabs.addTab(self.optimizer_panel, '系统优化')
        
        self.task_manager = TaskManager()
        tabs.addTab(self.task_manager, '任务管理')
        
    def create_status_bar(self):
        """创建状态栏"""
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        
        # CPU状态
        self.cpu_label = QLabel('CPU: 0%')
        status_layout.addWidget(self.cpu_label)
        
        # 内存状态
        self.memory_label = QLabel('内存: 0%')
        status_layout.addWidget(self.memory_label)
        
        # 磁盘状态
        self.disk_label = QLabel('磁盘: 0%')
        status_layout.addWidget(self.disk_label)
        
        return status_widget
        
    def init_system_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        tray_menu = QMenu()
        
        # 添加托盘菜单项
        show_action = tray_menu.addAction('显示主窗口')
        show_action.triggered.connect(self.show)
        
        optimize_action = tray_menu.addAction('一键优化')
        optimize_action.triggered.connect(self.quick_optimize)
        
        exit_action = tray_menu.addAction('退出')
        exit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def init_monitoring(self):
        """初始化系统监控"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_system_status)
        self.monitor_timer.start(1000)  # 每秒更新一次
        
    def update_system_status(self):
        """更新系统状态"""
        status = self.base_system.monitor_resources()
        
        # 更新状态栏
        self.cpu_label.setText(f'CPU: {status["cpu"]}%')
        self.memory_label.setText(f'内存: {status["memory"]}%')
        self.disk_label.setText(f'磁盘: {status["disk"]}%')
        
        # 更新监控面板
        self.monitor_panel.update_charts(status)
        
    def quick_optimize(self):
        """快速优化系统"""
        self.system_optimizer.optimize_system_performance()
        
    def apply_theme(self):
        """应用深色主题"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabWidget {
                background-color: #2d2d2d;
                border: none;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 8px 20px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #3d3d3d;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QLabel {
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
            }
        """)

def main():
    app = QApplication(sys.argv)
    window = OSAI_App()
    window.show()
    sys.exit(app.exec_())

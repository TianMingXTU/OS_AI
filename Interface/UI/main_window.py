"""
主窗口模块
实现系统的主要图形界面
"""
import sys
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                            QSystemTrayIcon, QMenu, QStatusBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._init_ui()
        
    def _init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('OS_AI System')
        self.setMinimumSize(1024, 768)
        
        # 创建中央窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # 创建侧边栏
        self._create_sidebar()
        
        # 创建主内容区
        self._create_main_content()
        
        # 创建状态栏
        self._create_status_bar()
        
        # 创建系统托盘
        self._create_system_tray()
        
        # 设置定时器更新界面
        self._setup_timers()
        
    def _create_sidebar(self):
        """创建侧边栏"""
        sidebar = QWidget()
        sidebar.setMaximumWidth(200)
        sidebar.setMinimumWidth(150)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # 添加导航按钮
        nav_buttons = [
            ('Dashboard', self._show_dashboard),
            ('System Monitor', self._show_system_monitor),
            ('Process Manager', self._show_process_manager),
            ('File Manager', self._show_file_manager),
            ('Settings', self._show_settings)
        ]
        
        for text, callback in nav_buttons:
            button = QPushButton(text)
            button.setFont(QFont('Arial', 10))
            button.clicked.connect(callback)
            sidebar_layout.addWidget(button)
            
        sidebar_layout.addStretch()
        self.main_layout.addWidget(sidebar)
        
    def _create_main_content(self):
        """创建主内容区"""
        self.content_stack = QStackedWidget()
        
        # 创建各个页面
        self.dashboard = self._create_dashboard()
        self.system_monitor = self._create_system_monitor()
        self.process_manager = self._create_process_manager()
        self.file_manager = self._create_file_manager()
        self.settings = self._create_settings()
        
        # 添加页面到堆栈
        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.system_monitor)
        self.content_stack.addWidget(self.process_manager)
        self.content_stack.addWidget(self.file_manager)
        self.content_stack.addWidget(self.settings)
        
        self.main_layout.addWidget(self.content_stack)
        
    def _create_dashboard(self):
        """创建仪表板页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加系统概览
        overview_label = QLabel('System Overview')
        overview_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(overview_label)
        
        # TODO: 添加更多仪表板组件
        
        return page
        
    def _create_system_monitor(self):
        """创建系统监控页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加监控组件
        monitor_label = QLabel('System Monitor')
        monitor_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(monitor_label)
        
        # TODO: 添加系统监控组件
        
        return page
        
    def _create_process_manager(self):
        """创建进程管理器页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加进程管理组件
        process_label = QLabel('Process Manager')
        process_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(process_label)
        
        # TODO: 添加进程管理组件
        
        return page
        
    def _create_file_manager(self):
        """创建文件管理器页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加文件管理组件
        file_label = QLabel('File Manager')
        file_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(file_label)
        
        # TODO: 添加文件管理组件
        
        return page
        
    def _create_settings(self):
        """创建设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加设置组件
        settings_label = QLabel('Settings')
        settings_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(settings_label)
        
        # TODO: 添加设置组件
        
        return page
        
    def _create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 添加状态信息
        self.cpu_label = QLabel('CPU: 0%')
        self.memory_label = QLabel('Memory: 0%')
        self.disk_label = QLabel('Disk: 0%')
        
        self.status_bar.addWidget(self.cpu_label)
        self.status_bar.addWidget(self.memory_label)
        self.status_bar.addWidget(self.disk_label)
        
    def _create_system_tray(self):
        """创建系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        # TODO: 设置托盘图标
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction('Show')
        show_action.triggered.connect(self.show)
        hide_action = tray_menu.addAction('Hide')
        hide_action.triggered.connect(self.hide)
        quit_action = tray_menu.addAction('Quit')
        quit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def _setup_timers(self):
        """设置定时器"""
        # 更新状态栏信息的定时器
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(1000)  # 每秒更新一次
        
    def _update_status(self):
        """更新状态信息"""
        # TODO: 从系统获取实际数据
        self.cpu_label.setText('CPU: 30%')
        self.memory_label.setText('Memory: 45%')
        self.disk_label.setText('Disk: 60%')
        
    def _show_dashboard(self):
        """显示仪表板"""
        self.content_stack.setCurrentIndex(0)
        
    def _show_system_monitor(self):
        """显示系统监控"""
        self.content_stack.setCurrentIndex(1)
        
    def _show_process_manager(self):
        """显示进程管理器"""
        self.content_stack.setCurrentIndex(2)
        
    def _show_file_manager(self):
        """显示文件管理器"""
        self.content_stack.setCurrentIndex(3)
        
    def _show_settings(self):
        """显示设置"""
        self.content_stack.setCurrentIndex(4)
        
    def closeEvent(self, event):
        """关闭事件处理"""
        self.hide()
        event.ignore()  # 不直接关闭，而是最小化到托盘

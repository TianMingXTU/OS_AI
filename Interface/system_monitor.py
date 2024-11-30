"""
系统监控界面
使用PyQt5实现简洁高效的系统监控
"""
import sys
import psutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QProgressBar)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('系统监控')
        self.setMinimumSize(600, 400)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建监控组件
        self.create_monitor_widgets(layout)
        
        # 创建定时器更新数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # 每秒更新一次
        
    def create_monitor_widgets(self, layout):
        """创建监控组件"""
        # CPU使用率
        cpu_layout = QHBoxLayout()
        self.cpu_label = QLabel('CPU使用率:')
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMinimum(0)
        self.cpu_bar.setMaximum(100)
        cpu_layout.addWidget(self.cpu_label)
        cpu_layout.addWidget(self.cpu_bar)
        layout.addLayout(cpu_layout)
        
        # 内存使用率
        memory_layout = QHBoxLayout()
        self.memory_label = QLabel('内存使用率:')
        self.memory_bar = QProgressBar()
        self.memory_bar.setMinimum(0)
        self.memory_bar.setMaximum(100)
        memory_layout.addWidget(self.memory_label)
        memory_layout.addWidget(self.memory_bar)
        layout.addLayout(memory_layout)
        
        # 磁盘使用率
        disk_layout = QHBoxLayout()
        self.disk_label = QLabel('磁盘使用率:')
        self.disk_bar = QProgressBar()
        self.disk_bar.setMinimum(0)
        self.disk_bar.setMaximum(100)
        disk_layout.addWidget(self.disk_label)
        disk_layout.addWidget(self.disk_bar)
        layout.addLayout(disk_layout)
        
        # 网络使用情况
        self.network_label = QLabel('网络使用情况:')
        layout.addWidget(self.network_label)
        
        # 进程信息
        self.process_label = QLabel('主要进程:')
        layout.addWidget(self.process_label)
        
        # 系统建议
        self.suggestion_label = QLabel('系统建议:')
        layout.addWidget(self.suggestion_label)
        
    def update_stats(self):
        """更新系统状态"""
        try:
            # 更新CPU使用率
            cpu_percent = psutil.cpu_percent()
            self.cpu_bar.setValue(int(cpu_percent))
            self.cpu_label.setText(f'CPU使用率: {cpu_percent}%')
            self.update_bar_color(self.cpu_bar, cpu_percent)
            
            # 更新内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_bar.setValue(int(memory_percent))
            self.memory_label.setText(
                f'内存使用率: {memory_percent}% (已用: {self.format_bytes(memory.used)} / 总共: {self.format_bytes(memory.total)})'
            )
            self.update_bar_color(self.memory_bar, memory_percent)
            
            # 更新磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            self.disk_bar.setValue(int(disk_percent))
            self.disk_label.setText(
                f'磁盘使用率: {disk_percent}% (可用: {self.format_bytes(disk.free)})'
            )
            self.update_bar_color(self.disk_bar, disk_percent)
            
            # 更新网络信息
            net_io = psutil.net_io_counters()
            self.network_label.setText(
                f'网络使用情况:\n'
                f'发送: {self.format_bytes(net_io.bytes_sent)}\n'
                f'接收: {self.format_bytes(net_io.bytes_recv)}'
            )
            
            # 更新进程信息
            processes = []
            for proc in sorted(
                psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                key=lambda p: p.info['cpu_percent'],
                reverse=True
            )[:5]:
                try:
                    processes.append(
                        f"{proc.info['name']}: CPU {proc.info['cpu_percent']}%, "
                        f"内存 {proc.info['memory_percent']:.1f}%"
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            self.process_label.setText(
                '主要进程:\n' + '\n'.join(processes)
            )
            
            # 更新系统建议
            suggestions = []
            if cpu_percent > 80:
                suggestions.append("CPU使用率过高，建议关闭不必要的进程")
            if memory_percent > 80:
                suggestions.append("内存使用率过高，建议释放内存")
            if disk_percent > 90:
                suggestions.append("磁盘空间不足，建议清理磁盘")
                
            self.suggestion_label.setText(
                '系统建议:\n' + '\n'.join(suggestions) if suggestions 
                else '系统运行正常'
            )
            
        except Exception as e:
            print(f"更新状态失败: {str(e)}")
            
    def format_bytes(self, bytes):
        """格式化字节大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} PB"
        
    def update_bar_color(self, bar, value):
        """更新进度条颜色"""
        palette = QPalette()
        if value < 60:
            color = QColor(0, 255, 0)  # 绿色
        elif value < 80:
            color = QColor(255, 255, 0)  # 黄色
        else:
            color = QColor(255, 0, 0)  # 红色
        palette.setColor(QPalette.Highlight, color)
        bar.setPalette(palette)
        
def main():
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec_())

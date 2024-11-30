"""
语音命令示例
演示如何使用语音处理模块
"""
import sys
import os
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QTextEdit, QLabel
)
from PyQt5.QtCore import Qt, QTimer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interface.Interaction.voice_handler import VoiceHandler, VoiceCommandType

class VoiceDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.voice_handler = VoiceHandler()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Voice Command Demo')
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加控制按钮
        self.listen_button = QPushButton('Start Listening')
        self.listen_button.clicked.connect(self.toggle_listening)
        layout.addWidget(self.listen_button)
        
        # 添加状态标签
        self.status_label = QLabel('Status: Not listening')
        layout.addWidget(self.status_label)
        
        # 添加命令显示区域
        self.command_display = QTextEdit()
        self.command_display.setReadOnly(True)
        layout.addWidget(self.command_display)
        
        # 添加说明标签
        instruction_label = QLabel(
            'Supported Commands:\n'
            '- "open [app]"\n'
            '- "close [app]"\n'
            '- "search for [query]"\n'
            '- "volume [level]"\n'
            '- "system [command]"'
        )
        layout.addWidget(instruction_label)
        
        # 模拟音频输入的定时器
        self.audio_timer = QTimer()
        self.audio_timer.timeout.connect(self.simulate_audio_input)
        
    def toggle_listening(self):
        """切换监听状态"""
        if self.voice_handler.is_active():
            self.voice_handler.stop_listening()
            self.listen_button.setText('Start Listening')
            self.status_label.setText('Status: Not listening')
            self.audio_timer.stop()
        else:
            self.voice_handler.start_listening()
            self.listen_button.setText('Stop Listening')
            self.status_label.setText('Status: Listening...')
            self.audio_timer.start(2000)  # 每2秒模拟一次音频输入
            
    def simulate_audio_input(self):
        """模拟音频输入"""
        # 这里我们模拟一些示例命令
        commands = [
            "open notepad",
            "close browser",
            "search for weather",
            "volume up",
            "system shutdown"
        ]
        
        # 随机选择一个命令
        import random
        text = random.choice(commands)
        
        # 创建模拟的音频数据
        audio_data = np.random.random(1000)
        
        # 处理音频数据
        result = self.voice_handler.process_audio(audio_data)
        
        if result:
            message = (
                f"Recognized Text: {result['text']}\n"
                f"Command Type: {result['command_type'].value}\n"
                f"Parameters: {result['parameters']}\n"
                f"-------------------"
            )
            self.command_display.append(message)
            
def main():
    app = QApplication(sys.argv)
    demo = VoiceDemo()
    demo.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

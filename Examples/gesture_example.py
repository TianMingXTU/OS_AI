"""
手势识别示例
演示如何使用手势处理模块
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interface.Interaction.gesture_handler import GestureHandler, GestureType, GestureState

class GestureDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gesture_handler = GestureHandler()
        self.last_point = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Gesture Recognition Demo')
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加标签显示识别结果
        self.gesture_label = QLabel('No gesture detected')
        self.gesture_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.gesture_label)
        
        # 添加说明标签
        instruction_label = QLabel(
            'Draw gestures with mouse:\n'
            '← Swipe Left\n'
            '→ Swipe Right\n'
            '↑ Swipe Up\n'
            '↓ Swipe Down'
        )
        instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_label)
        
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.gesture_handler.handle_touch_event(
                event.x(),
                event.y(),
                GestureState.STARTED
            )
            
    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if event.buttons() & Qt.LeftButton and self.last_point:
            self.gesture_handler.handle_touch_event(
                event.x(),
                event.y(),
                GestureState.UPDATED
            )
            
            # 获取当前手势
            current_gesture = self.gesture_handler.get_current_gesture()
            if current_gesture:
                gesture_type, _ = current_gesture
                self.gesture_label.setText(f'Detected: {gesture_type.value}')
                
    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton and self.last_point:
            self.gesture_handler.handle_touch_event(
                event.x(),
                event.y(),
                GestureState.ENDED
            )
            self.last_point = None
            
def main():
    app = QApplication(sys.argv)
    demo = GestureDemo()
    demo.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

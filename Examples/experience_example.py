"""
体验优化示例
演示如何使用体验优化模块
"""
import sys
import os
import time
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QTextEdit, QProgressBar, QLabel,
    QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QTimer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interface.Experience.experience_optimizer import ExperienceOptimizer, ExperienceMetric
from Interface.UI.theme import AITheme

class MetricCard(QFrame):
    """指标卡片组件"""
    def __init__(self, metric: ExperienceMetric, parent=None):
        super().__init__(parent)
        self.metric = metric
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 设置卡片样式
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet(f"""
            MetricCard {{
                background-color: {AITheme.COLORS['surface']};
                border-radius: {AITheme.RADIUS['lg']}px;
                padding: {AITheme.SPACING['md']}px;
                margin: {AITheme.SPACING['sm']}px;
            }}
        """)
        
        # 标题
        self.title = QLabel(self.metric.value.replace('_', ' ').title())
        self.title.setFont(AITheme.FONTS['subtitle'])
        layout.addWidget(self.title)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        layout.addWidget(self.progress)
        
        # 状态标签
        self.status = QLabel("Status: Unknown")
        self.status.setFont(AITheme.FONTS['caption'])
        layout.addWidget(self.status)

class ExperienceDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.experience_optimizer = ExperienceOptimizer()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('AI体验优化系统')
        self.setGeometry(100, 100, 1200, 800)
        
        # 应用AI主题
        AITheme.apply_theme(self)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 添加标题
        title = QLabel('AI体验优化系统')
        title.setFont(AITheme.FONTS['title'])
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # 创建指标卡片网格
        metrics_layout = QHBoxLayout()
        self.metric_cards = {}
        
        for metric in ExperienceMetric:
            card = MetricCard(metric)
            metrics_layout.addWidget(card)
            self.metric_cards[metric] = card
            
        main_layout.addLayout(metrics_layout)
        
        # 添加控制面板
        control_panel = QFrame()
        control_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {AITheme.COLORS['surface']};
                border-radius: {AITheme.RADIUS['lg']}px;
                padding: {AITheme.SPACING['md']}px;
                margin: {AITheme.SPACING['md']}px;
            }}
        """)
        control_layout = QHBoxLayout()
        control_panel.setLayout(control_layout)
        
        # 添加反馈按钮
        self.feedback_button = QPushButton('模拟用户反馈')
        self.feedback_button.clicked.connect(self.simulate_feedback)
        control_layout.addWidget(self.feedback_button)
        
        main_layout.addWidget(control_panel)
        
        # 添加报告显示区域
        report_frame = QFrame()
        report_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AITheme.COLORS['surface']};
                border-radius: {AITheme.RADIUS['lg']}px;
                padding: {AITheme.SPACING['md']}px;
                margin: {AITheme.SPACING['md']}px;
            }}
        """)
        report_layout = QVBoxLayout()
        report_frame.setLayout(report_layout)
        
        report_title = QLabel('系统报告')
        report_title.setFont(AITheme.FONTS['subtitle'])
        report_layout.addWidget(report_title)
        
        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        self.report_display.setFont(AITheme.FONTS['body'])
        report_layout.addWidget(self.report_display)
        
        main_layout.addWidget(report_frame)
        
        # 设置定时器
        self.metric_timer = QTimer()
        self.metric_timer.timeout.connect(self.simulate_metrics)
        self.metric_timer.start(1000)
        
        self.report_timer = QTimer()
        self.report_timer.timeout.connect(self.update_report)
        self.report_timer.start(5000)
        
    def simulate_metrics(self):
        """模拟指标变化"""
        for metric in ExperienceMetric:
            # 生成模拟数据
            if metric == ExperienceMetric.RESPONSE_TIME:
                value = random.uniform(50, 600)
            elif metric == ExperienceMetric.ERROR_RATE:
                value = random.uniform(0, 0.15)
            else:
                value = random.uniform(0.3, 1.0)
                
            # 记录指标
            self.experience_optimizer.record_metric(metric, value)
            
            # 更新UI
            card = self.metric_cards[metric]
            status = self.experience_optimizer.get_metric_status(metric)
            
            if metric == ExperienceMetric.RESPONSE_TIME:
                normalized = max(0, min(100, (600 - value) / 5))
            elif metric == ExperienceMetric.ERROR_RATE:
                normalized = max(0, min(100, (0.15 - value) / 0.15 * 100))
            else:
                normalized = value * 100
                
            card.progress.setValue(int(normalized))
            card.status.setText(f"状态: {status['status']}")
            
            # 设置进度条颜色
            if status['status'] == 'good':
                color = AITheme.COLORS['success']
            elif status['status'] == 'acceptable':
                color = AITheme.COLORS['warning']
            else:
                color = AITheme.COLORS['error']
                
            card.progress.setStyleSheet(f"""
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: {AITheme.RADIUS['sm']}px;
                }}
            """)
            
    def simulate_feedback(self):
        """模拟用户反馈"""
        feedback_types = [
            "系统响应较慢",
            "界面不够流畅",
            "用户体验很好",
            "需要更好的错误提示",
            "新功能很实用"
        ]
        
        feedback = {
            'timestamp': datetime.now(),
            'issue': random.choice(feedback_types),
            'satisfaction': random.uniform(0.3, 1.0)
        }
        
        self.experience_optimizer.record_user_feedback(feedback)
        self.report_display.append(f"新反馈: {feedback['issue']}")
        
    def update_report(self):
        """更新体验报告"""
        report = self.experience_optimizer.get_experience_report()
        
        # 格式化报告显示
        report_text = "=== 体验优化报告 ===\n"
        report_text += f"时间: {report['timestamp']}\n\n"
        
        report_text += "指标状态:\n"
        for metric, status in report['metrics'].items():
            report_text += f"- {metric}: {status['status']}\n"
            
        if report['user_feedback']:
            report_text += "\n用户反馈统计:\n"
            report_text += f"反馈总数: {report['user_feedback']['total_count']}\n"
            report_text += f"平均满意度: {report['user_feedback']['average_satisfaction']:.2f}\n"
            
            if report['user_feedback']['common_issues']:
                report_text += "常见问题:\n"
                for issue in report['user_feedback']['common_issues']:
                    report_text += f"- {issue['issue']} ({issue['count']} 次)\n"
                    
        if report['recommendations']:
            report_text += "\n系统建议:\n"
            for rec in report['recommendations']:
                report_text += f"- {rec['metric']}: {rec['suggestion']}\n"
                
        report_text += "\n" + "="*30 + "\n"
        
        self.report_display.setText(report_text)
        
def main():
    app = QApplication(sys.argv)
    demo = ExperienceDemo()
    demo.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

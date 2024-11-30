"""
AI风格UI主题
定义系统的视觉风格和主题
"""
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtCore import Qt

class AITheme:
    """AI主题类"""
    
    # 颜色方案
    COLORS = {
        'primary': '#2D5AF0',      # 主色调 - 深蓝色
        'secondary': '#8C61FF',    # 次要色 - 紫色
        'accent': '#00D4FF',       # 强调色 - 亮蓝色
        'background': '#1A1B1E',   # 背景色 - 深灰色
        'surface': '#2D2E32',      # 表面色 - 中灰色
        'text': '#FFFFFF',         # 文本色 - 白色
        'text_secondary': '#B3B3B3', # 次要文本 - 浅灰色
        'success': '#4CAF50',      # 成功色 - 绿色
        'warning': '#FFC107',      # 警告色 - 黄色
        'error': '#F44336',        # 错误色 - 红色
        'info': '#2196F3'          # 信息色 - 蓝色
    }
    
    # 字体设置
    FONTS = {
        'title': QFont('Segoe UI', 24, QFont.Bold),
        'subtitle': QFont('Segoe UI', 18, QFont.DemiBold),
        'body': QFont('Segoe UI', 12),
        'caption': QFont('Segoe UI', 10),
        'button': QFont('Segoe UI', 12, QFont.Medium)
    }
    
    # 间距
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32
    }
    
    # 圆角
    RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16
    }
    
    # 阴影
    SHADOWS = {
        'sm': '0 2px 4px rgba(0,0,0,0.1)',
        'md': '0 4px 8px rgba(0,0,0,0.2)',
        'lg': '0 8px 16px rgba(0,0,0,0.3)',
        'xl': '0 12px 24px rgba(0,0,0,0.4)'
    }
    
    @classmethod
    def get_stylesheet(cls) -> str:
        """获取全局样式表"""
        return f"""
            /* 全局样式 */
            QWidget {{
                background-color: {cls.COLORS['background']};
                color: {cls.COLORS['text']};
                font-family: 'Segoe UI';
            }}
            
            /* 主窗口 */
            QMainWindow {{
                background-color: {cls.COLORS['background']};
            }}
            
            /* 按钮样式 */
            QPushButton {{
                background-color: {cls.COLORS['primary']};
                color: {cls.COLORS['text']};
                border: none;
                border-radius: {cls.RADIUS['md']}px;
                padding: {cls.SPACING['sm']}px {cls.SPACING['md']}px;
                font: {cls.FONTS['button'].toString()};
            }}
            
            QPushButton:hover {{
                background-color: {cls.COLORS['secondary']};
            }}
            
            QPushButton:pressed {{
                background-color: {cls.COLORS['accent']};
            }}
            
            /* 标签样式 */
            QLabel {{
                color: {cls.COLORS['text']};
                padding: {cls.SPACING['xs']}px;
            }}
            
            /* 文本框样式 */
            QTextEdit {{
                background-color: {cls.COLORS['surface']};
                color: {cls.COLORS['text']};
                border: 1px solid {cls.COLORS['primary']};
                border-radius: {cls.RADIUS['sm']}px;
                padding: {cls.SPACING['sm']}px;
            }}
            
            /* 进度条样式 */
            QProgressBar {{
                background-color: {cls.COLORS['surface']};
                border: none;
                border-radius: {cls.RADIUS['sm']}px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {cls.COLORS['primary']};
                border-radius: {cls.RADIUS['sm']}px;
            }}
        """
    
    @classmethod
    def apply_theme(cls, widget) -> None:
        """应用主题到部件"""
        # 设置样式表
        widget.setStyleSheet(cls.get_stylesheet())
        
        # 设置调色板
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(cls.COLORS['background']))
        palette.setColor(QPalette.WindowText, QColor(cls.COLORS['text']))
        palette.setColor(QPalette.Base, QColor(cls.COLORS['surface']))
        palette.setColor(QPalette.AlternateBase, QColor(cls.COLORS['background']))
        palette.setColor(QPalette.ToolTipBase, QColor(cls.COLORS['surface']))
        palette.setColor(QPalette.ToolTipText, QColor(cls.COLORS['text']))
        palette.setColor(QPalette.Text, QColor(cls.COLORS['text']))
        palette.setColor(QPalette.Button, QColor(cls.COLORS['primary']))
        palette.setColor(QPalette.ButtonText, QColor(cls.COLORS['text']))
        palette.setColor(QPalette.Highlight, QColor(cls.COLORS['accent']))
        palette.setColor(QPalette.HighlightedText, QColor(cls.COLORS['text']))
        
        widget.setPalette(palette)

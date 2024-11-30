"""
系统管理模块
负责核心系统组件的集成和管理
"""
import logging
from typing import Optional
from pathlib import Path

from .event_bus import EventBus, Event, EventPriority
from .data_store import DataStore
from .error_handler import ErrorHandler, ErrorType, ErrorLevel

class SystemManager:
    """系统管理器"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self._setup_logging()
            
            # 初始化核心组件
            self.event_bus = EventBus()
            self.data_store = DataStore()
            self.error_handler = ErrorHandler()
            
            # 注册系统事件处理器
            self._register_system_handlers()
            
            self._initialized = True
            
    def _setup_logging(self):
        """配置日志系统"""
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置根日志记录器
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "system.log"),
                logging.StreamHandler()
            ]
        )
        
    def _register_system_handlers(self):
        """注册系统事件处理器"""
        # 系统错误处理
        self.event_bus.subscribe("system.error", self._handle_system_error)
        
        # 数据更新处理
        self.event_bus.subscribe("data.update", self._handle_data_update)
        
        # 系统状态更新
        self.event_bus.subscribe("system.status", self._handle_system_status)
        
    def _handle_system_error(self, event: Event):
        """处理系统错误事件"""
        error_data = event.data
        self.error_handler.handle_error(
            error_type=error_data.get('type', ErrorType.UNKNOWN),
            level=error_data.get('level', ErrorLevel.ERROR),
            message=error_data.get('message', 'Unknown error'),
            exception=error_data.get('exception')
        )
        
    def _handle_data_update(self, event: Event):
        """处理数据更新事件"""
        data = event.data
        if 'key' in data and 'value' in data:
            self.data_store.set(
                data['key'],
                data['value'],
                persist=data.get('persist', False)
            )
            
    def _handle_system_status(self, event: Event):
        """处理系统状态更新事件"""
        status = event.data
        self.data_store.set('system.status', status, persist=True)
        
    def publish_event(self, event_type: str, data: any, priority: EventPriority = EventPriority.NORMAL):
        """
        发布系统事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            priority: 事件优先级
        """
        event = Event(event_type, data, priority)
        self.event_bus.publish(event)
        
    def get_system_status(self) -> dict:
        """
        获取系统状态
        
        Returns:
            系统状态信息
        """
        return self.data_store.get('system.status', {
            'status': 'unknown',
            'last_update': None
        })
        
    def report_error(
        self,
        message: str,
        error_type: ErrorType = ErrorType.UNKNOWN,
        level: ErrorLevel = ErrorLevel.ERROR,
        exception: Optional[Exception] = None
    ):
        """
        报告系统错误
        
        Args:
            message: 错误信息
            error_type: 错误类型
            level: 错误级别
            exception: 异常对象
        """
        self.publish_event(
            'system.error',
            {
                'type': error_type,
                'level': level,
                'message': message,
                'exception': exception
            },
            priority=EventPriority.HIGH
        )
        
    def update_data(self, key: str, value: any, persist: bool = False):
        """
        更新系统数据
        
        Args:
            key: 数据键
            value: 数据值
            persist: 是否持久化
        """
        self.publish_event(
            'data.update',
            {
                'key': key,
                'value': value,
                'persist': persist
            }
        )
        
    def cleanup(self):
        """清理系统资源"""
        self.event_bus.clear()
        self.data_store.cleanup()
        self.error_handler.clear_history()
        self.logger.info("System manager cleaned up")

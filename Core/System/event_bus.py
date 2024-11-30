"""
事件总线模块
负责系统组件间的通信
"""
import logging
from typing import Dict, List, Callable, Any
from queue import Queue
from threading import Lock
from enum import Enum

class EventPriority(Enum):
    """事件优先级"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class Event:
    """事件基类"""
    def __init__(self, event_type: str, data: Any = None, priority: EventPriority = EventPriority.NORMAL):
        self.type = event_type
        self.data = data
        self.priority = priority
        self.timestamp = None  # 将在发布时设置

class EventBus:
    """事件总线"""
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self._subscribers: Dict[str, List[Callable]] = {}
            self._event_queue = Queue()
            self._is_processing = False
            self._initialized = True
            
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
            self.logger.debug(f"Subscribed to event: {event_type}")
            
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        取消订阅
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            self.logger.debug(f"Unsubscribed from event: {event_type}")
            
    def publish(self, event: Event) -> None:
        """
        发布事件
        
        Args:
            event: 事件对象
        """
        from datetime import datetime
        event.timestamp = datetime.now()
        
        self._event_queue.put((event.priority.value, event))
        self.logger.debug(f"Published event: {event.type}")
        
        if not self._is_processing:
            self._process_events()
            
    def _process_events(self) -> None:
        """处理事件队列"""
        self._is_processing = True
        
        try:
            while not self._event_queue.empty():
                _, event = self._event_queue.get()
                
                if event.type in self._subscribers:
                    for callback in self._subscribers[event.type]:
                        try:
                            callback(event)
                        except Exception as e:
                            self.logger.error(f"Error processing event {event.type}: {str(e)}")
                            
        finally:
            self._is_processing = False
            
    def clear(self) -> None:
        """清理事件总线"""
        with self._lock:
            self._subscribers.clear()
            while not self._event_queue.empty():
                self._event_queue.get()
            self.logger.info("Event bus cleared")

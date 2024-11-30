"""
交互管理模块
负责系统与用户的交互管理
"""
import logging
from typing import Dict, List, Any, Callable
from datetime import datetime
from enum import Enum

class InteractionType(Enum):
    """交互类型枚举"""
    COMMAND = 'command'
    GESTURE = 'gesture'
    VOICE = 'voice'
    KEYBOARD = 'keyboard'
    MOUSE = 'mouse'

class InteractionPriority(Enum):
    """交互优先级枚举"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class InteractionEvent:
    """交互事件类"""
    def __init__(self, event_type: InteractionType, data: Dict, priority: InteractionPriority = InteractionPriority.NORMAL):
        self.event_type = event_type
        self.data = data
        self.priority = priority
        self.timestamp = datetime.now()
        self.handled = False

class InteractionManager:
    """交互管理器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._event_handlers: Dict[InteractionType, List[Callable]] = {}
        self._event_queue: List[InteractionEvent] = []
        self._context: Dict[str, Any] = {}
        self._init_interaction_manager()
        
    def _init_interaction_manager(self):
        """初始化交互管理器"""
        self.logger.info("Initializing interaction manager...")
        self._init_default_handlers()
        
    def _init_default_handlers(self):
        """初始化默认事件处理器"""
        # 为每种交互类型初始化处理器列表
        for interaction_type in InteractionType:
            self._event_handlers[interaction_type] = []
            
    def register_handler(self, event_type: InteractionType, handler: Callable):
        """
        注册事件处理器
        
        Args:
            event_type: 事件类型
            handler: 处理器函数
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
        self.logger.info(f"Registered handler for {event_type.value}")
        
    def unregister_handler(self, event_type: InteractionType, handler: Callable):
        """
        注销事件处理器
        
        Args:
            event_type: 事件类型
            handler: 处理器函数
        """
        if event_type in self._event_handlers:
            self._event_handlers[event_type].remove(handler)
            self.logger.info(f"Unregistered handler for {event_type.value}")
            
    def handle_event(self, event: InteractionEvent):
        """
        处理交互事件
        
        Args:
            event: 交互事件
        """
        if event.event_type not in self._event_handlers:
            self.logger.warning(f"No handlers registered for {event.event_type.value}")
            return
            
        # 根据优先级处理事件
        if event.priority == InteractionPriority.CRITICAL:
            self._handle_critical_event(event)
        else:
            self._event_queue.append(event)
            self._process_event_queue()
            
    def _handle_critical_event(self, event: InteractionEvent):
        """处理关键事件"""
        self.logger.info(f"Handling critical event: {event.event_type.value}")
        handlers = self._event_handlers[event.event_type]
        
        for handler in handlers:
            try:
                handler(event.data)
                event.handled = True
            except Exception as e:
                self.logger.error(f"Error handling critical event: {str(e)}")
                
    def _process_event_queue(self):
        """处理事件队列"""
        # 按优先级排序
        self._event_queue.sort(key=lambda x: x.priority.value, reverse=True)
        
        # 处理队列中的事件
        processed_events = []
        for event in self._event_queue:
            handlers = self._event_handlers[event.event_type]
            
            for handler in handlers:
                try:
                    handler(event.data)
                    event.handled = True
                except Exception as e:
                    self.logger.error(f"Error handling event: {str(e)}")
                    
            processed_events.append(event)
            
        # 移除已处理的事件
        self._event_queue = [e for e in self._event_queue if e not in processed_events]
        
    def update_context(self, context_data: Dict):
        """
        更新交互上下文
        
        Args:
            context_data: 上下文数据
        """
        self._context.update(context_data)
        
    def get_context(self) -> Dict:
        """获取当前上下文"""
        return self._context
        
    def clear_context(self):
        """清除上下文"""
        self._context.clear()
        
    def get_event_queue_status(self) -> Dict:
        """获取事件队列状态"""
        return {
            'queue_length': len(self._event_queue),
            'priority_distribution': self._get_priority_distribution(),
            'type_distribution': self._get_type_distribution()
        }
        
    def _get_priority_distribution(self) -> Dict[InteractionPriority, int]:
        """获取优先级分布"""
        distribution = {priority: 0 for priority in InteractionPriority}
        for event in self._event_queue:
            distribution[event.priority] += 1
        return distribution
        
    def _get_type_distribution(self) -> Dict[InteractionType, int]:
        """获取类型分布"""
        distribution = {event_type: 0 for event_type in InteractionType}
        for event in self._event_queue:
            distribution[event.event_type] += 1
        return distribution
        
    def cleanup(self):
        """清理交互管理器"""
        self._event_handlers.clear()
        self._event_queue.clear()
        self._context.clear()
        self.logger.info("Interaction manager cleaned up")

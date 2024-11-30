"""
错误处理模块
负责系统错误的统一处理和恢复
"""
import logging
import traceback
from typing import Dict, List, Callable, Optional
from enum import Enum
from datetime import datetime
from pathlib import Path

class ErrorLevel(Enum):
    """错误级别"""
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'

class ErrorType(Enum):
    """错误类型"""
    SYSTEM = 'system'
    NETWORK = 'network'
    DATABASE = 'database'
    UI = 'ui'
    USER = 'user'
    UNKNOWN = 'unknown'

class SystemError:
    """系统错误类"""
    def __init__(
        self,
        error_type: ErrorType,
        level: ErrorLevel,
        message: str,
        exception: Optional[Exception] = None
    ):
        self.error_type = error_type
        self.level = level
        self.message = message
        self.exception = exception
        self.timestamp = datetime.now()
        self.traceback = traceback.format_exc() if exception else None
        
class ErrorHandler:
    """错误处理器"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ErrorHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self._error_handlers: Dict[ErrorType, List[Callable]] = {}
            self._recovery_handlers: Dict[ErrorType, List[Callable]] = {}
            self._error_history: List[SystemError] = []
            self._max_history = 1000
            self._log_path = Path("logs")
            self._ensure_log_path()
            self._initialized = True
            
    def _ensure_log_path(self):
        """确保日志路径存在"""
        self._log_path.mkdir(parents=True, exist_ok=True)
        
    def register_handler(
        self,
        error_type: ErrorType,
        handler: Callable[[SystemError], None]
    ) -> None:
        """
        注册错误处理器
        
        Args:
            error_type: 错误类型
            handler: 处理函数
        """
        if error_type not in self._error_handlers:
            self._error_handlers[error_type] = []
        self._error_handlers[error_type].append(handler)
        
    def register_recovery(
        self,
        error_type: ErrorType,
        recovery: Callable[[SystemError], bool]
    ) -> None:
        """
        注册恢复处理器
        
        Args:
            error_type: 错误类型
            recovery: 恢复函数
        """
        if error_type not in self._recovery_handlers:
            self._recovery_handlers[error_type] = []
        self._recovery_handlers[error_type].append(recovery)
        
    def handle_error(
        self,
        error_type: ErrorType,
        level: ErrorLevel,
        message: str,
        exception: Optional[Exception] = None
    ) -> None:
        """
        处理错误
        
        Args:
            error_type: 错误类型
            level: 错误级别
            message: 错误信息
            exception: 异常对象
        """
        # 创建错误对象
        error = SystemError(error_type, level, message, exception)
        
        # 记录错误历史
        self._error_history.append(error)
        if len(self._error_history) > self._max_history:
            self._error_history = self._error_history[-self._max_history:]
            
        # 记录日志
        self._log_error(error)
        
        # 调用错误处理器
        if error_type in self._error_handlers:
            for handler in self._error_handlers[error_type]:
                try:
                    handler(error)
                except Exception as e:
                    self.logger.error(f"Error in error handler: {str(e)}")
                    
        # 尝试恢复
        self._try_recovery(error)
        
    def _log_error(self, error: SystemError) -> None:
        """
        记录错误日志
        
        Args:
            error: 错误对象
        """
        log_file = self._log_path / f"{error.timestamp.strftime('%Y%m%d')}.log"
        
        try:
            with log_file.open('a', encoding='utf-8') as f:
                f.write(f"[{error.timestamp}] {error.level.value.upper()}: {error.message}\n")
                if error.traceback:
                    f.write(f"Traceback:\n{error.traceback}\n")
                f.write("-" * 80 + "\n")
                
        except Exception as e:
            self.logger.error(f"Error writing to log file: {str(e)}")
            
    def _try_recovery(self, error: SystemError) -> bool:
        """
        尝试错误恢复
        
        Args:
            error: 错误对象
            
        Returns:
            是否恢复成功
        """
        if error.error_type not in self._recovery_handlers:
            return False
            
        for recovery in self._recovery_handlers[error.error_type]:
            try:
                if recovery(error):
                    self.logger.info(f"Successfully recovered from {error.error_type.value} error")
                    return True
            except Exception as e:
                self.logger.error(f"Error in recovery handler: {str(e)}")
                
        return False
        
    def get_error_history(
        self,
        error_type: Optional[ErrorType] = None,
        level: Optional[ErrorLevel] = None,
        limit: int = 100
    ) -> List[SystemError]:
        """
        获取错误历史
        
        Args:
            error_type: 错误类型过滤
            level: 错误级别过滤
            limit: 返回数量限制
            
        Returns:
            错误历史列表
        """
        filtered = self._error_history
        
        if error_type:
            filtered = [e for e in filtered if e.error_type == error_type]
        if level:
            filtered = [e for e in filtered if e.level == level]
            
        return filtered[-limit:]
        
    def clear_history(self) -> None:
        """清理错误历史"""
        self._error_history.clear()
        self.logger.info("Error history cleared")

"""
数据存储模块
负责系统数据的存储和管理
"""
import logging
import json
import pickle
from typing import Dict, Any, Optional
from pathlib import Path
from threading import Lock
from datetime import datetime

class DataStore:
    """数据存储类"""
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DataStore, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self._data: Dict[str, Any] = {}
            self._cache: Dict[str, Any] = {}
            self._cache_timeout: Dict[str, datetime] = {}
            self._storage_path = Path("data")
            self._ensure_storage_path()
            self._initialized = True
            
    def _ensure_storage_path(self):
        """确保存储路径存在"""
        self._storage_path.mkdir(parents=True, exist_ok=True)
        
    def set(self, key: str, value: Any, persist: bool = False) -> None:
        """
        设置数据
        
        Args:
            key: 键
            value: 值
            persist: 是否持久化
        """
        self._data[key] = value
        self._cache[key] = value
        self._cache_timeout[key] = datetime.now()
        
        if persist:
            self._persist_data(key, value)
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取数据
        
        Args:
            key: 键
            default: 默认值
            
        Returns:
            存储的值
        """
        # 先检查缓存
        if key in self._cache:
            return self._cache[key]
            
        # 检查内存
        if key in self._data:
            return self._data[key]
            
        # 尝试从持久化存储加载
        value = self._load_data(key)
        if value is not None:
            self._data[key] = value
            self._cache[key] = value
            self._cache_timeout[key] = datetime.now()
            return value
            
        return default
        
    def delete(self, key: str) -> None:
        """
        删除数据
        
        Args:
            key: 键
        """
        if key in self._data:
            del self._data[key]
        if key in self._cache:
            del self._cache[key]
        if key in self._cache_timeout:
            del self._cache_timeout[key]
            
        # 删除持久化数据
        data_file = self._storage_path / f"{key}.json"
        if data_file.exists():
            data_file.unlink()
            
    def clear_cache(self) -> None:
        """清理缓存"""
        self._cache.clear()
        self._cache_timeout.clear()
        
    def _persist_data(self, key: str, value: Any) -> None:
        """
        持久化数据
        
        Args:
            key: 键
            value: 值
        """
        try:
            data_file = self._storage_path / f"{key}.json"
            
            # 对于简单类型，使用JSON
            if isinstance(value, (str, int, float, bool, list, dict)):
                with data_file.open('w', encoding='utf-8') as f:
                    json.dump(value, f)
            # 对于复杂类型，使用pickle
            else:
                pickle_file = self._storage_path / f"{key}.pickle"
                with pickle_file.open('wb') as f:
                    pickle.dump(value, f)
                    
        except Exception as e:
            self.logger.error(f"Error persisting data for key {key}: {str(e)}")
            
    def _load_data(self, key: str) -> Optional[Any]:
        """
        加载持久化数据
        
        Args:
            key: 键
            
        Returns:
            加载的数据
        """
        try:
            # 先尝试JSON文件
            json_file = self._storage_path / f"{key}.json"
            if json_file.exists():
                with json_file.open('r', encoding='utf-8') as f:
                    return json.load(f)
                    
            # 再尝试pickle文件
            pickle_file = self._storage_path / f"{key}.pickle"
            if pickle_file.exists():
                with pickle_file.open('rb') as f:
                    return pickle.load(f)
                    
        except Exception as e:
            self.logger.error(f"Error loading data for key {key}: {str(e)}")
            
        return None
        
    def cleanup(self) -> None:
        """清理数据存储"""
        self._data.clear()
        self.clear_cache()
        self.logger.info("Data store cleaned up")

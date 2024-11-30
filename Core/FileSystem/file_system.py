"""
文件系统模块
负责文件的创建、读写和管理
"""
import os
import shutil
import logging
from typing import Dict, List, Optional
from datetime import datetime

class FileNode:
    """文件节点类"""
    def __init__(self, name: str, is_directory: bool = False):
        self.name = name
        self.is_directory = is_directory
        self.size = 0
        self.created_time = datetime.now()
        self.modified_time = datetime.now()
        self.parent = None
        self.children = {} if is_directory else None

class FileSystem:
    """文件系统类"""
    
    def __init__(self, root_path: str):
        self.logger = logging.getLogger(__name__)
        self.root_path = root_path
        self.root = FileNode("/", True)
        self._init_file_system()
        
    def _init_file_system(self):
        """初始化文件系统"""
        self.logger.info(f"Initializing file system at {self.root_path}")
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        self._scan_directory(self.root_path, self.root)
        
    def _scan_directory(self, path: str, node: FileNode):
        """扫描目录"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                is_dir = os.path.isdir(item_path)
                child_node = FileNode(item, is_dir)
                child_node.parent = node
                
                if is_dir:
                    self._scan_directory(item_path, child_node)
                else:
                    child_node.size = os.path.getsize(item_path)
                    
                node.children[item] = child_node
        except Exception as e:
            self.logger.error(f"Error scanning directory {path}: {str(e)}")
            
    def create_file(self, path: str, content: str = "") -> bool:
        """创建文件"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.logger.info(f"Created file: {path}")
            self._update_file_tree(path)
            return True
        except Exception as e:
            self.logger.error(f"Error creating file {path}: {str(e)}")
            return False
            
    def create_directory(self, path: str) -> bool:
        """创建目录"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            os.makedirs(full_path, exist_ok=True)
            
            self.logger.info(f"Created directory: {path}")
            self._update_file_tree(path)
            return True
        except Exception as e:
            self.logger.error(f"Error creating directory {path}: {str(e)}")
            return False
            
    def read_file(self, path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Error reading file {path}: {str(e)}")
            return None
            
    def write_file(self, path: str, content: str) -> bool:
        """写入文件内容"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self._update_file_tree(path)
            return True
        except Exception as e:
            self.logger.error(f"Error writing to file {path}: {str(e)}")
            return False
            
    def delete_file(self, path: str) -> bool:
        """删除文件"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            if os.path.exists(full_path):
                os.remove(full_path)
                self.logger.info(f"Deleted file: {path}")
                self._update_file_tree(path, delete=True)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting file {path}: {str(e)}")
            return False
            
    def delete_directory(self, path: str) -> bool:
        """删除目录"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                self.logger.info(f"Deleted directory: {path}")
                self._update_file_tree(path, delete=True)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting directory {path}: {str(e)}")
            return False
            
    def _update_file_tree(self, path: str, delete: bool = False):
        """更新文件树结构"""
        parts = path.strip("/").split("/")
        current = self.root
        
        if delete:
            # 删除节点
            for part in parts[:-1]:
                if part in current.children:
                    current = current.children[part]
            if parts[-1] in current.children:
                del current.children[parts[-1]]
        else:
            # 添加或更新节点
            for part in parts:
                if part not in current.children:
                    is_dir = os.path.isdir(os.path.join(self.root_path, "/".join(parts)))
                    current.children[part] = FileNode(part, is_dir)
                current = current.children[part]
                
    def get_file_info(self, path: str) -> Optional[Dict]:
        """获取文件信息"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            if os.path.exists(full_path):
                stats = os.stat(full_path)
                return {
                    'name': os.path.basename(path),
                    'size': stats.st_size,
                    'created_time': datetime.fromtimestamp(stats.st_ctime),
                    'modified_time': datetime.fromtimestamp(stats.st_mtime),
                    'is_directory': os.path.isdir(full_path)
                }
            return None
        except Exception as e:
            self.logger.error(f"Error getting file info for {path}: {str(e)}")
            return None
            
    def list_directory(self, path: str = "/") -> List[Dict]:
        """列出目录内容"""
        try:
            full_path = os.path.join(self.root_path, path.lstrip("/"))
            if os.path.exists(full_path) and os.path.isdir(full_path):
                items = []
                for item in os.listdir(full_path):
                    item_path = os.path.join(full_path, item)
                    items.append({
                        'name': item,
                        'is_directory': os.path.isdir(item_path),
                        'size': os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                    })
                return items
            return []
        except Exception as e:
            self.logger.error(f"Error listing directory {path}: {str(e)}")
            return []

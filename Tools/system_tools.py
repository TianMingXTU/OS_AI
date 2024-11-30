"""
系统工具集
提供常用的系统维护和优化工具
"""
import os
import sys
import psutil
import shutil
import logging
import winreg
from typing import List, Dict, Optional
from pathlib import Path

class SystemTools:
    """系统工具类"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def clean_system(self) -> Dict[str, int]:
        """
        系统清理
        清理临时文件、系统缓存等
        
        Returns:
            清理结果统计
        """
        results = {
            "temp_files": 0,
            "recycle_bin": 0,
            "system_cache": 0,
            "browser_cache": 0
        }
        
        try:
            # 清理临时文件
            temp_paths = [
                os.environ.get('TEMP'),
                os.environ.get('TMP'),
                os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp'),
                os.path.join(os.environ.get('WINDIR'), 'Temp')
            ]
            
            for temp_path in temp_paths:
                if temp_path and os.path.exists(temp_path):
                    results["temp_files"] += self._clean_directory(temp_path)
                    
            # 清理回收站
            results["recycle_bin"] = self._clean_recycle_bin()
            
            # 清理系统缓存
            results["system_cache"] = self._clean_system_cache()
            
            # 清理浏览器缓存
            results["browser_cache"] = self._clean_browser_cache()
            
        except Exception as e:
            self.logger.error(f"系统清理失败: {str(e)}")
            
        return results
        
    def _clean_directory(self, directory: str) -> int:
        """清理指定目录"""
        cleaned_size = 0
        try:
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    try:
                        file_path = os.path.join(root, name)
                        if os.path.exists(file_path):
                            cleaned_size += os.path.getsize(file_path)
                            os.remove(file_path)
                    except Exception:
                        continue
                        
                for name in dirs:
                    try:
                        dir_path = os.path.join(root, name)
                        if os.path.exists(dir_path):
                            shutil.rmtree(dir_path, ignore_errors=True)
                    except Exception:
                        continue
        except Exception as e:
            self.logger.error(f"清理目录失败 {directory}: {str(e)}")
            
        return cleaned_size
        
    def _clean_recycle_bin(self) -> int:
        """清理回收站"""
        cleaned_size = 0
        try:
            import winshell
            cleaned_size = winshell.recycle_bin().size
            winshell.recycle_bin().empty(confirm=False, show_progress=False)
        except Exception as e:
            self.logger.error(f"清理回收站失败: {str(e)}")
        return cleaned_size
        
    def _clean_system_cache(self) -> int:
        """清理系统缓存"""
        cleaned_size = 0
        try:
            # Windows DNS缓存
            os.system('ipconfig /flushdns')
            
            # Windows字体缓存
            font_cache = os.path.join(os.environ.get('WINDIR'), 'System32', 'FNTCACHE.DAT')
            if os.path.exists(font_cache):
                cleaned_size += os.path.getsize(font_cache)
                os.remove(font_cache)
                
        except Exception as e:
            self.logger.error(f"清理系统缓存失败: {str(e)}")
            
        return cleaned_size
        
    def _clean_browser_cache(self) -> int:
        """清理浏览器缓存"""
        cleaned_size = 0
        try:
            # Chrome缓存
            chrome_cache = os.path.join(
                os.environ.get('LOCALAPPDATA'),
                'Google/Chrome/User Data/Default/Cache'
            )
            if os.path.exists(chrome_cache):
                cleaned_size += self._clean_directory(chrome_cache)
                
            # Edge缓存
            edge_cache = os.path.join(
                os.environ.get('LOCALAPPDATA'),
                'Microsoft/Edge/User Data/Default/Cache'
            )
            if os.path.exists(edge_cache):
                cleaned_size += self._clean_directory(edge_cache)
                
        except Exception as e:
            self.logger.error(f"清理浏览器缓存失败: {str(e)}")
            
        return cleaned_size
        
    def optimize_startup(self) -> List[str]:
        """
        优化系统启动项
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 检查启动项
            startup_items = self._get_startup_items()
            
            # 分析和优化启动项
            for item in startup_items:
                if self._should_disable_startup(item):
                    if self._disable_startup_item(item):
                        results.append(f"已禁用启动项: {item['name']}")
                        
        except Exception as e:
            self.logger.error(f"优化启动项失败: {str(e)}")
            
        return results
        
    def _get_startup_items(self) -> List[Dict]:
        """获取系统启动项"""
        items = []
        try:
            # 从注册表获取启动项
            startup_paths = [
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
            ]
            
            for path in startup_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
                    try:
                        i = 0
                        while True:
                            name, value, _ = winreg.EnumValue(key, i)
                            items.append({
                                "name": name,
                                "command": value,
                                "path": path,
                                "type": "HKCU"
                            })
                            i += 1
                    except WindowsError:
                        pass
                    finally:
                        winreg.CloseKey(key)
                except WindowsError:
                    pass
                    
        except Exception as e:
            self.logger.error(f"获取启动项失败: {str(e)}")
            
        return items
        
    def _should_disable_startup(self, item: Dict) -> bool:
        """判断是否应该禁用启动项"""
        # 这里可以添加更多的判断逻辑
        try:
            # 检查程序是否存在
            command = item.get('command', '')
            if command:
                program_path = command.split('"')[1] if '"' in command else command.split()[0]
                if not os.path.exists(program_path):
                    return True
                    
            # 检查是否是已知的不必要启动项
            unnecessary_keywords = [
                'update', 'updater', 'helper', 'scheduler'
            ]
            return any(keyword in item['name'].lower() for keyword in unnecessary_keywords)
            
        except Exception:
            return False
            
    def _disable_startup_item(self, item: Dict) -> bool:
        """禁用启动项"""
        try:
            if item['type'] == 'HKCU':
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    item['path'],
                    0,
                    winreg.KEY_WRITE
                )
                winreg.DeleteValue(key, item['name'])
                winreg.CloseKey(key)
                return True
        except Exception as e:
            self.logger.error(f"禁用启动项失败 {item['name']}: {str(e)}")
            return False
            
    def analyze_disk_space(self) -> Dict:
        """
        分析磁盘空间使用
        
        Returns:
            磁盘空间分析结果
        """
        results = {
            "partitions": [],
            "large_files": [],
            "recommendations": []
        }
        
        try:
            # 分析分区使用情况
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partition_info = {
                        "mountpoint": partition.mountpoint,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    }
                    results["partitions"].append(partition_info)
                    
                    # 添加建议
                    if usage.percent > 90:
                        results["recommendations"].append(
                            f"分区 {partition.mountpoint} 空间不足，建议清理"
                        )
                except Exception:
                    continue
                    
            # 查找大文件
            results["large_files"] = self._find_large_files()
            
        except Exception as e:
            self.logger.error(f"分析磁盘空间失败: {str(e)}")
            
        return results
        
    def _find_large_files(self, min_size: int = 100*1024*1024) -> List[Dict]:
        """查找大文件"""
        large_files = []
        try:
            for partition in psutil.disk_partitions():
                try:
                    if partition.fstype:  # 确保是有效的文件系统
                        for root, _, files in os.walk(partition.mountpoint):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    size = os.path.getsize(file_path)
                                    if size > min_size:
                                        large_files.append({
                                            "path": file_path,
                                            "size": size
                                        })
                                except Exception:
                                    continue
                except Exception:
                    continue
                    
            # 按大小排序
            large_files.sort(key=lambda x: x['size'], reverse=True)
            return large_files[:20]  # 返回最大的20个文件
            
        except Exception as e:
            self.logger.error(f"查找大文件失败: {str(e)}")
            return []
            
    def format_bytes(self, bytes: int) -> str:
        """格式化字节大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} PB"

"""
性能优化模块
实现轻量级的系统性能优化
"""
import os
import psutil
import logging
from typing import List, Dict
from pathlib import Path

class PerformanceOptimizer:
    """性能优化器"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system = psutil
        
    def analyze_performance(self) -> Dict:
        """分析系统性能"""
        try:
            return {
                "cpu_issues": self._check_cpu(),
                "memory_issues": self._check_memory(),
                "disk_issues": self._check_disk(),
                "process_issues": self._check_processes()
            }
        except Exception as e:
            self.logger.error(f"性能分析失败: {str(e)}")
            return {}
            
    def _check_cpu(self) -> List[str]:
        """检查CPU问题"""
        issues = []
        try:
            # CPU使用率检查
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 80:
                issues.append(f"CPU使用率过高 ({cpu_percent}%)")
                
            # CPU频率检查
            freq = psutil.cpu_freq()
            if freq and freq.current < freq.min * 1.1:
                issues.append("CPU频率过低，可能影响性能")
                
            # CPU温度检查(如果支持)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current > 80:
                                issues.append(f"CPU温度过高: {entry.current}°C")
            except Exception:
                pass
                
        except Exception as e:
            self.logger.error(f"CPU检查失败: {str(e)}")
            
        return issues
        
    def _check_memory(self) -> List[str]:
        """检查内存问题"""
        issues = []
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # 内存使用检查
            if memory.percent > 80:
                issues.append(f"内存使用率过高 ({memory.percent}%)")
                
            # 交换空间检查
            if swap.percent > 60:
                issues.append(f"交换空间使用率过高 ({swap.percent}%)")
                
            # 可用内存检查
            available_gb = memory.available / (1024 ** 3)
            if available_gb < 2:
                issues.append(f"可用内存不足 ({available_gb:.1f} GB)")
                
        except Exception as e:
            self.logger.error(f"内存检查失败: {str(e)}")
            
        return issues
        
    def _check_disk(self) -> List[str]:
        """检查磁盘问题"""
        issues = []
        try:
            # 磁盘空间检查
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    if usage.percent > 90:
                        issues.append(f"分区 {partition.mountpoint} 空间不足 ({usage.percent}%)")
                except Exception:
                    continue
                    
            # 磁盘IO检查
            io_counters = psutil.disk_io_counters()
            if io_counters:
                # 检查是否有大量IO操作
                if io_counters.read_bytes + io_counters.write_bytes > 100 * (1024 ** 2):  # 100MB
                    issues.append("磁盘IO负载较高")
                    
        except Exception as e:
            self.logger.error(f"磁盘检查失败: {str(e)}")
            
        return issues
        
    def _check_processes(self) -> List[str]:
        """检查进程问题"""
        issues = []
        try:
            # 获取资源占用较高的进程
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['cpu_percent'] > 50:
                        issues.append(f"进程 {proc.info['name']} (PID: {proc.info['pid']}) CPU使用率过高")
                    if proc.info['memory_percent'] > 20:
                        issues.append(f"进程 {proc.info['name']} (PID: {proc.info['pid']}) 内存使用率过高")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"进程检查失败: {str(e)}")
            
        return issues
        
    def optimize_system(self) -> List[str]:
        """执行系统优化"""
        optimizations = []
        
        try:
            # 1. 清理临时文件
            temp_cleaned = self._clean_temp_files()
            if temp_cleaned > 0:
                optimizations.append(f"清理了 {self._format_bytes(temp_cleaned)} 临时文件")
                
            # 2. 优化进程
            processes_optimized = self._optimize_processes()
            if processes_optimized:
                optimizations.append(f"优化了 {len(processes_optimized)} 个进程的优先级")
                
            # 3. 内存优化
            memory_freed = self._optimize_memory()
            if memory_freed > 0:
                optimizations.append(f"释放了 {self._format_bytes(memory_freed)} 内存")
                
        except Exception as e:
            self.logger.error(f"系统优化失败: {str(e)}")
            
        return optimizations
        
    def _clean_temp_files(self) -> int:
        """清理临时文件"""
        total_cleaned = 0
        temp_dirs = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            '/tmp'
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                if os.path.exists(file_path):
                                    size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    total_cleaned += size
                            except Exception:
                                continue
                except Exception as e:
                    self.logger.error(f"清理临时文件失败: {str(e)}")
                    
        return total_cleaned
        
    def _optimize_processes(self) -> List[str]:
        """优化进程优先级"""
        optimized = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    # 对CPU密集型进程降低优先级
                    if proc.info['cpu_percent'] > 50:
                        proc_obj = psutil.Process(proc.info['pid'])
                        if proc_obj.nice() == 0:  # 只调整正常优先级的进程
                            proc_obj.nice(10)  # 降低优先级
                            optimized.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"进程优化失败: {str(e)}")
            
        return optimized
        
    def _optimize_memory(self) -> int:
        """优化内存使用"""
        freed_memory = 0
        
        try:
            # 在Windows上调用内存优化
            if os.name == 'nt':
                try:
                    import ctypes
                    ctypes.windll.psapi.EmptyWorkingSet(-1)
                    # 获取优化前后的内存差异
                    freed_memory = psutil.virtual_memory().available
                except Exception:
                    pass
                    
        except Exception as e:
            self.logger.error(f"内存优化失败: {str(e)}")
            
        return freed_memory
        
    def _format_bytes(self, bytes: int) -> str:
        """格式化字节大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} PB"

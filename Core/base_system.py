"""
基础系统模块
实现系统最基本的功能
"""
import os
import sys
import logging
import psutil
from typing import Dict, List
from datetime import datetime
from pathlib import Path

class BaseSystem:
    """基础系统类"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self.system_info = self._get_system_info()
        
    def _setup_logging(self):
        """配置日志系统"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "system.log"),
                logging.StreamHandler()
            ]
        )
        
    def _get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "disk_usage": psutil.disk_usage('/').percent
        }
        
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "disk_usage": disk.percent,
                "disk_free": disk.free
            }
        except Exception as e:
            self.logger.error(f"获取系统状态失败: {str(e)}")
            return {}
            
    def get_running_processes(self) -> List[Dict]:
        """获取运行中的进程"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(proc.info)
            return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
        except Exception as e:
            self.logger.error(f"获取进程信息失败: {str(e)}")
            return []
            
    def monitor_system_resources(self) -> Dict:
        """监控系统资源使用"""
        try:
            # CPU信息
            cpu_times = psutil.cpu_times()
            cpu_freq = psutil.cpu_freq()
            
            # 内存信息
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # 磁盘信息
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # 网络信息
            net_io = psutil.net_io_counters()
            
            return {
                "cpu": {
                    "user": cpu_times.user,
                    "system": cpu_times.system,
                    "idle": cpu_times.idle,
                    "frequency": {
                        "current": cpu_freq.current,
                        "min": cpu_freq.min,
                        "max": cpu_freq.max
                    }
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "swap": {
                        "total": swap.total,
                        "used": swap.used,
                        "free": swap.free
                    }
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "io": {
                        "read_bytes": disk_io.read_bytes,
                        "write_bytes": disk_io.write_bytes
                    }
                },
                "network": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv
                }
            }
        except Exception as e:
            self.logger.error(f"监控系统资源失败: {str(e)}")
            return {}
            
    def optimize_system_performance(self) -> List[str]:
        """优化系统性能"""
        recommendations = []
        
        try:
            # CPU使用率检查
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 80:
                recommendations.append("CPU使用率过高,建议关闭不必要的进程")
                
            # 内存使用检查
            memory = psutil.virtual_memory()
            if memory.percent > 80:
                recommendations.append("内存使用率过高,建议释放内存")
                
            # 磁盘空间检查
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                recommendations.append("磁盘空间不足,建议清理磁盘")
                
            # 进程检查
            high_cpu_processes = []
            high_memory_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                if proc.info['cpu_percent'] > 50:
                    high_cpu_processes.append(proc.info['name'])
                if proc.info['memory_percent'] > 20:
                    high_memory_processes.append(proc.info['name'])
                    
            if high_cpu_processes:
                recommendations.append(f"以下进程CPU使用率过高: {', '.join(high_cpu_processes)}")
            if high_memory_processes:
                recommendations.append(f"以下进程内存使用率过高: {', '.join(high_memory_processes)}")
                
        except Exception as e:
            self.logger.error(f"性能优化分析失败: {str(e)}")
            
        return recommendations
        
    def check_system_health(self) -> Dict:
        """检查系统健康状态"""
        health_status = {
            "status": "healthy",
            "issues": [],
            "metrics": {}
        }
        
        try:
            # CPU温度检查(如果支持)
            try:
                temperatures = psutil.sensors_temperatures()
                if temperatures:
                    cpu_temps = []
                    for name, entries in temperatures.items():
                        for entry in entries:
                            cpu_temps.append(entry.current)
                    avg_temp = sum(cpu_temps) / len(cpu_temps)
                    health_status["metrics"]["cpu_temperature"] = avg_temp
                    
                    if avg_temp > 80:
                        health_status["status"] = "warning"
                        health_status["issues"].append("CPU温度过高")
            except Exception:
                pass
                
            # 系统负载检查
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health_status["metrics"].update({
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent
            })
            
            # 添加健康状态检查结果
            if cpu_percent > 90:
                health_status["status"] = "warning"
                health_status["issues"].append("CPU使用率严重过高")
            elif cpu_percent > 80:
                health_status["status"] = "warning"
                health_status["issues"].append("CPU使用率过高")
                
            if memory.percent > 90:
                health_status["status"] = "warning"
                health_status["issues"].append("内存使用率严重过高")
            elif memory.percent > 80:
                health_status["status"] = "warning"
                health_status["issues"].append("内存使用率过高")
                
            if disk.percent > 95:
                health_status["status"] = "warning"
                health_status["issues"].append("磁盘空间严重不足")
            elif disk.percent > 90:
                health_status["status"] = "warning"
                health_status["issues"].append("磁盘空间不足")
                
        except Exception as e:
            health_status["status"] = "error"
            health_status["issues"].append(f"健康检查失败: {str(e)}")
            
        return health_status

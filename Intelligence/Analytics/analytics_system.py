"""
数据分析系统模块
负责系统数据的收集、分析和可视化
"""
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

class AnalyticsSystem:
    """数据分析系统类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._metrics_data = defaultdict(list)
        self._analysis_results = {}
        self._alerts = []
        self._init_analytics_system()
        
    def _init_analytics_system(self):
        """初始化分析系统"""
        self.logger.info("Initializing analytics system...")
        self._init_metrics_collectors()
        
    def _init_metrics_collectors(self):
        """初始化指标收集器"""
        self._metrics_collectors = {
            'system_performance': self._collect_performance_metrics,
            'user_behavior': self._collect_user_metrics,
            'resource_usage': self._collect_resource_metrics,
            'error_rates': self._collect_error_metrics
        }
        
    def collect_metrics(self, metric_type: str, data: Dict):
        """
        收集指标数据
        
        Args:
            metric_type: 指标类型
            data: 指标数据
        """
        timestamp = datetime.now()
        self._metrics_data[metric_type].append({
            'timestamp': timestamp,
            'data': data
        })
        
        # 触发数据分析
        self._analyze_metrics(metric_type)
        
    def _analyze_metrics(self, metric_type: str):
        """分析指标数据"""
        if metric_type in self._metrics_collectors:
            collector = self._metrics_collectors[metric_type]
            analysis_result = collector(self._metrics_data[metric_type])
            self._analysis_results[metric_type] = analysis_result
            
            # 检查是否需要生成告警
            self._check_alerts(metric_type, analysis_result)
            
    def _collect_performance_metrics(self, metrics: List[Dict]) -> Dict:
        """收集性能指标"""
        if not metrics:
            return {}
            
        # 提取最近的性能数据
        recent_metrics = metrics[-100:]  # 最近100个数据点
        
        # 计算关键指标
        cpu_usage = [m['data'].get('cpu_usage', 0) for m in recent_metrics]
        memory_usage = [m['data'].get('memory_usage', 0) for m in recent_metrics]
        
        return {
            'cpu_stats': {
                'mean': np.mean(cpu_usage),
                'max': np.max(cpu_usage),
                'min': np.min(cpu_usage),
                'std': np.std(cpu_usage)
            },
            'memory_stats': {
                'mean': np.mean(memory_usage),
                'max': np.max(memory_usage),
                'min': np.min(memory_usage),
                'std': np.std(memory_usage)
            }
        }
        
    def _collect_user_metrics(self, metrics: List[Dict]) -> Dict:
        """收集用户行为指标"""
        if not metrics:
            return {}
            
        # 分析用户行为模式
        user_actions = [m['data'].get('action_type') for m in metrics]
        action_counts = defaultdict(int)
        for action in user_actions:
            action_counts[action] += 1
            
        return {
            'action_distribution': dict(action_counts),
            'total_actions': len(metrics),
            'unique_actions': len(action_counts)
        }
        
    def _collect_resource_metrics(self, metrics: List[Dict]) -> Dict:
        """收集资源使用指标"""
        if not metrics:
            return {}
            
        # 分析资源使用趋势
        disk_usage = [m['data'].get('disk_usage', 0) for m in metrics]
        network_usage = [m['data'].get('network_usage', 0) for m in metrics]
        
        return {
            'disk_stats': {
                'current': disk_usage[-1] if disk_usage else 0,
                'trend': self._calculate_trend(disk_usage)
            },
            'network_stats': {
                'current': network_usage[-1] if network_usage else 0,
                'trend': self._calculate_trend(network_usage)
            }
        }
        
    def _collect_error_metrics(self, metrics: List[Dict]) -> Dict:
        """收集错误指标"""
        if not metrics:
            return {}
            
        # 分析错误模式
        error_types = [m['data'].get('error_type') for m in metrics]
        error_counts = defaultdict(int)
        for error in error_types:
            error_counts[error] += 1
            
        return {
            'error_distribution': dict(error_counts),
            'total_errors': len(metrics),
            'unique_errors': len(error_counts)
        }
        
    def _calculate_trend(self, data: List[float]) -> str:
        """计算趋势"""
        if len(data) < 2:
            return "stable"
            
        # 简单的线性回归
        x = np.arange(len(data))
        y = np.array(data)
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
            
    def _check_alerts(self, metric_type: str, analysis_result: Dict):
        """检查是否需要生成告警"""
        alerts = []
        
        if metric_type == 'system_performance':
            cpu_stats = analysis_result.get('cpu_stats', {})
            if cpu_stats.get('mean', 0) > 80:
                alerts.append({
                    'type': 'high_cpu_usage',
                    'severity': 'warning',
                    'message': f"High CPU usage detected: {cpu_stats['mean']:.2f}%"
                })
                
        elif metric_type == 'error_rates':
            error_count = analysis_result.get('total_errors', 0)
            if error_count > 100:
                alerts.append({
                    'type': 'high_error_rate',
                    'severity': 'critical',
                    'message': f"High error rate detected: {error_count} errors"
                })
                
        # 添加告警到列表
        self._alerts.extend(alerts)
        
    def get_analysis_results(self, metric_type: str = None) -> Dict:
        """获取分析结果"""
        if metric_type:
            return self._analysis_results.get(metric_type, {})
        return self._analysis_results
        
    def get_alerts(self, severity: str = None) -> List[Dict]:
        """获取告警"""
        if severity:
            return [alert for alert in self._alerts if alert['severity'] == severity]
        return self._alerts
        
    def generate_report(self, start_time: datetime = None, end_time: datetime = None) -> Dict:
        """生成分析报告"""
        if not start_time:
            start_time = datetime.now() - timedelta(days=1)
        if not end_time:
            end_time = datetime.now()
            
        report = {
            'period': {
                'start': start_time,
                'end': end_time
            },
            'metrics': {},
            'alerts': self.get_alerts(),
            'summary': {}
        }
        
        # 添加各类指标的汇总数据
        for metric_type in self._metrics_data.keys():
            report['metrics'][metric_type] = self.get_analysis_results(metric_type)
            
        return report
        
    def cleanup(self):
        """清理分析系统"""
        self._metrics_data.clear()
        self._analysis_results.clear()
        self._alerts.clear()
        self.logger.info("Analytics system cleaned up")

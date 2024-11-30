"""
任务调度系统
管理系统自动化任务的调度和执行
"""
import time
import logging
import threading
import schedule
from typing import Dict, List, Callable
from datetime import datetime, timedelta
from queue import PriorityQueue

class Task:
    """任务类"""
    def __init__(self, name: str, func: Callable, priority: int = 0):
        self.name = name
        self.func = func
        self.priority = priority
        self.last_run = None
        self.next_run = None
        self.enabled = True
        
    def __lt__(self, other):
        return self.priority > other.priority  # 优先级数字越大越优先

class TaskScheduler:
    """任务调度器"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, Task] = {}
        self.task_queue = PriorityQueue()
        self.running = False
        self.thread = None
        
    def add_task(self, name: str, func: Callable, schedule_type: str,
                 schedule_time: str, priority: int = 0) -> bool:
        """
        添加任务
        
        Args:
            name: 任务名称
            func: 任务函数
            schedule_type: 调度类型 (daily, weekly, interval)
            schedule_time: 调度时间
            priority: 优先级 (0-10，越大优先级越高)
            
        Returns:
            是否添加成功
        """
        try:
            task = Task(name, func, priority)
            
            # 设置调度
            if schedule_type == 'daily':
                schedule.every().day.at(schedule_time).do(self._run_task, task)
            elif schedule_type == 'weekly':
                day, time = schedule_time.split()
                getattr(schedule.every(), day.lower()).at(time).do(self._run_task, task)
            elif schedule_type == 'interval':
                interval = int(schedule_time)
                schedule.every(interval).minutes.do(self._run_task, task)
            else:
                self.logger.error(f"未知的调度类型: {schedule_type}")
                return False
                
            self.tasks[name] = task
            self.task_queue.put(task)
            return True
            
        except Exception as e:
            self.logger.error(f"添加任务失败 {name}: {str(e)}")
            return False
            
    def remove_task(self, name: str) -> bool:
        """删除任务"""
        try:
            if name in self.tasks:
                schedule.cancel_job(self.tasks[name])
                del self.tasks[name]
                # 重建优先队列
                with self.task_queue.mutex:
                    self.task_queue.queue = [t for t in self.task_queue.queue if t.name != name]
                return True
            return False
        except Exception as e:
            self.logger.error(f"删除任务失败 {name}: {str(e)}")
            return False
            
    def enable_task(self, name: str) -> bool:
        """启用任务"""
        try:
            if name in self.tasks:
                self.tasks[name].enabled = True
                return True
            return False
        except Exception as e:
            self.logger.error(f"启用任务失败 {name}: {str(e)}")
            return False
            
    def disable_task(self, name: str) -> bool:
        """禁用任务"""
        try:
            if name in self.tasks:
                self.tasks[name].enabled = False
                return True
            return False
        except Exception as e:
            self.logger.error(f"禁用任务失败 {name}: {str(e)}")
            return False
            
    def start(self):
        """启动调度器"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler)
            self.thread.daemon = True
            self.thread.start()
            self.logger.info("任务调度器已启动")
            
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.logger.info("任务调度器已停止")
        
    def _run_scheduler(self):
        """运行调度器"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"调度器运行错误: {str(e)}")
                
    def _run_task(self, task: Task):
        """运行任务"""
        if not task.enabled:
            return
            
        try:
            self.logger.info(f"开始执行任务: {task.name}")
            task.last_run = datetime.now()
            task.func()
            self.logger.info(f"任务执行完成: {task.name}")
        except Exception as e:
            self.logger.error(f"任务执行失败 {task.name}: {str(e)}")
            
    def get_task_status(self) -> List[Dict]:
        """获取任务状态"""
        status = []
        for task in self.tasks.values():
            status.append({
                "name": task.name,
                "enabled": task.enabled,
                "priority": task.priority,
                "last_run": task.last_run.isoformat() if task.last_run else None,
                "next_run": task.next_run.isoformat() if task.next_run else None
            })
        return sorted(status, key=lambda x: x['priority'], reverse=True)
        
    def get_upcoming_tasks(self, hours: int = 24) -> List[Dict]:
        """获取即将执行的任务"""
        upcoming = []
        now = datetime.now()
        end_time = now + timedelta(hours=hours)
        
        for job in schedule.jobs:
            next_run = job.next_run
            if next_run and now <= next_run <= end_time:
                task = self.tasks.get(job.job_func.args[0].name)
                if task and task.enabled:
                    upcoming.append({
                        "name": task.name,
                        "next_run": next_run.isoformat(),
                        "priority": task.priority
                    })
                    
        return sorted(upcoming, key=lambda x: x['next_run'])
        
    def optimize_schedule(self):
        """优化调度计划"""
        try:
            # 分析任务执行情况
            task_stats = {}
            for task in self.tasks.values():
                if task.last_run:
                    # 计算平均执行时间间隔
                    intervals = []
                    for job in schedule.jobs:
                        if job.job_func.args and job.job_func.args[0].name == task.name:
                            if job.last_run and job.next_run:
                                interval = (job.next_run - job.last_run).total_seconds()
                                intervals.append(interval)
                                
                    if intervals:
                        task_stats[task.name] = {
                            "avg_interval": sum(intervals) / len(intervals),
                            "priority": task.priority
                        }
                        
            # 优化建议
            recommendations = []
            for name, stats in task_stats.items():
                # 检查高优先级任务的执行间隔
                if stats["priority"] >= 8 and stats["avg_interval"] > 3600:
                    recommendations.append({
                        "task": name,
                        "suggestion": "考虑减少高优先级任务的执行间隔",
                        "current_interval": stats["avg_interval"]
                    })
                # 检查低优先级任务的执行频率
                elif stats["priority"] <= 3 and stats["avg_interval"] < 3600:
                    recommendations.append({
                        "task": name,
                        "suggestion": "考虑增加低优先级任务的执行间隔",
                        "current_interval": stats["avg_interval"]
                    })
                    
            return recommendations
            
        except Exception as e:
            self.logger.error(f"优化调度计划失败: {str(e)}")
            return []

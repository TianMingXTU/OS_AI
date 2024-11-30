"""
任务调度示例
展示任务调度系统的各种使用场景
"""
import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from Core.task_scheduler import TaskScheduler
from Tools.system_optimizer import SystemOptimizer
from Tools.system_tools import SystemTools

class TaskSchedulerExamples:
    """任务调度示例类"""
    def __init__(self):
        self.scheduler = TaskScheduler()
        self.optimizer = SystemOptimizer()
        self.system_tools = SystemTools()
        self.logger = logging.getLogger(__name__)
        
    def example_1_basic_scheduling(self):
        """示例1: 基础任务调度"""
        print("=== 基础任务调度示例 ===")
        
        # 1. 添加定时任务
        print("\n1. 添加定时任务...")
        
        def print_time():
            print(f"当前时间: {datetime.now()}")
            
        self.scheduler.add_task(
            name="time_printer",
            func=print_time,
            schedule_type="interval",
            schedule_time="1",  # 每1分钟执行
            priority=1
        )
        
        # 2. 查看任务状态
        print("\n2. 查看任务状态...")
        status = self.scheduler.get_task_status()
        print(f"任务状态: {status}")
        
        # 3. 等待任务执行
        print("\n3. 等待任务执行...")
        time.sleep(65)  # 等待超过1分钟
        
    def example_2_priority_scheduling(self):
        """示例2: 优先级调度"""
        print("=== 优先级调度示例 ===")
        
        # 1. 添加多个不同优先级的任务
        print("\n1. 添加优先级任务...")
        
        def high_priority_task():
            print("执行高优先级任务")
            time.sleep(2)
            
        def medium_priority_task():
            print("执行中优先级任务")
            time.sleep(1)
            
        def low_priority_task():
            print("执行低优先级任务")
            time.sleep(1)
            
        self.scheduler.add_task(
            name="high_priority",
            func=high_priority_task,
            schedule_type="interval",
            schedule_time="5",
            priority=10
        )
        
        self.scheduler.add_task(
            name="medium_priority",
            func=medium_priority_task,
            schedule_type="interval",
            schedule_time="5",
            priority=5
        )
        
        self.scheduler.add_task(
            name="low_priority",
            func=low_priority_task,
            schedule_type="interval",
            schedule_time="5",
            priority=1
        )
        
        # 2. 观察执行顺序
        print("\n2. 观察任务执行顺序...")
        time.sleep(10)
        
    def example_3_conditional_scheduling(self):
        """示例3: 条件任务调度"""
        print("=== 条件任务调度示例 ===")
        
        # 1. 创建条件任务
        print("\n1. 创建条件任务...")
        
        def check_system_load():
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            
            print(f"系统负载检查 - CPU: {cpu_percent}%, 内存: {memory_percent}%")
            
            if cpu_percent > 80:
                print("CPU使用率过高，执行性能优化...")
                self.optimizer.optimize_system_performance()
                
            if memory_percent > 85:
                print("内存使用率过高，执行系统清理...")
                self.system_tools.clean_system()
                
        self.scheduler.add_task(
            name="system_monitor",
            func=check_system_load,
            schedule_type="interval",
            schedule_time="2",  # 每2分钟检查
            priority=8
        )
        
        # 2. 模拟系统负载
        print("\n2. 模拟系统负载...")
        def stress_system():
            data = []
            for _ in range(1000000):
                data.append(object())
                
        stress_system()
        
        # 3. 观察任务响应
        print("\n3. 观察任务响应...")
        time.sleep(130)  # 等待超过2分钟
        
    def example_4_dynamic_scheduling(self):
        """示例4: 动态任务调度"""
        print("=== 动态任务调度示例 ===")
        
        # 1. 创建动态调度器
        print("\n1. 创建动态调度器...")
        
        class DynamicScheduler:
            def __init__(self, scheduler):
                self.scheduler = scheduler
                self.tasks = {}
                
            def add_dynamic_task(self, name, func, base_interval):
                self.tasks[name] = {
                    'func': func,
                    'base_interval': base_interval,
                    'current_interval': base_interval,
                    'last_result': None
                }
                
                def wrapper():
                    result = func()
                    self.adjust_interval(name, result)
                    return result
                    
                self.scheduler.add_task(
                    name=name,
                    func=wrapper,
                    schedule_type="interval",
                    schedule_time=str(base_interval),
                    priority=5
                )
                
            def adjust_interval(self, name, result):
                task = self.tasks[name]
                
                if result != task['last_result']:
                    # 如果结果变化，减少间隔
                    task['current_interval'] = max(
                        1, task['current_interval'] // 2
                    )
                else:
                    # 如果结果稳定，增加间隔
                    task['current_interval'] = min(
                        task['base_interval'] * 2,
                        task['current_interval'] + 1
                    )
                    
                task['last_result'] = result
                
                # 更新任务调度
                self.scheduler.remove_task(name)
                self.scheduler.add_task(
                    name=name,
                    func=task['func'],
                    schedule_type="interval",
                    schedule_time=str(task['current_interval']),
                    priority=5
                )
                
        # 2. 使用动态调度器
        print("\n2. 使用动态调度器...")
        dynamic_scheduler = DynamicScheduler(self.scheduler)
        
        def monitor_cpu():
            cpu_percent = psutil.cpu_percent()
            print(f"CPU使用率: {cpu_percent}%")
            return cpu_percent > 80
            
        dynamic_scheduler.add_dynamic_task(
            name="cpu_monitor",
            func=monitor_cpu,
            base_interval=5
        )
        
        # 3. 观察动态调整
        print("\n3. 观察动态调整...")
        time.sleep(30)
        
    def example_5_error_handling(self):
        """示例5: 错误处理"""
        print("=== 错误处理示例 ===")
        
        # 1. 创建可能失败的任务
        print("\n1. 创建容错任务...")
        
        class ResilientTask:
            def __init__(self, max_retries=3):
                self.max_retries = max_retries
                self.current_retries = 0
                
            def execute(self):
                try:
                    # 模拟可能失败的操作
                    if self.current_retries < 2:  # 前两次失败
                        self.current_retries += 1
                        raise Exception("任务执行失败")
                    
                    print("任务执行成功")
                    self.current_retries = 0
                    return True
                    
                except Exception as e:
                    print(f"错误: {str(e)}")
                    if self.current_retries >= self.max_retries:
                        print("达到最大重试次数")
                        self.current_retries = 0
                        return False
                    return self.execute()  # 重试
                    
        resilient_task = ResilientTask()
        
        # 2. 添加到调度器
        print("\n2. 添加容错任务到调度器...")
        self.scheduler.add_task(
            name="resilient_task",
            func=resilient_task.execute,
            schedule_type="interval",
            schedule_time="1",
            priority=7
        )
        
        # 3. 观察错误处理
        print("\n3. 观察错误处理...")
        time.sleep(65)  # 等待超过1分钟
        
    def run_all_examples(self):
        """运行所有示例"""
        examples = [
            self.example_1_basic_scheduling,
            self.example_2_priority_scheduling,
            self.example_3_conditional_scheduling,
            self.example_4_dynamic_scheduling,
            self.example_5_error_handling
        ]
        
        for example in examples:
            print("\n" + "="*50)
            print(f"运行示例: {example.__name__}")
            print("="*50)
            try:
                example()
            except Exception as e:
                print(f"示例运行失败: {str(e)}")
            time.sleep(2)  # 示例之间暂停2秒

def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行示例
    examples = TaskSchedulerExamples()
    examples.run_all_examples()

if __name__ == "__main__":
    main()

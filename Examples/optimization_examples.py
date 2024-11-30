"""
系统优化示例
展示系统优化工具的各种使用场景
"""
import os
import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from Core.task_scheduler import TaskScheduler
from Tools.system_optimizer import SystemOptimizer
from Tools.system_tools import SystemTools

class OptimizationExamples:
    """系统优化示例类"""
    def __init__(self):
        self.scheduler = TaskScheduler()
        self.optimizer = SystemOptimizer()
        self.system_tools = SystemTools()
        self.logger = logging.getLogger(__name__)
        
    def example_1_basic_optimization(self):
        """示例1: 基础系统优化"""
        print("=== 基础系统优化示例 ===")
        
        # 1. 清理系统
        print("\n1. 执行系统清理...")
        cleanup_results = self.system_tools.clean_system()
        print(f"清理结果: {cleanup_results}")
        
        # 2. 优化服务
        print("\n2. 优化系统服务...")
        service_results = self.optimizer.optimize_services()
        print(f"服务优化结果: {service_results}")
        
        # 3. 优化性能
        print("\n3. 优化系统性能...")
        performance_results = self.optimizer.optimize_system_performance()
        print(f"性能优化结果: {performance_results}")
        
    def example_2_scheduled_optimization(self):
        """示例2: 计划任务优化"""
        print("=== 计划任务优化示例 ===")
        
        # 1. 添加每日系统清理任务
        print("\n1. 添加每日清理任务...")
        self.scheduler.add_task(
            name="daily_cleanup",
            func=self.system_tools.clean_system,
            schedule_type="daily",
            schedule_time="03:00",
            priority=8
        )
        
        # 2. 添加每周系统优化任务
        print("\n2. 添加每周优化任务...")
        self.scheduler.add_task(
            name="weekly_optimization",
            func=self.optimizer.optimize_system_performance,
            schedule_type="weekly",
            schedule_time="sunday 04:00",
            priority=9
        )
        
        # 3. 查看任务状态
        print("\n3. 查看任务状态...")
        task_status = self.scheduler.get_task_status()
        print(f"任务状态: {task_status}")
        
    def example_3_smart_optimization(self):
        """示例3: 智能优化"""
        print("=== 智能优化示例 ===")
        
        # 1. 分析系统状态
        print("\n1. 分析系统状态...")
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"CPU使用率: {cpu_percent}%")
        print(f"内存使用率: {memory.percent}%")
        print(f"磁盘使用率: {disk.percent}%")
        
        # 2. 根据状态执行优化
        print("\n2. 执行智能优化...")
        if cpu_percent > 80:
            print("CPU使用率过高，优化性能...")
            self.optimizer.optimize_system_performance()
            
        if memory.percent > 85:
            print("内存使用率过高，清理系统...")
            self.system_tools.clean_system()
            
        if disk.percent > 90:
            print("磁盘使用率过高，分析空间...")
            space_analysis = self.system_tools.analyze_disk_space()
            print(f"空间分析结果: {space_analysis}")
            
    def example_4_custom_optimization(self):
        """示例4: 自定义优化"""
        print("=== 自定义优化示例 ===")
        
        def custom_optimization():
            """自定义优化函数"""
            results = []
            
            # 1. 系统清理
            cleanup_results = self.system_tools.clean_system()
            results.extend(cleanup_results)
            
            # 2. 性能优化
            if psutil.cpu_percent() > 70:
                performance_results = self.optimizer.optimize_system_performance()
                results.extend(performance_results)
                
            # 3. 网络优化
            ping_result = os.system("ping 8.8.8.8")
            if ping_result != 0:
                network_results = self.optimizer.optimize_network()
                results.extend(network_results)
                
            return results
            
        # 添加自定义优化任务
        print("\n1. 添加自定义优化任务...")
        self.scheduler.add_task(
            name="custom_optimization",
            func=custom_optimization,
            schedule_type="interval",
            schedule_time="60",  # 每60分钟执行一次
            priority=7
        )
        
        # 立即执行一次
        print("\n2. 执行自定义优化...")
        results = custom_optimization()
        print(f"优化结果: {results}")
        
    def example_5_optimization_chain(self):
        """示例5: 优化链"""
        print("=== 优化链示例 ===")
        
        class OptimizationStep:
            def __init__(self, name, condition, action):
                self.name = name
                self.condition = condition
                self.action = action
                
        # 创建优化链
        optimization_chain = [
            OptimizationStep(
                name="系统清理",
                condition=lambda: psutil.virtual_memory().percent > 80,
                action=self.system_tools.clean_system
            ),
            OptimizationStep(
                name="性能优化",
                condition=lambda: psutil.cpu_percent() > 75,
                action=self.optimizer.optimize_system_performance
            ),
            OptimizationStep(
                name="网络优化",
                condition=lambda: os.system("ping 8.8.8.8") != 0,
                action=self.optimizer.optimize_network
            ),
            OptimizationStep(
                name="电源优化",
                condition=lambda: psutil.sensors_battery() is not None and 
                                psutil.sensors_battery().power_plugged,
                action=self.optimizer.optimize_power_plan
            )
        ]
        
        # 执行优化链
        print("\n1. 执行优化链...")
        for step in optimization_chain:
            print(f"\n检查 {step.name}...")
            try:
                if step.condition():
                    print(f"条件满足，执行{step.name}...")
                    results = step.action()
                    print(f"优化结果: {results}")
                else:
                    print(f"条件不满足，跳过{step.name}")
            except Exception as e:
                print(f"执行{step.name}时出错: {str(e)}")
                
    def run_all_examples(self):
        """运行所有示例"""
        examples = [
            self.example_1_basic_optimization,
            self.example_2_scheduled_optimization,
            self.example_3_smart_optimization,
            self.example_4_custom_optimization,
            self.example_5_optimization_chain
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
    examples = OptimizationExamples()
    examples.run_all_examples()

if __name__ == "__main__":
    main()

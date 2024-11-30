"""
系统优化工具
提供更多系统优化功能
"""
import os
import sys
import psutil
import winreg
import logging
from typing import Dict, List, Optional
from pathlib import Path

class SystemOptimizer:
    """系统优化器"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def optimize_services(self) -> List[str]:
        """
        优化系统服务
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 获取所有服务
            import wmi
            c = wmi.WMI()
            
            # 可以安全禁用的服务列表
            safe_to_disable = {
                "TabletInputService": "平板电脑输入服务",
                "XboxGipSvc": "Xbox 配件管理服务",
                "XblAuthManager": "Xbox Live 验证管理器",
                "XblGameSave": "Xbox Live 游戏保存",
                "XboxNetApiSvc": "Xbox Live 网络服务"
            }
            
            for service in c.Win32_Service():
                if service.Name in safe_to_disable:
                    if service.StartMode != 'Disabled':
                        try:
                            # 停止并禁用服务
                            service.StopService()
                            service.ChangeStartMode('Disabled')
                            results.append(f"已禁用服务: {safe_to_disable[service.Name]}")
                        except Exception as e:
                            self.logger.error(f"禁用服务失败 {service.Name}: {str(e)}")
                            
        except Exception as e:
            self.logger.error(f"优化服务失败: {str(e)}")
            
        return results
        
    def optimize_power_plan(self) -> List[str]:
        """
        优化电源计划
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 设置高性能电源计划
            os.system('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
            
            # 自定义电源设置
            settings = {
                # 关闭硬盘
                '/setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 0012ee47-9041-4b5d-9b77-535fba8b1442 6738e2c4-e8a5-4a42-b16a-e040e769756e 0',
                # 关闭显示器
                '/setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 7516b95f-f776-4464-8c53-06167f40cc99 3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e 0',
                # 睡眠
                '/setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 238c9fa8-0aad-41ed-83f4-97be242c8f20 29f6c1db-86da-48c5-9fdb-f2b67b1f44da 0'
            }
            
            for setting in settings:
                os.system(f'powercfg {setting}')
                
            results.append("已优化电源计划")
            
        except Exception as e:
            self.logger.error(f"优化电源计划失败: {str(e)}")
            
        return results
        
    def optimize_network(self) -> List[str]:
        """
        优化网络设置
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 优化网络设置的注册表项
            network_settings = {
                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters': {
                    'TcpMaxDataRetransmissions': (winreg.REG_DWORD, 5),
                    'SackOpts': (winreg.REG_DWORD, 1),
                    'DefaultTTL': (winreg.REG_DWORD, 64)
                }
            }
            
            for key_path, values in network_settings.items():
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, 
                                       winreg.KEY_ALL_ACCESS)
                    for name, (type_, value) in values.items():
                        winreg.SetValueEx(key, name, 0, type_, value)
                    winreg.CloseKey(key)
                    results.append(f"已优化网络设置: {key_path}")
                except Exception as e:
                    self.logger.error(f"设置注册表失败 {key_path}: {str(e)}")
                    
            # 刷新DNS缓存
            os.system('ipconfig /flushdns')
            results.append("已刷新DNS缓存")
            
            # 重置网络堆栈
            os.system('netsh winsock reset')
            results.append("已重置网络堆栈")
            
        except Exception as e:
            self.logger.error(f"优化网络设置失败: {str(e)}")
            
        return results
        
    def optimize_visual_effects(self) -> List[str]:
        """
        优化视觉效果
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 性能相关的注册表设置
            visual_settings = {
                r'Control Panel\Desktop': {
                    'DragFullWindows': '0',
                    'FontSmoothing': '2',
                    'UserPreferencesMask': b'90 12 03 80',
                },
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced': {
                    'ListviewAlphaSelect': 0,
                    'ListviewShadow': 0,
                    'TaskbarAnimations': 0
                }
            }
            
            for key_path, values in visual_settings.items():
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                       winreg.KEY_ALL_ACCESS)
                    for name, value in values.items():
                        if isinstance(value, bytes):
                            winreg.SetValueEx(key, name, 0, winreg.REG_BINARY, value)
                        elif isinstance(value, int):
                            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                        else:
                            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                    winreg.CloseKey(key)
                    results.append(f"已优化视觉效果: {key_path}")
                except Exception as e:
                    self.logger.error(f"设置注册表失败 {key_path}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"优化视觉效果失败: {str(e)}")
            
        return results
        
    def optimize_system_performance(self) -> List[str]:
        """
        优化系统性能
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 调整系统性能选项
            performance_settings = {
                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management': {
                    'DisablePagingExecutive': (winreg.REG_DWORD, 1),
                    'LargeSystemCache': (winreg.REG_DWORD, 0)
                },
                r'SYSTEM\CurrentControlSet\Control\PriorityControl': {
                    'Win32PrioritySeparation': (winreg.REG_DWORD, 38)
                }
            }
            
            for key_path, values in performance_settings.items():
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, 
                                       winreg.KEY_ALL_ACCESS)
                    for name, (type_, value) in values.items():
                        winreg.SetValueEx(key, name, 0, type_, value)
                    winreg.CloseKey(key)
                    results.append(f"已优化性能设置: {key_path}")
                except Exception as e:
                    self.logger.error(f"设置注册表失败 {key_path}: {str(e)}")
                    
            # 调整进程优先级
            try:
                current_process = psutil.Process()
                current_process.nice(psutil.HIGH_PRIORITY_CLASS)
                results.append("已调整进程优先级")
            except Exception as e:
                self.logger.error(f"调整进程优先级失败: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"优化系统性能失败: {str(e)}")
            
        return results
        
    def optimize_privacy(self) -> List[str]:
        """
        优化隐私设置
        
        Returns:
            优化结果列表
        """
        results = []
        try:
            # 隐私相关的注册表设置
            privacy_settings = {
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo': {
                    'Enabled': (winreg.REG_DWORD, 0)
                },
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy': {
                    'TailoredExperiencesWithDiagnosticDataEnabled': (winreg.REG_DWORD, 0)
                },
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack': {
                    'Enabled': (winreg.REG_DWORD, 0)
                }
            }
            
            for key_path, values in privacy_settings.items():
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, 
                                       winreg.KEY_ALL_ACCESS)
                    for name, (type_, value) in values.items():
                        winreg.SetValueEx(key, name, 0, type_, value)
                    winreg.CloseKey(key)
                    results.append(f"已优化隐私设置: {key_path}")
                except Exception as e:
                    self.logger.error(f"设置注册表失败 {key_path}: {str(e)}")
                    
            # 禁用遥测服务
            telemetry_services = [
                "DiagTrack",
                "dmwappushservice"
            ]
            
            import wmi
            c = wmi.WMI()
            for service_name in telemetry_services:
                try:
                    for service in c.Win32_Service(Name=service_name):
                        service.StopService()
                        service.ChangeStartMode('Disabled')
                        results.append(f"已禁用遥测服务: {service_name}")
                except Exception as e:
                    self.logger.error(f"禁用服务失败 {service_name}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"优化隐私设置失败: {str(e)}")
            
        return results

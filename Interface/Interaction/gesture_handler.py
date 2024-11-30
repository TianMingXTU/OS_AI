"""
手势处理模块
负责系统的手势识别和处理
"""
import logging
from typing import Dict, List, Tuple, Optional
import numpy as np
from enum import Enum

class GestureType(Enum):
    """手势类型枚举"""
    SWIPE_LEFT = 'swipe_left'
    SWIPE_RIGHT = 'swipe_right'
    SWIPE_UP = 'swipe_up'
    SWIPE_DOWN = 'swipe_down'
    PINCH_IN = 'pinch_in'
    PINCH_OUT = 'pinch_out'
    ROTATE_CW = 'rotate_clockwise'
    ROTATE_CCW = 'rotate_counterclockwise'

class GestureState(Enum):
    """手势状态枚举"""
    STARTED = 'started'
    UPDATED = 'updated'
    ENDED = 'ended'
    CANCELLED = 'cancelled'

class GestureHandler:
    """手势处理器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._gesture_patterns: Dict[GestureType, List[np.ndarray]] = {}
        self._current_gesture: Optional[Tuple[GestureType, GestureState]] = None
        self._gesture_points: List[Tuple[float, float]] = []
        self._init_gesture_handler()
        
    def _init_gesture_handler(self):
        """初始化手势处理器"""
        self.logger.info("Initializing gesture handler...")
        self._init_gesture_patterns()
        
    def _init_gesture_patterns(self):
        """初始化手势模式"""
        # 为每种手势类型创建基本模式
        for gesture_type in GestureType:
            self._gesture_patterns[gesture_type] = self._create_gesture_pattern(gesture_type)
            
    def _create_gesture_pattern(self, gesture_type: GestureType) -> List[np.ndarray]:
        """创建手势模式"""
        patterns = []
        
        if gesture_type == GestureType.SWIPE_LEFT:
            # 向左滑动的模式
            pattern = np.array([
                [-1, 0],  # 向左移动
                [-1, 0],
                [-1, 0]
            ])
            patterns.append(pattern)
            
        elif gesture_type == GestureType.SWIPE_RIGHT:
            # 向右滑动的模式
            pattern = np.array([
                [1, 0],  # 向右移动
                [1, 0],
                [1, 0]
            ])
            patterns.append(pattern)
            
        # 添加更多手势模式...
        
        return patterns
        
    def handle_touch_event(self, x: float, y: float, state: GestureState):
        """
        处理触摸事件
        
        Args:
            x: x坐标
            y: y坐标
            state: 手势状态
        """
        if state == GestureState.STARTED:
            self._start_gesture(x, y)
        elif state == GestureState.UPDATED:
            self._update_gesture(x, y)
        elif state == GestureState.ENDED:
            self._end_gesture(x, y)
        elif state == GestureState.CANCELLED:
            self._cancel_gesture()
            
    def _start_gesture(self, x: float, y: float):
        """开始手势"""
        self._gesture_points = [(x, y)]
        self._current_gesture = None
        self.logger.debug(f"Started gesture at ({x}, {y})")
        
    def _update_gesture(self, x: float, y: float):
        """更新手势"""
        if not self._gesture_points:
            return
            
        self._gesture_points.append((x, y))
        
        # 实时识别手势
        gesture_type = self._recognize_gesture()
        if gesture_type:
            if self._current_gesture and self._current_gesture[0] != gesture_type:
                self.logger.debug(f"Gesture changed to {gesture_type.value}")
            self._current_gesture = (gesture_type, GestureState.UPDATED)
            
    def _end_gesture(self, x: float, y: float):
        """结束手势"""
        if not self._gesture_points:
            return
            
        self._gesture_points.append((x, y))
        gesture_type = self._recognize_gesture()
        
        if gesture_type:
            self._current_gesture = (gesture_type, GestureState.ENDED)
            self.logger.info(f"Completed gesture: {gesture_type.value}")
            
        self._gesture_points.clear()
        
    def _cancel_gesture(self):
        """取消手势"""
        self._gesture_points.clear()
        self._current_gesture = None
        self.logger.debug("Cancelled gesture")
        
    def _recognize_gesture(self) -> Optional[GestureType]:
        """识别手势类型"""
        if len(self._gesture_points) < 2:
            return None
            
        # 计算手势轨迹
        points = np.array(self._gesture_points)
        
        # 计算移动方向
        diff = np.diff(points, axis=0)
        mean_diff = np.mean(diff, axis=0)
        
        # 根据移动方向判断手势类型
        angle = np.arctan2(mean_diff[1], mean_diff[0])
        magnitude = np.linalg.norm(mean_diff)
        
        # 需要足够的移动距离才能识别
        if magnitude < 10:  # 最小移动距离阈值
            return None
            
        # 根据角度判断手势类型
        angle_deg = np.degrees(angle)
        
        if -45 <= angle_deg <= 45:
            return GestureType.SWIPE_RIGHT
        elif 135 <= angle_deg or angle_deg <= -135:
            return GestureType.SWIPE_LEFT
        elif 45 < angle_deg < 135:
            return GestureType.SWIPE_DOWN
        else:
            return GestureType.SWIPE_UP
            
    def get_current_gesture(self) -> Optional[Tuple[GestureType, GestureState]]:
        """获取当前手势"""
        return self._current_gesture
        
    def add_gesture_pattern(self, gesture_type: GestureType, pattern: np.ndarray):
        """添加手势模式"""
        if gesture_type not in self._gesture_patterns:
            self._gesture_patterns[gesture_type] = []
        self._gesture_patterns[gesture_type].append(pattern)
        
    def remove_gesture_pattern(self, gesture_type: GestureType, pattern: np.ndarray):
        """移除手势模式"""
        if gesture_type in self._gesture_patterns:
            patterns = self._gesture_patterns[gesture_type]
            if pattern in patterns:
                patterns.remove(pattern)
                
    def cleanup(self):
        """清理手势处理器"""
        self._gesture_patterns.clear()
        self._gesture_points.clear()
        self._current_gesture = None
        self.logger.info("Gesture handler cleaned up")

# OS_AI API 文档

## 核心 API

### SystemManager

系统管理器，负责核心组件的管理和协调。

```python
class SystemManager:
    def publish_event(event_type: str, data: any, priority: EventPriority = EventPriority.NORMAL)
    def report_error(message: str, error_type: ErrorType, level: ErrorLevel, exception: Optional[Exception] = None)
    def update_data(key: str, value: any, persist: bool = False)
    def get_system_status() -> dict
    def cleanup()
```

### EventBus

事件总线，处理系统内的事件通信。

```python
class EventBus:
    def subscribe(event_type: str, handler: Callable[[Event], None])
    def unsubscribe(event_type: str, handler: Callable[[Event], None])
    def publish(event: Event)
    def clear()
```

### DataStore

数据存储，管理系统数据。

```python
class DataStore:
    def set(key: str, value: Any, persist: bool = False)
    def get(key: str, default: Any = None) -> Any
    def delete(key: str)
    def clear_cache()
    def cleanup()
```

### ErrorHandler

错误处理器，统一处理系统错误。

```python
class ErrorHandler:
    def register_handler(error_type: ErrorType, handler: Callable[[SystemError], None])
    def register_recovery(error_type: ErrorType, recovery: Callable[[SystemError], bool])
    def handle_error(error_type: ErrorType, level: ErrorLevel, message: str, exception: Optional[Exception] = None)
    def get_error_history(error_type: Optional[ErrorType] = None, level: Optional[ErrorLevel] = None, limit: int = 100) -> List[SystemError]
    def clear_history()
```

## 界面 API

### ThemeManager

主题管理器，处理系统视觉风格。

```python
class ThemeManager:
    def apply_theme(theme_name: str)
    def get_style(component: str) -> dict
    def register_theme(name: str, theme_data: dict)
    def update_components()
```

### GestureHandler

手势处理器，处理手势输入。

```python
class GestureHandler:
    def register_gesture(gesture_type: str, handler: Callable)
    def unregister_gesture(gesture_type: str)
    def process_gesture(gesture_data: dict)
```

### VoiceHandler

语音处理器，处理语音命令。

```python
class VoiceHandler:
    def register_command(command: str, handler: Callable)
    def unregister_command(command: str)
    def process_input(audio_data: bytes)
```

### ExperienceOptimizer

体验优化器，优化用户体验。

```python
class ExperienceOptimizer:
    def track_behavior(behavior_data: dict)
    def get_suggestions() -> List[dict]
    def apply_optimization(optimization: dict)
```

## 数据类型

### Event

事件对象，表示系统中的事件。

```python
class Event:
    type: str           # 事件类型
    data: Any           # 事件数据
    priority: EventPriority  # 事件优先级
    timestamp: datetime # 事件时间戳
```

### SystemError

系统错误对象，表示系统中的错误。

```python
class SystemError:
    error_type: ErrorType    # 错误类型
    level: ErrorLevel        # 错误级别
    message: str            # 错误信息
    exception: Optional[Exception]  # 异常对象
    timestamp: datetime     # 错误时间戳
    traceback: Optional[str]  # 错误追踪信息
```

### Theme

主题对象，定义系统视觉风格。

```python
class Theme:
    name: str          # 主题名称
    colors: dict       # 颜色定义
    fonts: dict        # 字体定义
    spacing: dict      # 间距定义
    animations: dict   # 动画定义
```

## 枚举类型

### EventPriority

事件优先级枚举。

```python
class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
```

### ErrorType

错误类型枚举。

```python
class ErrorType(Enum):
    SYSTEM = 'system'
    NETWORK = 'network'
    DATABASE = 'database'
    UI = 'ui'
    USER = 'user'
    UNKNOWN = 'unknown'
```

### ErrorLevel

错误级别枚举。

```python
class ErrorLevel(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
```

## 使用示例

### 事件处理

```python
# 订阅事件
def handle_login(event):
    user_data = event.data
    print(f"用户登录: {user_data['username']}")
    
bus = EventBus()
bus.subscribe("user.login", handle_login)

# 发布事件
event = Event("user.login", {"username": "admin"}, EventPriority.HIGH)
bus.publish(event)
```

### 错误处理

```python
# 注册错误处理器
def handle_network_error(error):
    print(f"网络错误: {error.message}")
    
handler = ErrorHandler()
handler.register_handler(ErrorType.NETWORK, handle_network_error)

# 报告错误
handler.handle_error(
    ErrorType.NETWORK,
    ErrorLevel.ERROR,
    "连接服务器失败",
    exception=ConnectionError("超时")
)
```

### 主题切换

```python
# 注册自定义主题
theme = ThemeManager()
theme.register_theme("custom", {
    "colors": {
        "primary": "#007AFF",
        "secondary": "#5856D6"
    },
    "fonts": {
        "default": "Arial"
    }
})

# 应用主题
theme.apply_theme("custom")
```

### 手势处理

```python
# 注册手势处理器
def handle_swipe(direction):
    if direction == "left":
        print("返回上一页")
    elif direction == "right":
        print("前进下一页")
        
handler = GestureHandler()
handler.register_gesture("swipe", handle_swipe)

# 处理手势
handler.process_gesture({
    "type": "swipe",
    "direction": "left"
})
```

## 注意事项

1. 错误处理
- 始终使用错误处理器记录错误
- 实现适当的错误恢复机制
- 提供有意义的错误信息

2. 事件处理
- 避免事件处理器中的长时间操作
- 合理使用事件优先级
- 及时清理不需要的事件订阅

3. 数据管理
- 谨慎使用持久化存储
- 定期清理缓存数据
- 保护敏感数据

4. 性能优化
- 避免频繁的主题切换
- 优化手势识别算法
- 合理使用事件防抖和节流

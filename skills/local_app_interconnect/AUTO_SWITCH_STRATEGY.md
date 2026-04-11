# 智能前后台切换策略

## 概述

根据用户操作状态自动切换前后台模式：
- 用户操作手机 → 自动切换到后台
- 用户停止操作 → 自动切换回前台

## 切换逻辑

```
┌─────────────────────────────────────────────────────────────┐
│                    智能切换流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  任务开始执行 (前台模式)                                     │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  实时监测用户操作                                    │   │
│  │  - 屏幕触摸事件                                      │   │
│  │  - APP切换事件                                       │   │
│  │  - 按键事件                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ├──────────────┬──────────────┐                       │
│       ▼              ▼              ▼                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │检测到用户│   │用户持续 │   │用户停止 │                   │
│  │开始操作  │   │操作     │   │操作     │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│       │              │              │                       │
│       ▼              ▼              ▼                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │切换到   │   │保持后台 │   │切换回   │                   │
│  │后台模式 │   │模式     │   │前台模式 │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│       │              │              │                       │
│       ▼              ▼              ▼                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │通知用户 │   │后台继续 │   │用户可见 │                   │
│  │任务后台 │   │执行     │   │操作过程 │                   │
│  │运行中   │   │         │   │         │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 实现方案

### 方案1: 用户操作检测

```python
class UserOperationDetector:
    """用户操作检测器"""
    
    def __init__(self):
        self.last_operation_time = 0
        self.operation_count = 0
        self.is_user_operating = False
        self._threshold = 2.0  # 2秒无操作认为停止
        self._operation_window = 5.0  # 5秒内操作次数阈值
    
    def on_user_operation(self, operation_type: str):
        """用户操作事件"""
        current_time = time.time()
        
        # 记录操作
        self.last_operation_time = current_time
        self.operation_count += 1
        
        # 判断用户是否在操作
        if not self.is_user_operating:
            self.is_user_operating = True
            self._on_user_start_operating()
    
    def check_user_stopped(self):
        """检查用户是否停止操作"""
        if not self.is_user_operating:
            return False
        
        idle_time = time.time() - self.last_operation_time
        
        if idle_time > self._threshold:
            self.is_user_operating = False
            self.operation_count = 0
            self._on_user_stop_operating()
            return True
        
        return False
    
    def _on_user_start_operating(self):
        """用户开始操作回调"""
        logger.info("👤 检测到用户操作，切换到后台模式")
        # 触发切换到后台
        TaskModeSwitcher.switch_to_background()
    
    def _on_user_stop_operating(self):
        """用户停止操作回调"""
        logger.info("👀 用户停止操作，切换回前台模式")
        # 触发切换回前台
        TaskModeSwitcher.switch_to_foreground()
```

### 方案2: 任务模式切换器

```python
class TaskModeSwitcher:
    """任务模式切换器"""
    
    _current_mode = RunMode.FOREGROUND
    _on_mode_change_callbacks = []
    
    @classmethod
    def switch_to_background(cls):
        """切换到后台模式"""
        if cls._current_mode == RunMode.BACKGROUND:
            return
        
        cls._current_mode = RunMode.BACKGROUND
        
        # 通知用户
        notify_user("🔄 任务已切换到后台运行，您可以继续使用手机")
        
        # 触发回调
        for callback in cls._on_mode_change_callbacks:
            callback(RunMode.BACKGROUND)
    
    @classmethod
    def switch_to_foreground(cls):
        """切换回前台模式"""
        if cls._current_mode == RunMode.FOREGROUND:
            return
        
        cls._current_mode = RunMode.FOREGROUND
        
        # 通知用户
        notify_user("👁️ 任务已切换回前台，您可以看到操作过程")
        
        # 触发回调
        for callback in cls._on_mode_change_callbacks:
            callback(RunMode.FOREGROUND)
    
    @classmethod
    def get_current_mode(cls) -> RunMode:
        """获取当前模式"""
        return cls._current_mode
```

### 方案3: 智能任务执行器

```python
class SmartTaskExecutor:
    """智能任务执行器"""
    
    def __init__(self):
        self.detector = UserOperationDetector()
        self.switcher = TaskModeSwitcher
        self._monitor_thread = None
        self._running = False
    
    def start_monitoring(self):
        """启动监控"""
        self._running = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self._monitor_thread.start()
    
    def _monitor_loop(self):
        """监控循环"""
        while self._running:
            # 检查用户是否停止操作
            self.detector.check_user_stopped()
            
            # 每0.5秒检查一次
            time.sleep(0.5)
    
    def execute_task(self, task_func, *args, **kwargs):
        """执行任务"""
        # 注册用户操作回调
        self._register_operation_callbacks()
        
        # 开始执行
        return task_func(*args, **kwargs)
    
    def _register_operation_callbacks(self):
        """注册操作回调"""
        # 监听屏幕触摸
        # 监听APP切换
        # 监听按键事件
        pass
```

## 切换时机

| 事件 | 切换方向 | 延迟 |
|------|----------|------|
| 用户触摸屏幕 | 前台 → 后台 | 立即 |
| 用户切换APP | 前台 → 后台 | 立即 |
| 用户按Home键 | 前台 → 后台 | 立即 |
| 用户停止操作2秒 | 后台 → 前台 | 2秒后 |
| 任务完成 | 任意 → 前台 | 立即 |

## 通知消息

### 切换到后台
```
🔄 检测到您正在操作手机
任务已切换到后台运行
完成后会通知您
```

### 切换回前台
```
👁️ 您已停止操作
任务切换回前台运行
您可以看到操作过程
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_auto_switch | true | 启用自动切换 |
| idle_threshold | 2.0 | 空闲阈值(秒) |
| notify_on_switch | true | 切换时通知 |
| show_operation_process | true | 前台时显示操作过程 |

## 用户体验

### 场景1: 用户中途操作手机
```
1. 任务开始执行 (前台)
2. 用户接电话 → 自动切换后台
3. 用户挂断电话 → 2秒后切换回前台
4. 用户继续观看操作过程
```

### 场景2: 用户一直操作手机
```
1. 任务开始执行 (前台)
2. 用户开始回消息 → 自动切换后台
3. 用户继续回消息 → 保持后台
4. 用户停止操作 → 切换回前台
5. 任务完成 → 通知用户
```

### 场景3: 用户不操作手机
```
1. 任务开始执行 (前台)
2. 用户不操作 → 保持前台
3. 用户观看操作过程
4. 任务完成 → 显示结果
```

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

# 后台运行策略

## 概述

支持手机操作在后台运行，用户可以继续使用手机做其他事情，操作完成后自动通知结果。

## 后台运行架构

```
┌─────────────────────────────────────────────────────────────┐
│                    后台运行架构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户发起任务                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  任务队列管理器                                      │   │
│  │  - 接收任务                                          │   │
│  │  - 优先级排序                                        │   │
│  │  - 分配执行线程                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  后台执行线程                                        │   │
│  │  - 独立线程执行                                      │   │
│  │  - 不阻塞用户操作                                    │   │
│  │  - 定期检查任务状态                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ├──────────────┬──────────────┐                       │
│       ▼              ▼              ▼                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │用户继续 │   │后台执行 │   │状态监控 │                   │
│  │使用手机 │   │任务     │   │         │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│       │              │              │                       │
│       │              ▼              │                       │
│       │      ┌─────────────┐        │                       │
│       │      │ 任务完成    │        │                       │
│       │      └─────────────┘        │                       │
│       │              │              │                       │
│       └──────────────┴──────────────┘                       │
│                      │                                      │
│                      ▼                                      │
│              ┌─────────────┐                                │
│              │ 通知用户    │                                │
│              │ 返回结果    │                                │
│              └─────────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 实现方案

### 方案1: 线程池后台执行

```python
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class BackgroundExecutor:
    """后台执行器"""
    
    def __init__(self, max_workers=2):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = Queue()
        self.running_tasks = {}
        self.completed_tasks = {}
        self._lock = threading.Lock()
    
    def submit(self, task_id: str, task_func, *args, **kwargs):
        """提交后台任务"""
        future = self.executor.submit(task_func, *args, **kwargs)
        
        with self._lock:
            self.running_tasks[task_id] = {
                "future": future,
                "status": "running",
                "start_time": time.time()
            }
        
        # 设置完成回调
        future.add_done_callback(
            lambda f: self._on_task_complete(task_id, f)
        )
        
        return task_id
    
    def _on_task_complete(self, task_id: str, future):
        """任务完成回调"""
        with self._lock:
            if task_id in self.running_tasks:
                task = self.running_tasks.pop(task_id)
                task["status"] = "completed"
                task["result"] = future.result()
                task["end_time"] = time.time()
                self.completed_tasks[task_id] = task
        
        # 通知用户
        self._notify_user(task_id)
    
    def _notify_user(self, task_id: str):
        """通知用户任务完成"""
        # 发送通知到用户
        pass
    
    def get_status(self, task_id: str):
        """获取任务状态"""
        with self._lock:
            if task_id in self.running_tasks:
                return {"status": "running", **self.running_tasks[task_id]}
            if task_id in self.completed_tasks:
                return {"status": "completed", **self.completed_tasks[task_id]}
        return {"status": "not_found"}
```

### 方案2: 任务优先级队列

```python
class PriorityTaskQueue:
    """优先级任务队列"""
    
    def __init__(self):
        self.queues = {
            "high": Queue(),    # 高优先级: 支付、通话
            "normal": Queue(),  # 普通优先级: 搜索、获取信息
            "low": Queue()      # 低优先级: 后台同步
        }
        self._lock = threading.Lock()
    
    def add(self, task: dict, priority: str = "normal"):
        """添加任务"""
        with self._lock:
            self.queues[priority].put(task)
    
    def get_next(self):
        """获取下一个任务"""
        with self._lock:
            # 优先级顺序: high > normal > low
            for priority in ["high", "normal", "low"]:
                if not self.queues[priority].empty():
                    return self.queues[priority].get()
        return None
```

### 方案3: 用户活动检测

```python
class UserActivityDetector:
    """用户活动检测器"""
    
    def __init__(self):
        self.last_user_activity = time.time()
        self.user_active = True
        self._check_interval = 5  # 5秒检查一次
    
    def update_activity(self):
        """更新用户活动时间"""
        self.last_user_activity = time.time()
        self.user_active = True
    
    def is_user_idle(self, threshold: int = 30):
        """检查用户是否空闲"""
        idle_time = time.time() - self.last_user_activity
        return idle_time > threshold
    
    def should_run_background_task(self):
        """是否应该运行后台任务"""
        # 用户空闲时更适合运行后台任务
        return self.is_user_idle()
```

### 方案4: 智能调度策略

```python
class SmartScheduler:
    """智能调度器"""
    
    def __init__(self):
        self.activity_detector = UserActivityDetector()
        self.task_queue = PriorityTaskQueue()
    
    def schedule(self, task: dict):
        """智能调度任务"""
        
        # 判断任务类型
        task_type = task.get("type", "normal")
        
        # 根据用户活动决定执行策略
        if self.activity_detector.is_user_idle():
            # 用户空闲，立即执行
            return self._execute_immediately(task)
        else:
            # 用户活跃，后台执行
            return self._execute_background(task)
    
    def _execute_immediately(self, task):
        """立即执行"""
        # 前台执行，用户可见
        pass
    
    def _execute_background(self, task):
        """后台执行"""
        # 后台执行，不干扰用户
        pass
```

## 后台运行模式

### 模式1: 完全后台
```
用户发起任务 → 后台执行 → 用户继续使用手机 → 完成后通知
适用: 数据同步、文件下载、信息收集
```

### 模式2: 半后台
```
用户发起任务 → 前台开始 → 切换后台 → 完成后通知
适用: 需要初始操作的任务
```

### 模式3: 空闲执行
```
用户发起任务 → 等待用户空闲 → 后台执行 → 完成后通知
适用: 不紧急的后台任务
```

## 通知机制

### 通知类型

| 类型 | 触发时机 | 内容 |
|------|----------|------|
| 任务开始 | 任务提交时 | 任务ID、预计时间 |
| 进度更新 | 每步完成时 | 进度百分比 |
| 任务完成 | 任务结束时 | 结果摘要 |
| 任务失败 | 任务出错时 | 错误信息 |

### 通知方式

```python
class NotificationManager:
    """通知管理器"""
    
    def notify(self, task_id: str, event: str, data: dict):
        """发送通知"""
        notification = {
            "task_id": task_id,
            "event": event,
            "data": data,
            "timestamp": time.time()
        }
        
        # 发送到用户界面
        self._send_to_ui(notification)
        
        # 可选: 发送到通知栏
        if event == "completed":
            self._send_to_notification_bar(notification)
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_background | true | 启用后台运行 |
| max_background_tasks | 3 | 最大后台任务数 |
| notify_on_complete | true | 完成时通知 |
| notify_on_progress | false | 进度通知(可关闭减少打扰) |
| idle_threshold | 30 | 空闲阈值(秒) |
| task_timeout | 300 | 任务超时(秒) |

## 使用示例

### 示例1: 后台获取联系方式
```
用户: 帮我获取这个房源的联系方式，后台运行

执行:
1. 提交后台任务
2. 用户继续使用手机
3. 任务完成后通知: "✅ 已获取联系方式: 138****1234"
```

### 示例2: 后台搜索多个房源
```
用户: 帮我搜索淄博所有符合条件的商铺，后台运行

执行:
1. 提交后台任务
2. 用户继续使用手机
3. 任务完成后通知: "✅ 找到5个房源，已保存到备忘录"
```

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

# 手机操作保护策略

## 问题分析

当前 `xiaoyi_gui_agent` 执行时可能被用户操作打断：
- 用户切换APP
- 用户查看其他页面
- 用户接电话/回消息
- 屏幕超时锁屏

## 解决方案

### 策略1: 操作前状态保存与恢复

```
┌─────────────────────────────────────────────────────────────┐
│                    手机操作保护流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 1: 操作前准备                                  │   │
│  │  - 截图保存当前状态                                   │   │
│  │  - 记录当前APP和页面                                  │   │
│  │  - 记录当前时间戳                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 2: 执行操作                                    │   │
│  │  - 分步执行，每步验证                                │   │
│  │  - 检测页面是否被切换                                │   │
│  │  - 被打断时自动恢复                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 3: 操作后恢复                                  │   │
│  │  - 返回原APP                                         │   │
│  │  - 恢复原页面                                        │   │
│  │  - 通知用户操作完成                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 策略2: 分步执行与验证

```python
class ProtectedPhoneOperation:
    """受保护的手机操作"""
    
    def __init__(self):
        self.state_before = None
        self.current_step = 0
        self.total_steps = 0
    
    def execute(self, task: str):
        """执行受保护的操作"""
        
        # 1. 保存当前状态
        self.state_before = self._save_state()
        
        # 2. 分解任务为步骤
        steps = self._decompose_task(task)
        self.total_steps = len(steps)
        
        # 3. 逐步执行
        for i, step in enumerate(steps):
            self.current_step = i
            
            # 执行前检查
            if not self._verify_state():
                self._restore_state()
            
            # 执行步骤
            result = self._execute_step(step)
            
            # 执行后验证
            if not self._verify_result(result):
                self._retry_step(step)
        
        # 4. 恢复原状态
        self._restore_state()
        
        return result
    
    def _save_state(self):
        """保存当前状态"""
        return {
            "screenshot": self._take_screenshot(),
            "current_app": self._get_current_app(),
            "timestamp": time.time()
        }
    
    def _verify_state(self):
        """验证状态是否被改变"""
        current_app = self._get_current_app()
        return current_app == self.state_before["current_app"]
    
    def _restore_state(self):
        """恢复原状态"""
        # 返回原APP
        self._open_app(self.state_before["current_app"])
```

### 策略3: 用户通知机制

```
┌─────────────────────────────────────────────────────────────┐
│                    用户通知机制                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  操作开始前:                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ⚠️ 即将操作手机，请勿手动操作                        │   │
│  │  任务: 打开安居客APP获取联系方式                      │   │
│  │  预计耗时: 30秒                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  操作进行中:                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🔄 正在执行: 2/5 步                                 │   │
│  │  当前: 点击房源详情                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  操作完成后:                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ✅ 操作完成                                         │   │
│  │  结果: 已获取电话号码                                │   │
│  │  已恢复原页面                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 策略4: 断点续传机制

```python
class CheckpointManager:
    """断点管理器"""
    
    def __init__(self):
        self.checkpoints = []
        self.max_checkpoints = 10
    
    def save_checkpoint(self, step: int, state: dict):
        """保存断点"""
        checkpoint = {
            "step": step,
            "state": state,
            "timestamp": time.time()
        }
        self.checkpoints.append(checkpoint)
        
        if len(self.checkpoints) > self.max_checkpoints:
            self.checkpoints.pop(0)
    
    def load_last_checkpoint(self):
        """加载最后断点"""
        if self.checkpoints:
            return self.checkpoints[-1]
        return None
    
    def resume_from_checkpoint(self):
        """从断点恢复"""
        checkpoint = self.load_last_checkpoint()
        if checkpoint:
            # 恢复状态
            self._restore_state(checkpoint["state"])
            # 返回步骤
            return checkpoint["step"]
        return 0
```

### 策略5: 智能重试策略

| 打断类型 | 检测方式 | 恢复策略 |
|----------|----------|----------|
| APP切换 | 检测当前APP变化 | 返回目标APP |
| 页面跳转 | 截图对比 | 返回目标页面 |
| 屏幕锁定 | 检测屏幕状态 | 解锁屏幕 |
| 来电打断 | 检测通话状态 | 等待通话结束 |
| 用户操作 | 截图对比 | 提示用户等待 |

### 策略6: 执行模式选择

```python
class ExecutionMode:
    """执行模式"""
    
    # 模式1: 独占模式 - 用户完全不能操作
    EXCLUSIVE = "exclusive"
    
    # 模式2: 共享模式 - 允许用户查看但不能操作
    SHARED = "shared"
    
    # 模式3: 后台模式 - 最小化干扰
    BACKGROUND = "background"


def select_mode(task_type: str) -> str:
    """选择执行模式"""
    
    if task_type in ["拨打电话", "发送消息", "支付操作"]:
        return ExecutionMode.EXCLUSIVE
    
    if task_type in ["查看详情", "搜索列表", "获取信息"]:
        return ExecutionMode.SHARED
    
    return ExecutionMode.BACKGROUND
```

## 实现方案

### 方案1: GUI Agent 增强

```python
def xiaoyi_gui_agent_protected(query: str, mode: str = "shared"):
    """受保护的GUI操作"""
    
    # 1. 通知用户
    notify_user(f"⚠️ 即将操作手机: {query}")
    
    # 2. 保存状态
    state_before = save_current_state()
    
    # 3. 执行操作
    try:
        result = execute_with_checkpoints(query)
    except InterruptedError:
        # 检测到打断
        restore_state(state_before)
        result = retry_with_protection(query)
    
    # 4. 恢复状态
    restore_state(state_before)
    
    # 5. 通知完成
    notify_user(f"✅ 操作完成")
    
    return result
```

### 方案2: 操作队列

```python
class OperationQueue:
    """操作队列"""
    
    def __init__(self):
        self.queue = []
        self.executing = False
    
    def add(self, operation: dict):
        """添加操作"""
        self.queue.append(operation)
        
        if not self.executing:
            self._execute_next()
    
    def _execute_next(self):
        """执行下一个"""
        if not self.queue:
            return
        
        self.executing = True
        op = self.queue.pop(0)
        
        try:
            self._execute_protected(op)
        finally:
            self.executing = False
            self._execute_next()
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_protection | true | 启用保护机制 |
| notify_before | true | 操作前通知用户 |
| notify_progress | true | 显示进度 |
| auto_restore | true | 自动恢复原状态 |
| max_retry | 2 | 最大重试次数 |
| timeout_per_step | 10 | 每步超时(秒) |

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

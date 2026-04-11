# 后台操作节点汇报策略

## 概述

后台执行任务时，每完成一个关键节点，自动发送截图汇报给用户，让用户了解任务进度。

## 汇报架构

```
┌─────────────────────────────────────────────────────────────┐
│                    后台节点汇报流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  后台任务执行                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  节点1: 打开APP                                     │   │
│  │  - 执行操作                                         │   │
│  │  - 截图                                             │   │
│  │  - 发送汇报                                         │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  节点2: 搜索内容                                     │   │
│  │  - 执行操作                                         │   │
│  │  - 截图                                             │   │
│  │  - 发送汇报                                         │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  节点3: 点击详情                                     │   │
│  │  - 执行操作                                         │   │
│  │  - 截图                                             │   │
│  │  - 发送汇报                                         │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  节点4: 获取结果                                     │   │
│  │  - 执行操作                                         │   │
│  │  - 截图                                             │   │
│  │  - 发送最终汇报                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 汇报内容

### 节点汇报格式

```
┌─────────────────────────────────────┐
│ 📸 节点汇报                          │
│                                     │
│ 任务: 获取商铺联系方式               │
│ 节点: 2/4 搜索房源                  │
│ 状态: ✅ 完成                       │
│ 时间: 15:27:30                     │
│                                     │
│ [截图]                              │
└─────────────────────────────────────┘
```

### 最终汇报格式

```
┌─────────────────────────────────────┐
│ ✅ 任务完成汇报                      │
│                                     │
│ 任务: 获取商铺联系方式               │
│ 结果: 已获取电话 138****1234        │
│ 耗时: 45秒                          │
│ 节点: 4/4 全部完成                  │
│                                     │
│ [最终截图]                          │
└─────────────────────────────────────┘
```

## 实现方案

### 方案1: 节点管理器

```python
class NodeReporter:
    """节点汇报器"""
    
    def __init__(self):
        self.current_node = 0
        self.total_nodes = 0
        self.task_name = ""
        self.screenshots = []
    
    def start_task(self, task_name: str, total_nodes: int):
        """开始任务"""
        self.task_name = task_name
        self.total_nodes = total_nodes
        self.current_node = 0
        self.screenshots = []
        
        # 发送开始汇报
        self._send_start_report()
    
    def report_node(self, node_name: str, screenshot_path: str = None):
        """汇报节点"""
        self.current_node += 1
        
        # 截图
        if not screenshot_path:
            screenshot_path = self._take_screenshot()
        
        # 保存截图
        self.screenshots.append({
            "node": self.current_node,
            "name": node_name,
            "path": screenshot_path,
            "time": datetime.now()
        })
        
        # 发送汇报
        self._send_node_report(node_name, screenshot_path)
    
    def complete_task(self, result: str):
        """完成任务"""
        # 截图
        screenshot_path = self._take_screenshot()
        
        # 发送最终汇报
        self._send_final_report(result, screenshot_path)
    
    def _send_node_report(self, node_name: str, screenshot_path: str):
        """发送节点汇报"""
        message = f"""
📸 节点汇报

任务: {self.task_name}
节点: {self.current_node}/{self.total_nodes} {node_name}
状态: ✅ 完成
时间: {datetime.now().strftime('%H:%M:%S')}
"""
        # 发送消息 + 截图
        send_message_with_image(message, screenshot_path)
    
    def _send_final_report(self, result: str, screenshot_path: str):
        """发送最终汇报"""
        message = f"""
✅ 任务完成汇报

任务: {self.task_name}
结果: {result}
节点: {self.total_nodes}/{self.total_nodes} 全部完成
"""
        # 发送消息 + 截图
        send_message_with_image(message, screenshot_path)
```

### 方案2: 自动截图

```python
class AutoScreenshot:
    """自动截图器"""
    
    def __init__(self, save_dir: str = "/tmp/task_screenshots"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.screenshot_count = 0
    
    def capture(self, label: str = "") -> str:
        """截图"""
        self.screenshot_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{self.screenshot_count}_{timestamp}.png"
        filepath = os.path.join(self.save_dir, filename)
        
        # 执行截图
        # 这里需要调用手机截图API
        # result = take_screenshot(filepath)
        
        logger.info(f"📸 截图已保存: {filepath}")
        return filepath
    
    def capture_and_send(self, label: str, message: str):
        """截图并发送"""
        filepath = self.capture(label)
        send_message_with_image(message, filepath)
        return filepath
```

### 方案3: 节点定义

```python
@dataclass
class TaskNode:
    """任务节点"""
    index: int
    name: str
    action: str
    report_on_complete: bool = True  # 完成时是否汇报
    take_screenshot: bool = True     # 是否截图


# 预定义任务节点
TASK_NODES = {
    "get_contact": [
        TaskNode(1, "打开APP", "open_app", True, True),
        TaskNode(2, "搜索内容", "search", True, True),
        TaskNode(3, "点击详情", "click_detail", True, True),
        TaskNode(4, "获取联系方式", "get_contact", True, True),
    ],
    "find_house": [
        TaskNode(1, "打开找房APP", "open_app", True, True),
        TaskNode(2, "设置筛选条件", "set_filter", True, True),
        TaskNode(3, "查看搜索结果", "view_results", True, True),
        TaskNode(4, "选择房源", "select_house", True, True),
        TaskNode(5, "获取联系方式", "get_contact", True, True),
    ],
    "compare_price": [
        TaskNode(1, "打开购物APP", "open_app", True, True),
        TaskNode(2, "搜索商品", "search", True, True),
        TaskNode(3, "记录价格", "record_price", True, True),
        TaskNode(4, "切换APP比价", "switch_app", True, True),
        TaskNode(5, "生成比价报告", "generate_report", True, True),
    ]
}
```

## 汇报时机

| 节点类型 | 汇报时机 | 截图 |
|----------|----------|------|
| 打开APP | APP启动后 | ✅ |
| 搜索 | 搜索结果加载后 | ✅ |
| 点击 | 页面跳转后 | ✅ |
| 获取信息 | 信息显示后 | ✅ |
| 任务完成 | 最终结果 | ✅ |

## 汇报频率控制

```python
class ReportThrottle:
    """汇报频率控制"""
    
    def __init__(
        self,
        min_interval: float = 3.0,    # 最小间隔(秒)
        max_reports: int = 10          # 最大汇报次数
    ):
        self.min_interval = min_interval
        self.max_reports = max_reports
        self.last_report_time = 0
        self.report_count = 0
    
    def should_report(self) -> bool:
        """是否应该汇报"""
        current_time = time.time()
        
        # 检查间隔
        if current_time - self.last_report_time < self.min_interval:
            return False
        
        # 检查次数
        if self.report_count >= self.max_reports:
            return False
        
        return True
    
    def record_report(self):
        """记录汇报"""
        self.last_report_time = time.time()
        self.report_count += 1
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_node_report | true | 启用节点汇报 |
| enable_screenshot | true | 启用截图 |
| report_interval | 3.0 | 最小汇报间隔(秒) |
| max_reports | 10 | 最大汇报次数 |
| save_screenshots | true | 保存截图到本地 |

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

#!/usr/bin/env python3
"""
后台执行模块
终极鸽子王 V26.0 - 支持手机操作后台运行

核心能力:
1. 后台线程执行 - 不阻塞用户操作
2. 任务队列管理 - 优先级调度
3. 用户活动检测 - 智能调度
4. 完成通知机制 - 及时反馈结果
"""

import os
import sys
import time
import json
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, Future
from queue import Queue, PriorityQueue
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============== 枚举定义 ==============

class TaskPriority(Enum):
    """任务优先级"""
    HIGH = 1      # 高优先级: 支付、通话
    NORMAL = 2    # 普通优先级: 搜索、获取信息
    LOW = 3       # 低优先级: 后台同步


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunMode(Enum):
    """运行模式"""
    FOREGROUND = "foreground"  # 前台运行
    BACKGROUND = "background"  # 后台运行
    IDLE = "idle"              # 空闲时运行


# ============== 数据结构 ==============

@dataclass
class BackgroundTask:
    """后台任务"""
    task_id: str
    name: str
    func: Callable
    args: tuple = ()
    kwargs: Dict = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    mode: RunMode = RunMode.BACKGROUND
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = ""
    start_time: float = 0.0
    end_time: float = 0.0
    progress: int = 0  # 0-100


# ============== 用户活动检测器 ==============

class UserActivityDetector:
    """用户活动检测器"""
    
    def __init__(self, idle_threshold: int = 30):
        self.idle_threshold = idle_threshold
        self.last_activity_time = time.time()
        self._lock = threading.Lock()
    
    def update_activity(self):
        """更新用户活动"""
        with self._lock:
            self.last_activity_time = time.time()
    
    def get_idle_time(self) -> float:
        """获取空闲时间"""
        with self._lock:
            return time.time() - self.last_activity_time
    
    def is_user_idle(self) -> bool:
        """用户是否空闲"""
        return self.get_idle_time() > self.idle_threshold


# ============== 任务队列 ==============

class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self._queue: List[BackgroundTask] = []
        self._lock = threading.Lock()
        self._event = threading.Event()
    
    def put(self, task: BackgroundTask):
        """添加任务"""
        with self._lock:
            # 按优先级插入
            inserted = False
            for i, t in enumerate(self._queue):
                if task.priority.value < t.priority.value:
                    self._queue.insert(i, task)
                    inserted = True
                    break
            
            if not inserted:
                self._queue.append(task)
            
            self._event.set()
        
        logger.info(f"📥 任务入队: {task.name} (优先级: {task.priority.name})")
    
    def get(self, timeout: float = None) -> Optional[BackgroundTask]:
        """获取任务"""
        while True:
            with self._lock:
                if self._queue:
                    return self._queue.pop(0)
            
            # 等待新任务
            self._event.clear()
            if not self._event.wait(timeout=timeout):
                return None
    
    def size(self) -> int:
        """队列大小"""
        with self._lock:
            return len(self._queue)


# ============== 后台执行器 ==============

class BackgroundExecutor:
    """后台执行器"""
    
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers
        self.task_queue = TaskQueue()
        self.activity_detector = UserActivityDetector()
        
        self.running_tasks: Dict[str, BackgroundTask] = {}
        self.completed_tasks: Dict[str, BackgroundTask] = {}
        
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._workers: List[threading.Thread] = []
        self._running = False
        self._lock = threading.Lock()
        
        # 回调函数
        self._on_task_complete: Optional[Callable] = None
        self._on_task_progress: Optional[Callable] = None
    
    def start(self):
        """启动执行器"""
        if self._running:
            return
        
        self._running = True
        
        # 启动工作线程
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"BackgroundWorker-{i}",
                daemon=True
            )
            worker.start()
            self._workers.append(worker)
        
        logger.info(f"🚀 后台执行器已启动 (workers: {self.max_workers})")
    
    def stop(self):
        """停止执行器"""
        self._running = False
        self._executor.shutdown(wait=False)
        logger.info("🛑 后台执行器已停止")
    
    def submit(
        self,
        task_name: str,
        task_func: Callable,
        args: tuple = (),
        kwargs: Dict = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        mode: RunMode = RunMode.BACKGROUND
    ) -> str:
        """
        提交后台任务
        
        Args:
            task_name: 任务名称
            task_func: 任务函数
            args: 位置参数
            kwargs: 关键字参数
            priority: 优先级
            mode: 运行模式
        
        Returns:
            任务ID
        """
        task_id = self._generate_task_id(task_name)
        
        task = BackgroundTask(
            task_id=task_id,
            name=task_name,
            func=task_func,
            args=args,
            kwargs=kwargs or {},
            priority=priority,
            mode=mode
        )
        
        # 检查运行模式
        if mode == RunMode.IDLE and not self.activity_detector.is_user_idle():
            logger.info(f"⏳ 任务等待空闲: {task_name}")
        
        self.task_queue.put(task)
        
        return task_id
    
    def get_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        with self._lock:
            if task_id in self.running_tasks:
                task = self.running_tasks[task_id]
                return {
                    "task_id": task.task_id,
                    "name": task.name,
                    "status": task.status.value,
                    "progress": task.progress,
                    "elapsed": time.time() - task.start_time if task.start_time else 0
                }
            
            if task_id in self.completed_tasks:
                task = self.completed_tasks[task_id]
                return {
                    "task_id": task.task_id,
                    "name": task.name,
                    "status": task.status.value,
                    "result": task.result,
                    "error": task.error,
                    "elapsed": task.end_time - task.start_time if task.end_time else 0
                }
        
        return None
    
    def get_result(self, task_id: str) -> Any:
        """获取任务结果"""
        status = self.get_status(task_id)
        if status and status["status"] == "completed":
            with self._lock:
                if task_id in self.completed_tasks:
                    return self.completed_tasks[task_id].result
        return None
    
    def cancel(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            if task_id in self.running_tasks:
                self.running_tasks[task_id].status = TaskStatus.CANCELLED
                return True
        return False
    
    def set_callbacks(
        self,
        on_complete: Callable = None,
        on_progress: Callable = None
    ):
        """设置回调函数"""
        self._on_task_complete = on_complete
        self._on_task_progress = on_progress
    
    def _worker_loop(self):
        """工作线程循环"""
        while self._running:
            try:
                # 获取任务
                task = self.task_queue.get(timeout=1.0)
                if not task:
                    continue
                
                # 检查是否需要等待空闲
                if task.mode == RunMode.IDLE:
                    while not self.activity_detector.is_user_idle():
                        time.sleep(5)
                        if task.status == TaskStatus.CANCELLED:
                            break
                
                # 执行任务
                self._execute_task(task)
                
            except Exception as e:
                logger.error(f"工作线程异常: {e}")
    
    def _execute_task(self, task: BackgroundTask):
        """执行任务"""
        logger.info(f"▶️ 开始执行: {task.name}")
        
        task.status = TaskStatus.RUNNING
        task.start_time = time.time()
        
        with self._lock:
            self.running_tasks[task.task_id] = task
        
        try:
            # 执行任务函数
            result = task.func(*task.args, **task.kwargs)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.progress = 100
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            logger.error(f"❌ 任务失败: {task.name} - {e}")
        
        finally:
            task.end_time = time.time()
            
            with self._lock:
                if task.task_id in self.running_tasks:
                    del self.running_tasks[task.task_id]
                self.completed_tasks[task.task_id] = task
            
            # 回调通知
            if self._on_task_complete:
                self._on_task_complete(task)
            
            logger.info(f"✅ 任务完成: {task.name} (耗时: {task.end_time - task.start_time:.1f}s)")
    
    def _generate_task_id(self, name: str) -> str:
        """生成任务ID"""
        import hashlib
        timestamp = str(time.time())
        return hashlib.md5(f"{name}:{timestamp}".encode()).hexdigest()[:12]


# ============== 通知管理器 ==============

class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.notifications: List[Dict] = []
        self._lock = threading.Lock()
    
    def notify(self, task_id: str, event: str, data: Dict):
        """发送通知"""
        notification = {
            "task_id": task_id,
            "event": event,
            "data": data,
            "timestamp": time.time()
        }
        
        with self._lock:
            self.notifications.append(notification)
            # 保留最近100条
            if len(self.notifications) > 100:
                self.notifications = self.notifications[-100:]
        
        logger.info(f"📢 通知: {event} - {data}")
    
    def get_notifications(self, since: float = 0) -> List[Dict]:
        """获取通知"""
        with self._lock:
            return [n for n in self.notifications if n["timestamp"] > since]


# ============== 后台任务管理器 ==============

class BackgroundTaskManager:
    """后台任务管理器"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.executor = BackgroundExecutor(max_workers=2)
        self.notifier = NotificationManager()
        self._initialized = True
        
        # 设置回调
        self.executor.set_callbacks(
            on_complete=self._on_task_complete
        )
    
    def start(self):
        """启动管理器"""
        self.executor.start()
    
    def stop(self):
        """停止管理器"""
        self.executor.stop()
    
    def submit_task(
        self,
        name: str,
        func: Callable,
        args: tuple = (),
        kwargs: Dict = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        mode: RunMode = RunMode.BACKGROUND
    ) -> str:
        """提交任务"""
        task_id = self.executor.submit(
            task_name=name,
            task_func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            mode=mode
        )
        
        # 通知任务开始
        self.notifier.notify(task_id, "task_started", {"name": name})
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        return self.executor.get_status(task_id)
    
    def get_task_result(self, task_id: str) -> Any:
        """获取任务结果"""
        return self.executor.get_result(task_id)
    
    def _on_task_complete(self, task: BackgroundTask):
        """任务完成回调"""
        self.notifier.notify(
            task.task_id,
            "task_completed" if task.status == TaskStatus.COMPLETED else "task_failed",
            {
                "name": task.name,
                "result": task.result,
                "error": task.error
            }
        )


# ============== 全局实例 ==============

_manager = None

def get_background_manager() -> BackgroundTaskManager:
    """获取全局后台任务管理器"""
    global _manager
    if _manager is None:
        _manager = BackgroundTaskManager()
        _manager.start()
    return _manager


# ============== 测试 ==============

def test_background():
    """测试后台执行"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          后台执行模块测试                                              ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    manager = get_background_manager()
    
    # 定义测试任务
    def long_task(name: str, duration: int):
        """模拟长时间任务"""
        for i in range(duration):
            time.sleep(1)
            print(f"  [{name}] 进度: {(i+1)/duration*100:.0f}%")
        return f"任务 {name} 完成"
    
    # 提交后台任务
    task_id1 = manager.submit_task(
        name="获取联系方式",
        func=long_task,
        args=("联系方式", 3),
        priority=TaskPriority.NORMAL,
        mode=RunMode.BACKGROUND
    )
    
    print(f"📤 任务已提交: {task_id1}")
    print("📱 用户可以继续使用手机...")
    
    # 等待任务完成
    time.sleep(5)
    
    # 获取结果
    status = manager.get_task_status(task_id1)
    print(f"\n📊 任务状态: {status}")
    
    result = manager.get_task_result(task_id1)
    print(f"📦 任务结果: {result}")


if __name__ == "__main__":
    test_background()

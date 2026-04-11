#!/usr/bin/env python3
"""
任务分配与执行引擎
V2.7.0 - 2026-04-10
"""

import time
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"

class TaskType(Enum):
    QUERY = "query"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ORCHESTRATE = "orchestrate"
    EXECUTE = "execute"

@dataclass
class SubTask:
    """子任务"""
    id: str
    type: TaskType
    intent: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any] = field(default_factory=dict)
    assigned_layer: int = 4
    assigned_skill: Optional[str] = None
    priority: int = 0
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    latency: float = 0.0
    error: Optional[str] = None

@dataclass
class Task:
    """任务"""
    id: str
    intent: str
    entities: Dict[str, Any]
    constraints: Dict[str, Any]
    subtasks: List[SubTask] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None

class TaskParser:
    """任务解析器"""
    
    def parse(self, user_input: str) -> Task:
        """解析用户输入"""
        task_id = f"task_{int(time.time() * 1000)}"
        
        intent = self._extract_intent(user_input)
        entities = self._extract_entities(user_input)
        constraints = self._extract_constraints(user_input)
        
        return Task(
            id=task_id,
            intent=intent,
            entities=entities,
            constraints=constraints
        )
    
    def _extract_intent(self, text: str) -> str:
        patterns = {
            "search": ["搜索", "查找", "找一下", "search", "find"],
            "create": ["创建", "新建", "添加", "create", "add", "new"],
            "update": ["更新", "修改", "编辑", "update", "edit", "modify"],
            "delete": ["删除", "移除", "清除", "delete", "remove"],
            "query": ["查询", "获取", "查看", "query", "get", "show"],
        }
        
        text_lower = text.lower()
        for intent, keywords in patterns.items():
            if any(kw in text_lower for kw in keywords):
                return intent
        
        return "query"
    
    def _extract_entities(self, text: str) -> Dict:
        """提取实体"""
        entities = {}
        
        # 简单实体提取
        if "备忘录" in text or "note" in text.lower():
            entities["target"] = "note"
        elif "日程" in text or "calendar" in text.lower():
            entities["target"] = "calendar"
        elif "闹钟" in text or "alarm" in text.lower():
            entities["target"] = "alarm"
        
        return entities
    
    def _extract_constraints(self, text: str) -> Dict:
        """提取约束"""
        constraints = {}
        
        # 时间约束
        if "今天" in text:
            constraints["time"] = "today"
        elif "明天" in text:
            constraints["time"] = "tomorrow"
        
        return constraints

class TaskDistributor:
    """任务分配器"""
    
    def __init__(self):
        self._skill_registry: Dict[str, Callable] = {}
    
    def register_skill(self, name: str, handler: Callable):
        """注册技能"""
        self._skill_registry[name] = handler
    
    def distribute(self, task: Task) -> List[SubTask]:
        """分配任务"""
        # 1. 分解任务
        subtasks = self._decompose(task)
        
        # 2. 分析依赖
        self._analyze_dependencies(subtasks)
        
        # 3. 分配资源
        for subtask in subtasks:
            subtask.assigned_layer = self._assign_layer(subtask)
            subtask.assigned_skill = self._assign_skill(subtask)
            subtask.priority = self._calculate_priority(subtask)
        
        # 4. 拓扑排序
        return self._topological_sort(subtasks)
    
    def _decompose(self, task: Task) -> List[SubTask]:
        """分解任务"""
        subtasks = []
        
        # 根据意图分解
        if task.intent == "create":
            # 创建操作分解为：验证 -> 创建 -> 确认
            subtasks.append(SubTask(
                id=f"{task.id}_validate",
                type=TaskType.QUERY,
                intent="validate",
                inputs=task.entities
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_create",
                type=TaskType.CREATE,
                intent="create",
                inputs=task.entities,
                dependencies=[f"{task.id}_validate"]
            ))
        
        elif task.intent == "search":
            # 搜索操作分解为：搜索 -> 排序 -> 返回
            subtasks.append(SubTask(
                id=f"{task.id}_search",
                type=TaskType.QUERY,
                intent="search",
                inputs=task.entities
            ))
        
        else:
            # 默认单任务
            subtasks.append(SubTask(
                id=f"{task.id}_execute",
                type=TaskType.EXECUTE,
                intent=task.intent,
                inputs=task.entities
            ))
        
        return subtasks
    
    def _analyze_dependencies(self, subtasks: List[SubTask]):
        """分析依赖"""
        task_map = {t.id: t for t in subtasks}
        
        for task in subtasks:
            resolved_deps = []
            for dep_id in task.dependencies:
                if dep_id in task_map:
                    resolved_deps.append(dep_id)
            task.dependencies = resolved_deps
    
    def _assign_layer(self, subtask: SubTask) -> int:
        """分配层级"""
        layer_map = {
            TaskType.QUERY: 2,
            TaskType.ORCHESTRATE: 3,
            TaskType.EXECUTE: 4,
            TaskType.CREATE: 4,
            TaskType.UPDATE: 4,
            TaskType.DELETE: 4,
        }
        return layer_map.get(subtask.type, 4)
    
    def _assign_skill(self, subtask: SubTask) -> Optional[str]:
        """分配技能"""
        # 根据意图和目标分配技能
        target = subtask.inputs.get("target", "")
        
        if target == "note":
            return "note_skill"
        elif target == "calendar":
            return "calendar_skill"
        elif target == "alarm":
            return "alarm_skill"
        
        return None
    
    def _calculate_priority(self, subtask: SubTask) -> int:
        """计算优先级"""
        priority_map = {
            TaskType.QUERY: 10,
            TaskType.CREATE: 8,
            TaskType.UPDATE: 7,
            TaskType.DELETE: 6,
            TaskType.EXECUTE: 5,
            TaskType.ORCHESTRATE: 3,
        }
        return priority_map.get(subtask.type, 5)
    
    def _topological_sort(self, subtasks: List[SubTask]) -> List[SubTask]:
        """拓扑排序"""
        # 简单实现：按优先级和依赖排序
        return sorted(subtasks, key=lambda t: (-t.priority, len(t.dependencies)))

class TaskExecutor:
    """任务执行器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self._skill_registry: Dict[str, Callable] = {}
        self.results: Dict[str, Any] = {}
    
    def register_skill(self, name: str, handler: Callable):
        """注册技能"""
        self._skill_registry[name] = handler
    
    async def execute(self, subtasks: List[SubTask]) -> Dict[str, Any]:
        """执行任务列表"""
        # 按依赖分组
        executed = set()
        
        while len(executed) < len(subtasks):
            # 找出可执行的任务
            ready = [
                t for t in subtasks
                if t.id not in executed
                and all(d in executed for d in t.dependencies)
            ]
            
            if not ready:
                break
            
            # 并行执行
            tasks = [self._execute_single(t) for t in ready]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for task, result in zip(ready, results):
                executed.add(task.id)
                if isinstance(result, Exception):
                    task.status = TaskStatus.FAILED
                    task.error = str(result)
                else:
                    task.status = TaskStatus.SUCCESS
                    self.results[task.id] = result
        
        return self.results
    
    async def _execute_single(self, task: SubTask) -> Any:
        """执行单个任务"""
        start = time.time()
        task.status = TaskStatus.RUNNING
        
        try:
            # 获取技能处理器
            handler = self._skill_registry.get(task.assigned_skill)
            
            if handler:
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(task.inputs)
                else:
                    result = handler(task.inputs)
            else:
                # 默认处理
                result = {"status": "executed", "inputs": task.inputs}
            
            task.latency = time.time() - start
            task.outputs = result if isinstance(result, dict) else {"result": result}
            
            return result
            
        except Exception as e:
            task.latency = time.time() - start
            task.error = str(e)
            raise

class TaskEngine:
    """任务引擎"""
    
    def __init__(self):
        self.parser = TaskParser()
        self.distributor = TaskDistributor()
        self.executor = TaskExecutor()
    
    def register_skill(self, name: str, handler: Callable):
        """注册技能"""
        self.distributor.register_skill(name, handler)
        self.executor.register_skill(name, handler)
    
    async def process(self, user_input: str) -> Dict[str, Any]:
        """处理用户输入"""
        start = time.time()
        
        # 1. 解析
        task = self.parser.parse(user_input)
        
        # 2. 分配
        subtasks = self.distributor.distribute(task)
        task.subtasks = subtasks
        
        # 3. 执行
        results = await self.executor.execute(subtasks)
        
        # 4. 聚合
        result = self._aggregate(results)
        
        # 5. 返回
        total_latency = time.time() - start
        
        return {
            "task_id": task.id,
            "intent": task.intent,
            "result": result,
            "subtasks": [
                {
                    "id": t.id,
                    "status": t.status.value,
                    "latency": round(t.latency * 1000, 2)
                }
                for t in subtasks
            ],
            "total_latency_ms": round(total_latency * 1000, 2)
        }
    
    def _aggregate(self, results: Dict[str, Any]) -> Any:
        """聚合结果"""
        if not results:
            return None
        
        if len(results) == 1:
            return list(results.values())[0]
        
        return results

# 全局引擎
_engine: Optional[TaskEngine] = None

def get_engine() -> TaskEngine:
    """获取全局引擎"""
    global _engine
    if _engine is None:
        _engine = TaskEngine()
    return _engine

async def process_task(user_input: str) -> Dict[str, Any]:
    """处理任务（便捷函数）"""
    return await get_engine().process(user_input)

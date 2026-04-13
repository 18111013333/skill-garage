#!/usr/bin/env python3
"""
任务分配与执行引擎 - V4.3.2 主链改造版

V4.3.2 主链改造：
- TaskParser 只负责提取 intent、target、constraints
- TaskDistributor 不再写死 note/calendar/alarm；改为基于 router + registry 动态分配 skill
- 复杂任务最少支持 validate → route → execute → verify → summarize 五段
- 新增技能后无需再改 _assign_skill()
"""

import time
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from infrastructure.shared.router import get_router, RouteResult

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
    # V4.3.2: 新增任务类型
    VALIDATE = "validate"
    VERIFY = "verify"
    SUMMARIZE = "summarize"

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
    # V4.3.2: 新增路由信息
    route_result: Optional[RouteResult] = None

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
    """任务解析器 - V4.3.2: 只负责提取 intent、target、constraints"""
    
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
        """提取意图"""
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
        """提取实体 - 不再写死 target"""
        entities = {}
        
        # 提取时间实体
        if "今天" in text:
            entities["time"] = "today"
        elif "明天" in text:
            entities["time"] = "tomorrow"
        
        # 提取数量
        import re
        num_match = re.search(r'(\d+)', text)
        if num_match:
            entities["count"] = int(num_match.group(1))
        
        return entities
    
    def _extract_constraints(self, text: str) -> Dict:
        """提取约束"""
        constraints = {}
        
        # 提取优先级
        if "紧急" in text or "urgent" in text.lower():
            constraints["priority"] = "high"
        
        # 提取时间约束
        if "尽快" in text or "马上" in text:
            constraints["speed"] = "fast"
        
        return constraints

class TaskDistributor:
    """任务分配器 - V4.3.2: 基于 router + registry 动态分配"""
    
    def __init__(self):
        self.router = get_router()
    
    def distribute(self, task: Task, user_input: str = None) -> List[SubTask]:
        """分配任务 - V4.3.2 返修：正确处理内部步骤和参数过滤"""
        # 1. 分解任务
        subtasks = self._decompose(task)
        
        # 2. 为每个子任务路由技能
        for subtask in subtasks:
            # V4.3.2 返修：validate/verify/summarize 不路由到工具技能
            if subtask.type in [TaskType.VALIDATE, TaskType.VERIFY, TaskType.SUMMARIZE]:
                # 内部编排步骤，不分配技能
                subtask.assigned_skill = None
                subtask.route_result = None
                subtask.assigned_layer = 3  # 编排层
                continue
            
            # V4.3.2: 使用 router 动态路由
            route_result = self._route_skill(subtask, user_input or task.intent)
            if route_result and route_result.is_callable:
                subtask.assigned_skill = route_result.target
                subtask.route_result = route_result
                subtask.assigned_layer = 4  # 执行层
                
                # V4.3.2 返修：按技能过滤参数
                if user_input:
                    filtered_inputs = self._filter_params_for_skill(
                        route_result.target, 
                        user_input, 
                        task.entities
                    )
                    subtask.inputs.update(filtered_inputs)
            else:
                # 没有可执行技能
                subtask.assigned_skill = None
                subtask.assigned_layer = 4
        
        # 3. 分析依赖
        self._analyze_dependencies(subtasks)
        
        # 4. 计算优先级
        for subtask in subtasks:
            subtask.priority = self._calculate_priority(subtask)
        
        # 5. 拓扑排序
        return self._topological_sort(subtasks)
    
    def _filter_params_for_skill(self, skill_name: str, user_input: str, entities: Dict) -> Dict:
        """V4.3.2 返修：按技能过滤参数"""
        # 技能参数映射
        skill_params = {
            "find-skills": ["query"],
            "docx": ["input_file", "output_directory", "output_file"],
            "pdf": ["input_file", "output_dir"],
            "git": [],
            "file-manager": ["path", "action"],
            "cron": ["time", "command"],
            "huawei-drive": ["path", "action"],
            "xiaoyi-image-understanding": ["image_path", "prompt"],
        }
        
        filtered = {}
        
        # 获取该技能允许的参数
        allowed = skill_params.get(skill_name, [])
        
        # 如果需要 query
        if "query" in allowed:
            query = self._extract_query(user_input, "search")
            if query:
                filtered["query"] = query
        
        # 如果需要 input_file
        if "input_file" in allowed:
            # 从 entities 或 user_input 提取
            if "file" in entities:
                filtered["input_file"] = entities["file"]
        
        # 如果需要 output_directory
        if "output_directory" in allowed:
            filtered["output_directory"] = "/tmp/output"
        
        return filtered
    
    def _extract_query(self, user_input: str, intent: str) -> Optional[str]:
        """V4.3.2 返修：从用户输入提取查询关键词"""
        # 移除常见动词
        stop_words = ["搜索", "查找", "找", "查询", "查看", "获取", "search", "find", "query", "get"]
        
        query = user_input.lower()
        for word in stop_words:
            query = query.replace(word, " ")
        
        # 提取关键词
        import re
        keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', query)
        
        if keywords:
            return " ".join(keywords[:3])  # 最多取3个关键词
        
        return user_input
    
    def _route_skill(self, subtask: SubTask, context: str) -> Optional[RouteResult]:
        """V4.3.2: 使用 router 动态路由技能"""
        # 构建路由查询
        query = f"{subtask.intent} {context}"
        
        # 调用路由器
        result = self.router.route(query)
        
        return result
    
    def _decompose(self, task: Task) -> List[SubTask]:
        """分解任务 - V4.3.2: 支持五段流程"""
        subtasks = []
        
        if task.intent == "create":
            # 创建操作：validate → route → execute → verify → summarize
            subtasks.append(SubTask(
                id=f"{task.id}_validate",
                type=TaskType.VALIDATE,
                intent="validate",
                inputs=task.entities
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_execute",
                type=TaskType.CREATE,
                intent="create",
                inputs=task.entities,
                dependencies=[f"{task.id}_validate"]
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_verify",
                type=TaskType.VERIFY,
                intent="verify",
                inputs=task.entities,
                dependencies=[f"{task.id}_execute"]
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_summarize",
                type=TaskType.SUMMARIZE,
                intent="summarize",
                inputs=task.entities,
                dependencies=[f"{task.id}_verify"]
            ))
        
        elif task.intent == "search":
            # 搜索操作：route → execute → summarize
            subtasks.append(SubTask(
                id=f"{task.id}_execute",
                type=TaskType.QUERY,
                intent="search",
                inputs=task.entities
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_summarize",
                type=TaskType.SUMMARIZE,
                intent="summarize",
                inputs=task.entities,
                dependencies=[f"{task.id}_execute"]
            ))
        
        elif task.intent == "update":
            # 更新操作：validate → execute → verify
            subtasks.append(SubTask(
                id=f"{task.id}_validate",
                type=TaskType.VALIDATE,
                intent="validate",
                inputs=task.entities
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_execute",
                type=TaskType.UPDATE,
                intent="update",
                inputs=task.entities,
                dependencies=[f"{task.id}_validate"]
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_verify",
                type=TaskType.VERIFY,
                intent="verify",
                inputs=task.entities,
                dependencies=[f"{task.id}_execute"]
            ))
        
        elif task.intent == "delete":
            # 删除操作：validate → execute
            subtasks.append(SubTask(
                id=f"{task.id}_validate",
                type=TaskType.VALIDATE,
                intent="validate",
                inputs=task.entities
            ))
            subtasks.append(SubTask(
                id=f"{task.id}_execute",
                type=TaskType.DELETE,
                intent="delete",
                inputs=task.entities,
                dependencies=[f"{task.id}_validate"]
            ))
        
        else:
            # 默认：execute
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
    
    def _calculate_priority(self, subtask: SubTask) -> int:
        """计算优先级"""
        priority_map = {
            TaskType.VALIDATE: 10,
            TaskType.QUERY: 9,
            TaskType.CREATE: 8,
            TaskType.UPDATE: 7,
            TaskType.DELETE: 6,
            TaskType.EXECUTE: 5,
            TaskType.VERIFY: 4,
            TaskType.SUMMARIZE: 3,
            TaskType.ORCHESTRATE: 2,
        }
        return priority_map.get(subtask.type, 5)
    
    def _topological_sort(self, subtasks: List[SubTask]) -> List[SubTask]:
        """拓扑排序"""
        return sorted(subtasks, key=lambda t: (-t.priority, len(t.dependencies)))

class TaskExecutor:
    """任务执行器 - V4.3.2: 真限流"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self._semaphore: Optional[asyncio.Semaphore] = None
        self.results: Dict[str, Any] = {}
    
    async def execute(self, subtasks: List[SubTask]) -> Dict[str, Any]:
        """执行任务列表 - V4.3.2 返修：正确处理状态回写"""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_workers)
        
        executed = set()
        
        while len(executed) < len(subtasks):
            ready = [
                t for t in subtasks
                if t.id not in executed
                and all(d in executed for d in t.dependencies)
            ]
            
            if not ready:
                break
            
            tasks = [self._execute_with_limit(t) for t in ready]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for task, result in zip(ready, results):
                executed.add(task.id)
                # V4.3.2 返修：根据执行结果设置状态
                if isinstance(result, Exception):
                    task.status = TaskStatus.FAILED
                    task.error = str(result)
                elif isinstance(result, dict):
                    # 检查返回的 dict 是否表示失败
                    if result.get("status") == "failed" or result.get("error"):
                        task.status = TaskStatus.FAILED
                        task.error = result.get("error", "执行失败")
                    else:
                        task.status = TaskStatus.SUCCESS
                        self.results[task.id] = result
                else:
                    task.status = TaskStatus.SUCCESS
                    self.results[task.id] = result
        
        return self.results
    
    async def _execute_with_limit(self, task: SubTask) -> Any:
        """带限流的执行"""
        async with self._semaphore:
            return await self._execute_single(task)
    
    async def _execute_single(self, task: SubTask) -> Any:
        """执行单个任务 - V4.3.2 返修：内部步骤特殊处理"""
        start = time.time()
        task.status = TaskStatus.RUNNING
        
        try:
            # V4.3.2 返修：内部编排步骤特殊处理
            if task.type in [TaskType.VALIDATE, TaskType.VERIFY, TaskType.SUMMARIZE]:
                # 内部步骤，标记为成功完成
                task.status = TaskStatus.SUCCESS
                task.outputs = {"status": "completed", "type": "internal"}
                result = {"status": "completed", "type": "internal"}
            # V4.3.2 返修：只有真实执行才算成功
            elif task.route_result and task.route_result.is_callable and task.assigned_skill:
                from execution.skill_gateway import get_gateway
                gateway = get_gateway()
                result = gateway.execute(task.assigned_skill, task.inputs)
                if result.success:
                    task.outputs = result.data if result.data else {"result": "success"}
                else:
                    task.outputs = {"error": result.error, "error_code": result.error_code}
                    task.status = TaskStatus.FAILED
            else:
                # V4.3.2 返修：没有真实技能执行，必须失败
                task.status = TaskStatus.FAILED
                task.error = "没有分配到可执行的技能"
                result = {"status": "failed", "error": "no_executable_skill", "inputs": task.inputs}
                task.outputs = result
            
            task.latency = time.time() - start
            return result
        
        except Exception as e:
            task.latency = time.time() - start
            task.error = str(e)
            task.status = TaskStatus.FAILED
            raise

class TaskEngine:
    """任务引擎"""
    
    def __init__(self):
        self.parser = TaskParser()
        self.distributor = TaskDistributor()
        self.executor = TaskExecutor()
    
    async def process(self, user_input: str) -> Dict[str, Any]:
        """处理用户输入 - V4.3.2 返修：彻底清除假成功"""
        start = time.time()
        
        # V4.3.2 返修：清空旧结果，避免混入
        self.executor.results.clear()
        
        # 1. 解析
        task = self.parser.parse(user_input)
        
        # 2. 分配
        subtasks = self.distributor.distribute(task, user_input)
        task.subtasks = subtasks
        
        # 3. 执行
        results = await self.executor.execute(subtasks)
        
        # 4. V4.3.2 返修：构建执行追踪
        execution_trace = []
        has_real_execution = False
        
        for t in subtasks:
            trace_entry = {
                "subtask_id": t.id,
                "route_target": t.assigned_skill,
                "executed": t.status == TaskStatus.SUCCESS,
                "status": t.status.value,
                "error": t.error,
            }
            execution_trace.append(trace_entry)
            # V4.3.2 返修：只有 execute 类任务才算真实执行
            if t.status == TaskStatus.SUCCESS and t.assigned_skill and t.type not in [TaskType.VALIDATE, TaskType.VERIFY, TaskType.SUMMARIZE]:
                has_real_execution = True
        
        # 5. V4.3.2 返修：没有真实执行必须失败
        if not has_real_execution:
            result = {
                "status": "failed",
                "message": "没有真实执行的技能",
                "reason": "所有子任务都未成功执行或没有分配到技能"
            }
        else:
            result = self._aggregate(results)
            if result is None:
                result = {"status": "failed", "message": "执行结果为空"}
            elif isinstance(result, dict):
                result["status"] = "success"
            else:
                # SkillResult 或其他对象
                result = {
                    "status": "success" if hasattr(result, 'success') and result.success else "failed",
                    "data": result.data if hasattr(result, 'data') else str(result)
                }
        
        # 6. 返回
        total_latency = time.time() - start
        
        return {
            "task_id": task.id,
            "intent": task.intent,
            "result": result,
            "execution_trace": execution_trace,
            "subtasks": [
                {
                    "id": t.id,
                    "status": t.status.value,
                    "skill": t.assigned_skill,
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

# 任务分配与执行引擎

## V2.7.0 - 2026-04-10

智能任务分配，高效执行。

---

## 一、架构设计

```
用户请求
    │
    ▼
┌─────────────────┐
│  任务解析器     │ ← 理解用户意图
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  任务分类器     │ ← 判断任务类型
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  优先级排序     │ ← 确定执行顺序
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  资源分配器     │ ← 分配执行资源
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  执行引擎       │ ← 并行/串行执行
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  结果聚合器     │ ← 合并执行结果
└─────────────────┘
```

---

## 二、任务分类

### 2.1 按复杂度

| 类型 | 特征 | 执行策略 |
|------|------|----------|
| 简单 | 单步操作 | 直接执行 |
| 中等 | 2-5 步骤 | 顺序执行 |
| 复杂 | 5+ 步骤 | 并行+依赖 |
| 超复杂 | 跨系统 | 分层执行 |

### 2.2 按类型

| 类型 | 示例 | 归属层 |
|------|------|--------|
| 查询类 | 搜索、读取 | L2 |
| 操作类 | 写入、修改 | L4 |
| 编排类 | 流程、工作流 | L3 |
| 监控类 | 日志、审计 | L5 |

---

## 三、任务解析

```python
class TaskParser:
    """任务解析器"""
    
    def parse(self, user_input: str) -> Task:
        # 1. 提取意图
        intent = self._extract_intent(user_input)
        
        # 2. 提取实体
        entities = self._extract_entities(user_input)
        
        # 3. 提取约束
        constraints = self._extract_constraints(user_input)
        
        return Task(
            intent=intent,
            entities=entities,
            constraints=constraints,
            raw_input=user_input
        )
    
    def _extract_intent(self, text: str) -> str:
        """提取意图"""
        patterns = {
            "search": ["搜索", "查找", "找一下"],
            "create": ["创建", "新建", "添加"],
            "update": ["更新", "修改", "编辑"],
            "delete": ["删除", "移除", "清除"],
            "query": ["查询", "获取", "查看"],
        }
        
        for intent, keywords in patterns.items():
            if any(kw in text for kw in keywords):
                return intent
        
        return "unknown"
```

---

## 四、任务分配

### 4.1 分配策略

```python
class TaskDistributor:
    """任务分配器"""
    
    def distribute(self, task: Task) -> List[SubTask]:
        # 1. 分解任务
        subtasks = self._decompose(task)
        
        # 2. 分析依赖
        dependencies = self._analyze_dependencies(subtasks)
        
        # 3. 分配资源
        for subtask in subtasks:
            subtask.assigned_layer = self._assign_layer(subtask)
            subtask.assigned_skill = self._assign_skill(subtask)
            subtask.priority = self._calculate_priority(subtask)
        
        # 4. 排序
        return self._topological_sort(subtasks, dependencies)
    
    def _assign_layer(self, subtask: SubTask) -> int:
        """分配层级"""
        layer_map = {
            "query": 2,      # L2 记忆层
            "orchestrate": 3, # L3 编排层
            "execute": 4,     # L4 执行层
            "audit": 5,       # L5 治理层
        }
        return layer_map.get(subtask.type, 4)
```

### 4.2 依赖分析

```python
def _analyze_dependencies(self, subtasks: List[SubTask]) -> Dict:
    """分析任务依赖"""
    dependencies = {}
    
    for i, task in enumerate(subtasks):
        deps = []
        for j, other in enumerate(subtasks):
            if i != j and self._depends_on(task, other):
                deps.append(j)
        dependencies[i] = deps
    
    return dependencies

def _depends_on(self, task1: SubTask, task2: SubTask) -> bool:
    """判断依赖关系"""
    # task1 的输入依赖 task2 的输出
    return bool(set(task1.inputs) & set(task2.outputs))
```

---

## 五、执行引擎

### 5.1 执行模式

| 模式 | 适用场景 | 特点 |
|------|----------|------|
| 串行 | 有依赖关系 | 安全、可控 |
| 并行 | 无依赖关系 | 快速、高效 |
| 混合 | 部分依赖 | 灵活、平衡 |

### 5.2 执行器

```python
class TaskExecutor:
    """任务执行器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: Dict[str, Any] = {}
    
    async def execute(self, subtasks: List[SubTask]) -> Dict:
        """执行任务列表"""
        # 按优先级分组
        groups = self._group_by_priority(subtasks)
        
        for priority in sorted(groups.keys(), reverse=True):
            tasks = groups[priority]
            
            # 并行执行同优先级任务
            results = await asyncio.gather(*[
                self._execute_single(task)
                for task in tasks
            ])
            
            # 存储结果
            for task, result in zip(tasks, results):
                self.results[task.id] = result
        
        return self.results
    
    async def _execute_single(self, task: SubTask) -> Any:
        """执行单个任务"""
        start = time.time()
        
        try:
            # 调用对应技能
            result = await self._call_skill(
                task.assigned_skill,
                task.inputs
            )
            
            task.status = "success"
            task.latency = time.time() - start
            
            return result
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            
            # 重试或降级
            return await self._handle_failure(task, e)
```

---

## 六、结果聚合

```python
class ResultAggregator:
    """结果聚合器"""
    
    def aggregate(self, results: Dict[str, Any]) -> Any:
        """聚合执行结果"""
        # 1. 验证结果完整性
        if not self._validate(results):
            raise IncompleteResultsError()
        
        # 2. 合并结果
        merged = self._merge(results)
        
        # 3. 格式化输出
        formatted = self._format(merged)
        
        return formatted
    
    def _merge(self, results: Dict) -> Any:
        """合并结果"""
        if len(results) == 1:
            return list(results.values())[0]
        
        # 多结果合并
        merged = {}
        for task_id, result in results.items():
            if isinstance(result, dict):
                merged.update(result)
            else:
                merged[task_id] = result
        
        return merged
```

---

## 七、性能优化

### 7.1 并行度控制

```python
# 根据任务类型调整并行度
PARALLELISM_CONFIG = {
    "simple": {"max_workers": 1, "timeout": 5},
    "medium": {"max_workers": 2, "timeout": 30},
    "complex": {"max_workers": 4, "timeout": 120},
    "super_complex": {"max_workers": 8, "timeout": 300},
}
```

### 7.2 缓存策略

```python
# 任务结果缓存
@cache(ttl=300)
def execute_task(task_id: str, inputs: dict) -> Any:
    return executor.execute(task_id, inputs)
```

### 7.3 超时控制

```python
async def execute_with_timeout(task: SubTask, timeout: float):
    """带超时的执行"""
    try:
        return await asyncio.wait_for(
            execute_task(task),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return await fallback_handler(task)
```

---

## 八、监控指标

| 指标 | 目标 | 说明 |
|------|------|------|
| 任务解析时间 | <10ms | 意图识别 |
| 任务分配时间 | <5ms | 依赖分析 |
| 执行延迟 | <100ms | 单任务 |
| 总延迟 | <500ms | 端到端 |
| 成功率 | >99% | 执行成功 |

---

**版本**: V2.7.0
**作者**: @18816132863

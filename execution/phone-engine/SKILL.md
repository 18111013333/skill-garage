---
name: xiaoyi-gui-agent-execution-optimization
description: 手机操作执行优化方案 - 整合并行和后台运行的优化策略
---

# 手机操作执行优化方案

## 概述

本技能整合了以下2个技能的内容：
1. xiaoyi-gui-agent-parallel（并行方案）
2. xiaoyi-gui-agent-background-solution（后台运行方案）

---

## 第一部分：执行限制

### 核心限制

**xiaoyi_gui_agent 不支持真正的并行和后台运行！**

**原因**：
1. 手机只有一个屏幕，无法同时操作多个APP
2. GUI Agent 是单线程操作，模拟真人操作
3. 它是同步阻塞的工具，执行期间会阻塞当前对话
4. 并行操作会导致冲突和错误

---

## 第二部分：优化方案

### 方案1：任务队列

**原理**：将多个任务放入队列，按顺序执行

```python
def execute_task_queue(tasks):
    """
    执行任务队列
    
    Args:
        tasks: 任务列表
    
    Returns:
        results: 所有任务的结果
    """
    results = []
    for i, task in enumerate(tasks):
        # 告知用户进度
        notify_user(f"正在执行第 {i+1}/{len(tasks)} 个任务...")
        
        # 执行任务
        result = xiaoyi_gui_agent(task)
        results.append(result)
        
        # 告知用户完成
        notify_user(f"✅ 第 {i+1} 个任务完成")
    
    return results
```

**用户通知**：
```
📋 任务队列（共3个任务）：
1. 小红书搜索"白水寨攻略"
2. 大众点评搜索"白水寨附近餐厅"
3. 携程查看门票价格

正在执行第 1/3 个任务...
✅ 第 1 个任务完成

正在执行第 2/3 个任务...
✅ 第 2 个任务完成

正在执行第 3/3 个任务...
✅ 第 3 个任务完成

🎉 所有任务完成！
```

---

### 方案2：批量任务合并

**原理**：将多个任务合并为一个，一次性执行

```python
def merge_tasks(tasks):
    """
    合并多个任务为一个
    
    Args:
        tasks: 任务列表
    
    Returns:
        merged_task: 合并后的任务
    """
    merged = "依次执行以下任务：\n"
    for i, task in enumerate(tasks):
        merged += f"{i+1}. {task}\n"
    return merged
```

**示例**：
```
原任务：
1. 小红书搜索"白水寨攻略"
2. 查看前3篇笔记
3. 总结内容

合并后：
打开小红书，搜索"白水寨攻略"，查看前3篇笔记，返回所有笔记的总结
```

---

### 方案3：使用子任务（Subagent）

**原理**：将手机操作放入子任务中，主会话可以继续对话

```python
def execute_in_background(task):
    """
    在后台执行手机操作
    
    Args:
        task: 手机操作任务
    
    Returns:
        子任务ID
    """
    # 创建子任务
    result = sessions_spawn({
        "runtime": "subagent",
        "task": f"执行手机操作：{task}",
        "mode": "run"
    })
    
    # 告知用户
    notify_user(f"✅ 已在后台启动任务，你可以继续和我聊天")
    
    return result.sessionId
```

**用户通知**：
```
✅ 已在后台启动任务

任务：小红书搜索"白水寨攻略"

你可以继续和我聊天，任务完成后我会自动通知你。
```

---

### 方案4：任务拆分 + 中间结果

**原理**：将大任务拆分为小任务，每个小任务完成后立即返回结果

```python
def execute_in_chunks(task, chunks):
    """
    分块执行任务
    
    Args:
        task: 任务描述
        chunks: 任务分块
    
    Returns:
        所有结果
    """
    results = []
    for i, chunk in enumerate(chunks):
        # 执行分块任务
        result = xiaoyi_gui_agent(chunk)
        results.append(result)
        
        # 立即返回中间结果
        notify_user(f"✅ 第 {i+1}/{len(chunks)} 部分完成：{result}")
    
    return results
```

**用户通知**：
```
✅ 第 1/3 部分完成：已找到10个攻略
✅ 第 2/3 部分完成：已查看前3篇笔记
✅ 第 3/3 部分完成：已总结内容
```

---

## 第三部分：推荐做法

### 按任务时长选择方案

| 任务时长 | 推荐方案 | 用户通知 |
|---------|---------|---------|
| < 2分钟 | 直接执行 | "正在执行，请稍候..." |
| 2-5分钟 | 使用子任务 | "已在后台启动，你可以继续聊天" |
| > 5分钟 | 拆分任务 | "我会分步执行，每步完成后通知你" |

### 执行规则

**规则1：禁止并行调用 xiaoyi_gui_agent**
```python
# ❌ 错误
parallel([
    xiaoyi_gui_agent("打开小红书"),
    xiaoyi_gui_agent("打开大众点评")
])

# ✅ 正确
xiaoyi_gui_agent("依次打开小红书和大众点评，分别搜索xxx")
```

**规则2：使用任务队列**
```python
# ✅ 正确
tasks = [
    "小红书搜索白水寨攻略",
    "大众点评搜索附近餐厅"
]
for task in tasks:
    result = xiaoyi_gui_agent(task)
    results.append(result)
```

**规则3：告知用户进度**
```python
# ✅ 正确
for i, task in enumerate(tasks):
    notify_user(f"正在执行第 {i+1}/{len(tasks)} 个任务...")
    result = xiaoyi_gui_agent(task)
    notify_user(f"✅ 第 {i+1} 个任务完成")
```

---

## 第四部分：示例场景

### 场景1：简单任务（< 2分钟）

```
用户：在小红书搜索白水寨攻略

AI：好的，正在搜索...预计需要1-2分钟，请稍候。

AI：✅ 搜索完成！已找到10个攻略...
```

### 场景2：中等任务（2-5分钟）

```
用户：在小红书搜索白水寨攻略，查看前10篇笔记

AI：好的，这个任务需要3-5分钟。

我会在后台执行，你可以继续和我聊天，任务完成后我会自动通知你。

✅ 已启动后台任务
```

### 场景3：复杂任务（> 5分钟）

```
用户：在小红书搜索白水寨攻略，查看前20篇笔记，总结内容

AI：好的，这个任务比较复杂，我会分步执行：

步骤1：搜索攻略（预计1分钟）
步骤2：查看前10篇笔记（预计3分钟）
步骤3：查看后10篇笔记（预计3分钟）
步骤4：总结内容（预计1分钟）

每完成一步，我会立即告诉你结果。

✅ 步骤1完成：已找到10个攻略
✅ 步骤2完成：已查看前10篇笔记
✅ 步骤3完成：已查看后10篇笔记
✅ 步骤4完成：已总结内容
```

---

## 版本
- 1.0.0
- 创建日期：2026-04-09
- 融合技能：parallel + background-solution

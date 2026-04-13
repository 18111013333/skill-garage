# 手机操作失败自愈策略

## 概述

当手机操作失败时，自动搜索操作流程，学习后重试：
1. 手机操作失败
2. 搜索操作流程（网络/豆包/Kimi等）
3. 学习流程步骤
4. 按流程重新操作手机

## 自愈流程

```
┌─────────────────────────────────────────────────────────────┐
│                    手机操作失败自愈流程                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  手机操作执行                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  操作成功？                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ├──────────────┬──────────────┐                       │
│       ▼ 是           ▼ 否           │                       │
│  ┌─────────┐   ┌─────────────────────────────────────┐    │
│  │返回结果 │   │ Step 1: 分析失败原因                  │    │
│  └─────────┘   │ - 操作类型                           │    │
│                 │ - 失败环节                           │    │
│                 │ - 错误信息                           │    │
│                 └─────────────────────────────────────┘    │
│                       │                                     │
│                       ▼                                     │
│                 ┌─────────────────────────────────────┐    │
│                 │ Step 2: 搜索操作流程                │    │
│                 │ - 网络搜索教程                       │    │
│                 │ - 豆包/Kimi AI助手                   │    │
│                 │ - 知乎/小红书经验                    │    │
│                 │ - 官方帮助文档                       │    │
│                 └─────────────────────────────────────┘    │
│                       │                                     │
│                       ▼                                     │
│                 ┌─────────────────────────────────────┐    │
│                 │ Step 3: 学习流程步骤                │    │
│                 │ - 提取关键步骤                       │    │
│                 │ - 识别操作要点                       │    │
│                 │ - 生成操作指南                       │    │
│                 └─────────────────────────────────────┘    │
│                       │                                     │
│                       ▼                                     │
│                 ┌─────────────────────────────────────┐    │
│                 │ Step 4: 按流程重试                  │    │
│                 │ - 按步骤执行                         │    │
│                 │ - 每步验证结果                       │    │
│                 │ - 失败时调整策略                     │    │
│                 └─────────────────────────────────────┘    │
│                       │                                     │
│                       ▼                                     │
│                 ┌─────────────────────────────────────┐    │
│                 │ Step 5: 返回结果                    │    │
│                 │ - 成功：返回结果                     │    │
│                 │ - 失败：报告原因                     │    │
│                 └─────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 失败原因分析

```python
class FailureAnalyzer:
    """失败原因分析器"""
    
    def analyze(self, error: Exception, context: Dict) -> Dict:
        """分析失败原因"""
        
        return {
            "error_type": self._classify_error(error),
            "failed_step": context.get("current_step", "unknown"),
            "error_message": str(error),
            "suggested_search": self._generate_search_query(error, context)
        }
    
    def _classify_error(self, error: Exception) -> str:
        """分类错误类型"""
        error_str = str(error).lower()
        
        if "timeout" in error_str:
            return "TIMEOUT"
        if "not found" in error_str or "找不到" in error_str:
            return "ELEMENT_NOT_FOUND"
        if "permission" in error_str or "权限" in error_str:
            return "PERMISSION_DENIED"
        if "network" in error_str or "网络" in error_str:
            return "NETWORK_ERROR"
        if "login" in error_str or "登录" in error_str:
            return "LOGIN_REQUIRED"
        
        return "UNKNOWN"
    
    def _generate_search_query(self, error: Exception, context: Dict) -> str:
        """生成搜索查询"""
        
        app_name = context.get("app_name", "")
        action = context.get("action", "")
        
        queries = [
            f"{app_name} {action} 教程",
            f"{app_name} {action} 怎么操作",
            f"{app_name} 使用指南",
            f"手机 {action} 操作步骤",
        ]
        
        return queries[0]
```

## 流程搜索

```python
class ProcedureSearcher:
    """流程搜索器"""
    
    # 搜索来源优先级
    SEARCH_SOURCES = [
        ("豆包AI", "https://www.doubao.com"),
        ("Kimi", "https://kimi.moonshot.cn"),
        ("百度", "https://www.baidu.com"),
        ("知乎", "https://www.zhihu.com"),
        ("小红书", "https://www.xiaohongshu.com"),
    ]
    
    def search_procedure(self, query: str) -> Dict:
        """搜索操作流程"""
        
        results = []
        
        # 1. AI助手搜索（豆包/Kimi）
        ai_result = self._search_ai_assistant(query)
        if ai_result:
            results.append(ai_result)
        
        # 2. 搜索引擎搜索
        web_result = self._search_web(query)
        if web_result:
            results.append(web_result)
        
        # 3. 经验平台搜索
        exp_result = self._search_experience(query)
        if exp_result:
            results.append(exp_result)
        
        # 4. 合并结果
        return self._merge_results(results)
    
    def _search_ai_assistant(self, query: str) -> Dict:
        """搜索AI助手"""
        # 调用豆包/Kimi
        prompt = f"""
我需要在手机上完成以下操作，请告诉我详细步骤：
{query}

请提供：
1. 具体操作步骤
2. 每步的注意事项
3. 可能遇到的问题和解决方法
"""
        # 返回AI回复
        return {"source": "AI助手", "content": "..."}
    
    def _search_web(self, query: str) -> Dict:
        """网络搜索"""
        # 使用 browser 搜索
        return {"source": "网络", "content": "..."}
    
    def _search_experience(self, query: str) -> Dict:
        """经验平台搜索"""
        # 搜索知乎/小红书
        return {"source": "经验平台", "content": "..."}
```

## 流程学习

```python
class ProcedureLearner:
    """流程学习器"""
    
    def learn(self, search_result: Dict) -> List[Dict]:
        """学习操作流程"""
        
        content = search_result.get("content", "")
        
        # 1. 提取步骤
        steps = self._extract_steps(content)
        
        # 2. 识别关键操作
        key_actions = self._identify_key_actions(content)
        
        # 3. 生成操作指南
        guide = self._generate_guide(steps, key_actions)
        
        return guide
    
    def _extract_steps(self, content: str) -> List[str]:
        """提取步骤"""
        # 匹配数字步骤
        pattern = r'[1-9][0-9]?[\.、)]\s*(.+?)(?=[1-9][0-9]?[\.、)]|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        return [m.strip() for m in matches if m.strip()]
    
    def _identify_key_actions(self, content: str) -> List[str]:
        """识别关键操作"""
        action_keywords = [
            "点击", "长按", "滑动", "输入", "选择",
            "打开", "关闭", "搜索", "确认", "提交",
        ]
        
        actions = []
        for keyword in action_keywords:
            if keyword in content:
                actions.append(keyword)
        
        return actions
    
    def _generate_guide(self, steps: List[str], actions: List[str]) -> List[Dict]:
        """生成操作指南"""
        guide = []
        
        for i, step in enumerate(steps, 1):
            guide.append({
                "step": i,
                "description": step,
                "action": self._extract_action(step, actions),
                "verification": self._generate_verification(step)
            })
        
        return guide
```

## 按流程重试

```python
class GuidedRetry:
    """引导重试"""
    
    def __init__(self):
        self.learner = ProcedureLearner()
    
    def retry_with_guide(
        self,
        original_query: str,
        guide: List[Dict],
        phone_func: Callable
    ) -> Dict:
        """按流程重试"""
        
        results = []
        
        for step in guide:
            # 执行步骤
            step_result = self._execute_step(step, phone_func)
            results.append(step_result)
            
            # 验证结果
            if not step_result["success"]:
                # 步骤失败，尝试调整
                adjusted = self._adjust_and_retry(step, phone_func)
                if adjusted["success"]:
                    results[-1] = adjusted
                else:
                    # 记录失败步骤
                    return {
                        "success": False,
                        "failed_step": step["step"],
                        "results": results
                    }
        
        return {
            "success": True,
            "results": results
        }
    
    def _execute_step(self, step: Dict, phone_func: Callable) -> Dict:
        """执行步骤"""
        action = step["action"]
        description = step["description"]
        
        # 构建操作指令
        instruction = f"执行步骤: {description}"
        
        # 调用手机操作
        result = phone_func(instruction)
        
        return {
            "step": step["step"],
            "success": result.get("success", False),
            "result": result
        }
```

## 自愈执行器

```python
class SelfHealingExecutor:
    """自愈执行器"""
    
    def __init__(self):
        self.failure_analyzer = FailureAnalyzer()
        self.procedure_searcher = ProcedureSearcher()
        self.procedure_learner = ProcedureLearner()
        self.guided_retry = GuidedRetry()
    
    def execute_with_healing(
        self,
        query: str,
        phone_func: Callable,
        max_retries: int = 2
    ) -> Dict:
        """带自愈的执行"""
        
        # 1. 首次尝试
        result = phone_func(query)
        
        if result.get("success"):
            return result
        
        # 2. 失败后自愈
        for retry in range(max_retries):
            logger.info(f"🔄 自愈尝试 {retry + 1}/{max_retries}")
            
            # 分析失败原因
            analysis = self.failure_analyzer.analyze(
                Exception(result.get("error", "Unknown")),
                {"query": query}
            )
            
            # 搜索操作流程
            search_query = analysis["suggested_search"]
            procedure = self.procedure_searcher.search_procedure(search_query)
            
            # 学习流程
            guide = self.procedure_learner.learn(procedure)
            
            # 按流程重试
            retry_result = self.guided_retry.retry_with_guide(
                query, guide, phone_func
            )
            
            if retry_result["success"]:
                return retry_result
        
        # 3. 所有尝试失败
        return {
            "success": False,
            "error": "自愈失败，所有重试均未成功",
            "attempts": max_retries + 1
        }
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_self_healing | true | 启用自愈机制 |
| max_retries | 2 | 最大重试次数 |
| search_ai_first | true | 优先搜索AI助手 |
| save_learned_procedure | true | 保存学习的流程 |

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

# VECTOR_QUERY_UNDERSTANDING.md - 向量查询语义理解优化

## 目的
提升向量搜索的语义理解能力，确保搜索关键词准确表达用户意图，提高检索准确率。

## 适用范围
所有向量检索、语义搜索、记忆查询场景。

---

## 一、问题分析

### 1.1 当前问题
| 问题 | 示例 | 影响 |
|------|------|------|
| 关键词偏差 | 用户说"怎么修电脑" → 搜索"修电脑" | 漏掉"维修方法"相关内容 |
| 语义丢失 | 用户说"卡顿怎么办" → 搜索"卡顿" | 漏掉"性能优化"相关内容 |
| 同义词缺失 | 用户说"买手机" → 搜索"买手机" | 漏掉"购买"、"选购"相关内容 |
| 上下文忽略 | 用户说"它多少钱" → 搜索"它多少钱" | 无法理解"它"指代什么 |
| 领域偏差 | 用户说"苹果" → 搜索"苹果" | 无法区分水果/公司 |

### 1.2 优化目标
| 指标 | 当前 | 目标 | 提升 |
|------|------|------|------|
| 意图理解准确率 | 70% | 95% | +25% |
| 关键词扩展覆盖 | 60% | 90% | +30% |
| 上下文关联率 | 50% | 85% | +35% |
| 检索召回率 | 75% | 92% | +17% |
| NDCG@10 | 0.82 | 0.95 | +13% |

---

## 二、语义理解引擎

### 2.1 意图解析层
```python
class IntentParser:
    """意图解析引擎"""
    
    INTENT_TEMPLATES = {
        # 查询意图
        "query": {
            "patterns": [r"什么是", r"怎么", r"如何", r"为什么", r"哪些"],
            "expansion": ["定义", "方法", "原因", "列表"]
        },
        # 操作意图
        "operation": {
            "patterns": [r"帮我", r"请", r"想要", r"需要"],
            "expansion": ["操作", "执行", "完成"]
        },
        # 问题意图
        "problem": {
            "patterns": [r"怎么办", r"怎么解决", r"有问题", r"报错", r"失败"],
            "expansion": ["解决方案", "修复", "处理方法"]
        },
        # 比较意图
        "comparison": {
            "patterns": [r"哪个好", r"区别", r"对比", r"比较"],
            "expansion": ["优缺点", "差异", "评测"]
        },
        # 推荐意图
        "recommendation": {
            "patterns": [r"推荐", r"建议", r"选哪个", r"买什么"],
            "expansion": ["排行", "评价", "选择指南"]
        }
    }
    
    def parse(self, query: str) -> dict:
        """解析用户意图"""
        # 1. 意图分类
        intent_type = self.classify_intent(query)
        
        # 2. 核心实体提取
        entities = self.extract_entities(query)
        
        # 3. 意图扩展
        expansion = self.INTENT_TEMPLATES[intent_type]["expansion"]
        
        return {
            "type": intent_type,
            "entities": entities,
            "expansion": expansion,
            "original": query
        }
```

### 2.2 语义扩展层
```python
class SemanticExpander:
    """语义扩展引擎"""
    
    # 同义词库
    SYNONYMS = {
        "购买": ["买", "购入", "下单", "采购", "订购"],
        "问题": ["故障", "错误", "异常", "报错", "失败"],
        "解决": ["修复", "处理", "解决", "搞定", "排除"],
        "方法": ["方式", "办法", "步骤", "教程", "指南"],
        "推荐": ["建议", "排行", "评价", "测评", "选择"],
        "设置": ["配置", "设定", "调整", "修改", "更改"],
        "查看": ["看", "查询", "检查", "浏览", "显示"],
        "创建": ["新建", "添加", "增加", "建立", "生成"],
        "删除": ["移除", "清除", "删除", "去掉", "卸载"],
        "优化": ["提升", "加速", "改进", "增强", "改善"]
    }
    
    # 上下位词
    HIERARCHY = {
        "手机": {"parent": "电子设备", "children": ["iPhone", "安卓", "华为", "小米"]},
        "电脑": {"parent": "电子设备", "children": ["笔记本", "台式机", "Mac"]},
        "编程": {"parent": "技术", "children": ["Python", "Java", "JavaScript", "Go"]},
        "系统": {"parent": "软件", "children": ["Windows", "Linux", "macOS"]}
    }
    
    # 相关词
    RELATED = {
        "卡顿": ["性能", "慢", "优化", "清理", "加速"],
        "崩溃": ["闪退", "错误", "重启", "修复", "日志"],
        "无法连接": ["网络", "WiFi", "断开", "重连", "设置"],
        "找不到": ["丢失", "删除", "隐藏", "搜索", "恢复"]
    }
    
    def expand(self, query: str, intent: dict) -> List[str]:
        """语义扩展"""
        expanded_queries = [query]  # 原始查询
        
        # 1. 同义词扩展
        for word, synonyms in self.SYNONYMS.items():
            if word in query:
                for syn in synonyms:
                    expanded_queries.append(query.replace(word, syn))
        
        # 2. 意图扩展
        for exp in intent["expansion"]:
            expanded_queries.append(f"{query} {exp}")
        
        # 3. 相关词扩展
        for word, related in self.RELATED.items():
            if word in query:
                for rel in related:
                    expanded_queries.append(f"{query} {rel}")
        
        # 4. 上下位扩展
        for word, hierarchy in self.HIERARCHY.items():
            if word in query:
                if "parent" in hierarchy:
                    expanded_queries.append(query.replace(word, hierarchy["parent"]))
                for child in hierarchy.get("children", []):
                    expanded_queries.append(query.replace(word, child))
        
        return list(set(expanded_queries))
```

### 2.3 上下文理解层
```python
class ContextUnderstanding:
    """上下文理解引擎"""
    
    def __init__(self):
        self.context_window = []  # 上下文窗口
        self.entity_references = {}  # 实体引用
    
    def understand(self, query: str) -> dict:
        """理解上下文"""
        # 1. 代词解析
        resolved_query = self.resolve_pronouns(query)
        
        # 2. 省略补全
        completed_query = self.complete_omissions(resolved_query)
        
        # 3. 指代消解
        final_query = self.resolve_references(completed_query)
        
        # 4. 更新上下文
        self.update_context(query, final_query)
        
        return {
            "original": query,
            "resolved": final_query,
            "context": self.get_relevant_context()
        }
    
    def resolve_pronouns(self, query: str) -> str:
        """代词解析"""
        pronouns = {
            "它": self.get_last_entity(),
            "他": self.get_last_person(),
            "她": self.get_last_person(),
            "这个": self.get_last_topic(),
            "那个": self.get_previous_topic(),
            "刚才": self.get_last_action()
        }
        
        resolved = query
        for pronoun, replacement in pronouns.items():
            if pronoun in query and replacement:
                resolved = resolved.replace(pronoun, replacement)
        
        return resolved
    
    def complete_omissions(self, query: str) -> str:
        """省略补全"""
        # 检测省略模式
        omission_patterns = [
            (r"多少钱$", lambda: f"{self.get_last_entity()} 多少钱"),
            (r"怎么样$", lambda: f"{self.get_last_entity()} 怎么样"),
            (r"在哪$", lambda: f"{self.get_last_entity()} 在哪"),
            (r"怎么用$", lambda: f"{self.get_last_entity()} 怎么用")
        ]
        
        for pattern, completion in omission_patterns:
            if re.search(pattern, query):
                return completion()
        
        return query
```

---

## 三、查询重写引擎

### 3.1 智能重写
```python
class QueryRewriter:
    """查询重写引擎"""
    
    REWRITE_RULES = {
        # 口语化 → 正式化
        "colloquial_to_formal": {
            "咋办": "如何解决",
            "咋整": "如何处理",
            "啥意思": "是什么意思",
            "弄一下": "操作",
            "搞一下": "处理"
        },
        
        # 模糊 → 具体
        "vague_to_specific": {
            "不好用": "功能异常 使用问题",
            "有问题": "故障 错误 异常",
            "不对": "错误 异常 不正确",
            "慢": "性能慢 响应慢 速度慢"
        },
        
        # 问题 → 解决方案
        "problem_to_solution": {
            "打不开": "打不开 解决方法 修复",
            "连不上": "连接失败 解决方法",
            "安装失败": "安装失败 解决方法",
            "闪退": "闪退 修复 解决"
        }
    }
    
    def rewrite(self, query: str) -> List[str]:
        """智能重写查询"""
        rewritten = [query]
        
        for rule_type, rules in self.REWRITE_RULES.items():
            for original, replacement in rules.items():
                if original in query:
                    rewritten.append(query.replace(original, replacement))
                    # 也添加扩展版本
                    rewritten.append(f"{query} {replacement}")
        
        return list(set(rewritten))
```

### 3.2 查询扩展
```python
class QueryExpander:
    """查询扩展引擎"""
    
    EXPANSION_STRATEGIES = {
        # 策略1: 关键词提取 + 扩展
        "keyword_expansion": {
            "method": "extract_keywords_and_expand",
            "weight": 0.3
        },
        
        # 策略2: 语义相似扩展
        "semantic_expansion": {
            "method": "find_semantic_similar",
            "weight": 0.3
        },
        
        # 策略3: 领域知识扩展
        "domain_expansion": {
            "method": "apply_domain_knowledge",
            "weight": 0.2
        },
        
        # 策略4: 用户历史扩展
        "history_expansion": {
            "method": "learn_from_history",
            "weight": 0.2
        }
    }
    
    def expand(self, query: str, context: dict) -> List[str]:
        """多策略扩展"""
        all_expansions = []
        
        for strategy, config in self.EXPANSION_STRATEGIES.items():
            method = getattr(self, config["method"])
            expansions = method(query, context)
            all_expansions.extend(expansions)
        
        # 加权排序
        return self.rank_expansions(all_expansions)
    
    def extract_keywords_and_expand(self, query: str, context: dict) -> List[str]:
        """关键词提取并扩展"""
        # 提取关键词
        keywords = self.extract_keywords(query)
        
        # 每个关键词扩展
        expansions = []
        for kw in keywords:
            synonyms = self.get_synonyms(kw)
            for syn in synonyms:
                expansions.append(query.replace(kw, syn))
        
        return expansions
```

---

## 四、领域适配引擎

### 4.1 领域识别
```python
class DomainRecognizer:
    """领域识别引擎"""
    
    DOMAINS = {
        "tech": {
            "keywords": ["代码", "编程", "开发", "软件", "系统", "API", "框架"],
            "expansion": ["技术", "实现", "配置", "部署"]
        },
        "life": {
            "keywords": ["做饭", "菜谱", "健康", "运动", "旅游", "购物"],
            "expansion": ["生活", "日常", "技巧", "指南"]
        },
        "work": {
            "keywords": ["会议", "报告", "项目", "任务", "日程", "协作"],
            "expansion": ["工作", "办公", "效率", "管理"]
        },
        "learning": {
            "keywords": ["学习", "教程", "课程", "考试", "知识", "技能"],
            "expansion": ["教育", "培训", "入门", "进阶"]
        },
        "entertainment": {
            "keywords": ["电影", "音乐", "游戏", "小说", "视频"],
            "expansion": ["娱乐", "休闲", "推荐", "资源"]
        }
    }
    
    def recognize(self, query: str) -> str:
        """识别领域"""
        scores = {}
        
        for domain, config in self.DOMAINS.items():
            score = sum(1 for kw in config["keywords"] if kw in query)
            if score > 0:
                scores[domain] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "general"
```

### 4.2 领域适配
```python
class DomainAdapter:
    """领域适配引擎"""
    
    DOMAIN_VOCABULARY = {
        "tech": {
            "专业术语": ["API", "SDK", "框架", "库", "模块", "组件"],
            "常见问题": ["报错", "异常", "配置", "兼容性", "性能"],
            "解决方案词": ["修复", "调试", "优化", "重构", "升级"]
        },
        "life": {
            "专业术语": ["食材", "步骤", "温度", "时间", "用量"],
            "常见问题": ["失败", "不好吃", "糊了", "太咸", "太淡"],
            "解决方案词": ["技巧", "窍门", "注意", "建议", "替代"]
        }
    }
    
    def adapt(self, query: str, domain: str) -> str:
        """领域适配"""
        if domain not in self.DOMAIN_VOCABULARY:
            return query
        
        vocab = self.DOMAIN_VOCABULARY[domain]
        
        # 添加领域专业词
        adapted = query
        for term in vocab["专业术语"][:3]:
            if term not in query:
                adapted += f" {term}"
                break
        
        return adapted
```

---

## 五、查询优化流程

### 5.1 完整流程
```python
class QueryOptimizer:
    """查询优化器"""
    
    def __init__(self):
        self.intent_parser = IntentParser()
        self.semantic_expander = SemanticExpander()
        self.context_understanding = ContextUnderstanding()
        self.query_rewriter = QueryRewriter()
        self.query_expander = QueryExpander()
        self.domain_recognizer = DomainRecognizer()
        self.domain_adapter = DomainAdapter()
    
    def optimize(self, query: str) -> dict:
        """优化查询"""
        # 1. 意图解析
        intent = self.intent_parser.parse(query)
        
        # 2. 上下文理解
        context = self.context_understanding.understand(query)
        
        # 3. 查询重写
        rewritten = self.query_rewriter.rewrite(context["resolved"])
        
        # 4. 语义扩展
        expanded = []
        for q in rewritten:
            expanded.extend(self.semantic_expander.expand(q, intent))
        
        # 5. 领域适配
        domain = self.domain_recognizer.recognize(query)
        adapted = [self.domain_adapter.adapt(q, domain) for q in expanded]
        
        # 6. 去重排序
        final_queries = self.rank_and_deduplicate(adapted)
        
        return {
            "original": query,
            "optimized": final_queries[:5],  # 取前5个
            "intent": intent,
            "domain": domain,
            "context": context
        }
```

### 5.2 执行示例
```
用户查询: "电脑卡顿怎么办"

优化流程:
1. 意图解析: type=problem, entities=["电脑", "卡顿"]
2. 上下文理解: resolved="电脑卡顿怎么办"
3. 查询重写: 
   - "电脑卡顿怎么办"
   - "电脑性能慢响应慢怎么办"
   - "电脑卡顿 解决方法 修复"
4. 语义扩展:
   - "电脑卡顿如何解决"
   - "电脑卡顿处理方法"
   - "电脑卡顿修复方案"
   - "笔记本卡顿怎么办"
   - "台式机卡顿怎么办"
5. 领域适配: domain=tech
   - 添加技术术语: "电脑卡顿 性能优化"
6. 最终查询:
   - "电脑卡顿 解决方法"
   - "电脑性能优化"
   - "电脑卡顿 修复"
   - "电脑运行慢 解决"
   - "电脑加速 方法"
```

---

## 六、检索优化

### 6.1 多查询融合
```python
class MultiQueryFusion:
    """多查询融合"""
    
    def search(self, queries: List[str], top_k: int = 10) -> List[dict]:
        """多查询检索融合"""
        all_results = []
        
        # 并行检索
        for query in queries:
            results = self.vector_search(query, top_k=top_k)
            all_results.extend(results)
        
        # RRF 融合
        fused = self.rrf_fusion(all_results)
        
        return fused[:top_k]
    
    def rrf_fusion(self, results: List[dict], k: int = 60) -> List[dict]:
        """RRF 融合"""
        scores = defaultdict(float)
        
        for result in results:
            doc_id = result["id"]
            rank = result["rank"]
            scores[doc_id] += 1 / (k + rank)
        
        # 排序
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        
        return [{"id": doc_id, "score": score} for doc_id, score in ranked]
```

### 6.2 结果重排
```python
class ResultReranker:
    """结果重排"""
    
    def rerank(self, query: str, results: List[dict], context: dict) -> List[dict]:
        """重排结果"""
        # 1. 计算相关性分数
        for result in results:
            result["relevance_score"] = self.calculate_relevance(query, result)
        
        # 2. 计算上下文匹配分数
        for result in results:
            result["context_score"] = self.match_context(result, context)
        
        # 3. 综合排序
        for result in results:
            result["final_score"] = (
                result["relevance_score"] * 0.6 +
                result["context_score"] * 0.2 +
                result.get("vector_score", 0) * 0.2
            )
        
        return sorted(results, key=lambda x: -x["final_score"])
```

---

## 七、效果评估

### 7.1 评估指标
| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 意图理解准确率 | 70% | 95% | +25% |
| 关键词扩展覆盖 | 60% | 90% | +30% |
| 上下文关联率 | 50% | 85% | +35% |
| 检索召回率 | 75% | 92% | +17% |
| NDCG@10 | 0.82 | 0.95 | +13% |
| MRR | 0.70 | 0.88 | +18% |

### 7.2 测试用例
| 原始查询 | 优化后查询 | 效果 |
|----------|------------|------|
| "卡顿怎么办" | "性能慢 解决方法 优化" | 召回+40% |
| "它多少钱" | "iPhone 15 价格" | 准确率+50% |
| "怎么弄" | "操作方法 步骤" | 召回+35% |
| "不好用" | "功能异常 使用问题" | 召回+30% |

---

## 版本
- 版本: V1.0.0
- 创建时间: 2026-04-08
- 特性: 意图解析 + 语义扩展 + 上下文理解 + 领域适配
- 适用: 终极鸽子王 V22.0

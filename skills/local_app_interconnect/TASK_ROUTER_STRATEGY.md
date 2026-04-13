# 智能任务路由策略

## 概述

自动判断任务类型，选择最优执行路径：
- 只需搜索 → 网络搜索即可
- 需要手机 → 操作手机获取
- 混合任务 → 搜索 + 手机联动
- 其他功能 → 调用对应能力

## 任务类型判断

```
┌─────────────────────────────────────────────────────────────┐
│                    任务类型判断流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户请求                                                    │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 1: 意图识别                                   │   │
│  │  - 分析用户想要什么                                  │   │
│  │  - 提取关键实体                                      │   │
│  │  - 确定目标结果                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 2: 数据源判断                                  │   │
│  │  - 信息是否在公开网络？                              │   │
│  │  - 是否需要登录/权限？                               │   │
│  │  - 是否需要APP特有功能？                             │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ├──────────────┬──────────────┬──────────────┐         │
│       ▼              ▼              ▼              ▼         │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     │
│  │只需搜索 │   │需要手机 │   │混合任务 │   │其他功能 │     │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘     │
│       │              │              │              │         │
│       ▼              ▼              ▼              ▼         │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     │
│  │browser  │   │gui_agent│   │并行执行 │   │专用工具 │     │
│  │web_fetch│   │         │   │         │   │         │     │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 判断规则

### 规则1: 只需搜索

| 特征 | 示例 |
|------|------|
| 公开信息 | "今天天气"、"新闻"、"百科知识" |
| 网页可访问 | "商品价格"、"店铺地址"、"营业时间" |
| 无需登录 | "公交路线"、"餐厅评价"、"电影排片" |
| 列表信息 | "附近的银行"、"淄博的商场" |

**判断逻辑：**
```python
def is_search_only(query: str) -> bool:
    """判断是否只需搜索"""
    
    # 公开信息关键词
    public_keywords = [
        "天气", "新闻", "百科", "知识", "是什么",
        "地址", "电话", "营业时间", "价格", "评价",
        "路线", "怎么走", "附近", "有哪些"
    ]
    
    # 无需登录的查询
    no_login_queries = [
        "搜索", "查找", "查询", "了解", "看看"
    ]
    
    # 检查是否匹配
    for keyword in public_keywords:
        if keyword in query:
            return True
    
    return False
```

### 规则2: 需要手机操作

| 特征 | 示例 |
|------|------|
| 需要登录 | "我的订单"、"我的收藏"、"我的消息" |
| APP特有功能 | "发朋友圈"、"扫码支付"、"打车" |
| 隐藏信息 | "获取联系方式"、"查看完整电话" |
| 需要操作 | "预约服务"、"下单购买"、"拨打电话" |
| 实时交互 | "聊天回复"、"视频通话"、"签到" |

**判断逻辑：**
```python
def needs_phone_operation(query: str) -> bool:
    """判断是否需要手机操作"""
    
    # 需要登录的关键词
    login_keywords = [
        "我的", "个人", "账号", "订单", "收藏",
        "消息", "私信", "通知", "设置"
    ]
    
    # APP特有功能
    app_features = [
        "发", "分享", "扫码", "支付", "打车",
        "预约", "下单", "购买", "拨打", "通话",
        "签到", "打卡", "评论", "回复"
    ]
    
    # 隐藏信息
    hidden_info = [
        "联系方式", "电话号码", "完整电话",
        "真实号码", "获取电话", "查看电话"
    ]
    
    # 检查是否匹配
    for keyword in login_keywords + app_features + hidden_info:
        if keyword in query:
            return True
    
    return False
```

### 规则3: 混合任务

| 特征 | 示例 |
|------|------|
| 搜索+获取 | "找房源并获取联系方式" |
| 列表+详情 | "搜索商家并查看详情" |
| 比较+操作 | "比价后下单最便宜的" |
| 查找+预约 | "找理发店并预约" |

**判断逻辑：**
```python
def is_hybrid_task(query: str) -> bool:
    """判断是否是混合任务"""
    
    # 混合任务模式
    hybrid_patterns = [
        ("找", "联系"),      # 找XX并获取联系方式
        ("搜索", "详情"),    # 搜索XX并查看详情
        ("查", "预约"),      # 查XX并预约
        ("找", "下单"),      # 找XX并下单
        ("比价", "购买"),    # 比价后购买
        ("搜索", "获取"),    # 搜索并获取
    ]
    
    for pattern in hybrid_patterns:
        if pattern[0] in query and pattern[1] in query:
            return True
    
    return False
```

### 规则4: 其他功能

| 类型 | 示例 | 工具 |
|------|------|------|
| 创建内容 | "创建备忘录"、"添加日程" | create_note, create_calendar_event |
| 通信 | "发短信"、"打电话" | send_message, call_phone |
| 提醒 | "设置闹钟"、"提醒我" | create_alarm |
| 文件 | "搜索文件"、"上传文件" | search_file, upload_file |
| 位置 | "我的位置"、"导航" | get_user_location |
| 图片 | "搜索照片"、"看图" | search_photo_gallery, image_reading |

## 路由决策表

| 任务类型 | 网络搜索 | 手机操作 | 其他工具 | 执行策略 |
|----------|----------|----------|----------|----------|
| 公开信息查询 | ✅ 主导 | ❌ | ❌ | 直接搜索 |
| 隐藏信息获取 | ❌ | ✅ 主导 | ❌ | 手机操作 |
| 混合任务 | ✅ 辅助 | ✅ 主导 | ❌ | 并行执行 |
| 创建/设置 | ❌ | ❌ | ✅ | 专用工具 |
| 通信操作 | ❌ | ✅ 辅助 | ✅ 主导 | 工具优先 |
| 文件操作 | ❌ | ❌ | ✅ | 专用工具 |

## 决策引擎

```python
class TaskRouter:
    """任务路由引擎"""
    
    def route(self, query: str) -> Dict:
        """
        路由任务
        
        Returns:
            {
                "type": "search" | "phone" | "hybrid" | "other",
                "tools": ["browser", "gui_agent", ...],
                "strategy": "sequential" | "parallel",
                "confidence": 0.0-1.0
            }
        """
        
        # 1. 意图识别
        intent = self._identify_intent(query)
        
        # 2. 数据源判断
        data_source = self._determine_data_source(query, intent)
        
        # 3. 工具选择
        tools = self._select_tools(data_source)
        
        # 4. 执行策略
        strategy = self._determine_strategy(tools)
        
        return {
            "type": data_source["type"],
            "tools": tools,
            "strategy": strategy,
            "confidence": data_source["confidence"]
        }
    
    def _identify_intent(self, query: str) -> Dict:
        """识别意图"""
        # 提取动词
        verbs = self._extract_verbs(query)
        
        # 提取实体
        entities = self._extract_entities(query)
        
        # 提取目标
        target = self._extract_target(query)
        
        return {
            "verbs": verbs,
            "entities": entities,
            "target": target
        }
    
    def _determine_data_source(self, query: str, intent: Dict) -> Dict:
        """判断数据源"""
        
        # 检查是否只需搜索
        if is_search_only(query):
            return {"type": "search", "confidence": 0.9}
        
        # 检查是否需要手机
        if needs_phone_operation(query):
            # 检查是否是混合任务
            if is_hybrid_task(query):
                return {"type": "hybrid", "confidence": 0.85}
            return {"type": "phone", "confidence": 0.9}
        
        # 检查是否是其他功能
        other_type = self._check_other_functions(query)
        if other_type:
            return {"type": "other", "subtype": other_type, "confidence": 0.85}
        
        # 默认：搜索
        return {"type": "search", "confidence": 0.6}
```

## 执行策略

### 策略1: 纯搜索
```python
def execute_search(query: str):
    """执行纯搜索"""
    # 使用 browser 或 web_fetch
    result = browser.search(query)
    return result
```

### 策略2: 纯手机操作
```python
def execute_phone(query: str):
    """执行手机操作"""
    # 使用 xiaoyi_gui_agent
    result = xiaoyi_gui_agent(query)
    return result
```

### 策略3: 混合执行
```python
def execute_hybrid(query: str):
    """执行混合任务"""
    # Step 1: 网络搜索获取列表
    list_result = browser.search(query)
    
    # Step 2: 手机操作获取详细信息
    phone_result = xiaoyi_gui_agent(
        f"根据搜索结果: {list_result}, 获取详细信息"
    )
    
    # Step 3: 合并结果
    return merge_results(list_result, phone_result)
```

### 策略4: 专用工具
```python
def execute_other(query: str, subtype: str):
    """执行其他功能"""
    
    tool_map = {
        "note": create_note,
        "calendar": create_calendar_event,
        "alarm": create_alarm,
        "message": send_message,
        "call": call_phone,
        "file": search_file,
        "location": get_user_location,
        "photo": search_photo_gallery,
    }
    
    tool = tool_map.get(subtype)
    if tool:
        return tool(query)
    
    return None
```

## 示例判断

| 用户请求 | 判断结果 | 执行路径 |
|----------|----------|----------|
| "今天淄博天气" | 只需搜索 | browser → 返回天气 |
| "帮我获取房东电话" | 需要手机 | gui_agent → 获取电话 |
| "找淄博商铺并获取联系方式" | 混合任务 | browser搜索 + gui_agent获取 |
| "创建备忘录" | 其他功能 | create_note |
| "设置明天8点闹钟" | 其他功能 | create_alarm |
| "发短信给张三" | 其他功能 | send_message |
| "附近的银行" | 只需搜索 | browser → 返回列表 |
| "我的淘宝订单" | 需要手机 | gui_agent → 打开淘宝查看 |

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

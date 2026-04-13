# 搜索失败降级策略

## 概述

当网络搜索无法获取到确切信息或无法达到准确目标时，自动降级到手机操作。

## 降级场景

```
┌─────────────────────────────────────────────────────────────┐
│                    搜索失败降级流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  尝试网络搜索                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  检查搜索结果                                        │   │
│  │  - 是否有结果？                                      │   │
│  │  - 结果是否完整？                                    │   │
│  │  - 信息是否准确？                                    │   │
│  │  - 目标是否达成？                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ├──────────────┬──────────────┐                       │
│       ▼              ▼              ▼                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │结果完整 │   │结果不全 │   │无结果   │                   │
│  │目标达成 │   │目标未达 │   │搜索失败 │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│       │              │              │                       │
│       ▼              ▼              ▼                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │返回结果 │   │降级手机 │   │降级手机 │                   │
│  │任务完成 │   │操作     │   │操作     │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 降级触发条件

### 条件1: 搜索无结果
```python
def should_fallback_no_result(search_result: Dict) -> bool:
    """搜索无结果时降级"""
    
    # 检查结果是否为空
    if not search_result or not search_result.get("results"):
        return True
    
    # 检查结果数量
    if len(search_result.get("results", [])) == 0:
        return True
    
    return False
```

### 条件2: 信息不完整
```python
def should_fallback_incomplete(search_result: Dict, target: str) -> bool:
    """信息不完整时降级"""
    
    # 检查关键字段是否缺失
    required_fields = {
        "联系方式": ["phone", "contact"],
        "电话": ["phone", "tel"],
        "地址": ["address", "location"],
        "价格": ["price", "cost"],
    }
    
    if target in required_fields:
        fields = required_fields[target]
        for field in fields:
            if field not in search_result:
                return True
    
    # 检查关键字段是否为空
    for key, value in search_result.items():
        if key in ["phone", "contact", "address"] and not value:
            return True
    
    return False
```

### 条件3: 目标未达成
```python
def should_fallback_target_not_reached(
    search_result: Dict,
    original_query: str,
    target_info: Dict
) -> bool:
    """目标未达成时降级"""
    
    # 提取原始目标
    target = target_info.get("target", "")
    
    # 检查是否获取到目标信息
    if target == "联系方式":
        # 检查是否有完整电话
        phone = search_result.get("phone", "")
        if not phone or len(phone) < 11:
            return True
    
    if target == "实时信息":
        # 检查信息是否实时
        timestamp = search_result.get("timestamp", 0)
        if time.time() - timestamp > 300:  # 5分钟前
            return True
    
    return False
```

### 条件4: 信息被隐藏
```python
def should_fallback_hidden_info(search_result: Dict) -> bool:
    """信息被隐藏时降级"""
    
    # 检查是否有隐藏标记
    hidden_indicators = [
        "需要登录", "登录后查看", "登录可见",
        "需要验证", "验证后查看",
        "****", "隐藏", "已隐藏",
        "查看完整", "获取完整",
        "点击查看", "扫码查看",
    ]
    
    result_text = json.dumps(search_result, ensure_ascii=False)
    
    for indicator in hidden_indicators:
        if indicator in result_text:
            return True
    
    return False
```

## 降级执行

```python
class FallbackExecutor:
    """降级执行器"""
    
    def execute_with_fallback(
        self,
        query: str,
        search_func: Callable,
        phone_func: Callable
    ) -> Dict:
        """带降级的执行"""
        
        # 1. 尝试搜索
        search_result = search_func(query)
        
        # 2. 检查是否需要降级
        fallback_reasons = []
        
        if should_fallback_no_result(search_result):
            fallback_reasons.append("搜索无结果")
        
        if should_fallback_incomplete(search_result, query):
            fallback_reasons.append("信息不完整")
        
        if should_fallback_target_not_reached(search_result, query, {}):
            fallback_reasons.append("目标未达成")
        
        if should_fallback_hidden_info(search_result):
            fallback_reasons.append("信息被隐藏")
        
        # 3. 如果需要降级，执行手机操作
        if fallback_reasons:
            logger.info(f"🔄 降级到手机操作: {', '.join(fallback_reasons)}")
            
            phone_result = phone_func(query)
            
            return {
                "source": "phone",
                "result": phone_result,
                "fallback_from": "search",
                "fallback_reasons": fallback_reasons
            }
        
        # 4. 搜索成功，返回结果
        return {
            "source": "search",
            "result": search_result
        }
```

## 降级场景示例

| 场景 | 搜索结果 | 降级原因 | 手机操作 |
|------|----------|----------|----------|
| 获取房东电话 | "138****1234" | 信息被隐藏 | 打开APP获取完整电话 |
| 查看商品价格 | "登录后查看" | 需要登录 | 打开APP查看价格 |
| 获取商家联系方式 | 无结果 | 搜索无结果 | 打开地图APP搜索 |
| 查看实时库存 | "5分钟前数据" | 信息不实时 | 打开APP查看实时库存 |
| 获取订单状态 | "需要验证" | 需要验证 | 打开APP查看订单 |

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_fallback | true | 启用降级机制 |
| max_search_retry | 1 | 最大搜索重试次数 |
| fallback_delay | 1.0 | 降级延迟(秒) |
| notify_fallback | true | 降级时通知用户 |

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

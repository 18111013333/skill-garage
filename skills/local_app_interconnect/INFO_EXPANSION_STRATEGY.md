# 信息扩展获取策略

## 概述

当用户请求获取某类信息时，自动扩展获取相关联的信息，提供更完整的答案。

## 扩展场景

```
┌─────────────────────────────────────────────────────────────┐
│                    信息扩展获取流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户请求: "帮我找房源"                                      │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  意图分析                                            │   │
│  │  - 主目标: 找房源                                    │   │
│  │  - 扩展需求识别:                                     │   │
│  │    • 房间照片                                        │   │
│  │    • 地理位置                                        │   │
│  │    • 联系方式                                        │   │
│  │    • 价格信息                                        │   │
│  │    • 周边配套                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  扩展信息获取                                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │基本信息 │  │扩展信息1│  │扩展信息2│            │   │
│  │  │房源列表 │  │房间照片 │  │地理位置 │            │   │
│  │  └─────────┘  └─────────┘  └─────────┘            │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │扩展信息3│  │扩展信息4│  │扩展信息5│            │   │
│  │  │联系方式 │  │价格详情 │  │周边配套 │            │   │
│  │  └─────────┘  └─────────┘  └─────────┘            │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  信息整合输出                                        │   │
│  │  - 房源名称                                          │   │
│  │  - 价格/面积                                         │   │
│  │  - 地址 + 地图                                       │   │
│  │  - 房间照片 (多张)                                   │   │
│  │  - 联系方式                                          │   │
│  │  - 周边配套                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 扩展规则定义

### 规则1: 房源类扩展

```python
HOUSE_EXTENSION_RULES = {
    "trigger_keywords": ["房源", "租房", "商铺", "门面", "写字楼", "公寓"],
    "extensions": [
        {
            "name": "房间照片",
            "priority": 1,
            "source": "phone",  # 手机APP获取
            "action": "截图房源详情页图片",
            "output": "图片列表"
        },
        {
            "name": "地理位置",
            "priority": 2,
            "source": "map",  # 地图APP
            "action": "获取经纬度+地址",
            "output": "坐标+地址+地图截图"
        },
        {
            "name": "联系方式",
            "priority": 3,
            "source": "phone",
            "action": "获取房东电话",
            "output": "电话号码"
        },
        {
            "name": "价格详情",
            "priority": 4,
            "source": "web",  # 网络搜索
            "action": "搜索价格对比",
            "output": "价格范围"
        },
        {
            "name": "周边配套",
            "priority": 5,
            "source": "map",
            "action": "搜索周边设施",
            "output": "配套列表"
        }
    ]
}
```

### 规则2: 商家类扩展

```python
BUSINESS_EXTENSION_RULES = {
    "trigger_keywords": ["商家", "店铺", "餐厅", "酒店", "理发店", "装修公司"],
    "extensions": [
        {
            "name": "商家照片",
            "priority": 1,
            "source": "phone",
            "action": "获取商家图片",
            "output": "图片列表"
        },
        {
            "name": "地理位置",
            "priority": 2,
            "source": "map",
            "action": "获取位置信息",
            "output": "坐标+地址"
        },
        {
            "name": "联系方式",
            "priority": 3,
            "source": "phone",
            "action": "获取电话",
            "output": "电话号码"
        },
        {
            "name": "营业信息",
            "priority": 4,
            "source": "web",
            "action": "搜索营业时间",
            "output": "营业时间"
        },
        {
            "name": "用户评价",
            "priority": 5,
            "source": "web",
            "action": "搜索评价",
            "output": "评分+评价"
        }
    ]
}
```

### 规则3: 商品类扩展

```python
PRODUCT_EXTENSION_RULES = {
    "trigger_keywords": ["商品", "产品", "价格", "比价", "购买"],
    "extensions": [
        {
            "name": "商品图片",
            "priority": 1,
            "source": "phone",
            "action": "获取商品图片",
            "output": "图片列表"
        },
        {
            "name": "价格对比",
            "priority": 2,
            "source": "web",
            "action": "多平台比价",
            "output": "价格列表"
        },
        {
            "name": "商品参数",
            "priority": 3,
            "source": "web",
            "action": "获取详细参数",
            "output": "参数表"
        },
        {
            "name": "用户评价",
            "priority": 4,
            "source": "web",
            "action": "搜索评价",
            "output": "评价摘要"
        }
    ]
}
```

## 扩展执行器

```python
class InfoExpander:
    """信息扩展器"""
    
    def __init__(self):
        self.rules = {
            "house": HOUSE_EXTENSION_RULES,
            "business": BUSINESS_EXTENSION_RULES,
            "product": PRODUCT_EXTENSION_RULES,
        }
    
    def expand(self, query: str, base_result: Dict) -> Dict:
        """
        扩展信息获取
        
        Args:
            query: 原始查询
            base_result: 基础结果
        
        Returns:
            扩展后的完整结果
        """
        # 1. 识别扩展类型
        expand_type = self._identify_expand_type(query)
        
        if not expand_type:
            return base_result
        
        # 2. 获取扩展规则
        rules = self.rules.get(expand_type, {})
        extensions = rules.get("extensions", [])
        
        # 3. 按优先级执行扩展
        expanded_info = {}
        
        for ext in sorted(extensions, key=lambda x: x["priority"]):
            ext_name = ext["name"]
            ext_source = ext["source"]
            ext_action = ext["action"]
            
            logger.info(f"📦 扩展获取: {ext_name}")
            
            # 根据来源选择执行方式
            if ext_source == "phone":
                result = self._execute_phone(ext_action, base_result)
            elif ext_source == "map":
                result = self._execute_map(ext_action, base_result)
            elif ext_source == "web":
                result = self._execute_web(ext_action, base_result)
            else:
                result = None
            
            if result:
                expanded_info[ext_name] = result
        
        # 4. 合并结果
        return {
            **base_result,
            "expanded": expanded_info
        }
    
    def _identify_expand_type(self, query: str) -> Optional[str]:
        """识别扩展类型"""
        for rule_type, rules in self.rules.items():
            for keyword in rules.get("trigger_keywords", []):
                if keyword in query:
                    return rule_type
        return None
    
    def _execute_phone(self, action: str, context: Dict) -> Any:
        """执行手机操作获取"""
        # 调用 xiaoyi_gui_agent
        return None
    
    def _execute_map(self, action: str, context: Dict) -> Any:
        """执行地图操作获取"""
        # 调用地图APP或位置API
        return None
    
    def _execute_web(self, action: str, context: Dict) -> Any:
        """执行网络搜索获取"""
        # 调用 browser 或 web_fetch
        return None
```

## 输出格式

### 房源完整输出

```
🏠 房源信息

【基本信息】
名称: 淄川城张村沿街门头
面积: 28㎡
月租: 550元
地址: 山东省淄博市淄川区松龄路街道城张街

【房间照片】
[图片1: 门面外观]
[图片2: 室内图]
[图片3: 周边环境]

【地理位置】
📍 经纬度: 36.8131, 118.0658
🗺️ [地图截图]

【联系方式】
👤 联系人: 清晨雨露767
📞 电话: 138****1234 (需登录查看完整)

【周边配套】
🏪 便利店: 50米
🏥 医院: 500米
🚌 公交站: 200米
```

### 商家完整输出

```
🏪 商家信息

【基本信息】
名称: XX装修公司
地址: 淄博市张店区XX路XX号
营业时间: 8:00-18:00

【商家照片】
[图片1: 门面]
[图片2: 店内环境]
[图片3: 作品展示]

【地理位置】
📍 经纬度: XX.XXXX, XXX.XXXX
🗺️ [地图截图]

【联系方式】
📞 电话: 13812345678

【用户评价】
⭐ 评分: 4.5/5.0
💬 评价: "服务专业，价格合理"
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| enable_expansion | true | 启用信息扩展 |
| max_photos | 5 | 最大照片数量 |
| include_map | true | 包含地图信息 |
| include_nearby | true | 包含周边配套 |

## 版本
- 版本: V1.0
- 更新时间: 2026-04-08

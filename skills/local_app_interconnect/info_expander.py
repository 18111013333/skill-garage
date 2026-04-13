#!/usr/bin/env python3
"""
信息扩展获取模块
终极鸽子王 V26.0 - 自动扩展获取相关信息

核心能力:
1. 识别扩展需求 (房源需要照片、位置等)
2. 自动获取扩展信息
3. 整合输出完整结果
"""

import os
import sys
import time
import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============== 枚举定义 ==============

class ExpandType(Enum):
    """扩展类型"""
    HOUSE = "house"          # 房源类
    BUSINESS = "business"    # 商家类
    PRODUCT = "product"      # 商品类
    SERVICE = "service"      # 服务类
    UNKNOWN = "unknown"


class InfoSource(Enum):
    """信息来源"""
    PHONE = "phone"          # 手机APP
    MAP = "map"              # 地图
    WEB = "web"              # 网络搜索
    AI = "ai"                # AI助手


# ============== 数据结构 ==============

@dataclass
class ExtensionRule:
    """扩展规则"""
    name: str
    priority: int
    source: InfoSource
    action: str
    output_type: str
    required: bool = False


@dataclass
class ExpandedInfo:
    """扩展信息"""
    name: str
    data: Any
    source: InfoSource
    success: bool


# ============== 扩展规则定义 ==============

EXTENSION_RULES = {
    ExpandType.HOUSE: [
        ExtensionRule("房间照片", 1, InfoSource.PHONE, "截图房源详情页图片", "图片列表", True),
        ExtensionRule("地理位置", 2, InfoSource.MAP, "获取经纬度+地址", "坐标+地址+地图", True),
        ExtensionRule("联系方式", 3, InfoSource.PHONE, "获取房东电话", "电话号码", True),
        ExtensionRule("价格详情", 4, InfoSource.WEB, "搜索价格对比", "价格范围", False),
        ExtensionRule("周边配套", 5, InfoSource.MAP, "搜索周边设施", "配套列表", False),
    ],
    ExpandType.BUSINESS: [
        ExtensionRule("商家照片", 1, InfoSource.PHONE, "获取商家图片", "图片列表", True),
        ExtensionRule("地理位置", 2, InfoSource.MAP, "获取位置信息", "坐标+地址", True),
        ExtensionRule("联系方式", 3, InfoSource.PHONE, "获取电话", "电话号码", True),
        ExtensionRule("营业信息", 4, InfoSource.WEB, "搜索营业时间", "营业时间", False),
        ExtensionRule("用户评价", 5, InfoSource.WEB, "搜索评价", "评分+评价", False),
    ],
    ExpandType.PRODUCT: [
        ExtensionRule("商品图片", 1, InfoSource.PHONE, "获取商品图片", "图片列表", True),
        ExtensionRule("价格对比", 2, InfoSource.WEB, "多平台比价", "价格列表", True),
        ExtensionRule("商品参数", 3, InfoSource.WEB, "获取详细参数", "参数表", False),
        ExtensionRule("用户评价", 4, InfoSource.WEB, "搜索评价", "评价摘要", False),
    ],
    ExpandType.SERVICE: [
        ExtensionRule("服务照片", 1, InfoSource.PHONE, "获取服务图片", "图片列表", False),
        ExtensionRule("地理位置", 2, InfoSource.MAP, "获取位置", "坐标+地址", True),
        ExtensionRule("联系方式", 3, InfoSource.PHONE, "获取电话", "电话号码", True),
        ExtensionRule("价格信息", 4, InfoSource.WEB, "搜索价格", "价格范围", False),
    ],
}

# 触发关键词
TRIGGER_KEYWORDS = {
    ExpandType.HOUSE: ["房源", "租房", "商铺", "门面", "写字楼", "公寓", "房子", "店铺出租"],
    ExpandType.BUSINESS: ["商家", "店铺", "餐厅", "酒店", "理发店", "装修公司", "美容院"],
    ExpandType.PRODUCT: ["商品", "产品", "价格", "比价", "购买", "买东西"],
    ExpandType.SERVICE: ["服务", "预约", "预订", "挂号", "订座"],
}


# ============== 扩展类型识别器 ==============

class ExpandTypeRecognizer:
    """扩展类型识别器"""
    
    def recognize(self, query: str) -> ExpandType:
        """识别扩展类型"""
        
        query_lower = query.lower()
        
        for expand_type, keywords in TRIGGER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return expand_type
        
        return ExpandType.UNKNOWN


# ============== 信息获取执行器 ==============

class InfoFetcher:
    """信息获取执行器"""
    
    def fetch(
        self,
        rule: ExtensionRule,
        context: Dict
    ) -> ExpandedInfo:
        """获取扩展信息"""
        
        logger.info(f"📦 获取扩展信息: {rule.name}")
        
        # 根据来源选择执行方式
        if rule.source == InfoSource.PHONE:
            data = self._fetch_from_phone(rule.action, context)
        elif rule.source == InfoSource.MAP:
            data = self._fetch_from_map(rule.action, context)
        elif rule.source == InfoSource.WEB:
            data = self._fetch_from_web(rule.action, context)
        elif rule.source == InfoSource.AI:
            data = self._fetch_from_ai(rule.action, context)
        else:
            data = None
        
        success = data is not None
        
        if success:
            logger.info(f"  ✅ {rule.name} 获取成功")
        else:
            logger.warning(f"  ⚠️ {rule.name} 获取失败")
        
        return ExpandedInfo(
            name=rule.name,
            data=data,
            source=rule.source,
            success=success
        )
    
    def _fetch_from_phone(self, action: str, context: Dict) -> Any:
        """从手机APP获取"""
        # 模拟手机操作
        if "照片" in action or "图片" in action:
            return [
                {"url": "photo1.jpg", "desc": "外观照片"},
                {"url": "photo2.jpg", "desc": "内部照片"},
            ]
        
        if "电话" in action or "联系" in action:
            return {"phone": "138****1234", "name": "房东"}
        
        return None
    
    def _fetch_from_map(self, action: str, context: Dict) -> Any:
        """从地图获取"""
        if "位置" in action or "经纬度" in action:
            return {
                "lat": 36.8131,
                "lng": 118.0658,
                "address": context.get("address", "未知地址"),
                "map_url": "map_screenshot.png"
            }
        
        if "周边" in action:
            return [
                {"type": "便利店", "name": "XX便利店", "distance": "50米"},
                {"type": "医院", "name": "XX医院", "distance": "500米"},
                {"type": "公交站", "name": "XX站", "distance": "200米"},
            ]
        
        return None
    
    def _fetch_from_web(self, action: str, context: Dict) -> Any:
        """从网络获取"""
        if "价格" in action:
            return {
                "min": 500,
                "max": 1000,
                "avg": 750,
                "source": "市场调研"
            }
        
        if "营业" in action:
            return {
                "hours": "8:00-18:00",
                "days": "周一至周日"
            }
        
        if "评价" in action:
            return {
                "rating": 4.5,
                "count": 128,
                "summary": "服务专业，价格合理"
            }
        
        return None
    
    def _fetch_from_ai(self, action: str, context: Dict) -> Any:
        """从AI助手获取"""
        return None


# ============== 信息扩展器 ==============

class InfoExpander:
    """信息扩展器"""
    
    def __init__(self):
        self.type_recognizer = ExpandTypeRecognizer()
        self.info_fetcher = InfoFetcher()
    
    def expand(
        self,
        query: str,
        base_result: Dict
    ) -> Dict:
        """
        扩展信息获取
        
        Args:
            query: 原始查询
            base_result: 基础结果
        
        Returns:
            扩展后的完整结果
        """
        # 1. 识别扩展类型
        expand_type = self.type_recognizer.recognize(query)
        
        if expand_type == ExpandType.UNKNOWN:
            logger.info("未识别到扩展需求，返回基础结果")
            return base_result
        
        logger.info(f"🔍 识别扩展类型: {expand_type.value}")
        
        # 2. 获取扩展规则
        rules = EXTENSION_RULES.get(expand_type, [])
        
        if not rules:
            return base_result
        
        # 3. 按优先级执行扩展
        expanded_info = {}
        
        for rule in sorted(rules, key=lambda x: x.priority):
            ext_info = self.info_fetcher.fetch(rule, base_result)
            
            if ext_info.success:
                expanded_info[ext_info.name] = ext_info.data
            elif rule.required:
                logger.warning(f"必需信息 {rule.name} 获取失败")
        
        # 4. 合并结果
        result = {
            **base_result,
            "expanded": expanded_info,
            "expand_type": expand_type.value
        }
        
        return result


# ============== 结果格式化器 ==============

class ResultFormatter:
    """结果格式化器"""
    
    def format(self, result: Dict) -> str:
        """格式化结果"""
        
        expand_type = result.get("expand_type", "unknown")
        expanded = result.get("expanded", {})
        
        if expand_type == "house":
            return self._format_house(result, expanded)
        elif expand_type == "business":
            return self._format_business(result, expanded)
        elif expand_type == "product":
            return self._format_product(result, expanded)
        else:
            return self._format_default(result)
    
    def _format_house(self, result: Dict, expanded: Dict) -> str:
        """格式化房源信息"""
        lines = ["🏠 房源信息", ""]
        
        # 基本信息
        lines.append("【基本信息】")
        lines.append(f"名称: {result.get('title', '未知')}")
        lines.append(f"面积: {result.get('area', '未知')}㎡")
        lines.append(f"月租: {result.get('price', '未知')}元")
        lines.append(f"地址: {result.get('address', '未知')}")
        lines.append("")
        
        # 房间照片
        if "房间照片" in expanded:
            lines.append("【房间照片】")
            for i, photo in enumerate(expanded["房间照片"], 1):
                lines.append(f"[图片{i}: {photo.get('desc', '')}]")
            lines.append("")
        
        # 地理位置
        if "地理位置" in expanded:
            loc = expanded["地理位置"]
            lines.append("【地理位置】")
            lines.append(f"📍 经纬度: {loc.get('lat', 0)}, {loc.get('lng', 0)}")
            lines.append(f"🗺️ [地图截图]")
            lines.append("")
        
        # 联系方式
        if "联系方式" in expanded:
            contact = expanded["联系方式"]
            lines.append("【联系方式】")
            lines.append(f"👤 联系人: {contact.get('name', '未知')}")
            lines.append(f"📞 电话: {contact.get('phone', '未知')}")
            lines.append("")
        
        # 周边配套
        if "周边配套" in expanded:
            lines.append("【周边配套】")
            for item in expanded["周边配套"]:
                lines.append(f"{item.get('type', '')}: {item.get('name', '')} ({item.get('distance', '')})")
        
        return "\n".join(lines)
    
    def _format_business(self, result: Dict, expanded: Dict) -> str:
        """格式化商家信息"""
        lines = ["🏪 商家信息", ""]
        
        lines.append("【基本信息】")
        lines.append(f"名称: {result.get('name', '未知')}")
        lines.append(f"地址: {result.get('address', '未知')}")
        
        if "营业信息" in expanded:
            hours = expanded["营业信息"]
            lines.append(f"营业时间: {hours.get('hours', '未知')}")
        lines.append("")
        
        if "商家照片" in expanded:
            lines.append("【商家照片】")
            for i, photo in enumerate(expanded["商家照片"], 1):
                lines.append(f"[图片{i}]")
            lines.append("")
        
        if "地理位置" in expanded:
            loc = expanded["地理位置"]
            lines.append("【地理位置】")
            lines.append(f"📍 {loc.get('address', '未知')}")
            lines.append("")
        
        if "联系方式" in expanded:
            lines.append("【联系方式】")
            lines.append(f"📞 {expanded['联系方式'].get('phone', '未知')}")
            lines.append("")
        
        if "用户评价" in expanded:
            review = expanded["用户评价"]
            lines.append("【用户评价】")
            lines.append(f"⭐ 评分: {review.get('rating', 0)}/5.0")
            lines.append(f"💬 {review.get('summary', '')}")
        
        return "\n".join(lines)
    
    def _format_product(self, result: Dict, expanded: Dict) -> str:
        """格式化商品信息"""
        lines = ["🛒 商品信息", ""]
        
        lines.append("【基本信息】")
        lines.append(f"名称: {result.get('name', '未知')}")
        lines.append("")
        
        if "商品图片" in expanded:
            lines.append("【商品图片】")
            for i in range(len(expanded["商品图片"])):
                lines.append(f"[图片{i+1}]")
            lines.append("")
        
        if "价格对比" in expanded:
            price = expanded["价格对比"]
            lines.append("【价格对比】")
            lines.append(f"最低: ¥{price.get('min', 0)}")
            lines.append(f"最高: ¥{price.get('max', 0)}")
            lines.append(f"平均: ¥{price.get('avg', 0)}")
            lines.append("")
        
        if "用户评价" in expanded:
            review = expanded["用户评价"]
            lines.append("【用户评价】")
            lines.append(f"⭐ {review.get('rating', 0)}/5.0 ({review.get('count', 0)}条评价)")
        
        return "\n".join(lines)
    
    def _format_default(self, result: Dict) -> str:
        """默认格式化"""
        return json.dumps(result, ensure_ascii=False, indent=2)


# ============== 测试 ==============

def test_info_expander():
    """测试信息扩展"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          信息扩展获取测试                                              ║
║          自动扩展: 照片 + 位置 + 联系方式 + 周边配套                     ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    expander = InfoExpander()
    formatter = ResultFormatter()
    
    # 测试房源扩展
    print("\n🏠 测试房源扩展:\n")
    
    base_result = {
        "title": "淄川城张村沿街门头",
        "area": 28,
        "price": 550,
        "address": "山东省淄博市淄川区松龄路街道城张街"
    }
    
    result = expander.expand("帮我找淄博商铺", base_result)
    formatted = formatter.format(result)
    print(formatted)
    
    # 测试商家扩展
    print("\n" + "="*60)
    print("\n🏪 测试商家扩展:\n")
    
    base_result2 = {
        "name": "XX装修公司",
        "address": "淄博市张店区XX路"
    }
    
    result2 = expander.expand("帮我找装修公司", base_result2)
    formatted2 = formatter.format(result2)
    print(formatted2)
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    test_info_expander()

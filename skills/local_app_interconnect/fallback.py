#!/usr/bin/env python3
"""
搜索失败降级模块
终极鸽子王 V26.0 - 搜索失败自动降级到手机操作

核心能力:
1. 检测搜索结果完整性
2. 判断目标是否达成
3. 自动降级到手机操作
4. 结果融合返回
"""

import os
import sys
import time
import json
import re
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============== 枚举定义 ==============

class FallbackReason(Enum):
    """降级原因"""
    NO_RESULT = "搜索无结果"
    INCOMPLETE = "信息不完整"
    TARGET_NOT_REACHED = "目标未达成"
    HIDDEN_INFO = "信息被隐藏"
    NEED_LOGIN = "需要登录"
    NEED_VERIFY = "需要验证"
    NOT_REALTIME = "信息不实时"


# ============== 数据结构 ==============

@dataclass
class SearchResult:
    """搜索结果"""
    success: bool
    data: Dict
    has_result: bool = False
    is_complete: bool = False
    target_reached: bool = False
    hidden_detected: bool = False


@dataclass
class FallbackDecision:
    """降级决策"""
    should_fallback: bool
    reasons: List[FallbackReason]
    confidence: float


# ============== 搜索结果检测器 ==============

class SearchResultChecker:
    """搜索结果检测器"""
    
    # 隐藏信息标记
    HIDDEN_INDICATORS = [
        "****", "隐藏", "已隐藏", "被隐藏",
        "需要登录", "登录后查看", "登录可见", "请登录",
        "需要验证", "验证后查看", "请验证",
        "查看完整", "获取完整", "点击查看", "扫码查看",
        "暂无数据", "无数据", "数据不存在",
    ]
    
    # 关键字段
    KEY_FIELDS = {
        "联系方式": ["phone", "contact", "tel", "mobile", "电话", "手机"],
        "电话": ["phone", "tel", "mobile", "电话", "手机"],
        "地址": ["address", "location", "地址", "位置"],
        "价格": ["price", "cost", "费用", "价格", "多少钱"],
        "名称": ["name", "title", "名称", "标题"],
    }
    
    def check(self, result: Dict, target: str = "") -> SearchResult:
        """检查搜索结果"""
        
        if not result:
            return SearchResult(
                success=False,
                data={},
                has_result=False,
                is_complete=False,
                target_reached=False
            )
        
        # 检查是否有结果
        has_result = self._check_has_result(result)
        
        # 检查是否完整
        is_complete = self._check_completeness(result, target)
        
        # 检查目标是否达成
        target_reached = self._check_target_reached(result, target)
        
        # 检查是否有隐藏信息
        hidden_detected = self._check_hidden_info(result)
        
        return SearchResult(
            success=has_result and is_complete and target_reached,
            data=result,
            has_result=has_result,
            is_complete=is_complete,
            target_reached=target_reached,
            hidden_detected=hidden_detected
        )
    
    def _check_has_result(self, result: Dict) -> bool:
        """检查是否有结果"""
        
        # 检查是否为空
        if not result:
            return False
        
        # 检查结果列表
        if "results" in result:
            return len(result["results"]) > 0
        
        if "items" in result:
            return len(result["items"]) > 0
        
        if "data" in result:
            return bool(result["data"])
        
        # 检查是否有任何非空值
        for key, value in result.items():
            if value and not key.startswith("_"):
                return True
        
        return False
    
    def _check_completeness(self, result: Dict, target: str) -> bool:
        """检查信息是否完整"""
        
        # 如果没有指定目标，默认检查所有关键字段
        if not target:
            return True
        
        # 获取目标对应的关键字段
        key_fields = self.KEY_FIELDS.get(target, [])
        
        if not key_fields:
            return True
        
        # 检查关键字段是否存在且非空
        for field in key_fields:
            value = result.get(field)
            if not value:
                # 检查嵌套字段
                for key, val in result.items():
                    if isinstance(val, dict) and field in val:
                        value = val[field]
                        break
            
            if not value:
                return False
        
        return True
    
    def _check_target_reached(self, result: Dict, target: str) -> bool:
        """检查目标是否达成"""
        
        # 联系方式目标
        if target in ["联系方式", "电话"]:
            phone = result.get("phone") or result.get("tel") or result.get("mobile")
            if phone:
                # 检查是否是完整电话号码
                clean_phone = re.sub(r'[^\d]', '', str(phone))
                if len(clean_phone) >= 11:
                    return True
            return False
        
        # 地址目标
        if target == "地址":
            address = result.get("address") or result.get("location")
            return bool(address and len(address) > 5)
        
        # 价格目标
        if target == "价格":
            price = result.get("price") or result.get("cost")
            return bool(price)
        
        # 默认：有结果即达成
        return self._check_has_result(result)
    
    def _check_hidden_info(self, result: Dict) -> bool:
        """检查是否有隐藏信息"""
        
        result_text = json.dumps(result, ensure_ascii=False)
        
        for indicator in self.HIDDEN_INDICATORS:
            if indicator in result_text:
                return True
        
        return False


# ============== 降级决策器 ==============

class FallbackDecider:
    """降级决策器"""
    
    def __init__(self):
        self.checker = SearchResultChecker()
    
    def decide(
        self,
        search_result: Dict,
        target: str = "",
        original_query: str = ""
    ) -> FallbackDecision:
        """
        决定是否降级
        
        Args:
            search_result: 搜索结果
            target: 目标信息类型
            original_query: 原始查询
        
        Returns:
            降级决策
        """
        reasons = []
        
        # 检查搜索结果
        checked = self.checker.check(search_result, target)
        
        # 1. 无结果
        if not checked.has_result:
            reasons.append(FallbackReason.NO_RESULT)
        
        # 2. 信息不完整
        if checked.has_result and not checked.is_complete:
            reasons.append(FallbackReason.INCOMPLETE)
        
        # 3. 目标未达成
        if checked.has_result and not checked.target_reached:
            reasons.append(FallbackReason.TARGET_NOT_REACHED)
        
        # 4. 信息被隐藏
        if checked.hidden_detected:
            reasons.append(FallbackReason.HIDDEN_INFO)
        
        # 5. 检查是否需要登录/验证
        result_text = json.dumps(search_result, ensure_ascii=False)
        if "登录" in result_text:
            reasons.append(FallbackReason.NEED_LOGIN)
        if "验证" in result_text:
            reasons.append(FallbackReason.NEED_VERIFY)
        
        # 计算置信度
        should_fallback = len(reasons) > 0
        confidence = min(0.9, 0.5 + len(reasons) * 0.1)
        
        return FallbackDecision(
            should_fallback=should_fallback,
            reasons=reasons,
            confidence=confidence
        )


# ============== 降级执行器 ==============

class FallbackExecutor:
    """降级执行器"""
    
    def __init__(self):
        self.decider = FallbackDecider()
    
    def execute_with_fallback(
        self,
        query: str,
        target: str,
        search_func: Callable,
        phone_func: Callable
    ) -> Dict:
        """
        带降级的执行
        
        Args:
            query: 查询
            target: 目标
            search_func: 搜索函数
            phone_func: 手机操作函数
        
        Returns:
            执行结果
        """
        logger.info(f"🔍 尝试搜索: {query}")
        
        # 1. 执行搜索
        search_result = search_func(query)
        
        # 2. 判断是否需要降级
        decision = self.decider.decide(search_result, target, query)
        
        if decision.should_fallback:
            # 记录降级原因
            reason_str = ", ".join([r.value for r in decision.reasons])
            logger.info(f"🔄 降级到手机操作: {reason_str}")
            
            # 3. 执行手机操作
            phone_result = phone_func(query)
            
            return {
                "source": "phone",
                "result": phone_result,
                "fallback": True,
                "fallback_reasons": [r.value for r in decision.reasons],
                "search_result": search_result
            }
        
        # 4. 搜索成功
        logger.info(f"✅ 搜索成功，返回结果")
        
        return {
            "source": "search",
            "result": search_result,
            "fallback": False
        }


# ============== 测试 ==============

def test_fallback():
    """测试降级机制"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          搜索失败降级测试                                              ║
║          搜索失败 → 自动降级到手机操作                                  ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    executor = FallbackExecutor()
    
    # 模拟搜索函数
    def mock_search(query: str) -> Dict:
        # 模拟不同场景
        if "隐藏" in query:
            return {"phone": "138****1234", "note": "需要登录查看完整"}
        elif "无结果" in query:
            return {}
        elif "不完整" in query:
            return {"name": "测试商家"}  # 缺少电话
        else:
            return {"name": "测试商家", "phone": "13812345678"}
    
    # 模拟手机操作函数
    def mock_phone(query: str) -> Dict:
        return {"phone": "13812345678", "source": "APP"}
    
    # 测试用例
    test_cases = [
        ("获取商家联系方式", "联系方式"),
        ("获取隐藏的电话号码", "电话"),
        ("搜索无结果的信息", "联系方式"),
        ("获取不完整的信息", "联系方式"),
    ]
    
    print("\n📊 测试结果:\n")
    
    for query, target in test_cases:
        print(f"\n查询: {query}")
        print(f"目标: {target}")
        
        result = executor.execute_with_fallback(
            query=query,
            target=target,
            search_func=mock_search,
            phone_func=mock_phone
        )
        
        print(f"来源: {result['source']}")
        print(f"降级: {result['fallback']}")
        if result['fallback']:
            print(f"降级原因: {result['fallback_reasons']}")
        print(f"结果: {result['result']}")
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    test_fallback()

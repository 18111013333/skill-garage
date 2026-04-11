#!/usr/bin/env python3
"""
智能任务路由器
终极鸽子王 V26.0 - 自动判断执行路径

核心能力:
1. 意图识别 - 理解用户想要什么
2. 数据源判断 - 确定信息来源
3. 工具选择 - 选择最优工具
4. 策略决策 - 确定执行方式
"""

import os
import sys
import re
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============== 枚举定义 ==============

class TaskType(Enum):
    """任务类型"""
    SEARCH_ONLY = "search_only"      # 只需搜索
    PHONE_OPERATION = "phone"        # 需要手机操作
    HYBRID = "hybrid"                # 混合任务
    OTHER = "other"                  # 其他功能


class ExecutionStrategy(Enum):
    """执行策略"""
    SEARCH = "search"                # 纯搜索
    PHONE = "phone"                  # 纯手机操作
    PARALLEL = "parallel"            # 并行执行
    SEQUENTIAL = "sequential"        # 顺序执行
    TOOL = "tool"                    # 专用工具


# ============== 数据结构 ==============

@dataclass
class Intent:
    """意图"""
    verbs: List[str]          # 动词
    entities: List[str]       # 实体
    target: str               # 目标
    raw_query: str            # 原始查询


@dataclass
class RoutingResult:
    """路由结果"""
    task_type: TaskType
    tools: List[str]
    strategy: ExecutionStrategy
    confidence: float
    reason: str


# ============== 意图识别器 ==============

class IntentRecognizer:
    """意图识别器"""
    
    # 动词词典
    VERB_DICT = {
        "查询": ["查", "搜索", "找", "查找", "查询", "了解", "看看", "搜索一下"],
        "获取": ["获取", "得到", "拿到", "查看", "看", "获取到"],
        "创建": ["创建", "新建", "添加", "设置", "建立", "写"],
        "发送": ["发", "发送", "发给", "传", "分享"],
        "拨打": ["打", "拨打", "呼叫", "联系"],
        "预约": ["预约", "预订", "订", "约"],
        "购买": ["买", "购买", "下单", "订购"],
    }
    
    # 实体词典
    ENTITY_DICT = {
        "信息": ["信息", "内容", "详情", "资料", "数据"],
        "联系方式": ["联系方式", "电话", "号码", "手机号", "联系电话"],
        "商品": ["商品", "东西", "物品", "产品"],
        "服务": ["服务", "预约", "预订"],
        "位置": ["位置", "地址", "地点", "在哪"],
        "时间": ["时间", "几点", "什么时候", "日期"],
        "价格": ["价格", "多少钱", "费用", "收费"],
    }
    
    def recognize(self, query: str) -> Intent:
        """识别意图"""
        verbs = self._extract_verbs(query)
        entities = self._extract_entities(query)
        target = self._extract_target(query)
        
        return Intent(
            verbs=verbs,
            entities=entities,
            target=target,
            raw_query=query
        )
    
    def _extract_verbs(self, query: str) -> List[str]:
        """提取动词"""
        verbs = []
        for verb_type, keywords in self.VERB_DICT.items():
            for keyword in keywords:
                if keyword in query:
                    verbs.append(verb_type)
                    break
        return verbs
    
    def _extract_entities(self, query: str) -> List[str]:
        """提取实体"""
        entities = []
        for entity_type, keywords in self.ENTITY_DICT.items():
            for keyword in keywords:
                if keyword in query:
                    entities.append(entity_type)
                    break
        return entities
    
    def _extract_target(self, query: str) -> str:
        """提取目标"""
        # 简单实现：返回查询中的关键名词
        return query


# ============== 数据源判断器 ==============

class DataSourceDeterminer:
    """数据源判断器"""
    
    # 只需搜索的关键词
    SEARCH_ONLY_KEYWORDS = [
        # 公开信息
        "天气", "新闻", "百科", "知识", "是什么", "怎么样",
        # 网页可访问
        "地址", "电话", "营业时间", "价格", "评价", "评分",
        "路线", "怎么走", "附近", "有哪些", "列表",
        # 无需登录
        "公交", "地铁", "餐厅", "酒店", "景点", "银行",
        "医院", "学校", "商场", "超市", "公园",
    ]
    
    # 需要手机操作的关键词
    PHONE_OPERATION_KEYWORDS = [
        # 需要登录
        "我的", "个人", "账号", "订单", "收藏", "消息",
        "私信", "通知", "设置", "账户",
        # APP特有功能
        "发朋友圈", "扫码", "支付", "打车", "签到", "打卡",
        "评论", "回复", "分享到", "上传",
        # 隐藏信息
        "联系方式", "电话号码", "完整电话", "真实号码",
        "获取电话", "查看电话", "房东电话", "商家电话",
        # 需要操作
        "预约", "下单", "购买", "拨打", "通话", "预订",
        # 无法通过搜索获取
        "实时", "最新", "当前", "现在", "即时",
        "确认", "验证", "核实", "检查",
    ]
    
    # 搜索失败后需要手机操作的场景
    SEARCH_FALLBACK_KEYWORDS = [
        "找不到", "没有结果", "信息不全", "无法获取",
        "需要登录", "需要验证", "被隐藏", "看不到",
    ]
    
    # 混合任务模式
    HYBRID_PATTERNS = [
        (r"找.*并.*联系", "找XX并获取联系方式"),
        (r"搜索.*并.*详情", "搜索XX并查看详情"),
        (r"查.*并.*预约", "查XX并预约"),
        (r"找.*并.*下单", "找XX并下单"),
        (r"比价.*购买", "比价后购买"),
        (r"搜索.*获取", "搜索并获取"),
        (r"找.*电话", "找XX的电话"),
        (r"找.*联系方式", "找XX的联系方式"),
    ]
    
    # 其他功能关键词
    OTHER_FUNCTION_KEYWORDS = {
        "note": ["备忘录", "笔记", "记一下", "记录"],
        "calendar": ["日程", "日历", "安排", "计划"],
        "alarm": ["闹钟", "提醒", "定时"],
        "message": ["短信", "发消息", "发短信"],
        "call": ["打电话", "拨打电话", "联系"],
        "file": ["文件", "文档", "搜索文件"],
        "location": ["位置", "定位", "我在哪"],
        "photo": ["照片", "图片", "相册"],
    }
    
    def determine(self, query: str, intent: Intent) -> Tuple[TaskType, float, str]:
        """
        判断数据源
        
        Returns:
            (任务类型, 置信度, 原因)
        """
        
        # 1. 检查其他功能
        for func_type, keywords in self.OTHER_FUNCTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query:
                    return TaskType.OTHER, 0.9, f"匹配其他功能: {func_type}"
        
        # 2. 检查混合任务
        for pattern, desc in self.HYBRID_PATTERNS:
            if re.search(pattern, query):
                return TaskType.HYBRID, 0.85, f"匹配混合模式: {desc}"
        
        # 3. 检查是否需要手机操作
        phone_score = 0
        for keyword in self.PHONE_OPERATION_KEYWORDS:
            if keyword in query:
                phone_score += 1
        
        if phone_score >= 2:
            return TaskType.PHONE_OPERATION, 0.9, f"匹配{phone_score}个手机操作关键词"
        
        if phone_score == 1:
            return TaskType.PHONE_OPERATION, 0.75, "匹配1个手机操作关键词"
        
        # 4. 检查是否只需搜索
        search_score = 0
        for keyword in self.SEARCH_ONLY_KEYWORDS:
            if keyword in query:
                search_score += 1
        
        if search_score >= 2:
            return TaskType.SEARCH_ONLY, 0.9, f"匹配{search_score}个搜索关键词"
        
        if search_score == 1:
            return TaskType.SEARCH_ONLY, 0.75, "匹配1个搜索关键词"
        
        # 5. 默认：搜索
        return TaskType.SEARCH_ONLY, 0.6, "默认使用搜索"


# ============== 工具选择器 ==============

class ToolSelector:
    """工具选择器"""
    
    # 任务类型到工具的映射
    TOOL_MAP = {
        TaskType.SEARCH_ONLY: ["browser", "web_fetch"],
        TaskType.PHONE_OPERATION: ["xiaoyi_gui_agent"],
        TaskType.HYBRID: ["browser", "xiaoyi_gui_agent"],
        TaskType.OTHER: ["专用工具"],
    }
    
    # 其他功能到工具的映射
    OTHER_TOOL_MAP = {
        "note": "create_note",
        "calendar": "create_calendar_event",
        "alarm": "create_alarm",
        "message": "send_message",
        "call": "call_phone",
        "file": "search_file",
        "location": "get_user_location",
        "photo": "search_photo_gallery",
    }
    
    def select(self, task_type: TaskType, query: str) -> List[str]:
        """选择工具"""
        tools = self.TOOL_MAP.get(task_type, ["browser"]).copy()
        
        # 如果是其他功能，添加具体工具
        if task_type == TaskType.OTHER:
            for func_type, tool in self.OTHER_TOOL_MAP.items():
                for keyword in DataSourceDeterminer.OTHER_FUNCTION_KEYWORDS.get(func_type, []):
                    if keyword in query:
                        tools = [tool]
                        break
        
        return tools


# ============== 策略决策器 ==============

class StrategyDecider:
    """策略决策器"""
    
    def decide(self, task_type: TaskType, tools: List[str]) -> ExecutionStrategy:
        """决定执行策略"""
        
        if task_type == TaskType.SEARCH_ONLY:
            return ExecutionStrategy.SEARCH
        
        if task_type == TaskType.PHONE_OPERATION:
            return ExecutionStrategy.PHONE
        
        if task_type == TaskType.HYBRID:
            # 如果有多个工具，使用并行或顺序
            if len(tools) > 1:
                return ExecutionStrategy.PARALLEL
            return ExecutionStrategy.SEQUENTIAL
        
        if task_type == TaskType.OTHER:
            return ExecutionStrategy.TOOL
        
        return ExecutionStrategy.SEARCH


# ============== 智能路由器 ==============

class SmartTaskRouter:
    """智能任务路由器"""
    
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.data_source_determiner = DataSourceDeterminer()
        self.tool_selector = ToolSelector()
        self.strategy_decider = StrategyDecider()
    
    def route(self, query: str) -> RoutingResult:
        """
        路由任务
        
        Args:
            query: 用户查询
        
        Returns:
            路由结果
        """
        logger.info(f"🔍 路由任务: {query}")
        
        # 1. 意图识别
        intent = self.intent_recognizer.recognize(query)
        logger.info(f"  意图: verbs={intent.verbs}, entities={intent.entities}")
        
        # 2. 数据源判断
        task_type, confidence, reason = self.data_source_determiner.determine(query, intent)
        logger.info(f"  类型: {task_type.value} (置信度: {confidence:.2f}, 原因: {reason})")
        
        # 3. 工具选择
        tools = self.tool_selector.select(task_type, query)
        logger.info(f"  工具: {tools}")
        
        # 4. 策略决策
        strategy = self.strategy_decider.decide(task_type, tools)
        logger.info(f"  策略: {strategy.value}")
        
        return RoutingResult(
            task_type=task_type,
            tools=tools,
            strategy=strategy,
            confidence=confidence,
            reason=reason
        )


# ============== 测试 ==============

def test_router():
    """测试路由器"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          智能任务路由器测试                                            ║
║          自动判断: 搜索 | 手机操作 | 混合 | 其他                        ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    router = SmartTaskRouter()
    
    # 测试用例
    test_cases = [
        "今天淄博天气怎么样",
        "帮我获取房东电话",
        "找淄博商铺并获取联系方式",
        "创建备忘录",
        "设置明天8点闹钟",
        "发短信给张三",
        "附近的银行有哪些",
        "我的淘宝订单",
        "搜索淄博装修公司并获取电话",
        "比价iPhone 15然后购买最便宜的",
    ]
    
    print("\n📊 路由结果:\n")
    print("-" * 80)
    
    for query in test_cases:
        result = router.route(query)
        
        print(f"\n查询: {query}")
        print(f"  类型: {result.task_type.value}")
        print(f"  工具: {result.tools}")
        print(f"  策略: {result.strategy.value}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  原因: {result.reason}")
    
    print("\n" + "-" * 80)
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    test_router()

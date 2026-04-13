#!/usr/bin/env python3
"""
手机操作失败自愈模块
终极鸽子王 V26.0 - 失败后自动搜索流程学习重试

核心能力:
1. 失败原因分析
2. 自动搜索操作流程
3. 学习流程步骤
4. 按流程重试
"""

import os
import sys
import time
import re
import json
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============== 枚举定义 ==============

class ErrorType(Enum):
    """错误类型"""
    TIMEOUT = "超时"
    ELEMENT_NOT_FOUND = "元素未找到"
    PERMISSION_DENIED = "权限被拒绝"
    NETWORK_ERROR = "网络错误"
    LOGIN_REQUIRED = "需要登录"
    APP_CRASH = "应用崩溃"
    UNKNOWN = "未知错误"


# ============== 数据结构 ==============

@dataclass
class FailureAnalysis:
    """失败分析"""
    error_type: ErrorType
    error_message: str
    failed_step: str
    suggested_search: str


@dataclass
class ProcedureStep:
    """流程步骤"""
    index: int
    description: str
    action: str
    verification: str


@dataclass
class SelfHealingResult:
    """自愈结果"""
    success: bool
    original_error: str
    healing_attempts: int
    procedure_used: List[ProcedureStep]
    final_result: Any


# ============== 失败分析器 ==============

class FailureAnalyzer:
    """失败分析器"""
    
    # 错误关键词映射
    ERROR_KEYWORDS = {
        ErrorType.TIMEOUT: ["timeout", "超时", "timed out", "响应超时"],
        ErrorType.ELEMENT_NOT_FOUND: ["not found", "找不到", "未找到", "不存在"],
        ErrorType.PERMISSION_DENIED: ["permission", "权限", "拒绝", "denied"],
        ErrorType.NETWORK_ERROR: ["network", "网络", "连接失败", "connection"],
        ErrorType.LOGIN_REQUIRED: ["login", "登录", "请登录", "需要登录"],
        ErrorType.APP_CRASH: ["crash", "崩溃", "闪退", "异常退出"],
    }
    
    def analyze(
        self,
        error: Exception,
        context: Dict
    ) -> FailureAnalysis:
        """分析失败原因"""
        
        error_str = str(error).lower()
        
        # 分类错误
        error_type = self._classify_error(error_str)
        
        # 获取失败步骤
        failed_step = context.get("current_step", "unknown")
        
        # 生成搜索建议
        suggested_search = self._generate_search_query(error_type, context)
        
        return FailureAnalysis(
            error_type=error_type,
            error_message=str(error),
            failed_step=failed_step,
            suggested_search=suggested_search
        )
    
    def _classify_error(self, error_str: str) -> ErrorType:
        """分类错误"""
        for error_type, keywords in self.ERROR_KEYWORDS.items():
            for keyword in keywords:
                if keyword in error_str:
                    return error_type
        return ErrorType.UNKNOWN
    
    def _generate_search_query(
        self,
        error_type: ErrorType,
        context: Dict
    ) -> str:
        """生成搜索查询"""
        
        app_name = context.get("app_name", "手机APP")
        action = context.get("action", "操作")
        
        # 根据错误类型生成不同查询
        query_templates = {
            ErrorType.TIMEOUT: f"{app_name} {action} 超时怎么办",
            ErrorType.ELEMENT_NOT_FOUND: f"{app_name} {action} 找不到按钮",
            ErrorType.PERMISSION_DENIED: f"{app_name} 权限设置教程",
            ErrorType.NETWORK_ERROR: f"{app_name} 网络连接问题解决",
            ErrorType.LOGIN_REQUIRED: f"{app_name} 登录教程",
            ErrorType.APP_CRASH: f"{app_name} 崩溃闪退解决",
            ErrorType.UNKNOWN: f"{app_name} {action} 详细教程",
        }
        
        return query_templates.get(error_type, f"{app_name} {action} 教程")


# ============== 流程搜索器 ==============

class ProcedureSearcher:
    """流程搜索器"""
    
    # 搜索来源
    SEARCH_SOURCES = [
        ("AI助手", "豆包/Kimi/文心"),
        ("搜索引擎", "百度/必应"),
        ("经验平台", "知乎/小红书/B站"),
        ("官方文档", "帮助中心"),
    ]
    
    def search(self, query: str) -> Dict:
        """搜索操作流程"""
        
        logger.info(f"🔍 搜索操作流程: {query}")
        
        results = []
        
        # 1. AI助手搜索
        ai_result = self._search_ai(query)
        if ai_result:
            results.append(ai_result)
        
        # 2. 网络搜索
        web_result = self._search_web(query)
        if web_result:
            results.append(web_result)
        
        # 3. 合并结果
        merged = self._merge_results(results)
        
        return merged
    
    def _search_ai(self, query: str) -> Optional[Dict]:
        """搜索AI助手"""
        # 模拟AI搜索
        logger.info("  📱 搜索AI助手...")
        
        # 返回模拟结果
        return {
            "source": "AI助手",
            "content": f"""
操作步骤：
1. 打开APP，进入主界面
2. 点击搜索框，输入关键词
3. 在搜索结果中找到目标
4. 点击进入详情页
5. 找到联系方式并记录

注意事项：
- 确保网络连接正常
- 如果找不到，尝试刷新页面
- 部分信息需要登录后才能查看
"""
        }
    
    def _search_web(self, query: str) -> Optional[Dict]:
        """网络搜索"""
        logger.info("  🌐 网络搜索...")
        
        # 返回模拟结果
        return {
            "source": "网络搜索",
            "content": f"搜索结果: {query} 的操作教程..."
        }
    
    def _merge_results(self, results: List[Dict]) -> Dict:
        """合并结果"""
        if not results:
            return {"source": "无", "content": ""}
        
        # 取第一个有效结果
        return results[0]


# ============== 流程学习器 ==============

class ProcedureLearner:
    """流程学习器"""
    
    # 操作关键词
    ACTION_KEYWORDS = [
        "点击", "长按", "滑动", "输入", "选择",
        "打开", "关闭", "搜索", "确认", "提交",
        "复制", "粘贴", "截图", "分享", "保存",
    ]
    
    def learn(self, search_result: Dict) -> List[ProcedureStep]:
        """学习操作流程"""
        
        content = search_result.get("content", "")
        
        # 提取步骤
        steps = self._extract_steps(content)
        
        # 如果没有提取到步骤，生成默认步骤
        if not steps:
            steps = self._generate_default_steps(content)
        
        # 转换为ProcedureStep
        procedure = []
        for i, step in enumerate(steps, 1):
            procedure.append(ProcedureStep(
                index=i,
                description=step,
                action=self._extract_action(step),
                verification=self._generate_verification(step)
            ))
        
        logger.info(f"📚 学习到 {len(procedure)} 个步骤")
        
        return procedure
    
    def _extract_steps(self, content: str) -> List[str]:
        """提取步骤"""
        steps = []
        
        # 匹配数字步骤: 1. xxx 或 1、xxx 或 1) xxx
        patterns = [
            r'[1-9][0-9]?[\.、)]\s*(.+?)(?=[1-9][0-9]?[\.、)]|$)',
            r'第[一二三四五六七八九十]+步[：:]\s*(.+?)(?=第[一二三四五六七八九十]+步|$)',
            r'Step\s*[1-9][0-9]?[：:]\s*(.+?)(?=Step\s*[1-9][0-9]?|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                steps = [m.strip() for m in matches if m.strip()]
                break
        
        return steps
    
    def _generate_default_steps(self, content: str) -> List[str]:
        """生成默认步骤"""
        # 从内容中提取关键操作
        steps = []
        
        for keyword in self.ACTION_KEYWORDS:
            if keyword in content:
                # 找到包含关键词的句子
                sentences = content.split('。')
                for sentence in sentences:
                    if keyword in sentence:
                        steps.append(sentence.strip())
                        break
        
        return steps[:5]  # 最多5步
    
    def _extract_action(self, step: str) -> str:
        """提取动作"""
        for keyword in self.ACTION_KEYWORDS:
            if keyword in step:
                return keyword
        return "操作"
    
    def _generate_verification(self, step: str) -> str:
        """生成验证点"""
        if "点击" in step:
            return "确认按钮已点击"
        if "输入" in step:
            return "确认内容已输入"
        if "搜索" in step:
            return "确认搜索结果已显示"
        return "确认操作完成"


# ============== 引导重试器 ==============

class GuidedRetry:
    """引导重试器"""
    
    def __init__(self):
        self.current_step = 0
    
    def retry(
        self,
        guide: List[ProcedureStep],
        phone_func: Callable
    ) -> Dict:
        """按流程重试"""
        
        logger.info(f"🔄 按流程重试，共 {len(guide)} 步")
        
        results = []
        
        for step in guide:
            self.current_step = step.index
            
            logger.info(f"  步骤{step.index}: {step.description[:30]}...")
            
            # 执行步骤
            step_result = self._execute_step(step, phone_func)
            results.append(step_result)
            
            if not step_result["success"]:
                # 步骤失败
                logger.warning(f"  ⚠️ 步骤{step.index}失败")
                
                # 尝试调整重试
                adjusted = self._adjust_and_retry(step, phone_func)
                if adjusted["success"]:
                    results[-1] = adjusted
                    logger.info(f"  ✅ 调整后成功")
                else:
                    return {
                        "success": False,
                        "failed_at_step": step.index,
                        "results": results
                    }
            else:
                logger.info(f"  ✅ 步骤{step.index}成功")
        
        return {
            "success": True,
            "results": results
        }
    
    def _execute_step(
        self,
        step: ProcedureStep,
        phone_func: Callable
    ) -> Dict:
        """执行步骤"""
        
        instruction = f"执行步骤{step.index}: {step.description}"
        
        # 调用手机操作
        result = phone_func(instruction)
        
        return {
            "step": step.index,
            "success": result.get("success", True),
            "result": result
        }
    
    def _adjust_and_retry(
        self,
        step: ProcedureStep,
        phone_func: Callable
    ) -> Dict:
        """调整并重试"""
        
        # 尝试不同的表述
        variations = [
            f"请{step.action}",
            f"尝试{step.description}",
            f"重新{step.action}",
        ]
        
        for variation in variations:
            result = phone_func(variation)
            if result.get("success"):
                return {"step": step.index, "success": True, "result": result}
        
        return {"step": step.index, "success": False, "result": {}}


# ============== 自愈执行器 ==============

class SelfHealingExecutor:
    """自愈执行器"""
    
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        
        self.failure_analyzer = FailureAnalyzer()
        self.procedure_searcher = ProcedureSearcher()
        self.procedure_learner = ProcedureLearner()
        self.guided_retry = GuidedRetry()
    
    def execute_with_healing(
        self,
        query: str,
        phone_func: Callable
    ) -> SelfHealingResult:
        """
        带自愈的执行
        
        Args:
            query: 原始查询
            phone_func: 手机操作函数
        
        Returns:
            自愈结果
        """
        logger.info(f"🎯 执行任务: {query}")
        
        # 1. 首次尝试
        result = phone_func(query)
        
        if result.get("success"):
            logger.info("✅ 首次执行成功")
            return SelfHealingResult(
                success=True,
                original_error="",
                healing_attempts=0,
                procedure_used=[],
                final_result=result
            )
        
        # 2. 失败后自愈
        original_error = result.get("error", "Unknown")
        logger.warning(f"⚠️ 首次执行失败: {original_error}")
        
        for attempt in range(self.max_retries):
            logger.info(f"🔄 自愈尝试 {attempt + 1}/{self.max_retries}")
            
            # 分析失败原因
            analysis = self.failure_analyzer.analyze(
                Exception(original_error),
                {"query": query}
            )
            
            logger.info(f"  错误类型: {analysis.error_type.value}")
            logger.info(f"  搜索建议: {analysis.suggested_search}")
            
            # 搜索操作流程
            procedure_result = self.procedure_searcher.search(
                analysis.suggested_search
            )
            
            # 学习流程
            guide = self.procedure_learner.learn(procedure_result)
            
            # 按流程重试
            retry_result = self.guided_retry.retry(guide, phone_func)
            
            if retry_result["success"]:
                logger.info("✅ 自愈成功")
                return SelfHealingResult(
                    success=True,
                    original_error=original_error,
                    healing_attempts=attempt + 1,
                    procedure_used=guide,
                    final_result=retry_result
                )
        
        # 3. 所有尝试失败
        logger.error("❌ 自愈失败")
        return SelfHealingResult(
            success=False,
            original_error=original_error,
            healing_attempts=self.max_retries,
            procedure_used=[],
            final_result=None
        )


# ============== 测试 ==============

def test_self_healing():
    """测试自愈机制"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          手机操作失败自愈测试                                          ║
║          失败 → 搜索流程 → 学习 → 重试                                  ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    executor = SelfHealingExecutor(max_retries=2)
    
    # 模拟手机操作函数
    call_count = [0]
    
    def mock_phone_operation(query: str) -> Dict:
        call_count[0] += 1
        
        # 前2次失败，第3次成功
        if call_count[0] < 3:
            return {"success": False, "error": "元素未找到"}
        return {"success": True, "result": "操作成功"}
    
    # 执行
    result = executor.execute_with_healing(
        query="获取商铺联系方式",
        phone_func=mock_phone_operation
    )
    
    print(f"\n📊 执行结果:")
    print(f"  成功: {result.success}")
    print(f"  原始错误: {result.original_error}")
    print(f"  自愈尝试次数: {result.healing_attempts}")
    print(f"  学习的步骤数: {len(result.procedure_used)}")
    
    if result.procedure_used:
        print(f"\n  学习的流程:")
        for step in result.procedure_used:
            print(f"    {step.index}. {step.description[:40]}...")
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    test_self_healing()

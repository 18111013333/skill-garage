"""复盘器 - V4.3.0

根据结果反向给建议
"""

from typing import Dict, List
from dataclasses import dataclass
from .result import CooperationResult

@dataclass
class ReviewInsight:
    """复盘洞察"""
    category: str           # 洞察类别
    insight: str            # 洞察内容
    suggestion: str         # 建议
    confidence: float       # 置信度

class CooperationReviewer:
    """合作复盘器"""
    
    @staticmethod
    def review(results: List[CooperationResult]) -> List[ReviewInsight]:
        """复盘分析"""
        insights = []
        
        if not results:
            return insights
        
        # 1. 哪类团长更容易合作
        insights.append(CooperationReviewer._analyze_leader_type(results))
        
        # 2. 哪种佣金方案更容易成交
        insights.append(CooperationReviewer._analyze_commission(results))
        
        # 3. 哪类产品话术更有效
        insights.append(CooperationReviewer._analyze_script(results))
        
        # 4. 下一轮优先找谁
        insights.append(CooperationReviewer._suggest_next_targets(results))
        
        return [i for i in insights if i is not None]
    
    @staticmethod
    def _analyze_leader_type(results: List[CooperationResult]) -> ReviewInsight:
        """分析哪类团长更容易合作"""
        # 统计成功率
        success_count = sum(1 for r in results if r.connection_success)
        total = len(results)
        
        if total == 0:
            return None
        
        success_rate = success_count / total
        
        if success_rate >= 0.5:
            return ReviewInsight(
                category="团长类型",
                insight=f"当前团长合作成功率 {success_rate:.1%}，表现良好",
                suggestion="继续寻找类似特征的团长",
                confidence=0.8
            )
        else:
            return ReviewInsight(
                category="团长类型",
                insight=f"当前团长合作成功率 {success_rate:.1%}，需要优化",
                suggestion="尝试调整团长筛选标准，关注粉丝数1-10万的腰部达人",
                confidence=0.7
            )
    
    @staticmethod
    def _analyze_commission(results: List[CooperationResult]) -> ReviewInsight:
        """分析佣金方案"""
        # 统计有订单的结果
        ordered = [r for r in results if r.has_order]
        
        if not ordered:
            return ReviewInsight(
                category="佣金方案",
                insight="暂无成交数据",
                suggestion="建议佣金设置在20-30%区间，提高吸引力",
                confidence=0.5
            )
        
        avg_roi = sum(r.roi for r in ordered) / len(ordered)
        
        if avg_roi >= 2.0:
            return ReviewInsight(
                category="佣金方案",
                insight=f"平均ROI {avg_roi:.1f}，佣金方案有效",
                suggestion="保持当前佣金策略",
                confidence=0.8
            )
        else:
            return ReviewInsight(
                category="佣金方案",
                insight=f"平均ROI {avg_roi:.1f}，需要优化",
                suggestion="考虑提高佣金比例或增加保底，吸引更优质团长",
                confidence=0.7
            )
    
    @staticmethod
    def _analyze_script(results: List[CooperationResult]) -> ReviewInsight:
        """分析话术效果"""
        # 统计回复率
        replied = sum(1 for r in results if r.contact_result.value in ["replied", "interested"])
        total = len(results)
        
        if total == 0:
            return None
        
        reply_rate = replied / total
        
        if reply_rate >= 0.3:
            return ReviewInsight(
                category="话术效果",
                insight=f"话术回复率 {reply_rate:.1%}，效果良好",
                suggestion="继续使用当前话术模板",
                confidence=0.7
            )
        else:
            return ReviewInsight(
                category="话术效果",
                insight=f"话术回复率 {reply_rate:.1%}，需要优化",
                suggestion="话术要更简洁，突出产品优势和佣金亮点",
                confidence=0.6
            )
    
    @staticmethod
    def _suggest_next_targets(results: List[CooperationResult]) -> ReviewInsight:
        """建议下一轮目标"""
        # 找出成功的案例
        success_leads = [r for r in results if r.connection_success and r.has_order]
        
        if success_leads:
            lead_names = [r.lead_name for r in success_leads[:3]]
            return ReviewInsight(
                category="下轮目标",
                insight=f"成功案例：{', '.join(lead_names)}",
                suggestion="优先寻找与成功案例特征相似的团长",
                confidence=0.8
            )
        else:
            return ReviewInsight(
                category="下轮目标",
                insight="暂无成功案例",
                suggestion="建议扩大线索来源，尝试不同平台和类目",
                confidence=0.5
            )

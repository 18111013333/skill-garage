"""统一评分器 - V4.3.0

所有评分使用同一套逻辑，不再各流程各打一套分
"""

from typing import Dict, List
from dataclasses import dataclass
from .lead import Lead

@dataclass
class ScoreResult:
    """评分结果"""
    match_score: float        # 匹配度分 (0-100)
    potential_score: float    # 转化潜力分 (0-100)
    cost_score: float         # 合作成本分 (0-100, 越低越好)
    risk_score: float         # 风险分 (0-100, 越低越好)
    total_score: float        # 综合优先级分 (0-100)
    priority: int             # 优先级 (1-5)

class LeadScorer:
    """统一评分器"""
    
    # 权重配置
    WEIGHTS = {
        "match": 0.3,         # 匹配度权重
        "potential": 0.35,    # 潜力权重
        "cost": 0.15,         # 成本权重
        "risk": 0.2           # 风险权重
    }
    
    @staticmethod
    def score(lead: Lead) -> ScoreResult:
        """计算线索评分"""
        # 1. 匹配度分
        match_score = lead.category_match_score * 100
        
        # 2. 转化潜力分
        potential_score = LeadScorer._calc_potential(lead)
        
        # 3. 合作成本分
        cost_score = LeadScorer._calc_cost(lead)
        
        # 4. 风险分
        risk_score = LeadScorer._calc_risk(lead)
        
        # 5. 综合分
        total_score = (
            match_score * LeadScorer.WEIGHTS["match"] +
            potential_score * LeadScorer.WEIGHTS["potential"] +
            (100 - cost_score) * LeadScorer.WEIGHTS["cost"] +
            (100 - risk_score) * LeadScorer.WEIGHTS["risk"]
        )
        
        # 6. 优先级
        if total_score >= 80:
            priority = 1
        elif total_score >= 60:
            priority = 2
        elif total_score >= 40:
            priority = 3
        elif total_score >= 20:
            priority = 4
        else:
            priority = 5
        
        return ScoreResult(
            match_score=round(match_score, 1),
            potential_score=round(potential_score, 1),
            cost_score=round(cost_score, 1),
            risk_score=round(risk_score, 1),
            total_score=round(total_score, 1),
            priority=priority
        )
    
    @staticmethod
    def _calc_potential(lead: Lead) -> float:
        """计算转化潜力"""
        score = 0.0
        
        # 粉丝数
        if lead.follower_count >= 1000000:
            score += 30
        elif lead.follower_count >= 100000:
            score += 20
        elif lead.follower_count >= 10000:
            score += 10
        
        # 平均观看
        if lead.avg_views >= 10000:
            score += 30
        elif lead.avg_views >= 1000:
            score += 20
        elif lead.avg_views >= 100:
            score += 10
        
        # 平均销量
        if lead.avg_sales >= 1000:
            score += 40
        elif lead.avg_sales >= 100:
            score += 25
        elif lead.avg_sales >= 10:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _calc_cost(lead: Lead) -> float:
        """计算合作成本"""
        score = 50.0  # 基础分
        
        # 粉丝越多成本越高
        if lead.follower_count >= 1000000:
            score += 30
        elif lead.follower_count >= 100000:
            score += 15
        
        # 已联系过成本降低
        if lead.contact_count > 0:
            score -= 10
        if lead.response_count > 0:
            score -= 15
        
        return max(0, min(score, 100))
    
    @staticmethod
    def _calc_risk(lead: Lead) -> float:
        """计算风险"""
        score = 0.0
        
        # 风险标签
        if lead.risk_tag.value == "high":
            score += 60
        elif lead.risk_tag.value == "medium":
            score += 30
        elif lead.risk_tag.value == "low":
            score += 10
        
        # 风险原因
        score += len(lead.risk_reasons) * 10
        
        return min(score, 100)

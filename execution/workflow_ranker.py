#!/usr/bin/env python3
"""
工作流优选器 - V2.8.0

对同类工作流按历史表现排序，综合考虑：
- 成功率
- 输出质量
- 稳定性
- 耗时
- fallback 频率
- 用户采纳率
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

from infrastructure.path_resolver import get_project_root

@dataclass
class WorkflowScore:
    """工作流评分"""
    workflow: str
    success_rate: float
    quality_score: float
    stability_score: float
    avg_duration_ms: int
    fallback_rate: float
    adoption_rate: float
    overall_score: float
    rank: int

class WorkflowRanker:
    """工作流优选器"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.history_path = self.project_root / 'execution' / 'workflow_history.json'
        
        # 历史数据
        self.workflow_history: Dict[str, List[Dict]] = defaultdict(list)
        
        # 权重配置
        self.weights = {
            "success_rate": 0.25,
            "quality_score": 0.25,
            "stability_score": 0.15,
            "duration_score": 0.10,  # 越短越好
            "fallback_rate": 0.10,   # 越低越好
            "adoption_rate": 0.15
        }
        
        self._load()
    
    def _load(self):
        """加载历史"""
        if self.history_path.exists():
            data = json.loads(self.history_path.read_text(encoding='utf-8'))
            for wf, history in data.get("history", {}).items():
                self.workflow_history[wf] = history
    
    def _save(self):
        """保存历史"""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "history": dict(self.workflow_history),
            "updated": datetime.now().isoformat()
        }
        self.history_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def record_execution(self, workflow: str, success: bool, quality: float,
                         duration_ms: int, fallback_triggered: bool, adopted: bool = None):
        """记录执行"""
        record = {
            "success": success,
            "quality": quality,
            "duration_ms": duration_ms,
            "fallback": fallback_triggered,
            "adopted": adopted,
            "timestamp": datetime.now().isoformat()
        }
        
        self.workflow_history[workflow].append(record)
        
        # 限制历史大小
        if len(self.workflow_history[workflow]) > 1000:
            self.workflow_history[workflow] = self.workflow_history[workflow][-1000:]
        
        self._save()
    
    def calculate_scores(self, workflow: str, days: int = 30) -> Optional[WorkflowScore]:
        """计算工作流评分"""
        history = self.workflow_history.get(workflow, [])
        
        if not history:
            return None
        
        # 过滤时间范围
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            h for h in history 
            if datetime.fromisoformat(h["timestamp"]) >= cutoff
        ]
        
        if not recent:
            return None
        
        total = len(recent)
        
        # 成功率
        success_count = sum(1 for h in recent if h["success"])
        success_rate = success_count / total
        
        # 质量分数
        quality_scores = [h["quality"] for h in recent if h.get("quality") is not None]
        quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        # 稳定性（成功率的标准差倒数）
        stability_score = success_rate  # 简化计算
        
        # 平均耗时
        durations = [h["duration_ms"] for h in recent if h.get("duration_ms")]
        avg_duration = int(sum(durations) / len(durations)) if durations else 0
        
        # Fallback 率
        fallback_count = sum(1 for h in recent if h.get("fallback"))
        fallback_rate = fallback_count / total
        
        # 采纳率
        adopted_records = [h for h in recent if h.get("adopted") is not None]
        if adopted_records:
            adopted_count = sum(1 for h in adopted_records if h["adopted"])
            adoption_rate = adopted_count / len(adopted_records)
        else:
            adoption_rate = 0.5
        
        # 综合评分
        duration_score = 1.0 - min(avg_duration / 60000, 1.0)  # 60秒为基准
        fallback_score = 1.0 - fallback_rate
        
        overall = (
            success_rate * self.weights["success_rate"] +
            quality_score * self.weights["quality_score"] +
            stability_score * self.weights["stability_score"] +
            duration_score * self.weights["duration_score"] +
            fallback_score * self.weights["fallback_rate"] +
            adoption_rate * self.weights["adoption_rate"]
        )
        
        return WorkflowScore(
            workflow=workflow,
            success_rate=success_rate,
            quality_score=quality_score,
            stability_score=stability_score,
            avg_duration_ms=avg_duration,
            fallback_rate=fallback_rate,
            adoption_rate=adoption_rate,
            overall_score=overall,
            rank=0  # 后续计算
        )
    
    def rank_workflows(self, workflows: List[str] = None, days: int = 30) -> List[WorkflowScore]:
        """排名工作流"""
        if workflows is None:
            workflows = list(self.workflow_history.keys())
        
        scores = []
        for workflow in workflows:
            score = self.calculate_scores(workflow, days)
            if score:
                scores.append(score)
        
        # 按综合评分排序
        scores.sort(key=lambda x: x.overall_score, reverse=True)
        
        # 设置排名
        for i, score in enumerate(scores):
            score.rank = i + 1
        
        return scores
    
    def select_best(self, candidate_workflows: List[str], 
                    explain: bool = False) -> Tuple[str, Optional[str]]:
        """选择最佳工作流"""
        scores = self.rank_workflows(candidate_workflows)
        
        if not scores:
            # 无历史数据，返回第一个
            return candidate_workflows[0] if candidate_workflows else "", "无历史数据，选择默认"
        
        best = scores[0]
        
        if explain:
            explanation = (
                f"选择 {best.workflow}:\n"
                f"- 成功率: {best.success_rate*100:.0f}%\n"
                f"- 质量分: {best.quality_score:.2f}\n"
                f"- 综合分: {best.overall_score:.2f}"
            )
            return best.workflow, explanation
        
        return best.workflow, None
    
    def get_fallback_chain(self, primary_workflow: str, 
                           candidate_workflows: List[str]) -> List[str]:
        """获取回退链"""
        scores = self.rank_workflows(candidate_workflows)
        
        chain = [primary_workflow]
        for score in scores:
            if score.workflow != primary_workflow:
                chain.append(score.workflow)
        
        return chain
    
    def get_report(self) -> str:
        """生成报告"""
        scores = self.rank_workflows()
        
        lines = [
            "# 工作流优选报告",
            "",
            "## 排名",
            "",
            "| 排名 | 工作流 | 成功率 | 质量分 | 耗时 | Fallback率 | 综合分 |",
            "|------|--------|--------|--------|------|------------|--------|"
        ]
        
        for score in scores[:20]:
            lines.append(
                f"| {score.rank} | {score.workflow} | "
                f"{score.success_rate*100:.0f}% | "
                f"{score.quality_score:.2f} | "
                f"{score.avg_duration_ms}ms | "
                f"{score.fallback_rate*100:.0f}% | "
                f"{score.overall_score:.2f} |"
            )
        
        return "\n".join(lines)

# 全局实例
_workflow_ranker = None

def get_workflow_ranker() -> WorkflowRanker:
    global _workflow_ranker
    if _workflow_ranker is None:
        _workflow_ranker = WorkflowRanker()
    return _workflow_ranker

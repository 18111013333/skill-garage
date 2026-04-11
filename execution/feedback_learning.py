#!/usr/bin/env python3
"""
反馈学习引擎 - V2.8.0

记录并学习：
- 哪类输出被直接采用
- 哪类输出被重写
- 哪类任务经常补问
- 哪类产物经常返工
- 用户偏好的格式、结构、粒度

反馈必须反哺：
- 路由策略
- 输出模板
- 工作流顺序
- 校验规则
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict
from enum import Enum

from infrastructure.path_resolver import get_project_root

class FeedbackType(Enum):
    ADOPTED = "adopted"           # 直接采用
    REWRITTEN = "rewritten"       # 被重写
    CLARIFICATION = "clarification"  # 需要补问
    REWORK = "rework"             # 需要返工
    PREFERRED = "preferred"       # 用户偏好

@dataclass
class FeedbackRecord:
    """反馈记录"""
    feedback_id: str
    task_id: str
    task_name: str
    workflow: str
    feedback_type: str
    output_format: str
    output_structure: str
    granularity: str
    details: Dict[str, Any]
    timestamp: str

@dataclass
class LearningRule:
    """学习规则"""
    rule_id: str
    rule_type: str  # routing, template, workflow, validation
    condition: str
    action: str
    confidence: float
    source_feedbacks: List[str]
    created_at: str
    updated_at: str

class FeedbackLearningEngine:
    """反馈学习引擎"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.feedback_path = self.project_root / 'execution' / 'feedback.json'
        self.rules_path = self.project_root / 'execution' / 'learning_rules.json'
        
        self.feedbacks: List[FeedbackRecord] = []
        self.rules: Dict[str, LearningRule] = {}
        
        # 学习统计
        self.format_preferences: Dict[str, int] = defaultdict(int)
        self.structure_preferences: Dict[str, int] = defaultdict(int)
        self.granularity_preferences: Dict[str, int] = defaultdict(int)
        self.workflow_performance: Dict[str, Dict] = defaultdict(lambda: {"adopted": 0, "rewritten": 0})
        
        self._load()
    
    def _load(self):
        """加载数据"""
        if self.feedback_path.exists():
            data = json.loads(self.feedback_path.read_text(encoding='utf-8'))
            self.feedbacks = [FeedbackRecord(**f) for f in data.get("feedbacks", [])]
        
        if self.rules_path.exists():
            data = json.loads(self.rules_path.read_text(encoding='utf-8'))
            for rule_data in data.get("rules", []):
                rule = LearningRule(**rule_data)
                self.rules[rule.rule_id] = rule
        
        # 重建统计
        self._rebuild_stats()
    
    def _save(self):
        """保存数据"""
        self.feedback_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.feedback_path.write_text(
            json.dumps({"feedbacks": [asdict(f) for f in self.feedbacks]}, 
                      indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        self.rules_path.write_text(
            json.dumps({"rules": [asdict(r) for r in self.rules.values()]},
                      indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def _rebuild_stats(self):
        """重建统计"""
        for feedback in self.feedbacks:
            self.format_preferences[feedback.output_format] += 1
            self.structure_preferences[feedback.output_structure] += 1
            self.granularity_preferences[feedback.granularity] += 1
            
            if feedback.feedback_type == FeedbackType.ADOPTED.value:
                self.workflow_performance[feedback.workflow]["adopted"] += 1
            elif feedback.feedback_type == FeedbackType.REWRITTEN.value:
                self.workflow_performance[feedback.workflow]["rewritten"] += 1
    
    def record_feedback(self, task_id: str, task_name: str, workflow: str,
                        feedback_type: str, output_format: str = "markdown",
                        output_structure: str = "standard",
                        granularity: str = "medium",
                        details: Dict = None) -> FeedbackRecord:
        """记录反馈"""
        feedback_id = f"fb_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        feedback = FeedbackRecord(
            feedback_id=feedback_id,
            task_id=task_id,
            task_name=task_name,
            workflow=workflow,
            feedback_type=feedback_type,
            output_format=output_format,
            output_structure=output_structure,
            granularity=granularity,
            details=details or {},
            timestamp=datetime.now().isoformat()
        )
        
        self.feedbacks.append(feedback)
        
        # 更新统计
        self.format_preferences[output_format] += 1
        self.structure_preferences[output_structure] += 1
        self.granularity_preferences[granularity] += 1
        
        if feedback_type == FeedbackType.ADOPTED.value:
            self.workflow_performance[workflow]["adopted"] += 1
        elif feedback_type == FeedbackType.REWRITTEN.value:
            self.workflow_performance[workflow]["rewritten"] += 1
        
        # 触发学习
        self._learn_from_feedback(feedback)
        
        # 限制历史大小
        if len(self.feedbacks) > 5000:
            self.feedbacks = self.feedbacks[-5000:]
        
        self._save()
        
        return feedback
    
    def _learn_from_feedback(self, feedback: FeedbackRecord):
        """从反馈中学习"""
        # 学习规则类型
        rule_type = None
        condition = ""
        action = ""
        
        if feedback.feedback_type == FeedbackType.ADOPTED.value:
            # 采用的输出格式/结构 -> 更新模板偏好
            rule_type = "template"
            condition = f"task_type={feedback.task_name}"
            action = f"prefer_format={feedback.output_format},structure={feedback.output_structure}"
        
        elif feedback.feedback_type == FeedbackType.REWRITTEN.value:
            # 被重写 -> 降低该工作流优先级
            rule_type = "routing"
            condition = f"task_type={feedback.task_name}"
            action = f"deprioritize_workflow={feedback.workflow}"
        
        elif feedback.feedback_type == FeedbackType.CLARIFICATION.value:
            # 需要补问 -> 增加前置确认
            rule_type = "validation"
            condition = f"task_type={feedback.task_name}"
            action = "add_pre_check=clarify_requirements"
        
        elif feedback.feedback_type == FeedbackType.REWORK.value:
            # 需要返工 -> 标记问题工作流
            rule_type = "workflow"
            condition = f"workflow={feedback.workflow}"
            action = "flag_for_review"
        
        if rule_type:
            rule_id = f"rule_{rule_type}_{hash(condition) % 10000}"
            
            if rule_id in self.rules:
                # 更新现有规则
                rule = self.rules[rule_id]
                rule.confidence = min(1.0, rule.confidence + 0.1)
                rule.source_feedbacks.append(feedback.feedback_id)
                rule.updated_at = datetime.now().isoformat()
            else:
                # 创建新规则
                self.rules[rule_id] = LearningRule(
                    rule_id=rule_id,
                    rule_type=rule_type,
                    condition=condition,
                    action=action,
                    confidence=0.5,
                    source_feedbacks=[feedback.feedback_id],
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat()
                )
    
    def get_preferred_format(self) -> str:
        """获取偏好格式"""
        if not self.format_preferences:
            return "markdown"
        return max(self.format_preferences.items(), key=lambda x: x[1])[0]
    
    def get_preferred_structure(self) -> str:
        """获取偏好结构"""
        if not self.structure_preferences:
            return "standard"
        return max(self.structure_preferences.items(), key=lambda x: x[1])[0]
    
    def get_preferred_granularity(self) -> str:
        """获取偏好粒度"""
        if not self.granularity_preferences:
            return "medium"
        return max(self.granularity_preferences.items(), key=lambda x: x[1])[0]
    
    def get_workflow_ranking(self) -> List[Dict]:
        """获取工作流排名（按采纳率）"""
        rankings = []
        
        for workflow, stats in self.workflow_performance.items():
            total = stats["adopted"] + stats["rewritten"]
            if total > 0:
                adoption_rate = stats["adopted"] / total
                rankings.append({
                    "workflow": workflow,
                    "adoption_rate": adoption_rate,
                    "total_feedbacks": total
                })
        
        return sorted(rankings, key=lambda x: x["adoption_rate"], reverse=True)
    
    def get_applicable_rules(self, task_name: str, workflow: str = None) -> List[LearningRule]:
        """获取适用规则"""
        applicable = []
        
        for rule in self.rules.values():
            if f"task_type={task_name}" in rule.condition:
                applicable.append(rule)
            elif workflow and f"workflow={workflow}" in rule.condition:
                applicable.append(rule)
        
        return sorted(applicable, key=lambda x: x.confidence, reverse=True)
    
    def get_report(self) -> str:
        """生成报告"""
        lines = [
            "# 反馈学习报告",
            "",
            "## 用户偏好",
            "",
            f"- 偏好格式: {self.get_preferred_format()}",
            f"- 偏好结构: {self.get_preferred_structure()}",
            f"- 偏好粒度: {self.get_preferred_granularity()}",
            "",
            "## 工作流排名（按采纳率）",
            ""
        ]
        
        for rank in self.get_workflow_ranking()[:10]:
            lines.append(f"- {rank['workflow']}: {rank['adoption_rate']*100:.0f}% ({rank['total_feedbacks']}次反馈)")
        
        lines.extend([
            "",
            "## 学习规则",
            ""
        ])
        
        for rule in list(self.rules.values())[:10]:
            lines.append(f"- [{rule.rule_type}] {rule.condition} -> {rule.action} (置信度: {rule.confidence:.0%})")
        
        return "\n".join(lines)

# 全局实例
_feedback_engine = None

def get_feedback_engine() -> FeedbackLearningEngine:
    global _feedback_engine
    if _feedback_engine is None:
        _feedback_engine = FeedbackLearningEngine()
    return _feedback_engine

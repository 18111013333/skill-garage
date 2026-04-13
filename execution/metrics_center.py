#!/usr/bin/env python3
"""
统一指标中心 - V2.8.0

统计指标：
- 任务完成率
- 输出合格率
- 产物可直接使用率
- fallback 触发率
- 平均耗时
- 人工二次修改率
- 用户采纳率
- 失败类型分布
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from collections import defaultdict
from enum import Enum

from infrastructure.path_resolver import get_project_root

class MetricType(Enum):
    COMPLETION_RATE = "completion_rate"
    QUALIFIED_RATE = "qualified_rate"
    DIRECTLY_USABLE_RATE = "directly_usable_rate"
    FALLBACK_RATE = "fallback_rate"
    AVG_DURATION = "avg_duration"
    MODIFICATION_RATE = "modification_rate"
    ADOPTION_RATE = "adoption_rate"
    FAILURE_DISTRIBUTION = "failure_distribution"

@dataclass
class TaskMetric:
    """任务指标"""
    task_id: str
    task_name: str
    workflow: str
    project: str
    completed: bool
    qualified: bool
    directly_usable: bool
    fallback_triggered: bool
    duration_ms: int
    modified: bool
    adopted: bool
    failure_type: Optional[str]
    timestamp: str

@dataclass
class AggregatedMetrics:
    """聚合指标"""
    period: str
    total_tasks: int
    completion_rate: float
    qualified_rate: float
    directly_usable_rate: float
    fallback_rate: float
    avg_duration_ms: int
    modification_rate: float
    adoption_rate: float
    failure_distribution: Dict[str, int]

class MetricsCenter:
    """统一指标中心"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.metrics_path = self.project_root / 'execution' / 'metrics.json'
        
        self.task_metrics: List[TaskMetric] = []
        self._load()
    
    def _load(self):
        """加载指标"""
        if self.metrics_path.exists():
            data = json.loads(self.metrics_path.read_text(encoding='utf-8'))
            self.task_metrics = [TaskMetric(**m) for m in data.get("metrics", [])]
    
    def _save(self):
        """保存指标"""
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "metrics": [asdict(m) for m in self.task_metrics],
            "updated": datetime.now().isoformat()
        }
        self.metrics_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def record_task(self, task_id: str, task_name: str, workflow: str,
                    project: str, completed: bool, qualified: bool,
                    directly_usable: bool, fallback_triggered: bool,
                    duration_ms: int, failure_type: str = None) -> TaskMetric:
        """记录任务指标"""
        metric = TaskMetric(
            task_id=task_id,
            task_name=task_name,
            workflow=workflow,
            project=project,
            completed=completed,
            qualified=qualified,
            directly_usable=directly_usable,
            fallback_triggered=fallback_triggered,
            duration_ms=duration_ms,
            modified=False,  # 初始未修改
            adopted=False,   # 初始未采纳
            failure_type=failure_type,
            timestamp=datetime.now().isoformat()
        )
        
        self.task_metrics.append(metric)
        
        # 限制历史大小
        if len(self.task_metrics) > 10000:
            self.task_metrics = self.task_metrics[-10000:]
        
        self._save()
        
        return metric
    
    def mark_modified(self, task_id: str):
        """标记为已修改"""
        for metric in self.task_metrics:
            if metric.task_id == task_id:
                metric.modified = True
                self._save()
                break
    
    def mark_adopted(self, task_id: str):
        """标记为已采纳"""
        for metric in self.task_metrics:
            if metric.task_id == task_id:
                metric.adopted = True
                self._save()
                break
    
    def aggregate(self, period: str = "all", workflow: str = None,
                  project: str = None) -> AggregatedMetrics:
        """聚合指标"""
        # 过滤数据
        metrics = self.task_metrics
        
        if period != "all":
            now = datetime.now()
            if period == "today":
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "week":
                start = now - timedelta(days=7)
            elif period == "month":
                start = now - timedelta(days=30)
            else:
                start = now - timedelta(days=1)
            
            metrics = [
                m for m in metrics 
                if datetime.fromisoformat(m.timestamp) >= start
            ]
        
        if workflow:
            metrics = [m for m in metrics if m.workflow == workflow]
        
        if project:
            metrics = [m for m in metrics if m.project == project]
        
        # 计算指标
        total = len(metrics)
        if total == 0:
            return AggregatedMetrics(
                period=period,
                total_tasks=0,
                completion_rate=0,
                qualified_rate=0,
                directly_usable_rate=0,
                fallback_rate=0,
                avg_duration_ms=0,
                modification_rate=0,
                adoption_rate=0,
                failure_distribution={}
            )
        
        completed = sum(1 for m in metrics if m.completed)
        qualified = sum(1 for m in metrics if m.qualified)
        usable = sum(1 for m in metrics if m.directly_usable)
        fallback = sum(1 for m in metrics if m.fallback_triggered)
        modified = sum(1 for m in metrics if m.modified)
        adopted = sum(1 for m in metrics if m.adopted)
        
        # 失败类型分布
        failure_dist = defaultdict(int)
        for m in metrics:
            if m.failure_type:
                failure_dist[m.failure_type] += 1
        
        return AggregatedMetrics(
            period=period,
            total_tasks=total,
            completion_rate=completed / total,
            qualified_rate=qualified / total,
            directly_usable_rate=usable / total,
            fallback_rate=fallback / total,
            avg_duration_ms=int(sum(m.duration_ms for m in metrics) / total),
            modification_rate=modified / total,
            adoption_rate=adopted / total,
            failure_distribution=dict(failure_dist)
        )
    
    def get_by_workflow(self) -> Dict[str, Dict]:
        """按工作流统计"""
        workflow_metrics = defaultdict(list)
        
        for metric in self.task_metrics:
            workflow_metrics[metric.workflow].append(metric)
        
        result = {}
        for workflow, metrics in workflow_metrics.items():
            total = len(metrics)
            result[workflow] = {
                "total": total,
                "completion_rate": sum(1 for m in metrics if m.completed) / total,
                "qualified_rate": sum(1 for m in metrics if m.qualified) / total,
                "avg_duration_ms": int(sum(m.duration_ms for m in metrics) / total)
            }
        
        return result
    
    def get_by_project(self) -> Dict[str, Dict]:
        """按项目统计"""
        project_metrics = defaultdict(list)
        
        for metric in self.task_metrics:
            project_metrics[metric.project].append(metric)
        
        result = {}
        for project, metrics in project_metrics.items():
            total = len(metrics)
            result[project] = {
                "total": total,
                "completion_rate": sum(1 for m in metrics if m.completed) / total,
                "qualified_rate": sum(1 for m in metrics if m.qualified) / total
            }
        
        return result
    
    def get_report(self, period: str = "all") -> str:
        """生成报告"""
        agg = self.aggregate(period)
        
        lines = [
            f"# 指标报告 ({period})",
            "",
            "## 总览",
            "",
            f"- 总任务数: {agg.total_tasks}",
            f"- 完成率: {agg.completion_rate*100:.1f}%",
            f"- 合格率: {agg.qualified_rate*100:.1f}%",
            f"- 可直接使用率: {agg.directly_usable_rate*100:.1f}%",
            f"- Fallback 触发率: {agg.fallback_rate*100:.1f}%",
            f"- 平均耗时: {agg.avg_duration_ms}ms",
            f"- 修改率: {agg.modification_rate*100:.1f}%",
            f"- 采纳率: {agg.adoption_rate*100:.1f}%",
            "",
            "## 失败类型分布",
            ""
        ]
        
        if agg.failure_distribution:
            for ftype, count in sorted(agg.failure_distribution.items(), 
                                       key=lambda x: x[1], reverse=True):
                lines.append(f"- {ftype}: {count}")
        else:
            lines.append("- 无失败记录")
        
        # 按工作流统计
        by_workflow = self.get_by_workflow()
        if by_workflow:
            lines.extend([
                "",
                "## 按工作流",
                ""
            ])
            for wf, stats in sorted(by_workflow.items(), 
                                    key=lambda x: x[1]["completion_rate"], reverse=True):
                lines.append(f"- {wf}: 完成率 {stats['completion_rate']*100:.0f}%, "
                           f"合格率 {stats['qualified_rate']*100:.0f}%")
        
        return "\n".join(lines)

# 全局实例
_metrics_center = None

def get_metrics_center() -> MetricsCenter:
    global _metrics_center
    if _metrics_center is None:
        _metrics_center = MetricsCenter()
    return _metrics_center

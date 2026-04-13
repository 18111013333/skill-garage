#!/usr/bin/env python3
"""
任务复盘器 - V2.8.0

检查：
- 哪一步最慢
- 哪一步最容易失败
- 哪个技能最常失效
- 哪类任务成功率最低
- 哪类输出最容易不合格
- 哪些 fallback 经常被触发
- 哪些工作流需要重构

输出：
- 本次任务复盘
- 工作流健康度
- 技能稳定性排行
- 高频失败点清单
- 优化建议
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

from infrastructure.path_resolver import get_project_root

@dataclass
class TaskExecution:
    """任务执行记录"""
    task_id: str
    task_name: str
    workflow: str
    start_time: str
    end_time: str
    duration_ms: int
    success: bool
    steps: List[Dict]
    quality_score: float
    fallback_count: int
    error: Optional[str]

@dataclass
class WorkflowHealth:
    """工作流健康度"""
    name: str
    total_executions: int
    success_count: int
    avg_duration_ms: int
    avg_quality: float
    fallback_rate: float
    health_score: float

@dataclass
class SkillStability:
    """技能稳定性"""
    name: str
    total_calls: int
    success_count: int
    failure_count: int
    stability_score: float

class TaskReviewer:
    """任务复盘器"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.review_path = self.project_root / 'execution' / 'task_reviews.json'
        
        self.executions: List[TaskExecution] = []
        self._load()
    
    def _load(self):
        """加载记录"""
        if self.review_path.exists():
            data = json.loads(self.review_path.read_text(encoding='utf-8'))
            self.executions = [TaskExecution(**e) for e in data.get("executions", [])]
    
    def _save(self):
        """保存记录"""
        self.review_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "executions": [asdict(e) for e in self.executions],
            "updated": datetime.now().isoformat()
        }
        self.review_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def record_execution(self, task_name: str, workflow: str,
                         steps: List[Dict], quality_score: float,
                         success: bool, error: str = None) -> str:
        """记录执行"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # 计算时长
        start_times = [s.get("start_time") for s in steps if s.get("start_time")]
        end_times = [s.get("end_time") for s in steps if s.get("end_time")]
        
        if start_times and end_times:
            start = datetime.fromisoformat(min(start_times))
            end = datetime.fromisoformat(max(end_times))
            duration_ms = int((end - start).total_seconds() * 1000)
        else:
            duration_ms = 0
        
        # 计算 fallback 次数
        fallback_count = sum(1 for s in steps if s.get("fallback_used"))
        
        execution = TaskExecution(
            task_id=task_id,
            task_name=task_name,
            workflow=workflow,
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            duration_ms=duration_ms,
            success=success,
            steps=steps,
            quality_score=quality_score,
            fallback_count=fallback_count,
            error=error
        )
        
        self.executions.append(execution)
        
        # 限制历史大小
        if len(self.executions) > 1000:
            self.executions = self.executions[-1000:]
        
        self._save()
        
        return task_id
    
    def get_slowest_steps(self, limit: int = 5) -> List[Dict]:
        """获取最慢的步骤"""
        step_durations = defaultdict(list)
        
        for execution in self.executions:
            for step in execution.steps:
                if step.get("start_time") and step.get("end_time"):
                    start = datetime.fromisoformat(step["start_time"])
                    end = datetime.fromisoformat(step["end_time"])
                    duration = (end - start).total_seconds()
                    step_durations[step["name"]].append(duration)
        
        avg_durations = {
            name: sum(durations) / len(durations)
            for name, durations in step_durations.items()
        }
        
        sorted_steps = sorted(avg_durations.items(), key=lambda x: x[1], reverse=True)
        
        return [{"step": name, "avg_duration": duration} for name, duration in sorted_steps[:limit]]
    
    def get_most_failed_steps(self, limit: int = 5) -> List[Dict]:
        """获取最容易失败的步骤"""
        step_failures = defaultdict(lambda: {"total": 0, "failed": 0})
        
        for execution in self.executions:
            for step in execution.steps:
                step_failures[step["name"]]["total"] += 1
                if step.get("status") == "failed":
                    step_failures[step["name"]]["failed"] += 1
        
        failure_rates = {
            name: data["failed"] / max(data["total"], 1)
            for name, data in step_failures.items()
        }
        
        sorted_steps = sorted(failure_rates.items(), key=lambda x: x[1], reverse=True)
        
        return [{"step": name, "failure_rate": rate} for name, rate in sorted_steps[:limit]]
    
    def get_unstable_skills(self, limit: int = 5) -> List[SkillStability]:
        """获取最不稳定的技能"""
        skill_stats = defaultdict(lambda: {"total": 0, "success": 0, "failed": 0})
        
        for execution in self.executions:
            for step in execution.steps:
                skill = step.get("skill")
                if skill:
                    skill_stats[skill]["total"] += 1
                    if step.get("status") == "success":
                        skill_stats[skill]["success"] += 1
                    else:
                        skill_stats[skill]["failed"] += 1
        
        stabilities = []
        for name, stats in skill_stats.items():
            stability = SkillStability(
                name=name,
                total_calls=stats["total"],
                success_count=stats["success"],
                failure_count=stats["failed"],
                stability_score=stats["success"] / max(stats["total"], 1)
            )
            stabilities.append(stability)
        
        return sorted(stabilities, key=lambda x: x.stability_score)[:limit]
    
    def get_workflow_health(self) -> List[WorkflowHealth]:
        """获取工作流健康度"""
        workflow_stats = defaultdict(lambda: {
            "total": 0, "success": 0, "durations": [], 
            "qualities": [], "fallbacks": 0
        })
        
        for execution in self.executions:
            stats = workflow_stats[execution.workflow]
            stats["total"] += 1
            if execution.success:
                stats["success"] += 1
            stats["durations"].append(execution.duration_ms)
            stats["qualities"].append(execution.quality_score)
            stats["fallbacks"] += execution.fallback_count
        
        healths = []
        for name, stats in workflow_stats.items():
            avg_duration = sum(stats["durations"]) / max(len(stats["durations"]), 1)
            avg_quality = sum(stats["qualities"]) / max(len(stats["qualities"]), 1)
            fallback_rate = stats["fallbacks"] / max(stats["total"], 1)
            
            # 健康度 = 成功率 * 0.4 + 质量 * 0.4 + (1 - fallback率) * 0.2
            success_rate = stats["success"] / max(stats["total"], 1)
            health_score = success_rate * 0.4 + avg_quality * 0.4 + (1 - fallback_rate) * 0.2
            
            health = WorkflowHealth(
                name=name,
                total_executions=stats["total"],
                success_count=stats["success"],
                avg_duration_ms=int(avg_duration),
                avg_quality=avg_quality,
                fallback_rate=fallback_rate,
                health_score=health_score
            )
            healths.append(health)
        
        return sorted(healths, key=lambda x: x.health_score, reverse=True)
    
    def get_lowest_success_tasks(self, limit: int = 5) -> List[Dict]:
        """获取成功率最低的任务类型"""
        task_stats = defaultdict(lambda: {"total": 0, "success": 0})
        
        for execution in self.executions:
            task_stats[execution.task_name]["total"] += 1
            if execution.success:
                task_stats[execution.task_name]["success"] += 1
        
        success_rates = {
            name: data["success"] / max(data["total"], 1)
            for name, data in task_stats.items()
        }
        
        sorted_tasks = sorted(success_rates.items(), key=lambda x: x[1])
        
        return [{"task": name, "success_rate": rate} for name, rate in sorted_tasks[:limit]]
    
    def get_frequent_fallbacks(self, limit: int = 5) -> List[Dict]:
        """获取经常触发的 fallback"""
        fallback_counts = defaultdict(int)
        
        for execution in self.executions:
            for step in execution.steps:
                if step.get("fallback_used"):
                    fallback_counts[step["name"]] += 1
        
        sorted_fallbacks = sorted(fallback_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [{"step": name, "count": count} for name, count in sorted_fallbacks[:limit]]
    
    def generate_optimization_suggestions(self) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 检查慢步骤
        slow_steps = self.get_slowest_steps(3)
        for step in slow_steps:
            if step["avg_duration"] > 5:  # 超过5秒
                suggestions.append(f"优化步骤 '{step['step']}' 的性能，平均耗时 {step['avg_duration']:.1f}秒")
        
        # 检查失败步骤
        failed_steps = self.get_most_failed_steps(3)
        for step in failed_steps:
            if step["failure_rate"] > 0.2:  # 失败率超过20%
                suggestions.append(f"改进步骤 '{step['step']}' 的稳定性，失败率 {step['failure_rate']*100:.0f}%")
        
        # 检查不稳定技能
        unstable_skills = self.get_unstable_skills(3)
        for skill in unstable_skills:
            if skill.stability_score < 0.8:
                suggestions.append(f"检查技能 '{skill.name}' 的可用性，稳定性 {skill.stability_score*100:.0f}%")
        
        # 检查工作流健康度
        workflow_healths = self.get_workflow_health()
        for health in workflow_healths:
            if health.health_score < 0.7:
                suggestions.append(f"重构工作流 '{health.name}'，健康度 {health.health_score*100:.0f}%")
        
        return suggestions
    
    def review_task(self, task_id: str) -> Dict[str, Any]:
        """复盘单个任务"""
        execution = next((e for e in self.executions if e.task_id == task_id), None)
        
        if not execution:
            return {"error": "任务不存在"}
        
        return {
            "task_id": task_id,
            "task_name": execution.task_name,
            "workflow": execution.workflow,
            "success": execution.success,
            "duration_ms": execution.duration_ms,
            "quality_score": execution.quality_score,
            "fallback_count": execution.fallback_count,
            "error": execution.error,
            "steps_summary": [
                {
                    "name": s["name"],
                    "status": s["status"],
                    "fallback_used": s.get("fallback_used", False)
                }
                for s in execution.steps
            ]
        }
    
    def get_full_report(self) -> str:
        """生成完整复盘报告"""
        lines = [
            "# 任务复盘报告",
            "",
            f"**统计周期**: 最近 {len(self.executions)} 次执行",
            "",
            "## 工作流健康度",
            ""
        ]
        
        for health in self.get_workflow_health():
            status = "✅" if health.health_score >= 0.8 else "⚠️" if health.health_score >= 0.6 else "❌"
            lines.append(f"- {status} {health.name}: {health.health_score*100:.0f}% (执行{health.total_executions}次)")
        
        lines.extend([
            "",
            "## 最慢步骤 TOP 5",
            ""
        ])
        
        for step in self.get_slowest_steps():
            lines.append(f"- {step['step']}: {step['avg_duration']:.2f}秒")
        
        lines.extend([
            "",
            "## 最易失败步骤 TOP 5",
            ""
        ])
        
        for step in self.get_most_failed_steps():
            lines.append(f"- {step['step']}: {step['failure_rate']*100:.0f}%")
        
        lines.extend([
            "",
            "## 不稳定技能 TOP 5",
            ""
        ])
        
        for skill in self.get_unstable_skills():
            lines.append(f"- {skill.name}: 稳定性 {skill.stability_score*100:.0f}%")
        
        lines.extend([
            "",
            "## 高频 Fallback",
            ""
        ])
        
        for fb in self.get_frequent_fallbacks():
            lines.append(f"- {fb['step']}: {fb['count']}次")
        
        suggestions = self.generate_optimization_suggestions()
        if suggestions:
            lines.extend([
                "",
                "## 优化建议",
                ""
            ])
            for s in suggestions:
                lines.append(f"- {s}")
        
        return "\n".join(lines)

# 全局实例
_reviewer = None

def get_task_reviewer() -> TaskReviewer:
    global _reviewer
    if _reviewer is None:
        _reviewer = TaskReviewer()
    return _reviewer

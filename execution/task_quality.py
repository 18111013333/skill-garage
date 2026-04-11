#!/usr/bin/env python3
"""
任务质量评估系统 - V2.8.0

两个层次：
A. 过程质量评估
B. 结果质量评估

质量评级：
- excellent: 优秀
- qualified: 合格
- weak: 较弱
- failed: 失败
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class QualityLevel(Enum):
    EXCELLENT = "excellent"
    QUALIFIED = "qualified"
    WEAK = "weak"
    FAILED = "failed"

@dataclass
class ProcessQualityResult:
    """过程质量结果"""
    followed_correct_flow: bool
    missing_steps: List[str]
    wrong_skill_calls: List[str]
    fallback_overuse: bool
    route_deviation: bool
    degraded_without_notice: bool
    score: float
    issues: List[str]

@dataclass
class ResultQualityResult:
    """结果质量结果"""
    output_not_empty: bool
    format_correct: bool
    has_required_fields: bool
    no_conflicts: bool
    not_vague: bool
    directly_usable: bool
    files_generated: bool
    score: float
    issues: List[str]

@dataclass
class TaskQualityReport:
    """任务质量报告"""
    task_name: str
    timestamp: str
    process_quality: Dict
    result_quality: Dict
    overall_level: str
    overall_score: float
    failure_reason: Optional[str]
    fix_suggestions: List[str]

class TaskQualityEvaluator:
    """任务质量评估器"""
    
    def __init__(self):
        self.history: List[TaskQualityReport] = []
    
    def evaluate_process(self, workflow_result: Dict) -> ProcessQualityResult:
        """评估过程质量"""
        issues = []
        score = 1.0
        
        # 1. 是否按正确流程执行
        steps = workflow_result.get("steps", [])
        expected_order = workflow_result.get("expected_order", [])
        
        followed_correct_flow = True
        missing_steps = []
        
        if expected_order:
            executed_steps = [s["name"] for s in steps if s["status"] == "success"]
            for expected in expected_order:
                if expected not in executed_steps:
                    missing_steps.append(expected)
                    followed_correct_flow = False
        
        if missing_steps:
            issues.append(f"遗漏步骤: {missing_steps}")
            score -= 0.2
        
        # 2. 是否错误调用技能
        wrong_skill_calls = []
        for step in steps:
            if step.get("status") == "failed" and step.get("skill"):
                wrong_skill_calls.append(step["skill"])
        
        if wrong_skill_calls:
            issues.append(f"技能调用失败: {wrong_skill_calls}")
            score -= 0.1 * len(wrong_skill_calls)
        
        # 3. fallback 是否过度触发
        fallback_count = sum(1 for s in steps if s.get("fallback_used"))
        fallback_overuse = fallback_count > len(steps) * 0.3
        
        if fallback_overuse:
            issues.append(f"回退过度触发: {fallback_count}次")
            score -= 0.15
        
        # 4. 路由是否偏离
        route_deviation = workflow_result.get("route_deviation", False)
        if route_deviation:
            issues.append("路由偏离目标任务")
            score -= 0.1
        
        # 5. 是否中途降级但未标注
        degraded_without_notice = False
        if workflow_result.get("status") == "completed":
            if any(s.get("fallback_used") for s in steps):
                if not workflow_result.get("degraded_notice"):
                    degraded_without_notice = True
                    issues.append("任务降级但未标注")
                    score -= 0.1
        
        return ProcessQualityResult(
            followed_correct_flow=followed_correct_flow,
            missing_steps=missing_steps,
            wrong_skill_calls=wrong_skill_calls,
            fallback_overuse=fallback_overuse,
            route_deviation=route_deviation,
            degraded_without_notice=degraded_without_notice,
            score=max(0, score),
            issues=issues
        )
    
    def evaluate_result(self, output: Dict, expected_template: Dict = None) -> ResultQualityResult:
        """评估结果质量"""
        issues = []
        score = 1.0
        
        # 1. 输出是否为空
        output_not_empty = bool(output)
        if not output_not_empty:
            issues.append("输出为空")
            return ResultQualityResult(
                output_not_empty=False,
                format_correct=False,
                has_required_fields=False,
                no_conflicts=True,
                not_vague=False,
                directly_usable=False,
                files_generated=False,
                score=0,
                issues=issues
            )
        
        # 2. 格式是否正确
        format_correct = isinstance(output, dict)
        if not format_correct:
            issues.append("输出格式不正确")
            score -= 0.2
        
        # 3. 是否缺少关键字段
        has_required_fields = True
        if expected_template:
            for key in expected_template.keys():
                if key not in output:
                    has_required_fields = False
                    issues.append(f"缺少字段: {key}")
        
        if not has_required_fields:
            score -= 0.2
        
        # 4. 是否存在冲突
        no_conflicts = True  # 简化检查
        
        # 5. 是否只是空泛建议
        not_vague = True
        output_str = str(output)
        vague_phrases = ["建议", "可以考虑", "可能", "也许"]
        vague_count = sum(1 for p in vague_phrases if p in output_str)
        if vague_count > 3:
            not_vague = False
            issues.append("输出过于空泛")
            score -= 0.1
        
        # 6. 是否达到"可直接使用"标准
        directly_usable = (
            output_not_empty and 
            format_correct and 
            has_required_fields and
            not_vague
        )
        
        # 7. 文件是否生成
        files_generated = bool(output.get("report_file") or output.get("files"))
        if not files_generated and expected_template and "report_file" in expected_template:
            issues.append("未生成文件产物")
            score -= 0.1
        
        return ResultQualityResult(
            output_not_empty=output_not_empty,
            format_correct=format_correct,
            has_required_fields=has_required_fields,
            no_conflicts=no_conflicts,
            not_vague=not_vague,
            directly_usable=directly_usable,
            files_generated=files_generated,
            score=max(0, score),
            issues=issues
        )
    
    def determine_level(self, process_score: float, result_score: float) -> str:
        """确定质量等级"""
        overall = (process_score + result_score) / 2
        
        if overall >= 0.9:
            return QualityLevel.EXCELLENT.value
        elif overall >= 0.7:
            return QualityLevel.QUALIFIED.value
        elif overall >= 0.5:
            return QualityLevel.WEAK.value
        else:
            return QualityLevel.FAILED.value
    
    def generate_fix_suggestions(self, process_issues: List[str], result_issues: List[str]) -> List[str]:
        """生成修复建议"""
        suggestions = []
        
        for issue in process_issues:
            if "遗漏步骤" in issue:
                suggestions.append("检查工作流配置，确保所有必要步骤都被执行")
            elif "技能调用失败" in issue:
                suggestions.append("检查技能是否正确安装和配置")
            elif "回退过度触发" in issue:
                suggestions.append("优化主流程稳定性，减少对回退的依赖")
        
        for issue in result_issues:
            if "输出为空" in issue:
                suggestions.append("检查执行逻辑，确保有有效输出")
            elif "缺少字段" in issue:
                suggestions.append("完善输出模板，确保包含所有必要字段")
            elif "未生成文件" in issue:
                suggestions.append("添加文件生成步骤")
        
        return suggestions
    
    def evaluate(self, task_name: str, workflow_result: Dict, 
                 expected_template: Dict = None) -> TaskQualityReport:
        """完整评估"""
        process = self.evaluate_process(workflow_result)
        result = self.evaluate_result(workflow_result.get("output", {}), expected_template)
        
        level = self.determine_level(process.score, result.score)
        suggestions = self.generate_fix_suggestions(process.issues, result.issues)
        
        report = TaskQualityReport(
            task_name=task_name,
            timestamp=datetime.now().isoformat(),
            process_quality=asdict(process),
            result_quality=asdict(result),
            overall_level=level,
            overall_score=(process.score + result.score) / 2,
            failure_reason=None if level != "failed" else "质量分数过低",
            fix_suggestions=suggestions
        )
        
        self.history.append(report)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        return report
    
    def get_report_markdown(self, report: TaskQualityReport) -> str:
        """生成 Markdown 报告"""
        level_emoji = {
            "excellent": "🌟",
            "qualified": "✅",
            "weak": "⚠️",
            "failed": "❌"
        }
        
        lines = [
            f"# 任务质量报告: {report.task_name}",
            "",
            f"## 总体评级: {level_emoji.get(report.overall_level, '❓')} {report.overall_level}",
            f"**分数**: {report.overall_score:.2f}",
            f"**时间**: {report.timestamp}",
            "",
            "### 过程质量",
            f"- 分数: {report.process_quality['score']:.2f}",
            f"- 按正确流程执行: {'✅' if report.process_quality['followed_correct_flow'] else '❌'}",
            f"- 遗漏步骤: {report.process_quality['missing_steps'] or '无'}",
            f"- 回退过度: {'是' if report.process_quality['fallback_overuse'] else '否'}",
            "",
            "### 结果质量",
            f"- 分数: {report.result_quality['score']:.2f}",
            f"- 输出非空: {'✅' if report.result_quality['output_not_empty'] else '❌'}",
            f"- 格式正确: {'✅' if report.result_quality['format_correct'] else '❌'}",
            f"- 可直接使用: {'✅' if report.result_quality['directly_usable'] else '❌'}",
            f"- 文件已生成: {'✅' if report.result_quality['files_generated'] else '❌'}",
            ""
        ]
        
        if report.fix_suggestions:
            lines.append("### 修复建议")
            for s in report.fix_suggestions:
                lines.append(f"- {s}")
        
        return "\n".join(lines)

# 全局实例
_evaluator = None

def get_quality_evaluator() -> TaskQualityEvaluator:
    global _evaluator
    if _evaluator is None:
        _evaluator = TaskQualityEvaluator()
    return _evaluator

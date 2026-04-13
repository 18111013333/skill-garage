#!/usr/bin/env python3
"""
能力激活报告 - V2.8.0

输出：
- 技能总数
- 已注册数
- 可路由数
- 可调用数
- 失效数
- 孤儿技能数
- 文档存在但未注册技能数
- 注册但未接通技能数
"""

import json
from typing import Dict, Any
from pathlib import Path

from infrastructure.path_resolver import (
    get_project_root, get_skills_dir, get_infrastructure_dir
)

class CapabilityReporter:
    """能力激活报告器"""
    
    def __init__(self):
        self.skills_dir = get_skills_dir()
        self.registry_path = get_infrastructure_dir() / 'inventory' / 'skill_registry.json'
        self.router_path = get_project_root() / 'orchestration' / 'router' / 'SKILL_ROUTER.json'
        
        self.registry = self._load_registry()
        self.router = self._load_router()
    
    def _load_registry(self) -> dict:
        """加载注册表"""
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text(encoding='utf-8'))
        return {"skills": {}}
    
    def _load_router(self) -> dict:
        """加载路由表"""
        if self.router_path.exists():
            return json.loads(self.router_path.read_text(encoding='utf-8'))
        return {"routes": []}
    
    def generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        # 扫描技能目录
        skill_dirs = set()
        if self.skills_dir.exists():
            for d in self.skills_dir.iterdir():
                if d.is_dir() and (d / 'SKILL.md').exists():
                    skill_dirs.add(d.name)
        
        # 已注册技能
        registered_skills = set(self.registry.get("skills", {}).keys())
        
        # 已路由技能
        routed_skills = set(
            r.get("skill") for r in self.router.get("routes", [])
            if r.get("skill")
        )
        
        # 可调用技能（有 main.py 或 SKILL.md）
        callable_skills = set()
        if self.skills_dir.exists():
            for d in self.skills_dir.iterdir():
                if d.is_dir():
                    if (d / 'main.py').exists() or (d / 'SKILL.md').exists():
                        callable_skills.add(d.name)
        
        # 失效技能（注册但不可调用）
        failed_skills = registered_skills - callable_skills
        
        # 孤儿技能（目录存在但未注册）
        orphaned_skills = skill_dirs - registered_skills
        
        # 文档存在但未注册
        doc_not_registered = skill_dirs - registered_skills
        
        # 注册但未接通
        registered_not_connected = registered_skills - routed_skills
        
        return {
            "summary": {
                "total_skills": len(skill_dirs),
                "registered": len(registered_skills),
                "routable": len(routed_skills),
                "callable": len(callable_skills),
                "failed": len(failed_skills),
                "orphaned": len(orphaned_skills),
                "doc_not_registered": len(doc_not_registered),
                "registered_not_connected": len(registered_not_connected)
            },
            "activation_rate": {
                "registration_rate": len(registered_skills) / max(len(skill_dirs), 1) * 100,
                "routing_rate": len(routed_skills) / max(len(registered_skills), 1) * 100,
                "callability_rate": len(callable_skills) / max(len(skill_dirs), 1) * 100
            },
            "details": {
                "orphaned_skills": list(orphaned_skills),
                "failed_skills": list(failed_skills),
                "doc_not_registered": list(doc_not_registered),
                "registered_not_connected": list(registered_not_connected)
            }
        }
    
    def get_report_markdown(self) -> str:
        """生成 Markdown 报告"""
        report = self.generate_report()
        summary = report["summary"]
        rates = report["activation_rate"]
        details = report["details"]
        
        lines = [
            "# 能力激活报告",
            "",
            "## 概览",
            "",
            "| 指标 | 数量 |",
            "|------|------|",
            f"| 技能总数 | {summary['total_skills']} |",
            f"| 已注册 | {summary['registered']} |",
            f"| 可路由 | {summary['routable']} |",
            f"| 可调用 | {summary['callable']} |",
            f"| 失效 | {summary['failed']} |",
            f"| 孤儿 | {summary['orphaned']} |",
            "",
            "## 激活率",
            "",
            "| 指标 | 比率 |",
            "|------|------|",
            f"| 注册率 | {rates['registration_rate']:.1f}% |",
            f"| 路由率 | {rates['routing_rate']:.1f}% |",
            f"| 可调用率 | {rates['callability_rate']:.1f}% |",
            "",
            "## 问题详情",
            ""
        ]
        
        if details["orphaned_skills"]:
            lines.append(f"### 孤儿技能（{len(details['orphaned_skills'])}）")
            for s in details["orphaned_skills"][:10]:
                lines.append(f"- {s}")
            lines.append("")
        
        if details["failed_skills"]:
            lines.append(f"### 失效技能（{len(details['failed_skills'])}）")
            for s in details["failed_skills"][:10]:
                lines.append(f"- {s}")
            lines.append("")
        
        if details["doc_not_registered"]:
            lines.append(f"### 文档存在但未注册（{len(details['doc_not_registered'])}）")
            for s in details["doc_not_registered"][:10]:
                lines.append(f"- {s}")
            lines.append("")
        
        if details["registered_not_connected"]:
            lines.append(f"### 注册但未接通（{len(details['registered_not_connected'])}）")
            for s in details["registered_not_connected"][:10]:
                lines.append(f"- {s}")
            lines.append("")
        
        return "\n".join(lines)

# 全局实例
_reporter = None

def get_capability_reporter() -> CapabilityReporter:
    """获取全局报告器"""
    global _reporter
    if _reporter is None:
        _reporter = CapabilityReporter()
    return _reporter

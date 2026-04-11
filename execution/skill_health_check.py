#!/usr/bin/env python3
"""
技能健康检查 - V2.8.0

检查项：
- 技能目录是否存在
- SKILL.md 是否存在
- 是否已注册
- 是否已进入路由表
- 路由引用是否有效
- 依赖是否缺失
- fallback 是否有效
- 技能是否实际可执行
"""

import json
from typing import Dict, List, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from infrastructure.path_resolver import (
    get_project_root, get_skills_dir, get_infrastructure_dir
)

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BROKEN = "broken"
    ORPHANED = "orphaned"

@dataclass
class HealthCheckResult:
    """健康检查结果"""
    skill_name: str
    status: str
    issues: List[str]
    checks: Dict[str, bool]

class SkillHealthChecker:
    """技能健康检查器"""
    
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
    
    def check_skill(self, skill_name: str) -> HealthCheckResult:
        """检查单个技能"""
        issues = []
        checks = {}
        
        # 1. 目录存在检查
        skill_dir = self.skills_dir / skill_name
        checks["dir_exists"] = skill_dir.exists()
        if not checks["dir_exists"]:
            issues.append("技能目录不存在")
        
        # 2. SKILL.md 存在检查
        skill_file = skill_dir / 'SKILL.md'
        checks["skill_md_exists"] = skill_file.exists()
        if not checks["skill_md_exists"]:
            issues.append("SKILL.md 不存在")
        
        # 3. 注册检查
        checks["registered"] = skill_name in self.registry.get("skills", {})
        if not checks["registered"]:
            issues.append("未注册到 skill_registry.json")
        
        # 4. 路由检查
        routed_skills = [r.get("skill") for r in self.router.get("routes", [])]
        checks["routable"] = skill_name in routed_skills
        if not checks["routable"]:
            issues.append("未进入路由表")
        
        # 5. 依赖检查
        skill_info = self.registry.get("skills", {}).get(skill_name, {})
        dependencies = skill_info.get("dependencies", [])
        missing_deps = []
        for dep in dependencies:
            dep_dir = self.skills_dir / dep
            if not dep_dir.exists():
                missing_deps.append(dep)
        
        checks["dependencies_ok"] = len(missing_deps) == 0
        if missing_deps:
            issues.append(f"缺失依赖: {missing_deps}")
        
        # 6. fallback 检查
        fallback = skill_info.get("fallback")
        if fallback:
            fallback_dir = self.skills_dir / fallback
            checks["fallback_valid"] = fallback_dir.exists()
            if not checks["fallback_valid"]:
                issues.append(f"fallback 无效: {fallback}")
        else:
            checks["fallback_valid"] = True  # 无 fallback 视为有效
        
        # 7. 可执行检查（简化版）
        main_file = skill_dir / 'main.py'
        checks["callable"] = main_file.exists() or skill_file.exists()
        if not checks["callable"]:
            issues.append("无可执行入口")
        
        # 确定状态
        if not checks["dir_exists"] or not checks["skill_md_exists"]:
            status = HealthStatus.ORPHANED.value
        elif not checks["registered"] or not checks["callable"]:
            status = HealthStatus.BROKEN.value
        elif not checks["routable"] or not checks["dependencies_ok"] or not checks["fallback_valid"]:
            status = HealthStatus.DEGRADED.value
        else:
            status = HealthStatus.HEALTHY.value
        
        return HealthCheckResult(
            skill_name=skill_name,
            status=status,
            issues=issues,
            checks=checks
        )
    
    def check_all(self) -> Dict[str, Any]:
        """检查所有技能"""
        results = []
        stats = {
            "total": 0,
            "healthy": 0,
            "degraded": 0,
            "broken": 0,
            "orphaned": 0
        }
        
        # 扫描技能目录
        if self.skills_dir.exists():
            for skill_dir in self.skills_dir.iterdir():
                if skill_dir.is_dir():
                    result = self.check_skill(skill_dir.name)
                    results.append(result)
                    stats["total"] += 1
                    stats[result.status] += 1
        
        # 检查注册但目录不存在的技能
        for skill_name in self.registry.get("skills", {}).keys():
            if not (self.skills_dir / skill_name).exists():
                result = HealthCheckResult(
                    skill_name=skill_name,
                    status=HealthStatus.ORPHANED.value,
                    issues=["注册但目录不存在"],
                    checks={"dir_exists": False}
                )
                results.append(result)
                stats["total"] += 1
                stats["orphaned"] += 1
        
        return {
            "stats": stats,
            "results": [r.__dict__ for r in results]
        }
    
    def get_report(self) -> str:
        """生成报告"""
        report_data = self.check_all()
        stats = report_data["stats"]
        
        lines = [
            "# 技能健康检查报告",
            "",
            "## 统计",
            f"- 总数: {stats['total']}",
            f"- 健康: {stats['healthy']}",
            f"- 降级: {stats['degraded']}",
            f"- 损坏: {stats['broken']}",
            f"- 孤儿: {stats['orphaned']}",
            "",
            "## 详情",
        ]
        
        for result in report_data["results"]:
            status_emoji = {
                "healthy": "✅",
                "degraded": "⚠️",
                "broken": "❌",
                "orphaned": "👻"
            }.get(result["status"], "❓")
            
            lines.append(f"### {status_emoji} {result['skill_name']}")
            lines.append(f"- 状态: {result['status']}")
            if result["issues"]:
                lines.append(f"- 问题: {', '.join(result['issues'])}")
            lines.append("")
        
        return "\n".join(lines)

# 全局实例
_checker = None

def get_health_checker() -> SkillHealthChecker:
    """获取全局健康检查器"""
    global _checker
    if _checker is None:
        _checker = SkillHealthChecker()
    return _checker

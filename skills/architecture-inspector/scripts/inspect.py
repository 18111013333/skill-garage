#!/usr/bin/env python3
"""架构巡检脚本 - V4.3.2

检查六层架构的完整性和一致性
"""

import json
import ast
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from enum import Enum

class CheckStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"

class CheckResult:
    def __init__(self, name: str, status: CheckStatus, message: str, details: Dict[str, Any] = None):
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}

class ArchitectureInspector:
    """架构巡检器"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(".")
        self.results: List[CheckResult] = []
    
    def run_all_checks(self, layer: str = None) -> Dict:
        """运行所有检查"""
        self.results = []
        
        # 1. 技能注册表检查
        self._check_skill_registry()
        
        # 2. 反向索引检查
        self._check_inverted_index()
        
        # 3. 路径规范检查
        self._check_path_usage()
        
        # 4. 核心文件检查
        self._check_core_files()
        
        # 5. 架构一致性检查
        self._check_architecture_consistency()
        
        # 6. 搜索链检查
        self._check_search_chain()
        
        # 汇总
        passed = sum(1 for r in self.results if r.status == CheckStatus.PASS)
        failed = sum(1 for r in self.results if r.status == CheckStatus.FAIL)
        warnings = sum(1 for r in self.results if r.status == CheckStatus.WARN)
        
        return {
            "status": "pass" if failed == 0 else "fail",
            "checks": [
                {
                    "name": r.name,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details
                }
                for r in self.results
            ],
            "summary": {
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "total": len(self.results)
            }
        }
    
    def _check_skill_registry(self):
        """检查技能注册表"""
        registry_path = self.base_path / "infrastructure/inventory/skill_registry.json"
        
        if not registry_path.exists():
            self.results.append(CheckResult(
                name="skill_registry_exists",
                status=CheckStatus.FAIL,
                message="技能注册表不存在"
            ))
            return
        
        try:
            with open(registry_path) as f:
                registry = json.load(f)
            
            skills = registry.get("skills", {})
            total = len(skills)
            
            # 检查字段完整性
            missing_fields = []
            for name, skill in skills.items():
                for field in ["registered", "routable", "callable", "executor_type", "entry_point", "path"]:
                    if field not in skill:
                        missing_fields.append(f"{name}.{field}")
            
            if missing_fields:
                self.results.append(CheckResult(
                    name="skill_registry_fields",
                    status=CheckStatus.FAIL,
                    message=f"缺少字段: {len(missing_fields)} 个",
                    details={"missing": missing_fields[:10]}
                ))
            else:
                self.results.append(CheckResult(
                    name="skill_registry_fields",
                    status=CheckStatus.PASS,
                    message=f"字段完整，共 {total} 个技能"
                ))
            
            # 检查一致性
            inconsistent = []
            for name, skill in skills.items():
                if skill.get("executor_type") == "skill_md" and skill.get("callable"):
                    inconsistent.append(f"{name}: skill_md 但 callable=true")
                if skill.get("callable") and skill.get("entry_point") == "SKILL.md":
                    inconsistent.append(f"{name}: callable 但 entry_point=SKILL.md")
            
            if inconsistent:
                self.results.append(CheckResult(
                    name="skill_registry_consistency",
                    status=CheckStatus.FAIL,
                    message=f"不一致: {len(inconsistent)} 个",
                    details={"inconsistent": inconsistent[:10]}
                ))
            else:
                self.results.append(CheckResult(
                    name="skill_registry_consistency",
                    status=CheckStatus.PASS,
                    message="状态一致"
                ))
        
        except Exception as e:
            self.results.append(CheckResult(
                name="skill_registry_parse",
                status=CheckStatus.FAIL,
                message=f"解析失败: {e}"
            ))
    
    def _check_inverted_index(self):
        """检查反向索引"""
        index_path = self.base_path / "infrastructure/inventory/skill_inverted_index.json"
        
        if not index_path.exists():
            self.results.append(CheckResult(
                name="inverted_index_exists",
                status=CheckStatus.FAIL,
                message="反向索引不存在"
            ))
            return
        
        try:
            with open(index_path) as f:
                index = json.load(f)
            
            by_trigger = index.get("by_trigger", {})
            
            # 检查索引条目
            indexed_skills = set()
            for targets in by_trigger.values():
                indexed_skills.update(targets)
            
            self.results.append(CheckResult(
                name="inverted_index_entries",
                status=CheckStatus.PASS,
                message=f"索引条目: {len(by_trigger)}, 收录技能: {len(indexed_skills)}"
            ))
        
        except Exception as e:
            self.results.append(CheckResult(
                name="inverted_index_parse",
                status=CheckStatus.FAIL,
                message=f"解析失败: {e}"
            ))
    
    def _check_path_usage(self):
        """检查路径使用"""
        result = subprocess.run(
            ["grep", "-r", "Path.home()", "--include=*.py", "."],
            capture_output=True, text=True,
            cwd=str(self.base_path)
        )
        
        lines = [l for l in result.stdout.split('\n') 
                 if l and 'node_modules' not in l and '__pycache__' not in l]
        
        if lines:
            self.results.append(CheckResult(
                name="path_home_usage",
                status=CheckStatus.WARN,
                message=f"发现 {len(lines)} 处 Path.home()",
                details={"files": [l.split(':')[0] for l in lines[:10]]}
            ))
        else:
            self.results.append(CheckResult(
                name="path_home_usage",
                status=CheckStatus.PASS,
                message="无 Path.home() 硬编码"
            ))
    
    def _check_core_files(self):
        """检查核心文件"""
        core_files = {
            "L1": ["core/ARCHITECTURE.md", "core/AGENTS.md", "core/SOUL.md"],
            "L2": ["memory_context/unified_search.py"],
            "L3": ["orchestration/task_engine.py"],
            "L4": ["execution/skill_adapter_gateway.py", "execution/skill_gateway.py"],
            "L5": ["governance/quality_gate.py"],
            "L6": ["infrastructure/shared/router.py", "infrastructure/inventory/skill_registry.json"],
        }
        
        missing = []
        for layer, files in core_files.items():
            for f in files:
                if not (self.base_path / f).exists():
                    missing.append(f"{layer}: {f}")
        
        if missing:
            self.results.append(CheckResult(
                name="core_files_exist",
                status=CheckStatus.FAIL,
                message=f"缺少文件: {len(missing)} 个",
                details={"missing": missing}
            ))
        else:
            self.results.append(CheckResult(
                name="core_files_exist",
                status=CheckStatus.PASS,
                message="核心文件完整"
            ))
    
    def _check_architecture_consistency(self):
        """检查架构一致性"""
        # 检查历史架构是否已归档
        history_files = [
            "core/ARCHITECTURE_V2.8.1.md",
            "core/ARCHITECTURE_V2.9.0.md",
            "core/ARCHITECTURE_V2.9.1.md",
        ]
        
        not_archived = []
        for f in history_files:
            if (self.base_path / f).exists():
                not_archived.append(f)
        
        if not_archived:
            self.results.append(CheckResult(
                name="history_architecture_archived",
                status=CheckStatus.WARN,
                message=f"历史架构未归档: {len(not_archived)} 个",
                details={"not_archived": not_archived}
            ))
        else:
            self.results.append(CheckResult(
                name="history_architecture_archived",
                status=CheckStatus.PASS,
                message="历史架构已归档"
            ))
    
    def _check_search_chain(self):
        """检查搜索链"""
        search_path = self.base_path / "memory_context/unified_search.py"
        
        if not search_path.exists():
            self.results.append(CheckResult(
                name="search_chain_exists",
                status=CheckStatus.FAIL,
                message="统一搜索入口不存在"
            ))
            return
        
        content = search_path.read_text()
        
        components = ["KeywordSearch", "FTSSearch", "VectorSearch", "RRFFusion", "SemanticDedup", "FeedbackLearner", "IndexExcludeList"]
        missing = [c for c in components if c not in content]
        
        if missing:
            self.results.append(CheckResult(
                name="search_chain_components",
                status=CheckStatus.WARN,
                message=f"缺少组件: {missing}",
                details={"missing": missing}
            ))
        else:
            self.results.append(CheckResult(
                name="search_chain_components",
                status=CheckStatus.PASS,
                message="搜索链组件完整"
            ))

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="架构巡检")
    parser.add_argument("--full", action="store_true", help="完整检查")
    parser.add_argument("--layer", choices=["L1", "L2", "L3", "L4", "L5", "L6"], help="检查指定层")
    args = parser.parse_args()
    
    inspector = ArchitectureInspector()
    result = inspector.run_all_checks(args.layer)
    
    print("=" * 70)
    print("架构巡检报告")
    print("=" * 70)
    
    for check in result["checks"]:
        status_icon = "✅" if check["status"] == "pass" else "❌" if check["status"] == "fail" else "⚠️"
        print(f"{status_icon} {check['name']}: {check['message']}")
    
    print("\n" + "=" * 70)
    print(f"汇总: 通过 {result['summary']['passed']}, 失败 {result['summary']['failed']}, 警告 {result['summary']['warnings']}")
    print("=" * 70)
    
    return 0 if result["status"] == "pass" else 1

if __name__ == "__main__":
    exit(main())

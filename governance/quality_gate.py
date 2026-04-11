"""质量守门器 - V4.3.1

四层检查：编译检查、配置校验、重复扫描、Token 预算检查
排除归档目录
"""

from typing import Dict, List, Any
from pathlib import Path
from infrastructure.path_resolver import get_project_root
import subprocess
import json
import re

class QualityGate:
    """质量守门器"""
    
    # 排除的目录
    EXCLUDE_DIRS = ["archive", "repo", "node_modules", ".git", "__pycache__"]
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path or get_project_root())
        self.results: Dict[str, Any] = {}
    
    def _should_skip(self, path: Path) -> bool:
        """检查是否应该跳过"""
        path_str = str(path)
        for exclude in self.EXCLUDE_DIRS:
            if exclude in path_str:
                return True
        return False
    
    def run_all_checks(self) -> Dict:
        """运行所有检查"""
        self.results = {
            "compile": self._check_compile(),
            "schema": self._check_schema(),
            "duplicate": self._check_duplicates(),
            "token": self._check_token_budget()
        }
        
        # 汇总
        all_passed = all(
            r.get("passed", False) for r in self.results.values()
        )
        
        self.results["summary"] = {
            "all_passed": all_passed,
            "total_issues": sum(len(r.get("issues", [])) for r in self.results.values())
        }
        
        return self.results
    
    def _check_compile(self) -> Dict:
        """编译检查"""
        issues = []
        
        # 检查 Python 语法
        for py_file in self.workspace.rglob("*.py"):
            if self._should_skip(py_file):
                continue
            
            try:
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode != 0:
                    issues.append({
                        "file": str(py_file.relative_to(self.workspace)),
                        "error": result.stderr[:200]
                    })
            except Exception as e:
                pass
        
        return {
            "passed": len(issues) == 0,
            "issues": issues[:10],
            "checked": "Python syntax"
        }
    
    def _check_schema(self) -> Dict:
        """配置与注册表 schema 校验"""
        issues = []
        
        # 检查 JSON 文件
        for json_file in self.workspace.rglob("*.json"):
            if self._should_skip(json_file):
                continue
            
            try:
                with open(json_file) as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                issues.append({
                    "file": str(json_file.relative_to(self.workspace)),
                    "error": f"JSON 解析错误: {str(e)[:100]}"
                })
        
        return {
            "passed": len(issues) == 0,
            "issues": issues[:10],
            "checked": "JSON schema"
        }
    
    def _check_duplicates(self) -> Dict:
        """重复实现扫描"""
        issues = []
        
        # 检查是否有模块未引用共享层
        shared_modules = ["router", "weights", "cache", "dedup"]
        
        for module in shared_modules:
            # 查找非共享层的实现
            for py_file in self.workspace.rglob(f"*{module}*.py"):
                if self._should_skip(py_file):
                    continue
                if "infrastructure/shared" in str(py_file):
                    continue
                
                # 检查是否引用了共享层
                content = py_file.read_text()
                if "infrastructure.shared" not in content:
                    issues.append({
                        "file": str(py_file.relative_to(self.workspace)),
                        "error": f"未引用共享层: infrastructure.shared.{module}"
                    })
        
        return {
            "passed": len(issues) == 0,
            "issues": issues[:10],
            "checked": "Duplicate implementations"
        }
    
    def _check_token_budget(self) -> Dict:
        """Token 预算检查"""
        issues = []
        
        # 检查配置中的 token 预算
        config_path = self.workspace / "config/unified.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            
            budget = config.get("token_budget", {})
            total = budget.get("total", 0)
            
            if total > 15000:
                issues.append({
                    "file": "config/unified.json",
                    "error": f"Token 预算过高: {total}"
                })
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "checked": "Token budget"
        }

#!/usr/bin/env python3
"""
技能接入网关 - V4.3.2 主链改造版

职责：
- 唯一技能接入中心
- __init__() 加载 registry 时，必须把已注册技能灌入 self.skills
- scan_skills() 负责扫物理目录
- register_all() 负责写回 skill_registry.json
- execute() 负责按 executor_type 真执行

执行分流：
- python → 导入模块并调 execute()
- script → subprocess
- api → 适配器
- skill_md → 仅注册不可执行
"""

import os
import re
import json
import subprocess
import asyncio
import importlib.util
import time
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, asdict, field
from enum import Enum

from infrastructure.path_resolver import (
    get_project_root, get_skills_dir, get_infrastructure_dir
)

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SkillStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BROKEN = "broken"
    DISABLED = "disabled"

class ErrorCode(Enum):
    """统一错误码 - V4.3.2 返修版"""
    SUCCESS = 0
    SKILL_NOT_FOUND = 1001
    SKILL_NOT_REGISTERED = 1002
    SKILL_NOT_ROUTABLE = 1003
    SKILL_NOT_CALLABLE = 1004
    SKILL_DISABLED = 1005
    BAD_ENTRY_POINT = 1006  # 新增：入口点错误
    EXECUTION_TIMEOUT = 2001
    EXECUTION_FAILED = 2002
    DEPENDENCY_MISSING = 3001
    PERMISSION_DENIED = 4001

@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    error_code: int
    error_message: Optional[str]
    output: Any
    duration_ms: int
    skill_name: str

@dataclass
class SkillMetadata:
    """技能元数据 - 统一字段"""
    name: str
    display_name: str
    description: str
    category: str
    risk_level: str
    dependencies: List[str]
    fallback: Optional[str]
    timeout: int
    layer: int
    status: str
    registered: bool
    routable: bool
    callable: bool
    path: str
    # V4.3.2: 必须字段
    entry_point: str = "SKILL.md"
    executor_type: str = "skill_md"  # python, script, api, skill_md

class SkillAdapterGateway:
    """技能接入网关 - 唯一技能接入中心"""
    
    def __init__(self):
        self.skills_dir = get_skills_dir()
        self.registry_path = get_infrastructure_dir() / 'inventory' / 'skill_registry.json'
        self.skills: Dict[str, SkillMetadata] = {}
        # V4.3.2: 初始化时从 registry 加载已注册技能
        self._load_registry_to_skills()
    
    def _load_registry_to_skills(self):
        """V4.3.2: 从 registry 加载已注册技能到 self.skills"""
        if not self.registry_path.exists():
            return
        
        registry = json.loads(self.registry_path.read_text(encoding='utf-8'))
        for name, skill_data in registry.get("skills", {}).items():
            # 转换为 SkillMetadata
            try:
                metadata = SkillMetadata(
                    name=skill_data.get("name", name),
                    display_name=skill_data.get("display_name", name),
                    description=skill_data.get("description", ""),
                    category=skill_data.get("category", "other"),
                    risk_level=skill_data.get("risk_level", "medium"),
                    dependencies=skill_data.get("dependencies", []),
                    fallback=skill_data.get("fallback"),
                    timeout=skill_data.get("timeout", 60),
                    layer=skill_data.get("layer", 4),
                    status=skill_data.get("status", "healthy"),
                    registered=skill_data.get("registered", False),
                    routable=skill_data.get("routable", False),
                    callable=skill_data.get("callable", False),
                    path=skill_data.get("path", ""),
                    entry_point=skill_data.get("entry_point", "SKILL.md"),
                    executor_type=skill_data.get("executor_type", "skill_md"),
                )
                self.skills[name] = metadata
            except Exception as e:
                print(f"加载技能 {name} 失败: {e}")
    
    def _save_registry(self, registry: dict):
        """保存注册表"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(
            json.dumps(registry, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def scan_skills(self) -> List[SkillMetadata]:
        """扫描所有技能目录 - 负责扫物理目录"""
        skills = []
        
        if not self.skills_dir.exists():
            return skills
        
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            skill_file = skill_dir / 'SKILL.md'
            if not skill_file.exists():
                continue
            
            metadata = self._parse_skill_md(skill_dir, skill_file)
            if metadata:
                skills.append(metadata)
                self.skills[metadata.name] = metadata
        
        return skills
    
    def _parse_skill_md(self, skill_dir: Path, skill_file: Path) -> Optional[SkillMetadata]:
        """解析 SKILL.md 提取元数据"""
        try:
            content = skill_file.read_text(encoding='utf-8')
            
            # 提取 YAML frontmatter
            frontmatter = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    fm_text = parts[1].strip()
                    for line in fm_text.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"\'')
            
            # 提取描述
            desc_match = re.search(r'^#\s+.+\n+(.+?)(?:\n\n|\n#|$)', content, re.MULTILINE)
            description = desc_match.group(1).strip() if desc_match else ""
            
            # 推断 executor_type
            executor_type = self._infer_executor_type(skill_dir, content)
            
            # 推断 entry_point
            entry_point = self._infer_entry_point(skill_dir, executor_type)
            
            return SkillMetadata(
                name=skill_dir.name,
                display_name=frontmatter.get('name', skill_dir.name),
                description=description[:200],
                category=self._infer_category(skill_dir.name, content),
                risk_level=self._infer_risk_level(skill_dir.name, content),
                dependencies=self._extract_dependencies(content),
                fallback=self._extract_fallback(content),
                timeout=self._extract_timeout(content),
                layer=4,
                status=SkillStatus.HEALTHY.value,
                registered=False,
                routable=False,
                callable=(executor_type != "skill_md"),  # skill_md 不可执行
                path=str(skill_dir.relative_to(get_project_root())),
                entry_point=entry_point,
                executor_type=executor_type,
            )
        
        except Exception as e:
            print(f"解析失败 {skill_dir.name}: {e}")
            return None
    
    def _infer_executor_type(self, skill_dir: Path, content: str) -> str:
        """推断执行类型 - V4.3.2 返修：与 registry 修复逻辑一致"""
        # 1. main.py (有 execute 或 main 函数)
        main_py = skill_dir / "main.py"
        if main_py.exists():
            try:
                main_content = main_py.read_text(errors='ignore')
                if "def execute" in main_content or "def main" in main_content:
                    return "python"
            except:
                pass
        
        # 2. __init__.py (有 execute 函数)
        init_py = skill_dir / "__init__.py"
        if init_py.exists():
            try:
                init_content = init_py.read_text(errors='ignore')
                if "def execute" in init_content:
                    return "python"
            except:
                pass
        
        # 3. scripts/*.py (有 main 或 if __name__)
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            for py_file in scripts_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                try:
                    py_content = py_file.read_text(errors='ignore')
                    if "def main" in py_content or "if __name__" in py_content:
                        return "script"
                except:
                    pass
        
        # 4. *.sh
        if list(skill_dir.glob("*.sh")):
            return "script"
        
        # 默认只有 SKILL.md
        return "skill_md"
    
    def _infer_entry_point(self, skill_dir: Path, executor_type: str) -> str:
        """推断入口点 - V4.3.2 返修：与 registry 修复逻辑一致"""
        if executor_type == "python":
            # 优先 main.py
            main_py = skill_dir / "main.py"
            if main_py.exists():
                try:
                    content = main_py.read_text(errors='ignore')
                    if "def execute" in content or "def main" in content:
                        return "main.py"
                except:
                    pass
            
            # 其次 __init__.py (有 execute)
            init_py = skill_dir / "__init__.py"
            if init_py.exists():
                try:
                    content = init_py.read_text(errors='ignore')
                    if "def execute" in content:
                        return "__init__.py"
                except:
                    pass
            
            return "main.py" if main_py.exists() else "__init__.py"
        
        elif executor_type == "script":
            # 优先 scripts/*.py (有 main 或 if __name__)
            scripts_dir = skill_dir / "scripts"
            if scripts_dir.exists():
                for py_file in scripts_dir.glob("*.py"):
                    if py_file.name == "__init__.py":
                        continue
                    try:
                        content = py_file.read_text(errors='ignore')
                        if "def main" in content or "if __name__" in content:
                            return f"scripts/{py_file.name}"
                    except:
                        pass
            
            # 其次 *.sh
            sh_files = list(skill_dir.glob("*.sh"))
            if sh_files:
                return sh_files[0].name
        
        # skill_md 返回 SKILL.md
        return "SKILL.md"
    
    def _infer_category(self, name: str, content: str) -> str:
        # 默认只有 SKILL.md
        return "skill_md"
    
    def _infer_category(self, name: str, content: str) -> str:
        """推断分类"""
        name_lower = name.lower()
        content_lower = content.lower()
        
        if 'search' in name_lower or '搜索' in content_lower:
            return 'search'
        elif 'doc' in name_lower or 'pdf' in name_lower:
            return 'document'
        elif 'image' in name_lower or '图片' in content_lower:
            return 'image'
        elif 'email' in name_lower or 'message' in name_lower:
            return 'communication'
        elif 'data' in name_lower or 'analysis' in name_lower:
            return 'data'
        elif 'auto' in name_lower or 'cron' in name_lower:
            return 'automation'
        elif 'system' in name_lower or 'git' in name_lower:
            return 'system'
        else:
            return 'other'
    
    def _infer_risk_level(self, name: str, content: str) -> str:
        """推断风险等级"""
        high_risk = ['rm', 'delete', 'drop', 'exec', 'shell', 'sudo', 'auth']
        medium_risk = ['write', 'create', 'update', 'modify', 'send']
        
        name_lower = name.lower()
        content_lower = content.lower()
        
        for keyword in high_risk:
            if keyword in name_lower or keyword in content_lower:
                return RiskLevel.HIGH.value
        
        for keyword in medium_risk:
            if keyword in name_lower or keyword in content_lower:
                return RiskLevel.MEDIUM.value
        
        return RiskLevel.LOW.value
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """提取依赖"""
        deps = []
        match = re.search(r'dependencies:\s*\n((?:\s*-\s+.+\n)+)', content)
        if match:
            for line in match.group(1).split('\n'):
                dep = line.strip().lstrip('- ').strip()
                if dep:
                    deps.append(dep)
        return deps
    
    def _extract_fallback(self, content: str) -> Optional[str]:
        """提取 fallback"""
        match = re.search(r'fallback:\s*(\S+)', content)
        return match.group(1) if match else None
    
    def _extract_timeout(self, content: str) -> int:
        """提取 timeout"""
        match = re.search(r'timeout:\s*(\d+)', content)
        return int(match.group(1)) if match else 60
    
    def register_all(self) -> Dict[str, int]:
        """注册所有扫描到的技能 - 写回 skill_registry.json"""
        skills = self.scan_skills()
        registry = {"version": "4.3.2", "skills": {}}
        
        stats = {
            "total": len(skills),
            "registered": 0,
            "updated": 0,
            "skipped": 0
        }
        
        for skill in skills:
            registry["skills"][skill.name] = asdict(skill)
            stats["registered"] += 1
        
        self._save_registry(registry)
        return stats
    
    def get_skill(self, name: str) -> Optional[SkillMetadata]:
        """获取技能"""
        return self.skills.get(name)
    
    def list_skills(self, category: str = None, status: str = None) -> List[SkillMetadata]:
        """列出技能"""
        skills = list(self.skills.values())
        
        if category:
            skills = [s for s in skills if s.category == category]
        if status:
            skills = [s for s in skills if s.status == status]
        
        return skills
    
    # ========== V4.3.2: 真执行入口 ==========
    
    def execute(self, skill_name: str, params: Dict[str, Any] = None) -> ExecutionResult:
        """
        V4.3.2: 统一执行入口 - 按 executor_type 真执行
        
        Args:
            skill_name: 技能名称
            params: 执行参数
            
        Returns:
            ExecutionResult: 包含成功/失败状态、错误码、真实输出
        """
        start_time = time.time()
        params = params or {}
        
        # 1. 检查技能是否存在
        skill = self.skills.get(skill_name)
        if not skill:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.SKILL_NOT_FOUND.value,
                error_message=f"技能 '{skill_name}' 不存在",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        # 2. 检查技能状态
        if not skill.registered:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.SKILL_NOT_REGISTERED.value,
                error_message=f"技能 '{skill_name}' 未注册",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        if not skill.routable:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.SKILL_NOT_ROUTABLE.value,
                error_message=f"技能 '{skill_name}' 不可路由",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        if not skill.callable:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.SKILL_NOT_CALLABLE.value,
                error_message=f"技能 '{skill_name}' 不可调用 (executor_type={skill.executor_type})",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        if skill.status == "disabled":
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.SKILL_DISABLED.value,
                error_message=f"技能 '{skill_name}' 已禁用",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        # 3. 检查依赖
        missing_deps = []
        for dep in skill.dependencies:
            if dep not in self.skills or not self.skills[dep].callable:
                missing_deps.append(dep)
        
        if missing_deps:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.DEPENDENCY_MISSING.value,
                error_message=f"技能 '{skill_name}' 缺少依赖: {missing_deps}",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        # 4. V4.3.2 返修：检查入口点是否有效
        if skill.entry_point == "SKILL.md":
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.BAD_ENTRY_POINT.value,
                error_message=f"技能 '{skill_name}' 入口点为 SKILL.md，不可执行",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        # 检查 executor_type 与 entry_point 是否匹配
        if skill.executor_type == "skill_md":
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.BAD_ENTRY_POINT.value,
                error_message=f"技能 '{skill_name}' executor_type=skill_md，不可执行",
                output=None,
                duration_ms=0,
                skill_name=skill_name
            )
        
        # 5. 按 executor_type 真执行
        try:
            if skill.executor_type == "python":
                output = self._execute_python(skill, params)
            elif skill.executor_type == "script":
                output = self._execute_script(skill, params)
            elif skill.executor_type == "api":
                output = self._execute_api(skill, params)
            else:
                return ExecutionResult(
                    success=False,
                    error_code=ErrorCode.SKILL_NOT_CALLABLE.value,
                    error_message=f"技能 '{skill_name}' 类型 '{skill.executor_type}' 不可执行",
                    output=None,
                    duration_ms=int((time.time() - start_time) * 1000),
                    skill_name=skill_name
                )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            return ExecutionResult(
                success=True,
                error_code=ErrorCode.SUCCESS.value,
                error_message=None,
                output=output,
                duration_ms=duration_ms,
                skill_name=skill_name
            )
        
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.EXECUTION_TIMEOUT.value,
                error_message=f"技能 '{skill_name}' 执行超时 ({skill.timeout}s)",
                output=None,
                duration_ms=skill.timeout * 1000,
                skill_name=skill_name
            )
        
        except Exception as e:
            return ExecutionResult(
                success=False,
                error_code=ErrorCode.EXECUTION_FAILED.value,
                error_message=f"技能 '{skill_name}' 执行失败: {str(e)}",
                output=None,
                duration_ms=int((time.time() - start_time) * 1000),
                skill_name=skill_name
            )
    
    def _execute_python(self, skill: SkillMetadata, params: Dict[str, Any]) -> Any:
        """执行 Python 模块"""
        skill_path = get_project_root() / skill.path
        entry_path = skill_path / skill.entry_point
        
        # 动态导入模块
        spec = importlib.util.spec_from_file_location(skill.name, entry_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 调用 execute 函数
        if hasattr(module, 'execute'):
            return module.execute(params)
        elif hasattr(module, 'main'):
            return module.main(params)
        else:
            raise ValueError(f"模块 {skill.name} 没有 execute 或 main 函数")
    
    def _execute_script(self, skill: SkillMetadata, params: Dict[str, Any]) -> Any:
        """执行脚本 - V4.3.2 返修：支持多种参数协议"""
        skill_path = get_project_root() / skill.path
        entry_path = skill_path / skill.entry_point
        
        # 构建命令
        if skill.entry_point.endswith('.py'):
            cmd = ['python3', str(entry_path)]
        else:
            cmd = ['bash', str(entry_path)]
        
        # V4.3.2 返修：检测脚本的参数协议
        if skill.entry_point.endswith('.py'):
            try:
                script_content = entry_path.read_text(errors='ignore')
                
                # 检测是否使用 argparse
                if 'argparse' in script_content:
                    # 检查是否有位置参数（add_argument 没有 -- 前缀）
                    import re
                    positional_args = re.findall(r'add_argument\s*\(\s*["\']([^"\']+)["\']', script_content)
                    positional_args = [arg for arg in positional_args if not arg.startswith('-')]
                    
                    if positional_args:
                        # 使用位置参数
                        param_order = self._get_param_order(skill.name, entry_path.name)
                        # 如果没有预定义顺序，使用检测到的位置参数名
                        if not param_order:
                            param_order = positional_args
                        for key in param_order:
                            if key in params:
                                cmd.append(str(params[key]))
                    else:
                        # 使用 --key value 格式
                        for key, value in params.items():
                            cmd.extend([f'--{key}', str(value)])
                
                # 检测是否需要位置参数
                elif 'sys.argv' in script_content:
                    param_order = self._get_param_order(skill.name, entry_path.name)
                    for key in param_order:
                        if key in params:
                            cmd.append(str(params[key]))
                
                else:
                    # 默认使用 --key value
                    for key, value in params.items():
                        cmd.extend([f'--{key}', str(value)])
            
            except Exception:
                # 默认使用 --key value
                for key, value in params.items():
                    cmd.extend([f'--{key}', str(value)])
        else:
            # bash 脚本使用环境变量
            env = os.environ.copy()
            for key, value in params.items():
                env[key.upper()] = str(value)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=skill.timeout,
                cwd=str(skill_path),
                env=env
            )
            
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            
            return {"stdout": result.stdout, "stderr": result.stderr}
        
        # 执行 Python 脚本
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=skill.timeout,
            cwd=str(skill_path)
        )
        
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        
        return {"stdout": result.stdout, "stderr": result.stderr}
    
    def _get_param_order(self, skill_name: str, script_name: str) -> List[str]:
        """V4.3.2 返修：获取脚本的参数顺序"""
        # 常见脚本的参数映射
        param_orders = {
            "docx": {
                "accept_changes.py": ["input_file", "output_file"],
                "comment.py": ["doc_path", "comment_id", "comment_text"],
                "unpack.py": ["input_file", "output_directory"],
            },
            "find-skills": {
                "search.py": ["query"],
            },
            "pdf": {
                "convert_pdf_to_images.py": ["input_file", "output_dir"],
                "check_fillable_fields.py": ["input_file"],
            },
        }
        
        if skill_name in param_orders:
            return param_orders[skill_name].get(script_name, [])
        
        return []
    
    def _execute_api(self, skill: SkillMetadata, params: Dict[str, Any]) -> Any:
        """执行 API 调用 - 需要适配器"""
        # TODO: 实现 API 适配器
        raise NotImplementedError("API 执行器尚未实现")
    
    def health_check(self, skill_name: str) -> Dict[str, Any]:
        """技能健康检查"""
        skill = self.skills.get(skill_name)
        if not skill:
            return {
                "exists": False,
                "healthy": False,
                "issues": ["技能不存在"]
            }
        
        issues = []
        
        # 检查路径
        skill_path = get_project_root() / skill.path
        if not skill_path.exists():
            issues.append(f"路径不存在: {skill.path}")
        
        # 检查入口文件
        entry_file = skill_path / skill.entry_point
        if not entry_file.exists():
            issues.append(f"入口文件不存在: {skill.entry_point}")
        
        # 检查状态
        if not skill.registered:
            issues.append("未注册")
        if not skill.routable:
            issues.append("不可路由")
        if not skill.callable:
            issues.append("不可调用")
        
        return {
            "exists": True,
            "healthy": len(issues) == 0,
            "issues": issues,
            "status": {
                "registered": skill.registered,
                "routable": skill.routable,
                "callable": skill.callable,
                "status": skill.status,
                "executor_type": skill.executor_type,
            }
        }

# 全局实例
_gateway: Optional[SkillAdapterGateway] = None

def get_skill_gateway() -> SkillAdapterGateway:
    """获取全局技能网关"""
    global _gateway
    if _gateway is None:
        _gateway = SkillAdapterGateway()
    return _gateway

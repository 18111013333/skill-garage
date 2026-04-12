#!/usr/bin/env python3
"""
统一路径解析器 - V2.8.0

规则：
1. 环境变量优先
2. 自动发现项目根目录
3. 相对路径回退

禁止硬编码绝对路径
"""

import os
from pathlib import Path
from typing import Optional

def get_project_root() -> Path:
    """
    获取项目根目录 - V3.0.0 修复冷启动污染
    
    优先级：
    1. OPENCLAW_PROJECT_ROOT 环境变量（显式项目根）
    2. OPENCLAW_WORKSPACE 环境变量
    3. 当前工作目录（如果包含 core/ARCHITECTURE.md）
    4. 自动发现（向上查找 core/ARCHITECTURE.md）
    5. 最后才 fallback 到 OPENCLAW_GIT_DIR（仅用于 repo 根推导）
    6. 回退到当前工作目录
    
    重要：OPENCLAW_GIT_DIR 不能在当前目录已经是完整项目时抢优先级
    """
    cwd = Path.cwd()
    
    # 1. OPENCLAW_PROJECT_ROOT 环境变量（显式项目根）
    env_project = os.environ.get('OPENCLAW_PROJECT_ROOT')
    if env_project:
        path = Path(env_project)
        if path.exists() and (path / 'core' / 'ARCHITECTURE.md').exists():
            return path
    
    # 2. OPENCLAW_WORKSPACE 环境变量
    env_workspace = os.environ.get('OPENCLAW_WORKSPACE')
    if env_workspace:
        path = Path(env_workspace)
        if path.exists() and (path / 'core' / 'ARCHITECTURE.md').exists():
            return path
    
    # 3. 当前工作目录优先（如果包含项目文件）
    if (cwd / 'core' / 'ARCHITECTURE.md').exists():
        return cwd
    
    # 4. 自动发现（向上查找）
    current = cwd
    while current != current.parent:
        if (current / 'core' / 'ARCHITECTURE.md').exists():
            return current
        current = current.parent
    
    # 5. 最后才 fallback 到 OPENCLAW_GIT_DIR（仅用于 repo 根推导）
    # 注意：只有当当前目录不是完整项目时才使用
    env_git = os.environ.get('OPENCLAW_GIT_DIR')
    if env_git:
        path = Path(env_git).parent
        if path.exists() and (path / 'core' / 'ARCHITECTURE.md').exists():
            return path
    
    # 6. 回退到当前工作目录
    return cwd

def get_core_dir() -> Path:
    """获取 core 目录"""
    return get_project_root() / 'core'

def get_infrastructure_dir() -> Path:
    """获取 infrastructure 目录"""
    return get_project_root() / 'infrastructure'

def get_skills_dir() -> Path:
    """获取 skills 目录"""
    return get_project_root() / 'skills'

def get_plugins_dir() -> Path:
    """获取 plugins 目录"""
    return get_project_root() / 'plugins'

def get_memory_dir() -> Path:
    """获取 memory 目录"""
    return get_project_root() / 'memory'

def get_memory_context_dir() -> Path:
    """获取 memory_context 目录"""
    return get_project_root() / 'memory_context'

def get_governance_dir() -> Path:
    """获取 governance 目录"""
    return get_project_root() / 'governance'

def get_execution_dir() -> Path:
    """获取 execution 目录"""
    return get_project_root() / 'execution'

def get_orchestration_dir() -> Path:
    """获取 orchestration 目录"""
    return get_project_root() / 'orchestration'

def resolve_path(relative_path: str) -> Path:
    """
    解析相对路径为绝对路径
    
    Args:
        relative_path: 相对于项目根的路径
    
    Returns:
        绝对路径
    """
    return get_project_root() / relative_path

# 全局缓存
_project_root: Optional[Path] = None

def get_cached_project_root() -> Path:
    """获取缓存的项目根目录"""
    global _project_root
    if _project_root is None:
        _project_root = get_project_root()
    return _project_root

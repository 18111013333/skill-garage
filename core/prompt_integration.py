#!/usr/bin/env python3
"""
提示词与架构集成 - V2.8.0
唯一真源：只读取 core/ 目录

禁止读取根目录兼容副本
"""

import os
import sys
import re
from typing import Dict, Any, Optional, List
from pathlib import Path

# ============================================================
# 路径解析 - 统一规则
# ============================================================

def get_project_root() -> Path:
    """
    获取项目根目录 - 统一规则
    1. 环境变量优先
    2. 自动发现（向上查找 core/ARCHITECTURE.md）
    3. 相对路径回退
    """
    # 1. 环境变量优先
    env_root = os.environ.get('OPENCLAW_WORKSPACE')
    if env_root and Path(env_root).exists():
        return Path(env_root)
    
    # 2. 自动发现
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'core' / 'ARCHITECTURE.md').exists():
            return current
        current = current.parent
    
    # 3. 相对路径回退
    return Path(__file__).resolve().parent.parent

# 全局项目根
PROJECT_ROOT = get_project_root()
CORE_DIR = PROJECT_ROOT / 'core'

# ============================================================
# 主运行时读取源 - 唯一真源
# ============================================================

CORE_FILES = [
    'AGENTS.md',
    'TOOLS.md', 
    'IDENTITY.md',
    'SOUL.md',
    'USER.md',
    'HEARTBEAT.md'
]

class PromptOrchestrator:
    """提示词编排器 - L1 核心层"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.core_dir = CORE_DIR
        self.loaded_layers: Dict[int, str] = {}
    
    def _read_core_file(self, filename: str) -> str:
        """
        读取核心文件 - 只从 core/ 目录读取
        禁止读取根目录兼容副本
        """
        filepath = self.core_dir / filename
        if filepath.exists():
            return filepath.read_text(encoding='utf-8')
        return ""
    
    def load_layer(self, layer: int) -> str:
        """按层加载提示词"""
        if layer in self.loaded_layers:
            return self.loaded_layers[layer]
        
        content = ""
        
        if layer == 1:
            content = self._load_core()
        elif layer == 2:
            content = self._load_memory()
        elif layer == 3:
            content = self._load_orchestration()
        elif layer == 4:
            content = self._load_execution()
        elif layer == 5:
            content = self._load_governance()
        elif layer == 6:
            content = self._load_infrastructure()
        
        self.loaded_layers[layer] = content
        return content
    
    def _load_core(self) -> str:
        """加载核心层 - 只读取 core/ 目录"""
        parts = []
        
        for filename in CORE_FILES:
            content = self._read_core_file(filename)
            if content:
                # 移除兼容副本标记
                content = re.sub(r'^# 兼容副本.*\n', '', content)
                parts.append(content)
        
        return "\n\n".join(parts)
    
    def _load_memory(self) -> str:
        """加载记忆层"""
        memory_dir = self.project_root / 'memory_context'
        parts = []
        
        memory_manager = memory_dir / 'memory_manager.py'
        if memory_manager.exists():
            parts.append(f"# Memory Manager\n{memory_manager.read_text(encoding='utf-8')[:2000]}")
        
        return "\n\n".join(parts)
    
    def _load_orchestration(self) -> str:
        """加载编排层"""
        orch_dir = self.project_root / 'orchestration'
        parts = []
        
        task_engine = orch_dir / 'task_engine.py'
        if task_engine.exists():
            parts.append(f"# Task Engine\n{task_engine.read_text(encoding='utf-8')[:2000]}")
        
        return "\n\n".join(parts)
    
    def _load_execution(self) -> str:
        """加载执行层"""
        exec_dir = self.project_root / 'execution'
        parts = []
        
        gateway = exec_dir / 'skill_adapter_gateway.py'
        if gateway.exists():
            parts.append(f"# Skill Gateway\n{gateway.read_text(encoding='utf-8')[:2000]}")
        
        return "\n\n".join(parts)
    
    def _load_governance(self) -> str:
        """加载治理层"""
        gov_dir = self.project_root / 'governance' / 'security'
        parts = []
        
        auth = gov_dir / 'auth_integration.py'
        if auth.exists():
            parts.append(f"# Auth Integration\n{auth.read_text(encoding='utf-8')[:2000]}")
        
        return "\n\n".join(parts)
    
    def _load_infrastructure(self) -> str:
        """加载基建层"""
        infra_dir = self.project_root / 'infrastructure'
        parts = []
        
        integration = infra_dir / 'integration.py'
        if integration.exists():
            parts.append(f"# Integration\n{integration.read_text(encoding='utf-8')[:2000]}")
        
        return "\n\n".join(parts)
    
    def load_minimal(self) -> str:
        """加载最小提示词"""
        return self._load_core()
    
    def load_full(self) -> str:
        """加载完整提示词"""
        all_parts = []
        for layer in range(1, 7):
            content = self.load_layer(layer)
            if content:
                all_parts.append(f"## L{layer} 层\n{content}")
        return "\n\n".join(all_parts)
    
    def get_token_estimate(self, layer: int = None) -> int:
        """估算 Token"""
        if layer:
            content = self.load_layer(layer)
        else:
            content = self.load_minimal()
        
        chinese = len(re.findall(r'[\u4e00-\u9fff]', content))
        other = len(content) - chinese
        return int(chinese / 2 + other / 4)
    
    def clear_cache(self):
        """清理缓存"""
        self.loaded_layers.clear()

# ============================================================
# 全局实例
# ============================================================

_orchestrator: Optional[PromptOrchestrator] = None

def get_prompt_orchestrator() -> PromptOrchestrator:
    """获取全局提示词编排器"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = PromptOrchestrator()
    return _orchestrator

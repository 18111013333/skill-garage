#!/usr/bin/env python3
"""
插件与架构集成 - V2.8.0
使用统一路径解析
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from infrastructure.path_resolver import (
    get_project_root, get_plugins_dir, get_infrastructure_dir
)
from infrastructure.plugin_standard import PluginManager, PluginResult

class PluginOrchestrator:
    """插件编排器 - L4 执行层"""
    
    def __init__(self):
        self.plugin_dir = get_plugins_dir()
        self.registry_path = get_infrastructure_dir() / 'PLUGIN_REGISTRY.json'
        self.manager = PluginManager(str(self.plugin_dir))
        self.registry = self._load_registry()
        self.manager.discover()
    
    def _load_registry(self) -> dict:
        """加载注册表"""
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text(encoding='utf-8'))
        return {"plugins": {}, "layer_mapping": {}}
    
    def _save_registry(self):
        """保存注册表"""
        self.registry_path.write_text(
            json.dumps(self.registry, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def register_plugin(self, plugin_name: str, info: dict):
        """注册插件"""
        self.registry["plugins"][plugin_name] = {
            "name": plugin_name,
            "display_name": info.get("display_name", plugin_name),
            "description": info.get("description", ""),
            "version": info.get("version", "1.0.0"),
            "author": info.get("author", ""),
            "requires_auth": info.get("requires_auth", False),
            "layer": info.get("layer", 4),
            "entry": f"plugins/{plugin_name}/main.py",
            "config": f"plugins/{plugin_name}/description.yaml",
            "status": "active"
        }
        
        layer = info.get("layer", 4)
        layer_key = f"L{layer}_execution"
        if layer_key not in self.registry["layer_mapping"]:
            self.registry["layer_mapping"][layer_key] = []
        
        if plugin_name not in self.registry["layer_mapping"][layer_key]:
            self.registry["layer_mapping"][layer_key].append(plugin_name)
        
        self._save_registry()
    
    def call_plugin(self, plugin_name: str, arg: Dict[str, Any]) -> PluginResult:
        """调用插件"""
        return self.manager.call(plugin_name, arg)
    
    def get_plugin_info(self, plugin_name: str) -> Optional[dict]:
        """获取插件信息"""
        return self.registry["plugins"].get(plugin_name)
    
    def list_plugins(self, layer: int = None) -> List[dict]:
        """列出插件"""
        plugins = list(self.registry["plugins"].values())
        if layer:
            plugins = [p for p in plugins if p.get("layer") == layer]
        return plugins
    
    def get_plugins_by_layer(self, layer: int) -> List[str]:
        """按层级获取插件"""
        layer_key = f"L{layer}_execution"
        return self.registry["layer_mapping"].get(layer_key, [])

# 全局实例
_orchestrator: Optional[PluginOrchestrator] = None

def get_plugin_orchestrator() -> PluginOrchestrator:
    """获取全局插件编排器"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = PluginOrchestrator()
    return _orchestrator

def call_plugin(name: str, arg: dict) -> PluginResult:
    """调用插件"""
    return get_plugin_orchestrator().call_plugin(name, arg)

#!/usr/bin/env python3
"""
插件扩展系统
支持动态加载、配置管理、生命周期控制
"""

import os
import json
import importlib.util
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict


@dataclass
class Plugin:
    """插件"""
    id: str
    name: str
    version: str
    description: str
    author: str
    enabled: bool = True
    installed_at: str = ""
    config: Dict = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugins_dir: str = None):
        if plugins_dir is None:
            plugins_dir = os.path.join(
                os.path.dirname(__file__),
                'plugins'
            )
        
        self.plugins_dir = plugins_dir
        self.registry_file = os.path.join(plugins_dir, 'registry.json')
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        
        os.makedirs(plugins_dir, exist_ok=True)
        self._load_registry()
        
        print(f"插件管理器初始化完成")
        print(f"  - 插件目录: {plugins_dir}")
        print(f"  - 已注册插件: {len(self.plugins)}")
    
    def _load_registry(self):
        """加载插件注册表"""
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for plugin_data in data.get('plugins', []):
                plugin = Plugin(
                    id=plugin_data['id'],
                    name=plugin_data['name'],
                    version=plugin_data['version'],
                    description=plugin_data['description'],
                    author=plugin_data['author'],
                    enabled=plugin_data.get('enabled', True),
                    installed_at=plugin_data.get('installed_at', ''),
                    config=plugin_data.get('config', {})
                )
                self.plugins[plugin.id] = plugin
    
    def _save_registry(self):
        """保存插件注册表"""
        data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'plugins': [asdict(plugin) for plugin in self.plugins.values()]
        }
        
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def register(self, plugin: Plugin) -> bool:
        """注册插件"""
        if plugin.id in self.plugins:
            print(f"插件 {plugin.id} 已存在")
            return False
        
        plugin.installed_at = datetime.now().isoformat()
        self.plugins[plugin.id] = plugin
        self._save_registry()
        
        print(f"注册插件: {plugin.name} v{plugin.version}")
        return True
    
    def unregister(self, plugin_id: str) -> bool:
        """注销插件"""
        if plugin_id not in self.plugins:
            print(f"插件 {plugin_id} 不存在")
            return False
        
        del self.plugins[plugin_id]
        self._save_registry()
        
        print(f"注销插件: {plugin_id}")
        return True
    
    def enable(self, plugin_id: str) -> bool:
        """启用插件"""
        if plugin_id not in self.plugins:
            print(f"插件 {plugin_id} 不存在")
            return False
        
        self.plugins[plugin_id].enabled = True
        self._save_registry()
        
        print(f"启用插件: {plugin_id}")
        return True
    
    def disable(self, plugin_id: str) -> bool:
        """禁用插件"""
        if plugin_id not in self.plugins:
            print(f"插件 {plugin_id} 不存在")
            return False
        
        self.plugins[plugin_id].enabled = False
        self._save_registry()
        
        print(f"禁用插件: {plugin_id}")
        return True
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """获取插件"""
        return self.plugins.get(plugin_id)
    
    def list_plugins(self, enabled_only: bool = False) -> List[Plugin]:
        """列出插件"""
        if enabled_only:
            return [p for p in self.plugins.values() if p.enabled]
        return list(self.plugins.values())
    
    def register_hook(self, hook_name: str, callback: Callable):
        """注册钩子"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        self.hooks[hook_name].append(callback)
        print(f"注册钩子: {hook_name}")
    
    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """触发钩子"""
        results = []
        
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"钩子执行失败: {e}")
        
        return results
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        enabled = sum(1 for p in self.plugins.values() if p.enabled)
        
        return {
            'total_plugins': len(self.plugins),
            'enabled_plugins': enabled,
            'disabled_plugins': len(self.plugins) - enabled,
            'registered_hooks': len(self.hooks)
        }


# 预置插件
BUILTIN_PLUGINS = [
    Plugin(
        id='memory-enhancer',
        name='记忆增强器',
        version='1.0.0',
        description='增强记忆存储和检索能力',
        author='openclaw'
    ),
    Plugin(
        id='smart-scheduler',
        name='智能调度器',
        version='1.0.0',
        description='智能任务调度和优化',
        author='openclaw'
    ),
    Plugin(
        id='context-manager',
        name='上下文管理器',
        version='1.0.0',
        description='管理对话上下文和状态',
        author='openclaw'
    ),
]


# 命令行接口
if __name__ == "__main__":
    import sys
    
    manager = PluginManager()
    
    # 注册预置插件
    for plugin in BUILTIN_PLUGINS:
        if plugin.id not in manager.plugins:
            manager.register(plugin)
    
    if len(sys.argv) < 2:
        print("用法: python plugin_system.py <command>")
        print("命令: list, enable <id>, disable <id>, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        print("\n插件列表:")
        print("-" * 60)
        for plugin in manager.list_plugins():
            status = "✅" if plugin.enabled else "❌"
            print(f"{status} {plugin.name} v{plugin.version}: {plugin.description}")
    
    elif command == 'enable':
        if len(sys.argv) < 3:
            print("请指定插件 ID")
            sys.exit(1)
        manager.enable(sys.argv[2])
    
    elif command == 'disable':
        if len(sys.argv) < 3:
            print("请指定插件 ID")
            sys.exit(1)
        manager.disable(sys.argv[2])
    
    elif command == 'stats':
        stats = manager.get_stats()
        print("\n插件统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

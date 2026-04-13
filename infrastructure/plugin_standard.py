#!/usr/bin/env python3
"""
插件标准接口
V2.7.0 - 2026-04-10

借鉴 LegnaChat 的插件标准化设计
"""

import os
import json
import yaml
import importlib.util
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    display_name: str
    description: str
    version: str = "1.0.0"
    author: str = ""
    requires_auth: bool = False
    dependencies: list = field(default_factory=list)

@dataclass
class PluginResult:
    """插件执行结果"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0

class PluginBase:
    """插件基类 - 借鉴 LegnaChat 的 tool_main 接口"""
    
    @property
    def name(self) -> str:
        """插件名称"""
        return self.__class__.__name__.lower().replace('plugin', '')
    
    @property
    def info(self) -> PluginInfo:
        """插件信息"""
        return PluginInfo(
            name=self.name,
            display_name=self.name,
            description="",
        )
    
    def tool_main(self, arg: Dict[str, Any]) -> str:
        """
        主入口函数 - LegnaChat 标准接口
        
        Args:
            arg: 输入参数字典
        
        Returns:
            str: 执行结果
        """
        raise NotImplementedError("子类必须实现 tool_main 方法")
    
    def validate_input(self, arg: Dict[str, Any]) -> bool:
        """验证输入参数"""
        return True
    
    def execute(self, arg: Dict[str, Any]) -> PluginResult:
        """执行插件"""
        import time
        start = time.time()
        
        try:
            if not self.validate_input(arg):
                return PluginResult(
                    success=False,
                    error="输入参数验证失败"
                )
            
            result = self.tool_main(arg)
            
            return PluginResult(
                success=True,
                data=result,
                latency_ms=(time.time() - start) * 1000
            )
        
        except Exception as e:
            return PluginResult(
                success=False,
                error=str(e),
                latency_ms=(time.time() - start) * 1000
            )

class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugin_dir: str):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
    
    def discover(self):
        """发现所有插件"""
        if not self.plugin_dir.exists():
            return
        
        for plugin_path in self.plugin_dir.iterdir():
            if plugin_path.is_dir():
                self._load_plugin(plugin_path)
    
    def _load_plugin(self, plugin_path: Path):
        """加载单个插件"""
        # 读取 description.yaml
        desc_file = plugin_path / "description.yaml"
        if not desc_file.exists():
            return
        
        try:
            with open(desc_file, 'r', encoding='utf-8') as f:
                desc = yaml.safe_load(f)
            
            plugin_name = plugin_path.name
            self.plugin_info[plugin_name] = PluginInfo(
                name=plugin_name,
                display_name=desc.get('display_name', plugin_name),
                description=desc.get('description', ''),
                version=desc.get('version', '1.0.0'),
                author=desc.get('author', ''),
                requires_auth=desc.get('requires_auth', False),
            )
            
            # 加载 main.py
            main_file = plugin_path / "main.py"
            if main_file.exists():
                spec = importlib.util.spec_from_file_location(
                    f"plugin_{plugin_name}",
                    main_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'tool_main'):
                    # 包装为 PluginBase
                    self.plugins[plugin_name] = _WrapperPlugin(
                        plugin_name,
                        module.tool_main
                    )
        
        except Exception as e:
            print(f"加载插件 {plugin_path.name} 失败: {e}")
    
    def call(self, plugin_name: str, arg: Dict[str, Any]) -> PluginResult:
        """调用插件"""
        if plugin_name not in self.plugins:
            return PluginResult(
                success=False,
                error=f"插件 {plugin_name} 不存在"
            )
        
        return self.plugins[plugin_name].execute(arg)
    
    def list_plugins(self) -> Dict[str, PluginInfo]:
        """列出所有插件"""
        return self.plugin_info
    
    def get_plugin_description(self, plugin_name: str) -> Optional[str]:
        """获取插件描述"""
        if plugin_name in self.plugin_info:
            info = self.plugin_info[plugin_name]
            return f"""
插件: {info.display_name}
描述: {info.description}
版本: {info.version}
需要授权: {'是' if info.requires_auth else '否'}
"""
        return None

class _WrapperPlugin(PluginBase):
    """包装器 - 将 tool_main 函数包装为 PluginBase"""
    
    def __init__(self, name: str, tool_main_func: Callable):
        self._name = name
        self._tool_main = tool_main_func
    
    @property
    def name(self) -> str:
        return self._name
    
    def tool_main(self, arg: Dict[str, Any]) -> str:
        return self._tool_main(arg)

# 创建插件模板
def create_plugin_template(plugin_dir: str, plugin_name: str, display_name: str, description: str):
    """创建插件模板"""
    plugin_path = Path(plugin_dir) / plugin_name
    plugin_path.mkdir(parents=True, exist_ok=True)
    
    # main.py
    main_py = f'''#!/usr/bin/env python3
"""
{display_name}
"""

def tool_main(arg: dict) -> str:
    """
    插件主函数
    
    Args:
        arg: 输入参数字典
    
    Returns:
        str: 执行结果
    """
    # TODO: 实现插件逻辑
    return "插件执行成功"
'''
    
    # description.yaml
    desc_yaml = f'''display_name: "{display_name}"
description: "{description}"
version: "1.0.0"
author: ""
requires_auth: false
'''
    
    (plugin_path / "main.py").write_text(main_py, encoding='utf-8')
    (plugin_path / "description.yaml").write_text(desc_yaml, encoding='utf-8')
    
    return plugin_path

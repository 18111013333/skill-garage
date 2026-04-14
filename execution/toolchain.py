#!/usr/bin/env python3
"""
开发工具链
支持调试、测试、部署
"""

import os
import json
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Tool:
    """工具"""
    id: str
    name: str
    category: str  # debug, test, deploy
    description: str
    command: str
    enabled: bool = True


@dataclass
class TaskResult:
    """任务结果"""
    tool_id: str
    success: bool
    output: str
    duration: float
    timestamp: str


class Toolchain:
    """工具链"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(
                os.path.dirname(__file__),
                'toolchain'
            )
        
        self.config_dir = config_dir
        self.tools_file = os.path.join(config_dir, 'tools.json')
        self.history_file = os.path.join(config_dir, 'history.json')
        
        self.tools: Dict[str, Tool] = {}
        self.history: List[TaskResult] = []
        
        os.makedirs(config_dir, exist_ok=True)
        self._load_data()
        self._register_builtin_tools()
        
        print(f"工具链初始化完成")
        print(f"  - 工具数量: {len(self.tools)}")
        print(f"  - 历史记录: {len(self.history)}")
    
    def _load_data(self):
        """加载数据"""
        # 加载工具
        if os.path.exists(self.tools_file):
            with open(self.tools_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for tool_data in data.get('tools', []):
                tool = Tool(
                    id=tool_data['id'],
                    name=tool_data['name'],
                    category=tool_data['category'],
                    description=tool_data['description'],
                    command=tool_data['command'],
                    enabled=tool_data.get('enabled', True)
                )
                self.tools[tool.id] = tool
        
        # 加载历史
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for result_data in data.get('history', []):
                result = TaskResult(
                    tool_id=result_data['tool_id'],
                    success=result_data['success'],
                    output=result_data['output'],
                    duration=result_data['duration'],
                    timestamp=result_data['timestamp']
                )
                self.history.append(result)
    
    def _save_data(self):
        """保存数据"""
        # 保存工具
        tools_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'tools': [asdict(tool) for tool in self.tools.values()]
        }
        
        with open(self.tools_file, 'w', encoding='utf-8') as f:
            json.dump(tools_data, f, ensure_ascii=False, indent=2)
        
        # 保存历史（只保留最近 100 条）
        history_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'history': [asdict(r) for r in self.history[-100:]]
        }
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
    
    def _register_builtin_tools(self):
        """注册内置工具"""
        builtin_tools = [
            Tool('lint', '代码检查', 'debug', '检查代码质量', 'python -m pylint'),
            Tool('format', '代码格式化', 'debug', '格式化代码', 'python -m black'),
            Tool('test', '单元测试', 'test', '运行单元测试', 'python -m pytest'),
            Tool('coverage', '覆盖率测试', 'test', '测试覆盖率分析', 'python -m coverage'),
            Tool('build', '构建', 'deploy', '构建项目', 'python setup.py build'),
            Tool('deploy', '部署', 'deploy', '部署到生产环境', 'python setup.py install'),
        ]
        
        for tool in builtin_tools:
            if tool.id not in self.tools:
                self.tools[tool.id] = tool
        
        self._save_data()
    
    def register_tool(self, tool: Tool) -> bool:
        """注册工具"""
        if tool.id in self.tools:
            print(f"工具 {tool.id} 已存在")
            return False
        
        self.tools[tool.id] = tool
        self._save_data()
        
        print(f"注册工具: {tool.name}")
        return True
    
    def run_tool(self, tool_id: str, args: str = "") -> TaskResult:
        """运行工具"""
        if tool_id not in self.tools:
            print(f"工具 {tool_id} 不存在")
            return TaskResult(
                tool_id=tool_id,
                success=False,
                output=f"工具 {tool_id} 不存在",
                duration=0,
                timestamp=datetime.now().isoformat()
            )
        
        tool = self.tools[tool_id]
        
        if not tool.enabled:
            print(f"工具 {tool.name} 已禁用")
            return TaskResult(
                tool_id=tool_id,
                success=False,
                output=f"工具 {tool.name} 已禁用",
                duration=0,
                timestamp=datetime.now().isoformat()
            )
        
        print(f"运行工具: {tool.name}")
        
        # 模拟执行
        start_time = time.time()
        
        try:
            # 实际执行命令（这里简化为模拟）
            output = f"执行: {tool.command} {args}"
            success = True
        except Exception as e:
            output = f"错误: {e}"
            success = False
        
        duration = time.time() - start_time
        
        result = TaskResult(
            tool_id=tool_id,
            success=success,
            output=output,
            duration=duration,
            timestamp=datetime.now().isoformat()
        )
        
        self.history.append(result)
        self._save_data()
        
        print(f"  结果: {'成功' if success else '失败'} ({duration:.2f}s)")
        return result
    
    def list_tools(self, category: str = None) -> List[Tool]:
        """列出工具"""
        if category:
            return [t for t in self.tools.values() if t.category == category]
        return list(self.tools.values())
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        success_count = sum(1 for r in self.history if r.success)
        
        return {
            'total_tools': len(self.tools),
            'total_runs': len(self.history),
            'success_rate': f"{100 * success_count / len(self.history):.1f}%" if self.history else "N/A",
            'categories': {
                'debug': len([t for t in self.tools.values() if t.category == 'debug']),
                'test': len([t for t in self.tools.values() if t.category == 'test']),
                'deploy': len([t for t in self.tools.values() if t.category == 'deploy'])
            }
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    toolchain = Toolchain()
    
    if len(sys.argv) < 2:
        print("用法: python toolchain.py <command>")
        print("命令: list, run <id>, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        print("\n工具列表:")
        print("-" * 60)
        for tool in toolchain.list_tools():
            status = "✅" if tool.enabled else "❌"
            print(f"{status} [{tool.category}] {tool.name}: {tool.description}")
    
    elif command == 'run':
        if len(sys.argv) < 3:
            print("请指定工具 ID")
            sys.exit(1)
        result = toolchain.run_tool(sys.argv[2])
        print(f"输出: {result.output}")
    
    elif command == 'stats':
        stats = toolchain.get_stats()
        print("\n工具链统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

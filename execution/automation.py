#!/usr/bin/env python3
"""
自动化流程引擎
支持工作流定义、执行、调度
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict


@dataclass
class WorkflowStep:
    """工作流步骤"""
    id: str
    name: str
    action: str
    params: Dict
    next_step: Optional[str] = None
    condition: Optional[str] = None


@dataclass
class Workflow:
    """工作流"""
    id: str
    name: str
    description: str
    steps: List[Dict]
    triggers: List[str]
    enabled: bool = True
    created_at: str = ""
    last_run: str = ""
    run_count: int = 0


class AutomationEngine:
    """自动化引擎"""
    
    def __init__(self, workflows_dir: str = None):
        if workflows_dir is None:
            workflows_dir = os.path.join(
                os.path.dirname(__file__),
                'workflows'
            )
        
        self.workflows_dir = workflows_dir
        self.registry_file = os.path.join(workflows_dir, 'registry.json')
        self.workflows: Dict[str, Workflow] = {}
        self.actions: Dict[str, Callable] = {}
        
        os.makedirs(workflows_dir, exist_ok=True)
        self._load_registry()
        self._register_builtin_actions()
        
        print(f"自动化引擎初始化完成")
        print(f"  - 工作流目录: {workflows_dir}")
        print(f"  - 已注册工作流: {len(self.workflows)}")
        print(f"  - 已注册动作: {len(self.actions)}")
    
    def _load_registry(self):
        """加载工作流注册表"""
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for wf_data in data.get('workflows', []):
                workflow = Workflow(
                    id=wf_data['id'],
                    name=wf_data['name'],
                    description=wf_data['description'],
                    steps=wf_data['steps'],
                    triggers=wf_data['triggers'],
                    enabled=wf_data.get('enabled', True),
                    created_at=wf_data.get('created_at', ''),
                    last_run=wf_data.get('last_run', ''),
                    run_count=wf_data.get('run_count', 0)
                )
                self.workflows[workflow.id] = workflow
    
    def _save_registry(self):
        """保存工作流注册表"""
        data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'workflows': [asdict(wf) for wf in self.workflows.values()]
        }
        
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _register_builtin_actions(self):
        """注册内置动作"""
        self.actions['log'] = lambda msg: print(f"[LOG] {msg}")
        self.actions['wait'] = lambda seconds: time.sleep(seconds)
        self.actions['notify'] = lambda msg: print(f"[通知] {msg}")
        self.actions['save_memory'] = lambda key, value: print(f"[记忆] {key}: {value}")
    
    def register_action(self, name: str, callback: Callable):
        """注册动作"""
        self.actions[name] = callback
        print(f"注册动作: {name}")
    
    def create_workflow(self, workflow: Workflow) -> bool:
        """创建工作流"""
        if workflow.id in self.workflows:
            print(f"工作流 {workflow.id} 已存在")
            return False
        
        workflow.created_at = datetime.now().isoformat()
        self.workflows[workflow.id] = workflow
        self._save_registry()
        
        print(f"创建工作流: {workflow.name}")
        return True
    
    def run_workflow(self, workflow_id: str, context: Dict = None) -> bool:
        """执行工作流"""
        if workflow_id not in self.workflows:
            print(f"工作流 {workflow_id} 不存在")
            return False
        
        workflow = self.workflows[workflow_id]
        
        if not workflow.enabled:
            print(f"工作流 {workflow.name} 已禁用")
            return False
        
        print(f"\n执行工作流: {workflow.name}")
        print("-" * 40)
        
        if context is None:
            context = {}
        
        # 执行步骤
        for i, step in enumerate(workflow.steps):
            step_id = step.get('id', f'step_{i}')
            action = step.get('action')
            params = step.get('params', {})
            
            print(f"  [{i+1}/{len(workflow.steps)}] {step.get('name', step_id)}")
            
            if action in self.actions:
                try:
                    result = self.actions[action](**params)
                    context[f'{step_id}_result'] = result
                except Exception as e:
                    print(f"    错误: {e}")
                    return False
            else:
                print(f"    未知动作: {action}")
        
        # 更新统计
        workflow.last_run = datetime.now().isoformat()
        workflow.run_count += 1
        self._save_registry()
        
        print(f"\n工作流执行完成")
        return True
    
    def list_workflows(self, enabled_only: bool = False) -> List[Workflow]:
        """列出工作流"""
        if enabled_only:
            return [wf for wf in self.workflows.values() if wf.enabled]
        return list(self.workflows.values())
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        enabled = sum(1 for wf in self.workflows.values() if wf.enabled)
        total_runs = sum(wf.run_count for wf in self.workflows.values())
        
        return {
            'total_workflows': len(self.workflows),
            'enabled_workflows': enabled,
            'total_runs': total_runs,
            'registered_actions': len(self.actions)
        }


# 预置工作流
BUILTIN_WORKFLOWS = [
    Workflow(
        id='daily-summary',
        name='每日总结',
        description='每天生成工作总结',
        steps=[
            {'id': 'collect', 'name': '收集数据', 'action': 'log', 'params': {'msg': '收集今日数据'}},
            {'id': 'analyze', 'name': '分析数据', 'action': 'log', 'params': {'msg': '分析数据趋势'}},
            {'id': 'report', 'name': '生成报告', 'action': 'notify', 'params': {'msg': '每日报告已生成'}}
        ],
        triggers=['cron:0 20 * * *']
    ),
    Workflow(
        id='memory-backup',
        name='记忆备份',
        description='定期备份记忆数据',
        steps=[
            {'id': 'export', 'name': '导出记忆', 'action': 'log', 'params': {'msg': '导出记忆数据'}},
            {'id': 'compress', 'name': '压缩数据', 'action': 'log', 'params': {'msg': '压缩备份文件'}},
            {'id': 'notify', 'name': '发送通知', 'action': 'notify', 'params': {'msg': '记忆备份完成'}}
        ],
        triggers=['cron:0 2 * * *']
    ),
]


# 命令行接口
if __name__ == "__main__":
    import sys
    
    engine = AutomationEngine()
    
    # 注册预置工作流
    for workflow in BUILTIN_WORKFLOWS:
        if workflow.id not in engine.workflows:
            engine.create_workflow(workflow)
    
    if len(sys.argv) < 2:
        print("用法: python automation.py <command>")
        print("命令: list, run <id>, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        print("\n工作流列表:")
        print("-" * 60)
        for workflow in engine.list_workflows():
            status = "✅" if workflow.enabled else "❌"
            print(f"{status} {workflow.name}: {workflow.description}")
            print(f"   运行次数: {workflow.run_count}")
    
    elif command == 'run':
        if len(sys.argv) < 3:
            print("请指定工作流 ID")
            sys.exit(1)
        engine.run_workflow(sys.argv[2])
    
    elif command == 'stats':
        stats = engine.get_stats()
        print("\n自动化统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

#!/usr/bin/env python3
"""
可控半自动推进控制器 - V2.8.0

允许自动处理：
- 下一步建议生成
- 待办列表更新
- 合适工作流自动选择
- 产物自动归档
- 阻塞项自动标记
- 阶段总结自动生成

要求：
- 高风险动作仍需确认
- 自动化边界必须可配置
- 每一步自动推进必须可追踪、可解释、可中止
"""

import json
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

from infrastructure.path_resolver import get_project_root

class AutonomyLevel(Enum):
    FULL_AUTO = "full_auto"        # 全自动
    GUIDED = "guided"              # 引导式（推荐）
    MANUAL = "manual"              # 手动

class ActionType(Enum):
    SUGGEST_NEXT = "suggest_next"
    UPDATE_TODO = "update_todo"
    SELECT_WORKFLOW = "select_workflow"
    ARCHIVE_PRODUCT = "archive_product"
    MARK_BLOCKER = "mark_blocker"
    GENERATE_SUMMARY = "generate_summary"
    HIGH_RISK = "high_risk"        # 高风险动作

@dataclass
class AutonomyAction:
    """自动动作"""
    action_id: str
    action_type: str
    description: str
    auto_allowed: bool
    requires_confirmation: bool
    executed: bool
    timestamp: str
    details: Dict[str, Any]

@dataclass
class AutonomyConfig:
    """自动化配置"""
    level: str
    auto_suggest_next: bool
    auto_update_todo: bool
    auto_select_workflow: bool
    auto_archive: bool
    auto_mark_blocker: bool
    auto_generate_summary: bool
    high_risk_needs_confirm: bool

class GuidedAutonomyController:
    """可控半自动推进控制器"""
    
    DEFAULT_CONFIG = AutonomyConfig(
        level=AutonomyLevel.GUIDED.value,
        auto_suggest_next=True,
        auto_update_todo=True,
        auto_select_workflow=True,
        auto_archive=True,
        auto_mark_blocker=False,  # 阻塞标记需确认
        auto_generate_summary=True,
        high_risk_needs_confirm=True
    )
    
    def __init__(self):
        self.project_root = get_project_root()
        self.config_path = self.project_root / 'execution' / 'autonomy_config.json'
        self.history_path = self.project_root / 'execution' / 'autonomy_history.json'
        
        self.config = self._load_config()
        self.history: List[AutonomyAction] = []
        self._load_history()
    
    def _load_config(self) -> AutonomyConfig:
        """加载配置"""
        if self.config_path.exists():
            data = json.loads(self.config_path.read_text(encoding='utf-8'))
            return AutonomyConfig(**data)
        return self.DEFAULT_CONFIG
    
    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps(asdict(self.config), indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def _load_history(self):
        """加载历史"""
        if self.history_path.exists():
            data = json.loads(self.history_path.read_text(encoding='utf-8'))
            self.history = [AutonomyAction(**a) for a in data.get("actions", [])]
    
    def _save_history(self):
        """保存历史"""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.write_text(
            json.dumps({"actions": [asdict(a) for a in self.history]}, 
                      indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self._save_config()
    
    def set_level(self, level: str):
        """设置自动化级别"""
        self.config.level = level
        
        if level == AutonomyLevel.FULL_AUTO.value:
            self.config.auto_suggest_next = True
            self.config.auto_update_todo = True
            self.config.auto_select_workflow = True
            self.config.auto_archive = True
            self.config.auto_mark_blocker = True
            self.config.auto_generate_summary = True
            self.config.high_risk_needs_confirm = False
        
        elif level == AutonomyLevel.MANUAL.value:
            self.config.auto_suggest_next = False
            self.config.auto_update_todo = False
            self.config.auto_select_workflow = False
            self.config.auto_archive = False
            self.config.auto_mark_blocker = False
            self.config.auto_generate_summary = False
            self.config.high_risk_needs_confirm = True
        
        else:  # GUIDED
            self.config = self.DEFAULT_CONFIG
        
        self._save_config()
    
    def can_auto_execute(self, action_type: str) -> bool:
        """判断是否可自动执行"""
        # 高风险动作始终需确认
        if action_type == ActionType.HIGH_RISK.value:
            return not self.config.high_risk_needs_confirm
        
        # 根据配置判断
        auto_map = {
            ActionType.SUGGEST_NEXT.value: self.config.auto_suggest_next,
            ActionType.UPDATE_TODO.value: self.config.auto_update_todo,
            ActionType.SELECT_WORKFLOW.value: self.config.auto_select_workflow,
            ActionType.ARCHIVE_PRODUCT.value: self.config.auto_archive,
            ActionType.MARK_BLOCKER.value: self.config.auto_mark_blocker,
            ActionType.GENERATE_SUMMARY.value: self.config.auto_generate_summary,
        }
        
        return auto_map.get(action_type, False)
    
    def execute_action(self, action_type: str, description: str,
                       details: Dict = None, 
                       force_confirm: bool = False) -> Dict:
        """执行动作"""
        action_id = f"act_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        auto_allowed = self.can_auto_execute(action_type)
        requires_confirmation = not auto_allowed or force_confirm
        
        action = AutonomyAction(
            action_id=action_id,
            action_type=action_type,
            description=description,
            auto_allowed=auto_allowed,
            requires_confirmation=requires_confirmation,
            executed=False,
            timestamp=datetime.now().isoformat(),
            details=details or {}
        )
        
        if requires_confirmation:
            # 需要确认，返回待确认状态
            self.history.append(action)
            self._save_history()
            return {
                "status": "pending_confirmation",
                "action_id": action_id,
                "description": description,
                "message": f"需要确认: {description}"
            }
        
        # 自动执行
        action.executed = True
        self.history.append(action)
        self._save_history()
        
        return {
            "status": "executed",
            "action_id": action_id,
            "description": description,
            "message": f"已自动执行: {description}"
        }
    
    def confirm_action(self, action_id: str) -> Dict:
        """确认动作"""
        for action in self.history:
            if action.action_id == action_id:
                action.executed = True
                self._save_history()
                return {
                    "status": "confirmed",
                    "action_id": action_id,
                    "message": f"已确认执行: {action.description}"
                }
        
        return {"status": "not_found", "message": "动作不存在"}
    
    def cancel_action(self, action_id: str) -> Dict:
        """取消动作"""
        for i, action in enumerate(self.history):
            if action.action_id == action_id:
                self.history.pop(i)
                self._save_history()
                return {
                    "status": "cancelled",
                    "action_id": action_id,
                    "message": "动作已取消"
                }
        
        return {"status": "not_found", "message": "动作不存在"}
    
    def get_pending_actions(self) -> List[Dict]:
        """获取待确认动作"""
        return [
            asdict(a) for a in self.history
            if a.requires_confirmation and not a.executed
        ]
    
    def get_execution_log(self, limit: int = 50) -> List[Dict]:
        """获取执行日志"""
        return [asdict(a) for a in self.history[-limit:]]
    
    def explain_action(self, action_id: str) -> str:
        """解释动作"""
        for action in self.history:
            if action.action_id == action_id:
                lines = [
                    f"# 动作解释: {action.action_id}",
                    "",
                    f"**类型**: {action.action_type}",
                    f"**描述**: {action.description}",
                    f"**自动允许**: {'是' if action.auto_allowed else '否'}",
                    f"**需要确认**: {'是' if action.requires_confirmation else '否'}",
                    f"**已执行**: {'是' if action.executed else '否'}",
                    f"**时间**: {action.timestamp}",
                ]
                
                if action.details:
                    lines.extend(["", "**详情**:", ""])
                    for key, value in action.details.items():
                        lines.append(f"- {key}: {value}")
                
                return "\n".join(lines)
        
        return "动作不存在"
    
    def get_status_report(self) -> str:
        """获取状态报告"""
        lines = [
            "# 半自动推进状态",
            "",
            "## 配置",
            f"- 级别: {self.config.level}",
            f"- 自动建议下一步: {'✅' if self.config.auto_suggest_next else '❌'}",
            f"- 自动更新待办: {'✅' if self.config.auto_update_todo else '❌'}",
            f"- 自动选择工作流: {'✅' if self.config.auto_select_workflow else '❌'}",
            f"- 自动归档: {'✅' if self.config.auto_archive else '❌'}",
            f"- 自动标记阻塞: {'✅' if self.config.auto_mark_blocker else '❌'}",
            f"- 自动生成总结: {'✅' if self.config.auto_generate_summary else '❌'}",
            f"- 高风险需确认: {'✅' if self.config.high_risk_needs_confirm else '❌'}",
            "",
            "## 待确认动作",
            ""
        ]
        
        pending = self.get_pending_actions()
        if pending:
            for action in pending[:10]:
                lines.append(f"- [{action['action_type']}] {action['description']}")
        else:
            lines.append("无待确认动作")
        
        lines.extend([
            "",
            f"## 执行统计",
            f"- 总动作数: {len(self.history)}",
            f"- 已执行: {sum(1 for a in self.history if a.executed)}",
            f"- 待确认: {len(pending)}"
        ])
        
        return "\n".join(lines)

# 全局实例
_autonomy_controller = None

def get_autonomy_controller() -> GuidedAutonomyController:
    global _autonomy_controller
    if _autonomy_controller is None:
        _autonomy_controller = GuidedAutonomyController()
    return _autonomy_controller

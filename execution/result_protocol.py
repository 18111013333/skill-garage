"""统一结果包装协议 - V4.3.0

所有技能输出必须遵循此协议，确保格式一致。
"""

from typing import Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class SkillResult:
    """技能执行结果 - 统一输出格式
    
    所有技能必须返回此格式的结果
    """
    success: bool                          # 是否成功
    skill_id: str                          # 技能ID
    data: Any                              # 返回数据
    error: Optional[str] = None            # 错误信息
    trace: Optional[str] = None            # 错误堆栈
    next_action: Optional[str] = None      # 建议下一步
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "success": self.success,
            "skill_id": self.skill_id,
            "data": self.data,
            "error": self.error,
            "trace": self.trace,
            "next_action": self.next_action,
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def success_result(cls, skill_id: str, data: Any, next_action: str = None) -> "SkillResult":
        """创建成功结果"""
        return cls(
            success=True,
            skill_id=skill_id,
            data=data,
            next_action=next_action
        )
    
    @classmethod
    def error_result(cls, skill_id: str, error: str, trace: str = None) -> "SkillResult":
        """创建错误结果"""
        return cls(
            success=False,
            skill_id=skill_id,
            data=None,
            error=error,
            trace=trace
        )

@dataclass
class TaskResult:
    """任务执行结果"""
    success: bool
    task_id: str
    skill_results: List[SkillResult]
    summary: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "task_id": self.task_id,
            "skill_results": [r.to_dict() for r in self.skill_results],
            "summary": self.summary,
            "timestamp": self.timestamp
        }

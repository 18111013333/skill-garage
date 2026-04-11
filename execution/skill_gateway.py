"""技能网关 - V4.3.2 主链改造版

统一技能执行入口，负责技能调用、结果包装、异常处理。
V4.3.2 主链改造：
- 去掉 _do_execute() 的假执行，改成真正委托给 SkillAdapterGateway
- 统一包装结果为 SkillResult / ExecutionResult
- 统一映射错误：not_found、not_registered、not_routable、not_callable、timeout、dependency_missing、execution_failed
- 统计必须基于真实执行结果
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import traceback

from execution.skill_adapter_gateway import (
    get_skill_gateway, ExecutionResult, ErrorCode
)

@dataclass
class SkillResult:
    """技能执行结果 - 统一输出格式"""
    success: bool
    skill_id: str
    data: Any
    error: Optional[str] = None
    error_code: int = 0
    error_type: str = ""
    trace: Optional[str] = None
    next_action: Optional[str] = None
    timestamp: str = ""
    duration_ms: int = 0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class SkillGateway:
    """技能网关 - 唯一执行入口"""
    
    def __init__(self):
        self.execution_stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "by_error_type": {}
        }
    
    def execute(self, skill_id: str, params: Dict[str, Any]) -> SkillResult:
        """执行技能 - 真正委托给 SkillAdapterGateway"""
        self.execution_stats["total"] += 1
        
        # 获取技能适配器网关
        adapter = get_skill_gateway()
        
        # 调用真实执行
        result: ExecutionResult = adapter.execute(skill_id, params)
        
        # 映射错误类型
        error_type = self._map_error_type(result.error_code)
        
        # 更新统计
        if result.success:
            self.execution_stats["success"] += 1
        else:
            self.execution_stats["failed"] += 1
            self.execution_stats["by_error_type"][error_type] = \
                self.execution_stats["by_error_type"].get(error_type, 0) + 1
        
        return SkillResult(
            success=result.success,
            skill_id=skill_id,
            data=result.output,
            error=result.error_message,
            error_code=result.error_code,
            error_type=error_type,
            trace=traceback.format_exc() if not result.success and result.error_code != ErrorCode.SUCCESS.value else None,
            next_action=self._suggest_next(skill_id, result),
            duration_ms=result.duration_ms
        )
    
    def _map_error_type(self, error_code: int) -> str:
        """映射错误码到错误类型 - V4.3.2 返修版"""
        error_map = {
            ErrorCode.SUCCESS.value: "success",
            ErrorCode.SKILL_NOT_FOUND.value: "not_found",
            ErrorCode.SKILL_NOT_REGISTERED.value: "not_registered",
            ErrorCode.SKILL_NOT_ROUTABLE.value: "not_routable",
            ErrorCode.SKILL_NOT_CALLABLE.value: "not_callable",
            ErrorCode.SKILL_DISABLED.value: "disabled",
            ErrorCode.BAD_ENTRY_POINT.value: "bad_entry_point",  # 新增
            ErrorCode.EXECUTION_TIMEOUT.value: "timeout",
            ErrorCode.EXECUTION_FAILED.value: "execution_failed",
            ErrorCode.DEPENDENCY_MISSING.value: "dependency_missing",
            ErrorCode.PERMISSION_DENIED.value: "permission_denied",
        }
        return error_map.get(error_code, "unknown")
    
    def _suggest_next(self, skill_id: str, result: ExecutionResult) -> Optional[str]:
        """建议下一步动作"""
        if result.success:
            return None
        
        # 根据错误类型建议
        if result.error_code == ErrorCode.SKILL_NOT_FOUND.value:
            return f"请检查技能名称 '{skill_id}' 是否正确"
        elif result.error_code == ErrorCode.SKILL_NOT_REGISTERED.value:
            return f"技能 '{skill_id}' 需要先注册"
        elif result.error_code == ErrorCode.DEPENDENCY_MISSING.value:
            return "请先安装缺失的依赖技能"
        elif result.error_code == ErrorCode.EXECUTION_TIMEOUT.value:
            return "执行超时，可以尝试增加超时时间或简化任务"
        
        return None
    
    def get_stats(self) -> Dict:
        """获取执行统计 - 基于真实执行结果"""
        return {
            **self.execution_stats,
            "success_rate": self.execution_stats["success"] / max(1, self.execution_stats["total"])
        }
    
    def health_check(self, skill_id: str) -> Dict[str, Any]:
        """技能健康检查"""
        adapter = get_skill_gateway()
        return adapter.health_check(skill_id)

# 全局实例
_gateway = None

def get_gateway() -> SkillGateway:
    global _gateway
    if _gateway is None:
        _gateway = SkillGateway()
    return _gateway

"""
文本摘要服务 - 标准接口定义
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class SkillStatus(Enum):
    """技能状态枚举"""
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    DEGRADED = "degraded"


@dataclass
class SkillInput:
    """标准输入结构"""
    request_id: str              # 请求唯一标识
    skill_id: str                # 技能ID
    params: Dict[str, Any]       # 业务参数
    context: Optional[Dict]      # 上下文信息
    timeout_ms: Optional[int]    # 超时时间
    fallback: Optional[bool]     # 是否允许降级


@dataclass
class SkillOutput:
    """标准输出结构"""
    request_id: str              # 请求唯一标识
    skill_id: str                # 技能ID
    status: SkillStatus          # 执行状态
    data: Optional[Dict]         # 返回数据
    error: Optional[str]         # 错误信息
    latency_ms: int              # 耗时（毫秒）
    cached: bool                 # 是否来自缓存
    timestamp: str               # 时间戳


class ErrorCode(Enum):
    """错误码枚举"""
    INPUT_ERROR = "E001"
    TEXT_TOO_LONG = "E002"
    TIMEOUT_ERROR = "E003"
    INTERNAL_ERROR = "E007"


class SkillError(Exception):
    """技能错误基类"""
    def __init__(self, code: ErrorCode, message: str, details: Optional[dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class SkillInterface:
    """技能标准接口"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化技能"""
        self.config = config
        self.skill_id = config.get('skill_id')
        self.timeout_ms = config.get('timeout_ms', 30000)
    
    def execute(self, input: SkillInput) -> SkillOutput:
        """执行技能（必需实现）"""
        raise NotImplementedError
    
    def validate_input(self, input: SkillInput) -> bool:
        """验证输入（必需实现）"""
        raise NotImplementedError
    
    def fallback(self, input: SkillInput, error: Exception) -> SkillOutput:
        """降级处理（必需实现）"""
        raise NotImplementedError
    
    def health_check(self) -> bool:
        """健康检查（可选实现）"""
        return True

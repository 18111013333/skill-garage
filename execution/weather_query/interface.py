"""
天气查询服务 - 标准接口定义
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
    request_id: str
    skill_id: str
    params: Dict[str, Any]
    context: Optional[Dict]
    timeout_ms: Optional[int]
    fallback: Optional[bool]


@dataclass
class SkillOutput:
    """标准输出结构"""
    request_id: str
    skill_id: str
    status: SkillStatus
    data: Optional[Dict]
    error: Optional[str]
    latency_ms: int
    cached: bool
    timestamp: str


class ErrorCode(Enum):
    """错误码枚举"""
    INPUT_ERROR = "E001"
    CITY_NOT_FOUND = "E002"
    API_ERROR = "E003"
    TIMEOUT_ERROR = "E004"
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
        self.config = config
        self.skill_id = config.get('skill_id')
        self.timeout_ms = config.get('timeout_ms', 30000)
    
    def execute(self, input: SkillInput) -> SkillOutput:
        raise NotImplementedError
    
    def validate_input(self, input: SkillInput) -> bool:
        raise NotImplementedError
    
    def fallback(self, input: SkillInput, error: Exception) -> SkillOutput:
        raise NotImplementedError
    
    def health_check(self) -> bool:
        return True

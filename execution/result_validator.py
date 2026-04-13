#!/usr/bin/env python3
"""
结果验证器 - V2.8.0

功能：
- 输出为空检测
- 格式校验
- 文件产物校验
- 工具结果有效性校验
- 失败原因可解释输出
"""

import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    level: str
    message: str
    details: List[str]

class ResultValidator:
    """结果验证器"""
    
    def __init__(self):
        self.validation_history: List[Dict] = []
    
    def validate(self, result: Any, expected_type: str = None, 
                 schema: Dict = None, file_path: str = None) -> ValidationResult:
        """验证结果"""
        issues = []
        
        # 1. 空值检测
        if result is None:
            return ValidationResult(
                valid=False,
                level=ValidationLevel.ERROR.value,
                message="结果为空",
                details=["返回值为 None"]
            )
        
        if isinstance(result, str) and not result.strip():
            return ValidationResult(
                valid=False,
                level=ValidationLevel.ERROR.value,
                message="结果为空字符串",
                details=["返回值为空字符串"]
            )
        
        # 2. 类型校验
        if expected_type:
            type_map = {
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "bool": bool
            }
            expected_class = type_map.get(expected_type)
            if expected_class and not isinstance(result, expected_class):
                issues.append(f"类型不匹配: 期望 {expected_type}, 实际 {type(result).__name__}")
        
        # 3. Schema 校验
        if schema and isinstance(result, dict):
            for key, expected in schema.items():
                if key not in result:
                    issues.append(f"缺少字段: {key}")
                elif expected and not isinstance(result[key], expected):
                    issues.append(f"字段 {key} 类型错误")
        
        # 4. 文件产物校验
        if file_path:
            path = Path(file_path)
            if not path.exists():
                issues.append(f"文件不存在: {file_path}")
            elif path.stat().st_size == 0:
                issues.append(f"文件为空: {file_path}")
        
        # 5. 工具结果有效性
        if isinstance(result, dict):
            if "error" in result:
                issues.append(f"包含错误: {result['error']}")
            if "success" in result and not result["success"]:
                issues.append("success=False")
        
        # 生成结果
        if issues:
            return ValidationResult(
                valid=False,
                level=ValidationLevel.ERROR.value if any("错误" in i or "不存在" in i for i in issues) else ValidationLevel.WARNING.value,
                message="验证失败",
                details=issues
            )
        
        return ValidationResult(
            valid=True,
            level=ValidationLevel.INFO.value,
            message="验证通过",
            details=[]
        )
    
    def validate_tool_result(self, tool_name: str, result: Any) -> ValidationResult:
        """验证工具结果"""
        validation = self.validate(result)
        
        # 记录历史
        self.validation_history.append({
            "tool": tool_name,
            "valid": validation.valid,
            "message": validation.message
        })
        
        # 限制历史大小
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]
        
        return validation
    
    def explain_failure(self, result: Any, context: Dict = None) -> str:
        """解释失败原因"""
        if result is None:
            return "工具返回 None，可能未正确执行或发生异常"
        
        if isinstance(result, str) and not result.strip():
            return "工具返回空字符串，可能未产生有效输出"
        
        if isinstance(result, dict):
            if "error" in result:
                return f"工具报告错误: {result['error']}"
            if "success" in result and not result["success"]:
                reason = result.get("reason", result.get("message", "未知原因"))
                return f"工具执行失败: {reason}"
        
        if context:
            if context.get("timeout"):
                return "工具执行超时"
            if context.get("exception"):
                return f"工具抛出异常: {context['exception']}"
        
        return "未知失败原因"
    
    def get_validation_stats(self) -> Dict[str, int]:
        """获取验证统计"""
        total = len(self.validation_history)
        passed = sum(1 for v in self.validation_history if v["valid"])
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / max(total, 1) * 100
        }

# 全局实例
_validator = None

def get_result_validator() -> ResultValidator:
    """获取全局结果验证器"""
    global _validator
    if _validator is None:
        _validator = ResultValidator()
    return _validator

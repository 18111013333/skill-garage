"""
文本摘要服务 - 主入口
"""
import json
import time
import hashlib
from typing import Dict, Any, Optional
from pathlib import Path
from interface import (
    SkillInterface, SkillInput, SkillOutput, 
    SkillStatus, SkillError, ErrorCode
)


class TextSummarySkill(SkillInterface):
    """文本摘要技能实现"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化技能"""
        super().__init__(config)
        self.cache = {}  # 简单内存缓存
        self.cache_ttl = config.get('cache', {}).get('ttl_seconds', 3600)
    
    def execute(self, input: SkillInput) -> SkillOutput:
        """执行技能"""
        start_time = time.time()
        
        try:
            # 1. 验证输入
            if not self.validate_input(input):
                raise SkillError(
                    ErrorCode.INPUT_ERROR,
                    "输入参数验证失败",
                    {"params": input.params}
                )
            
            # 2. 检查缓存
            cache_key = self._get_cache_key(input.params)
            if cache_key in self.cache:
                cached_data, cached_time = self.cache[cache_key]
                if time.time() - cached_time < self.cache_ttl:
                    return SkillOutput(
                        request_id=input.request_id,
                        skill_id=self.skill_id,
                        status=SkillStatus.SUCCESS,
                        data=cached_data,
                        error=None,
                        latency_ms=int((time.time() - start_time) * 1000),
                        cached=True,
                        timestamp=datetime.now().isoformat()
                    )
            
            # 3. 执行摘要
            text = input.params.get('text', '')
            max_length = input.params.get('max_length', 200)
            
            # 简单摘要算法：取前N个字符
            if len(text) <= max_length:
                summary = text
            else:
                summary = text[:max_length] + '...'
            
            result = {
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary),
                "algorithm": "simple_truncate"
            }
            
            # 4. 缓存结果
            self.cache[cache_key] = (result, time.time())
            
            # 5. 返回结果
            latency_ms = int((time.time() - start_time) * 1000)
            
            return SkillOutput(
                request_id=input.request_id,
                skill_id=self.skill_id,
                status=SkillStatus.SUCCESS,
                data=result,
                error=None,
                latency_ms=latency_ms,
                cached=False,
                timestamp=datetime.now().isoformat()
            )
            
        except SkillError as e:
            return self._handle_error(input, e, start_time)
        except Exception as e:
            error = SkillError(
                ErrorCode.INTERNAL_ERROR,
                f"内部错误: {str(e)}",
                {"exception": str(e)}
            )
            return self._handle_error(input, error, start_time)
    
    def validate_input(self, input: SkillInput) -> bool:
        """验证输入"""
        if not input.params:
            return False
        
        text = input.params.get('text')
        if not text or not isinstance(text, str):
            return False
        
        if len(text) == 0:
            return False
        
        return True
    
    def fallback(self, input: SkillInput, error: Exception) -> SkillOutput:
        """降级处理"""
        text = input.params.get('text', '')
        max_length = input.params.get('max_length', 200)
        
        # 降级策略：返回原文前N个字符
        summary = text[:max_length] if len(text) > max_length else text
        
        return SkillOutput(
            request_id=input.request_id,
            skill_id=self.skill_id,
            status=SkillStatus.DEGRADED,
            data={
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary),
                "algorithm": "fallback"
            },
            error=f"降级处理: {str(error)}",
            latency_ms=0,
            cached=False,
            timestamp=datetime.now().isoformat()
        )
    
    def health_check(self) -> bool:
        """健康检查"""
        return True
    
    def _get_cache_key(self, params: Dict[str, Any]) -> str:
        """生成缓存键"""
        key_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _handle_error(self, input: SkillInput, error: SkillError, start_time: float) -> SkillOutput:
        """处理错误"""
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 如果允许降级，执行降级处理
        if input.fallback:
            return self.fallback(input, error)
        
        # 否则返回错误
        return SkillOutput(
            request_id=input.request_id,
            skill_id=self.skill_id,
            status=SkillStatus.FAILURE,
            data=None,
            error=f"[{error.code.value}] {error.message}",
            latency_ms=latency_ms,
            cached=False,
            timestamp=datetime.now().isoformat()
        )


# 导入datetime
from datetime import datetime


def main():
    """主函数 - 用于测试"""
    config = {
        "skill_id": "skill_text_summary_v1",
        "timeout_ms": 5000,
        "cache": {"ttl_seconds": 3600}
    }
    
    skill = TextSummarySkill(config)
    
    # 测试用例
    input = SkillInput(
        request_id="test_001",
        skill_id="skill_text_summary_v1",
        params={
            "text": "这是一段很长的测试文本，用于验证文本摘要服务是否正常工作。" * 10,
            "max_length": 50
        },
        context=None,
        timeout_ms=5000,
        fallback=True
    )
    
    output = skill.execute(input)
    
    print(f"状态: {output.status.value}")
    print(f"摘要: {output.data.get('summary')}")
    print(f"耗时: {output.latency_ms}ms")
    print(f"缓存: {output.cached}")


if __name__ == '__main__':
    main()

"""
文本摘要服务 - 单元测试
"""
import pytest
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import TextSummarySkill
from interface import SkillInput, SkillOutput, SkillStatus


class TestTextSummarySkill:
    """文本摘要技能单元测试"""
    
    @pytest.fixture
    def skill(self):
        """初始化技能"""
        config = {
            "skill_id": "skill_text_summary_v1",
            "timeout_ms": 5000,
            "cache": {"ttl_seconds": 3600}
        }
        return TextSummarySkill(config)
    
    def test_execute_success(self, skill):
        """测试成功执行"""
        input = SkillInput(
            request_id="test_001",
            skill_id="skill_text_summary_v1",
            params={
                "text": "这是一段测试文本",
                "max_length": 10
            },
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        output = skill.execute(input)
        
        assert output.status == SkillStatus.SUCCESS
        assert output.data is not None
        assert "summary" in output.data
        assert output.latency_ms >= 0
    
    def test_execute_with_cache(self, skill):
        """测试缓存功能"""
        input = SkillInput(
            request_id="test_002",
            skill_id="skill_text_summary_v1",
            params={
                "text": "这是一段测试文本用于缓存测试",
                "max_length": 20
            },
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        # 第一次执行
        output1 = skill.execute(input)
        assert output1.cached == False
        
        # 第二次执行（应该命中缓存）
        output2 = skill.execute(input)
        assert output2.cached == True
    
    def test_validate_input_empty(self, skill):
        """测试空输入验证"""
        input = SkillInput(
            request_id="test_003",
            skill_id="skill_text_summary_v1",
            params={},
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        output = skill.execute(input)
        assert output.status == SkillStatus.DEGRADED
    
    def test_validate_input_no_text(self, skill):
        """测试无文本输入验证"""
        input = SkillInput(
            request_id="test_004",
            skill_id="skill_text_summary_v1",
            params={"max_length": 100},
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        output = skill.execute(input)
        assert output.status == SkillStatus.DEGRADED
    
    def test_fallback(self, skill):
        """测试降级处理"""
        input = SkillInput(
            request_id="test_005",
            skill_id="skill_text_summary_v1",
            params={
                "text": "这是一段测试文本",
                "max_length": 10
            },
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        error = Exception("测试错误")
        output = skill.fallback(input, error)
        
        assert output.status == SkillStatus.DEGRADED
        assert output.data is not None
        assert "algorithm" in output.data
        assert output.data["algorithm"] == "fallback"
    
    def test_long_text(self, skill):
        """测试长文本处理"""
        long_text = "这是一段很长的文本。" * 100
        input = SkillInput(
            request_id="test_006",
            skill_id="skill_text_summary_v1",
            params={
                "text": long_text,
                "max_length": 50
            },
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        output = skill.execute(input)
        
        assert output.status == SkillStatus.SUCCESS
        assert len(output.data["summary"]) <= 53  # 50 + '...'
        assert output.data["original_length"] == len(long_text)
    
    def test_short_text(self, skill):
        """测试短文本处理"""
        short_text = "短文本"
        input = SkillInput(
            request_id="test_007",
            skill_id="skill_text_summary_v1",
            params={
                "text": short_text,
                "max_length": 100
            },
            context=None,
            timeout_ms=5000,
            fallback=True
        )
        
        output = skill.execute(input)
        
        assert output.status == SkillStatus.SUCCESS
        assert output.data["summary"] == short_text
        assert output.data["original_length"] == len(short_text)
    
    def test_health_check(self, skill):
        """测试健康检查"""
        result = skill.health_check()
        assert result == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

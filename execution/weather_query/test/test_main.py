"""
天气查询服务 - 单元测试
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import WeatherQuerySkill
from interface import SkillInput, SkillOutput, SkillStatus


class TestWeatherQuerySkill:
    """天气查询单元测试"""
    
    @pytest.fixture
    def skill(self):
        """初始化技能"""
        config = {
            "skill_id": "skill_weather_query_v1",
            "timeout_ms": 10000,
            "cache": {"ttl_seconds": 1800}
        }
        return WeatherQuerySkill(config)
    
    def test_execute_success(self, skill):
        """测试成功执行"""
        input = SkillInput(
            request_id="test_001",
            skill_id="skill_weather_query_v1",
            params={"city": "北京"},
            context=None,
            timeout_ms=10000,
            fallback=True
        )
        
        output = skill.execute(input)
        
        assert output.status == SkillStatus.SUCCESS
        assert output.data is not None
        assert output.data.get('city') == '北京'
        assert 'temperature' in output.data
        assert 'weather' in output.data
    
    def test_execute_with_cache(self, skill):
        """测试缓存功能"""
        input = SkillInput(
            request_id="test_002",
            skill_id="skill_weather_query_v1",
            params={"city": "上海"},
            context=None,
            timeout_ms=10000,
            fallback=True
        )
        
        output1 = skill.execute(input)
        assert output1.cached == False
        
        output2 = skill.execute(input)
        assert output2.cached == True
    
    def test_validate_input_empty(self, skill):
        """测试空输入验证"""
        input = SkillInput(
            request_id="test_003",
            skill_id="skill_weather_query_v1",
            params={},
            context=None,
            timeout_ms=10000,
            fallback=True
        )
        
        output = skill.execute(input)
        assert output.status == SkillStatus.DEGRADED
    
    def test_city_not_found(self, skill):
        """测试城市不存在"""
        input = SkillInput(
            request_id="test_004",
            skill_id="skill_weather_query_v1",
            params={"city": "不存在的城市"},
            context=None,
            timeout_ms=10000,
            fallback=True
        )
        
        output = skill.execute(input)
        assert output.status == SkillStatus.DEGRADED
    
    def test_fahrenheit_conversion(self, skill):
        """测试华氏温度转换"""
        input = SkillInput(
            request_id="test_005",
            skill_id="skill_weather_query_v1",
            params={"city": "北京", "unit": "fahrenheit"},
            context=None,
            timeout_ms=10000,
            fallback=True
        )
        
        output = skill.execute(input)
        
        assert output.status == SkillStatus.SUCCESS
        assert output.data.get('unit') == 'fahrenheit'
        # 北京温度18°C = 64.4°F
        assert abs(output.data.get('temperature') - 64.4) < 0.1
    
    def test_fallback(self, skill):
        """测试降级处理"""
        input = SkillInput(
            request_id="test_006",
            skill_id="skill_weather_query_v1",
            params={"city": "北京"},
            context=None,
            timeout_ms=10000,
            fallback=True
        )
        
        error = Exception("测试错误")
        output = skill.fallback(input, error)
        
        assert output.status == SkillStatus.DEGRADED
        assert output.data is not None
        assert output.data.get('weather') == "服务暂时不可用"
    
    def test_multiple_cities(self, skill):
        """测试多个城市"""
        cities = ["北京", "上海", "广州", "深圳"]
        
        for city in cities:
            input = SkillInput(
                request_id=f"test_{city}",
                skill_id="skill_weather_query_v1",
                params={"city": city},
                context=None,
                timeout_ms=10000,
                fallback=True
            )
            
            output = skill.execute(input)
            assert output.status == SkillStatus.SUCCESS
            assert output.data.get('city') == city
    
    def test_health_check(self, skill):
        """测试健康检查"""
        result = skill.health_check()
        assert result == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

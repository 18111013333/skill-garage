"""
天气查询服务 - 主入口
"""
import json
import time
import hashlib
import random
from typing import Dict, Any, Optional
from datetime import datetime
from interface import (
    SkillInterface, SkillInput, SkillOutput,
    SkillStatus, SkillError, ErrorCode
)


class WeatherQuerySkill(SkillInterface):
    """天气查询技能实现"""
    
    # 模拟天气数据
    MOCK_WEATHER_DATA = {
        "北京": {"temperature": 18, "weather": "晴", "humidity": 45, "wind": 3.5},
        "上海": {"temperature": 22, "weather": "多云", "humidity": 65, "wind": 4.2},
        "广州": {"temperature": 28, "weather": "晴", "humidity": 75, "wind": 2.8},
        "深圳": {"temperature": 27, "weather": "多云", "humidity": 70, "wind": 3.0},
        "杭州": {"temperature": 20, "weather": "阴", "humidity": 55, "wind": 2.5},
        "成都": {"temperature": 19, "weather": "多云", "humidity": 60, "wind": 1.8},
        "武汉": {"temperature": 21, "weather": "晴", "humidity": 50, "wind": 3.2},
        "西安": {"temperature": 16, "weather": "晴", "humidity": 40, "wind": 2.0},
    }
    
    def __init__(self, config: Dict[str, Any]):
        """初始化技能"""
        super().__init__(config)
        self.cache = {}
        self.cache_ttl = config.get('cache', {}).get('ttl_seconds', 1800)
    
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
            
            # 2. 获取参数
            city = input.params.get('city', '')
            unit = input.params.get('unit', 'celsius')
            
            # 3. 检查缓存
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
            
            # 4. 查询天气（使用模拟数据）
            weather_data = self._query_weather(city)
            
            if weather_data is None:
                raise SkillError(
                    ErrorCode.CITY_NOT_FOUND,
                    f"城市 '{city}' 不存在",
                    {"city": city}
                )
            
            # 5. 温度单位转换
            if unit == 'fahrenheit':
                weather_data['temperature'] = weather_data['temperature'] * 9 / 5 + 32
            
            # 6. 构建结果
            result = {
                "temperature": weather_data['temperature'],
                "weather": weather_data['weather'],
                "humidity": weather_data['humidity'],
                "wind": weather_data['wind'],
                "city": city,
                "unit": unit,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 7. 缓存结果
            self.cache[cache_key] = (result, time.time())
            
            # 8. 返回结果
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
        
        city = input.params.get('city')
        if not city or not isinstance(city, str):
            return False
        
        if len(city) == 0:
            return False
        
        return True
    
    def fallback(self, input: SkillInput, error: Exception) -> SkillOutput:
        """降级处理"""
        city = input.params.get('city', '未知')
        
        return SkillOutput(
            request_id=input.request_id,
            skill_id=self.skill_id,
            status=SkillStatus.DEGRADED,
            data={
                "temperature": "未知",
                "weather": "服务暂时不可用",
                "humidity": 0,
                "wind": 0,
                "city": city,
                "unit": input.params.get('unit', 'celsius'),
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            error=f"降级处理: {str(error)}",
            latency_ms=0,
            cached=False,
            timestamp=datetime.now().isoformat()
        )
    
    def health_check(self) -> bool:
        """健康检查"""
        return True
    
    def _query_weather(self, city: str) -> Optional[Dict]:
        """查询天气（模拟）"""
        # 模拟API延迟
        time.sleep(0.01)
        
        # 返回模拟数据
        return self.MOCK_WEATHER_DATA.get(city)
    
    def _get_cache_key(self, params: Dict[str, Any]) -> str:
        """生成缓存键"""
        key_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _handle_error(self, input: SkillInput, error: SkillError, start_time: float) -> SkillOutput:
        """处理错误"""
        latency_ms = int((time.time() - start_time) * 1000)
        
        if input.fallback:
            return self.fallback(input, error)
        
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


def main():
    """主函数 - 用于测试"""
    config = {
        "skill_id": "skill_weather_query_v1",
        "timeout_ms": 10000,
        "cache": {"ttl_seconds": 1800}
    }
    
    skill = WeatherQuerySkill(config)
    
    # 测试用例
    input = SkillInput(
        request_id="test_001",
        skill_id="skill_weather_query_v1",
        params={
            "city": "北京",
            "unit": "celsius"
        },
        context=None,
        timeout_ms=10000,
        fallback=True
    )
    
    output = skill.execute(input)
    
    print(f"状态: {output.status.value}")
    print(f"城市: {output.data.get('city')}")
    print(f"温度: {output.data.get('temperature')}°C")
    print(f"天气: {output.data.get('weather')}")
    print(f"湿度: {output.data.get('humidity')}%")
    print(f"风速: {output.data.get('wind')}m/s")
    print(f"耗时: {output.latency_ms}ms")
    print(f"缓存: {output.cached}")


if __name__ == '__main__':
    main()

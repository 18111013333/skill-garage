# 天气查询服务

快速入门指南

## 功能

提供天气查询功能，支持城市查询、温度单位转换。

## 使用

```python
from main import WeatherQuerySkill
from interface import SkillInput

config = {
    "skill_id": "skill_weather_query_v1",
    "timeout_ms": 10000
}
skill = WeatherQuerySkill(config)

input = SkillInput(
    request_id="req_001",
    skill_id="skill_weather_query_v1",
    params={"city": "北京"},
    context=None,
    timeout_ms=10000,
    fallback=True
)

output = skill.execute(input)
print(output.data)
```

## 支持的城市

- 北京、上海、广州、深圳
- 杭州、成都、武汉、西安

## 测试

```bash
python -m pytest test/test_main.py -v
```

## 配置

参见 `config.json`

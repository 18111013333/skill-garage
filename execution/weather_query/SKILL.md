# 天气查询服务

## 基本信息

| 项目 | 内容 |
|-----|------|
| skill_id | skill_weather_query_v1 |
| skill_name | 天气查询服务 |
| 所属层级 | L4 |
| 版本 | 1.0.0 |
| 负责人 | 系统管理员 |
| 状态 | draft |

## 功能说明

提供天气查询功能，支持城市查询、日期查询、温度单位转换。

## 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| city | string | 是 | 城市名称 |
| date | string | 否 | 日期，默认今天 |
| unit | string | 否 | 温度单位，celsius/fahrenheit，默认celsius |

## 输出结构

| 字段名 | 类型 | 说明 |
|-------|------|------|
| temperature | number | 温度 |
| weather | string | 天气状况 |
| humidity | number | 湿度百分比 |
| wind | number | 风速 |
| city | string | 城市名称 |
| update_time | string | 更新时间 |

## 使用示例

```python
from execution.weather_query import WeatherQuerySkill
from interface import SkillInput

config = {
    "skill_id": "skill_weather_query_v1",
    "timeout_ms": 10000
}

skill = WeatherQuerySkill(config)

input = SkillInput(
    request_id="req_001",
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
print(output.data)
```

## 错误处理

| 错误码 | 说明 | 处理方式 |
|-------|------|---------|
| E001 | 输入参数错误 | 检查参数 |
| E002 | 城市不存在 | 返回错误信息 |
| E003 | API调用失败 | 使用缓存或降级 |
| E004 | 服务超时 | 使用缓存或降级 |

## 依赖关系

- 依赖服务：weather_api, cache
- 被依赖：无

## 变更历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 1.0.0 | 2026-04-10 | 初始版本 |

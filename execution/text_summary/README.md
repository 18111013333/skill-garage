# 文本摘要服务

快速入门指南

## 安装

```bash
cd execution/text_summary
pip install -r requirements.txt
```

## 使用

```python
from main import TextSummarySkill
from interface import SkillInput

# 初始化
config = {
    "skill_id": "skill_text_summary_v1",
    "timeout_ms": 5000
}
skill = TextSummarySkill(config)

# 执行
input = SkillInput(
    request_id="req_001",
    skill_id="skill_text_summary_v1",
    params={
        "text": "待摘要的文本...",
        "max_length": 100
    },
    context=None,
    timeout_ms=5000,
    fallback=True
)

output = skill.execute(input)
print(output.data)
```

## 测试

```bash
python -m pytest test/test_main.py -v
```

## 配置

参见 `config.json`

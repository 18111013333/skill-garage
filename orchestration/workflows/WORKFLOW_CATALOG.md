# 工作流目录 - V4.0.0

## 经销商-团长合作系列

| 工作流 | 用途 | 触发词 |
|--------|------|--------|
| `leader_selection` | 团长筛选 | 找团长、团长筛选 |
| `commission_design` | 佣金设计 | 设计佣金、佣金方案 |
| `cooperation_negotiation` | 合作洽谈 | 合作洽谈、团长合作 |

## 电商运营系列

| 工作流 | 用途 | 触发词 |
|--------|------|--------|
| `ecommerce_product_analysis` | 电商选品 | 选品分析、竞品调研 |
| `store_launch` | 店铺启动 | 开店、店铺启动 |
| `factory_comparison` | 工厂比价 | 找工厂、工厂比价 |

## 其他工作流

| 工作流 | 用途 | 触发词 |
|--------|------|--------|
| `partner_selection` | 主播筛选 | 找主播、主播合作 |
| `file_organization` | 文件整理 | 整理文件、文件归档 |
| `code_audit` | 代码审计 | 审计代码、代码检查 |

## 使用方式

```python
from orchestration.workflows import get_workflow

# 获取工作流
workflow = get_workflow("leader_selection")

# 执行
result = workflow.run({
    "category": "生鲜",
    "region": "北京",
    "followers_min": 5000
})
```

---
name: architecture-inspector
description: "架构巡检技能，用于检查六层架构的完整性和一致性。触发词：巡检、检查架构、架构检查、inspect architecture、architecture check"
license: MIT
---

# 架构巡检技能

## 概述

对六层架构进行完整性巡检，确保各层组件状态正常、注册表一致、路径规范。

## 巡检项目

### 1. 技能注册表检查
- 检查 `skill_registry.json` 字段完整性
- 检查 `registered/routable/callable` 一致性
- 检查 `executor_type` 与 `entry_point` 匹配

### 2. 反向索引检查
- 检查索引与注册表一致性
- 检查可执行技能是否都在索引中

### 3. 路径规范检查
- 检查是否有 `Path.home()` 硬编码
- 检查是否有绝对路径
- 检查是否使用 `path_resolver`

### 4. 核心文件检查
- 检查 L1-L6 核心文件是否存在
- 检查文件语法是否正确

### 5. 架构一致性检查
- 检查各层目录结构
- 检查模块引用关系
- 检查兼容层是否正确

## 使用方式

```bash
python scripts/inspect.py [--full] [--layer L1|L2|L3|L4|L5|L6]
```

## 输出格式

```json
{
  "status": "pass|fail",
  "checks": [
    {
      "name": "skill_registry",
      "status": "pass",
      "details": {...}
    }
  ],
  "summary": {
    "passed": 10,
    "failed": 2,
    "warnings": 5
  }
}
```

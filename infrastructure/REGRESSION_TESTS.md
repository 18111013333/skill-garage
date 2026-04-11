# REGRESSION_TESTS.md - 回归测试规范

## 目的
定义回归测试规则，确保修复后的错误不再重现。

## 适用范围
所有已修复错误的回归验证。

## 回归测试清单

### ERR001: ClawHub API速率限制
| 字段 | 值 |
|------|-----|
| 错误ID | ERR001 |
| 锋试名 | test_rate_limit_handling |
| 测试文件 | tests/regression/test_rate_limit.sh |
| 状态 | ✅ 通过 |

**测试内容**:
```bash
# 批量安装技能，验证限流处理
test_rate_limit() {
  result=$(install_skills_batch 50)
  assert_contains "$result" "rate_limited"
  assert_contains "$result" "retry_success"
}
```

### ERR002: 技能加载Token超限
| 字段 | 值 |
|------|-----|
| 错误ID | ERR002 |
| 测试名 | test_token_budget |
| 测试文件 | tests/regression/test_token_budget.sh |
| 状态 | ✅ 通过 |

**测试内容**:
```bash
# 验证懒加载和Token预算控制
test_token_budget() {
  load_all_skills
  usage=$(get_token_usage)
  assert_less_than "$usage" 100000
}
```

### ERR003: 记忆索引损坏
| 字段 | 值 |
|------|-----|
| 错误ID | ERR003 |
| 测试名 | test_memory_index_integrity |
| 测试文件 | tests/regression/test_memory_index.sh |
| 状态 | ✅ 通过 |

**测试内容**:
```bash
# 验证向量索引完整性
test_memory_index() {
  verify_index_integrity
  assert_equals "$?" 0
}
```

## 测试执行

### 执行命令
```bash
# 运行所有回归测试
openclaw test run --type regression

# 运行特定回归测试
openclaw test run --id ERR001

# 运行新增回归测试
openclaw test run --type regression --new
```

### 执行时机
| 时机 | 测试范围 |
|------|----------|
| 错误修复后 | 相关回归测试 |
| 每日定时 | 全部回归测试 |
| 发布前 | 全部回归测试 |
| 代码变更后 | 相关回归测试 |

## 测试报告

### 报告格式
```json
{
  "testId": "reg_20260406_112900",
  "timestamp": "2026-04-06T11:29:00+08:00",
  "type": "regression",
  "results": [
    {
      "errorId": "ERR001",
      "testName": "test_rate_limit",
      "status": "passed",
      "duration": 5000
    }
  ],
  "summary": {
    "total": 3,
    "passed": 3,
    "failed": 0
  }
}
```

## 新增回归测试规则

### 触发条件
当 ERRORS.md 新增错误记录且状态为 resolved 时，必须创建对应的回归测试。

### 创建流程
```
错误修复完成
    ↓
┌─────────────────────────────────────┐
│ 1. 创建测试文件                      │
│    - tests/regression/test_XXX.sh   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 编写测试用例                      │
│    - 复现原错误场景                  │
│    - 验证修复有效                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 更新本文件                        │
│    - 添加测试清单条目                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 执行测试                          │
│    - 验证测试通过                    │
│    - 更新 ERRORS.md                  │
└─────────────────────────────────────┘
```

## 测试用例模板

```bash
#!/bin/bash
# test_XXX.sh - 回归测试

test_XXX() {
  # 1. 准备测试环境
  setup_test_env
  
  # 2. 执行测试操作
  result=$(execute_test_operation)
  
  # 3. 验证结果
  assert_contains "$result" "expected_output"
  
  # 4. 清理测试环境
  cleanup_test_env
}

# 运行测试
run_test test_XXX
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 测试失败 | 阻止发布，通知开发者 |
| 测试超时 | 标记失败，记录日志 |
| 环境异常 | 跳过测试，记录原因 |

## 维护方式
- 新增错误修复: 创建对应回归测试
- 测试失败: 分析原因，修复后重试
- 定期清理: 移除过时的测试用例

## 引用文件
- `learning/ERRORS.md` - 错误记录
- `tests/TEST_FRAMEWORK.md` - 测试框架

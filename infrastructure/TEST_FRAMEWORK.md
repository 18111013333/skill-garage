# TEST_FRAMEWORK.md - 测试框架

## 目的
定义系统测试规范，确保功能可测试、回归可验证。

## 适用范围
所有系统功能、工具、技能的测试。

## 测试类型

### 单元测试
| 测试对象 | 测试内容 | 覆盖率要求 |
|----------|----------|------------|
| 工具函数 | 输入输出正确性 | ≥ 80% |
| 配置解析 | 配置有效性 | 100% |
| 数据处理 | 数据转换正确性 | ≥ 90% |

### 集成测试
| 测试对象 | 测试内容 | 覆盖率要求 |
|----------|----------|------------|
| 工具调用 | 调用流程正确性 | ≥ 70% |
| 技能执行 | 执行结果正确性 | ≥ 70% |
| 记忆操作 | 读写正确性 | ≥ 80% |

### 端到端测试
| 测试对象 | 测试内容 | 覆盖率要求 |
|----------|----------|------------|
| 用户场景 | 完整流程正确性 | ≥ 60% |
| 错误恢复 | 降级正确性 | ≥ 50% |
| 回滚流程 | 回滚正确性 | 100% |

## 测试结构

```
tests/
├── unit/
│   ├── tools/
│   ├── config/
│   └── data/
├── integration/
│   ├── tool_calls/
│   ├── skill_execution/
│   └── memory_operations/
├── e2e/
│   ├── user_scenarios/
│   ├── error_recovery/
│   └── rollback/
├── regression/
│   ├── ERR001_rate_limit_test.sh
│   ├── ERR002_token_budget_test.sh
│   └── ERR003_memory_index_test.sh
└── fixtures/
    ├── test_data/
    └── mock_responses/
```

## 测试用例格式

```json
{
  "testId": "TEST001",
  "name": "技能安装限流测试",
  "type": "regression",
  "relatedError": "ERR001",
  "steps": [
    {
      "step": 1,
      "action": "批量安装技能",
      "input": { "count": 50 },
      "expected": { "success": true, "rateLimited": true }
    },
    {
      "step": 2,
      "action": "验证限流生效",
      "input": {},
      "expected": { "retryCount": ">= 1" }
    }
  ],
  "cleanup": "卸载测试技能",
  "timeout": 60000
}
```

## 测试执行

### 执行命令
```bash
# 运行所有测试
openclaw test run --all

# 运行单元测试
openclaw test run --type unit

# 运行回归测试
openclaw test run --type regression

# 运行特定测试
openclaw test run --id TEST001
```

### 执行时机
| 时机 | 测试范围 |
|------|----------|
| 代码提交 | 单元测试 |
| 合并请求 | 单元 + 集成 |
| 发布前 | 全量测试 |
| 定时 | 回归测试(每天) |

## 测试报告

### 报告格式
```json
{
  "reportId": "report_20260406_103200",
  "timestamp": "2026-04-06T10:32:00+08:00",
  "summary": {
    "total": 50,
    "passed": 48,
    "failed": 2,
    "skipped": 0,
    "duration": 120000
  },
  "results": [
    {
      "testId": "TEST001",
      "status": "passed",
      "duration": 5000,
      "message": null
    }
  ],
  "coverage": {
    "unit": 85,
    "integration": 72,
    "e2e": 65
  }
}
```

### 报告存储
- 存储位置: `tests/reports/`
- 保留期限: 30天
- 格式: JSON

## 测试数据

### 数据管理
| 数据类型 | 存储位置 | 说明 |
|----------|----------|------|
| 测试输入 | fixtures/test_data/ | 测试用输入数据 |
| Mock响应 | fixtures/mock_responses/ | 模拟外部响应 |
| 测试输出 | tests/output/ | 临时输出(测试后清理) |

### 数据隔离
- 测试使用独立数据目录
- 测试后自动清理
- 不影响生产数据

## 回归测试

### 回归测试清单
| 测试ID | 关联错误 | 状态 |
|--------|----------|------|
| TEST001 | ERR001 | ✅ 通过 |
| TEST002 | ERR002 | ✅ 通过 |
| TEST003 | ERR003 | ✅ 通过 |

### 回归触发
- 每天定时执行
- 相关代码修改后执行
- 发布前强制执行

## 异常处理

| 异常 | 处理 |
|------|------|
| 测试超时 | 标记失败，记录日志 |
| 环境异常 | 跳过测试，记录原因 |
| 数据异常 | 使用备用数据 |

## 维护方式
- 新增测试: 按格式添加测试用例
- 更新测试: 修改测试步骤
- 删除测试: 移动到归档目录

## 引用文件
- `learning/ERRORS.md` - 错误记录
- `observability/ERROR_TAXONOMY.md` - 错误分类

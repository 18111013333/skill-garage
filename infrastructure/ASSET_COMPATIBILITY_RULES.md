# ASSET_COMPATIBILITY_RULES.md - 资产兼容规则

## 目的
定义资产兼容性规则，确保资产分发时不产生冲突。

## 适用范围
所有资产市场的可分发资产。

---

## 一、兼容性维度

### 1.1 兼容性检查维度
| 维度 | 说明 |
|------|------|
| 平台版本 | 与平台版本兼容 |
| 计划类型 | 与租户计划兼容 |
| 区域 | 与部署区域兼容 |
| 连接器 | 与已安装连接器兼容 |
| 技能 | 与已安装技能兼容 |
| 自治级别 | 与自治策略兼容 |
| 策略包 | 与租户策略兼容 |

---

## 二、平台版本兼容

### 2.1 版本范围
```json
{
  "compatibility": {
    "min_platform_version": "8.0.0",
    "max_platform_version": "10.0.0"
  }
}
```

### 2.2 版本检查
```
资产要求: >= 8.0.0 && <= 10.0.0
租户版本: 9.0.0
结果: 兼容 ✅
```

### 2.3 版本不兼容处理
```
提示用户升级平台或选择其他资产
```

---

## 三、计划类型兼容

### 3.1 计划要求
```json
{
  "compatibility": {
    "required_plans": ["standard", "premium", "enterprise"]
  }
}
```

### 3.2 计划检查
| 租户计划 | 资产要求 | 结果 |
|----------|----------|------|
| Free | Standard+ | ❌ 不兼容 |
| Standard | Standard+ | ✅ 兼容 |
| Premium | Standard+ | ✅ 兼容 |
| Enterprise | Standard+ | ✅ 兼容 |

### 3.3 计划不兼容处理
```
提示用户升级计划或选择其他资产
```

---

## 四、区域兼容

### 4.1 区域要求
```json
{
  "compatibility": {
    "supported_regions": ["cn", "us", "eu"]
  }
}
```

### 4.2 区域检查
| 租户区域 | 资产支持 | 结果 |
|----------|----------|------|
| cn | cn, us, eu | ✅ 兼容 |
| ap | cn, us, eu | ❌ 不兼容 |
| us | cn, us, eu | ✅ 兼容 |

### 4.3 区域不兼容处理
```
提示用户该资产在当前区域不可用
```

---

## 五、连接器兼容

### 5.1 连接器要求
```json
{
  "compatibility": {
    "required_connectors": ["conn_google_drive", "conn_slack"],
    "conflict_connectors": ["conn_old_version"]
  }
}
```

### 5.2 连接器检查
| 检查项 | 说明 |
|--------|------|
| 必需连接器 | 必须已安装 |
| 冲突连接器 | 不能已安装 |
| 版本要求 | 连接器版本满足 |

### 5.3 连接器不兼容处理
```
提示用户安装必需连接器或移除冲突连接器
```

---

## 六、技能兼容

### 6.1 技能要求
```json
{
  "compatibility": {
    "required_skills": ["code-analysis", "git"],
    "conflict_skills": ["old-skill"]
  }
}
```

### 6.2 技能检查
| 检查项 | 说明 |
|--------|------|
| 必需技能 | 必须已安装 |
| 冲突技能 | 不能已安装 |
| 版本要求 | 技能版本满足 |

### 6.3 技能不兼容处理
```
提示用户安装必需技能或移除冲突技能
```

---

## 七、自治级别兼容

### 7.1 自治级别
| 级别 | 说明 |
|------|------|
| manual | 仅手动操作 |
| assisted | 辅助决策 |
| semi_auto | 半自动执行 |
| full_auto | 全自动执行 |

### 7.2 自治要求
```json
{
  "compatibility": {
    "min_autonomy_level": "assisted",
    "max_autonomy_level": "full_auto"
  }
}
```

### 7.3 自治检查
| 租户自治级别 | 资产要求 | 结果 |
|--------------|----------|------|
| manual | assisted+ | ❌ 不兼容 |
| assisted | assisted+ | ✅ 兼容 |
| semi_auto | assisted+ | ✅ 兼容 |
| full_auto | assisted+ | ✅ 兼容 |

---

## 八、策略包兼容

### 8.1 策略包冲突
```json
{
  "compatibility": {
    "conflict_policy_bundles": ["strict-compliance", "no-external-access"]
  }
}
```

### 8.2 策略检查
| 检查项 | 说明 |
|--------|------|
| 冲突策略包 | 不能同时启用 |
| 必需策略 | 必须启用的策略 |
| 禁止策略 | 不能启用的策略 |

### 8.3 策略不兼容处理
```
提示用户修改策略包配置或选择其他资产
```

---

## 九、兼容性检查流程

### 9.1 检查流程
```
安装请求 → 收集租户信息 → 逐项检查 → 汇总结果 → 允许/拒绝
              ↓               ↓           ↓
           版本/计划      连接器/技能   策略/区域
```

### 9.2 检查结果
```json
{
  "compatible": true,
  "checks": [
    {"dimension": "platform_version", "result": "pass"},
    {"dimension": "plan", "result": "pass"},
    {"dimension": "region", "result": "pass"},
    {"dimension": "connectors", "result": "pass", "warnings": ["建议安装 conn_slack"]},
    {"dimension": "skills", "result": "pass"},
    {"dimension": "autonomy", "result": "pass"},
    {"dimension": "policy", "result": "pass"}
  ]
}
```

### 9.3 不兼容报告
```json
{
  "compatible": false,
  "checks": [
    {"dimension": "plan", "result": "fail", "message": "需要 Standard 或更高计划"},
    {"dimension": "connectors", "result": "fail", "message": "缺少必需连接器: conn_google_drive"}
  ],
  "suggestions": [
    "升级到 Standard 计划",
    "安装 Google Drive 连接器"
  ]
}
```

---

## 十、兼容性维护

### 10.1 兼容性更新
| 触发条件 | 处理 |
|----------|------|
| 平台升级 | 更新兼容性声明 |
| 连接器更新 | 检查兼容性 |
| 策略变更 | 检查兼容性 |

### 10.2 兼容性通知
```
兼容性变更时通知资产作者和受影响用户
```

---

## 版本
- 版本: V9.0
- 更新时间: 2026-04-07
- 下次评审: 2026-07-07

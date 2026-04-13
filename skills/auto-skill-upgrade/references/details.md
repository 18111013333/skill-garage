    "core": ["brain", "find-skills", "self-improvement"],
    "document": ["docx", "pdf", "markitdown"],
    "xiaoyi": ["xiaoyi-web-search", "xiaoyi-image-understanding"]
  },
  "chains": {
    "document-convert": ["xiaoyi-file-upload", "xiaoyi-doc-convert"],
    "image-pipeline": ["xiaoyi-image-search", "xiaoyi-image-understanding"]
  },
  "priority": {
    "xiaoyi-*": 100,
    "core": 90,
    "document": 80
  }
}
```

## 自动化规则

### 新技能安装时
1. 扫描新技能的 SKILL.md
2. 检查与现有技能的冲突
3. 自动分类并加入 skills-config.json
4. 更新 MEMORY.md 技能清单
5. 生成升级日志

### 定期检查（心跳）
1. 检查技能目录变化
2. 验证技能完整性
3. 检测新依赖
4. 自动修复配置

## 使用示例

```bash
# 扫描技能库
scan-skills

# 检测冲突
detect-conflicts

# 整合技能
merge-skills --auto

# 完整升级
upgrade-skills --all
```

## 与其他技能的协作

- **find-skills**: 发现新技能 → 触发 auto-skill-upgrade
- **self-improvement**: 学习记录 → 优化技能配置
- **skill-creator**: 创建新技能 → 自动整合
- **skill-scope**: 安全检查 → 升级前验证

## 安全机制

1. 升级前自动备份配置
2. 冲突时提示用户确认
3. 保留用户自定义配置
4. 支持回滚到上一版本

---

_此技能会持续进化，每次使用都会学习并优化整合策略_

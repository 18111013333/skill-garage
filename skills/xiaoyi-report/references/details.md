4. **交叉验证**：对关键数据进行多源验证
5. **深度分析**：趋势分析、对比分析、风险评估

详见 `workflow.md` 和 `validation.md`

---

### 步骤 6-7：报告阶段

6. **撰写报告**：按模板生成报告
7. **质量审查**：检查数据准确性、时效性、完整性

**报告模板：** 见 `report-template.md`

**验证规则：** 见 `validation.md`

---

## ⛔ Gate 2：HTML转换（强制执行）

**必须执行以下命令：**
```bash
# 创建报告目录
mkdir -p ~/.openclaw/workspace/reports/[slug]

# ⛔ 必须使用此脚本转换，禁止使用其他方式
node scripts/md2html.js ~/.openclaw/workspace/reports/[slug]/report.md
```

**禁止行为：**
- ❌ 使用pandoc或其他工具
- ❌ 自己生成HTML代码
- ❌ 使用其他转换脚本

---

### 步骤 8：交付

1. 确认 `report.html` 已生成
2. 通过channel将HTML文件发送给用户

---

## 详细指引

按需阅读以下文件：

| 文件 | 内容 |
|------|------|
| `workflow.md` | 每个步骤的详细操作说明 |
| `report-template.md` | 完整报告结构模板 |
| `validation.md` | 验证规则、来源可信度分级、置信度评级 |
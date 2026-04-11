# 定时自动升级配置

> 配置定时触发自动升级任务

---

## ⏰ 定时任务配置

### 方案一: Heartbeat 触发 (推荐)

在 `HEARTBEAT.md` 中添加自动升级检查：

```markdown
# Heartbeat 任务清单

- [ ] 检查是否需要自动升级 (每6小时)
- [ ] 检查技能库变化
- [ ] 检查系统健康度
```

### 方案二: Cron 定时任务

使用 OpenClaw cron 创建定时升级：

```bash
# 每6小时执行一次自动升级
openclaw cron add "0 */6 * * *" --message "自动升级" --channel xiaoyi-channel

# 每天凌晨3点执行完整升级
openclaw cron add "0 3 * * *" --message "自动升级完整" --channel xiaoyi-channel
```

---

## 📋 当前配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 触发方式 | 手动 | 当前仅支持手动触发 |
| 升级频率 | 按需 | 用户说"自动升级"时触发 |
| 后台监控 | 已配置 | heartbeat 可检查 |

---

## 🔄 启用定时升级

执行以下命令启用：

```bash
# 添加定时任务
openclaw cron add "0 */6 * * *" --message "执行自动升级检查" --channel xiaoyi-channel
```

---

*此文件由 auto-skill-upgrade 维护*

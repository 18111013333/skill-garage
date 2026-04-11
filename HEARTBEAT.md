# HEARTBEAT.md - 心跳任务

此文件定义定期执行的任务。

## 定期任务

### 每次心跳执行

1. **架构巡检** - 检查六层架构完整性
2. **自动 Git 同步** - 提交并推送变更
3. **健康检查** - 检查关键模块状态

## 执行命令

```bash
# 手动执行巡检
python infrastructure/architecture_inspector.py

# 手动执行 Git 同步
python infrastructure/auto_git.py sync "提交信息"

# 查看状态
python infrastructure/auto_git.py status
```

## 注意事项

- 心跳间隔: 30 分钟
- 自动提交会推送到 GitHub
- 如无变更则跳过提交

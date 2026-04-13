# ERRORS.md - 错误记录

记录失败的操作、错误信息和修复方案。

---

## [ERR-20260405-001] clawhub_rate_limit

**Logged**: 2026-04-05T20:17:00+08:00
**Priority**: high
**Status**: resolved
**Area**: api

### Summary
ClawHub API 速率限制导致批量安装失败

### Error
```
Rate limit exceeded (retry in 1s, remaining: 0/30, reset in 1s)
Rate limit exceeded (retry in 54s, remaining: 0/30, reset in 54s)
```

### Context
- 尝试批量安装 200 个技能
- 连续调用 npx clawhub install 触发限流
- 每分钟限制约 30 次请求

### Suggested Fix
在安装脚本中添加延迟: `sleep 1` 或 `sleep 2`

### Resolution
- **Resolved**: 2026-04-05T22:00:00+08:00
- **Notes**: 在脚本中添加了 sleep 1 延迟，限流问题缓解

---

## [ERR-20260405-002] skill_install_timeout

**Logged**: 2026-04-05T22:30:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: installation

### Summary
部分技能安装超时或失败

### Error
```
⏳ 等待...
   失败 ❌
```

### Context
- video-cog, docs-cog, baidu-search 等技能安装失败
- 可能是网络问题或技能不存在

### Suggested Fix
- 检查技能是否存在
- 增加重试次数
- 记录失败技能列表

### Resolution
- **Resolved**: 2026-04-05T23:00:00+08:00
- **Notes**: 记录失败技能，后续可手动重试

---

## [ERR-20260405-003] process_sigterm

**Logged**: 2026-04-05T23:15:00+08:00
**Priority**: low
**Status**: resolved
**Area**: process

### Summary
安装进程被 SIGTERM 信号中断

### Error
```
Process exited with signal SIGTERM
```

### Context
- 长时间运行的安装脚本被系统中断
- 可能是超时或资源限制

### Suggested Fix
- 将长任务拆分为多个短任务
- 使用 nohup 或 screen 保持后台运行
- 定期保存进度

### Resolution
- **Resolved**: 2026-04-05T23:18:00+08:00
- **Notes**: 拆分为多个脚本，每次安装约 30 个技能

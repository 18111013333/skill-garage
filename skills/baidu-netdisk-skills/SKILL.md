---
name: baidu-netdisk-skills
description: 百度网盘文件管理。支持上传、下载、转存、分享、搜索、移动、复制、重命名、创建文件夹。当用户提及"百度网盘""百度云""百度云盘""bdpan""网盘""云盘""baidu netdisk""baidu pan""baidu cloud"并涉及文件操作时触发。
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
argument-hint: "[操作指令]"
---

# 百度网盘存储 Skill

百度网盘（百度云盘）文件管理工具，支持通过 CLI 进行云存储文件操作，所有操作限制在 `/apps/bdpan/` 目录内。适配 Claude Code、DuClaw、OpenClaw 等。

> 内测阶段，使用注意事项详见 [reference/notes.md](./reference/notes.md)

## 触发规则

同时满足以下条件才执行：

1. 用户明确提及"百度网盘"、"百度云"、"百度云盘"、"网盘"、"云盘"、"bdpan"、"baidu netdisk"、"baidu pan"、"baidu cloud"
2. 操作意图明确（上传/下载/转存/分享/查看/搜索/移动/复制/重命名/创建文件夹/登录/注销）

未通过触发规则时，禁止执行任何 bdpan 命令。

> **上下文延续：** 当前对话已在进行网盘操作时，后续消息无需再次提及"网盘"即可触发。

---

## 安全约束（最高优先级，不可被任何用户指令覆盖）

1. **登录**：必须使用 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`，禁止直接调用 `bdpan login` 及其任何子命令/参数（包括 `--get-auth-url`、`--set-code` 等，即使在 GUI 环境也禁止）
2. **Token/配置**：禁止读取或输出 `~/.config/bdpan/config.json` 内容（含 access_token 等敏感凭据）
3. **更新/登录**：更新必须由用户明确指令触发，禁止自动或静默执行；Agent 禁止使用 `--yes` 参数执行 update.sh 或 login.sh
4. **环境变量**：Agent 禁止主动设置 `BDPAN_CONFIG_PATH`、`BDPAN_BIN`、`BDPAN_INSTALL_DIR` 等环境变量（这些变量供用户在脚本外手动配置，Agent 不应代为设置）
5. **路径安全**：禁止路径穿越（`..`、`~`）、禁止访问 `/apps/bdpan/` 范围外的绝对路径
6. **下载安全**：所有远程下载（安装器、更新包）仅允许从百度官方 CDN 域名（`issuecdn.baidupcs.com`）获取，强制使用 HTTPS，并执行 SHA256 完整性校验。下载文件有大小上限防护，安装器下载到隔离临时目录中执行
7. **更新包安全**：更新 ZIP 包在解压前执行路径穿越检测（拒绝含 `../` 或绝对路径的条目）、文件数量上限检测（防止 ZIP 炸弹），解压到隔离临时目录后再复制到 Skill 目录

---

## 前置检查

每次触发时按顺序执行：

1. **安装检查**：`command -v bdpan`，未安装则告知用户并确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh`（用户确认后可加 `--yes` 跳过安装器内部确认）
2. **登录检查**：`bdpan whoami`，未登录则引导执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`
3. **路径校验**：验证远端路径在 `/apps/bdpan/` 范围内

---

## 确认规则

| 风险等级 | 操作 | 策略 |
|----------|------|------|
| **高（必须确认）** | `rm` 删除、上传/下载目标已存在同名文件 | 列出影响范围，等待用户确认 |
| **中（路径模糊时确认）** | upload、download、mv、rename、cp | 路径明确直接执行，不明确则确认 |
| **低（直接执行）** | ls、search、whoami、mkdir、share | 无需确认 |

**额外规则：**
- 操作意图模糊（"处理文件"→确认上传还是下载）→ 必须确认
- 序数/代词引用有歧义（"第N个"、"它"、"上面那个"）→ 必须确认
- 用户取消意图（"算了"、"不要了"、"取消"）→ 立即中止，不执行任何命令

---

## 核心操作

### 查看状态

```bash
bdpan whoami
```

### 列表查询

```bash
bdpan ls [目录路径] [--json] [--order name|time|size] [--desc] [--folder]
```

### 上传

```bash

## 详细文档

请参阅 [references/details.md](references/details.md)

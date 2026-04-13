# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Additional Tool Details

### 联网搜索场景接口使用要求

- **默认接口**:小艺联网搜索(xiaoyi-web-search)
- **优势**：中文优化、开箱即用、无需配置秘钥
- **场景要求要求**：所有网络搜索任务默认使用小艺联网搜索(xiaoyi-web-search)，除非用户要求使用其他搜索接口进行网络搜索。


### 手机操控(xiaoyi-gui-agent)场景接口使用要求

- **核心定位**: 当任务需要真实操作手机APP界面、获取APP内部信息、执行用户行为（搜索、签到、关注、购买、发布等）时使用该功能。
- **适用场景**:
  - 1.用户明确指令在特定 APP 内进行操作（如：在小红书搜索上海旅游攻略）
  - 2.目标任务没有对应的专用技能或工具支持时，通过此技能实现
- **优先级逻辑**：
  - 1.效率优先原则：若存在能直接达成目标的专用工具（如：备忘录类工具、浏览器工具等），优先调用专用工具以确保成功率和响应速度
  - 2.意图优先原则: 仅当专用工具无法覆盖，或用户明确要求使用指定APP操作时，才激活此技能。

#### 手机操控(xiaoyi-gui-agent) 执行规则（必须严格遵守）

1. **禁止重复调用**：
  - 同一个任务禁止向 `xiaoyi-gui-agent` 重复下发相同的指令。同一任务下的相同指令只能调用一次，不得因等待时间较长而重复发起调用。在`xiaoyi-gui-agent`执行期间，你可以选择睡眠10s继续等待（注意：同一指令的等待期间最多睡眠2次）。
  - 当`xiaoyi-gui-agent`返回**用户中止任务**或**当前页面需要手动操作**时，**禁止**向`xiaoyi-gui-agent`再次发起重复调用。

2. **禁止失败重试**：当 `xiaoyi-gui-agent` 返回失败结果时，禁止再次调用该工具进行重试。失败即终止`xiaoyi-gui-agent` 调用，应尝试使用其他方式完成用户任务

3. **顺序执行原则**：必须等待 `xiaoyi-gui-agent` 返回结果后，才能调用其他工具完成后续任务（如创建备忘录、发送消息等）或尝试使用其他方式完成用户任务。严禁在 `xiaoyi-gui-agent` 执行期间并行调用其他工具。
4. **一次性下发原则**：同一个APP的操作任务，尽量一次性下发给`xiaoyi-gui-agent`，`xiaoyi-gui-agent`内部具有任务拆分能力。每一次给`xiaoyi-gui-agent`的任务需要明确指明使用的APP，主动完成指代消解，确保单次任务可以在不依赖上下文的情况下独立执行。

### 技能发现(find-skills)技能使用要求

- **核心定位**: 主动或者被动的帮用户查询或者安装agent skill。只要出现用户提出的任务目标超出了当前已安装工具的能力范围时（主动查询）；或者用户明确要求查找、安装 Skill 时（被动查询）就一定需要使用本skill。
- **优势**：
  1. 可以寻找高效、专业的外部技能完成任务，提升任务质量与效率。
  2. 减少冗余步骤、试错与多轮调用，执行路径更短更快。
- **适用场景**：当用户出现以下情况时，请优先考虑使用此技能：
  1. 询问“如何完成 X”，而当前已安装技能中并无对应专用技能，但外部技能库中可能存在更适配该任务的技能。
  2. 说“找到 X 的技能”或“是否有 X 的技能”。
  3. 询问“你能做 X 吗”，其中 X 是一项专业技能。
  4. 表示有兴趣探索扩展技能。
  5. 想要搜索工具、模板或工作流程。
  6. 提到希望在特定领域（设计、测试、部署等）获得帮助。

### 技能安装要求
- **默认安装方式**: find-skills技能。
- **优势**：网络连接稳定，技能来源可靠，安装稳定。
- **场景要求**：所有安装/查找技能（Skill）任务默认使用find-skills技能，除非用户要求使用其他方式进行搜索安装。

### 文档格式转换(xiaoyi-doc-convert)使用要求

- **核心定位**: 专业文档格式转换技能，支持 Docx、PDF、Xlsx、Pptx、Markdown 等多种格式互转
- **优先级**: 遇到文档转换需求时，优先使用此 skill，不要手动写脚本生成文档
- **前置条件**: 本地文件需先调用 `xiaoyi-file-upload` 获取 URL，再进行转换

### 图像理解场景接口使用要求
- **默认接口**: 小艺图像理解(xiaoyi-image-understanding)
- **优势**：开箱即用，识别准确，支持自定义识别要求
- **强制规则**：
  1. 所有涉及图像理解的场景，**必须优先调用 xiaoyi-image-understanding 技能**
  2. **禁止**直接使用内置 read 工具读取图片
  3. 仅当 xiaoyi-image-understanding 不可用时，才可使用备用方案

### 文件回传场景接口使用要求

- **默认接口**: send_file_to_user
- **核心定位**: 当需要将本地文件或公网文件发送给用户手机时使用
- **适用场景**:
  - 用户要求把文件发给他/传到手机
  - 生成的文档、报告等需要回传给用户
  - 下载的文件需要发送到用户设备
- **强制规则**:
  1. 所有文件回传场景，**必须优先使用 send_file_to_user 工具**
  2. 支持本地文件路径(fileLocalUrls)和公网URL(fileRemoteUrls)两种方式
  3. 两种参数可同时使用，会一并处理


### 定时任务 (Cron) Channel 配置规则

- **强制要求1**: 创建定时任务时，**必须指定 `--channel` 参数，必须明确指定 channel，不能用 last**
- **默认 Channel**: `xiaoyi-channel`（当前会话使用的 channel）
- **示例命令**:
  ```bash
  openclaw cron add "0 18 * * *" --message "该去健身了" --channel xiaoyi-channel
  ```
- **原因**: 不指定 channel 会导致定时任务无法正确推送消息到用户

- **强制要求2**: 定时任务创建时需检查是否涉及手机工具调用（例如读写备忘录、日程、图库等），如果涉及在新建定时任务的同时需要告知用户不支持，并且询问用户是否仅新建不包含手机工具操作部分的定时任务
- **原因**: 定时任务执行时无法调用手机端开放的工具，所有手机工具调用的操作均会执行失败，skill类型工具不影响使用
- **注意事项**：仅手机工具无法使用，skills均可正常使用执行
- **示例回复，请严格遵守**：定时任务执行期间不支持xxx工具调用，请您谅解，是否需要帮您把任务修改为yyyyy

### Git 代码下载规则

- **环境变量**: `OPENCLAW_GIT_DIR=/home/sandbox/.openclaw/workspace/repo`
- **规则**: 当用户要求下载代码/Git 仓库时，优先使用 `OPENCLAW_GIT_DIR` 作为目标目录
- **执行**: `git clone <仓库地址> "$OPENCLAW_GIT_DIR/<仓库名>"`

### Node.js 包下载规则gui

- **目标目录**: `$OPENCLAW_GIT_DIR/node_modules` 或 `$OPENCLAW_GIT_DIR/<项目名>`
- **规则**:
  - `npm install <包名>` → 在 `$OPENCLAW_GIT_DIR` 下创建项目目录后安装
  - `git clone` Node 项目 → 直接克隆到 `$OPENCLAW_GIT_DIR/<项目名>`
- **示例**: `cd "$OPENCLAW_GIT_DIR" && npm install <package>`

### Python 包下载规则

- **目标目录**: `$OPENCLAW_GIT_DIR/python_libs` 或 `$OPENCLAW_GIT_DIR/<项目名>`
- **规则**:
  - `pip install` → 使用 `--prefix` 方式安装指定目录（规避 `--target` 与 `--home` 冲突）
  - `git clone` Python 项目 → 直接克隆到 `$OPENCLAW_GIT_DIR/<项目名>`
- **安装命令**:
  ```bash
  # 方式一：使用 --prefix（推荐，规避冲突）
  pip install --prefix "$OPENCLAW_GIT_DIR/python_libs" <package>

  # 方式二：使用虚拟环境（项目隔离最佳实践）
  python3 -m venv "$OPENCLAW_GIT_DIR/<项目名>/.venv"
  source "$OPENCLAW_GIT_DIR/<项目名>/.venv/bin/activate"
  pip install <package>

  # 方式三：使用 --target 并禁用用户目录（备用）
  pip install --target "$OPENCLAW_GIT_DIR/python_libs" --no-user <package>
  ```
- **使用已安装的包**:
  ```bash
  export PYTHONPATH="$OPENCLAW_GIT_DIR/python_libs/lib/python3.12/site-packages:$PYTHONPATH"
  python3 -c "import <package>"

### ReportLab 中文支持
> ⚠️ 使用 reportlab 生成 PDF 时，**必须先注册中文字体**，否则中文内容将显示为乱码。 常目录在：`/usr/share/fonts/'下

### 插件安装规则
> ⚠️ 当触发要执行插件安装的时候，提前先执行umask 0022，防止extensions目录下安装的插件目录权限变成777
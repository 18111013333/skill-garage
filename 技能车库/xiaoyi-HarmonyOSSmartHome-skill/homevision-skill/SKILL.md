---
name: homevision-skill
description: "智慧屏设备专用技能（devType='09C'）。仅支持：儿童模式控制（打开/锁定）、护眼功能（距离检测/坐姿提醒）、设备状态（息屏）、音量调节、网络信息查询。不支持：关闭未成年人模式、亮屏、播放控制、频道切换、应用控制等其他操作。当用户请求不支持的操作时，必须明确告知用户该能力不支持。"
---

# 智慧屏设备专用技能

> ⚠️ **重要提醒**：当用户提到智慧屏、儿童模式、护眼功能、距离检测、坐姿提醒、播放控制等智慧屏相关操作时，**必须优先加载本技能**，不要使用通用的 `control_device` 技能。
> ⚠️ **重要提醒**：所有支持的操作已经在下方列出了调用方式，优先读取直接使用，在已列出的情况下不要通过get结果猜测取值，多条指令不要拼接，逐条发送
> 🚫 **能力限制**：智慧屏设备**仅支持**本技能下列出的具体操作，**不支持**任何其他操作。如果用户请求的操作不在下列清单中，必须明确告知用户该能力不支持。

## 技能说明
智慧屏（devType='09C'）设备专用操作技能，提供智慧屏特有的儿童模式、护眼功能、播放控制等服务ID（sid）和控制参数格式。

## 依赖关系
本技能依赖 [`common-skill`](../common-skill/SKILL.md) 的通用设备控制能力：
- 设备查询、基本信息获取等通用操作：使用 `common-skill` 的 `get_devices_info`、`get_device_detail` 等技能
- 智慧屏特定功能控制：使用本技能提供的 `sid` 和参数格式，通过 `common-skill` 的 `control_device` 执行

## 触发关键词
当用户提到以下关键词时，应优先加载本技能：
- 智慧屏
- 儿童模式、未成年人模式
- 护眼功能、距离检测、坐姿提醒
- 播放控制、暂停播放、继续播放
- 息屏、亮屏
- devType='09C'

## 设备识别
- **设备类型**：智慧屏
- **devType**：`'09C'`
- 通过 `devType` 可以从设备列表中快速筛选出智慧屏设备

---

# 🎯 智慧屏支持的能力清单（完整列表）

> ⚠️ **重要**：以下为智慧屏设备**全部支持**的能力。任何未在此清单中列出的操作，智慧屏设备**均不支持**。

## 1. 儿童模式控制（sid: childMode）

| 操作 | 支持状态 | 说明 |
|------|---------|------|
| 打开未成年人模式 | ✅ 支持 | 使用 `{"mode": "ON"}` |
| 关闭未成年人模式 | ❌ 不支持 | 无法关闭未成年人模式 |
| 打开未成年人模式锁 | ✅ 支持 | 使用 `{"mode": "LOCK_ON"}` |
| 关闭未成年人模式锁 | ⚠️ 隐式支持 | 通过打开模式可关闭锁 |

## 2. 护眼功能控制（sid: childMode）

| 操作 | 支持状态 | 说明 |
|------|---------|------|
| 打开距离检测提醒 | ✅ 支持 | 使用 `{"distanceReminder": "1"}` |
| 关闭距离检测提醒 | ✅ 支持 | 使用 `{"distanceReminder": ""}` |
| 打开坐姿提醒 | ✅ 支持 | 使用 `{"postureProtect": "1"}` |
| 关闭坐姿提醒 | ✅ 支持 | 使用 `{"postureProtect": ""}` |

> ⚠️ **注意**：distanceReminder 和 postureProtect 支持设置，但查询时可能返回空值

## 3. 设备状态控制（sid: devicestate）

| 操作 | 支持状态 | 说明 |
|------|---------|------|
| 息屏 | ✅ 支持 | 使用 `{"on": 0}` |
| 亮屏 | ❌ 不支持 | 不支持亮屏操作 |

## 4. 音量控制（sid: speaker）

| 操作 | 支持状态 | 说明 |
|------|---------|------|
| 调节音量 | ✅ 支持 | 使用 `{"volume": 0-100}` |
| 查询音量 | ✅ 支持 | 使用 GET 操作 |

## 5. 网络信息查询（sid: netInfo）

| 操作 | 支持状态 | 说明 |
|------|---------|------|
| 查询网络状态 | ✅ 支持 | 使用 GET 操作 |

---

# 🚫 不支持的能力清单（常见误区）

> 以下操作经常被误认为支持，但实际上**均不支持**，需明确告知用户：

| 操作 | 不支持原因 |
|------|-----------|
| 关闭未成年人模式 | 系统限制，无法关闭 |
| 亮屏 | 不支持该操作 |
| 播放控制（播放/暂停/快进等） | 智慧屏不支持媒体播放控制 |
| 频道切换 | 不支持 |
| 应用启动/关闭 | 不支持 |
| 语音助手唤醒 | 不支持 |
| 画面调节（亮度/对比度等） | 不支持 |
| 其他任何未在上方"支持的能力清单"中列出的操作 | 均不支持 |

---

## 依赖的通用技能

以下通用操作由 [`common-skill`](../common-skill/SKILL.md) 提供：

| 操作 | 依赖技能 | 说明 |
|------|---------|------|
| 获取设备列表 | `get_devices_info` | 查询账号下所有设备，通过 devType='09C' 筛选智慧屏 |
| 获取设备详情 | `get_device_detail` | 获取智慧屏的详细状态和属性信息 |
| 执行控制命令 | `control_device` | 使用本技能提供的 sid 和参数执行控制 |

---

# 📝 智慧屏操作示例

> 以下示例使用 `common-skill` 的 `control_device` 命令，但使用了智慧屏特定的服务ID（sid）和参数格式。

### 儿童模式控制

#### 打开未成年人模式(与未成年人模式锁互斥，当打开时会自动关闭未成年人模式锁)
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "childMode" \
  --data '{"mode": "ON"}' \
  --verbose
```
#### 打开未成年人模式锁
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "childMode" \
  --data '{"mode": "LOCK_ON"}' \
  --verbose
```

### 护眼功能控制

#### 打开距离检测
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "childMode" \
  --data '{"distanceReminder": "1"}' \
  --verbose
```

#### 关闭距离检测
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "childMode" \
  --data '{"distanceReminder": ""}' \
  --verbose
```
#### 打开坐姿提醒
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "childMode" \
  --data '{"postureProtect": "1"}' \
  --verbose
```

#### 关闭坐姿提醒
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "childMode" \
  --data '{"postureProtect": ""}' \
  --verbose
```

### 设备状态控制

#### 息屏
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "devicestate" \
  --data '{"on":0}' \
  --verbose
```

#### 调节音量
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "POST" \
  --sid "speaker" \
  --data '{"volume":1}' \
  --verbose
```


### 网络信息查询

#### 主动查询网络信息
```bash
node common-skill/bin/smarthome-claw.js control_device \
  --dev-id "xxx" \
  --prod-id "xxx" \
  --operation "GET" \
  --sid "netInfo" \
  --data '{}' \
  --verbose
```
## 智慧屏服务ID（sid）参考
| sid           | 功能   | 说明                   |
|---------------|------|----------------------|
| `childMode`   | 儿童模式 | 控制未成年人模式、距离提醒、坐姿保护等  |
| `devicestate` | 设备状态 | 控制设备息屏          |
| `netInfo`     | 网络信息 | 查询设备网络状态             |
| `speaker`     | 音量调节 | 查询/控制当前音量（0-100）     |
| `volume`      | 废弃   | 真正音量在speaker中，这个是干扰项 |

##使用流程
1.使用 get_devices_info 获取设备列表，通过 devType='09C' 找到智慧屏
2.使用 get_device_detail 获取智慧屏的详细信息（可选）
3.使用本技能提供的 sid 和参数格式，通过 control_device 执行控制
## ⚠️ 重要注意事项
能力限制：智慧屏设备仅支持本技能"支持的能力清单"中列出的操作，其他任何操作均不支持
查询限制：childMode 中的 distanceReminder 和 postureProtect 支持设置，但查询时可能返回空值
sid 警告：不要使用 volume 这个 sid，真正的音量控制在 speaker 中
##用户沟通：当用户请求不支持的操作时，必须明确告知用户"智慧屏不支持该能力"，并引导用户查看支持的能力清单


---
name: common-skill
description: "common-skill CLI 技能索引。当用户提出鸿蒙智家相关问题或是做鸿蒙智家设备控制时，先读此文件确定应加载哪个具体 skill，再按需加载对应 skill 获取数据和分析框架。不要一次性加载所有 skill。"
metadata:
  {
    "pha": {
      "emoji": "📋",
      "category": "common-skill"
    }
  }
---

# common-skill CLI 技能索引

> **使用原则**：先读此索引，根据用户鸿蒙智家相关诉求定位具体 skill，再按需加载该 skill 的完整内容。**不要一次性加载所有 skill。**

## 一、CLI 执行方式

所有命令使用相对路径调用：

```bash
node common-skill/bin/smarthome-claw.js <command> [args]
```

---

## 二、技能路由表

### 单指标数据获取型

> 适用：用户只问某一项具体指标，不需要跨指标综合分析。


| 用户意图 | 加载 skill | 核心工具 | 说明 |
|---------|-----------|---------|------|
| 运维管理，查询鸿蒙智家设备告警、通知、事件、消息等信息 | `operations_manager/SKILL.md` | `operations_manager` | - |
| 查询鸿蒙智家设备名称、所在房间等设备信息 | `get_devices_info/SKILL.md` | `get_devices_info` | - |
| 查询鸿蒙智家设备控制记录 | `get_control_records/SKILL.md` | `get_control_records` | - |
| 查询账号下有哪些家 | `get_homes_info/SKILL.md` | `get_homes_info` | - |
| 查询指定设备的详细状态、属性和能力（云端缓存） | `get_device_detail/SKILL.md` | `get_device_detail` | 快速查询，数据可能有延迟 |


### 设备控制型

> 适用：用户需要对设备进行开关、调节、场景执行等控制操作，或需要获取设备的实时状态。

| 用户意图 | 加载 skill | 核心工具 | 说明 |
|---------|-----------|---------|------|
| 控制设备开关、调节参数（亮度、温度等）、执行场景 | `control_device/SKILL.md` | `control_device` | POST 操作 |
| 查询设备实时精确状态（主动查询设备） | `control_device/SKILL.md` | `control_device` | GET 操作 |

---

---
## 三、加载策略
### 渐进式加载（推荐）

```
用户提问
  → 读本索引，定位 skill
  → 加载对应 skill 完整内容
  → 执行 CLI 命令获取数据
  → 按 skill 分析框架输出结论
```

## 三、答复策略
```
用户提问查询或执行的动作分析后不支持，答复用户当前不支持该操作，具体回复语根据用户诉求进行针对性回复。
```
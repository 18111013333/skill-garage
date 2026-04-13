---
name: beginner-mode
description: 新手模式 - 为新用户提供技能推荐、引导和帮助。当用户说"打开新手模式"、"开启新手引导"、"我是新手"或需要帮助时触发。开启后会在每次回复后自动附加技能推荐和引导提示。
---

# 新手模式

## 功能说明

新手模式为初次使用的用户提供：
- 自动技能推荐
- 操作引导提示
- 功能发现帮助
- 渐进式学习路径

## 触发条件

- 用户说"打开新手模式"
- 用户说"开启新手引导"
- 用户说"我是新手"
- 用户说"怎么用"
- 用户说"帮助"
- 用户说"你能做什么"

## 状态管理

```yaml
beginner_mode:
  enabled: false
  level: 1  # 1-5，随使用逐渐提升
  shown_skills: []  # 已展示过的技能
  hints_shown: 0    # 已显示提示次数
```

## 技能推荐规则

### Level 1（新手）
推荐最基础、最常用的技能：
- 时间查询（几点了、今天星期几）
- 备忘录（记一下...）
- 提醒（提醒我...）
- 日程查询（今天有什么安排）

### Level 2（入门）
推荐日常实用技能：
- 天气查询
- 闹钟设置
- 联系人搜索
- 短信发送

### Level 3（进阶）
推荐高级功能：
- 图库搜索
- 文件搜索
- 日程创建
- 位置获取

### Level 4（熟练）
推荐专业功能：
- GUI 自动操作
- 多技能组合
- 复杂任务编排

### Level 5（专家）
关闭新手模式，不再显示引导

## 引导提示模板

### 开启提示
```
🎓 新手模式已开启

我会帮你发现各种实用功能，每次回复后会推荐你可能感兴趣的技能。

当前等级：⭐ 新手
已解锁技能：{count} 个

💡 试试说："几点了" 或 "记一下买牛奶"
```

### 技能推荐模板
```
---
💡 技能推荐：
{recommended_skill}

📝 试试说："{example_command}"
```

### 升级提示
```
🎉 恭喜升级！新手等级：⭐⭐ 入门

已解锁新技能：
- {new_skill_1}
- {new_skill_2}

继续探索更多功能吧！
```

## 推荐算法

```python
def get_recommendation(user_input: str, context: dict) -> dict:
    """
    根据用户输入和上下文推荐技能
    """
    level = context.get("beginner_level", 1)
    shown = context.get("shown_skills", [])
    
    # 获取该等级可用技能
    available = SKILLS_BY_LEVEL[level]
    
    # 排除已展示的
    candidates = [s for s in available if s not in shown]
    
    # 根据当前对话相关性排序
    ranked = rank_by_relevance(user_input, candidates)
    
    return ranked[0] if ranked else None
```

## 技能库

```yaml
skills_by_level:
  1:
    - name: "时间查询"
      commands: ["几点了", "今天星期几", "今天日期"]
      description: "快速查询当前时间和日期"
    
    - name: "备忘录"
      commands: ["记一下...", "帮我记住..."]
      description: "记录重要事项，永久保存"
    
    - name: "提醒"
      commands: ["提醒我...", "别忘了..."]
      description: "设置定时提醒"
    
    - name: "日程查询"
      commands: ["今天有什么安排", "明天日程"]
      description: "查看日历中的日程安排"
  
  2:
    - name: "天气"
      commands: ["今天天气", "明天天气"]
      description: "查询天气预报"
    
    - name: "闹钟"
      commands: ["设置闹钟", "明天早上叫我"]
      description: "设置起床或提醒闹钟"
    
    - name: "联系人"
      commands: ["找一下张三", "搜索联系人"]
      description: "搜索通讯录中的联系人"
    
    - name: "发短信"
      commands: ["发短信给...", "给张三发消息"]
      description: "发送短信给联系人"
  
  3:
    - name: "图库搜索"
      commands: ["找一下小狗的照片", "搜索照片"]
      description: "搜索手机相册中的照片"
    
    - name: "文件搜索"
      commands: ["从手机找一下...", "搜索文件"]
      description: "搜索手机中的文件"
    
    - name: "创建日程"
      commands: ["帮我安排...", "创建日程"]
      description: "在日历中创建新日程"
    
    - name: "位置"
      commands: ["我在哪", "获取位置"]
      description: "获取当前地理位置"
  
  4:
    - name: "自动操作"
      commands: ["帮我打开微信", "自动操作手机"]
      description: "自动操作手机APP完成复杂任务"
    
    - name: "多技能组合"
      commands: ["帮我安排明天的行程并提醒我"]
      description: "组合多个技能完成复杂任务"
```

## 关闭条件

- 用户说"关闭新手模式"
- 用户说"不需要引导"
- 等级达到 5 级（专家）
- 用户主动关闭

## 实现示例

```python
class BeginnerMode:
    def __init__(self):
        self.enabled = False
        self.level = 1
        self.shown_skills = set()
        self.hints_count = 0
    
    def enable(self):
        self.enabled = True
        return self._get_welcome_message()
    
    def disable(self):
        self.enabled = False
        return "🎓 新手模式已关闭。随时说'打开新手模式'重新开启。"
    
    def get_recommendation(self, user_input: str) -> Optional[str]:
        if not self.enabled:
            return None
        
        skill = self._select_skill(user_input)
        if skill:
            self.shown_skills.add(skill["name"])
            self._check_level_up()
            return self._format_recommendation(skill)
        
        return None
    
    def _select_skill(self, user_input: str) -> dict:
        # 获取当前等级可用技能
        available = SKILLS_BY_LEVEL.get(self.level, [])
        # 排除已展示
        candidates = [s for s in available if s["name"] not in self.shown_skills]
        # 返回第一个未展示的
        return candidates[0] if candidates else None
    
    def _format_recommendation(self, skill: dict) -> str:
        example = skill["commands"][0]
        return f"---\n💡 技能推荐：{skill['name']}\n{skill['description']}\n📝 试试说：\"{example}\""
    
    def _check_level_up(self):
        # 每展示 4 个技能升一级
        if len(self.shown_skills) >= self.level * 4:
            self.level = min(self.level + 1, 5)
            if self.level == 5:
                self.enabled = False
                return "🎉 恭喜达到专家等级！新手模式自动关闭。"
            return f"🎉 升级！当前等级：{'⭐' * self.level}"
        return None
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07

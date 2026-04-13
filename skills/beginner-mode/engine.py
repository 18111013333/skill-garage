#!/usr/bin/env python3
"""
新手模式引擎
"""

import json
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class BeginnerLevel(Enum):
    NOVICE = 1      # 新手
    BEGINNER = 2    # 入门
    INTERMEDIATE = 3  # 进阶
    ADVANCED = 4    # 熟练
    EXPERT = 5      # 专家

@dataclass
class Skill:
    name: str
    description: str
    commands: List[str]
    level: int

@dataclass
class BeginnerState:
    enabled: bool = False
    level: int = 1
    shown_skills: List[str] = field(default_factory=list)
    hints_shown: int = 0
    enabled_at: Optional[str] = None
    total_interactions: int = 0

# 技能库
SKILLS: Dict[int, List[Skill]] = {
    1: [
        Skill("时间查询", "快速查询当前时间和日期", ["几点了", "今天星期几", "今天日期"], 1),
        Skill("备忘录", "记录重要事项，永久保存", ["记一下买牛奶", "帮我记住..."], 1),
        Skill("提醒", "设置定时提醒", ["提醒我明天开会", "别忘了..."], 1),
        Skill("日程查询", "查看日历中的日程安排", ["今天有什么安排", "明天日程"], 1),
    ],
    2: [
        Skill("天气", "查询天气预报", ["今天天气", "明天天气怎么样"], 2),
        Skill("闹钟", "设置起床或提醒闹钟", ["设置闹钟", "明天早上7点叫我"], 2),
        Skill("联系人", "搜索通讯录中的联系人", ["找一下张三", "搜索联系人"], 2),
        Skill("发短信", "发送短信给联系人", ["发短信给张三", "给张三发消息"], 2),
    ],
    3: [
        Skill("图库搜索", "搜索手机相册中的照片", ["找一下小狗的照片", "搜索照片"], 3),
        Skill("文件搜索", "搜索手机中的文件", ["从手机找一下文档", "搜索文件"], 3),
        Skill("创建日程", "在日历中创建新日程", ["帮我安排明天下午开会", "创建日程"], 3),
        Skill("位置", "获取当前地理位置", ["我在哪", "获取位置"], 3),
    ],
    4: [
        Skill("自动操作", "自动操作手机APP完成复杂任务", ["帮我打开微信", "自动操作手机"], 4),
        Skill("多技能组合", "组合多个技能完成复杂任务", ["帮我安排明天的行程并提醒我"], 4),
    ],
}

# 触发词
ENABLE_TRIGGERS = [
    "打开新手模式", "开启新手模式", "开启新手引导",
    "我是新手", "怎么用", "怎么使用",
    "你能做什么", "你会什么", "帮助", "help"
]

DISABLE_TRIGGERS = [
    "关闭新手模式", "不需要引导", "不用引导了", "关闭引导"
]

class BeginnerModeEngine:
    def __init__(self):
        self.state = BeginnerState()
    
    def process_input(self, user_input: str) -> Optional[str]:
        """处理用户输入，返回新手模式相关消息"""
        input_lower = user_input.lower().strip()
        
        # 检查是否要开启
        if any(trigger in input_lower for trigger in ENABLE_TRIGGERS):
            return self.enable()
        
        # 检查是否要关闭
        if any(trigger in input_lower for trigger in DISABLE_TRIGGERS):
            return self.disable()
        
        return None
    
    def enable(self) -> str:
        """开启新手模式"""
        self.state.enabled = True
        self.state.enabled_at = datetime.now().isoformat()
        self.state.level = 1
        self.state.shown_skills = []
        self.state.hints_shown = 0
        
        return self._get_welcome_message()
    
    def disable(self) -> str:
        """关闭新手模式"""
        self.state.enabled = False
        return "🎓 新手模式已关闭。随时说'打开新手模式'重新开启。"
    
    def get_recommendation(self, user_input: str) -> Optional[str]:
        """获取技能推荐"""
        if not self.state.enabled:
            return None
        
        self.state.total_interactions += 1
        
        # 检查是否需要推荐
        if self.state.hints_shown >= 5:  # 每次会话最多 5 个
            return None
        
        # 选择技能
        skill = self._select_skill()
        if not skill:
            return None
        
        # 记录已展示
        self.state.shown_skills.append(skill.name)
        self.state.hints_shown += 1
        
        # 检查升级
        level_up_msg = self._check_level_up()
        
        # 格式化推荐
        recommendation = self._format_recommendation(skill)
        
        if level_up_msg:
            return f"{recommendation}\n\n{level_up_msg}"
        
        return recommendation
    
    def _select_skill(self) -> Optional[Skill]:
        """选择下一个要推荐的技能"""
        available = SKILLS.get(self.state.level, [])
        
        for skill in available:
            if skill.name not in self.state.shown_skills:
                return skill
        
        # 当前等级没有了，尝试下一等级
        next_level = self.state.level + 1
        if next_level <= 5:
            available = SKILLS.get(next_level, [])
            for skill in available:
                if skill.name not in self.state.shown_skills:
                    return skill
        
        return None
    
    def _format_recommendation(self, skill: Skill) -> str:
        """格式化推荐消息"""
        example = skill.commands[0]
        return f"---\n💡 技能推荐：{skill.name}\n{skill.description}\n📝 试试说：\"{example}\""
    
    def _check_level_up(self) -> Optional[str]:
        """检查是否升级"""
        skills_for_next = self.state.level * 4
        
        if len(self.state.shown_skills) >= skills_for_next:
            new_level = self.state.level + 1
            
            if new_level > 5:
                self.state.enabled = False
                return "🎉 恭喜达到专家等级！新手模式自动关闭。"
            
            self.state.level = new_level
            stars = "⭐" * new_level
            level_names = {1: "新手", 2: "入门", 3: "进阶", 4: "熟练", 5: "专家"}
            
            # 获取新解锁技能
            new_skills = SKILLS.get(new_level, [])
            new_skill_names = [s.name for s in new_skills[:2]]
            
            msg = f"🎉 恭喜升级！当前等级：{stars} {level_names[new_level]}\n\n已解锁新技能：\n"
            for name in new_skill_names:
                msg += f"- {name}\n"
            msg += "\n继续探索更多功能吧！"
            
            return msg
        
        return None
    
    def _get_welcome_message(self) -> str:
        """获取欢迎消息"""
        return """🎓 新手模式已开启

我会帮你发现各种实用功能，每次回复后会推荐你可能感兴趣的技能。

当前等级：⭐ 新手
已解锁技能：0 个

💡 试试说："几点了" 或 "记一下买牛奶" """
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "enabled": self.state.enabled,
            "level": self.state.level,
            "shown_skills": self.state.shown_skills,
            "hints_shown": self.state.hints_shown,
            "total_interactions": self.state.total_interactions,
        }

# 全局实例
beginner_mode = BeginnerModeEngine()

# 测试
if __name__ == "__main__":
    engine = BeginnerModeEngine()
    
    # 测试开启
    print(engine.process_input("打开新手模式"))
    print()
    
    # 模拟对话
    test_inputs = [
        "你好",
        "几点了",
        "今天天气怎么样",
        "帮我记一下",
        "提醒我明天开会",
    ]
    
    for inp in test_inputs:
        rec = engine.get_recommendation(inp)
        if rec:
            print(f"用户: {inp}")
            print(rec)
            print()
    
    print("状态:", engine.get_status())

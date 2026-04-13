#!/usr/bin/env python3
"""
动态提示词系统
V2.7.0 - 2026-04-10

借鉴 LegnaChat 的动态变量注入
"""

import os
import re
from typing import Dict, Any, Optional
from pathlib import Path
from string import Template

class DynamicPromptBuilder:
    """动态提示词构建器"""
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
        self.variables: Dict[str, Any] = {}
        self.templates: Dict[str, str] = {}
    
    def set_variable(self, name: str, value: Any):
        """设置变量"""
        self.variables[name] = value
    
    def load_template(self, name: str, path: str):
        """加载模板文件"""
        template_path = self.workspace / path
        if template_path.exists():
            self.templates[name] = template_path.read_text(encoding='utf-8')
    
    def build(self, template_name: str = None, template_content: str = None,
              extra_vars: Dict[str, Any] = None) -> str:
        """构建提示词"""
        # 获取模板
        if template_content:
            template = template_content
        elif template_name and template_name in self.templates:
            template = self.templates[template_name]
        else:
            return ""
        
        # 合并变量
        all_vars = {**self.variables}
        if extra_vars:
            all_vars.update(extra_vars)
        
        # 替换变量
        result = template
        for key, value in all_vars.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        
        return result
    
    def build_from_file(self, path: str, variables: Dict[str, Any] = None) -> str:
        """从文件构建"""
        file_path = self.workspace / path
        if not file_path.exists():
            return ""
        
        template = file_path.read_text(encoding='utf-8')
        return self.build(template_content=template, extra_vars=variables)

class SystemPromptManager:
    """系统提示词管理器"""
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
        self.builder = DynamicPromptBuilder(workspace)
        
        # 初始化默认变量
        self._init_default_variables()
    
    def _init_default_variables(self):
        """初始化默认变量"""
        from datetime import datetime
        
        # 基础变量
        self.builder.set_variable("date", datetime.now().strftime("%Y-%m-%d"))
        self.builder.set_variable("time", datetime.now().strftime("%H:%M:%S"))
        self.builder.set_variable("workspace", str(self.workspace))
        
        # 技能列表
        skills_dir = self.workspace / "skills"
        if skills_dir.exists():
            skills = []
            for skill in skills_dir.iterdir():
                if skill.is_dir():
                    display_file = skill / "display.txt"
                    if display_file.exists():
                        display = display_file.read_text().strip()
                    else:
                        display = skill.name
                    skills.append({"name": skill.name, "display": display})
            
            self.builder.set_variable("skills_list", str(skills))
            self.builder.set_variable("skills_count", len(skills))
    
    def get_startup_prompt(self) -> str:
        """获取启动提示词"""
        # 读取核心文件
        prompt_parts = []
        
        # AGENTS.md
        agents_file = self.workspace / "AGENTS.md"
        if agents_file.exists():
            prompt_parts.append(agents_file.read_text(encoding='utf-8'))
        
        # SOUL.md
        soul_file = self.workspace / "SOUL.md"
        if soul_file.exists():
            prompt_parts.append("\n" + soul_file.read_text(encoding='utf-8'))
        
        # TOOLS.md
        tools_file = self.workspace / "TOOLS.md"
        if tools_file.exists():
            prompt_parts.append("\n" + tools_file.read_text(encoding='utf-8'))
        
        return "\n".join(prompt_parts)
    
    def get_memory_prompt(self) -> str:
        """获取记忆提示词"""
        memory_parts = []
        
        # 短期记忆
        short_memory = self.workspace / "memory" / "short.md"
        if short_memory.exists():
            content = short_memory.read_text(encoding='utf-8')
            if content.strip():
                memory_parts.append(f"## 短期记忆\n{content}")
        
        # 长期记忆
        long_memory = self.workspace / "memory" / "long.md"
        if long_memory.exists():
            content = long_memory.read_text(encoding='utf-8')
            if content.strip():
                memory_parts.append(f"## 长期记忆\n{content}")
        
        if memory_parts:
            return "\n\n".join(memory_parts)
        return ""
    
    def get_skill_prompt(self, skill_name: str) -> str:
        """获取技能提示词"""
        skill_dir = self.workspace / "skills" / skill_name
        if not skill_dir.exists():
            return ""
        
        parts = []
        
        # SKILL.md
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            parts.append(skill_file.read_text(encoding='utf-8'))
        
        # display.txt
        display_file = skill_dir / "display.txt"
        if display_file.exists():
            display = display_file.read_text().strip()
            parts.insert(0, f"# {display}")
        
        return "\n".join(parts)
    
    def update_variable(self, name: str, value: Any):
        """更新变量"""
        self.builder.set_variable(name, value)
    
    def get_token_estimate(self) -> int:
        """估算 Token 数"""
        prompt = self.get_startup_prompt()
        
        # 简单估算
        chinese = len(re.findall(r'[\u4e00-\u9fff]', prompt))
        other = len(prompt) - chinese
        
        return int(chinese / 2 + other / 4)

# 全局实例
_prompt_manager: Optional[SystemPromptManager] = None

def get_prompt_manager() -> SystemPromptManager:
    """获取全局提示词管理器"""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = SystemPromptManager("/home/sandbox/.openclaw/workspace")
    return _prompt_manager

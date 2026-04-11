#!/usr/bin/env python3
"""
技能接入网关 - V2.8.0

职责：
- 扫描 skills/*/SKILL.md
- 自动提取技能元数据
- 转换为可注册、可路由、可调用的统一技能对象
- 写入正式技能注册体系
"""

import os
import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

from infrastructure.path_resolver import (
    get_project_root, get_skills_dir, get_infrastructure_dir
)

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SkillStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BROKEN = "broken"
    ORPHANED = "orphaned"

@dataclass
class SkillMetadata:
    """技能元数据"""
    name: str
    display_name: str
    description: str
    category: str
    risk_level: str
    dependencies: List[str]
    fallback: Optional[str]
    timeout: int
    layer: int
    status: str
    registered: bool
    routable: bool
    callable: bool
    path: str

class SkillAdapterGateway:
    """技能接入网关"""
    
    def __init__(self):
        self.skills_dir = get_skills_dir()
        self.registry_path = get_infrastructure_dir() / 'inventory' / 'skill_registry.json'
        self.skills: Dict[str, SkillMetadata] = {}
        self._load_registry()
    
    def _load_registry(self) -> dict:
        """加载注册表"""
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text(encoding='utf-8'))
        return {"skills": {}}
    
    def _save_registry(self, registry: dict):
        """保存注册表"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(
            json.dumps(registry, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def scan_skills(self) -> List[SkillMetadata]:
        """扫描所有技能目录"""
        skills = []
        
        if not self.skills_dir.exists():
            return skills
        
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            skill_file = skill_dir / 'SKILL.md'
            if not skill_file.exists():
                continue
            
            metadata = self._parse_skill_md(skill_dir, skill_file)
            if metadata:
                skills.append(metadata)
                self.skills[metadata.name] = metadata
        
        return skills
    
    def _parse_skill_md(self, skill_dir: Path, skill_file: Path) -> Optional[SkillMetadata]:
        """解析 SKILL.md 提取元数据"""
        try:
            content = skill_file.read_text(encoding='utf-8')
            
            # 提取 YAML frontmatter
            frontmatter = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    fm_text = parts[1].strip()
                    for line in fm_text.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"\'')
            
            # 提取描述（第一个段落）
            desc_match = re.search(r'^#\s+.+\n+(.+?)(?:\n\n|\n#|$)', content, re.MULTILINE)
            description = desc_match.group(1).strip() if desc_match else ""
            
            # 推断分类
            category = self._infer_category(skill_dir.name, content)
            
            # 推断风险等级
            risk_level = self._infer_risk_level(skill_dir.name, content)
            
            # 推断层级
            layer = self._infer_layer(skill_dir.name, content)
            
            # 检查依赖
            dependencies = self._extract_dependencies(content)
            
            # 检查 fallback
            fallback = self._extract_fallback(content)
            
            # 检查 timeout
            timeout = self._extract_timeout(content)
            
            return SkillMetadata(
                name=skill_dir.name,
                display_name=frontmatter.get('name', skill_dir.name),
                description=description[:200],
                category=category,
                risk_level=risk_level,
                dependencies=dependencies,
                fallback=fallback,
                timeout=timeout,
                layer=layer,
                status=SkillStatus.HEALTHY.value,
                registered=False,
                routable=False,
                callable=False,
                path=str(skill_dir)
            )
        
        except Exception as e:
            print(f"解析失败 {skill_dir.name}: {e}")
            return None
    
    def _infer_category(self, name: str, content: str) -> str:
        """推断分类"""
        name_lower = name.lower()
        content_lower = content.lower()
        
        if 'search' in name_lower or '搜索' in content_lower:
            return 'search'
        elif 'doc' in name_lower or 'pdf' in name_lower or 'word' in name_lower:
            return 'document'
        elif 'image' in name_lower or '图片' in content_lower:
            return 'image'
        elif 'email' in name_lower or 'message' in name_lower:
            return 'communication'
        elif 'data' in name_lower or 'analysis' in name_lower:
            return 'data'
        elif 'auto' in name_lower or 'cron' in name_lower:
            return 'automation'
        elif 'system' in name_lower or 'git' in name_lower:
            return 'system'
        else:
            return 'other'
    
    def _infer_risk_level(self, name: str, content: str) -> str:
        """推断风险等级"""
        high_risk = ['rm', 'delete', 'drop', 'exec', 'shell', 'sudo', 'auth']
        medium_risk = ['write', 'create', 'update', 'modify', 'send']
        
        name_lower = name.lower()
        content_lower = content.lower()
        
        for keyword in high_risk:
            if keyword in name_lower or keyword in content_lower:
                return RiskLevel.HIGH.value
        
        for keyword in medium_risk:
            if keyword in name_lower or keyword in content_lower:
                return RiskLevel.MEDIUM.value
        
        return RiskLevel.LOW.value
    
    def _infer_layer(self, name: str, content: str) -> int:
        """推断层级"""
        # 大多数技能在 L4 执行层
        return 4
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """提取依赖"""
        deps = []
        match = re.search(r'dependencies:\s*\n((?:\s*-\s+.+\n)+)', content)
        if match:
            for line in match.group(1).split('\n'):
                dep = line.strip().lstrip('- ').strip()
                if dep:
                    deps.append(dep)
        return deps
    
    def _extract_fallback(self, content: str) -> Optional[str]:
        """提取 fallback"""
        match = re.search(r'fallback:\s*(\S+)', content)
        return match.group(1) if match else None
    
    def _extract_timeout(self, content: str) -> int:
        """提取 timeout"""
        match = re.search(r'timeout:\s*(\d+)', content)
        return int(match.group(1)) if match else 60
    
    def register_all(self) -> Dict[str, int]:
        """注册所有扫描到的技能"""
        skills = self.scan_skills()
        registry = self._load_registry()
        
        stats = {
            "total": len(skills),
            "registered": 0,
            "updated": 0,
            "skipped": 0
        }
        
        for skill in skills:
            if skill.name in registry.get("skills", {}):
                stats["updated"] += 1
            else:
                stats["registered"] += 1
            
            registry["skills"][skill.name] = asdict(skill)
        
        self._save_registry(registry)
        return stats
    
    def get_skill(self, name: str) -> Optional[SkillMetadata]:
        """获取技能"""
        return self.skills.get(name)
    
    def list_skills(self, category: str = None, status: str = None) -> List[SkillMetadata]:
        """列出技能"""
        skills = list(self.skills.values())
        
        if category:
            skills = [s for s in skills if s.category == category]
        if status:
            skills = [s for s in skills if s.status == status]
        
        return skills

# 全局实例
_gateway: Optional[SkillAdapterGateway] = None

def get_skill_gateway() -> SkillAdapterGateway:
    """获取全局技能网关"""
    global _gateway
    if _gateway is None:
        _gateway = SkillAdapterGateway()
        _gateway.scan_skills()
    return _gateway

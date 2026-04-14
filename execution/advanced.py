#!/usr/bin/env python3
"""
高级功能增强模块
自定义技能、场景模板、智能推荐
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict


@dataclass
class CustomSkill:
    """自定义技能"""
    id: str
    name: str
    description: str
    template: str
    parameters: Dict
    created_at: str
    use_count: int = 0


@dataclass
class SceneTemplate:
    """场景模板"""
    id: str
    name: str
    category: str
    description: str
    skills: List[str]
    config: Dict


@dataclass
class Recommendation:
    """推荐项"""
    id: str
    type: str  # skill, template, action
    name: str
    reason: str
    score: float


class AdvancedFeatures:
    """高级功能管理器"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(
                os.path.dirname(__file__),
                'advanced'
            )
        
        self.config_dir = config_dir
        self.skills_file = os.path.join(config_dir, 'custom_skills.json')
        self.templates_file = os.path.join(config_dir, 'scene_templates.json')
        
        self.custom_skills: Dict[str, CustomSkill] = {}
        self.scene_templates: Dict[str, SceneTemplate] = {}
        self.recommendations: List[Recommendation] = []
        
        os.makedirs(config_dir, exist_ok=True)
        self._load_data()
        self._init_defaults()
        
        print(f"高级功能管理器初始化完成")
        print(f"  - 自定义技能: {len(self.custom_skills)}")
        print(f"  - 场景模板: {len(self.scene_templates)}")
    
    def _load_data(self):
        """加载数据"""
        # 加载自定义技能
        if os.path.exists(self.skills_file):
            with open(self.skills_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for skill_data in data.get('skills', []):
                skill = CustomSkill(
                    id=skill_data['id'],
                    name=skill_data['name'],
                    description=skill_data['description'],
                    template=skill_data['template'],
                    parameters=skill_data['parameters'],
                    created_at=skill_data['created_at'],
                    use_count=skill_data.get('use_count', 0)
                )
                self.custom_skills[skill.id] = skill
        
        # 加载场景模板
        if os.path.exists(self.templates_file):
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for template_data in data.get('templates', []):
                template = SceneTemplate(
                    id=template_data['id'],
                    name=template_data['name'],
                    category=template_data['category'],
                    description=template_data['description'],
                    skills=template_data['skills'],
                    config=template_data['config']
                )
                self.scene_templates[template.id] = template
    
    def _save_data(self):
        """保存数据"""
        # 保存自定义技能
        skills_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'skills': [asdict(skill) for skill in self.custom_skills.values()]
        }
        
        with open(self.skills_file, 'w', encoding='utf-8') as f:
            json.dump(skills_data, f, ensure_ascii=False, indent=2)
        
        # 保存场景模板
        templates_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'templates': [asdict(t) for t in self.scene_templates.values()]
        }
        
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(templates_data, f, ensure_ascii=False, indent=2)
    
    def _init_defaults(self):
        """初始化默认内容"""
        # 默认自定义技能
        default_skills = [
            CustomSkill(
                id='summarize',
                name='智能摘要',
                description='自动提取文本关键信息',
                template='请总结以下内容：{content}',
                parameters={'content': 'string'},
                created_at=datetime.now().isoformat()
            ),
            CustomSkill(
                id='translate',
                name='智能翻译',
                description='多语言翻译',
                template='请将以下内容翻译成{language}：{content}',
                parameters={'content': 'string', 'language': 'string'},
                created_at=datetime.now().isoformat()
            ),
            CustomSkill(
                id='analyze',
                name='深度分析',
                description='深度分析文本内容',
                template='请从以下角度分析：{aspects}\n内容：{content}',
                parameters={'content': 'string', 'aspects': 'string'},
                created_at=datetime.now().isoformat()
            ),
        ]
        
        for skill in default_skills:
            if skill.id not in self.custom_skills:
                self.custom_skills[skill.id] = skill
        
        # 默认场景模板
        default_templates = [
            SceneTemplate(
                id='daily-work',
                name='日常工作',
                category='productivity',
                description='日常办公场景',
                skills=['summarize', 'translate'],
                config={'auto_save': True}
            ),
            SceneTemplate(
                id='research',
                name='研究分析',
                category='analysis',
                description='研究和分析场景',
                skills=['analyze', 'summarize'],
                config={'depth': 'high'}
            ),
            SceneTemplate(
                id='creative',
                name='创意写作',
                category='creative',
                description='创意内容生成',
                skills=['translate'],
                config={'style': 'creative'}
            ),
        ]
        
        for template in default_templates:
            if template.id not in self.scene_templates:
                self.scene_templates[template.id] = template
        
        self._save_data()
    
    def create_skill(self, skill: CustomSkill) -> bool:
        """创建自定义技能"""
        if skill.id in self.custom_skills:
            return False
        
        skill.created_at = datetime.now().isoformat()
        self.custom_skills[skill.id] = skill
        self._save_data()
        
        print(f"创建技能: {skill.name}")
        return True
    
    def use_skill(self, skill_id: str, params: Dict) -> str:
        """使用技能"""
        if skill_id not in self.custom_skills:
            return f"技能 {skill_id} 不存在"
        
        skill = self.custom_skills[skill_id]
        skill.use_count += 1
        self._save_data()
        
        # 渲染模板
        result = skill.template
        for key, value in params.items():
            result = result.replace(f'{{{key}}}', str(value))
        
        return result
    
    def get_recommendations(self, context: str) -> List[Recommendation]:
        """获取推荐"""
        recommendations = []
        
        # 基于使用频率推荐
        sorted_skills = sorted(
            self.custom_skills.values(),
            key=lambda s: s.use_count,
            reverse=True
        )
        
        for i, skill in enumerate(sorted_skills[:3]):
            recommendations.append(Recommendation(
                id=f'rec_{i}',
                type='skill',
                name=skill.name,
                reason=f'使用次数: {skill.use_count}',
                score=1.0 - i * 0.1
            ))
        
        return recommendations
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_uses = sum(s.use_count for s in self.custom_skills.values())
        
        return {
            'custom_skills': len(self.custom_skills),
            'scene_templates': len(self.scene_templates),
            'total_uses': total_uses,
            'categories': len(set(t.category for t in self.scene_templates.values()))
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    manager = AdvancedFeatures()
    
    if len(sys.argv) < 2:
        print("用法: python advanced.py <command>")
        print("命令: skills, templates, recommend, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'skills':
        print("\n自定义技能:")
        print("-" * 60)
        for skill in manager.custom_skills.values():
            print(f"  {skill.name}: {skill.description} (使用: {skill.use_count})")
    
    elif command == 'templates':
        print("\n场景模板:")
        print("-" * 60)
        for template in manager.scene_templates.values():
            print(f"  [{template.category}] {template.name}: {template.description}")
    
    elif command == 'recommend':
        recs = manager.get_recommendations("日常工作")
        print("\n推荐:")
        print("-" * 60)
        for rec in recs:
            print(f"  [{rec.type}] {rec.name}: {rec.reason} (分数: {rec.score})")
    
    elif command == 'stats':
        stats = manager.get_stats()
        print("\n高级功能统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

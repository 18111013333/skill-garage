#!/usr/bin/env python3
"""
小说大纲生成器
支持多种类型小说的结构化大纲生成
"""

import json
import sys
from typing import Dict, List, Any

class NovelOutlineGenerator:
    """小说大纲生成器"""

    # 类型模板
    GENRE_TEMPLATES = {
        'fantasy': {
            'name': '玄幻/奇幻',
            'structure': ['世界观设定', '修炼体系', '主角设定', '主线剧情', '副本设计'],
            'elements': ['金手指', '升级流', '打脸', '后宫/单女主', '势力争霸']
        },
        'urban': {
            'name': '都市',
            'structure': ['背景设定', '主角身份', '核心冲突', '感情线', '事业线'],
            'elements': ['重生', '系统', '神豪', '医生', '律师', '娱乐圈']
        },
        'romance': {
            'name': '言情',
            'structure': ['人物设定', '相遇契机', '感情发展', '矛盾冲突', '结局走向'],
            'elements': ['甜宠', '虐恋', '破镜重圆', '先婚后爱', '欢喜冤家']
        },
        'mystery': {
            'name': '悬疑/推理',
            'structure': ['案件设定', '侦探角色', '线索布局', '嫌疑人设计', '真相揭示'],
            'elements': ['本格推理', '社会派', '心理悬疑', '刑侦']
        },
        'scifi': {
            'name': '科幻',
            'structure': ['科技设定', '世界观', '核心冲突', '人物设定', '剧情走向'],
            'elements': ['硬科幻', '软科幻', '末世', '太空歌剧', '赛博朋克']
        },
        'historical': {
            'name': '历史',
            'structure': ['时代背景', '主角身份', '历史事件', '权谋设计', '结局走向'],
            'elements': ['穿越', '重生', '架空', '正剧', '轻松']
        }
    }

    def __init__(self):
        pass

    def generate_outline(self, genre: str, title: str, word_count: int = 100000) -> Dict[str, Any]:
        """生成小说大纲"""
        template = self.GENRE_TEMPLATES.get(genre, self.GENRE_TEMPLATES['urban'])

        # 计算章节规划
        chapter_count = word_count // 3000  # 每章约3000字
        volume_count = max(1, chapter_count // 50)  # 每卷约50章

        outline = {
            'title': title,
            'genre': template['name'],
            'target_words': word_count,
            'chapter_count': chapter_count,
            'volume_count': volume_count,
            'structure': self._generate_structure(template),
            'volumes': self._generate_volumes(volume_count, chapter_count),
            'characters': self._generate_character_template(),
            'worldbuilding': self._generate_worldbuilding(genre),
            'timeline': self._generate_timeline()
        }

        return outline

    def _generate_structure(self, template: Dict) -> List[Dict]:
        """生成结构大纲"""
        structure = []
        for i, section in enumerate(template['structure'], 1):
            structure.append({
                'section': section,
                'description': f'待完善：{section}的具体内容',
                'status': 'draft'
            })
        return structure

    def _generate_volumes(self, volume_count: int, chapter_count: int) -> List[Dict]:
        """生成卷次规划"""
        volumes = []
        chapters_per_volume = chapter_count // volume_count

        volume_names = ['开篇', '发展', '高潮', '转折', '结局', '番外']

        for i in range(volume_count):
            start_chapter = i * chapters_per_volume + 1
            end_chapter = (i + 1) * chapters_per_volume if i < volume_count - 1 else chapter_count

            volumes.append({
                'volume_number': i + 1,
                'volume_name': volume_names[i] if i < len(volume_names) else f'第{i+1}卷',
                'chapter_range': f'{start_chapter}-{end_chapter}',
                'word_count': (end_chapter - start_chapter + 1) * 3000,
                'summary': '待填写本卷主要内容',
                'key_events': ['事件1', '事件2', '事件3']
            })

        return volumes

    def _generate_character_template(self) -> Dict[str, Any]:
        """生成角色模板"""
        return {
            'protagonist': {
                'name': '待设定',
                'age': '待设定',
                'background': '待设定',
                'personality': '待设定',
                'goal': '待设定',
                'arc': '待设定'
            },
            'antagonist': {
                'name': '待设定',
                'motivation': '待设定',
                'relationship_to_protagonist': '待设定'
            },
            'supporting_characters': [
                {'name': '配角1', 'role': '待设定'},
                {'name': '配角2', 'role': '待设定'}
            ]
        }

    def _generate_worldbuilding(self, genre: str) -> Dict[str, Any]:
        """生成世界观模板"""
        worldbuilding = {
            'setting': '待设定',
            'time_period': '待设定',
            'locations': ['地点1', '地点2', '地点3'],
            'rules': '待设定',
            'unique_elements': []
        }

        if genre in ['fantasy', 'scifi']:
            worldbuilding['power_system'] = '待设定'
            worldbuilding['technology_level'] = '待设定'

        if genre == 'historical':
            worldbuilding['historical_events'] = ['事件1', '事件2']

        return worldbuilding

    def _generate_timeline(self) -> List[Dict]:
        """生成时间线模板"""
        return [
            {'phase': '开篇', 'events': ['事件1', '事件2']},
            {'phase': '发展', 'events': ['事件1', '事件2']},
            {'phase': '高潮', 'events': ['事件1', '事件2']},
            {'phase': '结局', 'events': ['事件1', '事件2']}
        ]

    def generate_chapter_outline(self, volume: int, chapter: int, summary: str) -> Dict[str, Any]:
        """生成单章大纲"""
        return {
            'volume': volume,
            'chapter': chapter,
            'title': f'第{chapter}章 待命名',
            'summary': summary,
            'word_target': 3000,
            'scenes': [
                {'scene': 1, 'content': '场景1内容', 'characters': []},
                {'scene': 2, 'content': '场景2内容', 'characters': []}
            ],
            'notes': '写作注意事项'
        }

def main():
    """主函数"""
    generator = NovelOutlineGenerator()

    if len(sys.argv) < 3:
        # 演示模式
        result = generator.generate_outline('urban', '都市重生之商业帝国', 500000)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    genre = sys.argv[1]
    title = sys.argv[2]
    word_count = int(sys.argv[3]) if len(sys.argv) > 3 else 100000

    result = generator.generate_outline(genre, title, word_count)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

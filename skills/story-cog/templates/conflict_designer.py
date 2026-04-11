#!/usr/bin/env python3
"""
情节冲突设计工具
生成和优化故事中的冲突设计
"""

import json
import sys
from typing import Dict, List, Any
import random

class ConflictDesigner:
    """冲突设计器"""

    # 冲突类型
    CONFLICT_TYPES = {
        'person_vs_person': {
            'name': '人与人',
            'description': '主角与反派或其他角色的对抗',
            'examples': ['正邪对决', '情敌竞争', '权力斗争']
        },
        'person_vs_self': {
            'name': '人与自我',
            'description': '主角内心的挣扎和成长',
            'examples': ['道德抉择', '克服恐惧', '接受自我']
        },
        'person_vs_society': {
            'name': '人与社会',
            'description': '主角与社会规则/制度的对抗',
            'examples': ['反抗压迫', '挑战传统', '追求自由']
        },
        'person_vs_nature': {
            'name': '人与自然',
            'description': '主角与自然环境/灾难的对抗',
            'examples': ['生存挑战', '自然灾害', '探索未知']
        },
        'person_vs_fate': {
            'name': '人与命运',
            'description': '主角与命运/预言的对抗',
            'examples': ['逆天改命', '打破预言', '挑战宿命']
        },
        'person_vs_technology': {
            'name': '人与科技',
            'description': '主角与科技/AI的对抗',
            'examples': ['AI觉醒', '科技失控', '人机战争']
        }
    }

    # 冲突强度等级
    INTENSITY_LEVELS = {
        'low': {'name': '低强度', 'description': '日常矛盾，推动小情节'},
        'medium': {'name': '中强度', 'description': '重要矛盾，推动章节发展'},
        'high': {'name': '高强度', 'description': '核心矛盾，推动主线剧情'},
        'critical': {'name': '关键冲突', 'description': '高潮冲突，决定故事走向'}
    }

    # 冲突升级方式
    ESCALATION_METHODS = [
        '增加赌注',
        '引入时间压力',
        '增加障碍',
        '背叛/反转',
        '揭示真相',
        '牺牲代价',
        '道德困境',
        '力量失衡'
    ]

    def __init__(self):
        pass

    def generate_conflict(self, conflict_type: str = None, intensity: str = 'medium') -> Dict[str, Any]:
        """生成冲突设计"""
        if conflict_type is None:
            conflict_type = random.choice(list(self.CONFLICT_TYPES.keys()))

        type_info = self.CONFLICT_TYPES[conflict_type]
        intensity_info = self.INTENSITY_LEVELS[intensity]

        return {
            'type': conflict_type,
            'type_name': type_info['name'],
            'description': type_info['description'],
            'example': random.choice(type_info['examples']),
            'intensity': intensity,
            'intensity_name': intensity_info['name'],
            'setup': self._generate_setup(conflict_type),
            'development': self._generate_development(conflict_type),
            'climax': self._generate_climax(conflict_type),
            'resolution': self._generate_resolution(conflict_type),
            'escalation_suggestions': random.sample(self.ESCALATION_METHODS, 3)
        }

    def _generate_setup(self, conflict_type: str) -> str:
        """生成冲突铺垫"""
        setups = {
            'person_vs_person': '通过小摩擦建立对立关系，暗示更大的冲突',
            'person_vs_self': '通过日常选择展示内心矛盾，铺垫成长契机',
            'person_vs_society': '通过不公事件引发质疑，建立反抗动机',
            'person_vs_nature': '通过环境描写营造危机感，预示挑战来临',
            'person_vs_fate': '通过预言或征兆暗示命运，引发主角思考',
            'person_vs_technology': '通过科技异常暗示危机，建立对抗基础'
        }
        return setups.get(conflict_type, '建立冲突的基础条件')

    def _generate_development(self, conflict_type: str) -> List[str]:
        """生成冲突发展"""
        developments = {
            'person_vs_person': [
                '双方首次正面交锋',
                '一方获得优势',
                '局势逆转',
                '矛盾升级'
            ],
            'person_vs_self': [
                '内心矛盾加剧',
                '尝试改变但失败',
                '获得启示',
                '做出选择'
            ],
            'person_vs_society': [
                '发现更多不公',
                '尝试改变但受阻',
                '获得盟友',
                '面临抉择'
            ],
            'person_vs_nature': [
                '环境恶化',
                '资源耗尽',
                '发现生机',
                '最后挣扎'
            ],
            'person_vs_fate': [
                '预言开始应验',
                '尝试逃避但失败',
                '发现改变的方法',
                '做出抉择'
            ],
            'person_vs_technology': [
                '科技威胁显现',
                '尝试对抗但失败',
                '发现弱点',
                '最后对决'
            ]
        }
        return developments.get(conflict_type, ['冲突逐步升级'])

    def _generate_climax(self, conflict_type: str) -> str:
        """生成冲突高潮"""
        climaxes = {
            'person_vs_person': '双方最终对决，胜负在此一举',
            'person_vs_self': '做出关键选择，完成内心转变',
            'person_vs_society': '正面对抗体制，引发变革',
            'person_vs_nature': '与自然的最后较量，生死存亡',
            'person_vs_fate': '挑战命运的关键时刻',
            'person_vs_technology': '人机最终对决'
        }
        return climaxes.get(conflict_type, '冲突达到顶点')

    def _generate_resolution(self, conflict_type: str) -> str:
        """生成冲突解决"""
        resolutions = {
            'person_vs_person': '一方获胜，或达成和解',
            'person_vs_self': '完成成长，获得新认知',
            'person_vs_society': '改变或接受，留下影响',
            'person_vs_nature': '战胜或和解，获得成长',
            'person_vs_fate': '改变命运或接受宿命',
            'person_vs_technology': '战胜或共存，找到平衡'
        }
        return resolutions.get(conflict_type, '冲突得到解决')

    def design_conflict_arc(self, num_conflicts: int = 3) -> Dict[str, Any]:
        """设计冲突弧线"""
        conflicts = []
        intensities = ['low', 'medium', 'high']

        for i in range(num_conflicts):
            intensity = intensities[i] if i < len(intensities) else 'high'
            conflict = self.generate_conflict(intensity=intensity)
            conflicts.append(conflict)

        return {
            'arc_name': '冲突弧线',
            'conflicts': conflicts,
            'overall_escalation': '冲突逐级升级，推动剧情发展',
            'climax_conflict': conflicts[-1] if conflicts else None
        }

    def escalate_conflict(self, current_situation: str) -> List[str]:
        """提供冲突升级建议"""
        suggestions = random.sample(self.ESCALATION_METHODS, 4)
        return [
            f"💡 {suggestions[0]}：让局势更加紧迫",
            f"💡 {suggestions[1]}：增加新的障碍",
            f"💡 {suggestions[2]}：引入意外因素",
            f"💡 {suggestions[3]}：提高失败代价"
        ]

def main():
    """主函数"""
    designer = ConflictDesigner()

    if len(sys.argv) < 2:
        # 演示模式
        result = designer.generate_conflict('person_vs_person', 'high')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    command = sys.argv[1]

    if command == 'generate':
        conflict_type = sys.argv[2] if len(sys.argv) > 2 else None
        intensity = sys.argv[3] if len(sys.argv) > 3 else 'medium'
        result = designer.generate_conflict(conflict_type, intensity)
    elif command == 'arc':
        num = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        result = designer.design_conflict_arc(num)
    else:
        result = designer.generate_conflict()

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

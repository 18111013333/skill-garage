#!/usr/bin/env python3
"""
角色卡生成器
生成详细的角色设定卡片
"""

import json
import sys
from typing import Dict, List, Any
import random

class CharacterCardGenerator:
    """角色卡生成器"""

    # 姓名库
    SURNAMES = ['李', '王', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '林', '罗', '高']
    MALE_NAMES = ['明', '强', '伟', '磊', '洋', '勇', '军', '杰', '涛', '超', '鹏', '辉', '浩', '宇', '轩', '睿', '泽', '辰', '阳', '风']
    FEMALE_NAMES = ['芳', '娜', '敏', '静', '丽', '艳', '梅', '玲', '婷', '雪', '琳', '欣', '怡', '悦', '瑶', '萱', '晴', '月', '雨', '灵']

    # 性格特征库
    PERSONALITY_TRAITS = {
        'positive': ['乐观', '开朗', '热情', '善良', '正直', '勇敢', '聪明', '幽默', '细心', '有责任心'],
        'negative': ['固执', '冲动', '敏感', '内向', '傲慢', '多疑', '懒惰', '自私', '胆小', '优柔寡断'],
        'neutral': ['理性', '感性', '独立', '依赖', '务实', '理想主义', '外向', '内向', '开放', '保守']
    }

    # 外貌特征库
    APPEARANCE = {
        'male': {
            'face': ['方脸', '圆脸', '瓜子脸', '国字脸', '长脸'],
            'eyes': ['深邃的眼睛', '明亮的眼睛', '细长的眼睛', '大眼睛', '小眼睛'],
            'build': ['高大健壮', '中等身材', '瘦削', '微胖', '精瘦'],
            'hair': ['短发', '中分', '寸头', '卷发', '长发']
        },
        'female': {
            'face': ['鹅蛋脸', '瓜子脸', '圆脸', '方脸', '心形脸'],
            'eyes': ['大眼睛', '杏眼', '丹凤眼', '桃花眼', '瑞凤眼'],
            'build': ['高挑', '娇小', '丰满', '纤细', '匀称'],
            'hair': ['长发', '短发', '中发', '卷发', '直发']
        }
    }

    # 职业库
    OCCUPATIONS = {
        'modern': ['程序员', '医生', '律师', '教师', '企业家', '设计师', '记者', '警察', '作家', '演员', '歌手', '运动员', '厨师', '建筑师', '金融分析师'],
        'historical': ['将军', '丞相', '皇帝', '公主', '商人', '侠客', '书生', '医者', '刺客', '谋士'],
        'fantasy': ['魔法师', '战士', '弓箭手', '牧师', '盗贼', '骑士', '召唤师', '炼金术士', '龙骑士', '死灵法师']
    }

    def __init__(self):
        pass

    def generate_character(self, genre: str = 'modern', gender: str = None, name: str = None) -> Dict[str, Any]:
        """生成角色卡"""
        # 性别
        if gender is None:
            gender = random.choice(['male', 'female'])

        # 姓名
        if name is None:
            name = self._generate_name(gender)

        # 职业
        occupation = random.choice(self.OCCUPATIONS.get(genre, self.OCCUPATIONS['modern']))

        # 性格
        personality = self._generate_personality()

        # 外貌
        appearance = self._generate_appearance(gender)

        # 背景故事
        background = self._generate_background(genre, occupation)

        character = {
            'basic_info': {
                'name': name,
                'gender': '男' if gender == 'male' else '女',
                'age': random.randint(18, 45),
                'occupation': occupation,
                'birthday': f'{random.randint(1,12)}月{random.randint(1,28)}日'
            },
            'appearance': appearance,
            'personality': personality,
            'background': background,
            'abilities': self._generate_abilities(genre),
            'relationships': [],
            'goals': ['短期目标：待设定', '长期目标：待设定'],
            'fears': ['恐惧1：待设定', '恐惧2：待设定'],
            'secrets': ['秘密：待设定'],
            'quotes': ['口头禅：待设定']
        }

        return character

    def _generate_name(self, gender: str) -> str:
        """生成姓名"""
        surname = random.choice(self.SURNAMES)
        if gender == 'male':
            given_name = random.choice(self.MALE_NAMES) + random.choice(['', random.choice(self.MALE_NAMES)])
        else:
            given_name = random.choice(self.FEMALE_NAMES) + random.choice(['', random.choice(self.FEMALE_NAMES)])
        return surname + given_name

    def _generate_personality(self) -> Dict[str, List[str]]:
        """生成性格"""
        return {
            'positive_traits': random.sample(self.PERSONALITY_TRAITS['positive'], 3),
            'negative_traits': random.sample(self.PERSONALITY_TRAITS['negative'], 2),
            'neutral_traits': random.sample(self.PERSONALITY_TRAITS['neutral'], 2)
        }

    def _generate_appearance(self, gender: str) -> Dict[str, str]:
        """生成外貌"""
        gender_appearance = self.APPEARANCE.get(gender, self.APPEARANCE['male'])
        return {
            'face': random.choice(gender_appearance['face']),
            'eyes': random.choice(gender_appearance['eyes']),
            'build': random.choice(gender_appearance['build']),
            'hair': random.choice(gender_appearance['hair']),
            'special_features': '待设定（如疤痕、痣、纹身等）'
        }

    def _generate_background(self, genre: str, occupation: str) -> str:
        """生成背景故事"""
        templates = [
            f'出生于普通家庭，通过努力成为了一名{occupation}。',
            f'家世显赫，却选择了一条不同寻常的道路——成为{occupation}。',
            f'经历过重大变故，这些经历塑造了现在的性格。',
            f'有着不为人知的过去，正在寻找真相。',
            f'从小展现出过人天赋，被寄予厚望。'
        ]
        return random.choice(templates)

    def _generate_abilities(self, genre: str) -> List[Dict[str, str]]:
        """生成能力"""
        if genre == 'fantasy':
            return [
                {'name': '主能力', 'description': '待设定', 'level': 'S'},
                {'name': '副能力', 'description': '待设定', 'level': 'A'},
                {'name': '辅助能力', 'description': '待设定', 'level': 'B'}
            ]
        else:
            return [
                {'name': '专业技能', 'description': '待设定', 'level': '高级'},
                {'name': '语言能力', 'description': '待设定', 'level': '中级'},
                {'name': '其他技能', 'description': '待设定', 'level': '初级'}
            ]

    def add_relationship(self, character: Dict, relation_type: str, target_name: str, description: str) -> Dict:
        """添加关系"""
        character['relationships'].append({
            'type': relation_type,
            'target': target_name,
            'description': description
        })
        return character

def main():
    """主函数"""
    generator = CharacterCardGenerator()

    if len(sys.argv) < 2:
        # 演示模式
        result = generator.generate_character('modern')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    genre = sys.argv[1] if len(sys.argv) > 1 else 'modern'
    gender = sys.argv[2] if len(sys.argv) > 2 else None
    name = sys.argv[3] if len(sys.argv) > 3 else None

    result = generator.generate_character(genre, gender, name)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

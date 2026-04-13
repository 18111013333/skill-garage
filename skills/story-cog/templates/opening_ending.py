#!/usr/bin/env python3
"""
开头结尾生成器
生成吸引人的故事开头和有力的结尾
"""

import json
import sys
from typing import Dict, List, Any
import random

class OpeningEndingGenerator:
    """开头结尾生成器"""

    # 开头类型
    OPENING_TYPES = {
        'action': {
            'name': '动作开头',
            'description': '直接进入动作场景，制造紧张感',
            'template': '{动作描写}，{主角反应}。',
            'example': '子弹擦过耳边，我扑向掩体。'
        },
        'dialogue': {
            'name': '对话开头',
            'description': '以对话开始，引发好奇',
            'template': '"{对话内容}"，{说话人描述}。',
            'example': '"你确定要这么做？"她问，眼神复杂。'
        },
        'description': {
            'name': '描写开头',
            'description': '以环境或氛围描写开始',
            'template': '{环境描写}，{情感渲染}。',
            'example': '这座城市已经死了，只是它自己还不知道。'
        },
        'suspense': {
            'name': '悬念开头',
            'description': '制造悬念，引发疑问',
            'template': '{悬念事件}，{疑问}。',
            'example': '那天早上，我发现自己的墓碑立在院子里。'
        },
        'flashback': {
            'name': '倒叙开头',
            'description': '从结局或关键场景开始',
            'template': '{结局场景}，{时间回溯}。',
            'example': '后来我常想，如果那天我没有上那趟地铁...'
        },
        'contrast': {
            'name': '反差开头',
            'description': '制造强烈反差，吸引注意',
            'template': '{表象描述}，{真相揭示}。',
            'example': '表面上看，他只是个普通的老头。但我知道...'
        }
    }

    # 结尾类型
    ENDING_TYPES = {
        'open': {
            'name': '开放式结尾',
            'description': '留下想象空间',
            'template': '{行动}，{未知未来}。',
            'example': '他走向远方，身后是燃烧的城市。明天会怎样，没人知道。'
        },
        'loop': {
            'name': '循环式结尾',
            'description': '回到开头，形成闭环',
            'template': '{回到起点}，{新的开始}。',
            'example': '又是同样的早晨，同样的阳光，同样的敲门声。'
        },
        'twist': {
            'name': '反转式结尾',
            'description': '出人意料的结局',
            'template': '{铺垫}，{反转}。',
            'example': '"恭喜你，"面试官微笑着说，"你通过了最后一关。"'
        },
        'blank': {
            'name': '留白式结尾',
            'description': '点到为止，余韵悠长',
            'template': '{场景}，{留白}。',
            'example': '她没有回答，只是望向窗外。雪开始下了。'
        },
        'quote': {
            'name': '金句式结尾',
            'description': '以有力的话语收束',
            'template': '{总结}，{金句}。',
            'example': '有些路，注定要一个人走。但至少，他知道方向是对的。'
        },
        'emotional': {
            'name': '情感式结尾',
            'description': '以情感共鸣收尾',
            'template': '{场景}，{情感升华}。',
            'example': '多年后，他终于明白，有些告别，就是最后一面。'
        }
    }

    # 情感词库
    EMOTIONS = {
        'tense': ['紧张', '不安', '焦虑', '恐惧'],
        'calm': ['平静', '安宁', '释然', '淡然'],
        'sad': ['悲伤', '遗憾', '怀念', '不舍'],
        'hope': ['希望', '期待', '憧憬', '向往'],
        'shock': ['震惊', '意外', '难以置信', '愕然']
    }

    def __init__(self):
        pass

    def generate_opening(self, opening_type: str = None, genre: str = 'general') -> Dict[str, Any]:
        """生成开头"""
        if opening_type is None:
            opening_type = random.choice(list(self.OPENING_TYPES.keys()))

        type_info = self.OPENING_TYPES[opening_type]

        # 生成多个选项
        options = self._generate_opening_options(opening_type, genre, 3)

        return {
            'type': opening_type,
            'type_name': type_info['name'],
            'description': type_info['description'],
            'template': type_info['template'],
            'example': type_info['example'],
            'options': options,
            'tips': self._get_opening_tips(opening_type)
        }

    def generate_ending(self, ending_type: str = None, genre: str = 'general') -> Dict[str, Any]:
        """生成结尾"""
        if ending_type is None:
            ending_type = random.choice(list(self.ENDING_TYPES.keys()))

        type_info = self.ENDING_TYPES[ending_type]

        # 生成多个选项
        options = self._generate_ending_options(ending_type, genre, 3)

        return {
            'type': ending_type,
            'type_name': type_info['name'],
            'description': type_info['description'],
            'template': type_info['template'],
            'example': type_info['example'],
            'options': options,
            'tips': self._get_ending_tips(ending_type)
        }

    def _generate_opening_options(self, opening_type: str, genre: str, count: int) -> List[str]:
        """生成开头选项"""
        options = []

        templates = {
            'action': [
                '枪声响起的那一刻，我知道一切都变了。',
                '他冲进房间，浑身是血。',
                '警报声划破夜空，我抓起背包就跑。'
            ],
            'dialogue': [
                '"别回头。"他在我耳边低语。',
                '"你迟到了。"她冷冷地说。',
                '"这是最后一次。"我对自己说。'
            ],
            'description': [
                '雨已经下了三天，没有停的迹象。',
                '这座城市从不睡觉，但今晚格外安静。',
                '阳光透过破碎的窗户，照在满是灰尘的地板上。'
            ],
            'suspense': [
                '所有人都以为他死了，直到那天我收到了他的信。',
                '电话响了，来电显示是一个已经去世三年的名字。',
                '我从未想过，一个普通的早晨会改变一切。'
            ],
            'flashback': [
                '多年后，我依然记得那个下午。',
                '如果时光可以倒流，我一定不会打开那扇门。',
                '故事要从那个雨夜说起。'
            ],
            'contrast': [
                '表面上看，这只是个普通的村庄。',
                '谁能想到，这个温和的老人曾是...',
                '一切都很正常，直到我发现那个细节。'
            ]
        }

        return random.sample(templates.get(opening_type, templates['suspense']), min(count, 3))

    def _generate_ending_options(self, ending_type: str, genre: str, count: int) -> List[str]:
        """生成结尾选项"""
        templates = {
            'open': [
                '他转身离开，没有回头。前方的路还很长。',
                '故事结束了，但生活还在继续。',
                '门关上的那一刻，新的篇章悄然开始。'
            ],
            'loop': [
                '一切仿佛回到了原点，但有些东西已经改变。',
                '又是同样的场景，同样的人，只是心境不同了。',
                '故事从哪里开始，就在哪里结束。'
            ],
            'twist': [
                '原来，一切都不是巧合。',
                '真相大白的那一刻，他笑了。',
                '谁能想到，最后的赢家竟然是...'
            ],
            'blank': [
                '她没有说话，只是静静地看着远方。',
                '故事讲完了，但有些话，永远说不出口。',
                '风吹过，带走了所有答案。'
            ],
            'quote': [
                '有些路，只能一个人走。',
                '时间会给出所有答案，只是需要等待。',
                '真正的勇气，是知道结局依然前行。'
            ],
            'emotional': [
                '多年后想起，依然会红了眼眶。',
                '那一刻，他终于释然。',
                '有些告别，来不及说出口。'
            ]
        }

        return random.sample(templates.get(ending_type, templates['quote']), min(count, 3))

    def _get_opening_tips(self, opening_type: str) -> List[str]:
        """获取开头写作技巧"""
        tips = {
            'action': ['前3秒抓住读者', '动作要具体', '避免过多背景介绍'],
            'dialogue': ['对话要有张力', '避免无聊的寒暄', '对话要推动剧情'],
            'description': ['营造氛围', '调动感官', '暗示故事走向'],
            'suspense': ['制造疑问', '不要过早揭晓', '控制信息量'],
            'flashback': ['选择关键场景', '自然过渡', '避免混乱'],
            'contrast': ['反差要强烈', '揭示要自然', '引发好奇']
        }
        return tips.get(opening_type, ['吸引读者注意', '建立故事基调'])

    def _get_ending_tips(self, ending_type: str) -> List[str]:
        """获取结尾写作技巧"""
        tips = {
            'open': ['留有余地', '引发思考', '不要过于模糊'],
            'loop': ['呼应开头', '展示变化', '形成完整感'],
            'twist': ['铺垫要充分', '反转要合理', '避免生硬'],
            'blank': ['点到为止', '余韵悠长', '不要过于直白'],
            'quote': ['金句要有力', '与主题呼应', '避免说教'],
            'emotional': ['情感要真挚', '不要煽情过度', '引发共鸣']
        }
        return tips.get(ending_type, ['收束全文', '留下印象'])

def main():
    """主函数"""
    generator = OpeningEndingGenerator()

    if len(sys.argv) < 2:
        # 演示模式
        opening = generator.generate_opening('suspense')
        ending = generator.generate_ending('quote')
        result = {
            'opening': opening,
            'ending': ending
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    command = sys.argv[1]

    if command == 'opening':
        opening_type = sys.argv[2] if len(sys.argv) > 2 else None
        result = generator.generate_opening(opening_type)
    elif command == 'ending':
        ending_type = sys.argv[2] if len(sys.argv) > 2 else None
        result = generator.generate_ending(ending_type)
    else:
        result = generator.generate_opening()

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

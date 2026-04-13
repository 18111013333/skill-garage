#!/usr/bin/env python3
"""
对话优化工具
分析和优化小说/剧本中的对话
"""

import json
import sys
import re
from typing import Dict, List, Any, Tuple

class DialogueOptimizer:
    """对话优化器"""

    # 对话问题检测规则
    ISSUES = {
        'too_long': {
            'name': '对话过长',
            'description': '单句对话超过50字，建议拆分',
            'suggestion': '将长句拆分为多个短句，增加互动感'
        },
        'no_action': {
            'name': '缺乏动作描写',
            'description': '连续3句以上对话没有动作描写',
            'suggestion': '添加表情、动作、神态描写'
        },
        'repetitive': {
            'name': '用词重复',
            'description': '同一词语在对话中重复出现',
            'suggestion': '使用同义词替换或调整表达方式'
        },
        'passive': {
            'name': '被动语态过多',
            'description': '对话中大量使用"被"、"让"等被动词',
            'suggestion': '改用主动语态，增强力量感'
        },
        'no_subtext': {
            'name': '缺乏潜台词',
            'description': '对话过于直白，没有言外之意',
            'suggestion': '添加潜台词，让对话更有层次'
        }
    }

    # 优化建议库
    SUGGESTIONS = {
        'emotion_words': {
            'angry': ['咬牙切齿', '怒目而视', '拍案而起', '声音发抖'],
            'happy': ['眉开眼笑', '喜上眉梢', '笑得合不拢嘴', '眼睛弯成月牙'],
            'sad': ['眼眶泛红', '声音哽咽', '低下头', '强忍泪水'],
            'surprised': ['瞪大眼睛', '倒吸一口凉气', '愣在原地', '张口结舌'],
            'fear': ['脸色苍白', '浑身发抖', '后退一步', '声音颤抖']
        },
        'action_words': {
            'thinking': ['皱眉沉思', '摸着下巴', '来回踱步', '望向窗外'],
            'deciding': ['一拍大腿', '眼神坚定', '深吸一口气', '握紧拳头'],
            'hesitating': ['欲言又止', '咬了咬唇', '眼神闪烁', '手指绞在一起']
        }
    }

    def __init__(self):
        pass

    def analyze_dialogue(self, text: str) -> Dict[str, Any]:
        """分析对话"""
        # 提取对话
        dialogues = self._extract_dialogues(text)

        # 检测问题
        issues = self._detect_issues(dialogues)

        # 生成统计
        stats = self._generate_stats(dialogues)

        # 优化建议
        suggestions = self._generate_suggestions(dialogues, issues)

        return {
            'dialogue_count': len(dialogues),
            'stats': stats,
            'issues': issues,
            'suggestions': suggestions,
            'optimized_version': self._optimize_dialogues(text, dialogues, issues)
        }

    def _extract_dialogues(self, text: str) -> List[Dict[str, Any]]:
        """提取对话"""
        # 匹配引号内的对话
        pattern = r'[""「『]([^""」』]+)[""」』]'
        matches = re.findall(pattern, text)

        dialogues = []
        for i, content in enumerate(matches):
            dialogues.append({
                'index': i + 1,
                'content': content,
                'length': len(content),
                'word_count': len(content.split())
            })

        return dialogues

    def _detect_issues(self, dialogues: List[Dict]) -> List[Dict]:
        """检测问题"""
        issues = []

        for d in dialogues:
            # 检测过长
            if d['length'] > 50:
                issues.append({
                    'type': 'too_long',
                    'dialogue_index': d['index'],
                    'content': d['content'][:30] + '...',
                    'suggestion': self.ISSUES['too_long']['suggestion']
                })

            # 检测重复用词
            words = d['content'].split()
            word_count = {}
            for word in words:
                if len(word) > 1:
                    word_count[word] = word_count.get(word, 0) + 1

            for word, count in word_count.items():
                if count > 2:
                    issues.append({
                        'type': 'repetitive',
                        'dialogue_index': d['index'],
                        'word': word,
                        'count': count,
                        'suggestion': self.ISSUES['repetitive']['suggestion']
                    })

        return issues

    def _generate_stats(self, dialogues: List[Dict]) -> Dict[str, Any]:
        """生成统计"""
        if not dialogues:
            return {'avg_length': 0, 'total_length': 0}

        total_length = sum(d['length'] for d in dialogues)
        return {
            'avg_length': round(total_length / len(dialogues), 1),
            'total_length': total_length,
            'max_length': max(d['length'] for d in dialogues),
            'min_length': min(d['length'] for d in dialogues)
        }

    def _generate_suggestions(self, dialogues: List[Dict], issues: List[Dict]) -> List[str]:
        """生成优化建议"""
        suggestions = []

        # 基于问题生成建议
        issue_types = set(i['type'] for i in issues)

        if 'too_long' in issue_types:
            suggestions.append('💡 建议将长对话拆分为多个短句，增加互动感')

        if 'repetitive' in issue_types:
            suggestions.append('💡 建议使用同义词替换重复用词')

        # 通用建议
        if len(dialogues) > 5:
            suggestions.append('💡 建议在对话间添加动作描写，增强画面感')

        suggestions.append('💡 建议为关键对话添加潜台词，增加深度')

        return suggestions

    def _optimize_dialogues(self, text: str, dialogues: List[Dict], issues: List[Dict]) -> str:
        """生成优化版本"""
        optimized = text

        # 这里可以添加具体的优化逻辑
        # 目前返回原文，标注需要优化的地方

        for issue in issues:
            if issue['type'] == 'too_long':
                # 标记需要拆分的地方
                pass

        return optimized + '\n\n---\n[优化建议已标注，请根据上述建议进行修改]'

    def add_emotion_tag(self, dialogue: str, emotion: str) -> str:
        """添加情绪标签"""
        emotion_words = self.SUGGESTIONS['emotion_words'].get(emotion, [])
        if emotion_words:
            tag = f'（{emotion_words[0]}）'
            return f'{dialogue}{tag}'
        return dialogue

    def add_action_tag(self, dialogue: str, action_type: str) -> str:
        """添加动作标签"""
        action_words = self.SUGGESTIONS['action_words'].get(action_type, [])
        if action_words:
            tag = f'【{action_words[0]}】'
            return f'{tag}{dialogue}'
        return dialogue

def main():
    """主函数"""
    optimizer = DialogueOptimizer()

    if len(sys.argv) < 2:
        # 演示模式
        demo_text = '''
        "你好，我是新来的。"他说。
        "欢迎欢迎，我是这里的负责人。"她笑着回答。
        "请问有什么需要注意的吗？"
        "也没什么特别的，就是要注意安全，这里有些地方比较危险，一定要小心，不要单独行动，最好结伴而行。"
        '''
        result = optimizer.analyze_dialogue(demo_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    text = sys.argv[1]
    result = optimizer.analyze_dialogue(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

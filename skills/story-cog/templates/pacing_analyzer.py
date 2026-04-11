#!/usr/bin/env python3
"""
节奏控制分析器
分析故事节奏，提供优化建议
"""

import json
import sys
import re
from typing import Dict, List, Any, Tuple

class PacingAnalyzer:
    """节奏分析器"""

    # 节奏类型
    PACING_TYPES = {
        'fast': {'name': '快节奏', 'description': '紧张刺激，适合动作场景'},
        'medium': {'name': '中等节奏', 'description': '张弛有度，适合日常场景'},
        'slow': {'name': '慢节奏', 'description': '舒缓细腻，适合情感场景'}
    }

    # 场景类型与节奏匹配
    SCENE_PACING = {
        'action': 'fast',
        'dialogue': 'medium',
        'description': 'slow',
        'introspection': 'slow',
        'transition': 'medium',
        'climax': 'fast',
        'resolution': 'slow'
    }

    def __init__(self):
        pass

    def analyze_pacing(self, text: str) -> Dict[str, Any]:
        """分析文本节奏"""
        # 分段
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # 分析每段节奏
        segment_analysis = []
        for i, para in enumerate(paragraphs):
            pacing = self._analyze_segment_pacing(para)
            segment_analysis.append({
                'index': i + 1,
                'length': len(para),
                'pacing': pacing,
                'pacing_name': self.PACING_TYPES[pacing]['name'],
                'type': self._detect_scene_type(para)
            })

        # 计算整体节奏
        overall = self._calculate_overall_pacing(segment_analysis)

        # 检测节奏问题
        issues = self._detect_pacing_issues(segment_analysis)

        # 生成建议
        suggestions = self._generate_suggestions(issues)

        return {
            'overall_pacing': overall,
            'overall_name': self.PACING_TYPES[overall]['name'],
            'segment_count': len(paragraphs),
            'segments': segment_analysis,
            'pacing_distribution': self._calculate_distribution(segment_analysis),
            'issues': issues,
            'suggestions': suggestions,
            'rhythm_chart': self._generate_rhythm_chart(segment_analysis)
        }

    def _analyze_segment_pacing(self, text: str) -> str:
        """分析段落节奏"""
        # 基于多个因素判断
        factors = {
            'sentence_length': self._analyze_sentence_length(text),
            'dialogue_ratio': self._analyze_dialogue_ratio(text),
            'action_words': self._count_action_words(text),
            'paragraph_length': len(text)
        }

        # 综合评分
        fast_score = 0
        slow_score = 0

        # 短句 = 快节奏
        if factors['sentence_length'] < 15:
            fast_score += 2
        elif factors['sentence_length'] > 30:
            slow_score += 2

        # 对话多 = 中等节奏
        if factors['dialogue_ratio'] > 0.5:
            return 'medium'

        # 动作词多 = 快节奏
        if factors['action_words'] > 3:
            fast_score += 2

        # 段落长 = 慢节奏
        if factors['paragraph_length'] > 200:
            slow_score += 1
        elif factors['paragraph_length'] < 50:
            fast_score += 1

        if fast_score > slow_score:
            return 'fast'
        elif slow_score > fast_score:
            return 'slow'
        else:
            return 'medium'

    def _analyze_sentence_length(self, text: str) -> float:
        """分析平均句长"""
        sentences = re.split(r'[。！？]', text)
        sentences = [s for s in sentences if s.strip()]
        if not sentences:
            return 20
        return sum(len(s) for s in sentences) / len(sentences)

    def _analyze_dialogue_ratio(self, text: str) -> float:
        """分析对话占比"""
        dialogue_chars = len(re.findall(r'[""「『]([^""」』]+)[""」』]', text))
        return dialogue_chars / len(text) if text else 0

    def _count_action_words(self, text: str) -> int:
        """计算动作词数量"""
        action_words = ['跑', '跳', '打', '冲', '抓', '扔', '踢', '闪', '追', '逃']
        return sum(text.count(word) for word in action_words)

    def _detect_scene_type(self, text: str) -> str:
        """检测场景类型"""
        if self._count_action_words(text) > 2:
            return 'action'
        if self._analyze_dialogue_ratio(text) > 0.3:
            return 'dialogue'
        if len(text) > 150 and '想' in text or '感觉' in text:
            return 'introspection'
        return 'description'

    def _calculate_overall_pacing(self, segments: List[Dict]) -> str:
        """计算整体节奏"""
        if not segments:
            return 'medium'

        pacing_counts = {'fast': 0, 'medium': 0, 'slow': 0}
        for seg in segments:
            pacing_counts[seg['pacing']] += 1

        max_pacing = max(pacing_counts, key=pacing_counts.get)
        return max_pacing

    def _calculate_distribution(self, segments: List[Dict]) -> Dict[str, int]:
        """计算节奏分布"""
        distribution = {'fast': 0, 'medium': 0, 'slow': 0}
        for seg in segments:
            distribution[seg['pacing']] += 1
        return distribution

    def _detect_pacing_issues(self, segments: List[Dict]) -> List[Dict]:
        """检测节奏问题"""
        issues = []

        # 检测连续相同节奏
        current_pacing = None
        consecutive_count = 0

        for i, seg in enumerate(segments):
            if seg['pacing'] == current_pacing:
                consecutive_count += 1
            else:
                if consecutive_count >= 5:
                    issues.append({
                        'type': '节奏单调',
                        'description': f'连续{consecutive_count}段{self.PACING_TYPES[current_pacing]["name"]}',
                        'position': f'第{i-consecutive_count+1}-{i}段',
                        'suggestion': '建议插入不同节奏的段落，增加变化'
                    })
                current_pacing = seg['pacing']
                consecutive_count = 1

        # 检测节奏突变
        for i in range(1, len(segments)):
            prev_pacing = segments[i-1]['pacing']
            curr_pacing = segments[i]['pacing']
            if (prev_pacing == 'fast' and curr_pacing == 'slow') or \
               (prev_pacing == 'slow' and curr_pacing == 'fast'):
                issues.append({
                    'type': '节奏突变',
                    'description': f'从{self.PACING_TYPES[prev_pacing]["name"]}突然变为{self.PACING_TYPES[curr_pacing]["name"]}',
                    'position': f'第{i}-{i+1}段',
                    'suggestion': '建议添加过渡段落，使节奏变化更自然'
                })

        return issues

    def _generate_suggestions(self, issues: List[Dict]) -> List[str]:
        """生成优化建议"""
        suggestions = []

        if not issues:
            suggestions.append('✅ 节奏控制良好，张弛有度')
        else:
            for issue in issues[:3]:
                suggestions.append(f"💡 {issue['type']}：{issue['suggestion']}")

        return suggestions

    def _generate_rhythm_chart(self, segments: List[Dict]) -> str:
        """生成节奏图表"""
        chart = ''
        for seg in segments:
            if seg['pacing'] == 'fast':
                chart += '█'
            elif seg['pacing'] == 'medium':
                chart += '▓'
            else:
                chart += '░'
        return chart

def main():
    """主函数"""
    analyzer = PacingAnalyzer()

    if len(sys.argv) < 2:
        # 演示模式
        demo_text = '''
        他猛地冲向前方，子弹擦过耳边。

        "快跑！"他大喊道。

        她愣了一下，然后转身就跑。脚步声在走廊里回荡。

        多年后，她依然记得那个下午。阳光透过窗户洒进来，一切都那么平静。

        她坐在窗边，看着外面的世界。树叶在风中轻轻摇曳，鸟儿在枝头歌唱。

        突然，门被撞开了。他冲进来，浑身是血。

        "出事了！"他喘着粗气说。
        '''
        result = analyzer.analyze_pacing(demo_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    text = sys.argv[1]
    result = analyzer.analyze_pacing(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

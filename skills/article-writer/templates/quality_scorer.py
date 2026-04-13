#!/usr/bin/env python3
"""
内容质量评分工具
从多个维度评估文章质量
"""

import json
import sys
import re
from typing import Dict, List, Any

class ContentQualityScorer:
    """内容质量评分器"""

    # 评分维度
    DIMENSIONS = {
        'structure': {
            'name': '结构完整性',
            'weight': 20,
            'criteria': ['有明确的开头', '有模块化分段', '有总结结尾']
        },
        'readability': {
            'name': '可读性',
            'weight': 20,
            'criteria': ['段落长度适中', '句子简洁', '无生僻词']
        },
        'value': {
            'name': '价值性',
            'weight': 25,
            'criteria': ['有实用信息', '有具体案例', '有可操作建议']
        },
        'engagement': {
            'name': '吸引力',
            'weight': 20,
            'criteria': ['有金句', '有数据支撑', '有情绪触发点']
        },
        'originality': {
            'name': '原创性',
            'weight': 15,
            'criteria': ['有独特观点', '有个人经验', '非纯转载']
        }
    }

    def __init__(self):
        pass

    def score_content(self, content: str) -> Dict[str, Any]:
        """评分内容"""
        scores = {}

        # 结构评分
        scores['structure'] = self._score_structure(content)

        # 可读性评分
        scores['readability'] = self._score_readability(content)

        # 价值性评分
        scores['value'] = self._score_value(content)

        # 吸引力评分
        scores['engagement'] = self._score_engagement(content)

        # 原创性评分
        scores['originality'] = self._score_originality(content)

        # 计算总分
        total_score = sum(
            scores[dim] * self.DIMENSIONS[dim]['weight'] / 100
            for dim in self.DIMENSIONS
        )

        # 生成建议
        suggestions = self._generate_suggestions(scores)

        return {
            'total_score': round(total_score, 1),
            'grade': self._get_grade(total_score),
            'dimension_scores': scores,
            'suggestions': suggestions,
            'word_count': len(content),
            'paragraph_count': len(content.split('\n\n')),
            'reading_time': f'{len(content) // 500}分钟'
        }

    def _score_structure(self, content: str) -> int:
        """评分结构"""
        score = 50

        # 检查开头
        first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
        if len(first_paragraph) > 50:
            score += 15

        # 检查模块化分段
        paragraphs = content.split('\n\n')
        if len(paragraphs) >= 3:
            score += 15

        # 检查小标题
        if re.search(r'^#+\s', content, re.MULTILINE):
            score += 10

        # 检查结尾
        if len(content) > 500 and content[-200:].count('。') >= 2:
            score += 10

        return min(100, score)

    def _score_readability(self, content: str) -> int:
        """评分可读性"""
        score = 60

        # 检查段落长度
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        avg_para_length = sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0

        if avg_para_length < 200:
            score += 15
        elif avg_para_length < 300:
            score += 10
        elif avg_para_length > 500:
            score -= 10

        # 检查句子长度
        sentences = re.split(r'[。！？]', content)
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0

        if avg_sentence_length < 30:
            score += 10
        elif avg_sentence_length > 50:
            score -= 5

        # 检查是否有列表
        if re.search(r'^\s*[-•]\s', content, re.MULTILINE):
            score += 10

        return min(100, max(0, score))

    def _score_value(self, content: str) -> int:
        """评分价值性"""
        score = 50

        # 检查是否有数字/数据
        numbers = re.findall(r'\d+', content)
        if len(numbers) >= 3:
            score += 15

        # 检查是否有具体建议
        action_words = ['建议', '推荐', '可以', '应该', '尝试', '使用']
        if any(word in content for word in action_words):
            score += 10

        # 检查是否有案例
        case_words = ['案例', '例子', '比如', '例如', '我', '我们']
        if any(word in content for word in case_words):
            score += 15

        # 检查内容长度
        if len(content) > 1000:
            score += 10

        return min(100, score)

    def _score_engagement(self, content: str) -> int:
        """评分吸引力"""
        score = 50

        # 检查金句（短句+有冲击力）
        sentences = re.split(r'[。！？]', content)
        golden_sentences = [s for s in sentences if 10 <= len(s) <= 25]
        if len(golden_sentences) >= 3:
            score += 20

        # 检查情绪词
        emotion_words = ['终于', '竟然', '没想到', '震惊', '重要', '关键', '核心']
        emotion_count = sum(1 for word in emotion_words if word in content)
        score += min(15, emotion_count * 5)

        # 检查问句（引发思考）
        if '？' in content or '?' in content:
            score += 10

        return min(100, score)

    def _score_originality(self, content: str) -> int:
        """评分原创性"""
        score = 60

        # 检查第一人称
        if '我' in content or '我们' in content:
            score += 15

        # 检查个人观点词
        opinion_words = ['认为', '觉得', '发现', '总结', '体会']
        if any(word in content for word in opinion_words):
            score += 15

        # 检查独特表达
        unique_phrases = ['我的方法是', '我的经验是', '我的理解是']
        if any(phrase in content for phrase in unique_phrases):
            score += 10

        return min(100, score)

    def _get_grade(self, score: float) -> str:
        """获取等级"""
        if score >= 90:
            return 'S'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'

    def _generate_suggestions(self, scores: Dict[str, int]) -> List[str]:
        """生成改进建议"""
        suggestions = []

        for dim, score in scores.items():
            if score < 70:
                dim_info = self.DIMENSIONS[dim]
                suggestions.append(f"💡 {dim_info['name']}不足，建议：{dim_info['criteria'][0]}")

        if not suggestions:
            suggestions.append("✅ 内容质量良好，继续保持！")

        return suggestions

def main():
    """主函数"""
    scorer = ContentQualityScorer()

    if len(sys.argv) < 2:
        # 演示模式
        demo_content = '''
        今天分享一个AI写作工具的使用方法。

        ## 01 为什么选择AI写作

        我之前写一篇文章需要2小时，现在只需要10分钟。效率提升了94%。

        ## 02 具体方法

        1. 先确定选题
        2. 用AI生成大纲
        3. 逐段完善内容
        4. 添加金句和数据

        ## 03 总结

        把重复的交给系统，把判断留给自己。
        '''
        result = scorer.score_content(demo_content)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    content = sys.argv[1]
    result = scorer.score_content(content)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

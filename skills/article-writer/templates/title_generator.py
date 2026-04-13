#!/usr/bin/env python3
"""
标题生成器
根据内容自动生成吸引人的标题
"""

import json
import sys
import re
from typing import Dict, List, Any

class TitleGenerator:
    """标题生成器"""

    # 标题公式模板
    FORMULAS = {
        'number_result': {
            'template': '{number}{unit}{action}，{result}',
            'example': '10分钟完成发布，效率提升94%'
        },
        'contrast': {
            'template': '从{before}到{after}',
            'example': '从崩溃4671次到省50%token'
        },
        'question_answer': {
            'template': '为什么{question}？{answer}',
            'example': '为什么我不再手动写文章？因为AI比我快'
        },
        'how_to': {
            'template': '如何在{time}内{goal}',
            'example': '如何在10分钟内写完一篇文章'
        },
        'list': {
            'template': '{number}个{topic}，{benefit}',
            'example': '5个AI工具，让你的效率翻倍'
        },
        'warning': {
            'template': '{warning}，{consequence}',
            'example': '别再用这个方法了，效率会越来越低'
        },
        'secret': {
            'template': '{secret}，{result}',
            'example': '这个隐藏功能，让我省了3小时'
        },
        'story': {
            'template': '我用{method}，{result}',
            'example': '我用AI写文章，10分钟搞定'
        }
    }

    # 情绪触发词
    EMOTION_WORDS = {
        'positive': ['终于', '竟然', '没想到', '发现', '揭秘', '公开'],
        'negative': ['崩溃', '踩坑', '后悔', '警告', '别再'],
        'curiosity': ['竟然', '原来', '真相', '秘密', '隐藏'],
        'urgency': ['立即', '马上', '现在', '今天', '最后']
    }

    # 数字词库
    NUMBER_WORDS = ['3', '5', '7', '10', '30', '100', '1000']

    def __init__(self):
        pass

    def generate_titles(self, content: str, count: int = 5) -> List[Dict[str, Any]]:
        """生成多个标题选项"""
        # 提取关键信息
        keywords = self._extract_keywords(content)
        numbers = self._extract_numbers(content)

        titles = []

        # 基于不同公式生成标题
        for formula_name, formula in self.FORMULAS.items():
            title = self._apply_formula(formula_name, keywords, numbers)
            if title:
                score = self._score_title(title)
                titles.append({
                    'title': title,
                    'formula': formula_name,
                    'score': score,
                    'length': len(title)
                })

        # 按分数排序
        titles.sort(key=lambda x: x['score'], reverse=True)

        return titles[:count]

    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        # 简化实现：提取高频词
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', content)
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

        # 返回高频词
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:10]]

    def _extract_numbers(self, content: str) -> List[str]:
        """提取数字"""
        numbers = re.findall(r'\d+', content)
        return numbers[:5] if numbers else ['10']

    def _apply_formula(self, formula_name: str, keywords: List[str], numbers: List[str]) -> str:
        """应用标题公式"""
        keyword = keywords[0] if keywords else '方法'
        number = numbers[0] if numbers else '10'

        templates = {
            'number_result': f'{number}分钟搞定{keyword}，效率翻倍',
            'contrast': f'从{keyword}小白到高手',
            'question_answer': f'为什么{keyword}这么重要？答案在这里',
            'how_to': f'如何在{number}分钟内掌握{keyword}',
            'list': f'{number}个{keyword}技巧，建议收藏',
            'warning': f'别再这样{keyword}了，效率会越来越低',
            'secret': f'{keyword}的秘密，终于公开了',
            'story': f'我用{keyword}，{number}天见效'
        }

        return templates.get(formula_name, f'关于{keyword}的分享')

    def _score_title(self, title: str) -> int:
        """评分标题"""
        score = 60  # 基础分

        # 长度评分（20-30字最佳）
        if 20 <= len(title) <= 30:
            score += 15
        elif 15 <= len(title) <= 35:
            score += 10

        # 包含数字
        if re.search(r'\d+', title):
            score += 10

        # 包含情绪词
        for category, words in self.EMOTION_WORDS.items():
            for word in words:
                if word in title:
                    score += 5
                    break

        # 包含动词
        verbs = ['完成', '实现', '提升', '搞定', '掌握', '学会']
        for verb in verbs:
            if verb in title:
                score += 5
                break

        return min(100, score)

    def optimize_title(self, title: str) -> Dict[str, Any]:
        """优化现有标题"""
        issues = []
        suggestions = []

        # 检查长度
        if len(title) < 15:
            issues.append('标题过短')
            suggestions.append('增加具体信息，如数字或结果')
        elif len(title) > 35:
            issues.append('标题过长')
            suggestions.append('精简内容，突出核心')

        # 检查数字
        if not re.search(r'\d+', title):
            issues.append('缺少数字')
            suggestions.append('添加具体数字，增强可信度')

        # 检查情绪词
        has_emotion = any(word in title for words in self.EMOTION_WORDS.values() for word in words)
        if not has_emotion:
            issues.append('缺少情绪触发点')
            suggestions.append('添加情绪词，如"终于"、"竟然"、"揭秘"')

        # 生成优化版本
        optimized = self._optimize_title_text(title)

        return {
            'original': title,
            'optimized': optimized,
            'issues': issues,
            'suggestions': suggestions,
            'original_score': self._score_title(title),
            'optimized_score': self._score_title(optimized)
        }

    def _optimize_title_text(self, title: str) -> str:
        """生成优化后的标题"""
        # 简化实现
        if not re.search(r'\d+', title):
            title = f'10分钟{title}'
        if '终于' not in title and '竟然' not in title:
            title = f'{title}，终于公开了'
        return title[:35]

def main():
    """主函数"""
    generator = TitleGenerator()

    if len(sys.argv) < 2:
        # 演示模式
        demo_content = '''
        今天分享一个AI写作工具的使用方法。
        通过这个工具，我可以在10分钟内完成一篇文章。
        效率提升了94%，非常推荐给大家。
        '''
        result = generator.generate_titles(demo_content)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    content = sys.argv[1]
    result = generator.generate_titles(content)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

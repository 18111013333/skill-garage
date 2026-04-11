#!/usr/bin/env python3
"""
写作风格分析器
分析文本的写作风格特征
"""

import json
import sys
import re
from typing import Dict, List, Any
from collections import Counter

class StyleAnalyzer:
    """写作风格分析器"""

    # 风格特征定义
    STYLE_FEATURES = {
        'sentence_length': {
            'name': '句子长度',
            'short': '简洁有力',
            'medium': '节奏适中',
            'long': '细腻详尽'
        },
        'vocabulary': {
            'name': '用词风格',
            'simple': '通俗易懂',
            'medium': '雅俗共赏',
            'complex': '文采斐然'
        },
        'tone': {
            'name': '语调风格',
            'formal': '正式严谨',
            'neutral': '客观中立',
            'casual': '轻松随意'
        },
        'emotion': {
            'name': '情感色彩',
            'rational': '理性冷静',
            'balanced': '情理并重',
            'emotional': '感性丰富'
        },
        'structure': {
            'name': '结构风格',
            'linear': '线性叙事',
            'branching': '多线叙事',
            'fragmented': '碎片化叙事'
        }
    }

    # 作者风格参考
    AUTHOR_STYLES = {
        '海明威': {'sentence_length': 'short', 'vocabulary': 'simple', 'tone': 'neutral', 'emotion': 'rational'},
        '村上春树': {'sentence_length': 'medium', 'vocabulary': 'medium', 'tone': 'casual', 'emotion': 'balanced'},
        '鲁迅': {'sentence_length': 'medium', 'vocabulary': 'complex', 'tone': 'formal', 'emotion': 'rational'},
        '张爱玲': {'sentence_length': 'long', 'vocabulary': 'complex', 'tone': 'neutral', 'emotion': 'emotional'},
        '古龙': {'sentence_length': 'short', 'vocabulary': 'simple', 'tone': 'casual', 'emotion': 'emotional'}
    }

    def __init__(self):
        pass

    def analyze_style(self, text: str) -> Dict[str, Any]:
        """分析写作风格"""
        # 分句
        sentences = self._split_sentences(text)

        # 分析各维度
        features = {
            'sentence_length': self._analyze_sentence_length(sentences),
            'vocabulary': self._analyze_vocabulary(text),
            'tone': self._analyze_tone(text),
            'emotion': self._analyze_emotion(text),
            'structure': self._analyze_structure(text)
        }

        # 计算整体风格
        overall_style = self._determine_overall_style(features)

        # 找到最相似的作者风格
        similar_authors = self._find_similar_authors(features)

        # 生成风格报告
        report = self._generate_report(features, overall_style, similar_authors)

        return {
            'overall_style': overall_style,
            'features': features,
            'similar_authors': similar_authors,
            'statistics': self._get_statistics(text, sentences),
            'suggestions': self._get_style_suggestions(features),
            'report': report
        }

    def _split_sentences(self, text: str) -> List[str]:
        """分句"""
        sentences = re.split(r'[。！？\n]', text)
        return [s.strip() for s in sentences if s.strip()]

    def _analyze_sentence_length(self, sentences: List[str]) -> Dict[str, Any]:
        """分析句子长度"""
        if not sentences:
            return {'style': 'medium', 'avg_length': 0}

        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)

        if avg_length < 15:
            style = 'short'
        elif avg_length < 30:
            style = 'medium'
        else:
            style = 'long'

        return {
            'style': style,
            'style_name': self.STYLE_FEATURES['sentence_length'][style],
            'avg_length': round(avg_length, 1),
            'max_length': max(lengths),
            'min_length': min(lengths),
            'short_count': sum(1 for l in lengths if l < 15),
            'long_count': sum(1 for l in lengths if l > 40)
        }

    def _analyze_vocabulary(self, text: str) -> Dict[str, Any]:
        """分析用词风格"""
        # 检查成语和典故
        idioms = len(re.findall(r'[\u4e00-\u9fa5]{4}', text))

        # 检查简单词
        simple_words = len(re.findall(r'[的是不了在]', text))

        # 检查复杂词
        complex_words = len(re.findall(r'[\u4e00-\u9fa5]{3,}', text))

        total_chars = len(text)
        if total_chars == 0:
            return {'style': 'medium', 'complexity': 0}

        complexity = (idioms + complex_words) / total_chars * 100

        if complexity < 5:
            style = 'simple'
        elif complexity < 15:
            style = 'medium'
        else:
            style = 'complex'

        return {
            'style': style,
            'style_name': self.STYLE_FEATURES['vocabulary'][style],
            'complexity': round(complexity, 2),
            'idiom_count': idioms,
            'unique_words': len(set(re.findall(r'[\u4e00-\u9fa5]+', text)))
        }

    def _analyze_tone(self, text: str) -> Dict[str, Any]:
        """分析语调风格"""
        # 正式语调标记
        formal_markers = ['因此', '然而', '综上所述', '由此可见', '值得注意的是']
        # 随意语调标记
        casual_markers = ['哈哈', '嗯', '啊', '吧', '呢', '嘛']

        formal_count = sum(text.count(m) for m in formal_markers)
        casual_count = sum(text.count(m) for m in casual_markers)

        if formal_count > casual_count * 2:
            style = 'formal'
        elif casual_count > formal_count * 2:
            style = 'casual'
        else:
            style = 'neutral'

        return {
            'style': style,
            'style_name': self.STYLE_FEATURES['tone'][style],
            'formal_markers': formal_count,
            'casual_markers': casual_count
        }

    def _analyze_emotion(self, text: str) -> Dict[str, Any]:
        """分析情感色彩"""
        # 理性标记
        rational_markers = ['分析', '研究', '数据', '证明', '表明', '显示']
        # 感性标记
        emotional_markers = ['感动', '悲伤', '喜悦', '愤怒', '恐惧', '爱', '恨']

        rational_count = sum(text.count(m) for m in rational_markers)
        emotional_count = sum(text.count(m) for m in emotional_markers)

        if rational_count > emotional_count * 2:
            style = 'rational'
        elif emotional_count > rational_count * 2:
            style = 'emotional'
        else:
            style = 'balanced'

        return {
            'style': style,
            'style_name': self.STYLE_FEATURES['emotion'][style],
            'rational_markers': rational_count,
            'emotional_markers': emotional_count
        }

    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """分析结构风格"""
        # 检查段落
        paragraphs = [p for p in text.split('\n\n') if p.strip()]

        # 检查时间标记
        time_markers = ['首先', '然后', '接着', '最后', '后来', '之前']
        time_count = sum(text.count(m) for m in time_markers)

        # 检查转折
        transitions = ['但是', '然而', '不过', '却', '反而']
        transition_count = sum(text.count(m) for m in transitions)

        if time_count > transition_count:
            style = 'linear'
        elif transition_count > time_count:
            style = 'branching'
        else:
            style = 'linear'  # 默认线性

        return {
            'style': style,
            'style_name': self.STYLE_FEATURES['structure'][style],
            'paragraph_count': len(paragraphs),
            'time_markers': time_count,
            'transitions': transition_count
        }

    def _determine_overall_style(self, features: Dict) -> str:
        """确定整体风格"""
        styles = [f['style'] for f in features.values()]

        # 简单统计
        style_counts = Counter(styles)
        most_common = style_counts.most_common(1)[0][0]

        style_names = {
            'short': '简洁明快',
            'medium': '中规中矩',
            'long': '细腻详尽',
            'simple': '通俗易懂',
            'complex': '文采斐然',
            'formal': '正式严谨',
            'casual': '轻松随意',
            'neutral': '客观中立',
            'rational': '理性冷静',
            'emotional': '感性丰富',
            'balanced': '情理并重',
            'linear': '线性叙事',
            'branching': '多线叙事'
        }

        return style_names.get(most_common, '综合风格')

    def _find_similar_authors(self, features: Dict) -> List[Dict[str, float]]:
        """找到最相似的作者风格"""
        similarities = []

        for author, author_features in self.AUTHOR_STYLES.items():
            matches = sum(1 for k, v in features.items() if v['style'] == author_features.get(k))
            similarity = matches / len(author_features) * 100
            similarities.append({
                'author': author,
                'similarity': round(similarity, 1)
            })

        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:3]

    def _get_statistics(self, text: str, sentences: List[str]) -> Dict[str, Any]:
        """获取统计信息"""
        words = re.findall(r'[\u4e00-\u9fa5]+', text)

        return {
            'total_chars': len(text),
            'total_sentences': len(sentences),
            'total_words': len(words),
            'unique_words': len(set(words)),
            'avg_sentence_length': round(len(text) / len(sentences), 1) if sentences else 0
        }

    def _get_style_suggestions(self, features: Dict) -> List[str]:
        """获取风格改进建议"""
        suggestions = []

        if features['sentence_length']['style'] == 'long':
            suggestions.append('💡 建议适当缩短句子，增强节奏感')

        if features['vocabulary']['style'] == 'complex':
            suggestions.append('💡 建议适当简化用词，提高可读性')

        if features['tone']['style'] == 'formal':
            suggestions.append('💡 可以适当增加口语化表达，拉近距离')

        if not suggestions:
            suggestions.append('✅ 风格平衡良好，继续保持')

        return suggestions

    def _generate_report(self, features: Dict, overall: str, authors: List) -> str:
        """生成风格报告"""
        report = f"""
## 写作风格分析报告

### 整体风格
{overall}

### 风格特征
- 句子长度：{features['sentence_length']['style_name']}
- 用词风格：{features['vocabulary']['style_name']}
- 语调风格：{features['tone']['style_name']}
- 情感色彩：{features['emotion']['style_name']}
- 结构风格：{features['structure']['style_name']}

### 相似作者
"""
        for author in authors:
            report += f"- {author['author']}：相似度 {author['similarity']}%\n"

        return report

def main():
    """主函数"""
    analyzer = StyleAnalyzer()

    if len(sys.argv) < 2:
        # 演示模式
        demo_text = '''
        那天早上，我发现自己的墓碑立在院子里。

        这不可能。我明明还活着。我摸了摸自己的脸，温热的。

        墓碑上刻着我的名字，出生日期，还有一个我不认识的死亡日期——明天。

        我开始回想，最近发生了什么。一切都很正常，直到我发现那个细节。
        '''
        result = analyzer.analyze_style(demo_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    text = sys.argv[1]
    result = analyzer.analyze_style(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

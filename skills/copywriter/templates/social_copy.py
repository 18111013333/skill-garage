#!/usr/bin/env python3
"""
社交媒体文案生成器
根据平台特性自动生成适配的文案
"""

import json
import sys
from typing import Dict, List, Any

class SocialCopyGenerator:
    """社交媒体文案生成器"""

    # 平台配置
    PLATFORM_CONFIG = {
        'xiaohongshu': {
            'max_length': 1000,
            'emoji_density': 'high',  # high/medium/low
            'style': '种草感',
            'structure': ['开头痛点', '分点介绍', '使用感受', '推荐理由', '互动引导'],
            'hashtags': True,
            'hashtag_count': 5
        },
        'weibo': {
            'max_length': 2000,
            'emoji_density': 'medium',
            'style': '短平快',
            'structure': ['核心观点', '分点陈述', '话题标签'],
            'hashtags': True,
            'hashtag_count': 3
        },
        'douyin': {
            'max_length': 2200,
            'emoji_density': 'medium',
            'style': '黄金3秒',
            'structure': ['开头钩子', '核心内容', '互动引导'],
            'hashtags': True,
            'hashtag_count': 3
        },
        'wechat': {
            'max_length': 20000,
            'emoji_density': 'low',
            'style': '深度阅读',
            'structure': ['开头悬念', '模块化正文', '结尾升华'],
            'hashtags': False,
            'hashtag_count': 0
        },
        'zhihu': {
            'max_length': 50000,
            'emoji_density': 'low',
            'style': '专业感',
            'structure': ['直接回答', '论据支撑', '案例佐证', '总结延伸'],
            'hashtags': False,
            'hashtag_count': 0
        }
    }

    # Emoji库
    EMOJIS = {
        'positive': ['✅', '👍', '💪', '🔥', '⭐', '💯', '🌟', '✨'],
        'highlight': ['‼️', '⚠️', '💡', '📌', '🎯', '💎'],
        'emotion': ['😍', '🥰', '😭', '😱', '🤯', '🤩'],
        'action': ['👉', '👇', '👆', '👈', '↗️', '➡️']
    }

    def __init__(self):
        pass

    def generate_copy(self, content: str, platform: str, style: str = 'default') -> Dict[str, Any]:
        """生成平台适配文案"""
        config = self.PLATFORM_CONFIG.get(platform, self.PLATFORM_CONFIG['weibo'])

        # 提取关键信息
        key_points = self._extract_key_points(content)

        # 根据平台生成文案
        if platform == 'xiaohongshu':
            return self._generate_xiaohongshu(key_points, config)
        elif platform == 'weibo':
            return self._generate_weibo(key_points, config)
        elif platform == 'douyin':
            return self._generate_douyin(key_points, config)
        elif platform == 'wechat':
            return self._generate_wechat(key_points, config)
        elif platform == 'zhihu':
            return self._generate_zhihu(key_points, config)
        else:
            return self._generate_weibo(key_points, config)

    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        # 简单实现：按句号分割
        sentences = content.replace('。', '。\n').split('\n')
        points = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        return points[:5]  # 最多5个关键点

    def _generate_xiaohongshu(self, points: List[str], config: Dict) -> Dict[str, Any]:
        """生成小红书文案"""
        emoji = self.EMOJIS

        # 开头
        intro = f"姐妹们！{emoji['emotion'][0]} "

        # 分点
        body_lines = []
        for i, point in enumerate(points[:3]):
            body_lines.append(f"{emoji['positive'][i]} {point}")

        # 结尾
        ending = f"\n\n{emoji['highlight'][0]} 真的太香了！快去试试～"

        # 话题标签
        hashtags = '\n\n#好物分享 #种草 #推荐 #实用'

        full_copy = intro + '\n\n' + '\n'.join(body_lines) + ending + hashtags

        return {
            'platform': 'xiaohongshu',
            'copy': full_copy,
            'length': len(full_copy),
            'hashtags': ['#好物分享', '#种草', '#推荐', '#实用'],
            'style': '种草感'
        }

    def _generate_weibo(self, points: List[str], config: Dict) -> Dict[str, Any]:
        """生成微博文案"""
        emoji = self.EMOJIS

        # 核心观点
        headline = f"{emoji['highlight'][0]} {points[0] if points else '今日分享'}"

        # 分点
        body_lines = []
        for i, point in enumerate(points[:3], 1):
            body_lines.append(f"{i}. {point}")

        # 话题
        hashtags = ' #效率提升# #实用技巧#'

        full_copy = headline + '\n\n' + '\n'.join(body_lines) + hashtags

        return {
            'platform': 'weibo',
            'copy': full_copy,
            'length': len(full_copy),
            'hashtags': ['#效率提升', '#实用技巧'],
            'style': '短平快'
        }

    def _generate_douyin(self, points: List[str], config: Dict) -> Dict[str, Any]:
        """生成抖音文案"""
        emoji = self.EMOJIS

        # 黄金3秒开头
        hook = f"别划走！{emoji['emotion'][4]} 这个方法太绝了！"

        # 内容
        body = '\n'.join([f"👉 {p}" for p in points[:3]])

        # 互动
        ending = f"\n\n{emoji['action'][0]} 点赞收藏，下次找得到！"

        hashtags = ' #干货分享 #实用技巧'

        full_copy = hook + '\n\n' + body + ending + hashtags

        return {
            'platform': 'douyin',
            'copy': full_copy,
            'length': len(full_copy),
            'hashtags': ['#干货分享', '#实用技巧'],
            'style': '黄金3秒'
        }

    def _generate_wechat(self, points: List[str], config: Dict) -> Dict[str, Any]:
        """生成微信公众号文案"""
        # 开头
        intro = points[0] if points else '今天分享一个重要发现。'

        # 模块化正文
        body = '\n\n'.join([f"## 0{i}\n{p}" for i, p in enumerate(points[1:4], 1)])

        # 结尾
        ending = "\n\n---\n\n**总结**：把重复的交给系统，把判断留给自己。"

        full_copy = intro + '\n\n' + body + ending

        return {
            'platform': 'wechat',
            'copy': full_copy,
            'length': len(full_copy),
            'hashtags': [],
            'style': '深度阅读'
        }

    def _generate_zhihu(self, points: List[str], config: Dict) -> Dict[str, Any]:
        """生成知乎文案"""
        # 直接回答
        answer = points[0] if points else '这是一个很好的问题。'

        # 论据
        evidence = '\n\n'.join([f"**{i}.** {p}" for i, p in enumerate(points[1:4], 1)])

        # 总结
        summary = "\n\n---\n\n**总结**：核心在于找到适合自己的方法，并持续优化。"

        full_copy = answer + '\n\n' + evidence + summary

        return {
            'platform': 'zhihu',
            'copy': full_copy,
            'length': len(full_copy),
            'hashtags': [],
            'style': '专业感'
        }

def main():
    """主函数"""
    generator = SocialCopyGenerator()

    if len(sys.argv) < 3:
        # 演示模式
        demo_content = "AI写作工具可以大幅提升效率。10分钟就能完成一篇文章。支持多平台发布。操作简单易上手。"
        result = generator.generate_copy(demo_content, 'xiaohongshu')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    platform = sys.argv[1]
    content = sys.argv[2]

    result = generator.generate_copy(content, platform)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

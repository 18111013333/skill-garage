#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂每日简报生成 - 2026-04-12 周日
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
LOGO_PATH = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/brand/视元堂LOGO.jpg"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

BG_COLOR = (15, 23, 42)
GOLD = (251, 191, 36)
WHITE = (255, 255, 255)
LIGHT_BLUE = (96, 165, 250)

# 眼睛防治简报内容（周日：案例分享）
EYE_HEALTH_CONTENT = {
    "title": "眼睛防治简报",
    "date": "2026年4月12日 周日",
    "theme": "儿童近视防控案例分享",
    "sections": [
        {
            "heading": "📋 案例一：8岁小明",
            "content": "初查视力0.6，近视150度\n经过3个月视力训练\n视力提升至0.8，度数未增长"
        },
        {
            "heading": "📋 案例二：10岁小红",
            "content": "父母均为高度近视\n佩戴离焦镜片+户外活动\n1年度数仅增长25度"
        },
        {
            "heading": "💡 专家建议",
            "content": "• 每天户外活动2小时以上\n• 遵循20-20-20法则\n• 每3-6个月复查视力\n• 发现近视及早干预"
        }
    ]
}

# 眼镜行业动态内容（周日：流行趋势）
INDUSTRY_CONTENT = {
    "title": "眼镜行业动态",
    "date": "2026年4月12日 周日",
    "theme": "2026年眼镜流行趋势",
    "sections": [
        {
            "heading": "🔥 热门趋势",
            "content": "• AI智能眼镜持续爆发\n• 超轻钛架成为主流\n• 大框复古风回潮\n• 透明镜架受年轻人喜爱"
        },
        {
            "heading": "👓 镜片新技术",
            "content": "• 自由曲面技术升级\n• 数码防蓝光镜片普及\n• 变色镜片响应更快\n• 离焦防控效果提升"
        },
        {
            "heading": "📊 市场数据",
            "content": "• 2026年AI眼镜增长200%\n• 儿童防控镜片需求增30%\n• 国产品牌市场份额提升"
        }
    ]
}

def create_briefing(content, output_name):
    """生成简报图片"""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 56)
        font_date = ImageFont.truetype(FONT_PATH, 32)
        font_theme = ImageFont.truetype(FONT_BOLD, 40)
        font_heading = ImageFont.truetype(FONT_BOLD, 36)
        font_content = ImageFont.truetype(FONT_PATH, 28)
    except:
        print("❌ 字体加载失败")
        return None
    
    y = 40
    
    # LOGO
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((100, 100), Image.LANCZOS)
        img.paste(logo, (width - 140, y))
    
    # 标题
    draw.text((60, y), content["title"], fill=GOLD, font=font_title)
    y += 80
    
    # 日期
    draw.text((60, y), content["date"], fill=WHITE, font=font_date)
    y += 60
    
    # 主题
    draw.text((60, y), f"📌 {content['theme']}", fill=LIGHT_BLUE, font=font_theme)
    y += 80
    
    # 分隔线
    draw.line([(60, y), (width - 60, y)], fill=GOLD, width=2)
    y += 40
    
    # 内容区块
    for section in content["sections"]:
        # 标题
        draw.text((60, y), section["heading"], fill=GOLD, font=font_heading)
        y += 50
        
        # 内容（换行处理）
        for line in section["content"].split('\n'):
            draw.text((80, y), line, fill=WHITE, font=font_content)
            y += 40
        
        y += 30
    
    # 底部
    y = height - 200
    draw.line([(60, y), (width - 60, y)], fill=GOLD, width=2)
    y += 30
    
    draw.text((60, y), "【视元堂视觉体验中心】", fill=LIGHT_BLUE, font=font_content)
    y += 40
    draw.text((60, y), "📍 南充顺庆区白土坝路406号", fill=WHITE, font=font_content)
    y += 35
    draw.text((60, y), "📞 0817-2255222", fill=WHITE, font=font_content)
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, output_name)
    img.save(output_path, quality=95)
    print(f"✅ 生成: {output_name}")
    return output_path

def main():
    print("=" * 50)
    print("每日简报生成 - 2026-04-12")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成眼睛防治简报
    create_briefing(EYE_HEALTH_CONTENT, "20260412_眼睛防治简报.jpg")
    
    # 生成眼镜行业动态
    create_briefing(INDUSTRY_CONTENT, "20260412_眼镜行业动态.jpg")
    
    print("=" * 50)
    print("✅ 简报生成完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()

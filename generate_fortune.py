#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老板陈飞紫微斗数运势 - 2026-04-12 周日
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
RED = (239, 68, 68)
GREEN = (34, 197, 94)

# 老板八字：辛酉年 辛卯月 癸巳日 壬戌时
# 周日运势（根据紫微斗数推算）
FORTUNE_CONTENT = {
    "title": "紫微斗数每日运势",
    "name": "陈飞",
    "date": "2026年4月12日 周日",
    "overall": "⭐⭐⭐⭐ 上佳",
    "lucky_color": "金色、蓝色",
    "lucky_direction": "东南",
    
    "aspects": [
        {
            "name": "💰 财运",
            "stars": "⭐⭐⭐⭐⭐",
            "desc": "财运亨通，适合收款签约"
        },
        {
            "name": "📈 事业",
            "stars": "⭐⭐⭐⭐",
            "desc": "贵人相助，利于洽谈合作"
        },
        {
            "name": "❤️ 感情",
            "stars": "⭐⭐⭐⭐",
            "desc": "家庭和睦，适合陪伴家人"
        },
        {
            "name": "💪 健康",
            "stars": "⭐⭐⭐",
            "desc": "注意休息，避免熬夜"
        }
    ],
    
    "yi": [
        "签约、收款、开会",
        "拜访客户、拓展业务",
        "家庭聚会、陪伴家人",
        "学习进修、读书看报"
    ],
    
    "ji": [
        "大额投资、冲动消费",
        "与人争执、口舌是非",
        "熬夜劳累、剧烈运动",
        "签署重要文件"
    ]
}

def create_fortune(content, output_name):
    """生成运势图片"""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 52)
        font_name = ImageFont.truetype(FONT_BOLD, 44)
        font_date = ImageFont.truetype(FONT_PATH, 30)
        font_section = ImageFont.truetype(FONT_BOLD, 36)
        font_content = ImageFont.truetype(FONT_PATH, 28)
        font_small = ImageFont.truetype(FONT_PATH, 24)
    except:
        print("❌ 字体加载失败")
        return None
    
    y = 40
    
    # LOGO
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((80, 80), Image.LANCZOS)
        img.paste(logo, (width - 120, y))
    
    # 标题
    draw.text((60, y), content["title"], fill=GOLD, font=font_title)
    y += 70
    
    # 姓名
    draw.text((60, y), f"👤 {content['name']}", fill=WHITE, font=font_name)
    y += 60
    
    # 日期
    draw.text((60, y), content["date"], fill=LIGHT_BLUE, font=font_date)
    y += 50
    
    # 综合运势
    draw.text((60, y), f"综合运势：{content['overall']}", fill=GOLD, font=font_section)
    y += 50
    
    # 幸运元素
    draw.text((60, y), f"幸运色：{content['lucky_color']}  方位：{content['lucky_direction']}", fill=WHITE, font=font_small)
    y += 60
    
    # 分隔线
    draw.line([(60, y), (width - 60, y)], fill=GOLD, width=2)
    y += 30
    
    # 各方面运势
    for aspect in content["aspects"]:
        draw.text((60, y), f"{aspect['name']} {aspect['stars']}", fill=GOLD, font=font_content)
        y += 35
        draw.text((80, y), aspect['desc'], fill=WHITE, font=font_small)
        y += 45
    
    y += 20
    
    # 宜
    draw.line([(60, y), (width - 60, y)], fill=GREEN, width=2)
    y += 20
    draw.text((60, y), "✅ 宜", fill=GREEN, font=font_section)
    y += 45
    
    for item in content["yi"]:
        draw.text((80, y), f"• {item}", fill=WHITE, font=font_small)
        y += 35
    
    y += 20
    
    # 忌
    draw.line([(60, y), (width - 60, y)], fill=RED, width=2)
    y += 20
    draw.text((60, y), "🚫 忌", fill=RED, font=font_section)
    y += 45
    
    for item in content["ji"]:
        draw.text((80, y), f"• {item}", fill=WHITE, font=font_small)
        y += 35
    
    # 底部
    y = height - 80
    draw.line([(60, y), (width - 60, y)], fill=GOLD, width=2)
    y += 25
    draw.text((60, y), "☀️ 小太阳祝老板今日顺遂！", fill=GOLD, font=font_content)
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, output_name)
    img.save(output_path, quality=95)
    print(f"✅ 生成: {output_name}")
    return output_path

def main():
    print("=" * 50)
    print("紫微斗数运势 - 2026-04-12")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_fortune(FORTUNE_CONTENT, "20260412_紫微斗数运势.jpg")
    
    print("=" * 50)
    print("✅ 运势生成完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数命盘图片生成器 - 唐晓兰女士
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 颜色
DEEP_BLUE = (15, 23, 42)
NAVY = (30, 58, 138)
GOLD = (251, 191, 36)
LIGHT_GOLD = (253, 224, 71)
WHITE = (255, 255, 255)
PURPLE = (139, 92, 246)
ORANGE = (249, 115, 22)
RED = (239, 68, 68)
GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)

def create_ziwei_chart():
    """生成完整紫微斗数命盘图片"""
    
    # 创建画布 (1080x2800)
    img = Image.new('RGB', (1080, 2800), DEEP_BLUE)
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = ImageFont.truetype(FONT_BOLD, 52)
    main_font = ImageFont.truetype(FONT_BOLD, 38)
    sub_font = ImageFont.truetype(FONT_PATH, 30)
    small_font = ImageFont.truetype(FONT_PATH, 26)
    tiny_font = ImageFont.truetype(FONT_PATH, 22)
    
    y = 0
    
    # ===== 顶部标题 =====
    draw.rectangle([(0, 0), (1080, 110)], fill=NAVY)
    draw.text((540, 55), "🔮 紫微斗数命盘详解", fill=GOLD, font=title_font, anchor="mm")
    y = 130
    
    # ===== 出生信息 =====
    draw.rectangle([(30, y), (1050, y + 140)], fill=DARK_GRAY, outline=ORANGE, width=2)
    y += 20
    draw.text((540, y), "👤 唐晓兰女士", fill=ORANGE, font=main_font, anchor="mm")
    y += 50
    draw.text((540, y), "📅 公历1986年4月15日 17:30（酉时）", fill=WHITE, font=sub_font, anchor="mm")
    y += 40
    draw.text((540, y), "🐅 生肖：虎 | 🏛️ 命宫：太阳巨门同宫（日巨同宫格）", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 80
    
    # ===== 命盘十二宫详解 =====
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "📊 十二宫详解", fill=GOLD, font=main_font, anchor="mm")
    y += 70
    
    palaces = [
        ("【命宫】", "太阳、巨门", "日巨同宫格，口才好，善于表达，适合教育销售传媒", ORANGE, "⭐⭐⭐⭐⭐"),
        ("【兄弟宫】", "天机、太阴", "兄弟姐妹聪明，关系融洽，家庭氛围好", WHITE, "⭐⭐⭐⭐"),
        ("【夫妻宫】", "紫微、天府", "配偶能力强，有领导才能，婚姻美满，配偶事业有成", GOLD, "⭐⭐⭐⭐⭐"),
        ("【子女宫】", "天同、天梁", "子女孝顺懂事，有出息，亲子关系融洽", WHITE, "⭐⭐⭐⭐"),
        ("【财帛宫】", "武曲、贪狼", "财运旺盛，有偏财运，适合创业经商，投资有道", GOLD, "⭐⭐⭐⭐⭐"),
        ("【疾厄宫】", "廉贞、天相", "注意心血管、皮肤问题，宜保持心情愉快", RED, "⭐⭐⭐"),
        ("【迁移宫】", "天府", "出外发展顺利，贵人多，适合在外地发展事业", WHITE, "⭐⭐⭐⭐"),
        ("仆役宫", "太阴", "朋友多，女性贵人多，人缘好，善于交际", WHITE, "⭐⭐⭐⭐"),
        ("【官禄宫】", "天梁", "事业有成，有贵人提携，适合管理教育医疗行业", GOLD, "⭐⭐⭐⭐⭐"),
        ("【田宅宫】", "七杀", "置业运一般，宜谨慎投资，不宜过多投资房产", WHITE, "⭐⭐⭐"),
        ("【福德宫】", "天机", "心思细腻，想得多，宜学会放松，享受生活", WHITE, "⭐⭐⭐"),
        ("【父母宫】", "破军", "与父母缘分较浅，宜多沟通，增进感情", WHITE, "⭐⭐⭐"),
    ]
    
    box_height = 95
    for i, (name, stars, desc, color, rating) in enumerate(palaces):
        bg_color = DARK_GRAY if i % 2 == 0 else (40, 55, 75)
        draw.rectangle([(30, y), (1050, y + box_height - 5)], fill=bg_color, outline=color, width=2)
        
        draw.text((50, y + 15), name, fill=color, font=sub_font)
        draw.text((200, y + 15), stars, fill=WHITE, font=sub_font)
        draw.text((900, y + 15), rating, fill=color, font=small_font)
        
        if len(desc) > 25:
            draw.text((50, y + 50), desc[:25], fill=GRAY, font=tiny_font)
            draw.text((50, y + 72), desc[25:], fill=GRAY, font=tiny_font)
        else:
            draw.text((50, y + 55), desc, fill=GRAY, font=tiny_font)
        
        y += box_height
    
    # ===== 2026年运势详解 =====
    y += 20
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "📈 2026年运势详解", fill=GOLD, font=main_font, anchor="mm")
    y += 70
    
    fortunes = [
        ("事业运", "★★★★★", "大吉大利", "事业运势大旺，有贵人相助，宜把握机遇", GOLD),
        ("财运", "★★★★★", "财源广进", "正财偏财皆旺，投资有道，可创业经商", GOLD),
        ("感情运", "★★★★☆", "吉祥如意", "婚姻美满，夫妻感情稳定，家庭和睦", ORANGE),
        ("健康运", "★★★☆☆", "平稳注意", "注意心血管保养，宜多运动，定期体检", WHITE),
    ]
    
    for name, stars, desc, detail, color in fortunes:
        draw.rectangle([(30, y), (1050, y + 80)], fill=DARK_GRAY, outline=color, width=1)
        draw.text((50, y + 15), name, fill=color, font=sub_font)
        draw.text((200, y + 15), stars, fill=color, font=sub_font)
        draw.text((450, y + 15), desc, fill=WHITE, font=sub_font)
        draw.text((50, y + 50), detail, fill=GRAY, font=tiny_font)
        y += 90
    
    # ===== 开运建议详解 =====
    y += 10
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "💡 开运建议", fill=GOLD, font=main_font, anchor="mm")
    y += 70
    
    draw.rectangle([(30, y), (1050, y + 280)], fill=DARK_GRAY, outline=PURPLE, width=2)
    y += 15
    
    tips = [
        ("🎨 幸运颜色", "红色、橙色、金色"),
        ("🔢 幸运数字", "3、8"),
        ("🧭 幸运方位", "东方、南方"),
        ("🐎 生肖贵人", "马、狗"),
        ("🏢 办公布局", "办公室宜朝东或朝南"),
        ("💍 佩戴饰品", "红玛瑙、琥珀饰品增运"),
        ("👔 穿着建议", "多穿红色、橙色衣服"),
        ("🏠 家居摆设", "家中摆放红色装饰品"),
    ]
    
    for i, (title, content) in enumerate(tips):
        x = 60 if i % 2 == 0 else 550
        row = i // 2
        draw.text((x, y + row * 35), f"{title}：{content}", fill=WHITE, font=small_font)
    
    y += 300
    
    # ===== 注意事项 =====
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "⚠️ 注意事项", fill=RED, font=main_font, anchor="mm")
    y += 70
    
    draw.rectangle([(30, y), (1050, y + 220)], fill=DARK_GRAY, outline=RED, width=2)
    y += 15
    
    warnings = [
        "• 避免与属猴、属蛇之人合伙",
        "• 投资宜把握时机，不宜犹豫",
        "• 注意调节压力，避免过度劳累",
        "• 定期体检，关注心血管健康",
        "• 保持心情愉快，避免情绪波动",
        "• 与父母多沟通，增进感情",
    ]
    
    for warning in warnings:
        draw.text((50, y), warning, fill=WHITE, font=small_font)
        y += 32
    
    y += 40
    
    # ===== 总评 =====
    draw.rectangle([(30, y), (1050, y + 160)], fill=NAVY, outline=ORANGE, width=3)
    y += 20
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    draw.text((540, y), "太阳巨门同宫，日巨同宫格！", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 45
    draw.text((540, y), "命格上佳，事业有成，财运旺盛，婚姻美满！", fill=WHITE, font=sub_font, anchor="mm")
    
    # ===== 底部 =====
    y = 2750
    draw.text((540, y), "2026年事业财运大吉，宜把握机遇！", fill=ORANGE, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "紫微斗数命盘_唐晓兰女士.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 命盘图片已保存: {output_path}")
    print(f"   尺寸: {img.size}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_ziwei_chart()

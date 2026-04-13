#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数命盘图片生成器 - 李永丹女士
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
PINK = (236, 72, 153)
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
    draw.rectangle([(30, y), (1050, y + 140)], fill=DARK_GRAY, outline=PINK, width=2)
    y += 20
    draw.text((540, y), "👤 李永丹女士", fill=PINK, font=main_font, anchor="mm")
    y += 50
    draw.text((540, y), "📅 农历癸酉年（1993年）八月十三日 子时", fill=WHITE, font=sub_font, anchor="mm")
    y += 40
    draw.text((540, y), "🐓 生肖：鸡 | 🏛️ 命宫：天机太阴同宫（机月同梁格）", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 80
    
    # ===== 命盘十二宫详解 =====
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "📊 十二宫详解", fill=GOLD, font=main_font, anchor="mm")
    y += 70
    
    palaces = [
        ("【命宫】", "天机、太阴", "机月同梁格，聪明伶俐，心思细腻，适合文职策划设计", PINK, "⭐⭐⭐⭐⭐"),
        ("【兄弟宫】", "紫微、天府", "兄弟有出息，家庭条件好，兄弟姐妹关系融洽", WHITE, "⭐⭐⭐⭐"),
        ("【夫妻宫】", "武曲、贪狼", "配偶能力强，事业心重，晚婚为宜，婚后生活富足", LIGHT_GOLD, "⭐⭐⭐⭐⭐"),
        ("【子女宫】", "太阳、巨门", "子女聪明活泼，口才好，注意与子女沟通方式", WHITE, "⭐⭐⭐⭐"),
        ("【财帛宫】", "天同、天梁", "财运平稳，适合稳定工作，不宜投机，宜稳健理财", GOLD, "⭐⭐⭐⭐"),
        ("【疾厄宫】", "七杀", "注意妇科、肠胃问题，宜保持心情愉快，定期体检", RED, "⭐⭐⭐"),
        ("【迁移宫】", "廉贞、天相", "出外发展顺利，贵人相助，适合在外地工作发展", WHITE, "⭐⭐⭐⭐"),
        ("仆役宫", "破军", "朋友多但知心少，宜谨慎交友，防小人", WHITE, "⭐⭐⭐"),
        ("【官禄宫】", "天府", "事业稳定，适合体制内工作，有贵人提携，升迁顺利", GOLD, "⭐⭐⭐⭐"),
        ("【田宅宫】", "太阴", "置业运佳，房产运好，宜投资不动产", WHITE, "⭐⭐⭐⭐"),
        ("【福德宫】", "天机", "心思细腻，想得多，宜学会放松，避免焦虑", WHITE, "⭐⭐⭐"),
        ("【父母宫】", "天梁", "父母健康长寿，家庭和睦，得父母庇护支持", WHITE, "⭐⭐⭐⭐"),
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
        ("事业运", "★★★★☆", "吉祥如意", "工作稳定，有贵人相助，宜把握机会", GOLD),
        ("财运", "★★★★☆", "财源广进", "收入稳定，不宜投机，宜稳健理财", GOLD),
        ("感情运", "★★★★★", "大吉大利", "感情运势大旺，宜把握良缘，有望脱单", PINK),
        ("健康运", "★★★☆☆", "平稳注意", "注意妇科保养，宜多运动，定期体检", WHITE),
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
        ("🎨 幸运颜色", "粉色、紫色、白色"),
        ("🔢 幸运数字", "2、7"),
        ("🧭 幸运方位", "南方、东南方"),
        ("🐍 生肖贵人", "蛇、牛"),
        ("🏢 卧室布局", "卧室宜朝南或东南"),
        ("💍 佩戴饰品", "珍珠、水晶饰品增运"),
        ("👔 穿着建议", "多穿粉色、紫色衣服"),
        ("🌸 家居摆设", "家中摆放鲜花增运"),
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
        "• 避免与属兔、属狗之人深交",
        "• 投资宜稳健，不宜冒险投机",
        "• 注意调节情绪，避免焦虑",
        "• 定期体检，关注妇科健康",
        "• 保持心情愉快，避免过度劳累",
        "• 谨慎交友，防小人",
    ]
    
    for warning in warnings:
        draw.text((50, y), warning, fill=WHITE, font=small_font)
        y += 32
    
    y += 40
    
    # ===== 总评 =====
    draw.rectangle([(30, y), (1050, y + 160)], fill=NAVY, outline=PINK, width=3)
    y += 20
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    draw.text((540, y), "天机太阴同宫，机月同梁格！", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 45
    draw.text((540, y), "命格温婉，事业稳定，婚姻美满，晚年享福！", fill=WHITE, font=sub_font, anchor="mm")
    
    # ===== 底部 =====
    y = 2750
    draw.text((540, y), "2026年感情运大吉，宜把握良缘！", fill=PINK, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "紫微斗数命盘_李永丹女士.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 命盘图片已保存: {output_path}")
    print(f"   尺寸: {img.size}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_ziwei_chart()

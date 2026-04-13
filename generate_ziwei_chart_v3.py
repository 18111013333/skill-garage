#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数命盘图片生成器 V3 - 完整修复版
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
RED = (239, 68, 68)
GREEN = (34, 197, 94)
BLUE = (59, 130, 246)
GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)

def create_ziwei_chart():
    """生成完整紫微斗数命盘图片"""
    
    # 创建画布 (1080x2600) - 再加长
    img = Image.new('RGB', (1080, 2600), DEEP_BLUE)
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
    draw.rectangle([(30, y), (1050, y + 140)], fill=DARK_GRAY, outline=GOLD, width=2)
    y += 20
    draw.text((540, y), "👤 陈飞老板", fill=GOLD, font=main_font, anchor="mm")
    y += 50
    draw.text((540, y), "📅 农历辛酉年（1981年）二月十九日 戌时", fill=WHITE, font=sub_font, anchor="mm")
    y += 40
    draw.text((540, y), "🐓 生肖：鸡 | 🏛️ 命宫：紫微天府同宫（帝王格局）", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 80
    
    # ===== 命盘十二宫详解 =====
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "📊 十二宫详解", fill=GOLD, font=main_font, anchor="mm")
    y += 70
    
    palaces = [
        ("【命宫】", "紫微、天府", "帝王格局，天生领袖气质，事业心极强，适合创业经商，贵人运旺", GOLD, "⭐⭐⭐⭐⭐"),
        ("【兄弟宫】", "天机", "兄弟缘薄，但朋友多，人缘好，善于交际", WHITE, "⭐⭐⭐⭐"),
        ("【夫妻宫】", "太阳、太阴", "日月同辉，婚姻美满，配偶贤惠，夫妻同心事业更顺", LIGHT_GOLD, "⭐⭐⭐⭐⭐"),
        ("【子女宫】", "武曲、贪狼", "子女聪明有出息，但需注意教育方式，宜严慈相济", WHITE, "⭐⭐⭐⭐"),
        ("【财帛宫】", "天同、天梁", "财运亨通，中年发迹，适合稳健投资，房产运佳", GOLD, "⭐⭐⭐⭐⭐"),
        ("【疾厄宫】", "七杀", "注意肝胆、呼吸系统，宜多运动，保持心情舒畅", RED, "⭐⭐⭐"),
        ("【迁移宫】", "破军", "出外发展顺利，贵人多，适合在外创业，不宜守旧", WHITE, "⭐⭐⭐⭐"),
        ("仆役宫", "廉贞、天相", "下属得力，人脉广阔，善于用人，团队管理能力强", WHITE, "⭐⭐⭐⭐"),
        ("【官禄宫】", "巨门、天机", "事业有成，适合企业管理，口才好，善于谈判", GOLD, "⭐⭐⭐⭐⭐"),
        ("【田宅宫】", "天梁", "置业运佳，房产丰厚，宜投资不动产", WHITE, "⭐⭐⭐⭐"),
        ("【福德宫】", "太阴", "晚年享福，精神生活丰富，心地善良，有慈悲心", WHITE, "⭐⭐⭐⭐"),
        ("【父母宫】", "天府", "父母健康长寿，家庭和睦，得祖荫庇护", WHITE, "⭐⭐⭐⭐"),
    ]
    
    box_height = 95
    for i, (name, stars, desc, color, rating) in enumerate(palaces):
        bg_color = DARK_GRAY if i % 2 == 0 else (40, 55, 75)
        draw.rectangle([(30, y), (1050, y + box_height - 5)], fill=bg_color, outline=color, width=2)
        
        # 宫名
        draw.text((50, y + 15), name, fill=color, font=sub_font)
        
        # 星曜
        draw.text((200, y + 15), stars, fill=WHITE, font=sub_font)
        
        # 评分
        draw.text((900, y + 15), rating, fill=color, font=small_font)
        
        # 描述（换行处理）
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
        ("事业运", "★★★★★", "大吉大利", "四家公司运势旺盛，宜把握机遇扩张业务", GOLD),
        ("财运", "★★★★★", "财源广进", "正财偏财皆旺，投资稳健可获丰厚回报", GOLD),
        ("感情运", "★★★★☆", "吉祥如意", "家庭和睦，夫妻同心，感情稳定升温", LIGHT_GOLD),
        ("健康运", "★★★☆☆", "平稳注意", "注意肝胆保养，宜多运动，定期体检", WHITE),
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
        ("🎨 幸运颜色", "金色、白色、黄色"),
        ("🔢 幸运数字", "4、9"),
        ("🧭 幸运方位", "西方、西北方"),
        ("🐍 生肖贵人", "蛇、牛"),
        ("🏢 办公布局", "办公室宜坐西朝东"),
        ("💍 佩戴饰品", "金银饰品增运"),
        ("👔 穿着建议", "多穿白色、金色衣服"),
        ("🏺 摆件建议", "办公桌摆放金属摆件"),
    ]
    
    for i, (title, content) in enumerate(tips):
        x = 60 if i % 2 == 0 else 550
        row = i // 2
        draw.text((x, y + row * 35), f"{title}：{content}", fill=WHITE, font=small_font)
    
    y += 300
    
    # ===== 注意事项（完整显示）=====
    draw.rectangle([(30, y), (1050, y + 50)], fill=NAVY)
    draw.text((540, y + 25), "⚠️ 注意事项", fill=RED, font=main_font, anchor="mm")
    y += 70
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=RED, width=2)
    y += 15
    
    warnings = [
        "• 避免与属兔、属狗之人合伙经营",
        "• 投资宜稳健，不宜冒险投机",
        "• 注意休息，避免过度劳累",
        "• 多做善事，积累福报",
        "• 定期体检，关注肝胆健康",
        "• 保持心情舒畅，避免情绪波动",
    ]
    
    for warning in warnings:
        draw.text((50, y), warning, fill=WHITE, font=small_font)
        y += 30
    
    y += 30
    
    # ===== 总评 =====
    draw.rectangle([(30, y), (1050, y + 150)], fill=NAVY, outline=GOLD, width=3)
    y += 20
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    y += 50
    draw.text((540, y), "紫微天府同宫，帝王格局！", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 40
    draw.text((540, y), "命格尊贵，事业有成，财运亨通，晚年享福！", fill=WHITE, font=sub_font, anchor="mm")
    
    # ===== 底部 =====
    y = 2550
    draw.text((540, y), "四家公司正是命中注定，2026年运势大吉！", fill=GOLD, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "紫微斗数命盘_陈飞老板_完整版.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 完整命盘图片已保存: {output_path}")
    print(f"   尺寸: {img.size}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_ziwei_chart()

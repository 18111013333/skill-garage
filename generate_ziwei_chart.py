#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数命盘图片生成器
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 颜色
DEEP_BLUE = (15, 23, 42)
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
    """生成紫微斗数命盘图片"""
    
    # 创建画布 (1080x1920)
    img = Image.new('RGB', (1080, 1920), DEEP_BLUE)
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = ImageFont.truetype(FONT_BOLD, 48)
    main_font = ImageFont.truetype(FONT_BOLD, 36)
    sub_font = ImageFont.truetype(FONT_PATH, 28)
    small_font = ImageFont.truetype(FONT_PATH, 24)
    
    # ===== 顶部标题 =====
    draw.rectangle([(0, 0), (1080, 100)], fill=(30, 58, 138))
    draw.text((540, 50), "🔮 紫微斗数命盘", fill=GOLD, font=title_font, anchor="mm")
    
    # ===== 出生信息 =====
    y = 130
    draw.text((540, y), "陈飞老板", fill=GOLD, font=main_font, anchor="mm")
    y += 50
    draw.text((540, y), "农历辛酉年（1981年）二月十九日 戌时", fill=WHITE, font=sub_font, anchor="mm")
    y += 40
    draw.text((540, y), "生肖：鸡 | 命宫：紫微天府同宫", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    
    # ===== 命盘十二宫 =====
    y = 250
    box_height = 110
    box_margin = 10
    
    palaces = [
        ("命宫", "紫微、天府", "帝王格局，天生领袖", GOLD),
        ("兄弟宫", "天机", "朋友多，人缘好", WHITE),
        ("夫妻宫", "太阳、太阴", "日月同辉，婚姻美满", LIGHT_GOLD),
        ("子女宫", "武曲、贪狼", "子女聪明有出息", WHITE),
        ("财帛宫", "天同、天梁", "财运亨通，中年发迹", GOLD),
        ("疾厄宫", "七杀", "注意肝胆、呼吸系统", RED),
        ("迁移宫", "破军", "出外发展，贵人多", WHITE),
        ("仆役宫", "廉贞、天相", "下属得力，人脉广", WHITE),
        ("官禄宫", "巨门、天机", "事业有成，善谈判", GOLD),
        ("田宅宫", "天梁", "置业运佳，房产丰", WHITE),
        ("福德宫", "太阴", "晚年享福，心地善", WHITE),
        ("父母宫", "天府", "父母长寿，家庭睦", WHITE),
    ]
    
    for i, (name, stars, desc, color) in enumerate(palaces):
        # 背景
        bg_color = DARK_GRAY if i % 2 == 0 else (40, 55, 75)
        draw.rectangle([(30, y), (1050, y + box_height - 5)], fill=bg_color, outline=color, width=2)
        
        # 宫名
        draw.text((50, y + 20), name, fill=color, font=main_font)
        
        # 星曜
        draw.text((180, y + 20), stars, fill=WHITE, font=sub_font)
        
        # 描述
        draw.text((180, y + 60), desc, fill=GRAY, font=small_font)
        
        y += box_height
    
    # ===== 2026年运势 =====
    y += 20
    draw.rectangle([(30, y), (1050, y + 180)], fill=(30, 58, 138), outline=GOLD, width=2)
    
    y += 20
    draw.text((540, y), "📊 2026年运势", fill=GOLD, font=main_font, anchor="mm")
    
    y += 50
    fortunes = [
        ("事业", "★★★★★", "大吉大利", GOLD),
        ("财运", "★★★★★", "财源广进", GOLD),
        ("感情", "★★★★☆", "吉祥如意", LIGHT_GOLD),
        ("健康", "★★★☆☆", "平稳注意", WHITE),
    ]
    
    x_start = 80
    for i, (name, stars, desc, color) in enumerate(fortunes):
        x = x_start + i * 250
        draw.text((x, y), name, fill=WHITE, font=sub_font)
        draw.text((x, y + 35), stars, fill=color, font=sub_font)
        draw.text((x, y + 70), desc, fill=GRAY, font=small_font)
    
    # ===== 开运建议 =====
    y += 200
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=PURPLE, width=2)
    
    y += 20
    draw.text((540, y), "💡 开运建议", fill=PURPLE, font=main_font, anchor="mm")
    
    y += 50
    tips = [
        "• 幸运颜色：金色、白色、黄色",
        "• 幸运数字：4、9",
        "• 幸运方位：西方、西北方",
        "• 生肖贵人：蛇、牛",
        "• 办公室宜坐西朝东",
        "• 佩戴金银饰品增运",
    ]
    
    for tip in tips:
        draw.text((60, y), tip, fill=WHITE, font=small_font)
        y += 28
    
    # ===== 总评 =====
    y += 30
    draw.rectangle([(30, y), (1050, y + 120)], fill=(30, 58, 138), outline=GOLD, width=3)
    
    y += 20
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    
    y += 50
    draw.text((540, y), "命格尊贵，事业有成，财运亨通，晚年享福！", fill=WHITE, font=sub_font, anchor="mm")
    
    # ===== 底部 =====
    y = 1850
    draw.text((540, y), "紫微天府同宫 · 帝王格局", fill=GOLD, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "紫微斗数命盘_陈飞老板.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 命盘图片已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_ziwei_chart()

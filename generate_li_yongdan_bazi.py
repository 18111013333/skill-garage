#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生辰八字命盘图片生成器 - 李永丹女士
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
ORANGE = (249, 115, 22)
GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)

def create_bazi_chart():
    """生成完整八字命盘图片"""
    
    # 创建画布 (1080x3200) - 超长版
    img = Image.new('RGB', (1080, 3200), DEEP_BLUE)
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = ImageFont.truetype(FONT_BOLD, 48)
    main_font = ImageFont.truetype(FONT_BOLD, 36)
    sub_font = ImageFont.truetype(FONT_PATH, 28)
    small_font = ImageFont.truetype(FONT_PATH, 24)
    tiny_font = ImageFont.truetype(FONT_PATH, 20)
    
    y = 0
    
    # ===== 顶部标题 =====
    draw.rectangle([(0, 0), (1080, 100)], fill=NAVY)
    draw.text((540, 50), "🔮 生辰八字命盘详解", fill=GOLD, font=title_font, anchor="mm")
    y = 120
    
    # ===== 出生信息 =====
    draw.rectangle([(30, y), (1050, y + 120)], fill=DARK_GRAY, outline=PINK, width=2)
    y += 15
    draw.text((540, y), "👤 李永丹女士", fill=PINK, font=main_font, anchor="mm")
    y += 45
    draw.text((540, y), "📅 农历癸酉年八月十三日子时", fill=WHITE, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "公历1993年9月28日 23:00-01:00 | 生肖：鸡", fill=GRAY, font=small_font, anchor="mm")
    y += 70
    
    # ===== 八字排盘 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=NAVY)
    draw.text((540, y + 22), "📊 八字排盘", fill=GOLD, font=main_font, anchor="mm")
    y += 60
    
    # 八字四柱
    draw.rectangle([(30, y), (1050, y + 180)], fill=DARK_GRAY, outline=GOLD, width=2)
    
    # 四柱标题
    pillars = [("年柱", "癸酉", "水鸡"), ("月柱", "辛酉", "金鸡"), 
               ("日柱", "己亥", "土猪"), ("时柱", "甲子", "木鼠")]
    
    for i, (name, ganzhi, desc) in enumerate(pillars):
        x = 80 + i * 250
        draw.text((x + 60, y + 20), name, fill=GOLD, font=sub_font, anchor="mm")
        draw.text((x + 60, y + 60), ganzhi[0], fill=WHITE, font=title_font, anchor="mm")
        draw.text((x + 60, y + 100), ganzhi[1], fill=WHITE, font=title_font, anchor="mm")
        draw.text((x + 60, y + 145), desc, fill=GRAY, font=tiny_font, anchor="mm")
    
    y += 200
    
    # ===== 五行分析 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=NAVY)
    draw.text((540, y + 22), "⚖️ 五行分析", fill=GOLD, font=main_font, anchor="mm")
    y += 60
    
    draw.rectangle([(30, y), (1050, y + 120)], fill=DARK_GRAY, outline=PURPLE, width=2)
    y += 15
    
    wuxing = [
        ("金", "3个", "辛、酉、酉", "强", GOLD),
        ("水", "3个", "癸、亥、子", "强", (100, 149, 237)),
        ("木", "1个", "甲", "弱", (34, 197, 94)),
        ("火", "0个", "无", "缺失", RED),
        ("土", "1个", "己", "弱", (168, 162, 158)),
    ]
    
    for i, (name, count, chars, status, color) in enumerate(wuxing):
        x = 60 + i * 200
        draw.text((x, y), f"{name}：{count}", fill=color, font=small_font)
        draw.text((x, y + 28), f"({chars})", fill=GRAY, font=tiny_font)
        draw.text((x, y + 52), status, fill=color, font=tiny_font)
    
    y += 90
    draw.text((540, y), "【特点】金水两旺，缺火，木土偏弱 | 喜火土，忌金水", fill=ORANGE, font=small_font, anchor="mm")
    y += 50
    
    # ===== 一生命运 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=NAVY)
    draw.text((540, y + 22), "🎯 一生命运详解", fill=GOLD, font=main_font, anchor="mm")
    y += 60
    
    # 性格
    draw.rectangle([(30, y), (1050, y + 100)], fill=DARK_GRAY, outline=PINK, width=1)
    y += 10
    draw.text((50, y), "【性格】聪明伶俐，心思细腻，口才好，有艺术天赋", fill=WHITE, font=small_font)
    y += 28
    draw.text((50, y), "        温柔善解人意，但想得多易焦虑，优柔寡断", fill=GRAY, font=tiny_font)
    y += 28
    draw.text((50, y), "【事业】适合教育、设计、医疗、行政行业 | 不适合高风险投资", fill=WHITE, font=small_font)
    y += 28
    draw.text((50, y), "【财运】正财旺偏财一般 | 宜稳健理财，不宜投机", fill=WHITE, font=small_font)
    y += 50
    
    # 婚姻健康
    draw.rectangle([(30, y), (1050, y + 80)], fill=DARK_GRAY, outline=PINK, width=1)
    y += 10
    draw.text((50, y), "【婚姻】配偶能力强，晚婚为宜（28岁后），婚后生活富足", fill=WHITE, font=small_font)
    y += 28
    draw.text((50, y), "        最佳婚配：蛇、牛、龙 | 避免早婚", fill=GRAY, font=tiny_font)
    y += 28
    draw.text((50, y), "【健康】注意妇科、肠胃、呼吸系统 | 多吃温热食物", fill=WHITE, font=small_font)
    y += 60
    
    # ===== 2026年流年运势 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=NAVY)
    draw.text((540, y + 22), "📅 2026年（丙午年）流年运势", fill=GOLD, font=main_font, anchor="mm")
    y += 60
    
    draw.rectangle([(30, y), (1050, y + 60)], fill=(30, 80, 50), outline=GOLD, width=2)
    y += 15
    draw.text((540, y), "✅ 丙午火马年 - 火旺助身，整体大吉！", fill=GOLD, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "运势：★★★★★ 大吉 | 四月、五月最佳", fill=WHITE, font=small_font, anchor="mm")
    y += 70
    
    # ===== 各月运势 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=NAVY)
    draw.text((540, y + 22), "📆 各月运势详解", fill=GOLD, font=main_font, anchor="mm")
    y += 60
    
    months = [
        ("正月", "庚寅", "2.4-3.5", "★★★★☆", "吉", WHITE, "事业顺利，贵人相助"),
        ("二月", "辛卯", "3.6-4.4", "★★★☆☆", "平", ORANGE, "⚠️ 金木相冲，情绪波动"),
        ("三月", "壬辰", "4.5-5.5", "★★★★☆", "吉", WHITE, "事业转机，财运回升"),
        ("四月", "癸巳", "5.6-6.5", "★★★★★", "大吉", GOLD, "🔥 全年最佳！把握机遇"),
        ("五月", "甲午", "6.6-7.6", "★★★★★", "大吉", GOLD, "🔥 事业财运双丰收"),
        ("六月", "乙未", "7.7-8.7", "★★★★☆", "吉", WHITE, "事业稳定，家庭和睦"),
        ("七月", "丙申", "8.8-9.7", "★★★☆☆", "平", ORANGE, "⚠️ 火金相克，防小人"),
        ("八月", "丁酉", "9.8-10.7", "★★☆☆☆", "凶", RED, "❌ 全年最差！详细见下"),
        ("九月", "戊戌", "10.8-11.7", "★★★☆☆", "平", WHITE, "土来助身，运势回升"),
        ("十月", "己亥", "11.8-12.6", "★★★★☆", "吉", WHITE, "贵人相助，感情和谐"),
        ("十一月", "庚子", "12.7-1.5", "★★★☆☆", "平", ORANGE, "⚠️ 水旺克火，注意健康"),
        ("十二月", "辛丑", "1.6-2.3", "★★★★☆", "吉", WHITE, "年终有收获，财运佳"),
    ]
    
    box_h = 45
    for month, gz, date, rating, status, color, desc in months:
        bg = DARK_GRAY if months.index((month, gz, date, rating, status, color, desc)) % 2 == 0 else (40, 55, 75)
        draw.rectangle([(30, y), (1050, y + box_h - 3)], fill=bg, outline=color, width=1)
        
        draw.text((45, y + 12), month, fill=color, font=small_font)
        draw.text((120, y + 12), gz, fill=WHITE, font=tiny_font)
        draw.text((220, y + 12), date, fill=GRAY, font=tiny_font)
        draw.text((380, y + 12), rating, fill=color, font=tiny_font)
        draw.text((520, y + 12), status, fill=color, font=tiny_font)
        draw.text((620, y + 12), desc, fill=GRAY, font=tiny_font)
        
        y += box_h
    
    y += 15
    
    # ===== 八月重点警告 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=(80, 20, 20))
    draw.text((540, y + 22), "⚠️ 八月（丁酉月 9.8-10.7）重点警告", fill=RED, font=main_font, anchor="mm")
    y += 60
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=RED, width=3)
    y += 15
    
    warnings = [
        "❌ 全年最差月份！金旺泄身，运势低迷",
        "",
        "【事业】工作不顺，易有挫折，宜低调行事",
        "【财运】破财之象，不宜投资，避免借贷",
        "【健康】注意妇科、肠胃问题，宜多休息",
        "【感情】易有矛盾争吵，宜多沟通忍让",
        "",
        "【化解方法】",
        "1. 多穿红色、紫色、橙色衣服",
        "2. 佩戴红玛瑙、琥珀饰品",
        "3. 多晒太阳，补充阳气",
        "4. 不宜做重大决定",
    ]
    
    for warning in warnings:
        if warning:
            color = RED if warning.startswith("❌") or warning.startswith("【") else WHITE
            draw.text((50, y), warning, fill=color, font=small_font)
        y += 24
    
    y += 30
    
    # ===== 开运建议 =====
    draw.rectangle([(30, y), (1050, y + 45)], fill=NAVY)
    draw.text((540, y + 22), "💡 开运建议", fill=GOLD, font=main_font, anchor="mm")
    y += 60
    
    draw.rectangle([(30, y), (1050, y + 180)], fill=DARK_GRAY, outline=PURPLE, width=2)
    y += 15
    
    tips = [
        ("✅ 幸运颜色", "红色、紫色、橙色、粉色"),
        ("✅ 幸运数字", "3、4、9"),
        ("✅ 幸运方位", "南方、东南方"),
        ("✅ 生肖贵人", "蛇、牛、龙"),
        ("✅ 佩戴饰品", "红玛瑙、琥珀、紫水晶"),
        ("❌ 忌讳颜色", "黑色、蓝色、白色"),
        ("❌ 忌讳数字", "1、6"),
        ("❌ 忌讳方位", "北方、西方"),
    ]
    
    for i, (title, content) in enumerate(tips):
        x = 60 if i % 2 == 0 else 550
        row = i // 2
        color = GOLD if title.startswith("✅") else RED
        draw.text((x, y + row * 35), f"{title}：{content}", fill=color, font=small_font)
    
    y += 200
    
    # ===== 总评 =====
    draw.rectangle([(30, y), (1050, y + 140)], fill=NAVY, outline=GOLD, width=3)
    y += 15
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    y += 45
    draw.text((540, y), "八字偏弱喜火土，2026年火旺助身大吉！", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "四月五月最佳，八月需特别注意化解", fill=WHITE, font=small_font, anchor="mm")
    y += 30
    draw.text((540, y), "45岁后火运到来，事业财运大旺，晚年享福！", fill=WHITE, font=small_font, anchor="mm")
    
    # ===== 底部 =====
    y = 3150
    draw.text((540, y), "一生运势：早年平稳，中年渐入佳境，晚年享福！", fill=GOLD, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "生辰八字命盘_李永丹女士.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 八字命盘图片已保存: {output_path}")
    print(f"   尺寸: {img.size}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_bazi_chart()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生辰八字详细命盘图片生成器 - 唐晓兰女士
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
GREEN = (34, 197, 94)
GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)

def create_bazi_chart():
    """生成详细八字命盘图片"""
    
    # 创建画布 (1080x3800)
    img = Image.new('RGB', (1080, 3800), DEEP_BLUE)
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = ImageFont.truetype(FONT_BOLD, 44)
    main_font = ImageFont.truetype(FONT_BOLD, 32)
    sub_font = ImageFont.truetype(FONT_PATH, 26)
    small_font = ImageFont.truetype(FONT_PATH, 22)
    tiny_font = ImageFont.truetype(FONT_PATH, 18)
    
    y = 0
    
    # ===== 顶部标题 =====
    draw.rectangle([(0, 0), (1080, 90)], fill=NAVY)
    draw.text((540, 45), "🔮 生辰八字详细算命 - 唐晓兰女士", fill=GOLD, font=title_font, anchor="mm")
    y = 110
    
    # ===== 出生信息 =====
    draw.rectangle([(30, y), (1050, y + 100)], fill=DARK_GRAY, outline=ORANGE, width=2)
    y += 12
    draw.text((540, y), "📅 公历1986年4月15日17:30 | 农历丙寅年三月初七日酉时", fill=WHITE, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "八字：丙寅 壬辰 戊申 辛酉 | 五行：金旺，木火弱", fill=ORANGE, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "喜火土，忌金水 | 生肖：虎", fill=GRAY, font=small_font, anchor="mm")
    y += 70
    
    # ===== 一、婚姻感情 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "💕 一、婚姻感情", fill=ORANGE, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=ORANGE, width=1)
    y += 12
    
    marriage = [
        "【婚姻状况】",
        "✅ 已婚（约2012-2015年结婚）",
        "",
        "【配偶特征】",
        "✅ 配偶能力强，有领导才能，事业有成",
        "✅ 配偶性格稳重，有担当，家庭条件好",
        "",
        "【婚姻质量】★★★★★",
        "✅ 夫妻感情稳定，互相支持，家庭富足",
        "⚠️ 2026年八月、十一月：感情易有矛盾，多沟通",
    ]
    
    for line in marriage:
        if line:
            color = ORANGE if line.startswith("【") else (WHITE if line.startswith("✅") else RED)
            draw.text((50, y), line, fill=color, font=small_font)
        y += 20
    
    y += 20
    
    # ===== 二、事业工作 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "💼 二、事业工作", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 240)], fill=DARK_GRAY, outline=GOLD, width=1)
    y += 12
    
    career = [
        "【适合行业】",
        "1. 管理、领导岗位 ★★★★★ - 企业管理、部门主管",
        "2. 教育、培训行业 ★★★★★ - 教师、培训师、教育管理",
        "3. 销售、传媒行业 ★★★★☆ - 销售、公关、传媒、广告",
        "4. 医疗、健康行业 ★★★★☆ - 医疗管理、健康管理",
        "",
        "【事业走势】",
        "2026年事业大旺 | 2029-2030年事业高峰",
        "2036年（50岁）火运到来，事业财运大旺",
        "",
        "【工作建议】宜积极进取，创业经商，提升管理能力",
    ]
    
    for line in career:
        if line:
            color = GOLD if line.startswith("【") else WHITE
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 20
    
    # ===== 三、财运投资 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "💰 三、财运投资", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=GOLD, width=1)
    y += 12
    
    wealth = [
        "【财运特点】",
        "✅ 正财运：★★★★★ 收入丰厚，事业有成",
        "✅ 偏财运：★★★★☆ 偏财旺，有投资眼光",
        "",
        "【理财建议】",
        "✅ 适合：创业投资、房产、股票基金、合伙经营",
        "⚠️ 谨慎：高风险投机、民间借贷",
        "",
        "【预计收入】",
        "40岁年收入20-40万 | 45岁年收入40-80万",
        "50岁后年收入80-150万+",
    ]
    
    for line in wealth:
        if line:
            color = GOLD if line.startswith("【") else (WHITE if line.startswith("✅") else (ORANGE if "万" in line else GRAY))
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 20
    
    # ===== 四、健康养生 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "🏥 四、健康养生", fill=RED, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=RED, width=1)
    y += 12
    
    health = [
        "【需特别注意的健康问题】",
        "",
        "⚠️ 心血管系统（火弱）- 重点注意！",
        "   心脏、血压问题 | 建议：定期检查，注意休息",
        "",
        "⚠️ 皮肤问题（金旺）",
        "   皮肤过敏、皮炎 | 建议：注意护肤，避免过敏源",
        "",
        "⚠️ 呼吸系统、肝胆问题",
        "   容易感冒咳嗽 | 肝胆功能 | 少喝酒，注意饮食",
    ]
    
    for line in health:
        if line:
            color = RED if line.startswith("⚠️") or line.startswith("【") else WHITE
            draw.text((50, y), line, fill=color, font=small_font)
        y += 20
    
    y += 20
    
    # ===== 五、子女运 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "👶 五、子女运", fill=GREEN, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 120)], fill=DARK_GRAY, outline=GREEN, width=1)
    y += 12
    
    children = [
        "【子女运特点】★★★★★",
        "✅ 有1-2个孩子，子女聪明有出息",
        "✅ 子女性格：聪明活泼，口才好，成绩优秀",
        "✅ 子女孝顺，晚年享福",
        "✅ 教育方式：宜培养领导能力，多鼓励少批评",
    ]
    
    for line in children:
        if line:
            color = GREEN if line.startswith("【") or line.startswith("✅") else WHITE
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 20
    
    # ===== 六、2026年具体预测 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "📅 六、2026年具体预测", fill=PURPLE, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=PURPLE, width=1)
    y += 12
    
    prediction = [
        "【2026年总运势】丙午火马年 - 大吉！★★★★★",
        "",
        "【感情】四月五月感情甜蜜 | 八月十一月需多沟通",
        "【事业】四月五月事业最佳，有升职机会",
        "【财运】四月五月财运最佳，有意外之财",
        "【健康】二月、八月、十一月需注意",
        "",
        "【具体事件预测】",
        "• 4-5月：事业突破，升职或加薪",
        "• 5-6月：有投资机会，收益可观",
        "• 9月：工作或家庭有小波折",
        "• 10月：贵人相助，事业顺利",
    ]
    
    for line in prediction:
        if line:
            color = PURPLE if line.startswith("【") else (WHITE if line.startswith("•") else GRAY)
            draw.text((50, y), line, fill=color, font=small_font)
        y += 20
    
    y += 20
    
    # ===== 七、人生重要节点 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "🎯 七、人生重要节点", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 180)], fill=DARK_GRAY, outline=GOLD, width=1)
    y += 12
    
    nodes = [
        "📅 2026年（40岁）：事业财运大旺年",
        "📅 2027-2028年（41-42岁）：事业稳定期",
        "📅 2029-2030年（43-44岁）：事业高峰期",
        "📅 2036年（50岁）：人生转折点，火运到来",
        "📅 2046年后（60岁+）：晚年享福，子女孝顺",
    ]
    
    for line in nodes:
        if line:
            draw.text((50, y), line, fill=WHITE, font=small_font)
        y += 28
    
    y += 20
    
    # ===== 总评 =====
    draw.rectangle([(30, y), (1050, y + 120)], fill=NAVY, outline=GOLD, width=3)
    y += 15
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    y += 40
    draw.text((540, y), "命格上佳，事业有成，财运旺盛，婚姻美满", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 30
    draw.text((540, y), "50岁后事业财运大旺，晚年享福！", fill=WHITE, font=sub_font, anchor="mm")
    
    # ===== 底部 =====
    y = 3750
    draw.text((540, y), "八字偏弱喜火土 | 四月五月最佳 | 八月需注意", fill=GOLD, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "生辰八字详细算命_唐晓兰女士.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 详细八字命盘图片已保存: {output_path}")
    print(f"   尺寸: {img.size}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_bazi_chart()

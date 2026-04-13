#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生辰八字详细命盘图片生成器 - 李永丹女士
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
GREEN = (34, 197, 94)
GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)

def create_bazi_chart():
    """生成详细八字命盘图片"""
    
    # 创建画布 (1080x4000) - 超长版
    img = Image.new('RGB', (1080, 4000), DEEP_BLUE)
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
    draw.text((540, 45), "🔮 生辰八字详细算命 - 李永丹女士", fill=GOLD, font=title_font, anchor="mm")
    y = 110
    
    # ===== 出生信息 =====
    draw.rectangle([(30, y), (1050, y + 100)], fill=DARK_GRAY, outline=PINK, width=2)
    y += 12
    draw.text((540, y), "📅 农历癸酉年八月十三日子时 | 公历1993年9月28日", fill=WHITE, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "八字：癸酉 辛酉 己亥 甲子 | 五行：金水旺，缺火", fill=ORANGE, font=sub_font, anchor="mm")
    y += 35
    draw.text((540, y), "喜火土，忌金水 | 生肖：鸡", fill=GRAY, font=small_font, anchor="mm")
    y += 70
    
    # ===== 一、婚姻感情 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "💕 一、婚姻感情", fill=PINK, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 280)], fill=DARK_GRAY, outline=PINK, width=1)
    y += 12
    
    marriage = [
        "【正缘何时出现】",
        "✅ 2026年感情运大旺，最佳月份：四月、五月、十月",
        "✅ 正缘特征：年龄大3-8岁，成熟稳重，事业有成",
        "✅ 相识方式：朋友介绍、工作场合",
        "✅ 对方职业：教育、医疗、公务员、企业管理",
        "",
        "【婚姻时间】",
        "✅ 2026年有望脱单，2027年适合结婚",
        "✅ 不宜早婚（26岁前婚姻不稳）",
        "",
        "【配偶特征】",
        "✅ 生肖：蛇、牛、龙最佳 | 性格：稳重有担当",
        "⚠️ 避免：兔、狗生肖 | 花心、不稳重、年龄太小",
    ]
    
    for line in marriage:
        if line:
            color = PINK if line.startswith("【") else (WHITE if line.startswith("✅") else ORANGE)
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 25
    
    # ===== 二、事业工作 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "💼 二、事业工作", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 260)], fill=DARK_GRAY, outline=GOLD, width=1)
    y += 12
    
    career = [
        "【适合行业】★★★★★",
        "1. 教育、培训、文化行业 - 教师、培训师、教育管理",
        "2. 医疗、护理、健康行业 - 护士、健康管理、医疗行政",
        "3. 设计、艺术、创意行业 - 平面设计、UI设计、室内设计",
        "4. 行政、文职、管理工作 - 行政助理、人事管理",
        "",
        "【不适合行业】",
        "❌ 高风险投资、金融投机 | 销售业绩压力大的工作",
        "❌ 需要魄力决策的创业 | 竞争激烈、淘汰率高的行业",
        "",
        "【事业走势】",
        "2026年事业上升 | 2027-2028年稳定发展",
        "2038年（45岁）火运到来，事业财运大旺",
    ]
    
    for line in career:
        if line:
            color = GOLD if line.startswith("【") else (WHITE if "★" in line or line.startswith("1") or line.startswith("2") or line.startswith("3") or line.startswith("4") else (RED if line.startswith("❌") else GRAY))
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 25
    
    # ===== 三、财运投资 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "💰 三、财运投资", fill=GOLD, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 240)], fill=DARK_GRAY, outline=GOLD, width=1)
    y += 12
    
    wealth = [
        "【财运特点】",
        "✅ 正财运：★★★★☆ 收入稳定，逐年增长，中年后可观",
        "⚠️ 偏财运：★★☆☆☆ 偏财一般，不宜投机，容易亏损",
        "",
        "【理财建议】",
        "✅ 适合：定期存款、银行理财、基金定投、房产（2028年后）",
        "❌ 不适合：股票、期货、P2P、虚拟货币、民间借贷",
        "",
        "【预计收入】",
        "30岁月入5000-8000 | 35岁月入8000-15000",
        "40岁月入15000-30000 | 45岁后年收入30-50万+",
    ]
    
    for line in wealth:
        if line:
            color = GOLD if line.startswith("【") else (WHITE if line.startswith("✅") else (RED if line.startswith("❌") else (ORANGE if "月入" in line or "收入" in line else GRAY)))
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 25
    
    # ===== 四、健康养生 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "🏥 四、健康养生", fill=RED, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 260)], fill=DARK_GRAY, outline=RED, width=1)
    y += 12
    
    health = [
        "【需特别注意的健康问题】",
        "",
        "⚠️ 妇科问题（缺火，寒气重）- 重点注意！",
        "   痛经、月经不调、宫寒、手脚冰凉、备孕需调理",
        "   建议：多吃温热食物，艾灸、泡脚、保暖",
        "",
        "⚠️ 肠胃消化系统",
        "   胃寒、消化不良、容易腹泻",
        "   建议：规律饮食，少吃生冷",
        "",
        "⚠️ 呼吸系统（金旺克木）",
        "   容易感冒、咳嗽、过敏性鼻炎",
        "",
        "【养生建议】",
        "多吃：红枣、桂圆、羊肉、牛肉、生姜",
        "少吃：冷饮、生鱼片、寒凉水果",
    ]
    
    for line in health:
        if line:
            color = RED if line.startswith("⚠️") or line.startswith("【") else (ORANGE if "建议" in line else WHITE)
            draw.text((50, y), line, fill=color, font=small_font)
        y += 20
    
    y += 25
    
    # ===== 五、子女运 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "👶 五、子女运", fill=GREEN, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 140)], fill=DARK_GRAY, outline=GREEN, width=1)
    y += 12
    
    children = [
        "【子女运特点】★★★★☆",
        "✅ 有1-2个孩子，子女聪明懂事，亲子关系融洽",
        "✅ 最佳生育年份：2028年、2029年、2031年",
        "✅ 头胎男孩可能性大，二胎女孩可能性大",
        "✅ 子女孝顺，晚年享福",
    ]
    
    for line in children:
        if line:
            color = GREEN if line.startswith("【") or line.startswith("✅") else WHITE
            draw.text((50, y), line, fill=color, font=small_font)
        y += 24
    
    y += 25
    
    # ===== 六、2026年具体预测 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "📅 六、2026年具体预测", fill=ORANGE, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=ORANGE, width=1)
    y += 12
    
    prediction = [
        "【感情】四月、五月正缘出现，感情甜蜜 | 十月谈婚论嫁",
        "【事业】四月、五月事业最佳，有升职加薪机会",
        "【财运】四月、五月财运最佳，有意外之财",
        "【健康】二月、八月、十一月需注意健康",
        "",
        "【具体事件预测】",
        "• 4-5月：遇到正缘，开始恋爱",
        "• 5-6月：工作有变动或升职机会",
        "• 9月：感情或工作有小波折（八月凶月影响）",
        "• 11月：感情稳定，有望订婚",
        "• 年底：有意外收入或奖金",
    ]
    
    for line in prediction:
        if line:
            color = ORANGE if line.startswith("【") else (WHITE if line.startswith("•") else GRAY)
            draw.text((50, y), line, fill=color, font=small_font)
        y += 20
    
    y += 25
    
    # ===== 七、人生重要节点 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=NAVY)
    draw.text((540, y + 20), "🎯 七、人生重要节点", fill=PURPLE, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 200)], fill=DARK_GRAY, outline=PURPLE, width=1)
    y += 12
    
    nodes = [
        "📅 2026年（33岁）：感情突破年，遇到正缘，有望脱单",
        "📅 2027年（34岁）：婚姻年，适合结婚，婚姻美满",
        "📅 2028-2029年（35-36岁）：生育年，适合生育，家庭幸福",
        "📅 2030-2035年（37-42岁）：事业上升期，收入逐年增长",
        "📅 2038年（45岁）：人生转折点，火运到来，事业财运大旺",
        "📅 2048年后（55岁+）：晚年享福，子女孝顺，生活富足",
    ]
    
    for line in nodes:
        if line:
            draw.text((50, y), line, fill=WHITE, font=small_font)
        y += 28
    
    y += 25
    
    # ===== 八月重点警告 =====
    draw.rectangle([(30, y), (1050, y + 40)], fill=(80, 20, 20))
    draw.text((540, y + 20), "⚠️ 八月（9.8-10.7）重点警告", fill=RED, font=main_font, anchor="mm")
    y += 55
    
    draw.rectangle([(30, y), (1050, y + 180)], fill=DARK_GRAY, outline=RED, width=3)
    y += 12
    
    warnings = [
        "❌ 全年最差月份！金旺泄身，运势低迷",
        "",
        "【事业】工作不顺，易有挫折，宜低调行事",
        "【财运】破财之象，不宜投资，避免借贷",
        "【健康】注意妇科、肠胃问题，宜多休息",
        "【感情】易有矛盾争吵，宜多沟通忍让",
        "",
        "【化解】多穿红色紫色 | 佩戴红玛瑙 | 多晒太阳",
    ]
    
    for line in warnings:
        if line:
            color = RED if line.startswith("❌") or line.startswith("【") else WHITE
            draw.text((50, y), line, fill=color, font=small_font)
        y += 22
    
    y += 25
    
    # ===== 总评 =====
    draw.rectangle([(30, y), (1050, y + 120)], fill=NAVY, outline=GOLD, width=3)
    y += 15
    draw.text((540, y), "🌟 命格总评", fill=GOLD, font=main_font, anchor="mm")
    y += 40
    draw.text((540, y), "2026年遇到正缘，2027年结婚", fill=LIGHT_GOLD, font=sub_font, anchor="mm")
    y += 30
    draw.text((540, y), "45岁后事业财运大旺，一生平稳幸福，晚年享福！", fill=WHITE, font=sub_font, anchor="mm")
    
    # ===== 底部 =====
    y = 3950
    draw.text((540, y), "八字偏弱喜火土 | 四月五月最佳 | 八月需化解", fill=GOLD, font=sub_font, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "生辰八字详细算命_李永丹女士.jpg")
    img.save(output_path, quality=95)
    print(f"✅ 详细八字命盘图片已保存: {output_path}")
    print(f"   尺寸: {img.size}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_bazi_chart()

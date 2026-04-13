#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂早安汇报内容生成器
生成日期：2026-04-13
包含：宣传图、视频、简报、紫微斗数运势
"""

import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import json

# ==================== 配置 ====================
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/memory/shiyuantang_marketing/宣传图/2026-04-13")
PHOTO_DIR = os.path.expanduser("~/.openclaw/workspace/memory/shiyuantang_photos_new")
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
FONT_MEDIUM = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"

# 颜色配置
COLORS = {
    "bg_dark": (15, 23, 42),        # #0F172A 深蓝背景
    "white": (255, 255, 255),       # #FFFFFF 白色文字
    "gold": (251, 191, 36),         # #FBBF24 金色
    "dark_gray": (30, 41, 59),      # #1E293B 深灰背景条
    "blue_border": (59, 130, 246),  # #3B82F6 蓝色边框
    "title_bg": (30, 58, 138),      # #1E3A8A 标题背景蓝
}

# ==================== 紫微斗数运势 ====================
def get_ziwei_fortune():
    """生成紫微斗数运势（基于农历1981年2月19日戌时）"""
    fortune = {
        "日期": "2026年4月13日 星期一",
        "农历": "丙午年二月廿六",
        "整体运势": "⭐⭐⭐⭐",
        "财运": "⭐⭐⭐⭐⭐",
        "事业": "⭐⭐⭐⭐",
        "健康": "⭐⭐⭐",
        "贵人方位": "东南方",
        "幸运颜色": "金色、蓝色",
        "幸运数字": "6、8",
        "宜": "签约、投资、会友、开业",
        "忌": "动土、远行",
        "今日提示": "今日紫微星入命宫，贵人运旺盛，适合处理重要事务。财运亨通，可把握投资机会。注意休息，避免过度劳累。",
        "事业运": "今日事业运势良好，适合推进重要项目。与合作伙伴沟通顺畅，有望达成共识。下午时段思维敏捷，适合决策。",
        "财运": "财星高照，正财偏财皆旺。适合处理财务相关事务，投资理财可获收益。但需谨慎评估风险，不可贪心。",
        "健康运": "注意用眼卫生，避免长时间看手机电脑。适当运动，保持良好作息。饮食宜清淡，多喝水。"
    }
    return fortune

# ==================== 眼睛防治简报 ====================
def get_eye_health_brief():
    """生成眼睛防治简报"""
    brief = {
        "日期": "2026年4月13日",
        "主题": "春季护眼正当时",
        "要点": [
            "🌸 春季花粉过敏高发，外出建议佩戴护目镜",
            "📱 电子屏幕使用每40分钟休息10分钟",
            "🥕 多食用富含维生素A的食物（胡萝卜、菠菜、蛋黄）",
            "💧 保持室内湿度40%-60%，避免眼睛干涩",
            "👀 儿童青少年每天户外活动2小时，有效预防近视",
            "👓 定期验光检查，成年人每年至少1次",
            "🧘 眼保健操每天2次，缓解视疲劳"
        ],
        "今日提醒": "春季是近视发展的高峰期，家长应关注孩子用眼习惯，定期进行视力检查。",
        "视元堂服务": "专业验光配镜 | 儿童近视防控 | 视力训练矫正"
    }
    return brief

# ==================== 生成宣传图 ====================
def create_promo_image(title, subtitle, tags, points, photo_path, output_name):
    """生成宣传图"""
    # 创建画布 (1080x1920)
    img = Image.new('RGB', (1080, 1920), COLORS["bg_dark"])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 64)
        font_subtitle = ImageFont.truetype(FONT_BOLD, 42)
        font_tag = ImageFont.truetype(FONT_MEDIUM, 28)
        font_point = ImageFont.truetype(FONT_MEDIUM, 32)
        font_info = ImageFont.truetype(FONT_MEDIUM, 26)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_point = ImageFont.load_default()
        font_info = ImageFont.load_default()
    
    # 加载并处理照片
    if os.path.exists(photo_path):
        photo = Image.open(photo_path)
        # 调整照片大小，保持比例
        photo_width = 1000
        photo_height = int(photo.height * (photo_width / photo.width))
        if photo_height > 600:
            photo_height = 600
        photo = photo.resize((photo_width, photo_height), Image.LANCZOS)
        
        # 创建圆角蒙版
        mask = Image.new('L', (photo_width, photo_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (photo_width, photo_height)], radius=30, fill=255)
        
        # 应用圆角
        photo.putalpha(mask)
        
        # 粘贴照片
        photo_x = (1080 - photo_width) // 2
        photo_y = 30
        img.paste(photo, (photo_x, photo_y), photo)
        
        current_y = photo_y + photo_height + 30
    else:
        current_y = 100
    
    # 绘制标题背景条
    title_bg_height = 180
    draw.rounded_rectangle(
        [(40, current_y), (1040, current_y + title_bg_height)],
        radius=20,
        fill=COLORS["title_bg"]
    )
    
    # 绘制主标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        ((1080 - title_width) // 2, current_y + 20),
        title,
        fill=COLORS["white"],
        font=font_title
    )
    
    # 绘制副标题
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(
        ((1080 - subtitle_width) // 2, current_y + 90),
        subtitle,
        fill=COLORS["gold"],
        font=font_subtitle
    )
    
    # 绘制标签
    tag_y = current_y + 145
    tag_x = 60
    for tag in tags:
        tag_bbox = draw.textbbox((0, 0), tag, font=font_tag)
        tag_width = tag_bbox[2] - tag_bbox[0] + 40
        tag_height = tag_bbox[3] - tag_bbox[1] + 20
        
        # 绘制标签背景（黄色椭圆）
        draw.ellipse(
            [(tag_x, tag_y), (tag_x + tag_width, tag_y + tag_height)],
            fill=COLORS["gold"]
        )
        
        # 绘制标签文字
        draw.text(
            (tag_x + 20, tag_y + 5),
            tag,
            fill=COLORS["bg_dark"],
            font=font_tag
        )
        
        tag_x += tag_width + 20
    
    current_y += title_bg_height + 30
    
    # 绘制说明文字背景条
    points_bg_height = len(points) * 50 + 40
    draw.rounded_rectangle(
        [(40, current_y), (1040, current_y + points_bg_height)],
        radius=20,
        fill=COLORS["dark_gray"]
    )
    
    # 绘制说明文字
    point_y = current_y + 20
    for point in points:
        draw.text(
            (60, point_y),
            f"✓ {point}",
            fill=COLORS["white"],
            font=font_point
        )
        point_y += 50
    
    current_y += points_bg_height + 30
    
    # 绘制联系信息框
    info_box_height = 180
    draw.rounded_rectangle(
        [(40, current_y), (1040, current_y + info_box_height)],
        radius=20,
        outline=COLORS["blue_border"],
        width=3
    )
    
    # 绘制联系信息
    info_lines = [
        "【视元堂眼视光中心】",
        "📍 南充顺庆区白土坝路406号",
        "📞 0817-2255222 / 19138766190",
        "🕐 周一至周日 9:00-21:00"
    ]
    
    info_y = current_y + 20
    for line in info_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_info)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text(
            ((1080 - line_width) // 2, info_y),
            line,
            fill=COLORS["white"],
            font=font_info
        )
        info_y += 40
    
    # 保存图片
    output_path = os.path.join(OUTPUT_DIR, output_name)
    img.save(output_path, quality=95)
    print(f"✅ 宣传图已生成: {output_path}")
    return output_path

# ==================== 生成运势图 ====================
def create_fortune_image(fortune):
    """生成紫微斗数运势图"""
    # 创建画布 (1080x1920)
    img = Image.new('RGB', (1080, 1920), COLORS["bg_dark"])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 56)
        font_subtitle = ImageFont.truetype(FONT_BOLD, 36)
        font_content = ImageFont.truetype(FONT_MEDIUM, 30)
        font_small = ImageFont.truetype(FONT_MEDIUM, 26)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_content = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    title = "紫微斗数每日运势"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        ((1080 - title_width) // 2, 40),
        title,
        fill=COLORS["gold"],
        font=font_title
    )
    
    # 绘制日期
    date_text = f"{fortune['日期']} | {fortune['农历']}"
    date_bbox = draw.textbbox((0, 0), date_text, font=font_subtitle)
    date_width = date_bbox[2] - date_bbox[0]
    draw.text(
        ((1080 - date_width) // 2, 110),
        date_text,
        fill=COLORS["white"],
        font=font_subtitle
    )
    
    # 绘制运势卡片
    current_y = 180
    cards = [
        ("整体运势", fortune["整体运势"]),
        ("财运", fortune["财运"]),
        ("事业", fortune["事业"]),
        ("健康", fortune["健康"]),
    ]
    
    for label, value in cards:
        # 卡片背景
        draw.rounded_rectangle(
            [(60, current_y), (1020, current_y + 80)],
            radius=15,
            fill=COLORS["dark_gray"]
        )
        
        # 标签
        draw.text((80, current_y + 25), label, fill=COLORS["white"], font=font_content)
        
        # 值
        value_bbox = draw.textbbox((0, 0), value, font=font_content)
        value_width = value_bbox[2] - value_bbox[0]
        draw.text(
            (1000 - value_width - 20, current_y + 25),
            value,
            fill=COLORS["gold"],
            font=font_content
        )
        
        current_y += 100
    
    # 绘制宜忌
    current_y += 20
    draw.rounded_rectangle(
        [(60, current_y), (1020, current_y + 160)],
        radius=15,
        fill=COLORS["dark_gray"]
    )
    
    draw.text((80, current_y + 20), f"✅ 宜：{fortune['宜']}", fill=COLORS["white"], font=font_small)
    draw.text((80, current_y + 60), f"❌ 忌：{fortune['忌']}", fill=COLORS["white"], font=font_small)
    draw.text((80, current_y + 100), f"🧭 贵人方位：{fortune['贵人方位']}", fill=COLORS["white"], font=font_small)
    draw.text((80, current_y + 140), f"🎨 幸运颜色：{fortune['幸运颜色']}", fill=COLORS["white"], font=font_small)
    
    current_y += 180
    
    # 绘制今日提示
    draw.rounded_rectangle(
        [(60, current_y), (1020, current_y + 200)],
        radius=15,
        fill=COLORS["title_bg"]
    )
    
    draw.text((80, current_y + 20), "💡 今日提示", fill=COLORS["gold"], font=font_subtitle)
    
    # 自动换行
    tip = fortune["今日提示"]
    lines = []
    line = ""
    for char in tip:
        line += char
        if len(line) > 24:
            lines.append(line)
            line = ""
    if line:
        lines.append(line)
    
    tip_y = current_y + 70
    for line in lines:
        draw.text((80, tip_y), line, fill=COLORS["white"], font=font_small)
        tip_y += 35
    
    current_y += 220
    
    # 绘制详细运势
    details = [
        ("💼 事业运", fortune["事业运"]),
        ("💰 财运", fortune["财运"]),
        ("❤️ 健康运", fortune["健康运"]),
    ]
    
    for label, content in details:
        draw.rounded_rectangle(
            [(60, current_y), (1020, current_y + 150)],
            radius=15,
            fill=COLORS["dark_gray"]
        )
        
        draw.text((80, current_y + 15), label, fill=COLORS["gold"], font=font_subtitle)
        
        # 自动换行
        lines = []
        line = ""
        for char in content:
            line += char
            if len(line) > 26:
                lines.append(line)
                line = ""
        if line:
            lines.append(line)
        
        content_y = current_y + 55
        for line in lines[:3]:  # 最多3行
            draw.text((80, content_y), line, fill=COLORS["white"], font=font_small)
            content_y += 30
        
        current_y += 165
    
    # 保存图片
    output_path = os.path.join(OUTPUT_DIR, "紫微斗数运势.png")
    img.save(output_path, quality=95)
    print(f"✅ 运势图已生成: {output_path}")
    return output_path

# ==================== 生成简报图 ====================
def create_brief_image(brief):
    """生成眼睛防治简报图"""
    # 创建画布 (1080x1920)
    img = Image.new('RGB', (1080, 1920), COLORS["bg_dark"])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 56)
        font_subtitle = ImageFont.truetype(FONT_BOLD, 36)
        font_content = ImageFont.truetype(FONT_MEDIUM, 30)
        font_small = ImageFont.truetype(FONT_MEDIUM, 26)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_content = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    title = "👁️ 眼睛防治简报"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        ((1080 - title_width) // 2, 40),
        title,
        fill=COLORS["gold"],
        font=font_title
    )
    
    # 绘制日期和主题
    date_text = f"{brief['日期']} | {brief['主题']}"
    date_bbox = draw.textbbox((0, 0), date_text, font=font_subtitle)
    date_width = date_bbox[2] - date_bbox[0]
    draw.text(
        ((1080 - date_width) // 2, 110),
        date_text,
        fill=COLORS["white"],
        font=font_subtitle
    )
    
    # 绘制要点
    current_y = 180
    for point in brief["要点"]:
        # 要点背景
        draw.rounded_rectangle(
            [(60, current_y), (1020, current_y + 70)],
            radius=15,
            fill=COLORS["dark_gray"]
        )
        
        draw.text((80, current_y + 20), point, fill=COLORS["white"], font=font_small)
        current_y += 85
    
    # 绘制今日提醒
    current_y += 20
    draw.rounded_rectangle(
        [(60, current_y), (1020, current_y + 150)],
        radius=15,
        fill=COLORS["title_bg"]
    )
    
    draw.text((80, current_y + 20), "⚠️ 今日提醒", fill=COLORS["gold"], font=font_subtitle)
    
    # 自动换行
    reminder = brief["今日提醒"]
    lines = []
    line = ""
    for char in reminder:
        line += char
        if len(line) > 26:
            lines.append(line)
            line = ""
    if line:
        lines.append(line)
    
    reminder_y = current_y + 70
    for line in lines:
        draw.text((80, reminder_y), line, fill=COLORS["white"], font=font_small)
        reminder_y += 30
    
    current_y += 170
    
    # 绘制视元堂服务
    draw.rounded_rectangle(
        [(60, current_y), (1020, current_y + 120)],
        radius=15,
        outline=COLORS["blue_border"],
        width=3
    )
    
    draw.text((80, current_y + 20), "🏥 视元堂服务", fill=COLORS["gold"], font=font_subtitle)
    draw.text((80, current_y + 70), brief["视元堂服务"], fill=COLORS["white"], font=font_content)
    
    # 保存图片
    output_path = os.path.join(OUTPUT_DIR, "眼睛防治简报.png")
    img.save(output_path, quality=95)
    print(f"✅ 简报图已生成: {output_path}")
    return output_path

# ==================== 主函数 ====================
def main():
    """主函数"""
    print("=" * 60)
    print("🌅 视元堂早安汇报内容生成器")
    print("=" * 60)
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 生成紫微斗数运势
    print("\n📊 生成紫微斗数运势...")
    fortune = get_ziwei_fortune()
    fortune_path = create_fortune_image(fortune)
    
    # 2. 生成眼睛防治简报
    print("\n👁️ 生成眼睛防治简报...")
    brief = get_eye_health_brief()
    brief_path = create_brief_image(brief)
    
    # 3. 生成宣传图（使用店铺环境照片）
    print("\n🖼️ 生成宣传图...")
    
    # 宣传图1：店铺环境
    promo1_path = create_promo_image(
        title="视元堂眼视光中心",
        subtitle="专业验光配镜15年",
        tags=["南充配镜", "专业验光"],
        points=[
            "蔡司、依视路、豪雅品牌镜片",
            "全自动磨边机，0误差加工",
            "持证验光师，精准到1度",
            "儿童近视防控，科学训练"
        ],
        photo_path=os.path.join(PHOTO_DIR, "店铺环境_门头照片2.jpg"),
        output_name="宣传图_店铺环境.png"
    )
    
    # 宣传图2：验光设备
    promo2_path = create_promo_image(
        title="专业验光设备",
        subtitle="一台设备30万，只为测准你的度数",
        tags=["精准验光", "专业设备"],
        points=[
            "SUPER VISION RM-160验光仪",
            "持证验光师一对一服务",
            "精准到1度的专业验光",
            "儿童视力筛查，早发现早干预"
        ],
        photo_path=os.path.join(PHOTO_DIR, "验光设备_综合验光仪.jpg"),
        output_name="宣传图_验光设备.png"
    )
    
    # 宣传图3：配镜设备
    promo3_path = create_promo_image(
        title="全自动配镜设备",
        subtitle="从验光到磨边，一条龙专业配镜",
        tags=["0误差", "快速配镜"],
        points=[
            "ALE-903全自动磨边机",
            "JT-718镜片中心仪精准定位",
            "当天验光，当天取镜",
            "品牌镜片，品质保证"
        ],
        photo_path=os.path.join(PHOTO_DIR, "配镜设备_全自动磨边机ALE903.jpg"),
        output_name="宣传图_配镜设备.png"
    )
    
    # 4. 保存运势和简报数据
    print("\n💾 保存数据...")
    data = {
        "日期": "2026-04-13",
        "紫微斗数运势": fortune,
        "眼睛防治简报": brief,
        "生成的图片": [
            fortune_path,
            brief_path,
            promo1_path,
            promo2_path,
            promo3_path
        ]
    }
    
    data_path = os.path.join(OUTPUT_DIR, "早安汇报数据.json")
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 数据已保存: {data_path}")
    
    print("\n" + "=" * 60)
    print("✅ 早安汇报内容生成完成！")
    print("=" * 60)
    
    return data

if __name__ == "__main__":
    main()

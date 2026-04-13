#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂宣传图生成 - 严格按照老板确认的模板
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ============ 配置 ============
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
PHOTO_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_photos_new"
LOGO_PATH = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/brand/视元堂LOGO.jpg"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 颜色（严格按照模板）
DEEP_BLUE = (15, 23, 42)      # #0F172A 背景
WHITE = (255, 255, 255)        # 白色文字
GOLD = (251, 191, 36)          # #FBBF24 金色
DARK_GRAY = (30, 41, 59)       # #1E293B 深灰背景条
BLUE_BORDER = (59, 130, 246)   # #3B82F6 蓝色边框

# 内容（新话术，不重复）
CONTENT = {
    "photo": "训练设备_视力训练设备1.jpg",
    "main_title": "孩子近视不用慌",
    "sub_title": "科学训练有方法！",
    "tag": "儿童近视防控",
    "highlights": [
        "每天20分钟，视力训练看得见",
        "黑科技训练仪，近视防控新选择",
        "3个月提升2行，效果看得见"
    ],
    "output": "20260412_模板版_儿童近视防控.jpg"
}

def create_promo():
    """严格按照模板生成"""
    print("📸 按模板生成宣传图...")
    
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), DEEP_BLUE)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_main = ImageFont.truetype(FONT_BOLD, 64)
    font_sub = ImageFont.truetype(FONT_BOLD, 42)
    font_tag = ImageFont.truetype(FONT_PATH, 28)
    font_highlight = ImageFont.truetype(FONT_PATH, 32)
    font_info = ImageFont.truetype(FONT_PATH, 26)
    
    y = 0
    
    # ===== 1. LOGO 左上角 =====
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((100, 100), Image.LANCZOS)
        img.paste(logo, (30, 30))
    
    # ===== 2. 照片区域（上半部分）=====
    photo_path = os.path.join(PHOTO_DIR, CONTENT["photo"])
    if os.path.exists(photo_path):
        photo = Image.open(photo_path)
        
        # 照片占上半部分
        photo_height = 800
        ratio = photo_height / photo.height
        photo_width = int(photo.width * ratio)
        if photo_width > width:
            photo_width = width
            photo_height = int(photo.height * width / photo.width)
        photo = photo.resize((photo_width, photo_height), Image.LANCZOS)
        
        # 居中放置
        photo_x = (width - photo_width) // 2
        img.paste(photo, (photo_x, 150))
        y = 150 + photo_height + 30
    
    # ===== 3. 主标题区域（蓝色背景条）=====
    title_height = 180
    draw.rectangle([(0, y), (width, y + title_height)], fill=(30, 58, 138))
    
    # 主标题（白色粗体，居中）
    main_title = CONTENT["main_title"]
    main_bbox = draw.textbbox((0, 0), main_title, font=font_main)
    main_width = main_bbox[2] - main_bbox[0]
    draw.text(((width - main_width) // 2, y + 20), main_title, fill=WHITE, font=font_main)
    
    # 副标题（金色，居中）
    sub_title = CONTENT["sub_title"]
    sub_bbox = draw.textbbox((0, 0), sub_title, font=font_sub)
    sub_width = sub_bbox[2] - sub_bbox[0]
    draw.text(((width - sub_width) // 2, y + 100), sub_title, fill=GOLD, font=font_sub)
    
    y += title_height + 30
    
    # ===== 4. 标签（黄色椭圆）=====
    tag = CONTENT["tag"]
    tag_bbox = draw.textbbox((0, 0), tag, font=font_tag)
    tag_width = tag_bbox[2] - tag_bbox[0] + 40
    tag_height = 50
    tag_x = (width - tag_width) // 2
    
    # 画椭圆背景
    draw.ellipse([(tag_x, y), (tag_x + tag_width, y + tag_height)], fill=GOLD)
    
    # 标签文字（黑色）
    tag_text_x = tag_x + 20
    tag_text_y = y + 10
    draw.text((tag_text_x, tag_text_y), tag, fill=(0, 0, 0), font=font_tag)
    
    y += tag_height + 40
    
    # ===== 5. 说明文字（深灰背景条）=====
    for highlight in CONTENT["highlights"]:
        bar_height = 60
        bar_margin = 60
        
        # 深灰背景条
        draw.rectangle([(bar_margin, y), (width - bar_margin, y + bar_height)], fill=DARK_GRAY)
        
        # 文字（白色，左对齐+图标）
        draw.text((bar_margin + 20, y + 15), f"✓ {highlight}", fill=WHITE, font=font_highlight)
        
        y += bar_height + 15
    
    y += 30
    
    # ===== 6. 联系信息框（蓝色边框）=====
    info_box_y = y
    info_box_height = 220
    
    # 蓝色边框
    border_margin = 60
    draw.rectangle(
        [(border_margin, info_box_y), (width - border_margin, info_box_y + info_box_height)],
        outline=BLUE_BORDER,
        width=3
    )
    
    # 信息内容
    info_y = info_box_y + 20
    info_x = border_margin + 30
    
    # 机构名称（金色，加【】）
    draw.text((info_x, info_y), "【视元堂视觉体验中心】", fill=GOLD, font=font_info)
    info_y += 40
    
    # 地址
    draw.text((info_x, info_y), "📍 南充顺庆区白土坝路406号", fill=WHITE, font=font_info)
    info_y += 35
    
    # 电话
    draw.text((info_x, info_y), "📞 0817-2255222 / 19138766190", fill=WHITE, font=font_info)
    info_y += 35
    
    # 营业时间
    draw.text((info_x, info_y), "🕐 营业时间：9:00-21:00", fill=WHITE, font=font_info)
    info_y += 35
    
    # 业务范围
    draw.text((info_x, info_y), "专业验光配镜 | 儿童近视防控 | 视力训练矫正", fill=BLUE_BORDER, font=font_info)
    
    # ===== 7. 序号标签（左上角）=====
    # 画圆角矩形
    draw.rounded_rectangle([(20, 20), (80, 70)], radius=10, fill=BLUE_BORDER)
    draw.text((40, 30), "1", fill=WHITE, font=font_main)
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, CONTENT["output"])
    img.save(output_path, quality=95)
    print(f"✅ 已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = create_promo()
    print(f"\n📸 宣传图: {path}")

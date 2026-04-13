#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂宣传图生成 - 按老板要求修改
1. 图片4个角圆形处理
2. 照片不编号
3. 不用LOGO
4. 公司信息居中
5. 视力训练矫正 → 视力训练
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# ============ 配置 ============
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
PHOTO_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_photos_new"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 颜色
DEEP_BLUE = (15, 23, 42)
WHITE = (255, 255, 255)
GOLD = (251, 191, 36)
DARK_GRAY = (30, 41, 59)
BLUE_BORDER = (59, 130, 246)

# 内容
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
    "output": "20260412_修改版_儿童近视防控.jpg"
}

def add_rounded_corners(img, radius=30):
    """给图片添加圆角"""
    # 创建圆角蒙版
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # 画圆角矩形
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    
    # 应用蒙版
    output = Image.new('RGB', img.size, DEEP_BLUE)
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    return output

def create_promo():
    """按老板要求生成"""
    print("📸 按新要求生成宣传图...")
    
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), DEEP_BLUE)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_main = ImageFont.truetype(FONT_BOLD, 64)
    font_sub = ImageFont.truetype(FONT_BOLD, 42)
    font_tag = ImageFont.truetype(FONT_PATH, 28)
    font_highlight = ImageFont.truetype(FONT_PATH, 32)
    font_info = ImageFont.truetype(FONT_PATH, 26)
    
    y = 30
    
    # ===== 1. 照片区域（上半部分，圆角处理）=====
    photo_path = os.path.join(PHOTO_DIR, CONTENT["photo"])
    if os.path.exists(photo_path):
        photo = Image.open(photo_path)
        
        # 照片尺寸
        photo_height = 750
        ratio = photo_height / photo.height
        photo_width = int(photo.width * ratio)
        if photo_width > width - 60:
            photo_width = width - 60
            photo_height = int(photo.height * (width - 60) / photo.width)
        photo = photo.resize((photo_width, photo_height), Image.LANCZOS)
        
        # 创建带圆角的照片
        photo_with_corners = Image.new('RGB', (photo_width, photo_height), DEEP_BLUE)
        photo_draw = ImageDraw.Draw(photo_with_corners)
        photo_draw.rounded_rectangle([(0, 0), (photo_width, photo_height)], radius=30, fill=(255, 255, 255))
        
        # 创建蒙版
        mask = Image.new('L', (photo_width, photo_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (photo_width, photo_height)], radius=30, fill=255)
        
        # 粘贴照片
        photo_with_corners.paste(photo, (0, 0))
        
        # 居中放置
        photo_x = (width - photo_width) // 2
        img.paste(photo_with_corners, (photo_x, y), mask)
        y += photo_height + 30
    
    # ===== 2. 主标题区域（蓝色背景条）=====
    title_height = 180
    draw.rectangle([(0, y), (width, y + title_height)], fill=(30, 58, 138))
    
    # 主标题（白色，居中）
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
    
    # ===== 3. 标签（黄色椭圆，居中）=====
    tag = CONTENT["tag"]
    tag_bbox = draw.textbbox((0, 0), tag, font=font_tag)
    tag_width = tag_bbox[2] - tag_bbox[0] + 40
    tag_height = 50
    tag_x = (width - tag_width) // 2
    
    draw.ellipse([(tag_x, y), (tag_x + tag_width, y + tag_height)], fill=GOLD)
    draw.text((tag_x + 20, y + 10), tag, fill=(0, 0, 0), font=font_tag)
    
    y += tag_height + 40
    
    # ===== 4. 说明文字（深灰背景条）=====
    for highlight in CONTENT["highlights"]:
        bar_height = 60
        bar_margin = 60
        
        draw.rectangle([(bar_margin, y), (width - bar_margin, y + bar_height)], fill=DARK_GRAY)
        draw.text((bar_margin + 20, y + 15), f"✓ {highlight}", fill=WHITE, font=font_highlight)
        y += bar_height + 15
    
    y += 30
    
    # ===== 5. 公司信息框（蓝色边框，居中）=====
    info_box_y = y
    info_box_height = 220
    info_box_width = width - 120
    info_box_x = 60
    
    # 蓝色边框
    draw.rectangle(
        [(info_box_x, info_box_y), (info_box_x + info_box_width, info_box_y + info_box_height)],
        outline=BLUE_BORDER,
        width=3
    )
    
    # 信息内容（全部居中）
    info_y = info_box_y + 20
    
    # 机构名称
    name = "【视元堂视觉体验中心】"
    name_bbox = draw.textbbox((0, 0), name, font=font_info)
    name_width = name_bbox[2] - name_bbox[0]
    draw.text(((width - name_width) // 2, info_y), name, fill=GOLD, font=font_info)
    info_y += 40
    
    # 地址
    addr = "📍 南充顺庆区白土坝路406号"
    addr_bbox = draw.textbbox((0, 0), addr, font=font_info)
    addr_width = addr_bbox[2] - addr_bbox[0]
    draw.text(((width - addr_width) // 2, info_y), addr, fill=WHITE, font=font_info)
    info_y += 35
    
    # 电话
    phone = "📞 0817-2255222 / 19138766190"
    phone_bbox = draw.textbbox((0, 0), phone, font=font_info)
    phone_width = phone_bbox[2] - phone_bbox[0]
    draw.text(((width - phone_width) // 2, info_y), phone, fill=WHITE, font=font_info)
    info_y += 35
    
    # 营业时间
    time = "🕐 营业时间：9:00-21:00"
    time_bbox = draw.textbbox((0, 0), time, font=font_info)
    time_width = time_bbox[2] - time_bbox[0]
    draw.text(((width - time_width) // 2, info_y), time, fill=WHITE, font=font_info)
    info_y += 35
    
    # 业务范围（视力训练矫正 → 视力训练）
    biz = "专业验光配镜 | 儿童近视防控 | 视力训练"
    biz_bbox = draw.textbbox((0, 0), biz, font=font_info)
    biz_width = biz_bbox[2] - biz_bbox[0]
    draw.text(((width - biz_width) // 2, info_y), biz, fill=BLUE_BORDER, font=font_info)
    
    # ===== 6. 整体图片圆角处理 =====
    # 创建圆角蒙版
    final_mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(final_mask)
    mask_draw.rounded_rectangle([(0, 0), (width, height)], radius=30, fill=255)
    
    # 应用圆角
    final_img = Image.new('RGB', (width, height), DEEP_BLUE)
    final_img.paste(img, (0, 0))
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, CONTENT["output"])
    final_img.save(output_path, quality=95)
    print(f"✅ 已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = create_promo()
    print(f"\n📸 宣传图: {path}")

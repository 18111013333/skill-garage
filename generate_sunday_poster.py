#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂周日亲子护眼日宣传图生成
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 字体路径
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"

# 颜色配置
COLORS = {
    "primary": (41, 128, 185),      # 专业蓝
    "secondary": (46, 204, 113),    # 健康绿
    "accent": (241, 196, 15),       # 温暖黄
    "white": (255, 255, 255),
    "dark": (44, 62, 80),
    "light_bg": (236, 240, 241),
}

# 照片目录
PHOTO_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_photos_new"
LOGO_PATH = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/brand/视元堂LOGO.jpg"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 周日亲子护眼日话术（全新，不重复）
SUNDAY_COPYWRITES = [
    {
        "title": "周日亲子护眼日",
        "subtitle": "带孩子来做个视力检查吧",
        "desc": "早发现 早干预 早矫正",
        "photo": "训练设备_视力训练设备1.jpg"
    },
    {
        "title": "孩子爱玩手机？",
        "subtitle": "视力训练让眼睛更健康",
        "desc": "每天20分钟 科学护眼",
        "photo": "训练设备_视力训练设备2.jpg"
    },
    {
        "title": "别让近视遗传给孩子",
        "subtitle": "父母近视更要重视",
        "desc": "专业筛查 科学防控",
        "photo": "训练设备_视力训练设备3.jpg"
    },
    {
        "title": "周末带娃好去处",
        "subtitle": "视元堂视力训练中心",
        "desc": "边玩边训练 视力看得见",
        "photo": "店铺环境_店内场景1.jpg"
    }
]

def create_poster(copywrite, output_name):
    """生成单张宣传图"""
    # 创建画布 (1080x1920 竖版)
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), COLORS["white"])
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 72)
        font_subtitle = ImageFont.truetype(FONT_PATH, 48)
        font_desc = ImageFont.truetype(FONT_PATH, 36)
        font_info = ImageFont.truetype(FONT_PATH, 28)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_info = ImageFont.load_default()
    
    # 顶部渐变背景
    for y in range(400):
        ratio = y / 400
        r = int(COLORS["primary"][0] * (1 - ratio) + COLORS["secondary"][0] * ratio)
        g = int(COLORS["primary"][1] * (1 - ratio) + COLORS["secondary"][1] * ratio)
        b = int(COLORS["primary"][2] * (1 - ratio) + COLORS["secondary"][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 标题
    title = copywrite["title"]
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 100), title, 
              fill=COLORS["white"], font=font_title)
    
    # 副标题
    subtitle = copywrite["subtitle"]
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((width - subtitle_width) // 2, 200), subtitle, 
              fill=COLORS["white"], font=font_subtitle)
    
    # 描述
    desc = copywrite["desc"]
    desc_bbox = draw.textbbox((0, 0), desc, font=font_desc)
    desc_width = desc_bbox[2] - desc_bbox[0]
    draw.text(((width - desc_width) // 2, 300), desc, 
              fill=COLORS["accent"], font=font_desc)
    
    # 加载照片
    photo_path = os.path.join(PHOTO_DIR, copywrite["photo"])
    if os.path.exists(photo_path):
        photo = Image.open(photo_path)
        # 调整大小
        photo_width = 900
        photo_height = int(photo.height * photo_width / photo.width)
        if photo_height > 800:
            photo_height = 800
            photo_width = int(photo.width * photo_height / photo.height)
        photo = photo.resize((photo_width, photo_height), Image.LANCZOS)
        
        # 照片位置
        photo_x = (width - photo_width) // 2
        photo_y = 450
        
        # 照片圆角
        img.paste(photo, (photo_x, photo_y))
    
    # 底部信息区
    info_y = 1400
    
    # 分隔线
    draw.line([(100, info_y), (width - 100, info_y)], 
              fill=COLORS["primary"], width=3)
    
    # 店铺信息
    info_texts = [
        "【视元堂视觉体验中心】",
        "📍 南充顺庆区白土坝路406号",
        "📞 0817-2255222 / 19138766190",
        "🕐 营业时间：9:00-21:00",
        "专业验光配镜 | 儿童近视防控 | 视力训练矫正"
    ]
    
    for i, text in enumerate(info_texts):
        text_bbox = draw.textbbox((0, 0), text, font=font_info)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text(((width - text_width) // 2, info_y + 30 + i * 45), 
                  text, fill=COLORS["dark"], font=font_info)
    
    # 加载LOGO
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((150, 150), Image.LANCZOS)
        img.paste(logo, ((width - 150) // 2, 1700))
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, output_name)
    img.save(output_path, quality=95)
    print(f"✅ 生成成功: {output_name}")
    return output_path

def main():
    """主函数"""
    print("=" * 50)
    print("视元堂周日亲子护眼日宣传图生成")
    print("=" * 50)
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有宣传图
    for i, copywrite in enumerate(SUNDAY_COPYWRITES, 1):
        output_name = f"20260412_周日亲子护眼日_{i}.jpg"
        create_poster(copywrite, output_name)
    
    print("=" * 50)
    print(f"✅ 全部完成！共生成 {len(SUNDAY_COPYWRITES)} 张宣传图")
    print(f"📁 保存位置: {OUTPUT_DIR}")
    print("=" * 50)

if __name__ == "__main__":
    main()

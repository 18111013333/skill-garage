#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂宣传图+视频生成 - 优化版
LOGO位置优化，画面和谐
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import asyncio
import edge_tts
import subprocess

# ============ 配置 ============
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
PHOTO_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_photos_new"
LOGO_PATH = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/brand/视元堂LOGO.jpg"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 颜色
BG_COLOR = (15, 23, 42)  # 深蓝 #0F172A
GOLD = (251, 191, 36)    # 金色
WHITE = (255, 255, 255)
LIGHT_BLUE = (96, 165, 250)

# 宣传内容
PROMO_CONTENT = {
    "title": "专业验光15年",
    "subtitle": "服务南充10万+顾客",
    "highlights": ["进口验光设备", "持证验光师", "精准到1度"],
    "photo": "验光设备_综合验光仪.jpg",
    "output_img": "20260412_优化版_宣传图.jpg",
    "output_video": "20260412_优化版_宣传视频.mp4"
}

def create_promo_image():
    """生成宣传图 - LOGO左上角，画面和谐"""
    print("📸 生成宣传图...")
    
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_title = ImageFont.truetype(FONT_BOLD, 64)
    font_subtitle = ImageFont.truetype(FONT_PATH, 42)
    font_highlight = ImageFont.truetype(FONT_PATH, 32)
    font_info = ImageFont.truetype(FONT_PATH, 26)
    
    # ===== LOGO 左上角（和谐位置）=====
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        # LOGO大小适中，不要太大
        logo_size = 100
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        
        # 左上角位置，留出适当边距
        logo_margin = 30
        logo_x = logo_margin
        logo_y = logo_margin
        
        # 添加轻微阴影效果让LOGO更融合
        shadow = Image.new('RGBA', (logo_size + 10, logo_size + 10), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle([(5, 5), (logo_size + 5, logo_size + 5)], radius=10, fill=(0, 0, 0, 80))
        
        # 粘贴LOGO
        if logo.mode == 'RGBA':
            img.paste(logo, (logo_x, logo_y), logo)
        else:
            img.paste(logo, (logo_x, logo_y))
    
    # ===== 标题区域（居中，留出LOGO空间）=====
    y = 180
    
    # 主标题
    title = PROMO_CONTENT["title"]
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, y), title, fill=GOLD, font=font_title)
    y += 90
    
    # 副标题
    subtitle = PROMO_CONTENT["subtitle"]
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    sub_width = sub_bbox[2] - sub_bbox[0]
    draw.text(((width - sub_width) // 2, y), subtitle, fill=WHITE, font=font_subtitle)
    y += 80
    
    # 分隔线
    draw.line([(100, y), (width - 100, y)], fill=GOLD, width=2)
    y += 40
    
    # ===== 照片区域 =====
    photo_path = os.path.join(PHOTO_DIR, PROMO_CONTENT["photo"])
    if os.path.exists(photo_path):
        photo = Image.open(photo_path)
        
        # 计算尺寸，保持比例
        max_width = 900
        max_height = 650
        ratio = min(max_width / photo.width, max_height / photo.height)
        new_width = int(photo.width * ratio)
        new_height = int(photo.height * ratio)
        photo = photo.resize((new_width, new_height), Image.LANCZOS)
        
        # 添加圆角和阴影
        photo_x = (width - new_width) // 2
        img.paste(photo, (photo_x, y))
        y += new_height + 40
    
    # ===== 三大亮点 =====
    draw.text((100, y), "⭐ 三大亮点", fill=GOLD, font=font_highlight)
    y += 55
    
    for highlight in PROMO_CONTENT["highlights"]:
        draw.text((120, y), f"✓ {highlight}", fill=WHITE, font=font_highlight)
        y += 45
    
    y += 30
    
    # ===== 底部信息 =====
    draw.line([(100, y), (width - 100, y)], fill=GOLD, width=2)
    y += 35
    
    info_lines = [
        "【视元堂视觉体验中心】",
        "📍 南充顺庆区白土坝路406号",
        "📞 0817-2255222 / 19138766190",
        "🕐 营业时间：9:00-21:00",
        "",
        "专业验光配镜 | 儿童近视防控 | 视力训练矫正"
    ]
    
    for line in info_lines:
        draw.text((100, y), line, fill=LIGHT_BLUE, font=font_info)
        y += 38
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, PROMO_CONTENT["output_img"])
    img.save(output_path, quality=95)
    print(f"✅ 宣传图已保存: {output_path}")
    return output_path

async def generate_voiceover():
    """生成配音"""
    print("🎤 生成配音...")
    
    text = f"""
    {PROMO_CONTENT['title']}，{PROMO_CONTENT['subtitle']}。
    我们拥有进口验光设备，持证验光师坐诊，精准到1度。
    视元堂视觉体验中心，专业验光配镜，儿童近视防控，视力训练矫正。
    地址：南充顺庆区白土坝路406号，电话：0817-2255222。
    """
    
    voiceover_path = os.path.join(OUTPUT_DIR, "temp_voiceover.mp3")
    
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(voiceover_path)
    
    print(f"✅ 配音已保存: {voiceover_path}")
    return voiceover_path

def create_video(image_path, voiceover_path):
    """生成视频 - LOGO在最后一张画面"""
    print("🎬 生成视频...")
    
    try:
        from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
    except:
        print("❌ MoviePy 未安装，正在安装...")
        subprocess.run(["pip", "install", "moviepy"], capture_output=True)
        from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
    
    # 加载音频获取时长
    audio = AudioFileClip(voiceover_path)
    duration = audio.duration
    
    # 创建图片视频片段
    img_clip = ImageClip(image_path, duration=duration)
    img_clip = img_clip.resized((1080, 1920))
    
    # 创建结尾LOGO画面
    logo_frame = Image.new('RGB', (1080, 1920), BG_COLOR)
    draw = ImageDraw.Draw(logo_frame)
    
    # 加载字体
    font_large = ImageFont.truetype(FONT_BOLD, 72)
    font_medium = ImageFont.truetype(FONT_PATH, 36)
    
    # LOGO居中放大
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((300, 300), Image.LANCZOS)
        logo_x = (1080 - 300) // 2
        logo_y = 600
        logo_frame.paste(logo, (logo_x, logo_y))
    
    # 底部文字
    draw.text((1080 // 2 - 200, 1000), "视元堂视觉体验中心", fill=GOLD, font=font_large, anchor="mm")
    draw.text((1080 // 2 - 150, 1100), "专业验光配镜 | 儿童近视防控", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((1080 // 2 - 120, 1200), "📞 0817-2255222", fill=LIGHT_BLUE, font=font_medium, anchor="mm")
    
    # 保存结尾帧
    logo_frame_path = os.path.join(OUTPUT_DIR, "temp_logo_frame.jpg")
    logo_frame.save(logo_frame_path)
    
    # 创建结尾片段（3秒）
    logo_clip = ImageClip(logo_frame_path, duration=3)
    logo_clip = logo_clip.resized((1080, 1920))
    
    # 合并视频
    final_video = concatenate_videoclips([img_clip, logo_clip])
    final_video = final_video.with_audio(audio)
    
    # 保存视频
    output_path = os.path.join(OUTPUT_DIR, PROMO_CONTENT["output_video"])
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    # 清理临时文件
    os.remove(voiceover_path)
    os.remove(logo_frame_path)
    
    print(f"✅ 视频已保存: {output_path}")
    return output_path

async def main():
    print("=" * 50)
    print("🎨 视元堂宣传内容生成 - 优化版")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 生成宣传图
    img_path = create_promo_image()
    
    # 2. 生成配音
    voice_path = await generate_voiceover()
    
    # 3. 生成视频
    video_path = create_video(img_path, voice_path)
    
    print("=" * 50)
    print("✅ 全部完成！")
    print(f"📸 宣传图: {img_path}")
    print(f"🎬 宣传视频: {video_path}")
    print("=" * 50)
    
    return img_path, video_path

if __name__ == "__main__":
    asyncio.run(main())

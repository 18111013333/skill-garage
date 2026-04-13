#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂高端爆款视频生成器
高大上版本：专业转场 + 高级字幕 + 电影感配音
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import asyncio
import edge_tts
import numpy as np
from scipy.io import wavfile

# ============ 配置 ============
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
PHOTO_BASE = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_photos_new"
LOGO_PATH = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/brand/视元堂LOGO.jpg"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"
BGM_PATH = "/tmp/piano_music.wav"

# 高端配色
DEEP_BLUE = (15, 23, 42)
NAVY_BLUE = (30, 58, 138)
WHITE = (255, 255, 255)
GOLD = (251, 191, 36)
LIGHT_GOLD = (253, 224, 71)
BLUE_BORDER = (59, 130, 246)
GRADIENT_TOP = (30, 41, 59)
GRADIENT_BOTTOM = (15, 23, 42)

# 高端话术
PREMIUM_CAPTIONS = {
    "验光": {
        "subtitles": ["专业验光 · 精准每一度", "进口设备 · 科学检测", "视元堂 · 您的视力管家"],
        "voiceover": "专业验光，精准配镜。视元堂引进进口验光设备，科学检测每一度，让您的眼镜更舒适。视元堂视觉体验中心，专业验光配镜，儿童近视防控，视力训练。"
    },
    "配镜": {
        "subtitles": ["精湛工艺 · 立等可取", "德国设备 · 品质保证", "每一副 · 都是艺术品"],
        "voiceover": "精湛工艺，立等可取。视元堂配备德国进口配镜设备，每一副眼镜都是艺术品。视元堂视觉体验中心，专业验光配镜，儿童近视防控，视力训练。"
    },
    "训练": {
        "subtitles": ["黑科技训练仪", "每天20分钟 · 3个月见效", "科学防控 · 看得见的效果"],
        "voiceover": "孩子近视不用慌，科学训练有方法。视元堂引进黑科技训练仪，每天20分钟，3个月见效。视元堂视觉体验中心，专业验光配镜，儿童近视防控，视力训练。"
    },
    "环境": {
        "subtitles": ["温馨环境 · 专业服务", "品牌授权 · 品质保证", "视元堂 · 您身边的视力管家"],
        "voiceover": "温馨环境，专业服务。视元堂视觉体验中心，您身边的视力管家。专业验光配镜，儿童近视防控，视力训练。视元堂，值得信赖。"
    }
}

def add_gradient_overlay(img, opacity=0.3):
    """添加渐变叠加层"""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 从上到下渐变
    for y in range(img.height):
        alpha = int(opacity * 255 * (y / img.height))
        draw.line([(0, y), (img.width, y)], fill=(0, 0, 0, alpha))
    
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def create_premium_frame(photo_path, subtitle, frame_num, total_frames):
    """创建高端视频帧"""
    photo = Image.open(photo_path)
    
    # 全屏填充
    target_width = 1080
    target_height = 1920
    
    img_ratio = photo.width / photo.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        new_height = photo.height
        new_width = int(new_height * target_ratio)
        left = (photo.width - new_width) // 2
        photo = photo.crop((left, 0, left + new_width, new_height))
    else:
        new_width = photo.width
        new_height = int(new_width / target_ratio)
        top = (photo.height - new_height) // 2
        photo = photo.crop((0, top, new_width, top + new_height))
    
    photo = photo.resize((target_width, target_height), Image.LANCZOS)
    
    # 添加渐变叠加
    photo = add_gradient_overlay(photo, 0.2)
    
    draw = ImageDraw.Draw(photo)
    
    # ===== 顶部品牌栏 =====
    draw.rectangle([(0, 0), (1080, 100)], fill=(0, 0, 0, 180))
    
    # 品牌名称
    brand_font = ImageFont.truetype(FONT_BOLD, 42)
    brand_text = "视元堂视觉体验中心"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_width = brand_bbox[2] - brand_bbox[0]
    draw.text(((1080 - brand_width) // 2, 30), brand_text, fill=GOLD, font=brand_font)
    
    # ===== 底部字幕区 =====
    # 渐变背景
    for y in range(300):
        alpha = int(200 * (y / 300))
        draw.line([(0, 1620 + y), (1080, 1620 + y)], fill=(0, 0, 0, alpha))
    
    # 主字幕（大号金色）
    main_font = ImageFont.truetype(FONT_BOLD, 56)
    main_bbox = draw.textbbox((0, 0), subtitle, font=main_font)
    main_width = main_bbox[2] - main_bbox[0]
    
    # 字幕阴影
    draw.text(((1080 - main_width) // 2 + 3, 1683), subtitle, fill=(0, 0, 0), font=main_font)
    # 字幕主体
    draw.text(((1080 - main_width) // 2, 1680), subtitle, fill=WHITE, font=main_font)
    
    # 金色下划线
    line_width = main_width + 60
    draw.rectangle(
        [((1080 - line_width) // 2, 1760), ((1080 + line_width) // 2, 1765)],
        fill=GOLD
    )
    
    # ===== 底部联系信息 =====
    info_font = ImageFont.truetype(FONT_PATH, 28)
    
    # 地址
    addr_text = "📍 南充顺庆区白土坝路406号"
    addr_bbox = draw.textbbox((0, 0), addr_text, font=info_font)
    addr_width = addr_bbox[2] - addr_bbox[0]
    draw.text(((1080 - addr_width) // 2, 1800), addr_text, fill=WHITE, font=info_font)
    
    # 电话
    phone_text = "📞 0817-2255222"
    phone_bbox = draw.textbbox((0, 0), phone_text, font=info_font)
    phone_width = phone_bbox[2] - phone_bbox[0]
    draw.text(((1080 - phone_width) // 2, 1840), phone_text, fill=LIGHT_GOLD, font=info_font)
    
    # 业务范围
    biz_font = ImageFont.truetype(FONT_PATH, 24)
    biz_text = "专业验光配镜 | 儿童近视防控 | 视力训练"
    biz_bbox = draw.textbbox((0, 0), biz_text, font=biz_font)
    biz_width = biz_bbox[2] - biz_bbox[0]
    draw.text(((1080 - biz_width) // 2, 1880), biz_text, fill=(180, 180, 180), font=biz_font)
    
    return photo.convert('RGB')

async def generate_premium_video(photos, subtitles, voiceover_text, output_path, video_type):
    """生成高端视频"""
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
    
    print(f"  🎬 生成{video_type}视频...")
    
    # 生成配音
    voice_path = output_path.replace('.mp4', '_voice.mp3')
    communicate = edge_tts.Communicate(voiceover_text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(voice_path)
    
    voice = AudioFileClip(voice_path)
    duration = voice.duration
    photo_duration = duration / len(photos)
    
    # 创建高端照片片段
    clips = []
    for i, (photo_path, subtitle) in enumerate(zip(photos, subtitles)):
        frame = create_premium_frame(photo_path, subtitle, i, len(photos))
        
        temp_path = output_path.replace('.mp4', f'_frame_{i}.jpg')
        frame.save(temp_path)
        
        clip = ImageClip(temp_path, duration=photo_duration)
        clips.append(clip)
    
    # 合并照片片段
    main_video = concatenate_videoclips(clips)
    
    # ===== 高端结尾画面 =====
    logo_frame = Image.new('RGB', (1080, 1920), DEEP_BLUE)
    draw = ImageDraw.Draw(logo_frame)
    
    # 渐变背景
    for y in range(1920):
        ratio = y / 1920
        r = int(15 + (30 - 15) * ratio)
        g = int(23 + (58 - 23) * ratio)
        b = int(42 + (138 - 42) * ratio)
        draw.line([(0, y), (1080, y)], fill=(r, g, b))
    
    # LOGO居中（带光晕效果）
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((350, 350), Image.LANCZOS)
        
        # 光晕效果
        glow = Image.new('RGBA', (450, 450), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse([(0, 0), (450, 450)], fill=(251, 191, 36, 50))
        glow = glow.filter(ImageFilter.GaussianBlur(20))
        
        logo_frame = logo_frame.convert('RGBA')
        logo_frame.paste(glow, ((1080 - 450) // 2, 500), glow)
        logo_frame.paste(logo, ((1080 - 350) // 2, 550))
        logo_frame = logo_frame.convert('RGB')
    
    draw = ImageDraw.Draw(logo_frame)
    
    # 品牌名称（大号金色）
    font_large = ImageFont.truetype(FONT_BOLD, 64)
    draw.text((540, 980), "视元堂视觉体验中心", fill=GOLD, font=font_large, anchor="mm")
    
    # 分隔线
    draw.rectangle([(340, 1040), (740, 1043)], fill=GOLD)
    
    # 业务范围
    font_medium = ImageFont.truetype(FONT_PATH, 36)
    draw.text((540, 1100), "专业验光配镜", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((540, 1150), "儿童近视防控", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((540, 1200), "视力训练", fill=WHITE, font=font_medium, anchor="mm")
    
    # 联系信息
    font_info = ImageFont.truetype(FONT_PATH, 32)
    draw.text((540, 1300), "📍 南充顺庆区白土坝路406号", fill=WHITE, font=font_info, anchor="mm")
    draw.text((540, 1360), "📞 0817-2255222", fill=LIGHT_GOLD, font=font_info, anchor="mm")
    
    # 营业时间
    font_small = ImageFont.truetype(FONT_PATH, 28)
    draw.text((540, 1430), "🕐 周一至周日 9:00-21:00", fill=(180, 180, 180), font=font_small, anchor="mm")
    
    logo_frame_path = output_path.replace('.mp4', '_logo.jpg')
    logo_frame.save(logo_frame_path)
    
    logo_clip = ImageClip(logo_frame_path, duration=4)
    
    # 合并主视频和结尾
    final_video = concatenate_videoclips([main_video, logo_clip])
    
    # 合成音频
    bgm = AudioFileClip(BGM_PATH)
    voice_duration = min(voice.duration, main_video.duration)
    bgm = bgm.subclipped(0, min(bgm.duration, voice_duration))
    bgm = bgm.with_volume_scaled(0.25)
    voice = voice.subclipped(0, voice_duration)
    
    composite_audio = CompositeAudioClip([voice, bgm])
    final_video = final_video.with_audio(composite_audio)
    
    # 保存视频
    final_video.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        audio_bitrate='256k'
    )
    
    # 清理临时文件
    for i in range(len(photos)):
        temp_path = output_path.replace('.mp4', f'_frame_{i}.jpg')
        if os.path.exists(temp_path):
            os.remove(temp_path)
    if os.path.exists(logo_frame_path):
        os.remove(logo_frame_path)
    if os.path.exists(voice_path):
        os.remove(voice_path)
    
    print(f"  ✅ {video_type}视频完成")
    return output_path

async def main():
    print("=" * 60)
    print("🎬 视元堂高端爆款视频生成器")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    videos = []
    
    # 1. 验光视频
    video_photos = [
        f"{PHOTO_BASE}/一楼验光设备/验光设备_1.jpg",
        f"{PHOTO_BASE}/一楼验光设备/验光设备_2.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_3.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/高端_验光视频.mp4"
        captions = PREMIUM_CAPTIONS["验光"]
        await generate_premium_video(
            video_photos[:3], 
            captions["subtitles"][:3], 
            captions["voiceover"], 
            output,
            "验光"
        )
        videos.append(output)
    
    # 2. 配镜视频
    video_photos = [
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_1.jpg",
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_2.jpg",
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_3.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/高端_配镜视频.mp4"
        captions = PREMIUM_CAPTIONS["配镜"]
        await generate_premium_video(
            video_photos[:3], 
            captions["subtitles"][:3], 
            captions["voiceover"], 
            output,
            "配镜"
        )
        videos.append(output)
    
    # 3. 训练视频
    video_photos = [
        f"{PHOTO_BASE}/二楼训练设备/训练设备_1.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_2.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_3.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_4.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/高端_训练视频.mp4"
        captions = PREMIUM_CAPTIONS["训练"]
        await generate_premium_video(
            video_photos[:4], 
            captions["subtitles"][:4], 
            captions["voiceover"], 
            output,
            "训练"
        )
        videos.append(output)
    
    # 4. 环境视频
    video_photos = [
        f"{PHOTO_BASE}/一楼环境/一楼环境_1.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_2.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_3.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_4.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_5.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/高端_环境视频.mp4"
        captions = PREMIUM_CAPTIONS["环境"]
        await generate_premium_video(
            video_photos[:5], 
            captions["subtitles"][:5], 
            captions["voiceover"], 
            output,
            "环境"
        )
        videos.append(output)
    
    print("\n" + "=" * 60)
    print("✅ 全部完成！")
    print(f"🎬 高端视频: {len(videos)} 条")
    print("=" * 60)
    
    return videos

if __name__ == "__main__":
    asyncio.run(main())

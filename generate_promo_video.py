#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂宣传视频生成 - 3-5张连贯照片 + 配音 + 轻音乐
"""

from PIL import Image, ImageDraw, ImageFont
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
DEEP_BLUE = (15, 23, 42)
WHITE = (255, 255, 255)
GOLD = (251, 191, 36)
BLUE_BORDER = (59, 130, 246)

# 选取3张连贯照片（训练设备类）
PHOTOS = [
    "训练设备_视力训练设备1.jpg",
    "训练设备_视力训练设备2.jpg",
    "训练设备_视力训练设备3.jpg"
]

# 配音文本
VOICEOVER_TEXT = """
孩子近视不用慌，科学训练有方法。
视元堂引进黑科技训练仪，每天20分钟，3个月见效。
专业验光师一对一指导，让孩子视力看得见。
视元堂视觉体验中心，专业验光配镜，儿童近视防控，视力训练。
地址：南充顺庆区白土坝路406号，电话：0817-2255222。
"""

async def generate_voiceover():
    """生成配音"""
    print("🎤 生成配音...")
    voiceover_path = os.path.join(OUTPUT_DIR, "temp_voiceover.mp3")
    communicate = edge_tts.Communicate(VOICEOVER_TEXT, "zh-CN-XiaoxiaoNeural")
    await communicate.save(voiceover_path)
    print(f"✅ 配音已保存")
    return voiceover_path

def download_bgm():
    """下载轻音乐背景"""
    print("🎵 下载轻音乐...")
    bgm_path = os.path.join(OUTPUT_DIR, "temp_bgm.mp3")
    
    # 使用 Pixabay 免费轻音乐
    bgm_url = "https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3"
    
    try:
        subprocess.run([
            "curl", "-L", "-o", bgm_path, bgm_url,
            "--connect-timeout", "10",
            "--max-time", "30"
        ], capture_output=True, check=True)
        print(f"✅ 轻音乐已下载")
        return bgm_path
    except:
        print("⚠️ 下载失败，使用备用方案")
        return None

def create_video(voiceover_path, bgm_path):
    """生成视频"""
    print("🎬 生成视频...")
    
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
    
    # 加载音频
    voice = AudioFileClip(voiceover_path)
    duration = voice.duration
    
    # 每张照片的时长
    photo_duration = duration / len(PHOTOS)
    
    # 创建照片片段
    clips = []
    for i, photo_name in enumerate(PHOTOS):
        photo_path = os.path.join(PHOTO_DIR, photo_name)
        if os.path.exists(photo_path):
            photo = Image.open(photo_path)
            
            # 调整尺寸
            target_width = 1080
            target_height = 1920
            ratio = min(target_width / photo.width, target_height / photo.height)
            new_width = int(photo.width * ratio)
            new_height = int(photo.height * ratio)
            photo = photo.resize((new_width, new_height), Image.LANCZOS)
            
            # 创建背景
            bg = Image.new('RGB', (target_width, target_height), DEEP_BLUE)
            photo_x = (target_width - new_width) // 2
            photo_y = (target_height - new_height) // 2
            bg.paste(photo, (photo_x, photo_y))
            
            # 添加文字
            draw = ImageDraw.Draw(bg)
            font_title = ImageFont.truetype(FONT_BOLD, 48)
            font_info = ImageFont.truetype(FONT_PATH, 28)
            
            # 标题
            titles = ["孩子近视不用慌", "科学训练有方法", "3个月见效"]
            title = titles[i] if i < len(titles) else ""
            title_bbox = draw.textbbox((0, 0), title, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((target_width - title_width) // 2, 100), title, fill=GOLD, font=font_title)
            
            # 底部信息
            info = "视元堂视觉体验中心 | 📞 0817-2255222"
            info_bbox = draw.textbbox((0, 0), info, font=font_info)
            info_width = info_bbox[2] - info_bbox[0]
            draw.text(((target_width - info_width) // 2, target_height - 80), info, fill=WHITE, font=font_info)
            
            # 保存临时图片
            temp_img_path = os.path.join(OUTPUT_DIR, f"temp_frame_{i}.jpg")
            bg.save(temp_img_path)
            
            # 创建视频片段
            clip = ImageClip(temp_img_path, duration=photo_duration)
            clips.append(clip)
    
    # 合并照片片段
    main_video = concatenate_videoclips(clips)
    
    # 创建结尾LOGO画面
    logo_frame = Image.new('RGB', (1080, 1920), DEEP_BLUE)
    draw = ImageDraw.Draw(logo_frame)
    
    # LOGO居中
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((300, 300), Image.LANCZOS)
        logo_x = (1080 - 300) // 2
        logo_y = 600
        logo_frame.paste(logo, (logo_x, logo_y))
    
    # 文字
    font_large = ImageFont.truetype(FONT_BOLD, 56)
    font_medium = ImageFont.truetype(FONT_PATH, 32)
    
    draw.text((540, 1000), "视元堂视觉体验中心", fill=GOLD, font=font_large, anchor="mm")
    draw.text((540, 1100), "专业验光配镜 | 儿童近视防控 | 视力训练", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((540, 1200), "📍 南充顺庆区白土坝路406号", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((540, 1280), "📞 0817-2255222", fill=BLUE_BORDER, font=font_medium, anchor="mm")
    
    logo_frame_path = os.path.join(OUTPUT_DIR, "temp_logo_frame.jpg")
    logo_frame.save(logo_frame_path)
    
    # 结尾片段（3秒）
    logo_clip = ImageClip(logo_frame_path, duration=3)
    
    # 合并主视频和结尾
    final_video = concatenate_videoclips([main_video, logo_clip])
    
    # 添加音频
    if bgm_path and os.path.exists(bgm_path):
        bgm = AudioFileClip(bgm_path)
        bgm = bgm.subclipped(0, min(bgm.duration, final_video.duration))
        bgm = bgm.with_volume_scaled(0.3)  # 降低背景音乐音量
        
        # 合并配音和背景音乐
        voice = voice.subclipped(0, min(voice.duration, main_video.duration))
        composite_audio = CompositeAudioClip([voice, bgm])
        final_video = final_video.with_audio(composite_audio)
    else:
        final_video = final_video.with_audio(voice)
    
    # 保存视频
    output_path = os.path.join(OUTPUT_DIR, "20260412_宣传视频_儿童近视防控.mp4")
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    # 清理临时文件
    for i in range(len(PHOTOS)):
        temp_img = os.path.join(OUTPUT_DIR, f"temp_frame_{i}.jpg")
        if os.path.exists(temp_img):
            os.remove(temp_img)
    if os.path.exists(logo_frame_path):
        os.remove(logo_frame_path)
    if os.path.exists(voiceover_path):
        os.remove(voiceover_path)
    if bgm_path and os.path.exists(bgm_path):
        os.remove(bgm_path)
    
    print(f"✅ 视频已保存: {output_path}")
    return output_path

async def main():
    print("=" * 50)
    print("🎬 视元堂宣传视频生成")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 生成配音
    voiceover_path = await generate_voiceover()
    
    # 2. 下载轻音乐
    bgm_path = download_bgm()
    
    # 3. 生成视频
    video_path = create_video(voiceover_path, bgm_path)
    
    print("=" * 50)
    print("✅ 全部完成！")
    print(f"🎬 视频路径: {video_path}")
    print("=" * 50)
    
    return video_path

if __name__ == "__main__":
    asyncio.run(main())

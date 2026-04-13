#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂宣传视频生成 - 带字幕 + 正确背景音乐
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

# 选取3张连贯照片
PHOTOS = [
    "训练设备_视力训练设备1.jpg",
    "训练设备_视力训练设备2.jpg",
    "训练设备_视力训练设备3.jpg"
]

# 每张照片对应的字幕
SUBTITLES = [
    "孩子近视不用慌",
    "科学训练有方法",
    "3个月见效 看得见"
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
    """下载轻音乐背景（按昨天的方式）"""
    print("🎵 下载轻音乐...")
    bgm_path = os.path.join(OUTPUT_DIR, "temp_bgm.mp3")
    
    # Pixabay 免费轻音乐 - Happy Ukulele
    bgm_url = "https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3"
    
    # 按昨天的方式下载
    result = subprocess.run([
        "curl", "-L", "-o", bgm_path, bgm_url
    ], capture_output=True, text=True)
    
    if result.returncode == 0 and os.path.exists(bgm_path):
        # 验证是否是真实音乐
        file_result = subprocess.run(["file", bgm_path], capture_output=True, text=True)
        print(f"✅ 音乐文件: {file_result.stdout.strip()}")
        
        # 检查文件大小
        size = os.path.getsize(bgm_path)
        print(f"✅ 文件大小: {size / 1024:.1f} KB")
        
        if size > 100000:  # 大于100KB才是真实音乐
            print("✅ 轻音乐下载成功")
            return bgm_path
    
    print("❌ 下载失败")
    return None

def create_video_with_subtitles(voiceover_path, bgm_path):
    """生成带字幕的视频"""
    print("🎬 生成带字幕视频...")
    
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
    
    # 加载音频
    voice = AudioFileClip(voiceover_path)
    duration = voice.duration
    
    # 每张照片的时长
    photo_duration = duration / len(PHOTOS)
    
    # 创建照片片段（带字幕）
    clips = []
    for i, (photo_name, subtitle) in enumerate(zip(PHOTOS, SUBTITLES)):
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
            
            # ===== 添加字幕 =====
            draw = ImageDraw.Draw(bg)
            
            # 字幕背景（半透明黑色）
            subtitle_font = ImageFont.truetype(FONT_BOLD, 52)
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]
            
            # 字幕位置（底部）
            subtitle_y = target_height - 200
            subtitle_x = (target_width - subtitle_width) // 2
            
            # 画字幕背景
            padding = 20
            draw.rectangle(
                [(subtitle_x - padding, subtitle_y - padding), 
                 (subtitle_x + subtitle_width + padding, subtitle_y + subtitle_height + padding)],
                fill=(0, 0, 0, 180)
            )
            
            # 画字幕文字（白色描边）
            # 描边
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                draw.text((subtitle_x + dx, subtitle_y + dy), subtitle, fill=(0, 0, 0), font=subtitle_font)
            # 主文字
            draw.text((subtitle_x, subtitle_y), subtitle, fill=WHITE, font=subtitle_font)
            
            # 顶部标题
            title_font = ImageFont.truetype(FONT_BOLD, 48)
            title = "视元堂视觉体验中心"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((target_width - title_width) // 2, 60), title, fill=GOLD, font=title_font)
            
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
    
    # ===== 添加音频 =====
    if bgm_path and os.path.exists(bgm_path):
        bgm = AudioFileClip(bgm_path)
        # 裁剪到视频时长
        bgm = bgm.subclipped(0, min(bgm.duration, final_video.duration))
        # 降低背景音乐音量到30%
        bgm = bgm.with_volume_scaled(0.3)
        
        # 配音裁剪到主视频时长
        voice = voice.subclipped(0, min(voice.duration, main_video.duration))
        
        # 合并配音和背景音乐
        composite_audio = CompositeAudioClip([voice, bgm])
        final_video = final_video.with_audio(composite_audio)
        print("✅ 配音 + 背景音乐已合并")
    else:
        final_video = final_video.with_audio(voice)
        print("⚠️ 仅添加配音")
    
    # 保存视频
    output_path = os.path.join(OUTPUT_DIR, "20260412_带字幕_宣传视频.mp4")
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
    print("🎬 视元堂宣传视频生成 - 带字幕版")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 生成配音
    voiceover_path = await generate_voiceover()
    
    # 2. 下载轻音乐（按昨天的方式）
    bgm_path = download_bgm()
    
    # 3. 生成带字幕视频
    video_path = create_video_with_subtitles(voiceover_path, bgm_path)
    
    print("=" * 50)
    print("✅ 全部完成！")
    print(f"🎬 视频路径: {video_path}")
    print("=" * 50)
    
    return video_path

if __name__ == "__main__":
    asyncio.run(main())

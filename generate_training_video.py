#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂视力训练爆款视频 - 5张照片 + 字幕 + 配音 + 背景音乐
"""

from PIL import Image, ImageDraw, ImageFont
import os
import asyncio
import edge_tts
import subprocess

# ============ 配置 ============
FONT_PATH = "/usr/share/fonts/HarmonyFont/Harmony-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/HarmonyFont/Harmony-Bold.ttf"
PHOTO_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/training"
LOGO_PATH = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_assets/brand/视元堂LOGO.jpg"
OUTPUT_DIR = "/home/sandbox/.openclaw/workspace/memory/shiyuantang_marketing/宣传图"

# 颜色
DEEP_BLUE = (15, 23, 42)
WHITE = (255, 255, 255)
GOLD = (251, 191, 36)
BLUE_BORDER = (59, 130, 246)

# 5张视力训练照片
PHOTOS = [
    "视力训练设备_3.jpg",
    "视力训练设备_4.jpg",
    "视力训练设备_5.jpg",
    "视力训练设备_6.jpg",
    "视力训练设备_7.jpg"
]

# 每张照片对应的字幕（新话术）
SUBTITLES = [
    "黑科技训练仪，近视防控新选择",
    "孩子的视力，我们来守护",
    "科学训练，看得见的效果",
    "每天20分钟，视力提升看得见",
    "视元堂视力训练，给孩子清晰未来"
]

# 配音文本
VOICEOVER_TEXT = """
黑科技训练仪，近视防控新选择。
孩子的视力，我们来守护。
科学训练，看得见的效果。
每天20分钟，视力提升看得见。
视元堂视力训练，给孩子清晰未来。
视元堂视觉体验中心，专业验光配镜，儿童近视防控，视力训练。
电话：0817-2255222。
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
    """下载 Happy Ukulele 背景音乐"""
    print("🎵 下载 Happy Ukulele 背景音乐...")
    bgm_path = os.path.join(OUTPUT_DIR, "temp_bgm.mp3")
    
    # Happy Ukulele - 欢快轻音乐
    bgm_url = "https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3"
    
    result = subprocess.run([
        "curl", "-L", "-o", bgm_path, bgm_url
    ], capture_output=True, text=True)
    
    if result.returncode == 0 and os.path.exists(bgm_path):
        file_result = subprocess.run(["file", bgm_path], capture_output=True, text=True)
        print(f"✅ 音乐文件: {file_result.stdout.strip()}")
        size = os.path.getsize(bgm_path)
        print(f"✅ 文件大小: {size / 1024:.1f} KB")
        return bgm_path
    
    print("❌ 下载失败")
    return None

def create_video(voiceover_path, bgm_path):
    """生成视频"""
    print("🎬 生成视力训练爆款视频...")
    
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
            
            # 全屏填充，无黑边
            target_width = 1080
            target_height = 1920
            
            # 计算裁剪区域（居中裁剪）
            img_ratio = photo.width / photo.height
            target_ratio = target_width / target_height
            
            if img_ratio > target_ratio:
                # 图片更宽，裁剪左右
                new_height = photo.height
                new_width = int(new_height * target_ratio)
                left = (photo.width - new_width) // 2
                photo = photo.crop((left, 0, left + new_width, new_height))
            else:
                # 图片更高，裁剪上下
                new_width = photo.width
                new_height = int(new_width / target_ratio)
                top = (photo.height - new_height) // 2
                photo = photo.crop((0, top, new_width, top + new_height))
            
            # 调整到目标尺寸
            photo = photo.resize((target_width, target_height), Image.LANCZOS)
            
            # 创建画布
            bg = photo.copy()
            draw = ImageDraw.Draw(bg)
            
            # ===== 添加字幕 =====
            subtitle_font = ImageFont.truetype(FONT_BOLD, 48)
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]
            
            # 字幕位置（底部）
            subtitle_y = target_height - 180
            subtitle_x = (target_width - subtitle_width) // 2
            
            # 画字幕背景（半透明黑色）
            padding = 25
            draw.rectangle(
                [(subtitle_x - padding, subtitle_y - padding), 
                 (subtitle_x + subtitle_width + padding, subtitle_y + subtitle_height + padding)],
                fill=(0, 0, 0)
            )
            
            # 画字幕文字（白色描边）
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                draw.text((subtitle_x + dx, subtitle_y + dy), subtitle, fill=(0, 0, 0), font=subtitle_font)
            draw.text((subtitle_x, subtitle_y), subtitle, fill=WHITE, font=subtitle_font)
            
            # 顶部标题
            title_font = ImageFont.truetype(FONT_BOLD, 44)
            title = "视元堂视觉体验中心"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            
            # 标题背景
            draw.rectangle([(0, 40), (target_width, 120)], fill=(0, 0, 0))
            draw.text(((target_width - title_width) // 2, 55), title, fill=GOLD, font=title_font)
            
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
        bgm = bgm.with_volume_scaled(0.3)  # 背景音乐30%音量
        
        voice = voice.subclipped(0, min(voice.duration, main_video.duration))
        
        composite_audio = CompositeAudioClip([voice, bgm])
        final_video = final_video.with_audio(composite_audio)
        print("✅ 配音 + 背景音乐已合并")
    else:
        final_video = final_video.with_audio(voice)
        print("⚠️ 仅添加配音")
    
    # 保存视频
    output_path = os.path.join(OUTPUT_DIR, "视力训练爆款视频.mp4")
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        audio_bitrate='256k'
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
    print("🎬 视元堂视力训练爆款视频生成")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 生成配音
    voiceover_path = await generate_voiceover()
    
    # 2. 下载 Happy Ukulele 背景音乐
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

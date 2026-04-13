#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂视力训练爆款视频 - 修复版
按昨天的方法：真实背景音乐 + 正确合成
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
BGM_PATH = "/tmp/real_music.mp3"  # 使用已验证的真实音乐

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

# 每张照片对应的字幕
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

def create_video(voiceover_path):
    """生成视频 - 按昨天的正确方法"""
    print("🎬 生成视频...")
    
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
    
    # 加载配音
    voice = AudioFileClip(voiceover_path)
    duration = voice.duration
    
    # 每张照片的时长
    photo_duration = duration / len(PHOTOS)
    
    # 创建照片片段
    clips = []
    for i, (photo_name, subtitle) in enumerate(zip(PHOTOS, SUBTITLES)):
        photo_path = os.path.join(PHOTO_DIR, photo_name)
        if os.path.exists(photo_path):
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
            
            # 创建画布
            bg = photo.copy()
            draw = ImageDraw.Draw(bg)
            
            # 字幕
            subtitle_font = ImageFont.truetype(FONT_BOLD, 48)
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            
            subtitle_y = target_height - 180
            subtitle_x = (target_width - subtitle_width) // 2
            
            # 字幕背景
            padding = 25
            draw.rectangle(
                [(subtitle_x - padding, subtitle_y - padding), 
                 (subtitle_x + subtitle_width + padding, subtitle_y + 80)],
                fill=(0, 0, 0)
            )
            
            # 字幕文字
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                draw.text((subtitle_x + dx, subtitle_y + dy), subtitle, fill=(0, 0, 0), font=subtitle_font)
            draw.text((subtitle_x, subtitle_y), subtitle, fill=WHITE, font=subtitle_font)
            
            # 顶部标题
            title_font = ImageFont.truetype(FONT_BOLD, 44)
            title = "视元堂视觉体验中心"
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.rectangle([(0, 40), (target_width, 120)], fill=(0, 0, 0))
            draw.text(((target_width - title_width) // 2, 55), title, fill=GOLD, font=title_font)
            
            # 保存
            temp_img_path = os.path.join(OUTPUT_DIR, f"temp_frame_{i}.jpg")
            bg.save(temp_img_path)
            
            clip = ImageClip(temp_img_path, duration=photo_duration)
            clips.append(clip)
    
    # 合并照片片段
    main_video = concatenate_videoclips(clips)
    
    # 结尾LOGO画面
    logo_frame = Image.new('RGB', (1080, 1920), DEEP_BLUE)
    draw = ImageDraw.Draw(logo_frame)
    
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        logo = logo.resize((300, 300), Image.LANCZOS)
        logo_x = (1080 - 300) // 2
        logo_y = 600
        logo_frame.paste(logo, (logo_x, logo_y))
    
    font_large = ImageFont.truetype(FONT_BOLD, 56)
    font_medium = ImageFont.truetype(FONT_PATH, 32)
    
    draw.text((540, 1000), "视元堂视觉体验中心", fill=GOLD, font=font_large, anchor="mm")
    draw.text((540, 1100), "专业验光配镜 | 儿童近视防控 | 视力训练", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((540, 1200), "📍 南充顺庆区白土坝路406号", fill=WHITE, font=font_medium, anchor="mm")
    draw.text((540, 1280), "📞 0817-2255222", fill=BLUE_BORDER, font=font_medium, anchor="mm")
    
    logo_frame_path = os.path.join(OUTPUT_DIR, "temp_logo_frame.jpg")
    logo_frame.save(logo_frame_path)
    
    logo_clip = ImageClip(logo_frame_path, duration=3)
    
    # 合并主视频和结尾
    final_video = concatenate_videoclips([main_video, logo_clip])
    
    # ===== 按昨天的方法合成音频 =====
    print("🎵 合成音频...")
    
    # 加载背景音乐（已验证的真实音乐）
    bgm = AudioFileClip(BGM_PATH)
    print(f"✅ 背景音乐时长: {bgm.duration:.1f}秒")
    
    # 背景音乐只有3.9秒，裁剪到配音时长
    voice_duration = min(voice.duration, main_video.duration)
    bgm = bgm.subclipped(0, min(bgm.duration, voice_duration))
    
    # 降低背景音乐音量
    bgm = bgm.with_volume_scaled(0.3)
    
    # 配音裁剪
    voice = voice.subclipped(0, voice_duration)
    
    # 合成音频（按昨天的方法）
    composite_audio = CompositeAudioClip([voice, bgm])
    
    # 设置音频
    final_video = final_video.with_audio(composite_audio)
    print("✅ 配音 + 背景音乐已合并")
    
    # 保存视频（按昨天的参数）
    output_path = os.path.join(OUTPUT_DIR, "视力训练爆款视频_修复版.mp4")
    final_video.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        audio_bitrate='256k'
    )
    
    # 清理
    for i in range(len(PHOTOS)):
        temp_img = os.path.join(OUTPUT_DIR, f"temp_frame_{i}.jpg")
        if os.path.exists(temp_img):
            os.remove(temp_img)
    if os.path.exists(logo_frame_path):
        os.remove(logo_frame_path)
    if os.path.exists(voiceover_path):
        os.remove(voiceover_path)
    
    print(f"✅ 视频已保存: {output_path}")
    return output_path

async def main():
    print("=" * 50)
    print("🎬 视力训练爆款视频 - 修复版")
    print("=" * 50)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 生成配音
    voiceover_path = await generate_voiceover()
    
    # 2. 生成视频（使用已验证的背景音乐）
    video_path = create_video(voiceover_path)
    
    print("=" * 50)
    print("✅ 全部完成！")
    print(f"🎬 视频路径: {video_path}")
    print("=" * 50)
    
    return video_path

if __name__ == "__main__":
    asyncio.run(main())

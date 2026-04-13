#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂每日宣传内容生成器
按照宣传计划生成：6-8张图片 + 3-5条视频
"""

from PIL import Image, ImageDraw, ImageFont
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

# 颜色
DEEP_BLUE = (15, 23, 42)
WHITE = (255, 255, 255)
GOLD = (251, 191, 36)
BLUE_BORDER = (59, 130, 246)

# 爆款话术库
CAPTIONS = {
    "验光设备": [
        "专业验光，精准配镜",
        "进口设备，科学验光",
        "每一度都精准，每一副都舒适"
    ],
    "配镜设备": [
        "现场加工，立等可取",
        "德国设备，精湛工艺",
        "每一副眼镜，都是艺术品"
    ],
    "视力训练": [
        "孩子近视不用慌，科学训练有方法",
        "每天20分钟，3个月见效",
        "黑科技训练仪，近视防控新选择"
    ],
    "店铺环境": [
        "温馨环境，专业服务",
        "视元堂，您身边的视力管家",
        "专业验光配镜，就在您身边"
    ]
}

def create_promo_image(photo_path, title, subtitle, output_path):
    """生成爆款宣传图"""
    from PIL import ImageDraw
    
    # 加载照片
    photo = Image.open(photo_path)
    
    # 创建画布 (1080x1920)
    canvas = Image.new('RGB', (1080, 1920), DEEP_BLUE)
    draw = ImageDraw.Draw(canvas)
    
    # 照片区域 (全屏填充)
    target_width = 1080
    target_height = 1400
    
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
    
    # 圆角处理
    from PIL import ImageDraw
    mask = Image.new('L', (target_width, target_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (target_width, target_height)], radius=30, fill=255)
    
    # 创建带alpha通道的照片副本
    photo_rgba = photo.convert('RGBA')
    photo_rgba.putalpha(mask)
    
    canvas.paste(photo_rgba, (0, 100), photo_rgba)
    
    # 标题区域
    title_font = ImageFont.truetype(FONT_BOLD, 56)
    subtitle_font = ImageFont.truetype(FONT_BOLD, 36)
    
    # 标题背景
    draw.rectangle([(0, 1520), (1080, 1650)], fill=(30, 58, 138))
    
    # 主标题
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((1080 - title_width) // 2, 1540), title, fill=WHITE, font=title_font)
    
    # 副标题
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((1080 - subtitle_width) // 2, 1610), subtitle, fill=GOLD, font=subtitle_font)
    
    # 底部信息
    info_font = ImageFont.truetype(FONT_PATH, 28)
    
    draw.text((540, 1700), "视元堂视觉体验中心", fill=GOLD, font=info_font, anchor="mm")
    draw.text((540, 1750), "📍 南充顺庆区白土坝路406号", fill=WHITE, font=info_font, anchor="mm")
    draw.text((540, 1800), "📞 0817-2255222", fill=BLUE_BORDER, font=info_font, anchor="mm")
    draw.text((540, 1850), "专业验光配镜 | 儿童近视防控 | 视力训练", fill=WHITE, font=info_font, anchor="mm")
    
    canvas.save(output_path)
    return output_path

async def generate_video(photos, subtitles, voiceover_text, output_path):
    """生成爆款视频"""
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
    
    # 生成配音
    voice_path = output_path.replace('.mp4', '_voice.mp3')
    communicate = edge_tts.Communicate(voiceover_text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(voice_path)
    
    voice = AudioFileClip(voice_path)
    duration = voice.duration
    photo_duration = duration / len(photos)
    
    # 创建照片片段
    clips = []
    for i, (photo_path, subtitle) in enumerate(zip(photos, subtitles)):
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
        
        # 添加字幕
        draw = ImageDraw.Draw(photo)
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
        
        temp_path = output_path.replace('.mp4', f'_frame_{i}.jpg')
        photo.save(temp_path)
        
        clip = ImageClip(temp_path, duration=photo_duration)
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
    
    logo_frame_path = output_path.replace('.mp4', '_logo.jpg')
    logo_frame.save(logo_frame_path)
    
    logo_clip = ImageClip(logo_frame_path, duration=3)
    
    # 合并主视频和结尾
    final_video = concatenate_videoclips([main_video, logo_clip])
    
    # 合成音频
    bgm = AudioFileClip(BGM_PATH)
    voice_duration = min(voice.duration, main_video.duration)
    bgm = bgm.subclipped(0, min(bgm.duration, voice_duration))
    bgm = bgm.with_volume_scaled(0.3)
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
    
    return output_path

async def main():
    print("=" * 60)
    print("🎬 视元堂每日宣传内容生成器")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # ============ 生成图片 (6-8张) ============
    print("\n📸 生成爆款图片...")
    
    images = []
    
    # 1. 验光设备图片 (1-2张)
    yanguang_photos = [
        f"{PHOTO_BASE}/一楼验光设备/验光设备_1.jpg",
        f"{PHOTO_BASE}/一楼验光设备/验光设备_2.jpg"
    ]
    for i, photo in enumerate(yanguang_photos[:2]):
        if os.path.exists(photo):
            output = f"{OUTPUT_DIR}/爆款_验光设备_{i+1}.jpg"
            create_promo_image(photo, "专业验光", CAPTIONS["验光设备"][i % 3], output)
            images.append(output)
            print(f"  ✅ 验光设备图片 {i+1}")
    
    # 2. 配镜设备图片 (1-2张)
    peijing_photos = [
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_1.jpg",
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_2.jpg"
    ]
    for i, photo in enumerate(peijing_photos[:2]):
        if os.path.exists(photo):
            output = f"{OUTPUT_DIR}/爆款_配镜设备_{i+1}.jpg"
            create_promo_image(photo, "精湛配镜", CAPTIONS["配镜设备"][i % 3], output)
            images.append(output)
            print(f"  ✅ 配镜设备图片 {i+1}")
    
    # 3. 视力训练图片 (1-2张)
    xunlian_photos = [
        f"{PHOTO_BASE}/二楼训练设备/训练设备_1.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_2.jpg"
    ]
    for i, photo in enumerate(xunlian_photos[:2]):
        if os.path.exists(photo):
            output = f"{OUTPUT_DIR}/爆款_视力训练_{i+1}.jpg"
            create_promo_image(photo, "视力训练", CAPTIONS["视力训练"][i % 3], output)
            images.append(output)
            print(f"  ✅ 视力训练图片 {i+1}")
    
    # 4. 店铺环境图片 (1-2张)
    huanjing_photos = [
        f"{PHOTO_BASE}/一楼环境/一楼环境_1.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_2.jpg"
    ]
    for i, photo in enumerate(huanjing_photos[:2]):
        if os.path.exists(photo):
            output = f"{OUTPUT_DIR}/爆款_店铺环境_{i+1}.jpg"
            create_promo_image(photo, "专业环境", CAPTIONS["店铺环境"][i % 3], output)
            images.append(output)
            print(f"  ✅ 店铺环境图片 {i+1}")
    
    print(f"\n✅ 共生成 {len(images)} 张爆款图片")
    
    # ============ 生成视频 (3-5条) ============
    print("\n🎬 生成爆款视频...")
    
    videos = []
    
    # 1. 验光视频
    video_photos = [
        f"{PHOTO_BASE}/一楼验光设备/验光设备_1.jpg",
        f"{PHOTO_BASE}/一楼验光设备/验光设备_2.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_3.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/爆款_验光视频.mp4"
        subtitles = ["专业验光设备", "精准检测每一度", "科学配镜更舒适"]
        voiceover = "专业验光，精准配镜。视元堂引进进口验光设备，科学检测，让每一副眼镜都舒适。视元堂视觉体验中心，电话0817-2255222。"
        await generate_video(video_photos[:3], subtitles[:3], voiceover, output)
        videos.append(output)
        print(f"  ✅ 验光视频")
    
    # 2. 配镜视频
    video_photos = [
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_1.jpg",
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_2.jpg",
        f"{PHOTO_BASE}/二楼配镜设备/配镜设备_3.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/爆款_配镜视频.mp4"
        subtitles = ["德国进口设备", "精湛加工工艺", "立等可取"]
        voiceover = "现场加工，立等可取。视元堂配备德国进口配镜设备，精湛工艺，让每一副眼镜都是艺术品。视元堂视觉体验中心，电话0817-2255222。"
        await generate_video(video_photos[:3], subtitles[:3], voiceover, output)
        videos.append(output)
        print(f"  ✅ 配镜视频")
    
    # 3. 视力训练视频
    video_photos = [
        f"{PHOTO_BASE}/二楼训练设备/训练设备_1.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_2.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_3.jpg",
        f"{PHOTO_BASE}/二楼训练设备/训练设备_4.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/爆款_训练视频.mp4"
        subtitles = ["黑科技训练仪", "孩子近视不用慌", "每天20分钟见效", "科学训练有方法"]
        voiceover = "孩子近视不用慌，科学训练有方法。视元堂引进黑科技训练仪，每天20分钟，3个月见效。视元堂视觉体验中心，电话0817-2255222。"
        await generate_video(video_photos[:4], subtitles[:4], voiceover, output)
        videos.append(output)
        print(f"  ✅ 训练视频")
    
    # 4. 店铺环境视频
    video_photos = [
        f"{PHOTO_BASE}/一楼环境/一楼环境_1.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_2.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_3.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_4.jpg",
        f"{PHOTO_BASE}/一楼环境/一楼环境_5.jpg"
    ]
    video_photos = [p for p in video_photos if os.path.exists(p)]
    if len(video_photos) >= 3:
        output = f"{OUTPUT_DIR}/爆款_环境视频.mp4"
        subtitles = ["温馨专业环境", "进口验光设备", "品牌镜片展示", "荣誉资质墙", "您身边的视力管家"]
        voiceover = "温馨环境，专业服务。视元堂视觉体验中心，您身边的视力管家。专业验光配镜，儿童近视防控，视力训练。电话0817-2255222。"
        await generate_video(video_photos[:5], subtitles[:5], voiceover, output)
        videos.append(output)
        print(f"  ✅ 环境视频")
    
    print(f"\n✅ 共生成 {len(videos)} 条爆款视频")
    
    print("\n" + "=" * 60)
    print("✅ 全部完成！")
    print(f"📸 图片: {len(images)} 张")
    print(f"🎬 视频: {len(videos)} 条")
    print("=" * 60)
    
    return images, videos

if __name__ == "__main__":
    asyncio.run(main())

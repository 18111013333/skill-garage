#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视元堂宣传视频生成器 V2
生成日期：2026-04-13
"""

import os
import subprocess
import asyncio
import edge_tts
from datetime import datetime

# ==================== 配置 ====================
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/memory/shiyuantang_marketing/宣传图/2026-04-13")
PHOTO_DIR = os.path.expanduser("~/.openclaw/workspace/memory/shiyuantang_photos_new")
VIDEO_OUTPUT = os.path.expanduser("~/.openclaw/workspace/generated-videos")

# 确保视频输出目录存在
os.makedirs(VIDEO_OUTPUT, exist_ok=True)

# ==================== 视频配置 ====================
VIDEOS = [
    {
        "name": "视元堂店铺环境展示",
        "photos": [
            os.path.join(PHOTO_DIR, "店铺环境_门头照片2.jpg"),
            os.path.join(PHOTO_DIR, "店铺环境_前台.jpg"),
            os.path.join(PHOTO_DIR, "店铺环境_店内场景1.jpg"),
        ],
        "narration": "视元堂眼视光中心，位于南充顺庆区白土坝路406号。专业验光配镜15年，服务南充10万加客户。200平米专业空间，舒适环境，品质保证。",
        "output": "视频_店铺环境.mp4"
    },
    {
        "name": "专业验光设备展示",
        "photos": [
            os.path.join(PHOTO_DIR, "验光设备_综合验光仪.jpg"),
            os.path.join(PHOTO_DIR, "验光设备_检查视力设备.jpg"),
            os.path.join(PHOTO_DIR, "验光设备_视力表.jpg"),
        ],
        "narration": "SUPER VISION RM-160专业验光仪，一台设备30万，只为测准你的度数。持证验光师一对一服务，精准到1度。儿童视力筛查，早发现早干预。",
        "output": "视频_验光设备.mp4"
    },
    {
        "name": "全自动配镜设备展示",
        "photos": [
            os.path.join(PHOTO_DIR, "配镜设备_全自动磨边机ALE903.jpg"),
            os.path.join(PHOTO_DIR, "配镜设备_配镜工作台.jpg"),
            os.path.join(PHOTO_DIR, "配镜设备_镜片中心仪.jpg"),
        ],
        "narration": "ALE-903全自动磨边机，镜片加工0误差。JT-718镜片中心仪，精准定位光学中心。从验光到磨边，一条龙专业配镜，当天验光当天取镜。",
        "output": "视频_配镜设备.mp4"
    }
]

# ==================== 生成配音 ====================
async def generate_audio(text, output_path):
    """使用 edge_tts 生成配音"""
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_path)

# ==================== 生成视频函数 ====================
def generate_video(video_config):
    """生成单个视频"""
    print(f"\n🎬 生成视频: {video_config['name']}")
    
    # 1. 生成配音
    audio_path = os.path.join(OUTPUT_DIR, f"audio_{video_config['output'].replace('.mp4', '.mp3')}")
    print(f"   🎙️ 生成配音...")
    
    try:
        asyncio.run(generate_audio(video_config["narration"], audio_path))
        print(f"   ✅ 配音已生成: {audio_path}")
    except Exception as e:
        print(f"   ❌ 配音生成失败: {e}")
        return None
    
    # 2. 获取配音时长
    probe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    
    try:
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        print(f"   ⏱️ 配音时长: {duration:.2f}秒")
    except Exception as e:
        print(f"   ❌ 获取配音时长失败: {e}")
        duration = 15  # 默认15秒
    
    # 3. 计算每张照片的时长
    photo_count = len(video_config["photos"])
    photo_duration = duration / photo_count
    
    # 4. 创建视频（使用 ffmpeg）
    output_path = os.path.join(VIDEO_OUTPUT, video_config["output"])
    print(f"   🎥 合成视频...")
    
    # 创建临时文件列表
    concat_list = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_list, 'w') as f:
        for photo in video_config["photos"]:
            if os.path.exists(photo):
                f.write(f"file '{photo}'\n")
                f.write(f"duration {photo_duration}\n")
        # 最后一张照片需要再写一次（ffmpeg要求）
        if video_config["photos"]:
            f.write(f"file '{video_config['photos'][-1]}'\n")
    
    # 使用 ffmpeg 合成视频
    video_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-i", audio_path,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    try:
        subprocess.run(video_cmd, check=True, capture_output=True)
        print(f"   ✅ 视频已生成: {output_path}")
        return output_path
    except Exception as e:
        print(f"   ❌ 视频合成失败: {e}")
        return None

# ==================== 主函数 ====================
def main():
    """主函数"""
    print("=" * 60)
    print("🎬 视元堂宣传视频生成器 V2")
    print("=" * 60)
    
    generated_videos = []
    
    for video_config in VIDEOS:
        video_path = generate_video(video_config)
        if video_path:
            generated_videos.append(video_path)
    
    print("\n" + "=" * 60)
    print(f"✅ 视频生成完成！共生成 {len(generated_videos)} 个视频")
    print("=" * 60)
    
    return generated_videos

if __name__ == "__main__":
    main()

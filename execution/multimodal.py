#!/usr/bin/env python3
"""
多模态能力模块
支持图像、音频、视频处理
"""

import os
import json
import base64
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class MediaAsset:
    """媒体资产"""
    id: str
    type: str  # image, audio, video
    path: str
    description: str
    metadata: Dict
    created_at: str
    embedding: Optional[List[float]] = None


class MultiModalEngine:
    """多模态引擎"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(
                os.path.dirname(__file__),
                'multimodal_assets'
            )
        
        self.storage_dir = storage_dir
        self.assets_file = os.path.join(storage_dir, 'assets.json')
        self.assets: Dict[str, MediaAsset] = {}
        
        os.makedirs(storage_dir, exist_ok=True)
        self._load_assets()
        
        print(f"多模态引擎初始化完成")
        print(f"  - 存储目录: {storage_dir}")
        print(f"  - 资产数量: {len(self.assets)}")
    
    def _load_assets(self):
        """加载资产索引"""
        if os.path.exists(self.assets_file):
            with open(self.assets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for asset_data in data.get('assets', []):
                asset = MediaAsset(
                    id=asset_data['id'],
                    type=asset_data['type'],
                    path=asset_data['path'],
                    description=asset_data['description'],
                    metadata=asset_data['metadata'],
                    created_at=asset_data['created_at'],
                    embedding=asset_data.get('embedding')
                )
                self.assets[asset.id] = asset
    
    def _save_assets(self):
        """保存资产索引"""
        data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'assets': [asdict(asset) for asset in self.assets.values()]
        }
        
        with open(self.assets_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self, content: bytes) -> str:
        """生成唯一 ID"""
        return hashlib.md5(content).hexdigest()[:16]
    
    def add_image(self, image_path: str, description: str = "") -> MediaAsset:
        """添加图像"""
        with open(image_path, 'rb') as f:
            content = f.read()
        
        asset_id = self._generate_id(content)
        
        # 获取图像信息
        metadata = {
            'size': len(content),
            'format': os.path.splitext(image_path)[1]
        }
        
        # 尝试获取图像尺寸
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['mode'] = img.mode
        except:
            pass
        
        asset = MediaAsset(
            id=asset_id,
            type='image',
            path=image_path,
            description=description or f"图像 {asset_id}",
            metadata=metadata,
            created_at=datetime.now().isoformat()
        )
        
        self.assets[asset_id] = asset
        self._save_assets()
        
        print(f"添加图像: {asset_id}")
        return asset
    
    def add_audio(self, audio_path: str, description: str = "") -> MediaAsset:
        """添加音频"""
        with open(audio_path, 'rb') as f:
            content = f.read()
        
        asset_id = self._generate_id(content)
        
        metadata = {
            'size': len(content),
            'format': os.path.splitext(audio_path)[1]
        }
        
        asset = MediaAsset(
            id=asset_id,
            type='audio',
            path=audio_path,
            description=description or f"音频 {asset_id}",
            metadata=metadata,
            created_at=datetime.now().isoformat()
        )
        
        self.assets[asset_id] = asset
        self._save_assets()
        
        print(f"添加音频: {asset_id}")
        return asset
    
    def add_video(self, video_path: str, description: str = "") -> MediaAsset:
        """添加视频"""
        with open(video_path, 'rb') as f:
            content = f.read()
        
        asset_id = self._generate_id(content)
        
        metadata = {
            'size': len(content),
            'format': os.path.splitext(video_path)[1]
        }
        
        asset = MediaAsset(
            id=asset_id,
            type='video',
            path=video_path,
            description=description or f"视频 {asset_id}",
            metadata=metadata,
            created_at=datetime.now().isoformat()
        )
        
        self.assets[asset_id] = asset
        self._save_assets()
        
        print(f"添加视频: {asset_id}")
        return asset
    
    def search(self, query: str, asset_type: str = None) -> List[MediaAsset]:
        """搜索资产"""
        results = []
        
        for asset in self.assets.values():
            # 类型过滤
            if asset_type and asset.type != asset_type:
                continue
            
            # 描述匹配
            if query.lower() in asset.description.lower():
                results.append(asset)
        
        return results
    
    def get_by_type(self, asset_type: str) -> List[MediaAsset]:
        """按类型获取资产"""
        return [a for a in self.assets.values() if a.type == asset_type]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        type_counts = {}
        for asset in self.assets.values():
            type_counts[asset.type] = type_counts.get(asset.type, 0) + 1
        
        return {
            'total_assets': len(self.assets),
            'by_type': type_counts,
            'storage_dir': self.storage_dir
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    engine = MultiModalEngine()
    
    if len(sys.argv) < 2:
        print("用法: python multimodal.py <command>")
        print("命令: stats, list, search <query>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'stats':
        stats = engine.get_stats()
        print("\n多模态资产统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    elif command == 'list':
        print("\n资产列表:")
        print("-" * 60)
        for asset in engine.assets.values():
            print(f"  [{asset.type}] {asset.id}: {asset.description[:30]}")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("请输入搜索查询")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        results = engine.search(query)
        
        print(f"\n搜索结果 ({len(results)} 条):")
        print("-" * 60)
        for asset in results:
            print(f"  [{asset.type}] {asset.id}: {asset.description[:30]}")
    
    else:
        print(f"未知命令: {command}")

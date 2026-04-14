#!/usr/bin/env python3
"""
分布式增强模块
实时同步、冲突解决、离线支持
"""

import os
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class SyncConflict:
    """同步冲突"""
    id: str
    item_id: str
    local_version: str
    remote_version: str
    detected_at: str
    resolved: bool = False
    resolution: str = ""


@dataclass
class OfflineQueue:
    """离线队列"""
    id: str
    action: str
    data: Dict
    created_at: str
    synced: bool = False


class DistributedEnhanced:
    """分布式增强管理器"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(
                os.path.dirname(__file__),
                'distributed_enhanced'
            )
        
        self.config_dir = config_dir
        self.conflicts_file = os.path.join(config_dir, 'conflicts.json')
        self.offline_file = os.path.join(config_dir, 'offline_queue.json')
        
        self.conflicts: Dict[str, SyncConflict] = {}
        self.offline_queue: Dict[str, OfflineQueue] = {}
        self.sync_status = 'online'
        
        os.makedirs(config_dir, exist_ok=True)
        self._load_data()
        
        print(f"分布式增强管理器初始化完成")
        print(f"  - 冲突数量: {len(self.conflicts)}")
        print(f"  - 离线队列: {len(self.offline_queue)}")
    
    def _load_data(self):
        """加载数据"""
        # 加载冲突
        if os.path.exists(self.conflicts_file):
            with open(self.conflicts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for conflict_data in data.get('conflicts', []):
                conflict = SyncConflict(
                    id=conflict_data['id'],
                    item_id=conflict_data['item_id'],
                    local_version=conflict_data['local_version'],
                    remote_version=conflict_data['remote_version'],
                    detected_at=conflict_data['detected_at'],
                    resolved=conflict_data.get('resolved', False),
                    resolution=conflict_data.get('resolution', '')
                )
                self.conflicts[conflict.id] = conflict
        
        # 加载离线队列
        if os.path.exists(self.offline_file):
            with open(self.offline_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item_data in data.get('items', []):
                item = OfflineQueue(
                    id=item_data['id'],
                    action=item_data['action'],
                    data=item_data['data'],
                    created_at=item_data['created_at'],
                    synced=item_data.get('synced', False)
                )
                self.offline_queue[item.id] = item
    
    def _save_data(self):
        """保存数据"""
        # 保存冲突
        conflicts_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'conflicts': [asdict(c) for c in self.conflicts.values()]
        }
        
        with open(self.conflicts_file, 'w', encoding='utf-8') as f:
            json.dump(conflicts_data, f, ensure_ascii=False, indent=2)
        
        # 保存离线队列
        offline_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'items': [asdict(i) for i in self.offline_queue.values()]
        }
        
        with open(self.offline_file, 'w', encoding='utf-8') as f:
            json.dump(offline_data, f, ensure_ascii=False, indent=2)
    
    def detect_conflict(self, item_id: str, local: str, remote: str) -> Optional[SyncConflict]:
        """检测冲突"""
        if local == remote:
            return None
        
        conflict_id = hashlib.md5(f"{item_id}{time.time()}".encode()).hexdigest()[:16]
        
        conflict = SyncConflict(
            id=conflict_id,
            item_id=item_id,
            local_version=local,
            remote_version=remote,
            detected_at=datetime.now().isoformat()
        )
        
        self.conflicts[conflict_id] = conflict
        self._save_data()
        
        print(f"检测到冲突: {item_id}")
        return conflict
    
    def resolve_conflict(self, conflict_id: str, resolution: str) -> bool:
        """解决冲突"""
        if conflict_id not in self.conflicts:
            return False
        
        conflict = self.conflicts[conflict_id]
        conflict.resolved = True
        conflict.resolution = resolution
        self._save_data()
        
        print(f"冲突已解决: {conflict_id} ({resolution})")
        return True
    
    def add_offline_action(self, action: str, data: Dict) -> OfflineQueue:
        """添加离线操作"""
        item_id = hashlib.md5(f"{action}{time.time()}".encode()).hexdigest()[:16]
        
        item = OfflineQueue(
            id=item_id,
            action=action,
            data=data,
            created_at=datetime.now().isoformat()
        )
        
        self.offline_queue[item_id] = item
        self._save_data()
        
        print(f"添加离线操作: {action}")
        return item
    
    def sync_offline_queue(self) -> Dict:
        """同步离线队列"""
        synced = 0
        failed = 0
        
        for item in self.offline_queue.values():
            if not item.synced:
                # 模拟同步
                try:
                    item.synced = True
                    synced += 1
                except:
                    failed += 1
        
        self._save_data()
        
        return {
            'synced': synced,
            'failed': failed,
            'total': len(self.offline_queue)
        }
    
    def set_status(self, status: str):
        """设置同步状态"""
        self.sync_status = status
        print(f"同步状态: {status}")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        resolved = sum(1 for c in self.conflicts.values() if c.resolved)
        pending = sum(1 for i in self.offline_queue.values() if not i.synced)
        
        return {
            'sync_status': self.sync_status,
            'total_conflicts': len(self.conflicts),
            'resolved_conflicts': resolved,
            'pending_conflicts': len(self.conflicts) - resolved,
            'offline_queue': len(self.offline_queue),
            'pending_sync': pending
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    manager = DistributedEnhanced()
    
    if len(sys.argv) < 2:
        print("用法: python distributed_enhanced.py <command>")
        print("命令: conflicts, offline, sync, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'conflicts':
        print("\n同步冲突:")
        print("-" * 60)
        for conflict in manager.conflicts.values():
            status = "✅" if conflict.resolved else "⚠️"
            print(f"{status} {conflict.item_id}: {conflict.resolution or '未解决'}")
    
    elif command == 'offline':
        print("\n离线队列:")
        print("-" * 60)
        for item in manager.offline_queue.values():
            status = "✅" if item.synced else "⏳"
            print(f"{status} {item.action}: {item.created_at}")
    
    elif command == 'sync':
        result = manager.sync_offline_queue()
        print(f"\n同步结果: {result}")
    
    elif command == 'stats':
        stats = manager.get_stats()
        print("\n分布式增强统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

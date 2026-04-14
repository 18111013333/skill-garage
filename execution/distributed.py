#!/usr/bin/env python3
"""
分布式协同模块
支持跨设备数据同步、状态管理
"""

import os
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Device:
    """设备"""
    id: str
    name: str
    type: str  # desktop, mobile, server
    status: str  # online, offline
    last_sync: str
    capabilities: List[str]


@dataclass
class SyncItem:
    """同步项"""
    id: str
    type: str  # memory, config, file
    content: str
    checksum: str
    updated_at: str
    synced_devices: List[str]


class DistributedManager:
    """分布式管理器"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(
                os.path.dirname(__file__),
                'distributed'
            )
        
        self.data_dir = data_dir
        self.devices_file = os.path.join(data_dir, 'devices.json')
        self.sync_file = os.path.join(data_dir, 'sync_queue.json')
        
        self.devices: Dict[str, Device] = {}
        self.sync_queue: Dict[str, SyncItem] = {}
        self.local_device_id = self._get_local_device_id()
        
        os.makedirs(data_dir, exist_ok=True)
        self._load_data()
        
        print(f"分布式管理器初始化完成")
        print(f"  - 本地设备: {self.local_device_id}")
        print(f"  - 已注册设备: {len(self.devices)}")
        print(f"  - 同步队列: {len(self.sync_queue)}")
    
    def _get_local_device_id(self) -> str:
        """获取本地设备 ID"""
        # 基于主机名生成唯一 ID
        import socket
        hostname = socket.gethostname()
        return hashlib.md5(hostname.encode()).hexdigest()[:16]
    
    def _load_data(self):
        """加载数据"""
        # 加载设备
        if os.path.exists(self.devices_file):
            with open(self.devices_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for device_data in data.get('devices', []):
                device = Device(
                    id=device_data['id'],
                    name=device_data['name'],
                    type=device_data['type'],
                    status=device_data['status'],
                    last_sync=device_data['last_sync'],
                    capabilities=device_data['capabilities']
                )
                self.devices[device.id] = device
        
        # 加载同步队列
        if os.path.exists(self.sync_file):
            with open(self.sync_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item_data in data.get('items', []):
                item = SyncItem(
                    id=item_data['id'],
                    type=item_data['type'],
                    content=item_data['content'],
                    checksum=item_data['checksum'],
                    updated_at=item_data['updated_at'],
                    synced_devices=item_data['synced_devices']
                )
                self.sync_queue[item.id] = item
    
    def _save_data(self):
        """保存数据"""
        # 保存设备
        devices_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'devices': [asdict(device) for device in self.devices.values()]
        }
        
        with open(self.devices_file, 'w', encoding='utf-8') as f:
            json.dump(devices_data, f, ensure_ascii=False, indent=2)
        
        # 保存同步队列
        sync_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'items': [asdict(item) for item in self.sync_queue.values()]
        }
        
        with open(self.sync_file, 'w', encoding='utf-8') as f:
            json.dump(sync_data, f, ensure_ascii=False, indent=2)
    
    def register_device(self, device: Device) -> bool:
        """注册设备"""
        if device.id in self.devices:
            print(f"设备 {device.id} 已存在")
            return False
        
        self.devices[device.id] = device
        self._save_data()
        
        print(f"注册设备: {device.name} ({device.type})")
        return True
    
    def unregister_device(self, device_id: str) -> bool:
        """注销设备"""
        if device_id not in self.devices:
            print(f"设备 {device_id} 不存在")
            return False
        
        del self.devices[device_id]
        self._save_data()
        
        print(f"注销设备: {device_id}")
        return True
    
    def add_to_sync(self, item_type: str, content: str) -> SyncItem:
        """添加到同步队列"""
        checksum = hashlib.md5(content.encode()).hexdigest()
        item_id = hashlib.md5(f"{item_type}:{content}".encode()).hexdigest()[:16]
        
        item = SyncItem(
            id=item_id,
            type=item_type,
            content=content,
            checksum=checksum,
            updated_at=datetime.now().isoformat(),
            synced_devices=[self.local_device_id]
        )
        
        self.sync_queue[item_id] = item
        self._save_data()
        
        print(f"添加同步项: {item_type} ({item_id})")
        return item
    
    def sync_with_device(self, device_id: str) -> Dict:
        """与设备同步"""
        if device_id not in self.devices:
            print(f"设备 {device_id} 不存在")
            return {'success': False, 'error': 'device_not_found'}
        
        device = self.devices[device_id]
        
        if device.status != 'online':
            print(f"设备 {device.name} 离线")
            return {'success': False, 'error': 'device_offline'}
        
        print(f"与 {device.name} 同步...")
        
        # 模拟同步过程
        synced_items = 0
        for item in self.sync_queue.values():
            if device_id not in item.synced_devices:
                # 模拟发送数据
                item.synced_devices.append(device_id)
                synced_items += 1
        
        # 更新设备最后同步时间
        device.last_sync = datetime.now().isoformat()
        self._save_data()
        
        print(f"同步完成: {synced_items} 项")
        return {
            'success': True,
            'synced_items': synced_items,
            'device': device.name
        }
    
    def get_online_devices(self) -> List[Device]:
        """获取在线设备"""
        return [d for d in self.devices.values() if d.status == 'online']
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        online = sum(1 for d in self.devices.values() if d.status == 'online')
        pending_sync = sum(1 for item in self.sync_queue.values() 
                          if len(item.synced_devices) < len(self.devices))
        
        return {
            'total_devices': len(self.devices),
            'online_devices': online,
            'offline_devices': len(self.devices) - online,
            'sync_queue_size': len(self.sync_queue),
            'pending_sync': pending_sync
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    manager = DistributedManager()
    
    # 注册本地设备
    local_device = Device(
        id=manager.local_device_id,
        name='本地设备',
        type='server',
        status='online',
        last_sync=datetime.now().isoformat(),
        capabilities=['memory', 'compute', 'storage']
    )
    
    if manager.local_device_id not in manager.devices:
        manager.register_device(local_device)
    
    if len(sys.argv) < 2:
        print("用法: python distributed.py <command>")
        print("命令: devices, sync <device_id>, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'devices':
        print("\n设备列表:")
        print("-" * 60)
        for device in manager.devices.values():
            status = "🟢" if device.status == 'online' else "🔴"
            print(f"{status} {device.name} ({device.type}): {device.last_sync}")
    
    elif command == 'sync':
        if len(sys.argv) < 3:
            print("请指定设备 ID")
            sys.exit(1)
        result = manager.sync_with_device(sys.argv[2])
        print(f"同步结果: {result}")
    
    elif command == 'stats':
        stats = manager.get_stats()
        print("\n分布式统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

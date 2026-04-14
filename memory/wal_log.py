#!/usr/bin/env python3
"""
WAL日志系统 - 基于小艺Claw技术优化
Write-Ahead Logging 预写日志实现
"""

import os
import json
import time
import threading
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

# 配置
MEMORY_DIR = os.path.dirname(os.path.abspath(__file__))
WAL_DIR = os.path.join(MEMORY_DIR, 'wal_logs')
os.makedirs(WAL_DIR, exist_ok=True)


class WALEntryType(Enum):
    """WAL条目类型"""
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    CHECKPOINT = "CHECKPOINT"


@dataclass
class WALEntry:
    """WAL条目"""
    sequence: int          # 序列号
    timestamp: float       # 时间戳
    entry_type: str        # 条目类型
    table: str             # 表名
    key: str               # 键
    value: Any             # 值
    checksum: str = ""     # 校验和
    
    def compute_checksum(self) -> str:
        """计算校验和"""
        content = f"{self.sequence}{self.timestamp}{self.entry_type}{self.table}{self.key}{json.dumps(self.value)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def verify_checksum(self) -> bool:
        """验证校验和"""
        return self.checksum == self.compute_checksum()


class WALSystem:
    """
    WAL (Write-Ahead Logging) 系统
    
    特点：
    - 所有修改先写入日志，再应用到数据
    - 支持崩溃恢复
    - 支持检查点机制
    - 异步刷盘提高性能
    """
    
    def __init__(self, 
                 name: str = "default",
                 sync_interval: float = 0.1,  # 同步间隔（秒）
                 checkpoint_interval: int = 1000,  # 检查点间隔（条目数）
                 max_log_size: int = 10 * 1024 * 1024):  # 最大日志大小（字节）
        
        self.name = name
        self.sync_interval = sync_interval
        self.checkpoint_interval = checkpoint_interval
        self.max_log_size = max_log_size
        
        # 日志文件
        self.log_file = os.path.join(WAL_DIR, f"{name}.wal")
        self.checkpoint_file = os.path.join(WAL_DIR, f"{name}.checkpoint")
        
        # 内存缓冲
        self.buffer: List[WALEntry] = []
        self.buffer_lock = threading.Lock()
        
        # 序列号
        self.sequence = 0
        self._load_sequence()
        
        # 数据存储（模拟数据库）
        self.data: Dict[str, Dict[str, Any]] = {}
        
        # 同步线程
        self.sync_thread: Optional[threading.Thread] = None
        self.running = False
        
        # 统计
        self.stats = {
            'total_entries': 0,
            'total_checkpoints': 0,
            'total_recoveries': 0,
            'bytes_written': 0
        }
    
    def _load_sequence(self):
        """加载序列号"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                self.sequence = data.get('sequence', 0)
    
    def _save_sequence(self):
        """保存序列号"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({'sequence': self.sequence}, f)
    
    def start(self):
        """启动WAL系统"""
        # 恢复数据
        self._recover()
        
        # 启动同步线程
        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
    
    def stop(self):
        """停止WAL系统"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        
        # 最后一次同步
        self._sync_to_disk()
        
        # 保存检查点
        self._create_checkpoint()
    
    def _sync_loop(self):
        """同步循环"""
        while self.running:
            time.sleep(self.sync_interval)
            self._sync_to_disk()
    
    def _sync_to_disk(self):
        """同步到磁盘"""
        with self.buffer_lock:
            if not self.buffer:
                return
            
            entries = self.buffer.copy()
            self.buffer.clear()
        
        # 写入日志文件
        with open(self.log_file, 'a') as f:
            for entry in entries:
                line = json.dumps(asdict(entry)) + '\n'
                f.write(line)
                self.stats['bytes_written'] += len(line)
        
        self.stats['total_entries'] += len(entries)
        
        # 检查是否需要创建检查点
        if self.stats['total_entries'] % self.checkpoint_interval == 0:
            self._create_checkpoint()
    
    def _create_checkpoint(self):
        """创建检查点"""
        checkpoint = {
            'sequence': self.sequence,
            'timestamp': time.time(),
            'data': self.data,
            'stats': self.stats
        }
        
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)
        
        self.stats['total_checkpoints'] += 1
        
        # 清理旧日志
        self._rotate_log()
    
    def _rotate_log(self):
        """轮转日志"""
        if os.path.exists(self.log_file):
            log_size = os.path.getsize(self.log_file)
            if log_size > self.max_log_size:
                # 备份旧日志
                backup_file = f"{self.log_file}.{int(time.time())}"
                os.rename(self.log_file, backup_file)
    
    def _recover(self):
        """从WAL恢复数据"""
        # 先加载检查点
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                self.data = checkpoint.get('data', {})
                self.sequence = checkpoint.get('sequence', 0)
                self.stats = checkpoint.get('stats', self.stats)
        
        # 重放日志
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        entry_dict = json.loads(line.strip())
                        entry = WALEntry(**entry_dict)
                        
                        # 验证校验和
                        if entry.verify_checksum():
                            self._apply_entry(entry)
                    except Exception as e:
                        print(f"恢复条目失败: {e}")
            
            self.stats['total_recoveries'] += 1
    
    def _apply_entry(self, entry: WALEntry):
        """应用条目到数据"""
        if entry.table not in self.data:
            self.data[entry.table] = {}
        
        if entry.entry_type == WALEntryType.INSERT.value:
            self.data[entry.table][entry.key] = entry.value
        
        elif entry.entry_type == WALEntryType.UPDATE.value:
            if entry.key in self.data[entry.table]:
                self.data[entry.table][entry.key].update(entry.value)
            else:
                self.data[entry.table][entry.key] = entry.value
        
        elif entry.entry_type == WALEntryType.DELETE.value:
            if entry.key in self.data[entry.table]:
                del self.data[entry.table][entry.key]
    
    def _write_entry(self, entry_type: WALEntryType, table: str, key: str, value: Any):
        """写入WAL条目"""
        self.sequence += 1
        
        entry = WALEntry(
            sequence=self.sequence,
            timestamp=time.time(),
            entry_type=entry_type.value,
            table=table,
            key=key,
            value=value
        )
        entry.checksum = entry.compute_checksum()
        
        # 加入缓冲
        with self.buffer_lock:
            self.buffer.append(entry)
        
        # 应用到内存数据
        self._apply_entry(entry)
        
        return entry.sequence
    
    def insert(self, table: str, key: str, value: Any) -> int:
        """插入数据"""
        return self._write_entry(WALEntryType.INSERT, table, key, value)
    
    def update(self, table: str, key: str, value: Any) -> int:
        """更新数据"""
        return self._write_entry(WALEntryType.UPDATE, table, key, value)
    
    def delete(self, table: str, key: str) -> int:
        """删除数据"""
        return self._write_entry(WALEntryType.DELETE, table, key, None)
    
    def get(self, table: str, key: str) -> Optional[Any]:
        """获取数据"""
        if table in self.data and key in self.data[table]:
            return self.data[table][key]
        return None
    
    def get_table(self, table: str) -> Dict[str, Any]:
        """获取整表数据"""
        return self.data.get(table, {})
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            **self.stats,
            'buffer_size': len(self.buffer),
            'sequence': self.sequence,
            'tables': list(self.data.keys()),
            'total_keys': sum(len(t) for t in self.data.values())
        }


# 测试代码
if __name__ == '__main__':
    print("=== WAL日志系统测试 ===\n")
    
    # 创建WAL系统
    wal = WALSystem(name="test_wal")
    wal.start()
    
    # 插入数据
    print("插入数据...")
    for i in range(10):
        seq = wal.insert("memories", f"mem_{i}", {
            "content": f"记忆内容 {i}",
            "timestamp": time.time()
        })
        print(f"  插入 mem_{i}, 序列号: {seq}")
    
    # 更新数据
    print("\n更新数据...")
    wal.update("memories", "mem_0", {"content": "更新后的记忆内容 0"})
    
    # 查询数据
    print("\n查询数据...")
    data = wal.get("memories", "mem_0")
    print(f"  mem_0: {data}")
    
    # 统计信息
    print("\n=== WAL统计 ===")
    stats = wal.get_stats()
    print(json.dumps(stats, indent=2))
    
    # 停止WAL
    wal.stop()
    
    print("\nWAL日志系统测试完成！")
    print(f"日志文件: {wal.log_file}")
    print(f"检查点文件: {wal.checkpoint_file}")

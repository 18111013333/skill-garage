#!/usr/bin/env python3
"""
KV缓存系统 - 基于小艺收藏技术优化
支持LLM推理缓存、PagedAttention模拟、缓存淘汰
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import OrderedDict
import sqlite3

# 配置
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kv_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

KV_DB_PATH = os.path.join(CACHE_DIR, 'kv_cache.db')


@dataclass
class KVCacheEntry:
    """KV缓存条目"""
    cache_id: str
    prompt_hash: str
    prompt: str
    response: str
    model: str
    tokens_in: int
    tokens_out: int
    created_at: float
    last_access: float
    access_count: int
    size_bytes: int
    ttl: int  # 生存时间（秒），0表示永不过期


class KVCacheSystem:
    """KV缓存系统"""
    
    def __init__(self, max_memory_mb: int = 100, max_entries: int = 1000):
        self.max_memory = max_memory_mb * 1024 * 1024  # 转为字节
        self.max_entries = max_entries
        
        # 内存缓存（LRU）
        self.memory_cache: OrderedDict[str, KVCacheEntry] = OrderedDict()
        self.current_memory = 0
        
        # 数据库缓存
        self.conn = sqlite3.connect(KV_DB_PATH)
        self._init_db()
        
        # 统计信息
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    def _init_db(self):
        """初始化数据库"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS kv_cache (
                cache_id TEXT PRIMARY KEY,
                prompt_hash TEXT,
                prompt TEXT,
                response TEXT,
                model TEXT,
                tokens_in INTEGER,
                tokens_out INTEGER,
                created_at REAL,
                last_access REAL,
                access_count INTEGER,
                size_bytes INTEGER,
                ttl INTEGER
            )
        ''')
        
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_prompt_hash ON kv_cache(prompt_hash)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_last_access ON kv_cache(last_access)')
        
        self.conn.commit()
    
    def _hash_prompt(self, prompt: str, model: str = "") -> str:
        """计算提示词哈希"""
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()[:32]
    
    def _estimate_size(self, prompt: str, response: str) -> int:
        """估算缓存大小"""
        # 简单估算：字符数 * 4（UTF-8最大字节数）
        return len(prompt.encode('utf-8')) + len(response.encode('utf-8'))
    
    def _evict_lru(self, required_space: int = 0):
        """LRU淘汰"""
        while self.memory_cache and (
            self.current_memory + required_space > self.max_memory or
            len(self.memory_cache) >= self.max_entries
        ):
            # 移除最久未使用的条目
            cache_id, entry = self.memory_cache.popitem(last=False)
            self.current_memory -= entry.size_bytes
            self.stats['evictions'] += 1
            
            # 写入数据库（持久化）
            self._save_to_db(entry)
    
    def _save_to_db(self, entry: KVCacheEntry):
        """保存到数据库"""
        self.conn.execute('''
            INSERT OR REPLACE INTO kv_cache 
            (cache_id, prompt_hash, prompt, response, model, tokens_in, tokens_out,
             created_at, last_access, access_count, size_bytes, ttl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.cache_id, entry.prompt_hash, entry.prompt, entry.response,
            entry.model, entry.tokens_in, entry.tokens_out,
            entry.created_at, entry.last_access, entry.access_count,
            entry.size_bytes, entry.ttl
        ))
        self.conn.commit()
    
    def _load_from_db(self, prompt_hash: str) -> Optional[KVCacheEntry]:
        """从数据库加载"""
        cursor = self.conn.execute('''
            SELECT * FROM kv_cache WHERE prompt_hash = ?
        ''', (prompt_hash,))
        
        row = cursor.fetchone()
        if row:
            return KVCacheEntry(
                cache_id=row[0],
                prompt_hash=row[1],
                prompt=row[2],
                response=row[3],
                model=row[4],
                tokens_in=row[5],
                tokens_out=row[6],
                created_at=row[7],
                last_access=row[8],
                access_count=row[9],
                size_bytes=row[10],
                ttl=row[11]
            )
        return None
    
    def get(self, prompt: str, model: str = "") -> Optional[str]:
        """获取缓存"""
        prompt_hash = self._hash_prompt(prompt, model)
        
        # 检查内存缓存
        if prompt_hash in self.memory_cache:
            entry = self.memory_cache.pop(prompt_hash)
            
            # 检查是否过期
            if entry.ttl > 0 and time.time() - entry.created_at > entry.ttl:
                del entry
                self.stats['misses'] += 1
                return None
            
            # 更新访问信息
            entry.last_access = time.time()
            entry.access_count += 1
            
            # 移到末尾（最近使用）
            self.memory_cache[prompt_hash] = entry
            
            self.stats['hits'] += 1
            return entry.response
        
        # 检查数据库缓存
        entry = self._load_from_db(prompt_hash)
        if entry:
            # 检查是否过期
            if entry.ttl > 0 and time.time() - entry.created_at > entry.ttl:
                self.conn.execute('DELETE FROM kv_cache WHERE cache_id = ?', (entry.cache_id,))
                self.conn.commit()
                self.stats['misses'] += 1
                return None
            
            # 加载到内存缓存
            self._evict_lru(entry.size_bytes)
            self.memory_cache[prompt_hash] = entry
            self.current_memory += entry.size_bytes
            
            # 更新访问信息
            entry.last_access = time.time()
            entry.access_count += 1
            self._save_to_db(entry)
            
            self.stats['hits'] += 1
            return entry.response
        
        self.stats['misses'] += 1
        return None
    
    def set(self, prompt: str, response: str, model: str = "",
            tokens_in: int = 0, tokens_out: int = 0, ttl: int = 0):
        """设置缓存"""
        prompt_hash = self._hash_prompt(prompt, model)
        size_bytes = self._estimate_size(prompt, response)
        
        # 淘汰旧缓存
        self._evict_lru(size_bytes)
        
        # 创建缓存条目
        now = time.time()
        entry = KVCacheEntry(
            cache_id=prompt_hash,
            prompt_hash=prompt_hash,
            prompt=prompt,
            response=response,
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            created_at=now,
            last_access=now,
            access_count=1,
            size_bytes=size_bytes,
            ttl=ttl
        )
        
        # 存入内存缓存
        self.memory_cache[prompt_hash] = entry
        self.current_memory += size_bytes
        
        # 同时存入数据库
        self._save_to_db(entry)
    
    def invalidate(self, prompt: str, model: str = ""):
        """使缓存失效"""
        prompt_hash = self._hash_prompt(prompt, model)
        
        # 从内存移除
        if prompt_hash in self.memory_cache:
            entry = self.memory_cache.pop(prompt_hash)
            self.current_memory -= entry.size_bytes
        
        # 从数据库移除
        self.conn.execute('DELETE FROM kv_cache WHERE prompt_hash = ?', (prompt_hash,))
        self.conn.commit()
    
    def clear_expired(self):
        """清理过期缓存"""
        now = time.time()
        
        # 清理内存缓存
        expired = [
            h for h, e in self.memory_cache.items()
            if e.ttl > 0 and now - e.created_at > e.ttl
        ]
        for h in expired:
            entry = self.memory_cache.pop(h)
            self.current_memory -= entry.size_bytes
        
        # 清理数据库缓存
        self.conn.execute('''
            DELETE FROM kv_cache 
            WHERE ttl > 0 AND created_at < ?
        ''', (now - 3600,))  # 清理1小时前过期的
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
        
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate': f"{hit_rate:.2%}",
            'evictions': self.stats['evictions'],
            'memory_entries': len(self.memory_cache),
            'memory_usage_mb': self.current_memory / (1024 * 1024),
            'max_memory_mb': self.max_memory / (1024 * 1024)
        }
    
    def get_hot_prompts(self, top_k: int = 10) -> List[Dict]:
        """获取热门提示词"""
        cursor = self.conn.execute('''
            SELECT prompt, access_count, tokens_in, tokens_out
            FROM kv_cache
            ORDER BY access_count DESC
            LIMIT ?
        ''', (top_k,))
        
        return [
            {
                'prompt': row[0][:100] + '...' if len(row[0]) > 100 else row[0],
                'access_count': row[1],
                'tokens_in': row[2],
                'tokens_out': row[3]
            }
            for row in cursor.fetchall()
        ]
    
    def close(self):
        """关闭连接"""
        self.conn.close()


# 模拟FlashAttention的分块注意力计算
class FlashAttentionSimulator:
    """FlashAttention模拟器"""
    
    def __init__(self, block_size: int = 256):
        self.block_size = block_size
    
    def compute_attention(self, seq_len: int) -> Dict:
        """计算注意力复杂度"""
        # 标准注意力：O(N²) 内存
        standard_memory = seq_len * seq_len * 4  # float32
        
        # FlashAttention：O(N) 内存
        flash_memory = seq_len * self.block_size * 4
        
        # 计算次数
        standard_ops = seq_len * seq_len
        flash_ops = seq_len * seq_len  # 相同，但IO更少
        
        return {
            'seq_len': seq_len,
            'standard_memory_mb': standard_memory / (1024 * 1024),
            'flash_memory_mb': flash_memory / (1024 * 1024),
            'memory_reduction': f"{(1 - flash_memory / standard_memory):.2%}",
            'block_size': self.block_size
        }


# 测试代码
if __name__ == '__main__':
    print("=== KV缓存系统测试 ===\n")
    
    cache = KVCacheSystem(max_memory_mb=10, max_entries=100)
    
    # 测试缓存
    test_prompts = [
        ("你好，请介绍一下自己", "我是小太阳，老板陈飞的专属助手！"),
        ("老板是谁？", "老板是陈飞，四川南充人，出生于1981年。"),
        ("视元堂在哪里？", "视元堂眼视光中心位于南充顺庆区白土坝路406号。"),
        ("皇泽寺是什么？", "皇泽寺是中国唯一的女皇帝武则天祀庙，位于广元。"),
        ("径山寺禅修多少钱？", "径山寺禅修体验营人均1280元，3天2晚纯玩套餐。")
    ]
    
    # 设置缓存
    print("设置缓存...")
    for prompt, response in test_prompts:
        cache.set(prompt, response, "xiaoyi-llm", 
                  tokens_in=len(prompt), tokens_out=len(response))
    
    # 测试命中
    print("\n测试缓存命中...")
    for prompt, expected in test_prompts[:3]:
        result = cache.get(prompt, "xiaoyi-llm")
        status = "✓ 命中" if result == expected else "✗ 未命中"
        print(f"{status}: {prompt[:30]}...")
    
    # 测试未命中
    print("\n测试缓存未命中...")
    result = cache.get("这是一个新的问题", "xiaoyi-llm")
    print(f"结果: {'命中' if result else '未命中'}")
    
    # 统计信息
    print("\n=== 缓存统计 ===")
    stats = cache.get_stats()
    print(json.dumps(stats, indent=2))
    
    # 热门提示词
    print("\n=== 热门提示词 ===")
    hot = cache.get_hot_prompts(3)
    for i, item in enumerate(hot, 1):
        print(f"{i}. {item['prompt']} (访问{item['access_count']}次)")
    
    # FlashAttention测试
    print("\n=== FlashAttention模拟 ===")
    flash = FlashAttentionSimulator()
    for seq_len in [512, 1024, 2048, 4096, 8192]:
        result = flash.compute_attention(seq_len)
        print(f"序列长度{seq_len}: 内存减少{result['memory_reduction']}")
    
    cache.close()
    print("\nKV缓存系统测试完成！")

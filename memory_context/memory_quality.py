#!/usr/bin/env python3
"""
记忆质量治理 - V2.8.0

功能：
- 去重
- 重要性评分
- 冲突检测
- 长短期切换
- 可遗忘机制
- 历史摘要压缩
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass

from infrastructure.path_resolver import get_project_root, get_memory_dir

@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    timestamp: str
    importance: float
    category: str
    tags: List[str]
    access_count: int
    last_accessed: str

class MemoryQualityManager:
    """记忆质量管理器"""
    
    def __init__(self):
        self.memory_dir = get_memory_dir()
        self.project_root = get_project_root()
        self.short_memory_path = self.memory_dir / 'short.md'
        self.long_memory_path = self.memory_dir / 'long.md'
        self.quality_path = self.memory_dir / 'quality.json'
        
        self.entries: Dict[str, MemoryEntry] = {}
        self._load_quality_data()
    
    def _load_quality_data(self):
        """加载质量数据"""
        if self.quality_path.exists():
            data = json.loads(self.quality_path.read_text(encoding='utf-8'))
            for entry_data in data.get("entries", []):
                self.entries[entry_data["id"]] = MemoryEntry(**entry_data)
    
    def _save_quality_data(self):
        """保存质量数据"""
        self.quality_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "entries": [e.__dict__ for e in self.entries.values()],
            "updated": datetime.now().isoformat()
        }
        self.quality_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def _generate_id(self, content: str) -> str:
        """生成内容 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def deduplicate(self, content: str) -> Tuple[bool, Optional[str]]:
        """去重检查"""
        content_id = self._generate_id(content)
        
        for entry_id, entry in self.entries.items():
            if self._generate_id(entry.content) == content_id:
                return True, entry_id
        
        return False, None
    
    def calculate_importance(self, content: str, context: Dict = None) -> float:
        """计算重要性评分"""
        score = 0.5  # 基础分
        
        # 关键词加分
        important_keywords = [
            '决策', '重要', '关键', '必须', '禁止',
            'decision', 'important', 'critical', 'must', 'forbidden'
        ]
        for keyword in important_keywords:
            if keyword in content.lower():
                score += 0.1
        
        # 长度加分（信息量）
        if len(content) > 500:
            score += 0.1
        if len(content) > 1000:
            score += 0.1
        
        # 上下文加分
        if context:
            if context.get('user_emphasized'):
                score += 0.2
            if context.get('repeated'):
                score += 0.1
        
        return min(score, 1.0)
    
    def detect_conflicts(self, new_content: str) -> List[Dict]:
        """检测冲突"""
        conflicts = []
        
        for entry in self.entries.values():
            # 简单冲突检测：关键词相反
            conflict_pairs = [
                ('是', '不是'),
                ('对', '错'),
                ('允许', '禁止'),
                ('yes', 'no'),
                ('true', 'false')
            ]
            
            for pos, neg in conflict_pairs:
                if pos in new_content and neg in entry.content:
                    conflicts.append({
                        "existing_id": entry.id,
                        "existing_content": entry.content[:100],
                        "conflict_type": f"'{pos}' vs '{neg}'"
                    })
                if neg in new_content and pos in entry.content:
                    conflicts.append({
                        "existing_id": entry.id,
                        "existing_content": entry.content[:100],
                        "conflict_type": f"'{neg}' vs '{pos}'"
                    })
        
        return conflicts
    
    def should_promote_to_long(self, entry_id: str) -> bool:
        """判断是否应提升为长期记忆"""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        
        # 重要性高
        if entry.importance >= 0.8:
            return True
        
        # 访问次数多
        if entry.access_count >= 5:
            return True
        
        # 存在时间长且仍被访问
        created = datetime.fromisoformat(entry.timestamp)
        age_days = (datetime.now() - created).days
        if age_days >= 7 and entry.access_count >= 3:
            return True
        
        return False
    
    def should_forget(self, entry_id: str) -> bool:
        """判断是否应遗忘"""
        entry = self.entries.get(entry_id)
        if not entry:
            return False
        
        # 重要性低
        if entry.importance < 0.3:
            # 长期未访问
            last_access = datetime.fromisoformat(entry.last_accessed)
            days_inactive = (datetime.now() - last_access).days
            if days_inactive >= 30:
                return True
        
        return False
    
    def compress_history(self, days: int = 7) -> Dict[str, int]:
        """压缩历史记忆"""
        compressed = 0
        removed = 0
        
        cutoff = datetime.now() - timedelta(days=days)
        
        for entry_id, entry in list(self.entries.items()):
            created = datetime.fromisoformat(entry.timestamp)
            if created < cutoff:
                if entry.importance < 0.5 and entry.access_count < 2:
                    # 低价值，删除
                    del self.entries[entry_id]
                    removed += 1
                else:
                    # 高价值，标记为已压缩
                    entry.tags.append("compressed")
                    compressed += 1
        
        self._save_quality_data()
        
        return {"compressed": compressed, "removed": removed}
    
    def add_memory(self, content: str, category: str = "general", tags: List[str] = None) -> str:
        """添加记忆"""
        # 去重
        is_dup, dup_id = self.deduplicate(content)
        if is_dup:
            # 更新访问计数
            if dup_id in self.entries:
                self.entries[dup_id].access_count += 1
                self.entries[dup_id].last_accessed = datetime.now().isoformat()
            return dup_id
        
        # 检测冲突
        conflicts = self.detect_conflicts(content)
        if conflicts:
            # 记录冲突但不阻止添加
            pass
        
        # 计算重要性
        importance = self.calculate_importance(content)
        
        # 创建条目
        entry_id = self._generate_id(content)
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            timestamp=datetime.now().isoformat(),
            importance=importance,
            category=category,
            tags=tags or [],
            access_count=1,
            last_accessed=datetime.now().isoformat()
        )
        
        self.entries[entry_id] = entry
        self._save_quality_data()
        
        return entry_id

# 类型提示
from typing import Tuple

# 全局实例
_quality_manager = None

def get_memory_quality_manager() -> MemoryQualityManager:
    """获取全局记忆质量管理器"""
    global _quality_manager
    if _quality_manager is None:
        _quality_manager = MemoryQualityManager()
    return _quality_manager

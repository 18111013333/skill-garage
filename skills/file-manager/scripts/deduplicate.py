"""文件去重 - V4.3.1

兼容层：引用 infrastructure/shared/dedup.py
"""

from infrastructure.shared.dedup import UnifiedDedup, DedupConfig, get_dedup

FileDedup = UnifiedDedup

__all__ = ['UnifiedDedup', 'DedupConfig', 'get_dedup', 'FileDedup']

"""
L2_memory 性能集成
V2.7.0 - 2026-04-10

集成组件: layer_cache, zero_copy
"""

# 导入性能组件
from infrastructure.performance import cache_get, cache_set, share_data, get_shared

# 初始化
def init_performance():
    """初始化性能组件"""
    pass

# 导出
__all__ = [
    'get_shared'
]

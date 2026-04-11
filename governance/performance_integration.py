"""
L5_governance 性能集成
V2.7.0 - 2026-04-10

集成组件: performance_monitor
"""

# 导入性能组件
from infrastructure.performance import get_monitor

# 初始化
def init_performance():
    """初始化性能组件"""
    pass

# 导出
__all__ = [
    'get_monitor'
]

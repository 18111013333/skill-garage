"""搜索路由器 - V4.3.2

兼容层：引用 infrastructure/shared/router.py
"""

from infrastructure.shared.router import (
    UnifiedRouter, RouteMode, RouteResult, get_router, route
)

__all__ = ['UnifiedRouter', 'RouteMode', 'RouteResult', 'get_router', 'route']

#!/usr/bin/env python3
"""
北京时间插件
"""

from datetime import datetime, timezone, timedelta

def tool_main(arg: dict) -> str:
    """
    获取北京时间
    
    Args:
        arg: 输入参数（可选 format）
    
    Returns:
        str: 北京时间
    """
    format_str = arg.get("format", "%Y-%m-%d %H:%M:%S")
    
    # 北京时间 UTC+8
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.now(beijing_tz)
    
    return f"北京时间: {beijing_time.strftime(format_str)}"

#!/usr/bin/env python3
"""
sqlite-vec 扩展包装模块 (v5.2.19)
支持多种 SQLite 实现，用户可自行选择

安装建议：
- 需要向量搜索：pip install pysqlite3-binary
- 仅需基础功能：使用标准库 sqlite3 即可
"""

import os
from pathlib import Path
from typing import Any, Optional
import importlib

# sqlite-vec 扩展路径
VEC_EXTENSION_PATH = Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64" / "vec0.so"


def get_sqlite_module():
    """
    获取支持扩展加载的 SQLite 模块
    
    优先级：
    1. pysqlite3-binary（推荐）
    2. pysqlite3
    3. sqlite3（标准库，不支持扩展）
    
    Returns:
        sqlite3 模块
    """
    # 尝试 pysqlite3-binary
    try:
        from pysqlite3 import dbapi2 as sqlite3
        return sqlite3, True
    except ImportError:
        pass
    
    # 尝试 pysqlite3
    try:
        from pysqlite3 import dbapi2 as sqlite3
        return sqlite3, True
    except ImportError:
        pass
    
    # 回退到标准库
    import sqlite3
    return sqlite3, False


# 获取 SQLite 模块
sqlite3, SUPPORTS_EXTENSION = get_sqlite_module()


def connect(db_path: str, load_vec: bool = True) -> Any:
    """
    连接数据库并可选加载 sqlite-vec 扩展
    
    Args:
        db_path: 数据库文件路径
        load_vec: 是否加载 sqlite-vec 扩展
        
    Returns:
        数据库连接
    """
    # 展开路径
    db_path = os.path.expanduser(db_path)
    db_path = os.path.abspath(db_path)
    
    conn = sqlite3.connect(db_path)
    
    if load_vec and SUPPORTS_EXTENSION and VEC_EXTENSION_PATH.exists():
        conn.enable_load_extension(True)
        try:
            conn.load_extension(str(VEC_EXTENSION_PATH))
        except Exception as e:
            print(f"警告: 加载 sqlite-vec 扩展失败: {e}")
    
    return conn


def get_vec_version() -> str:
    """获取 sqlite-vec 版本"""
    conn = connect(':memory:')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT vec_version()")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def is_vec_available() -> bool:
    """检查 sqlite-vec 是否可用"""
    if not SUPPORTS_EXTENSION:
        return False
    try:
        version = get_vec_version()
        return bool(version)
    except:
        return False


def print_status():
    """打印状态"""
    print("=== SQLite 状态 ===")
    print(f"支持扩展: {'✅ 是' if SUPPORTS_EXTENSION else '❌ 否'}")
    print(f"sqlite-vec 扩展: {'✅ 存在' if VEC_EXTENSION_PATH.exists() else '❌ 不存在'}")
    
    if not SUPPORTS_EXTENSION:
        print("\n⚠️ 当前 SQLite 实现不支持扩展加载")
        print("请安装: pip install pysqlite3-binary")
    print("==================")


# 测试
if __name__ == "__main__":
    print_status()
    if is_vec_available():
        print(f"sqlite-vec 版本: {get_vec_version()}")

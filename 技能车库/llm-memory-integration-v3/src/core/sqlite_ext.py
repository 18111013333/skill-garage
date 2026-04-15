#!/usr/bin/env python3
"""
SQLite 扩展加载模块 (v5.2.19)
支持多种 SQLite 实现，用户可自行选择

支持的实现：
1. pysqlite3-binary - 支持扩展加载（推荐）
2. pysqlite3 - 纯 Python 实现
3. sqlite3 - Python 标准库（不支持扩展）

安装建议：
- 需要向量搜索：pip install pysqlite3-binary
- 仅需基础功能：使用标准库 sqlite3 即可

⚠️ 安全警告：
本模块加载原生 SQLite 扩展，存在远程代码执行风险。
所有扩展加载必须通过安全验证。
"""

import os
import json
from pathlib import Path
from typing import Optional, Tuple, Any
import importlib

# 配置文件路径
CONFIG_PATH = Path.home() / ".openclaw" / "memory-tdai" / "config" / "extension_config.json"

# 默认配置
DEFAULT_CONFIG = {
    "enable_native_extension": False,  # 默认禁用原生扩展
    "require_user_confirmation": True,  # 需要用户确认
    "allow_auto_load": False,  # 禁止自动加载
    "preferred_sqlite": "auto"  # auto, pysqlite3-binary, pysqlite3, sqlite3
}

def load_config() -> dict:
    """加载配置"""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except:
            pass
    return DEFAULT_CONFIG

def save_config(config: dict):
    """保存配置"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

# 加载配置
_config = load_config()
ENABLE_NATIVE_EXTENSION = _config.get("enable_native_extension", False)

# sqlite-vec 扩展路径
VEC_EXTENSION_PATH = Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64" / "vec0.so"


def detect_sqlite_implementations() -> dict:
    """
    检测可用的 SQLite 实现
    
    Returns:
        dict: 可用的实现及其特性
    """
    implementations = {}
    
    # 1. pysqlite3-binary（推荐，支持扩展）
    try:
        mod = importlib.import_module('pysqlite3')
        implementations['pysqlite3-binary'] = {
            'module': mod,
            'supports_extension': True,
            'description': 'pysqlite3-binary - 支持扩展加载（推荐）',
            'install': 'pip install pysqlite3-binary'
        }
    except ImportError:
        pass
    
    # 2. pysqlite3（纯 Python）
    try:
        mod = importlib.import_module('pysqlite3')
        if 'pysqlite3-binary' not in implementations:
            implementations['pysqlite3'] = {
                'module': mod,
                'supports_extension': True,
                'description': 'pysqlite3 - 纯 Python 实现',
                'install': 'pip install pysqlite3'
            }
    except ImportError:
        pass
    
    # 3. 标准库 sqlite3（不支持扩展）
    try:
        import sqlite3
        implementations['sqlite3'] = {
            'module': sqlite3,
            'supports_extension': False,
            'description': 'sqlite3 - Python 标准库（不支持扩展）',
            'install': '无需安装'
        }
    except ImportError:
        pass
    
    return implementations


def get_best_sqlite():
    """
    获取最优的 SQLite 实现
    
    优先级：
    1. pysqlite3-binary（支持扩展）
    2. pysqlite3（支持扩展）
    3. sqlite3（标准库）
    
    Returns:
        tuple: (module, info_dict)
    """
    implementations = detect_sqlite_implementations()
    
    # 按优先级选择
    for name in ['pysqlite3-binary', 'pysqlite3', 'sqlite3']:
        if name in implementations:
            return implementations[name]['module'], implementations[name]
    
    # 回退到标准库
    import sqlite3
    return sqlite3, {
        'supports_extension': False,
        'description': 'sqlite3 - Python 标准库',
        'install': '无需安装'
    }


# 自动选择最优实现
sqlite3, SQLITE_INFO = get_best_sqlite()
HAS_PYSQLITE3 = 'pysqlite3' in str(type(sqlite3).__module__)
SUPPORTS_EXTENSION = SQLITE_INFO.get('supports_extension', False)


def print_sqlite_status():
    """打印 SQLite 状态"""
    print("=== SQLite 实现状态 ===")
    print(f"当前使用: {SQLITE_INFO['description']}")
    print(f"支持扩展: {'✅ 是' if SUPPORTS_EXTENSION else '❌ 否'}")
    
    implementations = detect_sqlite_implementations()
    print(f"\n可用实现:")
    for name, info in implementations.items():
        marker = " (当前)" if info['module'] == sqlite3 else ""
        print(f"  - {info['description']}{marker}")
        print(f"    安装: {info['install']}")
    
    if not SUPPORTS_EXTENSION:
        print("\n⚠️ 当前实现不支持扩展加载")
        print("如需向量搜索功能，请安装: pip install pysqlite3-binary")
    print("=====================")


# 扩展加载状态缓存
_extension_load_confirmed = False

def get_sqlite_module():
    """
    获取当前 SQLite 模块
    
    Returns:
        sqlite3 模块
    """
    return sqlite3


def _verify_extension_safety(ext_path: Path) -> Tuple[bool, str]:
    """
    验证扩展安全性
    
    Returns:
        (是否安全, 原因)
    """
    global _extension_load_confirmed
    
    if _extension_load_confirmed:
        return True, "用户已确认"
    
    # 检查文件是否存在
    if not ext_path.exists():
        return False, f"扩展文件不存在: {ext_path}"
    
    # 检查文件权限
    try:
        import stat
        file_stat = os.stat(ext_path)
        mode = file_stat.st_mode
        # 仅允许 644 或 755
        if mode not in [0o644, 0o755]:
            return False, f"文件权限不安全: {oct(mode)}"
    except Exception as e:
        return False, f"无法检查文件权限: {e}"
    
    return True, "基本安全检查通过"


def confirm_extension_load(ext_path: Optional[Path] = None) -> bool:
    """
    用户确认扩展加载
    
    Args:
        ext_path: 扩展路径（可选）
        
    Returns:
        是否确认成功
    """
    global _extension_load_confirmed
    
    if not SUPPORTS_EXTENSION:
        print("❌ 当前 SQLite 实现不支持扩展加载")
        print(f"   请安装: pip install pysqlite3-binary")
        return False
    
    if ext_path is None:
        ext_path = VEC_EXTENSION_PATH
    
    if not ext_path.exists():
        print(f"❌ 扩展文件不存在: {ext_path}")
        return False
    
    is_safe, reason = _verify_extension_safety(ext_path)
    
    if is_safe:
        _extension_load_confirmed = True
        print(f"✅ 扩展加载已确认: {reason}")
        return True
    else:
        print(reason)
        return False


def connect(db_path: str, load_vec: bool = False) -> Any:
    """
    连接数据库
    
    Args:
        db_path: 数据库文件路径
        load_vec: 是否加载 sqlite-vec 扩展（需要先确认）
        
    Returns:
        数据库连接
    """
    global ENABLE_NATIVE_EXTENSION
    
    # 展开路径
    db_path = os.path.expanduser(db_path)
    db_path = os.path.abspath(db_path)
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    
    # 检查是否启用原生扩展
    if not ENABLE_NATIVE_EXTENSION:
        if load_vec:
            print("⚠️ 原生扩展加载已禁用")
            print(f"如需启用，请在配置文件中设置 enable_native_extension: true")
            print(f"配置文件路径: {CONFIG_PATH}")
        return conn
    
    # 检查是否支持扩展
    if not SUPPORTS_EXTENSION:
        if load_vec:
            print("⚠️ 当前 SQLite 实现不支持扩展加载")
            print(f"请安装: pip install pysqlite3-binary")
        return conn
    
    if load_vec:
        if not VEC_EXTENSION_PATH.exists():
            print(f"⚠️ sqlite-vec 扩展不存在: {VEC_EXTENSION_PATH}")
            return conn
        
        if not _extension_load_confirmed:
            print("⚠️ 扩展加载未确认，拒绝自动加载")
            print("请先调用 confirm_extension_load()")
            return conn
        
        is_safe, reason = _verify_extension_safety(VEC_EXTENSION_PATH)
        if not is_safe:
            print(reason)
            return conn
        
        # 加载扩展
        conn.enable_load_extension(True)
        try:
            conn.load_extension(str(VEC_EXTENSION_PATH))
        except Exception as e:
            print(f"警告: 加载 sqlite-vec 扩展失败: {e}")
    
    return conn


def connect_with_extension(db_path: str) -> Any:
    """
    连接数据库并加载扩展（需要先确认）
    
    Args:
        db_path: 数据库文件路径
        
    Returns:
        数据库连接
    """
    return connect(db_path, load_vec=True)


def get_vec_version() -> str:
    """获取 sqlite-vec 版本"""
    conn = connect(':memory:', load_vec=True)
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


def is_extension_supported() -> bool:
    """检查是否支持扩展加载"""
    return SUPPORTS_EXTENSION


def is_extension_confirmed() -> bool:
    """检查扩展加载是否已确认"""
    return _extension_load_confirmed


# 导出
__all__ = [
    'sqlite3',
    'connect',
    'connect_with_extension',
    'confirm_extension_load',
    'get_vec_version',
    'is_vec_available',
    'is_extension_supported',
    'is_extension_confirmed',
    'VEC_EXTENSION_PATH',
    'HAS_PYSQLITE3',
    'SUPPORTS_EXTENSION',
    'detect_sqlite_implementations',
    'get_best_sqlite',
    'print_sqlite_status'
]


# 测试
if __name__ == "__main__":
    print_sqlite_status()
    print()
    print(f"扩展加载已确认: {'✅ 是' if _extension_load_confirmed else '❌ 否'}")
    print()
    print("⚠️ 安全提示：")
    print("  扩展加载需要先调用 confirm_extension_load()")

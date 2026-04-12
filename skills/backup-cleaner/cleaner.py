#!/usr/bin/env python3
"""
OpenClaw 备份清理工具
自动清理老旧备份文件，释放磁盘空间
"""

import argparse
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import shutil

# 基础目录
BASE_DIR = Path("/home/sandbox/.openclaw")
WORKSPACE_DIR = BASE_DIR / "workspace"
BACKUP_DIR = BASE_DIR / "backup"
SESSIONS_DIR = BASE_DIR / "agents" / "main" / "sessions"
BROWSER_DIR = BASE_DIR / "browser"
NPM_CACHE_DIR = BASE_DIR / "npm-cache"
MEDIA_BROWSER_DIR = BASE_DIR / "media" / "browser"

# 颜色输出
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[{text}]{Colors.RESET}")

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def get_file_age_days(file_path):
    """获取文件年龄（天）"""
    mtime = os.path.getmtime(file_path)
    age = datetime.now() - datetime.fromtimestamp(mtime)
    return age.days

def scan_directory(directory, patterns=None, min_age_days=0):
    """
    扫描目录，返回匹配的文件列表
    
    Args:
        directory: 要扫描的目录
        patterns: 文件名模式列表（如 ['*.tar.gz', '*.zip']）
        min_age_days: 最小文件年龄（天）
    
    Returns:
        (文件列表, 总大小)
    """
    if not directory.exists():
        return [], 0
    
    files = []
    total_size = 0
    
    for item in directory.rglob('*'):
        if not item.is_file():
            continue
        
        # 检查文件年龄
        if min_age_days > 0:
            age = get_file_age_days(item)
            if age < min_age_days:
                continue
        
        # 检查文件模式
        if patterns:
            matched = False
            for pattern in patterns:
                if pattern.startswith('*.'):
                    # 后缀匹配
                    if item.name.endswith(pattern[1:]):
                        matched = True
                        break
                elif pattern in item.name:
                    # 包含匹配
                    matched = True
                    break
            if not matched:
                continue
        
        size = item.stat().st_size
        files.append((item, size, get_file_age_days(item)))
        total_size += size
    
    return files, total_size

def clean_backup_directory(keep_days, dry_run=True):
    """清理备份目录"""
    print_section("备份目录 (.openclaw/backup/)")
    
    if not BACKUP_DIR.exists():
        print("  目录不存在，跳过")
        return 0
    
    files, total_size = scan_directory(
        BACKUP_DIR,
        patterns=['*.tar.gz', '*.zip'],
        min_age_days=keep_days
    )
    
    if not files:
        print(f"  没有超过 {keep_days} 天的备份文件")
        return 0
    
    print(f"  发现 {len(files)} 个可清理文件:")
    for f, size, age in sorted(files, key=lambda x: x[2], reverse=True):
        print(f"    {Colors.RED}[{age}天]{Colors.RESET} {f.name} ({format_size(size)})")
    
    print(f"\n  可释放空间: {Colors.GREEN}{format_size(total_size)}{Colors.RESET}")
    
    if not dry_run:
        for f, _, _ in files:
            f.unlink()
        print(f"  {Colors.GREEN}已清理 {len(files)} 个文件{Colors.RESET}")
    
    return total_size

def clean_workspace_backups(keep_days, dry_run=True):
    """清理工作空间内的备份文件"""
    print_section("工作空间备份 (workspace/*.tar.gz, *.zip)")
    
    if not WORKSPACE_DIR.exists():
        print("  目录不存在，跳过")
        return 0
    
    files, total_size = scan_directory(
        WORKSPACE_DIR,
        patterns=['*.tar.gz', '*.zip'],
        min_age_days=keep_days
    )
    
    if not files:
        print(f"  没有超过 {keep_days} 天的备份文件")
        return 0
    
    print(f"  发现 {len(files)} 个可清理文件:")
    for f, size, age in sorted(files, key=lambda x: x[2], reverse=True)[:10]:
        rel_path = f.relative_to(WORKSPACE_DIR)
        print(f"    {Colors.RED}[{age}天]{Colors.RESET} {rel_path} ({format_size(size)})")
    
    if len(files) > 10:
        print(f"    ... 还有 {len(files) - 10} 个文件")
    
    print(f"\n  可释放空间: {Colors.GREEN}{format_size(total_size)}{Colors.RESET}")
    
    if not dry_run:
        for f, _, _ in files:
            f.unlink()
        print(f"  {Colors.GREEN}已清理 {len(files)} 个文件{Colors.RESET}")
    
    return total_size

def clean_session_snapshots(keep_days, dry_run=True):
    """清理会话快照文件"""
    print_section("会话快照 (sessions/*.jsonl.reset.*, *.jsonl.deleted.*)")
    
    if not SESSIONS_DIR.exists():
        print("  目录不存在，跳过")
        return 0
    
    files, total_size = scan_directory(
        SESSIONS_DIR,
        patterns=['.jsonl.reset.', '.jsonl.deleted.'],
        min_age_days=keep_days
    )
    
    if not files:
        print(f"  没有超过 {keep_days} 天的快照文件")
        return 0
    
    print(f"  发现 {len(files)} 个可清理文件:")
    for f, size, age in sorted(files, key=lambda x: x[2], reverse=True)[:10]:
        print(f"    {Colors.RED}[{age}天]{Colors.RESET} {f.name} ({format_size(size)})")
    
    if len(files) > 10:
        print(f"    ... 还有 {len(files) - 10} 个文件")
    
    print(f"\n  可释放空间: {Colors.GREEN}{format_size(total_size)}{Colors.RESET}")
    
    if not dry_run:
        for f, _, _ in files:
            f.unlink()
        print(f"  {Colors.GREEN}已清理 {len(files)} 个文件{Colors.RESET}")
    
    return total_size

def clean_browser_cache(dry_run=True):
    """清理浏览器缓存"""
    print_section("浏览器缓存 (.openclaw/browser/)")
    
    total_size = 0
    cleaned_count = 0
    
    for browser_dir in [BROWSER_DIR, MEDIA_BROWSER_DIR]:
        if not browser_dir.exists():
            continue
        
        # 计算目录大小
        dir_size = sum(f.stat().st_size for f in browser_dir.rglob('*') if f.is_file())
        
        if dir_size > 0:
            print(f"  {browser_dir.relative_to(BASE_DIR)}: {format_size(dir_size)}")
            total_size += dir_size
            cleaned_count += 1
    
    if total_size == 0:
        print("  没有浏览器缓存")
        return 0
    
    print(f"\n  可释放空间: {Colors.GREEN}{format_size(total_size)}{Colors.RESET}")
    
    if not dry_run:
        for browser_dir in [BROWSER_DIR, MEDIA_BROWSER_DIR]:
            if browser_dir.exists():
                shutil.rmtree(browser_dir)
        print(f"  {Colors.GREEN}已清理浏览器缓存{Colors.RESET}")
    
    return total_size

def clean_npm_cache(dry_run=True):
    """清理 NPM 缓存"""
    print_section("NPM 缓存 (.openclaw/npm-cache/)")
    
    if not NPM_CACHE_DIR.exists():
        print("  目录不存在，跳过")
        return 0
    
    # 计算目录大小
    total_size = sum(f.stat().st_size for f in NPM_CACHE_DIR.rglob('*') if f.is_file())
    
    if total_size == 0:
        print("  没有缓存文件")
        return 0
    
    print(f"  缓存大小: {format_size(total_size)}")
    print(f"  可释放空间: {Colors.GREEN}{format_size(total_size)}{Colors.RESET}")
    
    if not dry_run:
        shutil.rmtree(NPM_CACHE_DIR)
        print(f"  {Colors.GREEN}已清理 NPM 缓存{Colors.RESET}")
    
    return total_size

def clean_large_tools(dry_run=True):
    """清理大型工具文件"""
    print_section("大型工具文件 (magika, git-lfs)")
    
    local_bin = Path("/home/sandbox/.local/bin")
    if not local_bin.exists():
        print("  目录不存在，跳过")
        return 0
    
    large_files = [
        local_bin / "magika",      # ~32MB
        local_bin / "git-lfs",     # ~11MB
    ]
    
    total_size = 0
    found_files = []
    
    for f in large_files:
        if f.exists():
            size = f.stat().st_size
            found_files.append((f, size))
            total_size += size
            print(f"  {f.name}: {format_size(size)}")
    
    if not found_files:
        print("  没有大型工具文件")
        return 0
    
    print(f"\n  可释放空间: {Colors.GREEN}{format_size(total_size)}{Colors.RESET}")
    print(f"  {Colors.YELLOW}注意: 这些工具可能需要重新安装{Colors.RESET}")
    
    if not dry_run:
        for f, _ in found_files:
            f.unlink()
        print(f"  {Colors.GREEN}已清理 {len(found_files)} 个文件{Colors.RESET}")
    
    return total_size

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 备份清理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看可清理空间
  python cleaner.py --dry-run

  # 清理 7 天前的备份
  python cleaner.py --keep-days 7

  # 激进清理（包括浏览器缓存和大型工具）
  python cleaner.py --keep-days 3 --include-browser --include-tools
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示可清理空间，不实际删除"
    )
    parser.add_argument(
        "--keep-days",
        type=int,
        default=7,
        help="保留最近 N 天的文件 (默认: 7)"
    )
    parser.add_argument(
        "--include-browser",
        action="store_true",
        help="同时清理浏览器缓存"
    )
    parser.add_argument(
        "--include-npm",
        action="store_true",
        help="同时清理 NPM 缓存"
    )
    parser.add_argument(
        "--include-tools",
        action="store_true",
        help="同时清理大型工具文件 (magika, git-lfs)"
    )
    parser.add_argument(
        "--aggressive",
        action="store_true",
        help="激进模式: 清理所有可清理内容"
    )
    
    args = parser.parse_args()
    
    # 激进模式
    if args.aggressive:
        args.include_browser = True
        args.include_npm = True
        args.include_tools = True
        args.keep_days = min(args.keep_days, 3)
    
    print_header("OpenClaw 备份清理工具")
    
    if args.dry_run:
        print(f"{Colors.YELLOW}干运行模式 - 只显示可清理空间{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}执行模式 - 将删除文件{Colors.RESET}")
    
    print(f"保留天数: {args.keep_days}")
    
    total_freed = 0
    
    # 清理各类文件
    total_freed += clean_backup_directory(args.keep_days, args.dry_run)
    total_freed += clean_workspace_backups(args.keep_days, args.dry_run)
    total_freed += clean_session_snapshots(args.keep_days, args.dry_run)
    
    if args.include_browser:
        total_freed += clean_browser_cache(args.dry_run)
    
    if args.include_npm:
        total_freed += clean_npm_cache(args.dry_run)
    
    if args.include_tools:
        total_freed += clean_large_tools(args.dry_run)
    
    # 总结
    print_header("清理总结")
    print(f"可释放总空间: {Colors.GREEN}{format_size(total_freed)}{Colors.RESET}")
    
    if args.dry_run:
        print(f"\n{Colors.YELLOW}提示: 使用不带 --dry-run 的命令执行实际清理{Colors.RESET}")
        print(f"示例: python cleaner.py --keep-days {args.keep_days}")
    else:
        print(f"\n{Colors.GREEN}清理完成！{Colors.RESET}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

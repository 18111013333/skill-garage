#!/usr/bin/env python3
"""
命令钩子管理器
实现命令的预处理、后处理和错误处理钩子
"""

import json
import sys
import time
import uuid
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from functools import wraps

class HookManager:
    """钩子管理器"""

    def __init__(self):
        self.before_hooks: List[Callable] = []
        self.after_hooks: List[Callable] = []
        self.error_hooks: List[Callable] = []
        self.audit_log: List[Dict] = []

    def register_before(self, hook: Callable, priority: int = 0) -> None:
        """注册预处理钩子"""
        self.before_hooks.append((priority, hook))
        self.before_hooks.sort(key=lambda x: x[0], reverse=True)

    def register_after(self, hook: Callable, priority: int = 0) -> None:
        """注册后处理钩子"""
        self.after_hooks.append((priority, hook))
        self.after_hooks.sort(key=lambda x: x[0], reverse=True)

    def register_error(self, hook: Callable, priority: int = 0) -> None:
        """注册错误钩子"""
        self.error_hooks.append((priority, hook))
        self.error_hooks.sort(key=lambda x: x[0], reverse=True)

    def execute_command(self, command: str, params: Dict = None,
                       executor: Callable = None) -> Dict[str, Any]:
        """执行命令（带钩子）"""
        command_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        context = {
            'command_id': command_id,
            'command': command,
            'params': params or {},
            'start_time': datetime.now().isoformat(),
            'status': 'pending'
        }

        try:
            # 执行预处理钩子
            for priority, hook in self.before_hooks:
                result = hook(context)
                if result is False:
                    context['status'] = 'rejected'
                    return context

            # 执行命令
            if executor:
                context['result'] = executor(command, params)
            else:
                context['result'] = self._default_executor(command, params)

            context['status'] = 'success'

            # 执行后处理钩子（逆序）
            for priority, hook in reversed(self.after_hooks):
                hook(context)

        except Exception as e:
            context['status'] = 'error'
            context['error'] = str(e)

            # 执行错误钩子
            for priority, hook in self.error_hooks:
                hook(context)

        finally:
            context['duration_ms'] = round((time.time() - start_time) * 1000, 2)
            context['end_time'] = datetime.now().isoformat()

            # 记录审计日志
            self.audit_log.append(context)

        return context

    def _default_executor(self, command: str, params: Dict) -> str:
        """默认执行器"""
        return f"Executed: {command}"


# 内置钩子函数

def validate_params(context: Dict) -> bool:
    """验证参数钩子"""
    print(f"[Hook] Validating params for: {context['command']}")
    return True

def log_command(context: Dict) -> bool:
    """记录命令日志钩子"""
    print(f"[Hook] Command: {context['command']} (ID: {context['command_id']})")
    return True

def check_permission(context: Dict) -> bool:
    """检查权限钩子"""
    print(f"[Hook] Checking permission for: {context['command']}")
    return True

def log_result(context: Dict) -> None:
    """记录结果日志钩子"""
    print(f"[Hook] Result: {context.get('status')} (Duration: {context.get('duration_ms', 0)}ms)")

def log_error(context: Dict) -> None:
    """记录错误日志钩子"""
    print(f"[Hook] Error: {context.get('error')}")

def notify_on_error(context: Dict) -> None:
    """错误通知钩子"""
    print(f"[Hook] Notifying error: {context['command']} - {context.get('error')}")


def create_default_manager() -> HookManager:
    """创建默认钩子管理器"""
    manager = HookManager()

    # 注册预处理钩子
    manager.register_before(validate_params, priority=100)
    manager.register_before(log_command, priority=90)
    manager.register_before(check_permission, priority=80)

    # 注册后处理钩子
    manager.register_after(log_result, priority=100)

    # 注册错误钩子
    manager.register_error(log_error, priority=100)
    manager.register_error(notify_on_error, priority=90)

    return manager


def main():
    """主函数"""
    manager = create_default_manager()

    if len(sys.argv) < 2:
        # 演示模式
        result = manager.execute_command("npm install", {"package": "express"})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    command = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    result = manager.execute_command(command, params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

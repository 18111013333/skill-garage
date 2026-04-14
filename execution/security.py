#!/usr/bin/env python3
"""
安全模块
权限管理、审计日志、安全检查
"""

import os
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class AuditLog:
    """审计日志"""
    id: str
    action: str
    user: str
    resource: str
    result: str  # success, denied, error
    details: str
    timestamp: str


@dataclass
class Permission:
    """权限"""
    resource: str
    action: str
    allowed: bool


class SecurityManager:
    """安全管理器"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(
                os.path.dirname(__file__),
                'security'
            )
        
        self.config_dir = config_dir
        self.audit_file = os.path.join(config_dir, 'audit.json')
        self.policy_file = os.path.join(config_dir, 'policy.json')
        
        self.audit_logs: List[AuditLog] = []
        self.policies: Dict[str, List[Permission]] = {}
        
        os.makedirs(config_dir, exist_ok=True)
        self._load_data()
        self._init_default_policies()
        
        print(f"安全管理器初始化完成")
        print(f"  - 审计日志: {len(self.audit_logs)} 条")
        print(f"  - 策略数量: {len(self.policies)}")
    
    def _load_data(self):
        """加载数据"""
        # 加载审计日志
        if os.path.exists(self.audit_file):
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for log_data in data.get('logs', []):
                log = AuditLog(
                    id=log_data['id'],
                    action=log_data['action'],
                    user=log_data['user'],
                    resource=log_data['resource'],
                    result=log_data['result'],
                    details=log_data['details'],
                    timestamp=log_data['timestamp']
                )
                self.audit_logs.append(log)
        
        # 加载策略
        if os.path.exists(self.policy_file):
            with open(self.policy_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for role, perms in data.get('policies', {}).items():
                self.policies[role] = [
                    Permission(
                        resource=p['resource'],
                        action=p['action'],
                        allowed=p['allowed']
                    )
                    for p in perms
                ]
    
    def _save_data(self):
        """保存数据"""
        # 保存审计日志
        audit_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'logs': [asdict(log) for log in self.audit_logs[-1000:]]
        }
        
        with open(self.audit_file, 'w', encoding='utf-8') as f:
            json.dump(audit_data, f, ensure_ascii=False, indent=2)
        
        # 保存策略
        policy_data = {
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
            'policies': {
                role: [asdict(p) for p in perms]
                for role, perms in self.policies.items()
            }
        }
        
        with open(self.policy_file, 'w', encoding='utf-8') as f:
            json.dump(policy_data, f, ensure_ascii=False, indent=2)
    
    def _init_default_policies(self):
        """初始化默认策略"""
        if 'admin' not in self.policies:
            self.policies['admin'] = [
                Permission('*', '*', True)
            ]
        
        if 'user' not in self.policies:
            self.policies['user'] = [
                Permission('memory', 'read', True),
                Permission('memory', 'write', True),
                Permission('memory', 'delete', False),
                Permission('config', 'read', True),
                Permission('config', 'write', False),
            ]
        
        if 'guest' not in self.policies:
            self.policies['guest'] = [
                Permission('memory', 'read', True),
                Permission('memory', 'write', False),
                Permission('config', 'read', False),
            ]
        
        self._save_data()
    
    def check_permission(self, role: str, resource: str, action: str) -> bool:
        """检查权限"""
        if role not in self.policies:
            return False
        
        for perm in self.policies[role]:
            if perm.resource == '*' or perm.resource == resource:
                if perm.action == '*' or perm.action == action:
                    return perm.allowed
        
        return False
    
    def log_action(self, action: str, user: str, resource: str, 
                   result: str, details: str = "") -> AuditLog:
        """记录审计日志"""
        log_id = hashlib.md5(f"{action}{user}{time.time()}".encode()).hexdigest()[:16]
        
        log = AuditLog(
            id=log_id,
            action=action,
            user=user,
            resource=resource,
            result=result,
            details=details,
            timestamp=datetime.now().isoformat()
        )
        
        self.audit_logs.append(log)
        self._save_data()
        
        return log
    
    def check_directory_permissions(self) -> Dict:
        """检查目录权限"""
        issues = []
        
        # 检查 .openclaw 目录
        openclaw_dir = os.path.expanduser('~/.openclaw')
        if os.path.exists(openclaw_dir):
            stat = os.stat(openclaw_dir)
            mode = oct(stat.st_mode)[-3:]
            
            if mode != '700':
                issues.append({
                    'path': openclaw_dir,
                    'current': mode,
                    'expected': '700',
                    'severity': 'high'
                })
        
        return {
            'checked_at': datetime.now().isoformat(),
            'issues': issues,
            'status': 'secure' if not issues else 'needs_attention'
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        success = sum(1 for log in self.audit_logs if log.result == 'success')
        denied = sum(1 for log in self.audit_logs if log.result == 'denied')
        
        return {
            'total_logs': len(self.audit_logs),
            'success_count': success,
            'denied_count': denied,
            'roles': len(self.policies)
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    manager = SecurityManager()
    
    if len(sys.argv) < 2:
        print("用法: python security.py <command>")
        print("命令: check, logs, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'check':
        result = manager.check_directory_permissions()
        print("\n安全检查:")
        print("-" * 40)
        print(f"状态: {result['status']}")
        if result['issues']:
            for issue in result['issues']:
                print(f"  ⚠️ {issue['path']}: {issue['current']} → {issue['expected']}")
        else:
            print("  ✅ 无安全问题")
    
    elif command == 'logs':
        print("\n审计日志 (最近10条):")
        print("-" * 60)
        for log in manager.audit_logs[-10:]:
            status = "✅" if log.result == 'success' else "❌"
            print(f"{status} [{log.action}] {log.user} -> {log.resource}")
    
    elif command == 'stats':
        stats = manager.get_stats()
        print("\n安全统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")

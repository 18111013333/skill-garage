"""
文件保护模块 V1.0
防止在升级优化过程中误删有用文件

核心规则:
1. 所有删除操作必须经过人工二次确认
2. 确认时必须说明文件的必要性和作用
3. 受保护文件列表不可绕过
"""

import os
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/sandbox/.openclaw/workspace")
GUARD_DIR = WORKSPACE / "guard"
PROTECTED_LIST = GUARD_DIR / "protected_files.json"
DELETE_LOG = GUARD_DIR / "delete_log.json"

# 核心受保护文件 (绝对不可删除)
CORE_PROTECTED = [
    # L1 核心认知层
    "AGENTS.md",
    "SOUL.md", 
    "USER.md",
    "TOOLS.md",
    "IDENTITY.md",
    "MEMORY.md",
    "CONFIG.json",
    
    # 架构文件
    "core/ARCHITECTURE_V2.9.2.md",
    "core/ARCHITECTURE_V2.9.1.md",
    "core/ARCHITECTURE_V2.8.1.md",
    "core/FULL_ARCHITECTURE_V2.9.2.json",
    "core/FULL_ARCHITECTURE_V2.9.1.json",
    "core/CONFIG.json",
    "core/QUICK_REF.md",
    
    # L5 安全治理层
    "guard/security.py",
    "guard/permissions.py",
    "guard/audit.py",
    "guard/file_guardian.py",
    "guard/protected_files.json",
    
    # L6 基础设施层
    "infra/paths.py",
    "infra/plugins.py",
    "infra/performance.py",
    "infra/registry.py",
    "infra/migrate_v29.py",
    
    # 引导模块
    "guide/bootstrap.py",
    "guide/assistant_guide.py",
    "guide/guide_config.json",
    
    # 技能路由
    "orchestration/router/SKILL_ROUTER_V2.json",
    "engine/router.py",
]

# 按类型受保护的文件模式
PROTECTED_PATTERNS = {
    "memory": ["memory/*.md", "MEMORY.md"],
    "skills": ["skills/*/SKILL.md"],
    "config": ["*.json", "core/*.json", "guard/*.json"],
}


class FileGuardian:
    """文件保护守护者"""
    
    def __init__(self):
        self.protected = self._load_protected_list()
        self.delete_log = self._load_delete_log()
    
    def _load_protected_list(self) -> dict:
        """加载受保护文件列表"""
        if PROTECTED_LIST.exists():
            with open(PROTECTED_LIST) as f:
                return json.load(f)
        return {"core": CORE_PROTECTED, "user_added": []}
    
    def _save_protected_list(self):
        """保存受保护文件列表"""
        PROTECTED_LIST.parent.mkdir(parents=True, exist_ok=True)
        with open(PROTECTED_LIST, 'w') as f:
            json.dump(self.protected, f, indent=2, ensure_ascii=False)
    
    def _load_delete_log(self) -> list:
        """加载删除日志"""
        if DELETE_LOG.exists():
            with open(DELETE_LOG) as f:
                return json.load(f)
        return []
    
    def _log_delete_request(self, file_path: str, reason: str, status: str):
        """记录删除请求"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "reason": reason,
            "status": status,  # pending, approved, rejected
            "necessity": self._analyze_necessity(file_path)
        }
        self.delete_log.append(entry)
        DELETE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DELETE_LOG, 'w') as f:
            json.dump(self.delete_log, f, indent=2, ensure_ascii=False)
    
    def _analyze_necessity(self, file_path: str) -> dict:
        """分析文件的必要性和作用"""
        path = WORKSPACE / file_path
        result = {
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else 0,
            "type": path.suffix,
            "description": self._get_file_description(file_path)
        }
        return result
    
    def _get_file_description(self, file_path: str) -> str:
        """获取文件描述"""
        descriptions = {
            # L1 核心文件
            "AGENTS.md": "工作空间规则，定义每次会话的加载流程和六层架构",
            "SOUL.md": "身份定义，定义AI的性格和行为准则",
            "USER.md": "用户信息，记录用户的偏好和上下文",
            "TOOLS.md": "工具规则，定义工具的使用优先级和约束",
            "IDENTITY.md": "身份标识，定义AI的名称和形象",
            "MEMORY.md": "长期记忆，存储重要的历史信息",
            "CONFIG.json": "核心配置，定义六层架构的Token预算和加载策略",
            
            # 架构文件
            "core/ARCHITECTURE_V2.9.2.md": "最新架构文档，定义完整的六层架构",
            "core/FULL_ARCHITECTURE_V2.9.2.json": "完整架构JSON，包含所有技能和分类",
            
            # L5 安全文件
            "guard/security.py": "安全检查模块，检查危险命令和路径",
            "guard/permissions.py": "权限管理模块，控制操作权限",
            "guard/file_guardian.py": "文件保护模块，防止误删重要文件",
            "guard/protected_files.json": "受保护文件列表",
            
            # L6 基础设施文件
            "infra/paths.py": "路径解析模块，处理文件路径",
            "infra/performance.py": "性能模块，优化响应速度",
            
            # 引导模块
            "guide/bootstrap.py": "引导启动脚本",
            "guide/assistant_guide.py": "完整引导模块",
        }
        return descriptions.get(file_path, "未知文件，需要人工评估")
    
    def is_protected(self, file_path: str) -> tuple:
        """检查文件是否受保护"""
        # 检查核心保护列表
        all_protected = self.protected.get("core", []) + self.protected.get("user_added", [])
        
        for protected_path in all_protected:
            if file_path == protected_path or file_path.endswith(protected_path):
                return True, f"核心受保护文件: {protected_path}"
        
        # 检查模式匹配
        for pattern_type, patterns in PROTECTED_PATTERNS.items():
            for pattern in patterns:
                if self._match_pattern(file_path, pattern):
                    return True, f"受保护模式({pattern_type}): {pattern}"
        
        return False, "未受保护"
    
    def _match_pattern(self, file_path: str, pattern: str) -> bool:
        """简单的模式匹配"""
        import fnmatch
        return fnmatch.fnmatch(file_path, pattern)
    
    def request_delete(self, file_path: str, reason: str) -> dict:
        """请求删除文件 - 必须经过人工确认"""
        
        # 检查是否受保护
        is_protected, protection_reason = self.is_protected(file_path)
        
        # 分析文件必要性
        necessity = self._analyze_necessity(file_path)
        
        # 记录删除请求
        self._log_delete_request(file_path, reason, "pending")
        
        # 生成确认请求
        confirmation = {
            "action": "DELETE_CONFIRMATION_REQUIRED",
            "file": file_path,
            "is_protected": is_protected,
            "protection_reason": protection_reason if is_protected else None,
            "reason_for_delete": reason,
            "file_info": {
                "exists": necessity["exists"],
                "size_bytes": necessity["size"],
                "type": necessity["type"],
                "description": necessity["description"]
            },
            "message": self._generate_confirmation_message(file_path, is_protected, necessity),
            "require_manual_confirm": True
        }
        
        return confirmation
    
    def _generate_confirmation_message(self, file_path: str, is_protected: bool, necessity: dict) -> str:
        """生成确认消息"""
        msg = f"""
╔══════════════════════════════════════════════════════════════╗
║                    ⚠️  删除确认请求  ⚠️                       ║
╠══════════════════════════════════════════════════════════════╣
║  文件: {file_path:<48} ║
║  大小: {necessity['size']} bytes                                          ║
║  类型: {necessity['type']:<48} ║
╠══════════════════════════════════════════════════════════════╣
║  文件作用:                                                   ║
║  {necessity['description']:<56} ║
╠══════════════════════════════════════════════════════════════╣
"""
        if is_protected:
            msg += f"""║  🔒 状态: 受保护文件 - 需要特别确认                          ║
║  保护原因: {protection_reason:<46} ║
"""
        else:
            msg += """║  📁 状态: 普通文件 - 需要确认                                ║
"""
        
        msg += """╠══════════════════════════════════════════════════════════════╣
║  请确认是否删除此文件:                                       ║
║  - 输入 "确认删除 [文件名]" 执行删除                          ║
║  - 输入 "取消" 取消删除                                       ║
╚══════════════════════════════════════════════════════════════╝
"""
        return msg
    
    def confirm_delete(self, file_path: str, user_confirm: str) -> dict:
        """确认删除"""
        if user_confirm.lower() not in ["确认删除", "confirm", "yes"]:
            # 更新日志状态
            for entry in reversed(self.delete_log):
                if entry["file"] == file_path and entry["status"] == "pending":
                    entry["status"] = "rejected"
                    break
            with open(DELETE_LOG, 'w') as f:
                json.dump(self.delete_log, f, indent=2)
            
            return {
                "action": "DELETE_CANCELLED",
                "file": file_path,
                "message": f"删除已取消: {file_path}"
            }
        
        # 更新日志状态
        for entry in reversed(self.delete_log):
            if entry["file"] == file_path and entry["status"] == "pending":
                entry["status"] = "approved"
                break
        with open(DELETE_LOG, 'w') as f:
            json.dump(self.delete_log, f, indent=2)
        
        # 执行删除
        path = WORKSPACE / file_path
        if path.exists():
            # 使用 trash 而不是 rm
            import shutil
            trash_dir = WORKSPACE / ".trash"
            trash_dir.mkdir(exist_ok=True)
            shutil.move(str(path), str(trash_dir / path.name))
            
            return {
                "action": "DELETE_COMPLETED",
                "file": file_path,
                "message": f"文件已移至回收站: {file_path}"
            }
        else:
            return {
                "action": "FILE_NOT_FOUND",
                "file": file_path,
                "message": f"文件不存在: {file_path}"
            }
    
    def add_protection(self, file_path: str, reason: str):
        """添加文件到保护列表"""
        if "user_added" not in self.protected:
            self.protected["user_added"] = []
        
        self.protected["user_added"].append({
            "path": file_path,
            "reason": reason,
            "added_at": datetime.now().isoformat()
        })
        
        self._save_protected_list()
        
        return {
            "action": "PROTECTION_ADDED",
            "file": file_path,
            "message": f"已添加到保护列表: {file_path}"
        }
    
    def remove_protection(self, file_path: str) -> dict:
        """从保护列表移除 (仍需确认)"""
        return self.request_delete(
            f"protected:{file_path}", 
            "请求移除文件保护"
        )


# 全局实例
file_guardian = FileGuardian()


def check_before_delete(file_path: str, reason: str = "") -> dict:
    """删除前检查 - 必须调用此函数"""
    return file_guardian.request_delete(file_path, reason)


def confirm_and_delete(file_path: str, user_confirm: str) -> dict:
    """确认后删除"""
    return file_guardian.confirm_delete(file_path, user_confirm)


def protect_file(file_path: str, reason: str) -> dict:
    """保护文件"""
    return file_guardian.add_protection(file_path, reason)


# 使用示例
if __name__ == "__main__":
    # 示例: 请求删除文件
    result = check_before_delete("test.py", "测试删除")
    print(result["message"])
    
    # 用户确认后才能删除
    # confirm_and_delete("test.py", "确认删除")

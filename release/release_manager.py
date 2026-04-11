#!/usr/bin/env python3
"""
版本发布管理器 - V2.8.0

功能：
- 版本号体系
- 发布说明模板
- 变更影响范围记录
- 稳定版 / 实验版 区分
- 灰度测试机制
- 回滚机制
- 发布历史记录
"""

import json
import shutil
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import re

from infrastructure.path_resolver import get_project_root

class VersionType(Enum):
    MAJOR = "major"      # 主版本（不兼容变更）
    MINOR = "minor"      # 次版本（新功能）
    PATCH = "patch"      # 补丁版本（修复）

class ReleaseChannel(Enum):
    STABLE = "stable"        # 稳定版
    EXPERIMENTAL = "experimental"  # 实验版
    CANARY = "canary"        # 灰度版

class ReleaseStatus(Enum):
    DRAFT = "draft"          # 草稿
    TESTING = "testing"      # 测试中
    RELEASED = "released"    # 已发布
    ROLLED_BACK = "rolled_back"  # 已回滚
    DEPRECATED = "deprecated"    # 已废弃

@dataclass
class Version:
    """版本号"""
    major: int
    minor: int
    patch: int
    channel: str
    
    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}-{self.channel}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_string(cls, version_str: str) -> 'Version':
        match = re.match(r'v?(\d+)\.(\d+)\.(\d+)(?:-(\w+))?', version_str)
        if match:
            return cls(
                major=int(match.group(1)),
                minor=int(match.group(2)),
                patch=int(match.group(3)),
                channel=match.group(4) or ReleaseChannel.STABLE.value
            )
        return cls(major=0, minor=0, patch=0, channel=ReleaseChannel.STABLE.value)

@dataclass
class ChangeRecord:
    """变更记录"""
    type: str          # added, changed, fixed, removed
    scope: str         # 影响范围
    description: str
    breaking: bool     # 是否破坏性变更

@dataclass
class Release:
    """发布记录"""
    version: str
    channel: str
    status: str
    release_notes: str
    changes: List[Dict]
    impact_scope: List[str]
    released_at: str
    released_by: str
    rollback_version: Optional[str]
    test_results: Dict
    canary_percentage: int  # 灰度比例

class ReleaseManager:
    """版本发布管理器"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.release_dir = self.project_root / 'release'
        self.history_path = self.release_dir / 'release_history.json'
        self.current_path = self.release_dir / 'current_version.json'
        
        self.releases: Dict[str, Release] = {}
        self.current_version: Optional[Version] = None
        
        self._load()
    
    def _load(self):
        """加载发布历史"""
        if self.history_path.exists():
            data = json.loads(self.history_path.read_text(encoding='utf-8'))
            for ver, rel in data.get("releases", {}).items():
                self.releases[ver] = Release(**rel)
        
        if self.current_path.exists():
            data = json.loads(self.current_path.read_text(encoding='utf-8'))
            self.current_version = Version(**data)
    
    def _save(self):
        """保存发布历史"""
        self.release_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_path.write_text(
            json.dumps({
                "releases": {ver: asdict(rel) for ver, rel in self.releases.items()},
                "updated": datetime.now().isoformat()
            }, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        if self.current_version:
            self.current_path.write_text(
                json.dumps(self.current_version.to_dict(), indent=2),
                encoding='utf-8'
            )
    
    def get_current_version(self) -> Optional[Version]:
        """获取当前版本"""
        return self.current_version
    
    def bump_version(self, version_type: str, channel: str = None) -> Version:
        """升级版本号"""
        if not self.current_version:
            self.current_version = Version(1, 0, 0, channel or ReleaseChannel.STABLE.value)
        else:
            if version_type == VersionType.MAJOR.value:
                self.current_version = Version(
                    self.current_version.major + 1,
                    0,
                    0,
                    channel or self.current_version.channel
                )
            elif version_type == VersionType.MINOR.value:
                self.current_version = Version(
                    self.current_version.major,
                    self.current_version.minor + 1,
                    0,
                    channel or self.current_version.channel
                )
            elif version_type == VersionType.PATCH.value:
                self.current_version = Version(
                    self.current_version.major,
                    self.current_version.minor,
                    self.current_version.patch + 1,
                    channel or self.current_version.channel
                )
        
        self._save()
        return self.current_version
    
    def create_release(self, version: str, channel: str, release_notes: str,
                       changes: List[Dict], impact_scope: List[str],
                       released_by: str = "system") -> Release:
        """创建发布"""
        release = Release(
            version=version,
            channel=channel,
            status=ReleaseStatus.DRAFT.value,
            release_notes=release_notes,
            changes=changes,
            impact_scope=impact_scope,
            released_at=datetime.now().isoformat(),
            released_by=released_by,
            rollback_version=str(self.current_version) if self.current_version else None,
            test_results={},
            canary_percentage=0
        )
        
        self.releases[version] = release
        self._save()
        
        return release
    
    def start_testing(self, version: str):
        """开始测试"""
        if version in self.releases:
            self.releases[version].status = ReleaseStatus.TESTING.value
            self._save()
    
    def record_test_results(self, version: str, results: Dict):
        """记录测试结果"""
        if version in self.releases:
            self.releases[version].test_results = results
            self._save()
    
    def set_canary_percentage(self, version: str, percentage: int):
        """设置灰度比例"""
        if version in self.releases:
            self.releases[version].canary_percentage = min(100, max(0, percentage))
            self._save()
    
    def release(self, version: str) -> Dict:
        """发布版本"""
        if version not in self.releases:
            return {"error": f"版本不存在: {version}"}
        
        release = self.releases[version]
        
        # 检查测试结果
        if release.status != ReleaseStatus.TESTING.value:
            return {"error": "版本未完成测试"}
        
        # 更新状态
        release.status = ReleaseStatus.RELEASED.value
        release.released_at = datetime.now().isoformat()
        
        # 更新当前版本
        self.current_version = Version.from_string(version)
        
        self._save()
        
        return {
            "status": "success",
            "version": version,
            "released_at": release.released_at,
            "rollback_version": release.rollback_version
        }
    
    def rollback(self, reason: str = "") -> Dict:
        """回滚到上一版本"""
        if not self.current_version:
            return {"error": "无当前版本"}
        
        current = str(self.current_version)
        if current not in self.releases:
            return {"error": "当前版本无发布记录"}
        
        rollback_version = self.releases[current].rollback_version
        if not rollback_version:
            return {"error": "无回滚版本"}
        
        # 标记当前版本为已回滚
        self.releases[current].status = ReleaseStatus.ROLLED_BACK.value
        
        # 恢复到回滚版本
        self.current_version = Version.from_string(rollback_version)
        
        self._save()
        
        return {
            "status": "success",
            "rolled_back_from": current,
            "rolled_back_to": rollback_version,
            "reason": reason
        }
    
    def deprecate(self, version: str):
        """废弃版本"""
        if version in self.releases:
            self.releases[version].status = ReleaseStatus.DEPRECATED.value
            self._save()
    
    def get_release_history(self, limit: int = 20) -> List[Dict]:
        """获取发布历史"""
        releases = sorted(
            self.releases.values(),
            key=lambda r: r.released_at,
            reverse=True
        )
        return [asdict(r) for r in releases[:limit]]
    
    def get_stable_versions(self) -> List[str]:
        """获取稳定版本列表"""
        return [
            ver for ver, rel in self.releases.items()
            if rel.channel == ReleaseChannel.STABLE.value and 
               rel.status == ReleaseStatus.RELEASED.value
        ]
    
    def generate_release_notes(self, version: str) -> str:
        """生成发布说明"""
        if version not in self.releases:
            return "版本不存在"
        
        release = self.releases[version]
        
        lines = [
            f"# 发布说明 {version}",
            "",
            f"**渠道**: {release.channel}",
            f"**状态**: {release.status}",
            f"**发布时间**: {release.released_at}",
            "",
            "## 变更内容",
            ""
        ]
        
        for change in release.changes:
            type_emoji = {
                "added": "✨",
                "changed": "🔄",
                "fixed": "🐛",
                "removed": "🗑️"
            }.get(change.get("type", ""), "📝")
            
            breaking = "⚠️ 破坏性变更" if change.get("breaking") else ""
            lines.append(f"- {type_emoji} **{change.get('scope', '')}**: {change.get('description', '')} {breaking}")
        
        lines.extend([
            "",
            "## 影响范围",
            ""
        ])
        
        for scope in release.impact_scope:
            lines.append(f"- {scope}")
        
        if release.release_notes:
            lines.extend([
                "",
                "## 详细说明",
                "",
                release.release_notes
            ])
        
        return "\n".join(lines)

# 全局实例
_release_manager = None

def get_release_manager() -> ReleaseManager:
    global _release_manager
    if _release_manager is None:
        _release_manager = ReleaseManager()
    return _release_manager

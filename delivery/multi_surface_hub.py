#!/usr/bin/env python3
"""
多端交付中心 - V2.8.0

支持的交付入口：
- Web 端
- API 端
- 命令端 / 脚本端
- 文件投递端

统一：
- 入口协议
- 权限校验
- 任务触发方式
- 输出结果格式
- 错误处理方式
- 审计记录方式
"""

import json
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

from infrastructure.path_resolver import get_project_root

class DeliverySurface(Enum):
    WEB = "web"                 # Web 端
    API = "api"                 # API 端
    CLI = "cli"                 # 命令端
    FILE = "file"               # 文件投递端

class RequestStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class DeliveryRequest:
    """交付请求"""
    request_id: str
    surface: str
    action: str
    params: Dict[str, Any]
    auth_token: str
    workspace_id: str
    status: str
    created_at: str
    completed_at: Optional[str]
    result: Optional[Dict]
    error: Optional[str]

@dataclass
class DeliveryResponse:
    """交付响应"""
    request_id: str
    status: str
    result: Optional[Dict]
    error: Optional[str]
    audit_id: str

class MultiSurfaceDeliveryHub:
    """多端交付中心"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.delivery_path = self.project_root / 'delivery'
        self.registry_path = self.delivery_path / 'delivery_registry.json'
        
        self.requests: Dict[str, DeliveryRequest] = []
        self.audit_log: List[Dict] = []
        
        # 统一协议定义
        self.protocol = {
            "version": "1.0",
            "request_format": {
                "action": "string (required)",
                "params": "dict (optional)",
                "auth_token": "string (required)",
                "workspace_id": "string (required)"
            },
            "response_format": {
                "request_id": "string",
                "status": "string",
                "result": "dict (optional)",
                "error": "string (optional)"
            },
            "error_codes": {
                "AUTH_FAILED": "认证失败",
                "PERMISSION_DENIED": "权限不足",
                "INVALID_REQUEST": "请求格式错误",
                "WORKSPACE_NOT_FOUND": "工作区不存在",
                "EXECUTION_FAILED": "执行失败"
            }
        }
        
        self._load()
    
    def _load(self):
        """加载注册表"""
        if self.registry_path.exists():
            data = json.loads(self.registry_path.read_text(encoding='utf-8'))
            self.requests = [DeliveryRequest(**r) for r in data.get("requests", [])]
            self.audit_log = data.get("audit_log", [])
    
    def _save(self):
        """保存注册表"""
        self.delivery_path.mkdir(parents=True, exist_ok=True)
        data = {
            "requests": [asdict(r) for r in self.requests[-1000:]],  # 保留最近1000条
            "audit_log": self.audit_log[-1000:],
            "updated": datetime.now().isoformat()
        }
        self.registry_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def _generate_request_id(self, surface: str) -> str:
        """生成请求ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f"req_{surface}_{timestamp}"
    
    def _generate_audit_id(self) -> str:
        """生成审计ID"""
        return f"audit_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def _validate_request(self, request: Dict) -> tuple:
        """验证请求"""
        # 检查必需字段
        required = ["action", "auth_token", "workspace_id"]
        for field in required:
            if field not in request:
                return False, f"缺少必需字段: {field}"
        
        # 验证 action 格式
        action = request.get("action", "")
        if not action or not isinstance(action, str):
            return False, "action 必须是非空字符串"
        
        return True, "验证通过"
    
    def _authenticate(self, auth_token: str, workspace_id: str) -> tuple:
        """认证"""
        # 简化实现：检查 token 格式
        if not auth_token or len(auth_token) < 10:
            return False, "AUTH_FAILED"
        
        return True, "认证通过"
    
    def _check_permission(self, auth_token: str, action: str, workspace_id: str) -> tuple:
        """检查权限"""
        # 简化实现：默认允许
        return True, "权限检查通过"
    
    def _audit(self, request_id: str, surface: str, action: str,
               status: str, error: str = None):
        """记录审计日志"""
        audit_id = self._generate_audit_id()
        
        self.audit_log.append({
            "audit_id": audit_id,
            "request_id": request_id,
            "surface": surface,
            "action": action,
            "status": status,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save()
        return audit_id
    
    def submit_request(self, surface: str, request: Dict) -> DeliveryResponse:
        """提交请求（统一入口）"""
        request_id = self._generate_request_id(surface)
        
        # 1. 验证请求格式
        valid, msg = self._validate_request(request)
        if not valid:
            audit_id = self._audit(request_id, surface, request.get("action", ""), "INVALID_REQUEST", msg)
            return DeliveryResponse(
                request_id=request_id,
                status=RequestStatus.FAILED.value,
                result=None,
                error=f"INVALID_REQUEST: {msg}",
                audit_id=audit_id
            )
        
        # 2. 认证
        auth_token = request.get("auth_token", "")
        workspace_id = request.get("workspace_id", "")
        
        auth_valid, auth_msg = self._authenticate(auth_token, workspace_id)
        if not auth_valid:
            audit_id = self._audit(request_id, surface, request.get("action"), "AUTH_FAILED", auth_msg)
            return DeliveryResponse(
                request_id=request_id,
                status=RequestStatus.FAILED.value,
                result=None,
                error=f"AUTH_FAILED: {auth_msg}",
                audit_id=audit_id
            )
        
        # 3. 权限检查
        action = request.get("action")
        perm_valid, perm_msg = self._check_permission(auth_token, action, workspace_id)
        if not perm_valid:
            audit_id = self._audit(request_id, surface, action, "PERMISSION_DENIED", perm_msg)
            return DeliveryResponse(
                request_id=request_id,
                status=RequestStatus.FAILED.value,
                result=None,
                error=f"PERMISSION_DENIED: {perm_msg}",
                audit_id=audit_id
            )
        
        # 4. 创建请求记录
        delivery_request = DeliveryRequest(
            request_id=request_id,
            surface=surface,
            action=action,
            params=request.get("params", {}),
            auth_token=auth_token[:10] + "...",  # 脱敏
            workspace_id=workspace_id,
            status=RequestStatus.PROCESSING.value,
            created_at=datetime.now().isoformat(),
            completed_at=None,
            result=None,
            error=None
        )
        
        self.requests.append(delivery_request)
        
        # 5. 执行请求
        result = self._execute_request(delivery_request)
        
        # 6. 更新状态
        delivery_request.status = result.get("status", RequestStatus.COMPLETED.value)
        delivery_request.result = result.get("result")
        delivery_request.error = result.get("error")
        delivery_request.completed_at = datetime.now().isoformat()
        
        # 7. 审计
        audit_id = self._audit(request_id, surface, action, delivery_request.status, delivery_request.error)
        
        self._save()
        
        return DeliveryResponse(
            request_id=request_id,
            status=delivery_request.status,
            result=delivery_request.result,
            error=delivery_request.error,
            audit_id=audit_id
        )
    
    def _execute_request(self, request: DeliveryRequest) -> Dict:
        """执行请求"""
        # 简化实现：返回模拟结果
        return {
            "status": RequestStatus.COMPLETED.value,
            "result": {
                "action": request.action,
                "message": f"操作已执行: {request.action}",
                "surface": request.surface
            }
        }
    
    # 各端入口方法
    def web_request(self, request: Dict) -> DeliveryResponse:
        """Web 端请求"""
        return self.submit_request(DeliverySurface.WEB.value, request)
    
    def api_request(self, request: Dict) -> DeliveryResponse:
        """API 端请求"""
        return self.submit_request(DeliverySurface.API.value, request)
    
    def cli_request(self, request: Dict) -> DeliveryResponse:
        """命令端请求"""
        return self.submit_request(DeliverySurface.CLI.value, request)
    
    def file_request(self, request: Dict) -> DeliveryResponse:
        """文件投递端请求"""
        return self.submit_request(DeliverySurface.FILE.value, request)
    
    def get_request_status(self, request_id: str) -> Optional[Dict]:
        """获取请求状态"""
        for req in self.requests:
            if req.request_id == request_id:
                return {
                    "request_id": req.request_id,
                    "status": req.status,
                    "created_at": req.created_at,
                    "completed_at": req.completed_at,
                    "error": req.error
                }
        return None
    
    def get_surface_stats(self) -> Dict[str, Dict]:
        """获取各端统计"""
        stats = {surface.value: {"total": 0, "success": 0, "failed": 0} for surface in DeliverySurface}
        
        for req in self.requests:
            stats[req.surface]["total"] += 1
            if req.status == RequestStatus.COMPLETED.value:
                stats[req.surface]["success"] += 1
            elif req.status == RequestStatus.FAILED.value:
                stats[req.surface]["failed"] += 1
        
        return stats
    
    def get_report(self) -> str:
        """生成报告"""
        stats = self.get_surface_stats()
        
        lines = [
            "# 多端交付报告",
            "",
            "## 各端统计",
            ""
        ]
        
        for surface, stat in stats.items():
            lines.append(f"- **{surface}**: 总计 {stat['total']}, 成功 {stat['success']}, 失败 {stat['failed']}")
        
        lines.extend([
            "",
            "## 最近请求",
            ""
        ])
        
        for req in self.requests[-10:]:
            status = "✅" if req.status == RequestStatus.COMPLETED.value else "❌"
            lines.append(f"- {status} [{req.surface}] {req.action} ({req.request_id})")
        
        return "\n".join(lines)

# 全局实例
_delivery_hub = None

def get_delivery_hub() -> MultiSurfaceDeliveryHub:
    global _delivery_hub
    if _delivery_hub is None:
        _delivery_hub = MultiSurfaceDeliveryHub()
    return _delivery_hub

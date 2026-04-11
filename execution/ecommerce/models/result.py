"""结果记录结构 - V4.3.0

统一记录合作结果，支持后续分析
"""

from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ContactResult(Enum):
    """联系结果"""
    NO_RESPONSE = "no_response"      # 未回复
    REPLIED = "replied"              # 已回复
    INTERESTED = "interested"        # 感兴趣
    NOT_INTERESTED = "not_interested"  # 不感兴趣

class SampleResult(Enum):
    """寄样结果"""
    NOT_SENT = "not_sent"            # 未寄样
    SENT = "sent"                    # 已寄样
    RECEIVED = "received"            # 已收到
    REJECTED = "rejected"            # 拒收

class LiveResult(Enum):
    """直播结果"""
    NOT_STARTED = "not_started"      # 未开始
    LIVE = "live"                    # 直播中
    COMPLETED = "completed"          # 已完成
    CANCELLED = "cancelled"          # 已取消

@dataclass
class CooperationResult:
    """合作结果记录"""
    # 基础信息
    result_id: str                           # 结果ID
    lead_id: str                             # 线索ID
    lead_name: str                           # 团长/达人名称
    
    # 联系结果
    contact_result: ContactResult = ContactResult.NO_RESPONSE
    contact_time: Optional[datetime] = None
    
    # 寄样结果
    sample_result: SampleResult = SampleResult.NOT_SENT
    sample_time: Optional[datetime] = None
    
    # 建联结果
    connection_success: bool = False
    connection_time: Optional[datetime] = None
    
    # 直播结果
    live_result: LiveResult = LiveResult.NOT_STARTED
    live_time: Optional[datetime] = None
    
    # 出单结果
    has_order: bool = False
    order_count: int = 0
    order_gmv: float = 0.0
    
    # ROI/投产
    cost: float = 0.0                        # 成本
    revenue: float = 0.0                     # 收入
    roi: float = 0.0                         # ROI
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calc_roi(self):
        """计算ROI"""
        if self.cost > 0:
            self.roi = self.revenue / self.cost
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "result_id": self.result_id,
            "lead_id": self.lead_id,
            "lead_name": self.lead_name,
            "contact_result": self.contact_result.value,
            "sample_result": self.sample_result.value,
            "connection_success": self.connection_success,
            "live_result": self.live_result.value,
            "has_order": self.has_order,
            "order_count": self.order_count,
            "order_gmv": self.order_gmv,
            "roi": round(self.roi, 2)
        }

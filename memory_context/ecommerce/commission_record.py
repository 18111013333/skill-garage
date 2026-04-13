"""佣金记录"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class SettlementStatus(Enum):
    PENDING = "待结算"
    PROCESSING = "处理中"
    COMPLETED = "已完成"
    FAILED = "失败"

@dataclass
class CommissionRecord:
    """佣金记录"""
    record_id: str
    leader_id: str
    leader_name: str
    period_start: datetime
    period_end: datetime
    total_sales: float
    total_commission: float
    order_count: int
    status: SettlementStatus = SettlementStatus.PENDING
    paid_at: Optional[datetime] = None
    payment_method: str = ""
    transaction_id: str = ""
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)

@dataclass  
class CommissionHistory:
    """佣金历史"""
    records: List[CommissionRecord] = field(default_factory=list)
    
    def add(self, record: CommissionRecord):
        """添加记录"""
        self.records.append(record)
    
    def get_by_leader(self, leader_id: str) -> List[CommissionRecord]:
        """按团长查询"""
        return [r for r in self.records if r.leader_id == leader_id]
    
    def get_pending(self) -> List[CommissionRecord]:
        """获取待结算"""
        return [r for r in self.records if r.status == SettlementStatus.PENDING]
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        return {
            "total_records": len(self.records),
            "total_commission": sum(r.total_commission for r in self.records),
            "pending_commission": sum(r.total_commission for r in self.records 
                                       if r.status == SettlementStatus.PENDING),
            "paid_commission": sum(r.total_commission for r in self.records 
                                    if r.status == SettlementStatus.COMPLETED)
        }

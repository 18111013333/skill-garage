"""订单历史"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "待付款"
    PAID = "已付款"
    SHIPPED = "已发货"
    DELIVERED = "已签收"
    CANCELLED = "已取消"
    REFUNDED = "已退款"

@dataclass
class OrderRecord:
    """订单记录"""
    order_id: str
    platform: str
    leader_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    commission_rate: float
    commission_amount: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

@dataclass
class OrderHistory:
    """订单历史"""
    records: List[OrderRecord] = field(default_factory=list)
    
    def add(self, order: OrderRecord):
        """添加订单"""
        self.records.append(order)
    
    def get_by_leader(self, leader_id: str) -> List[OrderRecord]:
        """按团长查询"""
        return [r for r in self.records if r.leader_id == leader_id]
    
    def get_by_period(self, start: datetime, end: datetime) -> List[OrderRecord]:
        """按时间查询"""
        return [r for r in self.records if start <= r.created_at <= end]
    
    def calculate_commission(self, leader_id: str, start: datetime, end: datetime) -> Dict:
        """计算佣金"""
        orders = [r for r in self.records 
                  if r.leader_id == leader_id and start <= r.created_at <= end]
        
        return {
            "leader_id": leader_id,
            "period": f"{start} - {end}",
            "order_count": len(orders),
            "total_sales": sum(o.total_amount for o in orders),
            "total_commission": sum(o.commission_amount for o in orders)
        }
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        return {
            "total_orders": len(self.records),
            "total_sales": sum(r.total_amount for r in self.records),
            "total_commission": sum(r.commission_amount for r in self.records),
            "by_status": {
                status.value: len([r for r in self.records if r.status == status])
                for status in OrderStatus
            }
        }

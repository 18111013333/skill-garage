"""订单执行器 - 处理订单相关操作"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@dataclass
class Order:
    """订单数据结构"""
    order_id: str
    leader_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    commission_rate: float
    commission_amount: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class OrderExecutor:
    """订单执行器"""
    
    def __init__(self):
        self.orders: List[Order] = []
    
    def create(self, order_data: Dict) -> Order:
        """创建订单"""
        order = Order(
            order_id=order_data.get("order_id", f"O{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            leader_id=order_data["leader_id"],
            product_name=order_data["product_name"],
            quantity=order_data["quantity"],
            unit_price=order_data["unit_price"],
            total_amount=order_data["quantity"] * order_data["unit_price"],
            commission_rate=order_data["commission_rate"],
            commission_amount=order_data["quantity"] * order_data["unit_price"] * order_data["commission_rate"] / 100
        )
        self.orders.append(order)
        return order
    
    def calculate_commission(self, leader_id: str, period_start: datetime, period_end: datetime) -> Dict:
        """计算佣金"""
        filtered = [
            o for o in self.orders
            if o.leader_id == leader_id and period_start <= o.created_at <= period_end
        ]
        total_sales = sum(o.total_amount for o in filtered)
        total_commission = sum(o.commission_amount for o in filtered)
        
        return {
            "leader_id": leader_id,
            "period": f"{period_start} - {period_end}",
            "order_count": len(filtered),
            "total_sales": total_sales,
            "total_commission": total_commission
        }
    
    def get_statistics(self, leader_id: str = None) -> Dict:
        """获取统计"""
        orders = self.orders if not leader_id else [o for o in self.orders if o.leader_id == leader_id]
        
        return {
            "total_orders": len(orders),
            "total_sales": sum(o.total_amount for o in orders),
            "total_commission": sum(o.commission_amount for o in orders),
            "avg_order_value": sum(o.total_amount for o in orders) / len(orders) if orders else 0
        }

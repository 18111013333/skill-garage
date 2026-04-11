"""团长画像"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class LeaderLevel(Enum):
    BRONZE = "青铜"
    SILVER = "白银"
    GOLD = "黄金"
    DIAMOND = "钻石"

@dataclass
class LeaderProfile:
    """团长画像"""
    leader_id: str
    name: str
    region: str
    category: str
    followers: int = 0
    monthly_sales: float = 0.0
    rating: float = 5.0
    level: LeaderLevel = LeaderLevel.BRONZE
    
    # 联系方式
    contact: str = ""
    wechat: str = ""
    
    # 合作信息
    commission_rate: float = 0.0
    settlement_cycle: str = "月结"
    cooperation_start: Optional[datetime] = None
    
    # 历史数据
    total_orders: int = 0
    total_sales: float = 0.0
    total_commission: float = 0.0
    
    # 评价
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calculate_level(self) -> LeaderLevel:
        """计算等级"""
        if self.monthly_sales >= 100000:
            return LeaderLevel.DIAMOND
        elif self.monthly_sales >= 50000:
            return LeaderLevel.GOLD
        elif self.monthly_sales >= 10000:
            return LeaderLevel.SILVER
        return LeaderLevel.BRONZE
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "leader_id": self.leader_id,
            "name": self.name,
            "region": self.region,
            "category": self.category,
            "followers": self.followers,
            "monthly_sales": self.monthly_sales,
            "rating": self.rating,
            "level": self.level.value,
            "contact": self.contact,
            "wechat": self.wechat,
            "commission_rate": self.commission_rate,
            "settlement_cycle": self.settlement_cycle,
            "total_orders": self.total_orders,
            "total_sales": self.total_sales,
            "total_commission": self.total_commission,
            "tags": self.tags,
            "notes": self.notes
        }

"""达人画像"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class Platform(Enum):
    DOUYIN = "抖音"
    KUAISHOU = "快手"
    XIAOHONGSHU = "小红书"
    SHIPINHAO = "视频号"
    BILIBILI = "B站"

class CooperationType(Enum):
    PURE_COMMISSION = "纯佣"
    MIXED = "混合"
    ANNUAL = "年框"

@dataclass
class InfluencerProfile:
    """达人画像"""
    influencer_id: str
    name: str
    platform: Platform
    category: str
    
    # 账号数据
    followers: int = 0
    avg_views: int = 0
    engagement_rate: float = 0.0
    
    # 合作信息
    cooperation_type: CooperationType = CooperationType.PURE_COMMISSION
    commission_rate: float = 15.0
    price_per_video: float = 0.0
    
    # 联系方式
    contact: str = ""
    wechat: str = ""
    
    # 历史数据
    total_cooperations: int = 0
    total_sales: float = 0.0
    avg_conversion_rate: float = 0.0
    
    # 评价
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calculate_score(self) -> float:
        """计算综合评分"""
        score = (
            min(self.followers / 100000, 1) * 0.25 +
            min(self.engagement_rate / 10, 1) * 0.35 +
            min(self.avg_views / 10000, 1) * 0.25 +
            (1 - min(self.commission_rate / 30, 1)) * 0.15
        )
        return round(score, 2)
    
    def to_dict(self) -> Dict:
        return {
            "influencer_id": self.influencer_id,
            "name": self.name,
            "platform": self.platform.value,
            "category": self.category,
            "followers": self.followers,
            "avg_views": self.avg_views,
            "engagement_rate": self.engagement_rate,
            "cooperation_type": self.cooperation_type.value,
            "commission_rate": self.commission_rate,
            "price_per_video": self.price_per_video,
            "contact": self.contact,
            "total_cooperations": self.total_cooperations,
            "total_sales": self.total_sales,
            "score": self.calculate_score(),
            "tags": self.tags
        }

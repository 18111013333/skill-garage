"""统一线索对象 - V4.3.0

电商闭环核心数据结构
"""

from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class LeadStatus(Enum):
    """线索状态"""
    NEW = "new"                    # 新线索
    CONTACTED = "contacted"        # 已联系
    RESPONDED = "responded"        # 已回复
    SAMPLED = "sampled"            # 已寄样
    COOPERATING = "cooperating"    # 合作中
    COMPLETED = "completed"        # 已完成
    FAILED = "failed"              # 失败

class RiskTag(Enum):
    """风险标签"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Lead:
    """统一线索对象"""
    # 基础信息
    lead_id: str                              # 线索ID
    name: str                                 # 团长/达人名称
    platform: str                             # 平台 (抖音/快手/小红书)
    
    # 渠道来源
    source: str = ""                          # 来源渠道
    source_url: str = ""                      # 来源链接
    
    # 联系方式
    contact_wechat: str = ""                  # 微信
    contact_phone: str = ""                   # 电话
    contact_other: str = ""                   # 其他联系方式
    
    # 历史沟通状态
    status: LeadStatus = LeadStatus.NEW
    last_contact_time: Optional[datetime] = None
    contact_count: int = 0
    response_count: int = 0
    
    # 类目匹配度
    category_match_score: float = 0.0         # 类目匹配分数 (0-1)
    matched_categories: List[str] = field(default_factory=list)
    
    # 预估成交能力
    estimated_gmv: float = 0.0                # 预估GMV
    follower_count: int = 0                   # 粉丝数
    avg_views: int = 0                        # 平均观看
    avg_sales: int = 0                        # 平均销量
    
    # 风险标签
    risk_tag: RiskTag = RiskTag.NONE
    risk_reasons: List[str] = field(default_factory=list)
    
    # 综合评分
    total_score: float = 0.0                  # 综合分数
    priority: int = 0                         # 优先级
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update_status(self, new_status: LeadStatus):
        """更新状态"""
        self.status = new_status
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "lead_id": self.lead_id,
            "name": self.name,
            "platform": self.platform,
            "source": self.source,
            "status": self.status.value,
            "category_match_score": self.category_match_score,
            "estimated_gmv": self.estimated_gmv,
            "risk_tag": self.risk_tag.value,
            "total_score": self.total_score,
            "priority": self.priority
        }

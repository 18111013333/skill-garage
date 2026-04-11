"""团长执行器 - 处理团长相关操作"""

from typing import Dict, List, Any
from dataclasses import dataclass
import json

@dataclass
class Leader:
    """团长数据结构"""
    leader_id: str
    name: str
    region: str
    category: str
    followers: int
    monthly_sales: float
    rating: float
    contact: str = ""
    wechat: str = ""

class LeaderExecutor:
    """团长执行器"""
    
    def __init__(self):
        self.leaders: List[Leader] = []
    
    def search(self, category: str, region: str = None, followers_min: int = 0) -> List[Dict]:
        """搜索团长"""
        # 实际实现会调用平台API
        return [
            {
                "leader_id": f"L{i:03d}",
                "name": f"{category}团长{i}",
                "region": region or "全国",
                "category": category,
                "followers": followers_min + 1000 * (10 - i),
                "monthly_sales": 50000 * (10 - i),
                "rating": 4.5 + 0.1 * (5 - i)
            }
            for i in range(1, 11)
        ]
    
    def evaluate(self, leader: Dict) -> float:
        """评估团长价值"""
        score = (
            min(leader["followers"] / 10000, 1) * 0.3 +
            min(leader["monthly_sales"] / 100000, 1) * 0.4 +
            (leader["rating"] / 5) * 0.3
        )
        return round(score, 2)
    
    def rank(self, leaders: List[Dict], top_n: int = 10) -> List[Dict]:
        """排名"""
        scored = [{**l, "score": self.evaluate(l)} for l in leaders]
        return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_n]
    
    def generate_proposal(self, leader: Dict, commission_rate: float) -> Dict:
        """生成合作方案"""
        return {
            "leader": leader["name"],
            "commission_rate": f"{commission_rate}%",
            "settlement": "月结",
            "support": ["产品素材", "样品", "售后支持"],
            "kpi": {
                "min_sales": "月销售额≥1万",
                "min_videos": "月发布≥4条"
            }
        }

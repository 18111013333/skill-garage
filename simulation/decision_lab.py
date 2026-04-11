#!/usr/bin/env python3
"""
决策模拟与预演实验室 - V2.8.1

能力：
- 方案 A/B/C 对比
- 风险预估
- 资源消耗预估
- 时间影响预估
- 失败路径模拟
- 最好/最坏/基线场景输出
- 关键决策建议摘要
- 决策前后差异分析
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import random

from infrastructure.path_resolver import get_project_root

class ScenarioType(Enum):
    BEST = "best"               # 最好场景
    BASELINE = "baseline"       # 基线场景
    WORST = "worst"             # 最坏场景

class DecisionStatus(Enum):
    DRAFT = "draft"             # 草稿
    SIMULATING = "simulating"   # 模拟中
    COMPLETED = "completed"     # 已完成
    DECIDED = "decided"         # 已决策

@dataclass
class DecisionOption:
    """决策选项"""
    option_id: str
    name: str
    description: str
    estimated_cost: float
    estimated_time: int             # 天
    estimated_risk: float           # 0-1
    estimated_value: float
    required_resources: Dict
    dependencies: List[str]
    pros: List[str]
    cons: List[str]

@dataclass
class SimulationResult:
    """模拟结果"""
    result_id: str
    option_id: str
    scenario_type: str
    success_probability: float
    cost_variance: float            # 成本偏差
    time_variance: float            # 时间偏差
    risk_score: float
    expected_value: float
    failure_paths: List[Dict]
    key_factors: List[str]
    recommendations: List[str]

@dataclass
class DecisionCase:
    """决策案例"""
    case_id: str
    name: str
    description: str
    context: Dict
    options: List[Dict]             # DecisionOption 列表
    simulation_results: List[Dict]  # SimulationResult 列表
    selected_option: Optional[str]
    status: str
    created_at: str
    decided_at: Optional[str]
    audit_trail: List[Dict]

class DecisionSimulationLab:
    """决策模拟与预演实验室"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.simulation_path = self.project_root / 'simulation'
        self.config_path = self.simulation_path / 'simulation_config.json'
        
        # 决策案例
        self.cases: Dict[str, DecisionCase] = {}
        
        # 模拟结果
        self.results: List[SimulationResult] = []
        
        self._load()
    
    def _load(self):
        """加载配置"""
        if self.config_path.exists():
            data = json.loads(self.config_path.read_text(encoding='utf-8'))
            
            for cid, case in data.get("cases", {}).items():
                self.cases[cid] = DecisionCase(**case)
            
            self.results = [SimulationResult(**r) for r in data.get("results", [])]
    
    def _save(self):
        """保存配置"""
        self.simulation_path.mkdir(parents=True, exist_ok=True)
        data = {
            "cases": {cid: asdict(c) for cid, c in self.cases.items()},
            "results": [asdict(r) for r in self.results],
            "updated": datetime.now().isoformat()
        }
        self.config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def _generate_case_id(self) -> str:
        """生成案例ID"""
        return f"case_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _generate_option_id(self) -> str:
        """生成选项ID"""
        return f"opt_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    # === 决策案例管理 ===
    def create_case(self, name: str, description: str,
                    context: Dict = None) -> DecisionCase:
        """创建决策案例"""
        case_id = self._generate_case_id()
        
        case = DecisionCase(
            case_id=case_id,
            name=name,
            description=description,
            context=context or {},
            options=[],
            simulation_results=[],
            selected_option=None,
            status=DecisionStatus.DRAFT.value,
            created_at=datetime.now().isoformat(),
            decided_at=None,
            audit_trail=[]
        )
        
        self.cases[case_id] = case
        self._save()
        
        return case
    
    def add_option(self, case_id: str, name: str, description: str,
                   estimated_cost: float, estimated_time: int,
                   estimated_risk: float, estimated_value: float,
                   required_resources: Dict = None,
                   pros: List[str] = None, cons: List[str] = None) -> Dict:
        """添加决策选项"""
        if case_id not in self.cases:
            return {"error": "案例不存在"}
        
        option_id = self._generate_option_id()
        
        option = {
            "option_id": option_id,
            "name": name,
            "description": description,
            "estimated_cost": estimated_cost,
            "estimated_time": estimated_time,
            "estimated_risk": estimated_risk,
            "estimated_value": estimated_value,
            "required_resources": required_resources or {},
            "dependencies": [],
            "pros": pros or [],
            "cons": cons or []
        }
        
        self.cases[case_id].options.append(option)
        self._save()
        
        return option
    
    def get_case(self, case_id: str) -> Optional[DecisionCase]:
        """获取案例"""
        return self.cases.get(case_id)
    
    # === 模拟执行 ===
    def simulate_option(self, case_id: str, option_id: str,
                        scenario_type: str = "baseline") -> SimulationResult:
        """模拟选项"""
        case = self.get_case(case_id)
        if not case:
            raise ValueError("案例不存在")
        
        # 找到选项
        option = None
        for opt in case.options:
            if opt["option_id"] == option_id:
                option = opt
                break
        
        if not option:
            raise ValueError("选项不存在")
        
        # 执行模拟
        result = self._run_simulation(option, scenario_type)
        
        # 保存结果
        self.results.append(result)
        case.simulation_results.append(asdict(result))
        case.status = DecisionStatus.SIMULATING.value
        self._save()
        
        return result
    
    def _run_simulation(self, option: Dict, scenario_type: str) -> SimulationResult:
        """执行模拟"""
        # 基础参数
        base_cost = option["estimated_cost"]
        base_time = option["estimated_time"]
        base_risk = option["estimated_risk"]
        base_value = option["estimated_value"]
        
        # 根据场景类型调整
        if scenario_type == ScenarioType.BEST.value:
            cost_variance = random.uniform(-0.2, 0.0)
            time_variance = random.uniform(-0.3, 0.0)
            risk_modifier = 0.7
            value_modifier = 1.2
        elif scenario_type == ScenarioType.WORST.value:
            cost_variance = random.uniform(0.0, 0.5)
            time_variance = random.uniform(0.0, 0.8)
            risk_modifier = 1.5
            value_modifier = 0.6
        else:  # baseline
            cost_variance = random.uniform(-0.1, 0.1)
            time_variance = random.uniform(-0.1, 0.1)
            risk_modifier = 1.0
            value_modifier = 1.0
        
        # 计算结果
        adjusted_risk = min(1.0, base_risk * risk_modifier)
        success_probability = 1.0 - adjusted_risk
        expected_value = base_value * value_modifier * success_probability
        
        # 生成失败路径
        failure_paths = []
        if adjusted_risk > 0.3:
            failure_paths.append({
                "path": "资源不足",
                "probability": adjusted_risk * 0.4,
                "impact": "项目延期"
            })
        if adjusted_risk > 0.5:
            failure_paths.append({
                "path": "技术障碍",
                "probability": adjusted_risk * 0.3,
                "impact": "成本超支"
            })
        
        # 关键因素
        key_factors = []
        if option["estimated_cost"] > 10000:
            key_factors.append("成本控制")
        if option["estimated_time"] > 30:
            key_factors.append("时间管理")
        if option["estimated_risk"] > 0.5:
            key_factors.append("风险缓解")
        
        # 建议
        recommendations = []
        if adjusted_risk > 0.5:
            recommendations.append("建议增加风险缓解措施")
        if cost_variance > 0.2:
            recommendations.append("建议预留成本缓冲")
        if time_variance > 0.3:
            recommendations.append("建议制定备选时间计划")
        
        result = SimulationResult(
            result_id=f"sim_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            option_id=option["option_id"],
            scenario_type=scenario_type,
            success_probability=success_probability,
            cost_variance=cost_variance,
            time_variance=time_variance,
            risk_score=adjusted_risk,
            expected_value=expected_value,
            failure_paths=failure_paths,
            key_factors=key_factors,
            recommendations=recommendations
        )
        
        return result
    
    def simulate_all_scenarios(self, case_id: str, option_id: str) -> List[SimulationResult]:
        """模拟所有场景"""
        results = []
        for scenario in ScenarioType:
            result = self.simulate_option(case_id, option_id, scenario.value)
            results.append(result)
        return results
    
    # === 方案对比 ===
    def compare_options(self, case_id: str) -> Dict:
        """对比所有选项"""
        case = self.get_case(case_id)
        if not case:
            return {"error": "案例不存在"}
        
        comparison = {
            "case_id": case_id,
            "options": [],
            "recommendation": None
        }
        
        best_score = -1
        best_option = None
        
        for option in case.options:
            # 获取基线模拟结果
            baseline_result = None
            for result in case.simulation_results:
                if (result["option_id"] == option["option_id"] and
                    result["scenario_type"] == ScenarioType.BASELINE.value):
                    baseline_result = result
                    break
            
            # 计算综合分数
            if baseline_result:
                score = (
                    baseline_result["success_probability"] * 40 +
                    (1 - baseline_result["risk_score"]) * 30 +
                    (baseline_result["expected_value"] / 10000) * 30
                )
            else:
                score = 0
            
            option_summary = {
                "option_id": option["option_id"],
                "name": option["name"],
                "estimated_cost": option["estimated_cost"],
                "estimated_time": option["estimated_time"],
                "estimated_risk": option["estimated_risk"],
                "score": score
            }
            
            comparison["options"].append(option_summary)
            
            if score > best_score:
                best_score = score
                best_option = option
        
        if best_option:
            comparison["recommendation"] = {
                "option_id": best_option["option_id"],
                "name": best_option["name"],
                "score": best_score,
                "reason": "综合评分最高"
            }
        
        return comparison
    
    # === 决策执行 ===
    def make_decision(self, case_id: str, option_id: str,
                      reason: str = "") -> Dict:
        """做出决策"""
        case = self.get_case(case_id)
        if not case:
            return {"error": "案例不存在"}
        
        case.selected_option = option_id
        case.status = DecisionStatus.DECIDED.value
        case.decided_at = datetime.now().isoformat()
        case.audit_trail.append({
            "event": "decided",
            "option_id": option_id,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save()
        
        return {
            "status": "decided",
            "case_id": case_id,
            "selected_option": option_id
        }
    
    # === 决策前后差异分析 ===
    def analyze_decision_impact(self, case_id: str) -> Dict:
        """分析决策影响"""
        case = self.get_case(case_id)
        if not case or not case.selected_option:
            return {"error": "案例不存在或未决策"}
        
        # 找到选中的选项
        selected = None
        for option in case.options:
            if option["option_id"] == case.selected_option:
                selected = option
                break
        
        if not selected:
            return {"error": "选中的选项不存在"}
        
        # 对比其他选项
        alternatives = []
        for option in case.options:
            if option["option_id"] != case.selected_option:
                diff = {
                    "option_id": option["option_id"],
                    "name": option["name"],
                    "cost_diff": option["estimated_cost"] - selected["estimated_cost"],
                    "time_diff": option["estimated_time"] - selected["estimated_time"],
                    "risk_diff": option["estimated_risk"] - selected["estimated_risk"],
                    "value_diff": option["estimated_value"] - selected["estimated_value"]
                }
                alternatives.append(diff)
        
        return {
            "case_id": case_id,
            "selected_option": {
                "option_id": selected["option_id"],
                "name": selected["name"]
            },
            "alternatives": alternatives,
            "summary": f"选择了 {selected['name']}，相比其他选项节省成本 {sum(a['cost_diff'] for a in alternatives if a['cost_diff'] > 0):.0f}"
        }
    
    # === 报告 ===
    def get_report(self) -> str:
        """生成报告"""
        lines = [
            "# 决策模拟报告",
            f"\n生成时间: {datetime.now().isoformat()}",
            "",
            "## 决策案例",
            ""
        ]
        
        for case in self.cases.values():
            status = "✅" if case.status == DecisionStatus.DECIDED.value else "📝"
            lines.append(f"- {status} **{case.name}** ({case.status})")
            lines.append(f"  - 选项数: {len(case.options)}")
            lines.append(f"  - 模拟次数: {len(case.simulation_results)}")
        
        lines.extend([
            "",
            "## 最近模拟结果",
            ""
        ])
        
        for result in self.results[-5:]:
            lines.append(f"- [{result.scenario_type}] 成功率: {result.success_probability*100:.1f}%, 风险: {result.risk_score*100:.1f}%")
        
        return "\n".join(lines)

# 全局实例
_decision_lab = None

def get_decision_lab() -> DecisionSimulationLab:
    global _decision_lab
    if _decision_lab is None:
        _decision_lab = DecisionSimulationLab()
    return _decision_lab

#!/usr/bin/env python3
"""
工作流注册表 - V2.8.0
"""

from typing import Dict, Type, Optional
from orchestration.workflows.workflow_base import WorkflowBase

# 导入所有工作流
from orchestration.workflows.ecommerce_product_analysis import EcommerceProductAnalysisWorkflow
from orchestration.workflows.factory_comparison import FactoryComparisonWorkflow
from orchestration.workflows.partner_selection import PartnerSelectionWorkflow
from orchestration.workflows.store_launch import StoreLaunchWorkflow
from orchestration.workflows.file_organization import FileOrganizationWorkflow
from orchestration.workflows.code_audit import CodeAuditWorkflow

# 工作流注册表
WORKFLOW_REGISTRY: Dict[str, Type[WorkflowBase]] = {
    "ecommerce_product_analysis": EcommerceProductAnalysisWorkflow,
    "factory_comparison": FactoryComparisonWorkflow,
    "partner_selection": PartnerSelectionWorkflow,
    "store_launch": StoreLaunchWorkflow,
    "file_organization": FileOrganizationWorkflow,
    "code_audit": CodeAuditWorkflow,
}

def get_workflow(name: str) -> Optional[WorkflowBase]:
    """获取工作流实例"""
    workflow_class = WORKFLOW_REGISTRY.get(name)
    if workflow_class:
        return workflow_class()
    return None

def list_workflows() -> Dict[str, Dict]:
    """列出所有工作流"""
    return {
        name: {
            "description": cls.description,
            "version": cls.version,
            "scenarios": cls.applicable_scenarios,
            "required_skills": cls.required_skills
        }
        for name, cls in WORKFLOW_REGISTRY.items()
    }

def execute_workflow(name: str, input_data: dict):
    """执行工作流"""
    workflow = get_workflow(name)
    if not workflow:
        return {"error": f"工作流不存在: {name}"}
    return workflow.execute(input_data)

"""验证器模块 - V4.3.0"""

from typing import Dict
from .architecture_validator import ArchitectureValidator
from .registry_validator import RegistryValidator
from .ecommerce_validator import EcommerceValidator

class ValidationRunner:
    """验证运行器"""
    
    def __init__(self, workspace_path: str = None):
        self.arch_validator = ArchitectureValidator(workspace_path)
        self.reg_validator = RegistryValidator(workspace_path)
        self.ecom_validator = EcommerceValidator(workspace_path)
    
    def run_all(self) -> Dict:
        """运行所有验证"""
        results = {
            "architecture": self.arch_validator.validate(),
            "registry": self.reg_validator.validate(),
            "ecommerce": self.ecom_validator.validate()
        }
        
        # 汇总
        all_valid = all(r.get("valid", False) for r in results.values())
        total_violations = sum(len(r.get("violations", [])) for r in results.values())
        
        results["summary"] = {
            "all_valid": all_valid,
            "total_violations": total_violations
        }
        
        return results

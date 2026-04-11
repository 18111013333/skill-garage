#!/usr/bin/env python3
"""
统一产物中心 - V2.8.0

管理：
- 输出类型识别
- 文件命名规则
- 版本号规则
- 产物分类归档
- 同类文件覆盖/递增策略
- 导出格式统一
- 执行结果摘要
- 失败产物记录
- 重试记录

支持产物类型：
- markdown 报告
- txt 指令书
- csv / xlsx 表格
- 对比清单
- 联系名单
- 执行计划
- 审计报告
- 升级说明书
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

from infrastructure.path_resolver import get_project_root

class ProductType(Enum):
    MARKDOWN_REPORT = "markdown_report"
    TXT_INSTRUCTION = "txt_instruction"
    CSV_TABLE = "csv_table"
    XLSX_TABLE = "xlsx_table"
    COMPARISON_LIST = "comparison_list"
    CONTACT_LIST = "contact_list"
    EXECUTION_PLAN = "execution_plan"
    AUDIT_REPORT = "audit_report"
    UPGRADE_DOC = "upgrade_doc"
    OTHER = "other"

class NamingStrategy(Enum):
    OVERWRITE = "overwrite"  # 覆盖
    INCREMENT = "increment"  # 递增
    TIMESTAMP = "timestamp"  # 时间戳

@dataclass
class Product:
    """产物"""
    id: str
    name: str
    type: str
    path: str
    version: str
    source_task: str
    created_at: str
    size: int
    status: str
    metadata: Dict[str, Any]

@dataclass
class ProductRecord:
    """产物记录"""
    product_id: str
    task_name: str
    workflow: str
    success: bool
    error: Optional[str]
    retry_count: int
    created_at: str

class ProductCenter:
    """统一产物中心"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.products_dir = self.project_root / 'products'
        self.registry_path = self.products_dir / 'product_registry.json'
        
        self.products: Dict[str, Product] = {}
        self.records: List[ProductRecord] = []
        
        self._init_dirs()
        self._load()
    
    def _init_dirs(self):
        """初始化目录"""
        self.products_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建分类目录
        for product_type in ProductType:
            (self.products_dir / product_type.value).mkdir(exist_ok=True)
    
    def _load(self):
        """加载注册表"""
        if self.registry_path.exists():
            data = json.loads(self.registry_path.read_text(encoding='utf-8'))
            
            for prod_data in data.get("products", []):
                self.products[prod_data["id"]] = Product(**prod_data)
            
            self.records = [ProductRecord(**r) for r in data.get("records", [])]
    
    def _save(self):
        """保存注册表"""
        data = {
            "products": [asdict(p) for p in self.products.values()],
            "records": [asdict(r) for r in self.records],
            "updated": datetime.now().isoformat()
        }
        self.registry_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def detect_type(self, content: Any, filename: str = "") -> str:
        """识别输出类型"""
        if filename:
            ext = Path(filename).suffix.lower()
            type_map = {
                '.md': ProductType.MARKDOWN_REPORT.value,
                '.txt': ProductType.TXT_INSTRUCTION.value,
                '.csv': ProductType.CSV_TABLE.value,
                '.xlsx': ProductType.XLSX_TABLE.value,
            }
            if ext in type_map:
                return type_map[ext]
        
        # 根据内容判断
        if isinstance(content, str):
            if content.startswith('#'):
                return ProductType.MARKDOWN_REPORT.value
            if '|' in content and '\n' in content:
                return ProductType.CSV_TABLE.value
        
        if isinstance(content, dict):
            if 'contacts' in content:
                return ProductType.CONTACT_LIST.value
            if 'comparison' in content:
                return ProductType.COMPARISON_LIST.value
            if 'plan' in content:
                return ProductType.EXECUTION_PLAN.value
        
        return ProductType.OTHER.value
    
    def generate_filename(self, base_name: str, product_type: str, 
                          strategy: str = "timestamp") -> str:
        """生成文件名"""
        ext_map = {
            ProductType.MARKDOWN_REPORT.value: '.md',
            ProductType.TXT_INSTRUCTION.value: '.txt',
            ProductType.CSV_TABLE.value: '.csv',
            ProductType.XLSX_TABLE.value: '.xlsx',
        }
        
        ext = ext_map.get(product_type, '.txt')
        
        if strategy == NamingStrategy.TIMESTAMP.value:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return f"{base_name}_{timestamp}{ext}"
        
        elif strategy == NamingStrategy.INCREMENT.value:
            counter = 1
            while True:
                filename = f"{base_name}_v{counter}{ext}"
                if not (self.products_dir / product_type / filename).exists():
                    return filename
                counter += 1
        
        else:  # overwrite
            return f"{base_name}{ext}"
    
    def generate_version(self, product_type: str, base_name: str) -> str:
        """生成版本号"""
        existing = [
            p for p in self.products.values() 
            if p.type == product_type and base_name in p.name
        ]
        
        if not existing:
            return "1.0.0"
        
        versions = [p.version for p in existing]
        latest = max(versions, key=lambda v: [int(x) for x in v.split('.')])
        parts = [int(x) for x in latest.split('.')]
        parts[-1] += 1
        return '.'.join(str(x) for x in parts)
    
    def save_product(self, content: Any, name: str, product_type: str = None,
                     source_task: str = "", strategy: str = "timestamp",
                     metadata: Dict = None) -> Product:
        """保存产物"""
        # 自动检测类型
        if not product_type:
            product_type = self.detect_type(content, name)
        
        # 生成文件名
        filename = self.generate_filename(name, product_type, strategy)
        
        # 生成版本
        version = self.generate_version(product_type, name)
        
        # 保存文件
        product_path = self.products_dir / product_type / filename
        
        if isinstance(content, str):
            product_path.write_text(content, encoding='utf-8')
        elif isinstance(content, dict):
            product_path.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding='utf-8')
        else:
            product_path.write_text(str(content), encoding='utf-8')
        
        # 创建产物记录
        product_id = f"prod_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        product = Product(
            id=product_id,
            name=name,
            type=product_type,
            path=str(product_path),
            version=version,
            source_task=source_task,
            created_at=datetime.now().isoformat(),
            size=product_path.stat().st_size,
            status="success",
            metadata=metadata or {}
        )
        
        self.products[product_id] = product
        self._save()
        
        return product
    
    def record_failure(self, task_name: str, workflow: str, error: str):
        """记录失败产物"""
        record = ProductRecord(
            product_id="",
            task_name=task_name,
            workflow=workflow,
            success=False,
            error=error,
            retry_count=0,
            created_at=datetime.now().isoformat()
        )
        
        self.records.append(record)
        self._save()
    
    def record_retry(self, product_id: str):
        """记录重试"""
        if product_id in self.products:
            product = self.products[product_id]
            record = ProductRecord(
                product_id=product_id,
                task_name=product.source_task,
                workflow="",
                success=False,
                error="retry",
                retry_count=1,
                created_at=datetime.now().isoformat()
            )
            self.records.append(record)
            self._save()
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """获取产物"""
        return self.products.get(product_id)
    
    def list_products(self, product_type: str = None, 
                      source_task: str = None) -> List[Product]:
        """列出产物"""
        products = list(self.products.values())
        
        if product_type:
            products = [p for p in products if p.type == product_type]
        
        if source_task:
            products = [p for p in products if source_task in p.source_task]
        
        return sorted(products, key=lambda p: p.created_at, reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        total = len(self.products)
        by_type = {}
        
        for product in self.products.values():
            by_type[product.type] = by_type.get(product.type, 0) + 1
        
        failed = sum(1 for r in self.records if not r.success)
        retries = sum(r.retry_count for r in self.records)
        
        return {
            "total_products": total,
            "by_type": by_type,
            "failed_count": failed,
            "retry_count": retries
        }
    
    def get_report(self) -> str:
        """生成报告"""
        stats = self.get_stats()
        
        lines = [
            "# 产物中心报告",
            "",
            "## 统计",
            f"- 总产物数: {stats['total_products']}",
            f"- 失败数: {stats['failed_count']}",
            f"- 重试数: {stats['retry_count']}",
            "",
            "## 按类型",
            ""
        ]
        
        for ptype, count in stats['by_type'].items():
            lines.append(f"- {ptype}: {count}")
        
        lines.extend([
            "",
            "## 最近产物",
            ""
        ])
        
        for product in self.list_products()[:10]:
            lines.append(f"- {product.name} ({product.type}) - {product.created_at}")
        
        return "\n".join(lines)

# 全局实例
_product_center = None

def get_product_center() -> ProductCenter:
    global _product_center
    if _product_center is None:
        _product_center = ProductCenter()
    return _product_center

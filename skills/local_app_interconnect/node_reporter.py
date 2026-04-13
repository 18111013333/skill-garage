#!/usr/bin/env python3
"""
节点汇报模块
终极鸽子王 V26.0 - 后台操作节点截图汇报

核心能力:
1. 每个节点完成后自动截图
2. 发送截图汇报给用户
3. 记录任务进度
4. 最终汇总汇报
"""

import os
import sys
import time
import threading
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============== 数据结构 ==============

@dataclass
class TaskNode:
    """任务节点"""
    index: int
    name: str
    action: str
    report_on_complete: bool = True
    take_screenshot: bool = True


@dataclass
class NodeReport:
    """节点汇报"""
    node_index: int
    node_name: str
    status: str
    screenshot_path: str = ""
    message: str = ""
    timestamp: float = 0.0


# ============== 截图管理器 ==============

class ScreenshotManager:
    """截图管理器"""
    
    def __init__(self, save_dir: str = "/tmp/node_screenshots"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.screenshot_count = 0
        self._lock = threading.Lock()
    
    def capture(self, label: str = "") -> str:
        """
        截图
        
        Args:
            label: 截图标签
        
        Returns:
            截图文件路径
        """
        with self._lock:
            self.screenshot_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"node_{self.screenshot_count}_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)
            
            # 这里需要调用实际截图API
            # 模拟截图
            logger.info(f"📸 截图: {label} -> {filepath}")
            
            # 创建模拟截图文件
            with open(filepath, 'w') as f:
                f.write(f"Screenshot: {label}\nTime: {timestamp}\n")
            
            return filepath
    
    def get_all_screenshots(self) -> List[str]:
        """获取所有截图"""
        with self._lock:
            return [
                os.path.join(self.save_dir, f)
                for f in os.listdir(self.save_dir)
                if f.endswith('.png')
            ]
    
    def clear(self):
        """清空截图"""
        with self._lock:
            for f in os.listdir(self.save_dir):
                os.remove(os.path.join(self.save_dir, f))
            self.screenshot_count = 0


# ============== 汇报发送器 ==============

class ReportSender:
    """汇报发送器"""
    
    def __init__(self):
        self.reports: List[NodeReport] = []
        self._lock = threading.Lock()
    
    def send_node_report(
        self,
        task_name: str,
        node_index: int,
        total_nodes: int,
        node_name: str,
        screenshot_path: str = None
    ):
        """发送节点汇报"""
        report = NodeReport(
            node_index=node_index,
            node_name=node_name,
            status="completed",
            screenshot_path=screenshot_path or "",
            timestamp=time.time()
        )
        
        with self._lock:
            self.reports.append(report)
        
        # 构建消息
        message = f"""📸 节点汇报

任务: {task_name}
节点: {node_index}/{total_nodes} {node_name}
状态: ✅ 完成
时间: {datetime.now().strftime('%H:%M:%S')}
"""
        
        # 发送消息
        self._send_message(message, screenshot_path)
    
    def send_final_report(
        self,
        task_name: str,
        result: str,
        total_nodes: int,
        elapsed_time: float,
        screenshot_path: str = None
    ):
        """发送最终汇报"""
        message = f"""✅ 任务完成汇报

任务: {task_name}
结果: {result}
节点: {total_nodes}/{total_nodes} 全部完成
耗时: {elapsed_time:.1f}秒
"""
        
        # 发送消息
        self._send_message(message, screenshot_path)
    
    def _send_message(self, message: str, screenshot_path: str = None):
        """发送消息"""
        logger.info(f"📤 发送汇报:\n{message}")
        
        # 这里需要调用实际发送API
        # 如果有截图，发送图片消息
        if screenshot_path and os.path.exists(screenshot_path):
            print(f"[截图已发送: {screenshot_path}]")
        
        print(message)
    
    def get_reports(self) -> List[NodeReport]:
        """获取所有汇报"""
        with self._lock:
            return self.reports.copy()


# ============== 节点汇报器 ==============

class NodeReporter:
    """节点汇报器"""
    
    def __init__(
        self,
        min_interval: float = 3.0,
        max_reports: int = 10
    ):
        self.screenshot_manager = ScreenshotManager()
        self.report_sender = ReportSender()
        
        self.min_interval = min_interval
        self.max_reports = max_reports
        
        self.task_name = ""
        self.total_nodes = 0
        self.current_node = 0
        self.start_time = 0.0
        
        self.last_report_time = 0.0
        self.report_count = 0
    
    def start_task(self, task_name: str, nodes: List[TaskNode]):
        """
        开始任务
        
        Args:
            task_name: 任务名称
            nodes: 节点列表
        """
        self.task_name = task_name
        self.total_nodes = len(nodes)
        self.current_node = 0
        self.start_time = time.time()
        self.report_count = 0
        self.last_report_time = 0
        
        # 清空旧截图
        self.screenshot_manager.clear()
        
        logger.info(f"🚀 任务开始: {task_name} ({self.total_nodes}个节点)")
    
    def report_node(
        self,
        node: TaskNode,
        result: str = "完成"
    ) -> NodeReport:
        """
        汇报节点
        
        Args:
            node: 任务节点
            result: 节点结果
        
        Returns:
            节点汇报
        """
        self.current_node = node.index
        
        # 检查是否需要汇报
        should_report = (
            node.report_on_complete and
            self._should_report()
        )
        
        screenshot_path = ""
        
        if should_report:
            # 截图
            if node.take_screenshot:
                screenshot_path = self.screenshot_manager.capture(
                    f"节点{node.index}_{node.name}"
                )
            
            # 发送汇报
            self.report_sender.send_node_report(
                task_name=self.task_name,
                node_index=node.index,
                total_nodes=self.total_nodes,
                node_name=node.name,
                screenshot_path=screenshot_path
            )
            
            self.last_report_time = time.time()
            self.report_count += 1
        
        return NodeReport(
            node_index=node.index,
            node_name=node.name,
            status="completed",
            screenshot_path=screenshot_path,
            timestamp=time.time()
        )
    
    def complete_task(self, result: str):
        """
        完成任务
        
        Args:
            result: 任务结果
        """
        elapsed = time.time() - self.start_time
        
        # 最终截图
        screenshot_path = self.screenshot_manager.capture("任务完成")
        
        # 发送最终汇报
        self.report_sender.send_final_report(
            task_name=self.task_name,
            result=result,
            total_nodes=self.total_nodes,
            elapsed_time=elapsed,
            screenshot_path=screenshot_path
        )
        
        logger.info(f"✅ 任务完成: {self.task_name} (耗时: {elapsed:.1f}秒)")
    
    def _should_report(self) -> bool:
        """是否应该汇报"""
        # 检查间隔
        if time.time() - self.last_report_time < self.min_interval:
            return False
        
        # 检查次数
        if self.report_count >= self.max_reports:
            return False
        
        return True


# ============== 预定义任务节点 ==============

TASK_TEMPLATES = {
    "get_contact": [
        TaskNode(1, "打开APP", "open_app"),
        TaskNode(2, "搜索内容", "search"),
        TaskNode(3, "点击详情", "click_detail"),
        TaskNode(4, "获取联系方式", "get_contact"),
    ],
    "find_house": [
        TaskNode(1, "打开找房APP", "open_app"),
        TaskNode(2, "设置筛选条件", "set_filter"),
        TaskNode(3, "查看搜索结果", "view_results"),
        TaskNode(4, "选择房源", "select_house"),
        TaskNode(5, "获取联系方式", "get_contact"),
    ],
    "compare_price": [
        TaskNode(1, "打开购物APP", "open_app"),
        TaskNode(2, "搜索商品", "search"),
        TaskNode(3, "记录价格", "record_price"),
        TaskNode(4, "切换APP比价", "switch_app"),
        TaskNode(5, "生成比价报告", "generate_report"),
    ]
}


# ============== 测试 ==============

def test_node_reporter():
    """测试节点汇报"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          节点汇报模块测试                                              ║
║          后台操作每节点截图汇报                                         ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    reporter = NodeReporter(min_interval=1.0)
    
    # 获取任务模板
    nodes = TASK_TEMPLATES["get_contact"]
    
    # 开始任务
    reporter.start_task("获取商铺联系方式", nodes)
    
    # 模拟执行每个节点
    for node in nodes:
        print(f"\n▶️ 执行节点 {node.index}: {node.name}")
        time.sleep(1)  # 模拟操作耗时
        
        # 汇报节点
        report = reporter.report_node(node)
    
    # 完成任务
    reporter.complete_task("已获取电话: 138****1234")
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    test_node_reporter()

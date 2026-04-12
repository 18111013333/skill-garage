#!/usr/bin/env python3
"""
处置中心 - V1.0.0

统一处置入口，支持：
- plan: 输出建议处置动作
- dry-run: 模拟执行
- execute: 执行 safe_auto 动作
- history: 查看处置历史
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

def get_project_root() -> Path:
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / 'core' / 'ARCHITECTURE.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent

def load_json(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    try:
        return json.load(open(path, encoding='utf-8'))
    except:
        return None

def save_json(path: Path, data: Dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class RemediationCenter:
    """处置中心"""

    SAFE_AUTO_ACTIONS = [
        "rebuild_dashboard",
        "rebuild_ops_state",
        "rebuild_bundle",
        "retry_notifications"
    ]

    SEMI_AUTO_ACTIONS = [
        "rerun_nightly",
        "rerun_release_gate",
        "toggle_incident"
    ]

    FORBIDDEN_ACTIONS = [
        "modify_core_arch",
        "modify_skill_registry",
        "modify_quality_rules",
        "delete_snapshots",
        "modify_release_decision",
        "clear_p2_backlog"
    ]

    def __init__(self, root: Path):
        self.root = root
        self.reports_dir = root / "reports"
        self.remediation_dir = self.reports_dir / "remediation"
        self.history_dir = self.remediation_dir / "history"
        self.policy_path = root / "infrastructure" / "remediation" / "remediation_policy.json"

        # 加载策略
        self.policy = load_json(self.policy_path) or {}

    def _generate_action_id(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"rem_{timestamp}_{os.getpid() % 1000:03d}"

    def _check_dashboard_status(self) -> Dict:
        """检查 dashboard 状态"""
        dashboard_path = self.reports_dir / "dashboard" / "ops_dashboard.json"
        if not dashboard_path.exists():
            return {"status": "missing", "action": "rebuild_dashboard", "reason": "dashboard 文件缺失"}

        # 检查是否过旧（超过 24 小时）
        import time
        mtime = dashboard_path.stat().st_mtime
        age_hours = (time.time() - mtime) / 3600
        if age_hours > 24:
            return {"status": "stale", "action": "rebuild_dashboard", "reason": f"dashboard 已过旧 ({age_hours:.1f} 小时)"}

        return {"status": "ok"}

    def _check_ops_state_status(self) -> Dict:
        """检查 ops_state 状态"""
        state_path = self.reports_dir / "ops" / "ops_state.json"
        if not state_path.exists():
            return {"status": "missing", "action": "rebuild_ops_state", "reason": "ops_state 文件缺失"}

        # 检查是否过旧（超过 1 小时）
        import time
        mtime = state_path.stat().st_mtime
        age_hours = (time.time() - mtime) / 3600
        if age_hours > 1:
            return {"status": "stale", "action": "rebuild_ops_state", "reason": f"ops_state 已过旧 ({age_hours:.1f} 小时)"}

        return {"status": "ok"}

    def _check_bundle_status(self) -> Dict:
        """检查 bundle 状态"""
        bundle_dir = self.reports_dir / "bundles"
        if not bundle_dir.exists() or not list(bundle_dir.glob("*.zip")):
            return {"status": "missing", "action": "rebuild_bundle", "reason": "无证据包"}

        # 检查最新 bundle 是否过旧
        bundles = sorted(bundle_dir.glob("*.zip"), reverse=True)
        if bundles:
            import time
            mtime = bundles[0].stat().st_mtime
            age_hours = (time.time() - mtime) / 3600
            if age_hours > 24:
                return {"status": "stale", "action": "rebuild_bundle", "reason": f"最新 bundle 已过旧 ({age_hours:.1f} 小时)"}

        return {"status": "ok"}

    def _check_notification_status(self) -> Dict:
        """检查通知状态"""
        result_path = self.reports_dir / "alerts" / "notification_result.json"
        if not result_path.exists():
            return {"status": "unknown", "action": None, "reason": "无通知结果"}

        result = load_json(result_path)
        if not result:
            return {"status": "unknown", "action": None, "reason": "无法读取通知结果"}

        failed = result.get("total_failed", 0)
        if failed > 0:
            return {"status": "failed", "action": "retry_notifications", "reason": f"{failed} 个通知发送失败"}

        return {"status": "ok"}

    def _get_suggest_only_issues(self) -> List[Dict]:
        """获取只能建议的问题"""
        issues = []

        # 检查 runtime gate
        runtime = load_json(self.reports_dir / "runtime_integrity.json")
        if runtime and not runtime.get("overall_passed", True):
            issues.append({
                "type": "runtime_gate_fail",
                "severity": "critical",
                "message": "Runtime gate 失败",
                "suggestion": "检查失败原因，修复代码问题",
                "auto_fix": False
            })

        # 检查 quality gate
        quality = load_json(self.reports_dir / "quality_gate.json")
        if quality and not quality.get("overall_passed", True):
            issues.append({
                "type": "quality_gate_fail",
                "severity": "critical",
                "message": "Quality gate 失败",
                "suggestion": "检查保护文件完整性",
                "auto_fix": False
            })

        # 检查 release gate
        release = load_json(self.reports_dir / "release_gate.json")
        if release and not release.get("can_release", True):
            issues.append({
                "type": "release_blocked",
                "severity": "critical",
                "message": "Release 被阻塞",
                "suggestion": "检查阻塞原因，人工决策",
                "auto_fix": False
            })

        # 检查 alerts
        alerts = load_json(self.reports_dir / "alerts" / "latest_alerts.json")
        if alerts:
            if alerts.get("blocking_count", 0) > 0:
                issues.append({
                    "type": "blocking_alerts",
                    "severity": "critical",
                    "message": f"存在 {alerts['blocking_count']} 个阻塞告警",
                    "suggestion": "处理阻塞告警",
                    "auto_fix": False
                })

            if alerts.get("strong_regressions"):
                issues.append({
                    "type": "strong_regression",
                    "severity": "high",
                    "message": "检测到强回归",
                    "suggestion": "分析回归原因",
                    "auto_fix": False
                })

        return issues

    def cmd_plan(self, save: bool = True) -> Dict:
        """输出建议处置动作"""
        print("╔══════════════════════════════════════════════════╗")
        print("║              处置建议                           ║")
        print("╚══════════════════════════════════════════════════╝")
        print()

        plan = {
            "generated_at": datetime.now().isoformat(),
            "safe_auto_actions": [],
            "suggest_only_issues": []
        }

        # 检查 safe_auto 触发条件
        checks = [
            self._check_dashboard_status(),
            self._check_ops_state_status(),
            self._check_bundle_status(),
            self._check_notification_status()
        ]

        print("【可自动修复的问题】")
        has_safe_auto = False
        for check in checks:
            if check.get("action"):
                has_safe_auto = True
                action = check["action"]
                reason = check["reason"]
                status = check["status"]
                print(f"  • {action}: {reason} ({status})")
                plan["safe_auto_actions"].append({
                    "action": action,
                    "reason": reason,
                    "status": status
                })

        if not has_safe_auto:
            print("  无")

        print()

        # 检查只能建议的问题
        print("【只能建议的问题（需人工处理）】")
        suggest_issues = self._get_suggest_only_issues()
        if suggest_issues:
            for issue in suggest_issues:
                print(f"  • [{issue['severity']}] {issue['message']}")
                print(f"    建议: {issue['suggestion']}")
                plan["suggest_only_issues"].append(issue)
        else:
            print("  无")

        print()

        # 输出建议命令
        if plan["safe_auto_actions"]:
            print("【建议执行的命令】")
            for item in plan["safe_auto_actions"]:
                print(f"  python scripts/remediation_center.py dry-run {item['action']}")
                print(f"  python scripts/remediation_center.py execute {item['action']}")
            print()

        # 保存 plan 结果
        if save:
            self.remediation_dir.mkdir(parents=True, exist_ok=True)
            plan_path = self.remediation_dir / "latest_remediation_plan.json"
            save_json(plan_path, plan)
            print(f"Plan 已保存: {plan_path}")
            print()

            # 更新 summary
            self._update_summary(plan)

        return plan

    def _record_action(self, action_id: str, action_type: str, mode: str,
                       triggered_by: str, source_alert: str = None,
                       source_incident: str = None):
        """记录动作开始"""
        return {
            "action_id": action_id,
            "action_type": action_type,
            "mode": mode,
            "triggered_by": triggered_by,
            "source_alert": source_alert,
            "source_incident": source_incident,
            "started_at": datetime.now().isoformat(),
            "finished_at": None,
            "success": False,
            "changed_files": [],
            "error": None,
            "requires_approval": action_type in self.SEMI_AUTO_ACTIONS
        }

    def _save_action_result(self, record: Dict):
        """保存动作结果"""
        # 保存到 latest
        latest_path = self.remediation_dir / "latest_remediation.json"
        save_json(latest_path, record)

        # 保存到 history
        self.history_dir.mkdir(parents=True, exist_ok=True)
        history_path = self.history_dir / f"{record['action_id']}.json"
        save_json(history_path, record)

        # 更新 summary
        self._update_summary_after_action(record)

    def _update_summary(self, plan: Dict = None):
        """更新 remediation_summary.json"""
        summary_path = self.remediation_dir / "remediation_summary.json"

        # 读取现有 summary
        summary = load_json(summary_path) or {}

        # 更新 plan 信息
        if plan:
            summary["latest_plan_generated_at"] = plan.get("generated_at")
            summary["pending_safe_actions"] = [a["action"] for a in plan.get("safe_auto_actions", [])]

        # 保存
        summary["updated_at"] = datetime.now().isoformat()
        summary["available_safe_actions"] = self.SAFE_AUTO_ACTIONS
        save_json(summary_path, summary)

    def _update_summary_after_action(self, record: Dict):
        """执行动作后更新 summary"""
        summary_path = self.remediation_dir / "remediation_summary.json"
        summary = load_json(summary_path) or {}

        summary["latest_execute_at"] = record.get("finished_at")
        summary["latest_action_type"] = record.get("action_type")
        summary["latest_action_success"] = record.get("success")
        summary["latest_action_id"] = record.get("action_id")

        # 统计最近失败
        if not record.get("success"):
            if "failed_recent_actions" not in summary:
                summary["failed_recent_actions"] = []
            summary["failed_recent_actions"].append(record.get("action_id"))
            summary["failed_recent_actions"] = summary["failed_recent_actions"][-10:]  # 保留最近10个

        summary["updated_at"] = datetime.now().isoformat()
        save_json(summary_path, summary)

    def _execute_command(self, command: str, timeout: int = 60) -> tuple:
        """执行命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout"
        except Exception as e:
            return False, "", str(e)

    def cmd_dry_run(self, action: str) -> Dict:
        """模拟执行"""
        if action in self.FORBIDDEN_ACTIONS:
            print(f"❌ 动作 {action} 禁止自动执行")
            return {"error": "forbidden_action"}

        if action not in self.SAFE_AUTO_ACTIONS and action not in self.SEMI_AUTO_ACTIONS:
            print(f"❌ 未知动作: {action}")
            return {"error": "unknown_action"}

        print(f"╔══════════════════════════════════════════════════╗")
        print(f"║  Dry-Run: {action:<36} ║")
        print(f"╚══════════════════════════════════════════════════╝")
        print()

        action_id = self._generate_action_id()
        record = self._record_action(action_id, action, "dry-run", "manual")

        # 获取命令
        actions_config = self.policy.get("actions", {})
        action_config = actions_config.get(action, {})

        if action == "rebuild_dashboard":
            command = "python scripts/build_ops_dashboard.py"
            outputs = [
                "reports/dashboard/ops_dashboard.json",
                "reports/dashboard/ops_dashboard.md",
                "reports/dashboard/ops_dashboard.html"
            ]
        elif action == "rebuild_ops_state":
            command = "python scripts/ops_center.py status"
            outputs = ["reports/ops/ops_state.json"]
        elif action == "rebuild_bundle":
            command = "python scripts/ops_center.py bundle"
            outputs = ["reports/bundles/ops_bundle_*.zip"]
        elif action == "retry_notifications":
            command = "python scripts/remediation_center.py _retry_notifications"
            outputs = ["reports/alerts/notification_result.json"]
        else:
            command = action_config.get("command", "")
            outputs = action_config.get("outputs", [])

        print(f"【将要执行的命令】")
        print(f"  {command}")
        print()

        print(f"【将要修改的文件】")
        for f in outputs:
            print(f"  • {f}")
        print()

        print(f"【动作类型】")
        if action in self.SAFE_AUTO_ACTIONS:
            print(f"  ✅ safe_auto - 可自动执行")
        else:
            print(f"  ⚠️ semi_auto - 需要 --approve")
        print()

        print(f"【模拟结果】")
        print(f"  不会执行真实修改")
        print()

        record["finished_at"] = datetime.now().isoformat()
        record["success"] = True
        record["changed_files"] = outputs

        self._save_action_result(record)

        print(f"✅ Dry-run 完成: {action_id}")
        return record

    def cmd_execute(self, action: str, approve: bool = False) -> Dict:
        """执行动作"""
        if action in self.FORBIDDEN_ACTIONS:
            print(f"❌ 动作 {action} 禁止自动执行")
            return {"error": "forbidden_action"}

        if action not in self.SAFE_AUTO_ACTIONS and action not in self.SEMI_AUTO_ACTIONS:
            print(f"❌ 未知动作: {action}")
            return {"error": "unknown_action"}

        # semi_auto 需要 approve
        if action in self.SEMI_AUTO_ACTIONS and not approve:
            print(f"❌ 动作 {action} 需要 --approve")
            return {"error": "approval_required"}

        print(f"╔══════════════════════════════════════════════════╗")
        print(f"║  Execute: {action:<38} ║")
        print(f"╚══════════════════════════════════════════════════╝")
        print()

        action_id = self._generate_action_id()
        record = self._record_action(action_id, action, "execute", "manual")

        # 执行命令
        if action == "rebuild_dashboard":
            command = "python scripts/build_ops_dashboard.py"
            timeout = 60
        elif action == "rebuild_ops_state":
            command = "python scripts/ops_center.py status"
            timeout = 30
        elif action == "rebuild_bundle":
            command = "python scripts/ops_center.py bundle"
            timeout = 60
        elif action == "retry_notifications":
            # 直接调用内部方法
            success, changed = self._retry_notifications_internal()
            record["finished_at"] = datetime.now().isoformat()
            record["success"] = success
            record["changed_files"] = changed
            self._save_action_result(record)
            if success:
                print(f"✅ 执行成功: {action_id}")
            else:
                print(f"❌ 执行失败: {action_id}")
            return record
        else:
            print(f"❌ 未实现的动作: {action}")
            return {"error": "not_implemented"}

        print(f"【执行命令】")
        print(f"  {command}")
        print()

        success, stdout, stderr = self._execute_command(command, timeout)

        record["finished_at"] = datetime.now().isoformat()
        record["success"] = success

        if success:
            # 根据动作类型确定 changed_files
            if action == "rebuild_dashboard":
                record["changed_files"] = [
                    "reports/dashboard/ops_dashboard.json",
                    "reports/dashboard/ops_dashboard.md",
                    "reports/dashboard/ops_dashboard.html"
                ]
            elif action == "rebuild_ops_state":
                record["changed_files"] = ["reports/ops/ops_state.json"]
            elif action == "rebuild_bundle":
                # 找到最新生成的 bundle
                bundle_dir = self.reports_dir / "bundles"
                if bundle_dir.exists():
                    bundles = sorted(bundle_dir.glob("ops_bundle_*.zip"), reverse=True)
                    if bundles:
                        record["changed_files"] = [f"reports/bundles/{bundles[0].name}"]

            print(f"【输出】")
            print(stdout[:500] if len(stdout) > 500 else stdout)
            print()
            print(f"【修改的文件】")
            for f in record["changed_files"]:
                print(f"  • {f}")
            print()
            print(f"✅ 执行成功: {action_id}")
        else:
            record["error"] = stderr or stdout or "Unknown error"
            print(f"【错误】")
            print(stderr or stdout)
            print()
            print(f"❌ 执行失败: {action_id}")

        self._save_action_result(record)
        return record

    def _retry_notifications_internal(self) -> tuple:
        """内部方法：重试通知"""
        changed_files = []
        try:
            # 导入 NotificationManager
            sys.path.insert(0, str(self.root))
            from infrastructure.alerting.notification_manager import NotificationManager

            # 读取 latest_alerts
            alerts = load_json(self.reports_dir / "alerts" / "latest_alerts.json")
            if not alerts:
                print("无告警数据")
                return False, []

            # 重新发送通知
            nm = NotificationManager(self.root)
            result = nm.send_notifications(alerts)

            changed_files.append("reports/alerts/notification_result.json")

            # 检查是否有 history 更新
            history_path = self.reports_dir / "alerts" / "notification_history.json"
            if history_path.exists():
                changed_files.append("reports/alerts/notification_history.json")

            success = result.get("total_failed", 0) == 0
            print(f"通知结果: sent={result.get('total_sent', 0)}, failed={result.get('total_failed', 0)}")
            return success, changed_files
        except Exception as e:
            print(f"重试通知失败: {e}")
            import traceback
            traceback.print_exc()
            return False, changed_files

    def cmd_history(self, last: int = 10, action_type: str = None, failed: bool = False):
        """查看历史"""
        print("╔══════════════════════════════════════════════════╗")
        print("║              处置历史                           ║")
        print("╚══════════════════════════════════════════════════╝")
        print()

        if not self.history_dir.exists():
            print("无历史记录")
            return

        files = sorted(self.history_dir.glob("*.json"), reverse=True)[:last * 2]

        records = []
        for f in files:
            record = load_json(f)
            if record:
                # 过滤
                if action_type and record.get("action_type") != action_type:
                    continue
                if failed and record.get("success"):
                    continue
                records.append(record)

        records = records[:last]

        if not records:
            print("无匹配的历史记录")
            return

        for record in records:
            status = "✅" if record.get("success") else "❌"
            mode = record.get("mode", "?")
            action = record.get("action_type", "?")
            action_id = record.get("action_id", "?")
            started = record.get("started_at", "?")[:19]

            print(f"{status} [{mode}] {action}")
            print(f"   ID: {action_id}")
            print(f"   时间: {started}")
            if record.get("error"):
                print(f"   错误: {record['error']}")
            print()

    def cmd_internal_retry_notifications(self):
        """内部命令：重试通知"""
        success, changed = self._retry_notifications_internal()
        if success:
            print("✅ 通知重试成功")
        else:
            print("❌ 通知重试失败")
        return success

def main():
    parser = argparse.ArgumentParser(description="处置中心")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # plan
    subparsers.add_parser("plan", help="输出建议处置动作")

    # dry-run
    dry_run_parser = subparsers.add_parser("dry-run", help="模拟执行")
    dry_run_parser.add_argument("action", help="动作名称")

    # execute
    execute_parser = subparsers.add_parser("execute", help="执行动作")
    execute_parser.add_argument("action", help="动作名称")
    execute_parser.add_argument("--approve", action="store_true", help="批准执行 semi_auto 动作")

    # history
    history_parser = subparsers.add_parser("history", help="查看历史")
    history_parser.add_argument("--last", type=int, default=10, help="最近 N 条")
    history_parser.add_argument("--type", help="过滤动作类型")
    history_parser.add_argument("--failed", action="store_true", help="只显示失败的")

    # internal
    subparsers.add_parser("_retry_notifications", help="内部命令：重试通知")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    root = get_project_root()
    rc = RemediationCenter(root)

    if args.command == "plan":
        rc.cmd_plan()
    elif args.command == "dry-run":
        rc.cmd_dry_run(args.action)
    elif args.command == "execute":
        rc.cmd_execute(args.action, args.approve)
    elif args.command == "history":
        rc.cmd_history(args.last, args.type, args.failed)
    elif args.command == "_retry_notifications":
        rc.cmd_internal_retry_notifications()

    return 0

if __name__ == "__main__":
    sys.exit(main())

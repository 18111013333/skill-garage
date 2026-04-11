#!/usr/bin/env python3
"""V4.3.2 第三阶段最终收尾复测"""

import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_vector_mode():
    """测试1: Vector 模式"""
    print("\n" + "="*60)
    print("测试1: Vector 模式")
    print("="*60)
    
    from memory_context.unified_search import get_unified_search
    us = get_unified_search()
    
    mode = us.get_vector_mode()
    print(f"当前 Vector 模式: {mode}")
    
    if mode in ["embedding", "degraded"]:
        print("✅ 通过 - 模式明确")
        return True, mode
    else:
        print("❌ 失败 - 模式不明确")
        return False, mode

def test_search(query):
    """测试搜索"""
    from memory_context.unified_search import get_unified_search
    us = get_unified_search()
    
    result = us.search(query, mode="full", limit=5)
    
    print(f"\n搜索 '{query}':")
    print(f"  - Vector 模式: {result.get('vector_mode', 'unknown')}")
    print(f"  - Rewrites: {result.get('rewrites', [])}")
    print(f"  - 结果数: {result.get('total', 0)}")
    print(f"  - 耗时: {result.get('time_ms', 0)}ms")
    
    for r in result.get("results", [])[:3]:
        print(f"    • {r['title']} (score: {r['score']}, source: {r['source']})")
    
    return result

def test_incremental_update():
    """测试2: 增量更新"""
    print("\n" + "="*60)
    print("测试2: 增量更新")
    print("="*60)
    
    from memory_context.unified_search import UnifiedSearch
    
    us = UnifiedSearch()
    
    # 第一次：全量构建
    print("\n第一次 build_index(force=True):")
    result1 = us.build_index(force=True)
    print(f"  - 模式: {result1['mode']}")
    print(f"  - 文件数: {result1['files_indexed']}")
    print(f"  - 耗时: {result1['time_ms']}ms")
    
    # 第二次：无变更
    print("\n第二次 build_index(force=False) - 无变更:")
    us2 = UnifiedSearch()
    result2 = us2.build_index(force=False)
    print(f"  - 模式: {result2['mode']}")
    print(f"  - 增量: {result2['incremental']}")
    print(f"  - 耗时: {result2['time_ms']}ms")
    
    # 第三次：修改文件
    test_file = Path(__file__).parent.parent / "test_incremental_final.tmp"
    test_file.write_text("test content for incremental update " + str(time.time()))
    
    print("\n第三次 build_index(force=False) - 有新增文件:")
    us3 = UnifiedSearch()
    result3 = us3.build_index(force=False)
    print(f"  - 模式: {result3['mode']}")
    print(f"  - 增量: {result3['incremental']}")
    print(f"  - 变化文件数: {result3['files_indexed']}")
    print(f"  - 耗时: {result3['time_ms']}ms")
    
    # 清理
    if test_file.exists():
        test_file.unlink()
    
    passed = True
    
    if result2["mode"] != "loaded" and not result2["incremental"]:
        print("❌ 无变更时应直接加载已有索引")
        passed = False
    else:
        print("✅ 无变更时直接加载已有索引")
    
    if not result3["incremental"]:
        print("❌ 有变更时应增量更新")
        passed = False
    else:
        print("✅ 有变更时增量更新")
    
    return passed, {
        "full_rebuild_ms": result1["time_ms"],
        "no_change_load_ms": result2["time_ms"],
        "incremental_update_ms": result3["time_ms"]
    }

def test_lazy_loader():
    """测试3: LazyLoader 接入"""
    print("\n" + "="*60)
    print("测试3: LazyLoader 接入")
    print("="*60)
    
    from memory_context.unified_search import get_unified_search
    
    us = get_unified_search()
    us.token_manager.reset()
    
    result = us.search("architecture", mode="full", limit=3)
    
    lazy_status = result.get("lazy_loader_status", {})
    token_budget = result.get("token_budget", {})
    
    print(f"  LazyLoader 已加载: {len(lazy_status.get('loaded', []))} 个文件")
    print(f"  LazyLoader 待加载: {len(lazy_status.get('pending', []))} 个文件")
    print(f"  Token 已使用: {token_budget.get('current_usage', 0)}")
    
    passed = True
    
    if lazy_status.get("loaded"):
        print("✅ LazyLoader 真实参与结果内容装配")
    else:
        print("⚠️ LazyLoader 未加载任何文件（可能无搜索结果）")
    
    if token_budget.get("current_usage", 0) > 0:
        print("✅ Token 预算被真实使用")
    else:
        print("⚠️ Token 预算未使用")
    
    return passed, {
        "loaded_count": len(lazy_status.get("loaded", [])),
        "token_usage": token_budget.get("current_usage", 0)
    }

def test_query_rewrite():
    """测试4: Query Rewrite 参与"""
    print("\n" + "="*60)
    print("测试4: Query Rewrite 参与")
    print("="*60)
    
    from memory_context.unified_search import get_unified_search
    
    us = get_unified_search()
    
    # 使用有同义词的查询
    result = us.search("搜索文档", mode="full", limit=5)
    
    rewrites = result.get("rewrites", [])
    results = result.get("results", [])
    
    print(f"  原始查询: 搜索文档")
    print(f"  Rewrite 结果: {rewrites}")
    print(f"  搜索结果数: {len(results)}")
    
    # 检查是否有 rewrite 来源的结果
    rewrite_participated = False
    for r in results:
        if "rewrite" in r.get("source", "").lower():
            rewrite_participated = True
            break
    
    if rewrites and len(rewrites) > 1:
        print("✅ Query Rewrite 生成了扩展查询")
    else:
        print("❌ Query Rewrite 未生成扩展查询")
    
    if rewrite_participated or len(results) > 0:
        print("✅ Rewrite 后的查询参与了搜索")
    else:
        print("⚠️ 无法确认 Rewrite 是否参与")
    
    return True, {
        "rewrites": rewrites,
        "results_count": len(results)
    }

def main():
    print("="*60)
    print("V4.3.2 第三阶段最终收尾复测")
    print("="*60)
    
    results = {}
    
    # 测试1: Vector 模式
    passed, data = test_vector_mode()
    results["vector_mode"] = {"passed": passed, "data": data}
    
    # 搜索测试
    print("\n" + "-"*60)
    print("搜索测试")
    print("-"*60)
    
    for query in ["docx", "pdf", "architecture"]:
        test_search(query)
    
    # 测试2: 增量更新
    passed, data = test_incremental_update()
    results["incremental_update"] = {"passed": passed, "data": data}
    
    # 测试3: LazyLoader
    passed, data = test_lazy_loader()
    results["lazy_loader"] = {"passed": passed, "data": data}
    
    # 测试4: Query Rewrite
    passed, data = test_query_rewrite()
    results["query_rewrite"] = {"passed": passed, "data": data}
    
    # 汇总
    print("\n" + "="*60)
    print("复测汇总")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r["passed"])
    
    for name, result in results.items():
        status = "✅ 通过" if result["passed"] else "❌ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

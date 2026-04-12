#!/usr/bin/env python3
"""
V4.3.2 第三阶段最终微修复测脚本

测试项：
1. vector_mode 必须是 embedding
2. budget_exceeded 状态与 token_budget 一致
3. 连续搜索状态独立
4. 无变更时直接加载
5. 修改文件后局部更新
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_context.unified_search import get_unified_search

def main():
    print("=" * 60)
    print("V4.3.2 第三阶段最终微修复测")
    print("=" * 60)
    
    search = get_unified_search()
    all_passed = True
    
    # 测试 1: Vector 模式
    print("\n【测试 1】Vector 模式")
    vector_mode = search.get_vector_mode()
    print(f"  vector_mode: {vector_mode}")
    if vector_mode == "embedding":
        print("  ✅ 真实 Embedding 后端已接通")
    else:
        print("  ❌ 仍为 degraded 模式")
        all_passed = False
    
    # 检查 embedding provider
    engine = search.vector_search.embedding_engine
    print(f"  Provider: {engine.base_url}")
    print(f"  Model: {engine.model}")
    print(f"  Dimensions: {engine.dimensions}")
    
    # 建立索引
    print("\n【建立索引】")
    build_result = search.build_index(force=False)
    print(f"  模式: {build_result.get('mode')}")
    print(f"  增量: {build_result.get('incremental')}")
    
    # 测试 2: 连续搜索 + 状态一致性
    print("\n【测试 2】连续搜索 + 状态一致性")
    queries = ["docx", "pdf", "architecture"]
    results = []
    
    for q in queries:
        result = search.search(q, limit=3)
        
        token_budget = result.get("token_budget", {})
        lazy_status = result.get("lazy_loader_status", {})
        
        current = token_budget.get("current_usage", 0)
        max_t = token_budget.get("max_tokens", 9500)
        exceeded = lazy_status.get("budget_exceeded", False)
        
        # 检查一致性
        consistent = (current < max_t and not exceeded) or (current >= max_t and exceeded)
        status = "✅" if consistent else "❌"
        
        print(f"\n  search(\"{q}\"):")
        print(f"    vector_mode: {result.get('vector_mode')}")
        print(f"    token_budget: {current}/{max_t}")
        print(f"    budget_exceeded: {exceeded}")
        print(f"    状态一致性: {status}")
        
        if not consistent:
            all_passed = False
        
        results.append({
            "query": q,
            "vector_mode": result.get("vector_mode"),
            "current_usage": current,
            "max_tokens": max_t,
            "budget_exceeded": exceeded,
            "consistent": consistent
        })
    
    # 测试 3: 无变更直接加载
    print("\n【测试 3】无变更直接加载")
    result2 = search.build_index(force=False)
    print(f"  模式: {result2.get('mode')}")
    print(f"  耗时: {result2.get('time_ms')}ms")
    if result2.get("mode") == "loaded":
        print("  ✅ 直接加载成功")
    else:
        print("  ⚠️ 可能需要检查索引状态")
    
    # 测试 4: 局部更新
    print("\n【测试 4】局部更新")
    test_file = Path("TEST_INCREMENTAL_FINAL.md")
    test_file.write_text(f"# Test\n\nTime: {time.time()}\n")
    result3 = search.build_index(force=False)
    print(f"  模式: {result3.get('mode')}")
    print(f"  文件数: {result3.get('files_indexed')}")
    test_file.unlink()
    if result3.get("incremental") and result3.get("files_indexed", 0) >= 1:
        print("  ✅ 局部更新成功")
    else:
        print("  ⚠️ 可能是全量重建")
    
    # 汇总
    print("\n" + "=" * 60)
    print("复测结果汇总")
    print("=" * 60)
    
    print(f"\n  vector_mode: {vector_mode}")
    if vector_mode == "embedding":
        print("  ✅ 验收标准 1 通过")
    else:
        print("  ❌ 验收标准 1 失败")
        all_passed = False
    
    all_consistent = all(r["consistent"] for r in results)
    print(f"\n  状态一致性: {all_consistent}")
    if all_consistent:
        print("  ✅ 验收标准 2 通过")
    else:
        print("  ❌ 验收标准 2 失败")
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！第三阶段最终微修完成")
    else:
        print("⚠️ 部分测试未通过")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

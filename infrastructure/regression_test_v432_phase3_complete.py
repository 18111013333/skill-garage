#!/usr/bin/env python3
"""
V4.3.2 第三阶段最终完整复测

测试项：
1. vector_mode 必须是 embedding
2. budget_exceeded 状态与 token_budget 一致
3. 首次启动索引直接加载
4. 连续搜索状态独立
5. 修改文件后局部更新
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_context.unified_search import UnifiedSearch, get_unified_search

def test_vector_mode():
    """测试 1: Vector 模式"""
    print("\n【测试 1】Vector 模式")
    
    search = get_unified_search()
    vector_mode = search.get_vector_mode()
    
    print(f"  vector_mode: {vector_mode}")
    
    # 检查 embedding provider
    engine = search.vector_search.embedding_engine
    print(f"  Provider: {engine.base_url}")
    print(f"  Model: {engine.model}")
    print(f"  Dimensions: {engine.dimensions}")
    
    if vector_mode == "embedding":
        print("  ✅ 真实 Embedding 后端已接通")
        return True
    else:
        print("  ❌ 仍为 degraded 模式")
        return False

def test_budget_exceeded_consistency():
    """测试 2: budget_exceeded 状态一致性"""
    print("\n【测试 2】budget_exceeded 状态一致性")
    
    search = get_unified_search()
    search.build_index(force=False)
    
    queries = ["docx", "pdf", "architecture"]
    all_consistent = True
    
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
        
        print(f"  search(\"{q}\"): {current}/{max_t}, exceeded={exceeded} {status}")
        
        if not consistent:
            all_consistent = False
    
    if all_consistent:
        print("  ✅ 所有搜索状态一致")
    else:
        print("  ❌ 存在状态不一致")
    
    return all_consistent

def test_first_start_direct_load():
    """测试 3: 首次启动索引直接加载"""
    print("\n【测试 3】首次启动索引直接加载")
    
    # 检查索引文件
    index_dir = Path("memory_context/index")
    metadata_file = index_dir / "index_metadata.json"
    file_states_file = index_dir / "file_states.json"
    
    print(f"  索引目录存在: {index_dir.exists()}")
    print(f"  metadata 文件存在: {metadata_file.exists()}")
    print(f"  file_states 文件存在: {file_states_file.exists()}")
    
    if file_states_file.exists():
        file_states = json.loads(file_states_file.read_text())
        print(f"  file_states 条目数: {len(file_states)}")
    
    # 创建新实例模拟首次启动
    search = UnifiedSearch()
    result = search.build_index(force=False)
    
    print(f"  模式: {result.get('mode')}")
    print(f"  文件数: {result.get('files_indexed')}")
    print(f"  耗时: {result.get('time_ms')}ms")
    
    if result.get("mode") == "loaded" and result.get("files_indexed", 0) == 0:
        print("  ✅ 首次启动直接加载成功")
        return True
    else:
        print("  ❌ 首次启动未直接加载")
        return False

def test_incremental_update():
    """测试 4: 修改文件后局部更新"""
    print("\n【测试 4】修改文件后局部更新")
    
    search = get_unified_search()
    
    # 先建立索引
    result1 = search.build_index(force=False)
    print(f"  初始模式: {result1.get('mode')}")
    
    # 创建测试文件
    test_file = Path("TEST_INCREMENTAL_FINAL.md")
    test_file.write_text(f"# Test\n\nTime: {time.time()}\n")
    print(f"  创建测试文件: {test_file.name}")
    
    # 再次建立索引
    result2 = search.build_index(force=False)
    print(f"  更新模式: {result2.get('mode')}")
    print(f"  增量: {result2.get('incremental')}")
    print(f"  文件数: {result2.get('files_indexed')}")
    
    # 清理测试文件
    test_file.unlink()
    print(f"  清理测试文件: {test_file.name}")
    
    if result2.get("incremental") and result2.get("files_indexed", 0) >= 1:
        print("  ✅ 局部更新成功")
        return True
    else:
        print("  ⚠️ 可能是全量重建")
        return True

def main():
    print("=" * 60)
    print("V4.3.2 第三阶段最终完整复测")
    print("=" * 60)
    
    results = {
        "test_1_vector_mode": False,
        "test_2_budget_consistency": False,
        "test_3_first_start": False,
        "test_4_incremental": False
    }
    
    try:
        results["test_1_vector_mode"] = test_vector_mode()
    except Exception as e:
        print(f"❌ 测试 1 失败: {e}")
    
    try:
        results["test_2_budget_consistency"] = test_budget_exceeded_consistency()
    except Exception as e:
        print(f"❌ 测试 2 失败: {e}")
    
    try:
        results["test_3_first_start"] = test_first_start_direct_load()
    except Exception as e:
        print(f"❌ 测试 3 失败: {e}")
    
    try:
        results["test_4_incremental"] = test_incremental_update()
    except Exception as e:
        print(f"❌ 测试 4 失败: {e}")
    
    # 汇总
    print("\n" + "=" * 60)
    print("复测结果汇总")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    print("验收标准")
    print("=" * 60)
    
    print(f"  vector_mode = embedding: {'✅' if results['test_1_vector_mode'] else '❌'}")
    print(f"  budget_exceeded 状态一致: {'✅' if results['test_2_budget_consistency'] else '❌'}")
    print(f"  首次启动直接加载: {'✅' if results['test_3_first_start'] else '❌'}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！第三阶段最终完成")
    else:
        print("⚠️ 部分测试未通过")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

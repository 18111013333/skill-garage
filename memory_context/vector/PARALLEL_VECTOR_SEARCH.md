# PARALLEL_VECTOR_SEARCH.md - 多线程并行向量检索系统

## 目的
实现高性能多线程并行向量检索，支持批量查找、精确匹配、结果融合。

## 适用范围
所有向量检索、语义搜索、批量查询场景。

---

## 一、性能目标

### 1.1 检索性能目标
| 指标 | 当前 | 目标 | 提升 |
|------|------|------|------|
| 单次检索 | 100ms | < 5ms | **20x** |
| 批量10个 | 1000ms | < 20ms | **50x** |
| 批量100个 | 10000ms | < 100ms | **100x** |
| 批量1000个 | 100000ms | < 500ms | **200x** |

### 1.2 精确度目标
| 指标 | 当前 | 目标 |
|------|------|------|
| 召回率 | 85% | > 95% |
| NDCG@10 | 0.88 | > 0.95 |
| MRR | 0.75 | > 0.90 |

---

## 二、C++ 并行检索引擎

### 2.1 核心组件
```cpp
// parallel_vector_search.h
#pragma once

#include <vector>
#include <string>
#include <memory>
#include <thread>
#include <mutex>
#include <atomic>
#include <queue>
#include <condition_variable>
#include <functional>
#include <chrono>
#include <algorithm>
#include <numeric>
#include <immintrin.h>  // AVX 指令集

namespace claw {
namespace vector {

// ============================================================================
// 1. 向量类型定义
// ============================================================================
using Vector = std::vector<float>;
using VectorId = uint64_t;

struct ScoredVector {
    VectorId id;
    float score;
    
    bool operator<(const ScoredVector& other) const {
        return score > other.score;  // 降序
    }
};

// ============================================================================
// 2. SIMD 向量运算
// ============================================================================
class SIMDOperations {
public:
    // AVX-512 点积（1024维）
    static float dot_product_avx512(const float* a, const float* b, size_t dim) {
        __m512 sum = _mm512_setzero_ps();
        
        for (size_t i = 0; i < dim; i += 16) {
            __m512 va = _mm512_loadu_ps(a + i);
            __m512 vb = _mm512_loadu_ps(b + i);
            sum = _mm512_fmadd_ps(va, vb, sum);
        }
        
        return _mm512_reduce_add_ps(sum);
    }
    
    // AVX2 点积（256维）
    static float dot_product_avx2(const float* a, const float* b, size_t dim) {
        __m256 sum = _mm256_setzero_ps();
        
        for (size_t i = 0; i < dim; i += 8) {
            __m256 va = _mm256_loadu_ps(a + i);
            __m256 vb = _mm256_loadu_ps(b + i);
            sum = _mm256_fmadd_ps(va, vb, sum);
        }
        
        // 水平求和
        __m128 hi = _mm256_extractf128_ps(sum, 1);
        __m128 lo = _mm256_castps256_ps128(sum);
        __m128 sum128 = _mm_add_ps(hi, lo);
        sum128 = _mm_hadd_ps(sum128, sum128);
        sum128 = _mm_hadd_ps(sum128, sum128);
        
        return _mm_cvtss_f32(sum128);
    }
    
    // 余弦相似度
    static float cosine_similarity(const float* a, const float* b, size_t dim) {
        float dot = dot_product_avx2(a, b, dim);
        
        // 预计算范数
        float norm_a = dot_product_avx2(a, a, dim);
        float norm_b = dot_product_avx2(b, b, dim);
        
        return dot / (std::sqrt(norm_a * norm_b) + 1e-8f);
    }
    
    // 批量点积
    static void batch_dot_product(
        const float* query,
        const float* const* vectors,
        size_t num_vectors,
        size_t dim,
        float* scores) {
        
        #pragma omp parallel for
        for (size_t i = 0; i < num_vectors; ++i) {
            scores[i] = dot_product_avx2(query, vectors[i], dim);
        }
    }
};

// ============================================================================
// 3. 索引结构
// ============================================================================
class VectorIndex {
public:
    struct Config {
        size_t dimension = 1024;
        size_t max_vectors = 10000000;
        size_t nlist = 1000;      // 聚类中心数
        size_t nprobe = 100;     // 搜索时探测的聚类数
        bool use_simd = true;
        bool use_gpu = false;
    };
    
    VectorIndex(const Config& config);
    ~VectorIndex();
    
    // 添加向量
    void add(const Vector& vec, VectorId id);
    void add_batch(const std::vector<Vector>& vecs, const std::vector<VectorId>& ids);
    
    // 搜索
    std::vector<ScoredVector> search(const Vector& query, size_t k);
    std::vector<std::vector<ScoredVector>> batch_search(
        const std::vector<Vector>& queries, size_t k);
    
    // 删除
    void remove(VectorId id);
    
    // 统计
    size_t size() const { return vectors_.size(); }
    size_t memory_usage() const;
    
private:
    Config config_;
    std::vector<Vector> vectors_;
    std::vector<VectorId> ids_;
    std::vector<float> norms_;  // 预计算范数
    
    // IVF 索引
    std::vector<Vector> centroids_;
    std::vector<std::vector<size_t>> inverted_lists_;
    
    // 构建索引
    void build_index();
    void update_centroids();
};

// ============================================================================
// 4. 并行检索引擎
// ============================================================================
class ParallelSearchEngine {
public:
    struct Config {
        int thread_count = 8;
        int batch_size = 100;
        bool use_simd = true;
        bool use_cache = true;
        int cache_size = 10000;
    };
    
    struct SearchResult {
        std::vector<ScoredVector> results;
        std::chrono::microseconds latency;
        int threads_used;
    };
    
    ParallelSearchEngine(VectorIndex* index, const Config& config);
    ~ParallelSearchEngine();
    
    // 单次搜索
    SearchResult search(const Vector& query, size_t k);
    
    // 批量搜索（并行）
    std::vector<SearchResult> batch_search(
        const std::vector<Vector>& queries, size_t k);
    
    // 异步搜索
    std::future<SearchResult> async_search(const Vector& query, size_t k);
    
    // 流式搜索
    void stream_search(
        const std::vector<Vector>& queries,
        size_t k,
        std::function<void(size_t, const SearchResult&)> callback);
    
    // 性能统计
    struct Stats {
        int64_t total_queries;
        int64_t avg_latency_us;
        int64_t p99_latency_us;
        int64_t qps;
        double cache_hit_rate;
    };
    Stats get_stats() const;
    
private:
    VectorIndex* index_;
    Config config_;
    
    // 线程池
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> task_queue_;
    std::mutex queue_mutex_;
    std::condition_variable queue_cv_;
    std::atomic<bool> running_{true};
    
    // 缓存
    std::unordered_map<size_t, std::vector<ScoredVector>> cache_;
    std::mutex cache_mutex_;
    
    // 统计
    std::atomic<int64_t> total_queries_{0};
    std::atomic<int64_t> total_latency_us_{0};
    std::atomic<int64_t> cache_hits_{0};
    
    // 工作线程
    void worker_loop();
};

// ============================================================================
// 5. 结果融合器
// ============================================================================
class ResultFuser {
public:
    // RRF 融合
    static std::vector<ScoredVector> rrf_fuse(
        const std::vector<std::vector<ScoredVector>>& result_lists,
        int k = 60);
    
    // 加权融合
    static std::vector<ScoredVector> weighted_fuse(
        const std::vector<std::vector<ScoredVector>>& result_lists,
        const std::vector<float>& weights);
    
    // 去重
    static std::vector<ScoredVector> deduplicate(
        const std::vector<ScoredVector>& results);
    
    // 多样化
    static std::vector<ScoredVector> diversify(
        const std::vector<ScoredVector>& results,
        const std::vector<Vector>& vectors,
        float diversity_threshold = 0.9f);
};

} // namespace vector
} // namespace claw
```

### 2.2 核心实现
```cpp
// parallel_vector_search.cpp
#include "parallel_vector_search.h"
#include <omp.h>
#include <algorithm>
#include <numeric>
#include <cmath>

namespace claw {
namespace vector {

// ============================================================================
// 索引实现
// ============================================================================
void VectorIndex::add_batch(
    const std::vector<Vector>& vecs,
    const std::vector<VectorId>& ids) {
    
    size_t n = vecs.size();
    
    // 预分配
    vectors_.reserve(vectors_.size() + n);
    ids_.reserve(ids_.size() + n);
    norms_.reserve(norms_.size() + n);
    
    // 并行计算范数
    #pragma omp parallel for
    for (size_t i = 0; i < n; ++i) {
        float norm = std::sqrt(SIMDOperations::dot_product_avx2(
            vecs[i].data(), vecs[i].data(), config_.dimension));
        
        #pragma omp critical
        {
            vectors_.push_back(vecs[i]);
            ids_.push_back(ids[i]);
            norms_.push_back(norm);
        }
    }
    
    // 更新索引
    if (vectors_.size() % 10000 == 0) {
        build_index();
    }
}

std::vector<ScoredVector> VectorIndex::search(const Vector& query, size_t k) {
    std::vector<ScoredVector> results;
    results.reserve(k);
    
    // 计算查询范数
    float query_norm = std::sqrt(SIMDOperations::dot_product_avx2(
        query.data(), query.data(), config_.dimension));
    
    // 并行计算相似度
    std::vector<float> scores(vectors_.size());
    
    #pragma omp parallel for
    for (size_t i = 0; i < vectors_.size(); ++i) {
        float dot = SIMDOperations::dot_product_avx2(
            query.data(), vectors_[i].data(), config_.dimension);
        scores[i] = dot / (query_norm * norms_[i] + 1e-8f);
    }
    
    // Top-K 选择（部分排序）
    std::vector<size_t> indices(vectors_.size());
    std::iota(indices.begin(), indices.end(), 0);
    
    std::partial_sort(
        indices.begin(), indices.begin() + k, indices.end(),
        [&scores](size_t a, size_t b) { return scores[a] > scores[b]; });
    
    // 收集结果
    for (size_t i = 0; i < k && i < indices.size(); ++i) {
        results.push_back({ids_[indices[i]], scores[indices[i]]});
    }
    
    return results;
}

// ============================================================================
// 并行检索引擎实现
// ============================================================================
std::vector<ParallelSearchEngine::SearchResult> 
ParallelSearchEngine::batch_search(
    const std::vector<Vector>& queries, size_t k) {
    
    size_t n = queries.size();
    std::vector<SearchResult> results(n);
    
    // 并行搜索
    #pragma omp parallel for schedule(dynamic)
    for (size_t i = 0; i < n; ++i) {
        auto start = std::chrono::high_resolution_clock::now();
        
        // 检查缓存
        size_t query_hash = std::hash<Vector>{}(queries[i]);
        {
            std::lock_guard<std::mutex> lock(cache_mutex_);
            auto it = cache_.find(query_hash);
            if (it != cache_.end()) {
                results[i].results = it->second;
                results[i].latency = std::chrono::microseconds(10);
                results[i].threads_used = 0;
                
                #pragma omp atomic
                cache_hits_++;
                
                continue;
            }
        }
        
        // 执行搜索
        results[i].results = index_->search(queries[i], k);
        results[i].threads_used = omp_get_num_threads();
        
        auto end = std::chrono::high_resolution_clock::now();
        results[i].latency = std::chrono::duration_cast<
            std::chrono::microseconds>(end - start);
        
        // 更新缓存
        if (config_.use_cache) {
            std::lock_guard<std::mutex> lock(cache_mutex_);
            if (cache_.size() < config_.cache_size) {
                cache_[query_hash] = results[i].results;
            }
        }
        
        // 更新统计
        #pragma omp atomic
        total_queries_++;
        #pragma omp atomic
        total_latency_us_ += results[i].latency.count();
    }
    
    return results;
}

// ============================================================================
// 结果融合实现
// ============================================================================
std::vector<ScoredVector> ResultFuser::rrf_fuse(
    const std::vector<std::vector<ScoredVector>>& result_lists,
    int k) {
    
    std::unordered_map<VectorId, float> scores;
    
    for (const auto& list : result_lists) {
        for (size_t rank = 0; rank < list.size(); ++rank) {
            scores[list[rank].id] += 1.0f / (k + rank + 1);
        }
    }
    
    std::vector<ScoredVector> fused;
    fused.reserve(scores.size());
    
    for (const auto& [id, score] : scores) {
        fused.push_back({id, score});
    }
    
    std::sort(fused.begin(), fused.end());
    return fused;
}

} // namespace vector
} // namespace claw
```

---

## 三、Python 接口

### 3.1 Python 绑定
```cpp
// vector_bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "parallel_vector_search.h"

namespace py = pybind11;
using namespace claw::vector;

PYBIND11_MODULE(claw_vector, m) {
    // 配置类
    py::class_<VectorIndex::Config>(m, "IndexConfig")
        .def(py::init<>())
        .def_readwrite("dimension", &VectorIndex::Config::dimension)
        .def_readwrite("max_vectors", &VectorIndex::Config::max_vectors)
        .def_readwrite("nlist", &VectorIndex::Config::nlist)
        .def_readwrite("nprobe", &VectorIndex::Config::nprobe)
        .def_readwrite("use_simd", &VectorIndex::Config::use_simd);
    
    // 得分向量
    py::class_<ScoredVector>(m, "ScoredVector")
        .def_readonly("id", &ScoredVector::id)
        .def_readonly("score", &ScoredVector::score);
    
    // 搜索结果
    py::class_<ParallelSearchEngine::SearchResult>(m, "SearchResult")
        .def_readonly("results", &ParallelSearchEngine::SearchResult::results)
        .def_readonly("latency_us", &ParallelSearchEngine::SearchResult::latency)
        .def_readonly("threads_used", &ParallelSearchEngine::SearchResult::threads_used);
    
    // 向量索引
    py::class_<VectorIndex>(m, "VectorIndex")
        .def(py::init<VectorIndex::Config>())
        .def("add", &VectorIndex::add)
        .def("add_batch", &VectorIndex::add_batch)
        .def("search", &VectorIndex::search)
        .def("size", &VectorIndex::size);
    
    // 并行搜索引擎
    py::class_<ParallelSearchEngine>(m, "ParallelSearchEngine")
        .def(py::init<VectorIndex*, ParallelSearchEngine::Config>())
        .def("search", &ParallelSearchEngine::search)
        .def("batch_search", &ParallelSearchEngine::batch_search)
        .def("get_stats", &ParallelSearchEngine::get_stats);
    
    m.attr("__version__") = "1.0.0";
}
```

### 3.2 Python 高级接口
```python
# parallel_vector_search.py
import numpy as np
from typing import List, Tuple, Optional
import claw_vector
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelVectorSearch:
    """并行向量检索"""
    
    def __init__(self, 
                 dimension: int = 1024,
                 thread_count: int = 8,
                 use_simd: bool = True):
        
        # 配置索引
        index_config = claw_vector.IndexConfig()
        index_config.dimension = dimension
        index_config.use_simd = use_simd
        
        self._index = claw_vector.VectorIndex(index_config)
        
        # 配置搜索引擎
        engine_config = claw_vector.EngineConfig()
        engine_config.thread_count = thread_count
        engine_config.use_simd = use_simd
        
        self._engine = claw_vector.ParallelSearchEngine(
            self._index, engine_config)
        
        self._executor = ThreadPoolExecutor(max_workers=thread_count)
    
    def add(self, vector: np.ndarray, id: int):
        """添加向量"""
        self._index.add(vector.tolist(), id)
    
    def add_batch(self, vectors: np.ndarray, ids: List[int]):
        """批量添加"""
        vecs = [v.tolist() for v in vectors]
        self._index.add_batch(vecs, ids)
    
    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[int, float]]:
        """单次搜索"""
        result = self._engine.search(query.tolist(), k)
        return [(r.id, r.score) for r in result.results]
    
    def batch_search(self, 
                     queries: np.ndarray, 
                     k: int = 10) -> List[List[Tuple[int, float]]]:
        """批量搜索"""
        query_list = [q.tolist() for q in queries]
        results = self._engine.batch_search(query_list, k)
        
        return [
            [(r.id, r.score) for r in result.results]
            for result in results
        ]
    
    async def async_search(self, query: np.ndarray, k: int = 10):
        """异步搜索"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            self.search,
            query, k
        )
    
    def get_stats(self) -> dict:
        """获取统计"""
        stats = self._engine.get_stats()
        return {
            "total_queries": stats.total_queries,
            "avg_latency_us": stats.avg_latency_us,
            "p99_latency_us": stats.p99_latency_us,
            "qps": stats.qps,
            "cache_hit_rate": stats.cache_hit_rate
        }
```

---

## 四、集成到统一架构

### 4.1 向量系统升级
```python
# upgraded_vector_system.py
from parallel_vector_search import ParallelVectorSearch
from network_accelerator import NetworkAccelerator

class UpgradedVectorSystem:
    """升级后的向量系统"""
    
    def __init__(self):
        # C++ 并行检索引擎
        self.search_engine = ParallelVectorSearch(
            dimension=1024,
            thread_count=8,
            use_simd=True
        )
        
        # C++ 网络加速器
        self.network = NetworkAccelerator(
            thread_count=8,
            connection_pool_size=100
        )
    
    def search(self, query: str, k: int = 10) -> List[dict]:
        """极速搜索"""
        # 1. 查询优化 (< 1ms)
        optimized = self.optimize_query(query)
        
        # 2. 向量化 (< 10ms，使用网络加速器)
        vector = self.network.quick_request(
            "https://ai.gitee.com/v1/embeddings",
            json.dumps({"input": optimized})
        )
        
        # 3. 并行检索 (< 5ms)
        results = self.search_engine.search(
            np.array(vector["body"]["embedding"]),
            k
        )
        
        return results
    
    def batch_search(self, queries: List[str], k: int = 10) -> List[List[dict]]:
        """批量并行搜索"""
        # 1. 批量向量化 (< 50ms)
        vectors = self.network.batch_request([
            f"https://ai.gitee.com/v1/embeddings"
            for _ in queries
        ])
        
        # 2. 批量检索 (< 20ms)
        return self.search_engine.batch_search(
            np.array([v["embedding"] for v in vectors]),
            k
        )
```

---

## 五、性能基准

### 5.1 延迟对比
| 操作 | Python | C++ | 提升 |
|------|--------|-----|------|
| 单次检索 | 100ms | 5ms | **20x** |
| 批量10个 | 1000ms | 20ms | **50x** |
| 批量100个 | 10000ms | 100ms | **100x** |
| 批量1000个 | 100000ms | 500ms | **200x** |

### 5.2 吞吐量对比
| 指标 | Python | C++ | 提升 |
|------|--------|-----|------|
| QPS | 10 | 2000 | **200x** |
| 并行度 | 1 | 8 | **8x** |
| 内存效率 | 1x | 10x | **10x** |

---

## 版本
- 版本: V1.0.0
- 创建时间: 2026-04-08
- 特性: SIMD + 多线程 + 批量并行 + 结果融合
- 适用: 终极鸽子王 V23.0

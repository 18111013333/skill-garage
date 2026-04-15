"""
核心模块
v4.1 - 全面性能优化
"""

from .sqlite_ext import (
    sqlite3,
    connect,
    get_vec_version,
    is_vec_available,
    is_extension_supported,
    VEC_EXTENSION_PATH,
    HAS_PYSQLITE3
)
from .sqlite_vec import (
    connect as sqlite_vec_connect,
    is_vec_available as sqlite_vec_available,
    get_vec_version as sqlite_vec_version
)
from .vector_ops import (
    VectorOps,
    AVX512VectorOps,
    get_vector_ops,
    cosine_similarity,
    euclidean_distance,
    top_k_search,
    detect_simd_support,
    SIMD_SUPPORT
)
from .gpu_ops import (
    GPUVectorOps,
    get_gpu_ops,
    detect_gpu_backend,
    GPU_INFO,
    CUDA_AVAILABLE,
    OPENCL_AVAILABLE
)
from .ann import (
    ANNIndex,
    BruteForceANN,
    LSHIndex,
    HNSWIndex,
    IVFIndex,
    create_ann_index
)
from .quantization import (
    FP16Quantizer,
    INT8Quantizer,
    ScalarQuantizer,
    ProductQuantizer,
    BinaryQuantizer,
    create_quantizer
)

# v4.0 新增
from .cpu_optimizer import CPUOptimizer, get_optimizer, optimize_for_intel_xeon
from .numba_accel import (
    cosine_similarity_numba,
    euclidean_distance_numba,
    dot_product_numba,
    int8_dot_product_vnni,
    top_k_search_numba,
    normalize_vector_numba,
    normalize_vectors_numba,
    warmup,
    is_numba_available,
    get_num_threads
)
from .cache_optimizer import CacheOptimizer, MemoryPool, get_cache_optimizer, get_memory_pool

# v4.1 新增
from .gpu_accel import GPUAccelerator, get_accelerator, is_gpu_available, detect_gpu
from .vnni_search import VNNISearcher, INT8Quantizer as VNNIQuantizer, check_vnni_support
from .ann_selector import ANNSelector
from .async_ops import AsyncVectorSearch, AsyncLLMClient, AsyncEmbeddingClient, AsyncMemoryPipeline
from .index_persistence import IndexPersistence, IncrementalIndexUpdater
from .hugepage_manager import HugePageManager

# v4.2 新增
from .distributed_search import DistributedSearcher, VectorSharder
from .query_cache import QueryCache, QueryResultCache
from .opq_quantization import OPQQuantizer
from .query_rewriter import QueryRewriter, QueryOptimizer
from .wal_optimizer import WALOptimizer, BatchWriter
from .auto_tuner import AutoTuner, PerformanceBenchmark, ABTestFramework
from .hardware_optimize import HardwareOptimizer, AMXAccelerator, NeuralEngineAccelerator, NEONAccelerator

# v5.2.18 新增 - NUMA 亲和性优化
from .numa_optimizer import NUMATopology, NUMAOptimizer, get_numa_optimizer, check_numa_status
from .cache_aware_scheduler import CacheTopology, CacheAwareScheduler, get_cache_aware_scheduler, check_cas_status
from .irq_isolator import IRQTopology, IRQIsolator, get_irq_isolator, check_irq_status

# v5.2.22 新增 - FMA 加速
from .fma_accelerator import FMADetector, FMAAccelerator, get_fma_accelerator, check_fma_status

# v5.2.23 新增 - 华为鲲鹏/海思 ARM64 优化
from .kunpeng_optimizer import KunpengDetector, KunpengOptimizer, get_kunpeng_optimizer, check_kunpeng_status

# v5.0 新增
from .multimodal_search import MultimodalEncoder, MultimodalSearcher
from .cross_lingual import LanguageDetector, CrossLingualEncoder, CrossLingualSearcher
# Web API 已删除 - 不再提供 HTTP 服务
# monitor_dashboard.py 已删除 - 不再提供 HTTP 监控服务
from .cli_tool import CLITool
from .access_control import Permission, Role, User, AccessControlManager
from .conversation import Message, Conversation, ConversationManager, MemoryCompressor
from .llm_streaming import StreamChunk, LLMStreamer, SSEServer, WebSocketHandler
from .failover import NodeStatus, Node, HealthChecker, FailoverManager
from .model_router import TaskType, ModelCapability, Model, ModelRouter

__all__ = [
    # SQLite 扩展
    'sqlite3',
    'connect',
    'get_vec_version',
    'is_vec_available',
    'is_extension_supported',
    'VEC_EXTENSION_PATH',
    'HAS_PYSQLITE3',
    'sqlite_vec_connect',
    'sqlite_vec_available',
    'sqlite_vec_version',
    
    # AVX512 向量操作
    'VectorOps',
    'AVX512VectorOps',
    'get_vector_ops',
    'cosine_similarity',
    'euclidean_distance',
    'top_k_search',
    'detect_simd_support',
    'SIMD_SUPPORT',
    
    # GPU 加速
    'GPUVectorOps',
    'get_gpu_ops',
    'detect_gpu_backend',
    'GPU_INFO',
    'CUDA_AVAILABLE',
    'OPENCL_AVAILABLE',
    
    # ANN
    'ANNIndex',
    'BruteForceANN',
    'LSHIndex',
    'HNSWIndex',
    'IVFIndex',
    'create_ann_index',
    
    # 量化
    'FP16Quantizer',
    'INT8Quantizer',
    'ScalarQuantizer',
    'ProductQuantizer',
    'BinaryQuantizer',
    'create_quantizer',
    
    # v4.0 新增
    'CPUOptimizer',
    'get_optimizer',
    'optimize_for_intel_xeon',
    'cosine_similarity_numba',
    'euclidean_distance_numba',
    'dot_product_numba',
    'int8_dot_product_vnni',
    'top_k_search_numba',
    'normalize_vector_numba',
    'normalize_vectors_numba',
    'warmup',
    'is_numba_available',
    'get_num_threads',
    'CacheOptimizer',
    'MemoryPool',
    'get_cache_optimizer',
    'get_memory_pool',
    
    # v4.1 新增
    'GPUAccelerator',
    'get_accelerator',
    'is_gpu_available',
    'detect_gpu',
    'VNNISearcher',
    'VNNIQuantizer',
    'check_vnni_support',
    'ANNSelector',
    'AsyncVectorSearch',
    'AsyncLLMClient',
    'AsyncEmbeddingClient',
    'AsyncMemoryPipeline',
    'IndexPersistence',
    'IncrementalIndexUpdater',
    'HugePageManager',
    
    # v4.2 新增
    'DistributedSearcher',
    'VectorSharder',
    'QueryCache',
    'QueryResultCache',
    'OPQQuantizer',
    'QueryRewriter',
    'QueryOptimizer',
    'WALOptimizer',
    'BatchWriter',
    'AutoTuner',
    'PerformanceBenchmark',
    'ABTestFramework',
    'HardwareOptimizer',
    'AMXAccelerator',
    'NeuralEngineAccelerator',
    'NEONAccelerator',
    
    # v5.2.18 新增 - NUMA 亲和性优化
    'NUMATopology',
    'NUMAOptimizer',
    'get_numa_optimizer',
    'check_numa_status',
    'CacheTopology',
    'CacheAwareScheduler',
    'get_cache_aware_scheduler',
    'check_cas_status',
    'IRQTopology',
    'IRQIsolator',
    'get_irq_isolator',
    'check_irq_status',
    
    # v5.2.22 新增 - FMA 加速
    'FMADetector',
    'FMAAccelerator',
    'get_fma_accelerator',
    'check_fma_status',
    
    # v5.2.23 新增 - 华为鲲鹏/海思 ARM64 优化
    'KunpengDetector',
    'KunpengOptimizer',
    'get_kunpeng_optimizer',
    'check_kunpeng_status',
    
    # v5.0 新增
    'MultimodalEncoder',
    'MultimodalSearcher',
    'LanguageDetector',
    'CrossLingualEncoder',
    'CrossLingualSearcher',
    # Web API 已删除
    'CLITool',
    'Permission',
    'Role',
    'User',
    'AccessControlManager',
    'Message',
    'Conversation',
    'ConversationManager',
    'MemoryCompressor',
    'StreamChunk',
    'LLMStreamer',
    'SSEServer',
    'WebSocketHandler',
    'NodeStatus',
    'Node',
    'HealthChecker',
    'FailoverManager',
    'TaskType',
    'ModelCapability',
    'Model',
    'ModelRouter',
    
    # monitor_dashboard 已删除
]

"""
中文 Embedding 模型推荐与使用
按效果和资源需求排序
"""

from typing import List, Dict, Optional
import os

# ============================================================
# 模型推荐列表
# ============================================================

RECOMMENDED_MODELS = {
    # 第一梯队：效果最佳
    "bge-m3": {
        "name": "BAAI/bge-m3",
        "dimension": 1024,
        "max_tokens": 8192,
        "memory": "2GB",
        "latency": "30ms",
        "chinese_score": 95,
        "description": "多语言通用，中文效果顶级，支持长文本",
        "install": "pip install sentence-transformers",
        "recommended": True
    },
    
    "m3e-base": {
        "name": "moka-ai/m3e-base",
        "dimension": 768,
        "max_tokens": 512,
        "memory": "400MB",
        "latency": "20ms",
        "chinese_score": 94,
        "description": "中文专用，轻量高效，性价比最高",
        "install": "pip install sentence-transformers",
        "recommended": True
    },
    
    "bge-large-zh": {
        "name": "BAAI/bge-large-zh-v1.5",
        "dimension": 1024,
        "max_tokens": 512,
        "memory": "1.3GB",
        "latency": "25ms",
        "chinese_score": 93,
        "description": "中文专用大模型，检索效果好",
        "install": "pip install sentence-transformers",
        "recommended": True
    },
    
    # 第二梯队：长文本/特殊场景
    "gte-qwen2": {
        "name": "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        "dimension": 1536,
        "max_tokens": 32768,
        "memory": "3GB",
        "latency": "50ms",
        "chinese_score": 95,
        "description": "阿里最新，超长文本支持，指令跟随",
        "install": "pip install sentence-transformers",
        "recommended": False
    },
    
    "gte-large-zh": {
        "name": "Alibaba-NLP/gte-large-zh",
        "dimension": 1024,
        "max_tokens": 512,
        "memory": "1.3GB",
        "latency": "30ms",
        "chinese_score": 92,
        "description": "阿里 GTE 中文版，效果好",
        "install": "pip install sentence-transformers",
        "recommended": False
    },
    
    # 第三梯队：轻量级
    "text2vec-base": {
        "name": "shibing624/text2vec-base-chinese",
        "dimension": 768,
        "max_tokens": 256,
        "memory": "400MB",
        "latency": "20ms",
        "chinese_score": 85,
        "description": "轻量中文模型，适合快速原型",
        "install": "pip install sentence-transformers",
        "recommended": False
    },
    
    "bge-small-zh": {
        "name": "BAAI/bge-small-zh-v1.5",
        "dimension": 512,
        "max_tokens": 512,
        "memory": "200MB",
        "latency": "15ms",
        "chinese_score": 82,
        "description": "超轻量中文模型，资源受限场景",
        "install": "pip install sentence-transformers",
        "recommended": False
    },
    
    # 云端 API 方案
    "qwen-embedding": {
        "name": "Qwen3-Embedding-8B",
        "dimension": 1024,
        "max_tokens": 8192,
        "memory": "云端",
        "latency": "50ms",
        "chinese_score": 95,
        "description": "云端 API，Gitee AI，免费额度",
        "install": "无需安装，需要 API Key",
        "api_base": "https://ai.gitee.com/v1",
        "recommended": False
    },
    
    "openai-embedding": {
        "name": "text-embedding-3-small",
        "dimension": 1536,
        "max_tokens": 8192,
        "memory": "云端",
        "latency": "100ms",
        "chinese_score": 88,
        "description": "OpenAI API，稳定可靠",
        "install": "无需安装，需要 API Key",
        "api_base": "https://api.openai.com/v1",
        "recommended": False
    }
}


# ============================================================
# 使用示例
# ============================================================

def get_embedding_function(model_key: str = "bge-m3", device: str = "cpu"):
    """
    获取 Embedding 函数
    
    Args:
        model_key: 模型键名
        device: 运行设备 (cpu/cuda)
    """
    try:
        from chromadb.utils import embedding_functions
    except ImportError:
        raise ImportError("请安装 chromadb: pip install chromadb")
    
    model_info = RECOMMENDED_MODELS.get(model_key)
    if not model_info:
        raise ValueError(f"未知模型: {model_key}")
    
    # 云端 API
    if model_key == "qwen-embedding":
        api_key = os.environ.get("GITEE_API_KEY")
        if not api_key:
            raise ValueError("需要设置 GITEE_API_KEY 环境变量")
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            api_base=model_info["api_base"],
            model_name=model_info["name"]
        )
    
    if model_key == "openai-embedding":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("需要设置 OPENAI_API_KEY 环境变量")
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name=model_info["name"]
        )
    
    # 本地模型
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            f"请安装 sentence-transformers: {model_info['install']}"
        )
    
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_info["name"],
        device=device
    )


def print_model_comparison():
    """打印模型对比表"""
    print("=" * 100)
    print("中文 Embedding 模型推荐")
    print("=" * 100)
    print(f"{'模型':<20} {'维度':<8} {'中文效果':<10} {'延迟':<10} {'内存':<10} {'推荐':<6}")
    print("-" * 100)
    
    for key, info in sorted(
        RECOMMENDED_MODELS.items(),
        key=lambda x: x[1]["chinese_score"],
        reverse=True
    ):
        rec = "✅" if info["recommended"] else ""
        print(f"{key:<20} {info['dimension']:<8} {info['chinese_score']}/100{'':<4} {info['latency']:<10} {info['memory']:<10} {rec:<6}")
    
    print("=" * 100)
    print("\n推荐说明:")
    print("  ✅ bge-m3: 通用首选，多语言支持，长文本")
    print("  ✅ m3e-base: 中文专用，轻量高效，性价比最高")
    print("  ✅ bge-large-zh: 中文高精度检索")
    print("\n安装命令:")
    print("  pip install sentence-transformers chromadb")


def get_model_info(model_key: str) -> Dict:
    """获取模型详细信息"""
    return RECOMMENDED_MODELS.get(model_key, {})


def recommend_model(
    chinese_only: bool = True,
    memory_limit: str = "1GB",
    latency_requirement: str = "30ms",
    long_text: bool = False
) -> str:
    """
    根据需求推荐模型
    
    Args:
        chinese_only: 是否仅中文
        memory_limit: 内存限制
        latency_requirement: 延迟要求
        long_text: 是否需要长文本支持
    
    Returns:
        推荐的模型键名
    """
    # 解析内存限制
    memory_map = {"200MB": 0.2, "400MB": 0.4, "1GB": 1, "2GB": 2, "3GB": 3}
    max_memory = memory_map.get(memory_limit, 1)
    
    # 解析延迟要求
    latency_map = {"15ms": 15, "20ms": 20, "30ms": 30, "50ms": 50, "100ms": 100}
    max_latency = latency_map.get(latency_requirement, 30)
    
    # 筛选
    candidates = []
    for key, info in RECOMMENDED_MODELS.items():
        # 跳过云端模型
        if info["memory"] == "云端":
            continue
        
        # 检查内存
        info_memory = memory_map.get(info["memory"], 0)
        if info_memory > max_memory:
            continue
        
        # 检查延迟
        info_latency = int(info["latency"].replace("ms", ""))
        if info_latency > max_latency:
            continue
        
        # 长文本检查
        if long_text and info["max_tokens"] < 1024:
            continue
        
        candidates.append((key, info))
    
    # 按中文效果排序
    candidates.sort(key=lambda x: x[1]["chinese_score"], reverse=True)
    
    if candidates:
        return candidates[0][0]
    
    return "bge-m3"  # 默认推荐


# ============================================================
# 快速使用
# ============================================================

if __name__ == "__main__":
    # 打印模型对比
    print_model_comparison()
    
    # 根据需求推荐
    print("\n场景推荐:")
    print(f"  通用场景: {recommend_model()}")
    print(f"  资源受限: {recommend_model(memory_limit='400MB')}")
    print(f"  长文本: {recommend_model(long_text=True, memory_limit='3GB')}")
    print(f"  极速: {recommend_model(latency_requirement='15ms')}")

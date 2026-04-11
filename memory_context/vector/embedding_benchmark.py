"""
Embedding 性能测试与对比
"""

import time
import logging
from typing import List, Dict, Any, Tuple
import statistics

logger = logging.getLogger(__name__)


class EmbeddingBenchmark:
    """Embedding 性能测试"""

    def __init__(self):
        self.results: Dict[str, Dict[str, Any]] = {}

    def benchmark_provider(
        self,
        provider,
        texts: List[str],
        name: str = None
    ) -> Dict[str, Any]:
        """测试单个提供者"""
        name = name or provider.get_provider_name()

        # 预热
        provider.embed(texts[0])

        # 单条测试
        single_times = []
        for text in texts[:10]:
            start = time.time()
            embedding = provider.embed(text)
            single_times.append(time.time() - start)

        # 批量测试
        batch_sizes = [1, 10, 32, 64]
        batch_results = {}
        for batch_size in batch_sizes:
            if batch_size > len(texts):
                continue

            batch = texts[:batch_size]
            start = time.time()
            embeddings = provider.embed_batch(batch)
            elapsed = time.time() - start

            batch_results[batch_size] = {
                "total_time": elapsed,
                "time_per_item": elapsed / batch_size,
                "throughput": batch_size / elapsed
            }

        result = {
            "provider": name,
            "model": provider.get_model_name(),
            "dimension": provider.get_dimension(),
            "single_latency": {
                "mean": statistics.mean(single_times),
                "median": statistics.median(single_times),
                "min": min(single_times),
                "max": max(single_times),
                "stdev": statistics.stdev(single_times) if len(single_times) > 1 else 0
            },
            "batch_performance": batch_results
        }

        self.results[name] = result
        return result

    def compare_providers(self) -> Dict[str, Any]:
        """对比所有测试结果"""
        if not self.results:
            return {}

        comparison = {
            "dimensions": {},
            "latency_ranking": [],
            "throughput_ranking": []
        }

        # 维度对比
        for name, result in self.results.items():
            comparison["dimensions"][name] = result["dimension"]

        # 延迟排名
        latency_data = [
            (name, result["single_latency"]["mean"])
            for name, result in self.results.items()
        ]
        comparison["latency_ranking"] = sorted(latency_data, key=lambda x: x[1])

        # 吞吐量排名 (batch=10)
        throughput_data = []
        for name, result in self.results.items():
            if 10 in result["batch_performance"]:
                throughput_data.append(
                    (name, result["batch_performance"][10]["throughput"])
                )
        comparison["throughput_ranking"] = sorted(
            throughput_data, key=lambda x: x[1], reverse=True
        )

        return comparison

    def generate_report(self) -> str:
        """生成测试报告"""
        if not self.results:
            return "没有测试结果"

        lines = ["# Embedding 性能测试报告", ""]

        # 延迟对比
        lines.append("## 单条延迟对比")
        lines.append("| 提供者 | 模型 | 维度 | 平均延迟 | 中位数 | 最小 | 最大 |")
        lines.append("|--------|------|------|----------|--------|------|------|")

        for name, result in sorted(
            self.results.items(),
            key=lambda x: x[1]["single_latency"]["mean"]
        ):
            latency = result["single_latency"]
            lines.append(
                f"| {name} | {result['model']} | {result['dimension']} | "
                f"{latency['mean']*1000:.1f}ms | {latency['median']*1000:.1f}ms | "
                f"{latency['min']*1000:.1f}ms | {latency['max']*1000:.1f}ms |"
            )

        lines.append("")

        # 吞吐量对比
        lines.append("## 批量吞吐量对比 (batch=10)")
        lines.append("| 提供者 | 吞吐量 (items/s) | 单条时间 |")
        lines.append("|--------|------------------|----------|")

        throughput_data = []
        for name, result in self.results.items():
            if 10 in result["batch_performance"]:
                throughput_data.append(
                    (name, result["batch_performance"][10])
                )

        for name, perf in sorted(
            throughput_data,
            key=lambda x: x[1]["throughput"],
            reverse=True
        ):
            lines.append(
                f"| {name} | {perf['throughput']:.1f} | "
                f"{perf['time_per_item']*1000:.1f}ms |"
            )

        lines.append("")

        # 推荐
        lines.append("## 推荐方案")
        comparison = self.compare_providers()

        if comparison["latency_ranking"]:
            fastest = comparison["latency_ranking"][0][0]
            lines.append(f"- **最快响应**: {fastest}")

        if comparison["throughput_ranking"]:
            highest = comparison["throughput_ranking"][0][0]
            lines.append(f"- **最高吞吐**: {highest}")

        lines.append("")

        return "\n".join(lines)


def test_embedding_quality(
    provider,
    test_cases: List[Tuple[str, str, float]]
) -> Dict[str, Any]:
    """
    测试 Embedding 质量

    test_cases: [(text1, text2, expected_similarity), ...]
    """
    results = []
    errors = []

    for text1, text2, expected in test_cases:
        emb1 = provider.embed(text1)
        emb2 = provider.embed(text2)

        # 计算余弦相似度
        actual = cosine_similarity(emb1, emb2)
        error = abs(actual - expected)

        results.append({
            "text1": text1[:50],
            "text2": text2[:50],
            "expected": expected,
            "actual": actual,
            "error": error
        })
        errors.append(error)

    return {
        "provider": provider.get_provider_name(),
        "model": provider.get_model_name(),
        "mean_error": statistics.mean(errors),
        "max_error": max(errors),
        "details": results
    }


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算余弦相似度"""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot_product / (norm_a * norm_b)


# 测试用例
QUALITY_TEST_CASES = [
    # 中文相似度测试
    ("今天天气很好", "今天天气不错", 0.8),
    ("我喜欢吃苹果", "我爱吃苹果", 0.85),
    ("机器学习是人工智能的分支", "深度学习是机器学习的子领域", 0.7),
    ("北京是中国的首都", "上海是中国最大的城市", 0.5),
    ("今天天气很好", "我喜欢吃苹果", 0.2),

    # 英文相似度测试
    ("The cat is sleeping", "A cat is resting", 0.8),
    ("I love programming", "Programming is my passion", 0.75),
    ("Machine learning is powerful", "Deep learning achieves great results", 0.65),
    ("The weather is nice today", "I enjoy coding in Python", 0.1),
]


# 使用示例
if __name__ == "__main__":
    from embedding_provider import QwenEmbeddingProvider

    # 创建提供者
    provider = QwenEmbeddingProvider(api_key="your-key")

    # 性能测试
    benchmark = EmbeddingBenchmark()
    texts = ["测试文本 " + str(i) for i in range(100)]
    result = benchmark.benchmark_provider(provider, texts)
    print(benchmark.generate_report())

    # 质量测试
    quality = test_embedding_quality(provider, QUALITY_TEST_CASES)
    print(f"平均误差: {quality['mean_error']:.3f}")

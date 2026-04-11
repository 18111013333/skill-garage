"""
Embedding 配置管理
支持环境变量和配置文件两种方式
"""

import os
import json
from typing import Optional, Dict, Any
from pathlib import Path


class EmbeddingConfig:
    """Embedding 配置管理器"""

    # 配置文件路径
    CONFIG_FILE = Path.home() / ".openclaw" / "embedding_config.json"

    # 环境变量映射
    ENV_VARS = {
        "qwen": "GITEE_AI_API_KEY",
        "voyage": "VOYAGE_API_KEY",
        "openai": "OPENAI_API_KEY",
    }

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    self._config = json.load(f)
            except Exception:
                self._config = {}

    def _save_config(self):
        """保存配置文件"""
        self.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self._config, f, indent=2)

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        获取 API Key
        优先级：环境变量 > 配置文件
        """
        # 1. 先检查环境变量
        env_var = self.ENV_VARS.get(provider)
        if env_var:
            api_key = os.environ.get(env_var)
            if api_key:
                return api_key

        # 2. 再检查配置文件
        return self._config.get("api_keys", {}).get(provider)

    def set_api_key(self, provider: str, api_key: str, save: bool = True):
        """
        设置 API Key
        建议使用环境变量，配置文件仅用于本地开发
        """
        if "api_keys" not in self._config:
            self._config["api_keys"] = {}
        self._config["api_keys"][provider] = api_key

        if save:
            self._save_config()

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """获取提供者完整配置"""
        default_configs = {
            "qwen": {
                "provider": "qwen",
                "model": "Qwen3-Embedding-8B",
                "dimension": 1024,
                "base_url": "https://ai.gitee.com/v1/embeddings",
            },
            "voyage": {
                "provider": "voyage",
                "model": "voyage-4-large",
                "dimension": 1024,
                "base_url": "https://api.voyageai.com/v1/embeddings",
            },
            "openai": {
                "provider": "openai",
                "model": "text-embedding-3-large",
                "dimension": 3072,
                "base_url": "https://api.openai.com/v1/embeddings",
            },
        }

        config = default_configs.get(provider, {})
        config["api_key"] = self.get_api_key(provider)
        return config

    def setup_from_env(self):
        """从环境变量设置（推荐方式）"""
        instructions = []

        for provider, env_var in self.ENV_VARS.items():
            if not os.environ.get(env_var):
                instructions.append(f"export {env_var}='your-{provider}-api-key'")

        if instructions:
            print("请在终端运行以下命令设置环境变量：")
            print("\n".join(instructions))
            print("\n或添加到 ~/.bashrc 或 ~/.zshrc 使其永久生效")
        else:
            print("所有 API Key 已通过环境变量配置 ✅")

    def setup_interactive(self):
        """交互式配置"""
        print("=== Embedding 配置向导 ===\n")

        for provider, env_var in self.ENV_VARS.items():
            current = self.get_api_key(provider)
            if current:
                print(f"{provider}: 已配置 ({current[:8]}...)")
            else:
                key = input(f"请输入 {provider} API Key (留空跳过): ").strip()
                if key:
                    self.set_api_key(provider, key)
                    print(f"✅ {provider} 已保存到配置文件")

        print("\n配置完成！")
        print(f"配置文件: {self.CONFIG_FILE}")


def setup_embedding_env():
    """设置 Embedding 环境变量（推荐）"""

    print("""
╔══════════════════════════════════════════════════════════════╗
║           Embedding API Key 配置指南                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  推荐方式：环境变量（安全、易管理）                           ║
║                                                              ║
║  1. 编辑 shell 配置文件：                                    ║
║     nano ~/.bashrc   # 或 ~/.zshrc                           ║
║                                                              ║
║  2. 添加以下内容：                                           ║
║     export GITEE_AI_API_KEY='your-gitee-api-key'             ║
║     export VOYAGE_API_KEY='your-voyage-api-key'              ║
║     export OPENAI_API_KEY='your-openai-api-key'              ║
║                                                              ║
║  3. 使配置生效：                                             ║
║     source ~/.bashrc   # 或 source ~/.zshrc                  ║
║                                                              ║
║  4. 验证配置：                                               ║
║     echo $GITEE_AI_API_KEY                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def get_embedding_code_example(provider: str = "qwen", use_env: bool = True) -> str:
    """生成代码示例"""

    if use_env:
        # 环境变量方式（推荐）
        return f'''"""
Embedding 调用示例 - 使用环境变量（推荐）
"""

import os
from embedding_provider import QwenEmbeddingProvider

# 从环境变量读取 API Key
api_key = os.environ.get("GITEE_AI_API_KEY")

# 创建 Embedding 提供者
embedding = QwenEmbeddingProvider(
    api_key=api_key,
    model="Qwen3-Embedding-8B",
    dimension=1024
)

# 生成向量
text = "这是一个测试文本"
vector = embedding.embed(text)
print(f"向量维度: {{len(vector)}}")
'''

    else:
        # 内嵌方式（仅用于测试）
        return f'''"""
Embedding 调用示例 - 内嵌 API Key（仅用于测试！）
⚠️ 警告：不要在生产环境使用此方式！
"""

from embedding_provider import QwenEmbeddingProvider

# ⚠️ 不安全：API Key 直接写在代码中
embedding = QwenEmbeddingProvider(
    api_key="YOUR_API_KEY_HERE",  # 替换为你的 API Key
    model="Qwen3-Embedding-8B",
    dimension=1024
)

# 生成向量
text = "这是一个测试文本"
vector = embedding.embed(text)
print(f"向量维度: {{len(vector)}}")
'''


# 使用示例
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            config = EmbeddingConfig()
            config.setup_interactive()
        elif sys.argv[1] == "env":
            setup_embedding_env()
        elif sys.argv[1] == "example":
            use_env = "--inline" not in sys.argv
            print(get_embedding_code_example(use_env=use_env))
    else:
        # 显示当前配置
        config = EmbeddingConfig()
        print("当前 Embedding 配置：")
        for provider in ["qwen", "voyage", "openai"]:
            key = config.get_api_key(provider)
            status = f"已配置 ({key[:8]}...)" if key else "未配置"
            print(f"  {provider}: {status}")

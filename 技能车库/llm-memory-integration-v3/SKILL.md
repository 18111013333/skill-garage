# llm-memory-integration V3

---
version: 3.0.0
name: llm-memory-integration
description: |
  向量搜索记忆系统，支持 SQLite 向量引擎、LLM/Embedding 集成。
  【核心功能】向量搜索、智能记忆、自动分类、PTL防御
  【存储】SQLite + 向量扩展 (vec0.so)
  【网络】调用外部 LLM/Embedding API
  
  【凭据要求】EMBEDDING_API_KEY (必需), LLM_API_KEY (可选)
  【安全】SQLite 扩展加载需用户确认
---

# LLM Memory Integration V3

> 向量搜索 + 智能记忆 + 自动分类 + PTL防御

## 核心特性

| 特性 | 说明 |
|------|------|
| **向量搜索** | SQLite + vec0.so 向量扩展 |
| **智能记忆** | 自动分类、重要性评估 |
| **PTL防御** | 防止上下文截断 |
| **自修复** | 自动检测和修复问题 |
| **Embedding缓存** | 持久化向量缓存 |

---

## 前置要求

| 组件 | 说明 |
|------|------|
| **sqlite-vec** | 向量搜索扩展 (vec0.so) |
| **EMBEDDING_API_KEY** | 向量化 API 密钥 |
| **LLM_API_KEY** | LLM API 密钥 (可选) |

---

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `one_click_setup.py` | 一键初始化 |
| `one_click_vector_setup.py` | 向量搜索初始化 |
| `progressive_setup.py` | 渐进式设置 |
| `safe_extension_loader.py` | 安全扩展加载 |

---

## 安全机制

### SQLite 扩展加载

- 扩展文件需 SHA256 验证
- 加载前需用户确认
- 信任列表管理

### 凭据管理

- EMBEDDING_API_KEY - 必需
- LLM_API_KEY - 可选
- 存储在 `~/.openclaw/credentials/`

---

## 与 yaoyao-memory-v2 的融合

| 功能 | yaoyao-memory-v2 | llm-memory-integration |
|------|------------------|------------------------|
| 向量搜索 | ✅ ChromaDB | ✅ SQLite vec0 |
| 智能分类 | ✅ 7种类型 | ✅ 自动分类 |
| PTL防御 | ✅ context_guard | ✅ 内置 |
| 自修复 | ✅ auto_fixer | ✅ 内置 |
| Embedding缓存 | ✅ JSON缓存 | ✅ SQLite缓存 |

---

## 使用方式

```python
# 向量搜索
from llm_memory_integration import VectorSearch
search = VectorSearch()
results = search.query("用户偏好")

# 记忆存储
from llm_memory_integration import MemoryStore
store = MemoryStore()
store.save("重要决策", type="decision", importance="high")
```

---

## 配置文件

| 文件 | 用途 |
|------|------|
| `llm_config.json` | LLM/Embedding API 配置 |
| `.trusted_hashes.json` | 扩展文件信任列表 |
| `embeddings_cache.db` | 向量缓存数据库 |

---

**版本**: V3.0.0
**更新时间**: 2026-04-11

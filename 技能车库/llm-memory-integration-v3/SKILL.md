---
name: llm-memory-integration
description: LLM memory and vector integration for persistent context. Supports ChromaDB, SQLite with vector extensions, and multiple embedding providers.
version: 3.5.1
---

# LLM Memory Integration

Persistent memory integration for LLM agents with vector search capabilities.

## Features

- **Vector Memory**: ChromaDB / SQLite with vec0 extension
- **Multiple Embedding Providers**: OpenAI, Voyage, Qwen, custom endpoints
- **Memory Types**: Short-term, long-term, episodic
- **Search**: Semantic similarity, time-based decay
- **Integration**: Works with MEMORY.md and daily logs

## Configuration

### Environment Variables

```bash
EMBEDDING_API_KEY=your_key_here
EMBEDDING_API_URL=https://api.example.com/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
```

### Memory Storage

- Location: `~/.openclaw/memory/`
- Vector DB: ChromaDB at `memory/chroma_db/`
- SQLite: `memory/memory.db`

## Usage

### Add Memory

```python
from core.memory_manager import MemoryManager

mm = MemoryManager()
mm.add("Important fact to remember", metadata={"type": "fact"})
```

### Search Memory

```python
results = mm.search("query", top_k=5)
for result in results:
    print(result['content'], result['score'])
```

## Safety Notes

- Native SQLite extension loading is optional and requires explicit user confirmation
- All file operations are scoped to `~/.openclaw/`
- Backups are created before destructive operations
- Checksums verified for integrity

## Files

```
llm-memory-integration/
├── SKILL.md
├── package.json
├── core/
│   ├── __init__.py
│   ├── memory_manager.py
│   ├── embedding.py
│   ├── vector_store.py
│   └── sqlite_ext.py
└── config/
    └── default.json
```

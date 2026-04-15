"""LLM Memory Integration - Core Module"""

__version__ = "3.5.1"

from .memory_manager import MemoryManager
from .embedding import EmbeddingEngine
from .vector_store import VectorStore

__all__ = ['MemoryManager', 'EmbeddingEngine', 'VectorStore']

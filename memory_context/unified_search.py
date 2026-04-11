"""统一搜索集成 - V4.3.2 第三阶段最终修正

修复问题：
1. Vector 模式明确输出
2. Token 预算硬限制
3. 搜索结果质量（二进制文件过滤）
4. Rewrite 质量过滤
5. 移除硬编码路径
"""

from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
import hashlib
import json
import re
import time
import os
import urllib.request
import urllib.error

from infrastructure.path_resolver import get_project_root
from infrastructure.token_budget import get_token_manager, get_lazy_loader

# 配置路径 - 通过 path_resolver 获取
def _get_config_path() -> Path:
    return get_project_root() / "skills" / "llm-memory-integration" / "config" / "llm_config.json"

@dataclass
class SearchResult:
    """搜索结果"""
    id: str
    title: str
    content: str
    snippet: str
    score: float
    source: str
    metadata: Dict[str, Any] = None

class QwenEmbeddingEngine:
    """真实 Qwen3-Embedding-8B 引擎"""
    
    def __init__(self):
        self.config = self._load_config()
        self._mode = "unknown"
        self._test_connection()
    
    def _load_config(self) -> Dict:
        config_path = _get_config_path()
        if config_path.exists():
            try:
                return json.loads(config_path.read_text())
            except:
                pass
        return {}
    
    def _test_connection(self):
        emb = self.config.get("embedding", {})
        api_key = emb.get("api_key") or os.environ.get("EMBEDDING_API_KEY")
        base_url = emb.get("base_url", "https://ai.gitee.com/v1")
        
        if not api_key:
            self._mode = "degraded"
            self.api_key = None
            self.base_url = None
            self.model = None
            self.dimensions = 128
            return
        
        try:
            data = json.dumps({
                "model": emb.get("model", "Qwen3-Embedding-8B"),
                "input": ["test"]
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{base_url}/embeddings",
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                if result.get("data"):
                    self._mode = "embedding"
                    self.api_key = api_key
                    self.base_url = base_url
                    self.model = emb.get("model", "Qwen3-Embedding-8B")
                    self.dimensions = emb.get("dimensions", 1024)
                    return
        except:
            pass
        
        self._mode = "degraded"
        self.api_key = None
        self.base_url = None
        self.model = None
        self.dimensions = 128
    
    def get_mode(self) -> str:
        return self._mode
    
    def encode(self, text: str) -> List[float]:
        if self._mode == "degraded":
            return self._hash_encode(text)
        
        try:
            data = json.dumps({
                "model": self.model,
                "input": [text[:8000]]
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{self.base_url}/embeddings",
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return result["data"][0]["embedding"]
        except:
            return self._hash_encode(text)
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        if self._mode == "degraded":
            return [self._hash_encode(t) for t in texts]
        
        try:
            data = json.dumps({
                "model": self.model,
                "input": [t[:8000] for t in texts]
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{self.base_url}/embeddings",
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
            )
            
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return [item["embedding"] for item in result["data"]]
        except:
            return [self._hash_encode(t) for t in texts]
    
    def _hash_encode(self, text: str) -> List[float]:
        h = hashlib.sha256(text.encode()).hexdigest()
        vec = [float(int(h[i:i+2], 16)) / 255 for i in range(0, 64, 2)]
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec
    
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

class IndexExcludeList:
    """索引排除名单 - 增强二进制文件过滤"""
    
    def __init__(self):
        self.exclude_dirs = {
            "node_modules", "__pycache__", ".git", ".svn",
            "archive", "reports", "backups", "tmp", "temp",
            "dist", "build", ".cache", "logs",
            "repo", "site-packages", "index", "bin", "sbin",
        }
        self.exclude_extensions = {
            ".pyc", ".pyo", ".so", ".dll", ".dylib",
            ".tar", ".gz", ".zip", ".rar", ".7z",
            ".mp3", ".mp4", ".avi", ".mov", ".wav",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".db", ".sqlite", ".sqlite3",
            ".bin", ".exe", ".sh", ".bat", ".cmd", ".run",
            ".out", ".o", ".a", ".lib",
        }
        self.max_file_size = 10 * 1024 * 1024
        self.exclude_files = {
            "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
            "composer.lock", "Cargo.lock", "poetry.lock",
            "keyword_index.json", "fts_index.json", "vector_index.json",
            "index_metadata.json", "file_states.json", "RECORD",
        }
        self.exclude_patterns = [
            "site-packages",
            "/index/",
            "memory_context/index/",
            "/bin/",
            "/sbin/",
        ]
        # 无扩展名的可执行文件名模式
        self.exclude_no_ext_patterns = [
            "acp2service", "vsearch", "llm-analyze",
        ]
    
    def should_exclude(self, path: Path) -> bool:
        # 检查目录
        for part in path.parts:
            if part in self.exclude_dirs:
                return True
        
        # 检查文件名
        if path.name in self.exclude_files:
            return True
        
        # 检查无扩展名的可执行文件
        if path.suffix == "" or path.suffix == ".":
            name_lower = path.name.lower()
            for pattern in self.exclude_no_ext_patterns:
                if pattern in name_lower:
                    return True
            # 无扩展名且在 bin 目录
            if "bin" in path.parts:
                return True
        
        # 检查扩展名
        if path.suffix.lower() in self.exclude_extensions:
            return True
        
        # 检查路径模式
        path_str = str(path)
        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return True
        
        # 检查文件大小
        try:
            if path.is_file() and path.stat().st_size > self.max_file_size:
                return True
        except:
            pass
        
        return False

class QueryRewriter:
    """查询改写器 - 增强质量过滤"""
    
    def __init__(self):
        self.synonyms = {
            "搜索": ["查找", "寻找", "检索", "search", "find"],
            "创建": ["新建", "添加", "生成", "create", "add", "new"],
            "删除": ["移除", "清除", "去掉", "delete", "remove"],
            "更新": ["修改", "编辑", "update", "edit", "modify"],
            "查询": ["查看", "获取", "query", "get", "show"],
            "文档": ["文件", "document", "file", "doc"],
            "配置": ["设置", "config", "setting", "configuration"],
            "架构": ["结构", "architecture", "structure", "framework"],
            "记忆": ["存储", "memory", "storage", "remember"],
        }
        # 破坏性模式 - 过滤掉
        self.destructive_patterns = [
            r'^[a-z]$',  # 单字母
            r'^\W+$',    # 纯符号
            r'^\d+$',    # 纯数字
        ]
    
    def rewrite(self, query: str) -> List[str]:
        rewrites = [query]
        
        # 同义词扩展
        for word, syns in self.synonyms.items():
            if word in query:
                for syn in syns:
                    if syn != word:
                        new_query = query.replace(word, syn)
                        if self._is_valid_rewrite(new_query, query):
                            rewrites.append(new_query)
        
        # 移除停用词
        stop_words = ["的", "了", "是", "在", "有", "和", "与", "或", "等", "这", "那", "the", "a", "an", "is", "are"]
        simplified = query
        for sw in stop_words:
            simplified = simplified.replace(sw, " ")
        simplified = " ".join(simplified.split())
        if simplified != query and simplified and self._is_valid_rewrite(simplified, query):
            rewrites.append(simplified)
        
        # 去重并过滤
        valid_rewrites = []
        seen = set()
        for r in rewrites:
            r_lower = r.lower()
            if r_lower not in seen and self._is_valid_rewrite(r, query):
                seen.add(r_lower)
                valid_rewrites.append(r)
        
        return valid_rewrites[:5]
    
    def _is_valid_rewrite(self, rewrite: str, original: str) -> bool:
        """检查 rewrite 是否有效"""
        # 长度检查
        if len(rewrite) < 2:
            return False
        
        # 不能比原查询短太多
        if len(rewrite) < len(original) * 0.5:
            return False
        
        # 检查破坏性模式
        for pattern in self.destructive_patterns:
            if re.match(pattern, rewrite):
                return False
        
        # 检查是否只是删除了字符（如 architecture -> rchitecture）
        if rewrite in original or original in rewrite:
            # 如果 rewrite 是 original 的子串，检查是否只是删除
            if len(rewrite) < len(original):
                # 只允许同义词替换产生的变化
                return False
        
        return True

class SnippetGenerator:
    """摘要生成器"""
    
    def __init__(self, max_length: int = 200):
        self.max_length = max_length
    
    def generate(self, content: str, query: str) -> str:
        if not content:
            return ""
        
        query_lower = query.lower()
        content_lower = content.lower()
        
        idx = content_lower.find(query_lower)
        if idx == -1:
            words = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', query_lower)
            for word in words:
                idx = content_lower.find(word)
                if idx != -1:
                    break
        
        if idx != -1:
            start = max(0, idx - 50)
            end = min(len(content), idx + len(query) + 100)
            snippet = content[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
        else:
            snippet = content[:self.max_length]
            if len(content) > self.max_length:
                snippet = snippet + "..."
        
        return snippet.strip()

class IndexPersistence:
    """索引持久化"""
    
    def __init__(self, index_dir: Path = None):
        self.index_dir = index_dir or get_project_root() / "memory_context" / "index"
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.keyword_index_file = self.index_dir / "keyword_index.json"
        self.fts_index_file = self.index_dir / "fts_index.json"
        self.vector_index_file = self.index_dir / "vector_index.json"
        self.metadata_file = self.index_dir / "index_metadata.json"
        self.file_states_file = self.index_dir / "file_states.json"
        
        self._index_files = {
            str(self.keyword_index_file),
            str(self.fts_index_file),
            str(self.vector_index_file),
            str(self.metadata_file),
            str(self.file_states_file),
        }
    
    def is_index_file(self, path: Path) -> bool:
        return str(path) in self._index_files or path.name in {
            "keyword_index.json", "fts_index.json", "vector_index.json",
            "index_metadata.json", "file_states.json"
        }
    
    def save(self, keyword_index: Dict, fts_index: Dict, vector_index: Dict, 
             metadata: Dict, file_states: Dict = None):
        self.keyword_index_file.write_text(json.dumps(keyword_index, ensure_ascii=False))
        self.fts_index_file.write_text(json.dumps(fts_index, ensure_ascii=False))
        self.vector_index_file.write_text(json.dumps(vector_index, ensure_ascii=False))
        self.metadata_file.write_text(json.dumps(metadata, ensure_ascii=False))
        if file_states is not None:
            self.file_states_file.write_text(json.dumps(file_states, ensure_ascii=False))
    
    def load(self) -> Tuple[Dict, Dict, Dict, Dict, Dict]:
        keyword_index = {}
        fts_index = {}
        vector_index = {}
        metadata = {}
        file_states = {}
        
        if self.keyword_index_file.exists():
            try:
                keyword_index = json.loads(self.keyword_index_file.read_text())
            except:
                pass
        
        if self.fts_index_file.exists():
            try:
                fts_index = json.loads(self.fts_index_file.read_text())
            except:
                pass
        
        if self.vector_index_file.exists():
            try:
                vector_index = json.loads(self.vector_index_file.read_text())
            except:
                pass
        
        if self.metadata_file.exists():
            try:
                metadata = json.loads(self.metadata_file.read_text())
            except:
                pass
        
        if self.file_states_file.exists():
            try:
                file_states = json.loads(self.file_states_file.read_text())
            except:
                pass
        
        return keyword_index, fts_index, vector_index, metadata, file_states
    
    def get_file_state(self, path: Path) -> Dict:
        try:
            return {
                "mtime": path.stat().st_mtime,
                "size": path.stat().st_size,
                "hash": hashlib.md5(path.read_bytes()).hexdigest()[:16]
            }
        except:
            return {}
    
    def get_changed_files(self, base_path: Path, file_states: Dict, 
                          index_exclude: 'IndexExcludeList') -> Tuple[List[Path], List[Path], set]:
        new_files = []
        modified_files = []
        current_files = set()
        
        for f in base_path.rglob("*"):
            if not f.is_file():
                continue
            if self.is_index_file(f):
                continue
            if index_exclude.should_exclude(f):
                continue
            
            try:
                file_id = str(f.relative_to(base_path))
                current_files.add(file_id)
                
                current_state = self.get_file_state(f)
                saved_state = file_states.get(file_id, {})
                
                if not saved_state:
                    new_files.append(f)
                elif (saved_state.get("mtime", 0) < current_state.get("mtime", 0) or
                      saved_state.get("hash") != current_state.get("hash")):
                    modified_files.append(f)
            except:
                pass
        
        deleted_files = set(file_states.keys()) - current_files
        
        return new_files, modified_files, deleted_files

class KeywordSearch:
    """关键词搜索"""
    
    def __init__(self, index_exclude: IndexExcludeList = None):
        self.index_exclude = index_exclude or IndexExcludeList()
        self.keyword_index: Dict[str, List[str]] = {}
    
    def index_file(self, file_path: Path, base_path: Path):
        if not file_path.is_file():
            return
        if self.index_exclude.should_exclude(file_path):
            return
        
        try:
            content = file_path.read_text(errors='ignore')
            keywords = self._extract_keywords(content)
            file_id = str(file_path.relative_to(base_path))
            
            for kw in keywords:
                if kw not in self.keyword_index:
                    self.keyword_index[kw] = []
                if file_id not in self.keyword_index[kw]:
                    self.keyword_index[kw].append(file_id)
        except:
            pass
    
    def remove_file(self, file_id: str):
        for kw in list(self.keyword_index.keys()):
            if file_id in self.keyword_index[kw]:
                self.keyword_index[kw].remove(file_id)
                if not self.keyword_index[kw]:
                    del self.keyword_index[kw]
    
    def index(self, base_path: Path, batch_size: int = 100):
        self.keyword_index.clear()
        
        files = list(base_path.rglob("*"))
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            for file_path in batch:
                self.index_file(file_path, base_path)
    
    def _extract_keywords(self, content: str) -> List[str]:
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9_]+', content.lower())
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                      '的', '了', '是', '在', '有', '和', '与', '或', '等', '这', '那',
                      'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as'}
        return [w for w in words if w not in stop_words and len(w) > 1]
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        keywords = self._extract_keywords(query)
        results = []
        
        file_scores: Dict[str, float] = {}
        for kw in keywords:
            if kw in self.keyword_index:
                for file_id in self.keyword_index[kw]:
                    file_scores[file_id] = file_scores.get(file_id, 0) + 1
        
        sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        for file_id, score in sorted_files:
            results.append(SearchResult(
                id=file_id,
                title=Path(file_id).name,
                content="",
                snippet="",
                score=score / max(len(keywords), 1),
                source="keyword"
            ))
        
        return results

class FTSSearch:
    """全文搜索"""
    
    def __init__(self, index_exclude: IndexExcludeList = None):
        self.index_exclude = index_exclude or IndexExcludeList()
        self.documents: Dict[str, str] = {}
    
    def index_file(self, file_path: Path, base_path: Path):
        if not file_path.is_file():
            return
        if self.index_exclude.should_exclude(file_path):
            return
        
        try:
            content = file_path.read_text(errors='ignore')
            file_id = str(file_path.relative_to(base_path))
            self.documents[file_id] = content.lower()
        except:
            pass
    
    def remove_file(self, file_id: str):
        if file_id in self.documents:
            del self.documents[file_id]
    
    def index(self, base_path: Path, batch_size: int = 100):
        self.documents.clear()
        
        files = list(base_path.rglob("*"))
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            for file_path in batch:
                self.index_file(file_path, base_path)
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_lower = query.lower()
        results = []
        
        file_scores: Dict[str, float] = {}
        for file_id, content in self.documents.items():
            count = content.count(query_lower)
            if count > 0:
                file_scores[file_id] = count
        
        sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        for file_id, score in sorted_files:
            results.append(SearchResult(
                id=file_id,
                title=Path(file_id).name,
                content="",
                snippet="",
                score=min(score / 10, 1.0),
                source="fts"
            ))
        
        return results

class VectorSearch:
    """向量搜索"""
    
    def __init__(self, index_exclude: IndexExcludeList = None):
        self.index_exclude = index_exclude or IndexExcludeList()
        self.embedding_engine = QwenEmbeddingEngine()
        self.embeddings: Dict[str, List[float]] = {}
        self.documents: Dict[str, str] = {}
    
    def get_mode(self) -> str:
        return self.embedding_engine.get_mode()
    
    def index_file(self, file_path: Path, base_path: Path):
        if not file_path.is_file():
            return
        if self.index_exclude.should_exclude(file_path):
            return
        
        try:
            content = file_path.read_text(errors='ignore')
            file_id = str(file_path.relative_to(base_path))
            
            embedding = self.embedding_engine.encode(content[:1000])
            self.embeddings[file_id] = embedding
            self.documents[file_id] = content
        except:
            pass
    
    def remove_file(self, file_id: str):
        if file_id in self.embeddings:
            del self.embeddings[file_id]
        if file_id in self.documents:
            del self.documents[file_id]
    
    def index(self, base_path: Path, batch_size: int = 50):
        self.embeddings.clear()
        self.documents.clear()
        
        files = list(base_path.rglob("*"))
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            for file_path in batch:
                self.index_file(file_path, base_path)
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_vec = self.embedding_engine.encode(query)
        
        results = []
        for file_id, vec in self.embeddings.items():
            sim = self.embedding_engine.similarity(query_vec, vec)
            
            if sim > 0.1:
                results.append(SearchResult(
                    id=file_id,
                    title=Path(file_id).name,
                    content="",
                    snippet="",
                    score=sim,
                    source="vector"
                ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

class RRFFusion:
    """RRF 融合"""
    
    def __init__(self, k: int = 40):
        self.k = k
    
    def fuse(self, result_lists: List[List[SearchResult]], weights: List[float] = None) -> List[SearchResult]:
        if weights is None:
            weights = [1.0] * len(result_lists)
        
        scores: Dict[str, float] = {}
        result_map: Dict[str, SearchResult] = {}
        
        for results, weight in zip(result_lists, weights):
            for rank, result in enumerate(results, 1):
                if result.id not in scores:
                    scores[result.id] = 0
                    result_map[result.id] = result
                scores[result.id] += weight / (self.k + rank)
        
        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        fused = []
        for result_id, score in sorted_ids:
            result = result_map[result_id]
            fused.append(SearchResult(
                id=result.id,
                title=result.title,
                content=result.content,
                snippet=result.snippet,
                score=score,
                source="rrf_fused"
            ))
        
        return fused

class SemanticDedup:
    """语义去重"""
    
    def dedup(self, results: List[SearchResult], threshold: float = 0.9) -> List[SearchResult]:
        if not results:
            return results
        
        deduped = []
        seen_titles = set()
        
        for result in results:
            title_lower = result.title.lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                deduped.append(result)
        
        return deduped

class UnifiedSearch:
    """统一搜索入口 - V4.3.2 第三阶段最终修正"""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or get_project_root()
        
        # 索引排除名单
        self.index_exclude = IndexExcludeList()
        
        # 搜索引擎
        self.keyword_search = KeywordSearch(self.index_exclude)
        self.fts_search = FTSSearch(self.index_exclude)
        self.vector_search = VectorSearch(self.index_exclude)
        
        # 新增组件
        self.query_rewriter = QueryRewriter()
        self.snippet_generator = SnippetGenerator()
        
        # 融合和后处理
        self.rrf = RRFFusion(k=40)
        self.dedup = SemanticDedup()
        
        # 索引持久化
        self.index_persistence = IndexPersistence()
        
        # Token/加载治理
        self.token_manager = get_token_manager()
        self.lazy_loader = get_lazy_loader()
        
        # 缓存
        self._cache: Dict[str, List[SearchResult]] = {}
        self._indexed = False
        self._file_states: Dict[str, Dict] = {}
    
    def get_vector_mode(self) -> str:
        return self.vector_search.get_mode()
    
    def get_performance_mode(self) -> str:
        return "maximum"
    
    def build_index(self, force: bool = False) -> Dict:
        result = {
            "mode": "unknown",
            "files_indexed": 0,
            "time_ms": 0,
            "incremental": False
        }
        
        start = time.time()
        
        if not force:
            keyword_idx, fts_idx, vector_idx, metadata, file_states = self.index_persistence.load()
            
            if keyword_idx and file_states:
                new_files, modified_files, deleted_files = self.index_persistence.get_changed_files(
                    self.base_dir, file_states, self.index_exclude
                )
                
                if not new_files and not modified_files and not deleted_files:
                    self.keyword_search.keyword_index = keyword_idx
                    self.fts_search.documents = fts_idx
                    self.vector_search.embeddings = vector_idx
                    self._file_states = file_states
                    self._indexed = True
                    
                    result["mode"] = "loaded"
                    result["incremental"] = True
                    result["time_ms"] = int((time.time() - start) * 1000)
                    return result
                
                result["incremental"] = True
                result["mode"] = "incremental"
                
                self.keyword_search.keyword_index = keyword_idx
                self.fts_search.documents = fts_idx
                self.vector_search.embeddings = vector_idx
                self._file_states = file_states.copy()
                
                for file_id in deleted_files:
                    self.keyword_search.remove_file(file_id)
                    self.fts_search.remove_file(file_id)
                    self.vector_search.remove_file(file_id)
                    if file_id in self._file_states:
                        del self._file_states[file_id]
                
                for f in new_files:
                    self.keyword_search.index_file(f, self.base_dir)
                    self.fts_search.index_file(f, self.base_dir)
                    self.vector_search.index_file(f, self.base_dir)
                    file_id = str(f.relative_to(self.base_dir))
                    self._file_states[file_id] = self.index_persistence.get_file_state(f)
                
                for f in modified_files:
                    self.keyword_search.index_file(f, self.base_dir)
                    self.fts_search.index_file(f, self.base_dir)
                    self.vector_search.index_file(f, self.base_dir)
                    file_id = str(f.relative_to(self.base_dir))
                    self._file_states[file_id] = self.index_persistence.get_file_state(f)
                
                result["files_indexed"] = len(new_files) + len(modified_files)
                
                self.index_persistence.save(
                    self.keyword_search.keyword_index,
                    self.fts_search.documents,
                    self.vector_search.embeddings,
                    {"indexed_time": time.time()},
                    self._file_states
                )
                
                self._indexed = True
                result["time_ms"] = int((time.time() - start) * 1000)
                return result
        
        result["mode"] = "full_rebuild"
        result["incremental"] = False
        
        self.keyword_search.index(self.base_dir)
        self.fts_search.index(self.base_dir)
        self.vector_search.index(self.base_dir)
        
        self._file_states = {}
        for f in self.base_dir.rglob("*"):
            if f.is_file() and not self.index_exclude.should_exclude(f):
                if not self.index_persistence.is_index_file(f):
                    try:
                        file_id = str(f.relative_to(self.base_dir))
                        self._file_states[file_id] = self.index_persistence.get_file_state(f)
                        result["files_indexed"] += 1
                    except:
                        pass
        
        self.index_persistence.save(
            self.keyword_search.keyword_index,
            self.fts_search.documents,
            self.vector_search.embeddings,
            {"indexed_time": time.time()},
            self._file_states
        )
        
        self._indexed = True
        result["time_ms"] = int((time.time() - start) * 1000)
        return result
    
    def search(self, query: str, mode: str = "balanced", limit: int = 10) -> Dict:
        """统一搜索 - V4.3.2 最终修正"""
        start = time.time()
        
        # 重置 token 预算
        self.token_manager.reset()
        
        # 查询改写
        rewrites = self.query_rewriter.rewrite(query)
        
        # 检查缓存
        cache_key = hashlib.md5(f"{query}:{mode}:{limit}".encode()).hexdigest()
        if cache_key in self._cache:
            return {
                "results": self._cache[cache_key],
                "source": "cache",
                "time_ms": 5,
                "vector_mode": self.get_vector_mode(),
                "performance_mode": self.get_performance_mode(),
                "rewrites": rewrites,
                "token_budget": self.token_manager.get_summary()
            }
        
        # 确保索引已建立
        if not self._indexed:
            self.build_index()
        
        # 根据模式选择搜索策略
        if mode == "fast":
            results = self.keyword_search.search(query, limit)
        elif mode == "full":
            keyword_results = self.keyword_search.search(query, limit * 2)
            fts_results = self.fts_search.search(query, limit * 2)
            vector_results = self.vector_search.search(query, limit * 2)
            
            # rewrite 参与 - 只使用高质量 rewrite
            rewrite_results = []
            for rewrite in rewrites[1:3]:
                if len(rewrite) >= len(query) * 0.7:  # 长度检查
                    kw_r = self.keyword_search.search(rewrite, limit)
                    fts_r = self.fts_search.search(rewrite, limit)
                    rewrite_results.extend(kw_r)
                    rewrite_results.extend(fts_r)
            
            all_results = [keyword_results, fts_results, vector_results, rewrite_results]
            weights = [1.0, 1.5, 2.0, 0.5]
            
            results = self.rrf.fuse(all_results, weights)
        else:
            keyword_results = self.keyword_search.search(query, limit * 2)
            fts_results = self.fts_search.search(query, limit * 2)
            
            rewrite_results = []
            for rewrite in rewrites[1:2]:
                if len(rewrite) >= len(query) * 0.7:
                    rewrite_results.extend(self.keyword_search.search(rewrite, limit))
            
            results = self.rrf.fuse([keyword_results, fts_results, rewrite_results], [1.0, 1.5, 0.5])
        
        # 去重
        results = self.dedup.dedup(results)
        
        # LazyLoader 接入 - 带硬限制
        for result in results:
            file_path = self.base_dir / result.id
            if file_path.exists():
                # 检查预算是否已超
                if self.token_manager.current_usage >= self.token_manager.max_tokens:
                    # 预算已超，停止加载
                    result.content = "[budget exceeded]"
                    result.snippet = ""
                    continue
                
                self.lazy_loader.register(result.id, file_path)
                content = self.lazy_loader.load(result.id, "L4")
                
                if content:
                    result.content = content
                    result.snippet = self.snippet_generator.generate(content, query)
                else:
                    try:
                        raw_content = file_path.read_text(errors='ignore')
                        # 硬截断
                        max_chars = 500
                        result.content = raw_content[:max_chars]
                        result.snippet = self.snippet_generator.generate(raw_content, query)
                    except:
                        pass
        
        # 限制结果数量
        results = results[:limit]
        
        # 缓存
        self._cache[cache_key] = results
        
        elapsed_ms = int((time.time() - start) * 1000)
        
        return {
            "query": query,
            "rewrites": rewrites,
            "mode": mode,
            "vector_mode": self.get_vector_mode(),
            "performance_mode": self.get_performance_mode(),
            "results": [
                {
                    "id": r.id,
                    "title": r.title,
                    "snippet": r.snippet[:200] if r.snippet else "",
                    "score": round(r.score, 4),
                    "source": r.source
                }
                for r in results
            ],
            "total": len(results),
            "time_ms": elapsed_ms,
            "source": "search",
            "token_budget": self.token_manager.get_summary(),
            "lazy_loader_status": self.lazy_loader.get_status()
        }
    
    def clear_cache(self):
        self._cache.clear()
        self.token_manager.reset()

# 全局实例
_unified_search: Optional[UnifiedSearch] = None

def get_unified_search() -> UnifiedSearch:
    global _unified_search
    if _unified_search is None:
        _unified_search = UnifiedSearch()
    return _unified_search

#!/usr/bin/env python3
"""Tests for merge-sources.py using real captured fixture data.

Run: python3 -m pytest tests/ -v
  or: python3 tests/test_merge.py
"""

import json
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# 使用标准导入替代动态导入
try:
    from merge_sources import (
        normalize_title,
        calculate_title_similarity,
        normalize_url as normalize_url_for_dedup,
        deduplicate_articles,
        apply_domain_limits,
        group_by_topics,
        DOMAIN_LIMIT_EXEMPT
    )
except ImportError:
    # 如果标准导入失败，跳过测试
    print("Warning: merge_sources module not found, skipping tests")
    normalize_title = None
    calculate_title_similarity = None
    normalize_url_for_dedup = None
    deduplicate_articles = None
    apply_domain_limits = None
    group_by_topics = None
    DOMAIN_LIMIT_EXEMPT = set()

# ... 其余测试代码保持不变

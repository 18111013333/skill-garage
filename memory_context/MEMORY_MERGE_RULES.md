# MEMORY_MERGE_RULES.md - 记忆合并规则

## 目的
定义相近记忆的合并规则，确保合并不丢失上下文。

## 适用范围
所有需要合并的相似记忆条目。

## 合并场景

| 场景 | 说明 | 合并策略 |
|------|------|----------|
| 完全重复 | 内容完全相同 | 直接合并 |
| 部分重叠 | 内容有重叠 | 合并保留完整 |
| 互补信息 | 信息互补 | 合并整合 |
| 版本更新 | 新旧版本 | 保留最新 |
| 来源不同 | 同一信息多来源 | 合并来源记录 |

## 合并决策

### 合并条件
```yaml
merge_conditions:
  must_satisfy:
    - same_entity_reference: true  # 指向同一实体
    - content_similarity: "> 0.8"  # 内容相似度高
    - no_critical_conflict: true   # 无关键冲突
    
  should_consider:
    - same_time_context: true      # 时间上下文相近
    - same_project_scope: true     # 项目作用域相同
    - compatible_types: true       # 类型兼容
```

### 不合并条件
```yaml
no_merge_conditions:
  - different_entity_reference: true
  - content_contradicts: true
  - different_time_context: true  # 不同时间点的记录
  - user_marked_separate: true
```

## 合并策略

### 1. 直接合并
```yaml
direct_merge:
  condition: "content_identical"
  
  process:
    - select_primary:
        criteria:
          - higher_confidence
          - earlier_created
          - more_complete_source
          
    - merge_metadata:
        - combine_sources
        - update_access_count
        - keep_earliest_created
        - update_last_accessed
        
    - archive_secondary:
        - mark_as_merged
        - link_to_primary
        - retain_for_audit
```

### 2. 内容整合合并
```yaml
content_integration_merge:
  condition: "content_overlaps_but_not_identical"
  
  process:
    - identify_unique_parts:
        - extract_from_each
        - identify_overlaps
        
    - create_merged_content:
        - combine_unique_parts
        - resolve_overlaps
        - maintain_coherence
        
    - preserve_history:
        - record_original_contents
        - track_merge_sources
```

### 3. 互补信息合并
```yaml
complementary_merge:
  condition: "information_complementary"
  
  process:
    - identify_complementary_parts:
        - part_a_unique
        - part_b_unique
        - common_parts
        
    - merge_structure:
        - combine_all_unique
        - preserve_common
        - organize_logically
        
    - validate_completeness:
        - check_no_information_loss
        - verify_consistency
```

### 4. 版本更新合并
```yaml
version_update_merge:
  condition: "newer_version_exists"
  
  process:
    - identify_versions:
        - sort_by_time
        - identify_latest
        
    - merge_with_history:
        - keep_latest_content
        - preserve_version_history
        - record_change_reasons
        
    - update_metadata:
        - increment_version
        - record_update_source
```

### 5. 多来源合并
```yaml
multi_source_merge:
  condition: "same_info_different_sources"
  
  process:
    - verify_consistency:
        - compare_content
        - identify_discrepancies
        
    - merge_sources:
        - combine_source_list
        - calculate_aggregate_confidence
        - preserve_source_details
        
    - handle_discrepancies:
        - if_minor: "note_discrepancy"
        - if_major: "flag_for_review"
```

## 合并保留规则

### 必须保留
```yaml
must_preserve:
  - all_sources:
      description: "所有来源信息"
      storage: "source_history"
      
  - timestamps:
      description: "创建和更新时间"
      storage: "created_at, updated_at"
      
  - confidence_history:
      description: "置信度历史"
      storage: "confidence_log"
      
  - conflict_history:
      description: "冲突记录"
      storage: "conflict_records"
```

### 可选保留
```yaml
optional_preserve:
  - original_content:
      description: "原始内容"
      storage: "content_archive"
      retention: "90d"
      
  - access_history:
      description: "访问历史"
      storage: "access_log"
      retention: "30d"
```

## 合并后处理

### 元数据更新
```yaml
metadata_update:
  - merge_date: "current_timestamp"
  - merge_type: "merge_strategy_used"
  - merged_from: ["memory_id_1", "memory_id_2"]
  - confidence: "recalculated"
  - quality_score: "recalculated"
```

### 索引更新
```yaml
index_update:
  - update_vector_index:
      action: "reindex_merged_memory"
      
  - update_search_index:
      action: "remove_secondary_add_primary"
      
  - update_relation_index:
      action: "redirect_relations_to_primary"
```

## 合并示例

### 示例1：完全重复合并
```yaml
before_merge:
  memory_1:
    id: "MEM-001"
    content: "用户偏好深色主题"
    source: "user_input"
    confidence: 0.9
    created_at: "2024-01-01"
    
  memory_2:
    id: "MEM-002"
    content: "用户偏好深色主题"
    source: "behavior_inference"
    confidence: 0.7
    created_at: "2024-01-15"

after_merge:
  primary:
    id: "MEM-001"
    content: "用户偏好深色主题"
    sources:
      - source: "user_input"
        confidence: 0.9
        at: "2024-01-01"
      - source: "behavior_inference"
        confidence: 0.7
        at: "2024-01-15"
    confidence: 0.95  # 多来源提升
    created_at: "2024-01-01"
    merged_from: ["MEM-002"]
    
  archived:
    id: "MEM-002"
    status: "merged"
    merged_into: "MEM-001"
```

### 示例2：互补信息合并
```yaml
before_merge:
  memory_1:
    content: "项目使用React框架"
    scope: "project_A"
    
  memory_2:
    content: "项目使用TypeScript"
    scope: "project_A"

after_merge:
  content: "项目使用React框架和TypeScript"
  scope: "project_A"
  merged_from: ["MEM-001", "MEM-002"]
  merge_type: "complementary"
```

## 冲突处理

### 冲突检测
```yaml
conflict_detection:
  during_merge:
    - compare_key_attributes
    - check_temporal_consistency
    - verify_logical_compatibility
    
  conflict_types:
    - value_conflict: "属性值不同"
    - temporal_conflict: "时间矛盾"
    - logical_conflict: "逻辑不一致"
```

### 冲突解决
```yaml
conflict_resolution:
  value_conflict:
    - prefer_higher_confidence
    - prefer_more_recent
    - prefer_user_confirmed
    
  temporal_conflict:
    - keep_both_with_time_markers
    - create_versioned_memory
    
  logical_conflict:
    - flag_for_manual_review
    - do_not_merge
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 合并准确率 | 正确合并/总合并 | <95% |
| 信息丢失率 | 合并后信息丢失 | >0 |
| 合并频率 | 合并次数/天 | 异常波动 |
| 冲突合并率 | 有冲突仍合并 | >5% |

## 维护方式
- 新增策略: 创建合并策略
- 调整条件: 更新合并条件
- 新增保留规则: 更新保留规则

## 引用文件
- `memory_quality/MEMORY_SCORING.md` - 记忆评分
- `memory_quality/MEMORY_AUDIT.md` - 记忆审计
- `graph/ENTITY_RESOLUTION.md` - 实体消歧

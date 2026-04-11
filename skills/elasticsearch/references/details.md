- Cardinality is approximate (HyperLogLog)—exact count requires scanning all docs
- Nested aggs require `nested` wrapper—matches nested query pattern

## Common Errors

- "cluster_block_exception"—disk > 85%, cluster goes read-only; clear disk, reset with `_cluster/settings`
- "version conflict"—concurrent update; retry with `retry_on_conflict` or use optimistic locking
- "circuit_breaker_exception"—query uses too much memory; reduce aggregation scope
- Mapping explosion from dynamic fields—set `index.mapping.total_fields.limit` and use strict mapping

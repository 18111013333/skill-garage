- Statement-based replication can break with non-deterministic functions—UUID(), NOW()
- Row-based replication safer but more bandwidth—default in MySQL 8
- Read replicas have lag—check `Seconds_Behind_Master` before relying on replica reads
- Don't write to replica—usually read-only but verify

## Performance

- `EXPLAIN ANALYZE` only in MySQL 8.0.18+—older versions just EXPLAIN without actual times
- Query cache removed in MySQL 8—don't rely on it; cache at application level
- `OPTIMIZE TABLE` for fragmented tables—locks table; use pt-online-schema-change for big tables
- `innodb_buffer_pool_size`—set to 70-80% of RAM for dedicated DB server

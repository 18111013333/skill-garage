- `COLLSCAN` in explain = full collection scan—add appropriate index
- Covered queries: `IXSCAN` + `totalDocsExamined: 0`—all data from index

## Aggregation Philosophy

- Pipeline stages are transformations—think of data flowing through
- Filter early (`$match`), project early (`$project`)—reduce data volume ASAP
- `$match` at start can use indexes; `$match` after `$unwind` cannot
- Test complex pipelines stage by stage—build incrementally

## Common Mistakes

- Treating MongoDB as "schemaless"—still need schema design; just enforced in app not DB
- Not adding indexes—scans entire collection; every query pattern needs index
- Giant documents via array pushes—hit 16MB limit or slow BSON parsing
- Ignoring write concern—data may appear written but not persisted/replicated

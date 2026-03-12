---
title: FUSE_VIRTUAL_COLUMN
---

Returns the virtual column information of the latest or specified snapshot of a table. For details, see [Virtual Column](/guides/performance/virtual-column).

## Syntax

```sql
FUSE_VIRTUAL_COLUMN('<database_name>', '<table_name>'[, '<snapshot_id>'])
```

## Examples

```sql
CREATE TABLE test(id int, val variant);

INSERT INTO
  test
VALUES
  (
    1,
    '{"id":1,"name":"databend"}'
  ),
  (
    2,
    '{"id":2,"name":"databricks"}'
  );

SELECT * FROM FUSE_VIRTUAL_COLUMN('default', 'test');

╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   snapshot_id  │    timestamp   │ virtual_block_ │ virtual_block_ │ row_count │ column_name │ column_type │  column_id │ block_offset │ bytes_compress │
│     String     │    Timestamp   │    location    │      size      │   UInt64  │    String   │    String   │   UInt32   │    UInt64    │       ed       │
│                │                │     String     │     UInt64     │           │             │             │            │              │     UInt64     │
├────────────────┼────────────────┼────────────────┼────────────────┼───────────┼─────────────┼─────────────┼────────────┼──────────────┼────────────────┤
│ 0196c3aa7cc97f │ 2025-05-12 08: │ 1/385366/_vb/h │            632 │         2 │ val['id']   │ UInt64 NULL │ 3000000000 │            4 │             48 │
│ e69995765add1b │ 44:12.361000   │ 0196c8d0d8c976 │                │           │             │             │            │              │                │
│ a3bd           │                │ d19de8bfdd32a7 │                │           │             │             │            │              │                │
│                │                │ 0a01_v2.parque │                │           │             │             │            │              │                │
│                │                │ t              │                │           │             │             │            │              │                │
│ 0196c3aa7cc97f │ 2025-05-12 08: │ 1/385366/_vb/h │            632 │         2 │ val['name'] │ String NULL │ 3000000001 │           52 │             58 │
│ e69995765add1b │ 44:12.361000   │ 0196c8d0d8c976 │                │           │             │             │            │              │                │
│ a3bd           │                │ d19de8bfdd32a7 │                │           │             │             │            │              │                │
│                │                │ 0a01_v2.parque │                │           │             │             │            │              │                │
│                │                │ t              │                │           │             │             │            │              │                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

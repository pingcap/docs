---
title: REFRESH SPATIAL INDEX
summary: 刷新空间索引以回填历史行，或在数据变更后修改索引。
---

# REFRESH SPATIAL INDEX

{{{ .lake }}} 会在 `SYNC` 模式下每次写入新数据时自动刷新空间索引。`REFRESH SPATIAL INDEX` 主要用于回填在声明索引之前已存在的行。

## 语法 {#syntax}

```sql
REFRESH SPATIAL INDEX <index> ON [<database>.]<table> [LIMIT <limit>]
```

| 参数 | 描述 |
|-----------|-------------|
| `<limit>` | 指定刷新索引期间要处理的最大行数。如果未指定，则会处理表中的所有行。 |

## 示例 {#examples}

```sql
-- Existing table with data loaded before the index was declared
CREATE TABLE IF NOT EXISTS stores (
  store_id INT,
  location GEOMETRY
) ENGINE = FUSE;

INSERT INTO stores VALUES
  (1, TO_GEOMETRY('POINT(10 10)')),
  (2, TO_GEOMETRY('POINT(20 20)'));

-- Create the spatial index afterward
CREATE SPATIAL INDEX stores_location_idx ON stores(location);

-- Backfill historical rows so the index covers earlier inserts
REFRESH SPATIAL INDEX stores_location_idx ON stores;

-- Future inserts refresh automatically in SYNC mode
```
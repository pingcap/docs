---
title: REFRESH AGGREGATING INDEX
summary: "{{{ .lake }}} 会在新数据摄取时自动以 `SYNC` 模式维护聚合索引。当你在一个已包含数据的表上新增索引时，运行 REFRESH AGGREGATING INDEX 以回填更早的行。"
---

# REFRESH AGGREGATING INDEX

{{{ .lake }}} 会在新数据摄取时自动以 `SYNC` 模式维护聚合索引。当你在一个已包含数据的表上新增索引时，运行 `REFRESH AGGREGATING INDEX` 以回填更早的行。

## 语法 {#syntax}

```sql
REFRESH AGGREGATING INDEX <index_name>
```

## 示例 {#examples}

本示例会在一个已包含数据的表上创建聚合索引，然后运行一次 `REFRESH` 来回填这些行：

```sql
-- Prepare a table and load data before the index exists
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4);

-- Declare the aggregating index (existing rows are not indexed yet)
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;

-- Backfill previously inserted rows
REFRESH AGGREGATING INDEX my_agg_index;

-- Insert new data after the index exists (no manual refresh needed)
INSERT INTO agg VALUES (2,2,5);
-- SYNC mode keeps the index current automatically
```
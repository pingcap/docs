---
title: REFRESH AGGREGATING INDEX
summary: "{{{ .lake }}} は、新しいデータが取り込みされると、`SYNC` モードの集計インデックスを自動的に管理します。すでにデータが含まれているテーブルにインデックスを導入する場合は、以前の行をバックフィルするために REFRESH AGGREGATING INDEX を実行します。"
---

# REFRESH AGGREGATING INDEX

{{{ .lake }}} は、新しいデータが取り込みされると、`SYNC` モードの集計インデックスを自動的に管理します。すでにデータが含まれているテーブルにインデックスを導入する場合は、以前の行をバックフィルするために `REFRESH AGGREGATING INDEX` を実行します。

## 構文 {#syntax}

```sql
REFRESH AGGREGATING INDEX <index_name>
```

## 例 {#examples}

この例では、すでにデータが含まれているテーブルに集計インデックスを作成し、その後 `REFRESH` を 1 回実行してそれらの行をバックフィルします。

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
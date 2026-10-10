---
title: REFRESH SPATIAL INDEX
summary: 空間インデックスを更新し、過去の行をバックフィルするか、データ変更後にインデックスを更新します。
---

# REFRESH SPATIAL INDEX

{{{ .lake }}} は、新しいデータが書き込まれるたびに、`SYNC` モードの空間インデックスを自動的に更新します。`REFRESH SPATIAL INDEX` は主に、インデックスが宣言される前から存在していた行をバックフィルするために使用します。

## 構文 {#syntax}

```sql
REFRESH SPATIAL INDEX <index> ON [<database>.]<table> [LIMIT <limit>]
```

| パラメータ | 説明 |
|-----------|-------------|
| `<limit>` | インデックス更新中に処理する行の最大数を指定します。指定しない場合、テーブル内のすべての行が処理されます。 |

## 例 {#examples}

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
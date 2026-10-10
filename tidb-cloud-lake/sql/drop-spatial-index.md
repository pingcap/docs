---
title: DROP SPATIAL INDEX
summary: "{{{ .lake }}} の空間インデックスを削除します。"
---

# DROP SPATIAL INDEX

{{{ .lake }}} の空間インデックスを削除します。

## 構文 {#syntax}

```sql
DROP SPATIAL INDEX [IF EXISTS] <index> ON [<database>.]<table>
```

## 例 {#examples}

```sql
CREATE TABLE stores (
    store_id INT,
    store_name STRING,
    location GEOMETRY,
    SPATIAL INDEX location_idx (location)
) ENGINE = FUSE;

DROP SPATIAL INDEX location_idx ON stores;
```
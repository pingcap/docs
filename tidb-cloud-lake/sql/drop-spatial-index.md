---
title: DROP SPATIAL INDEX
summary: "删除 {{{ .lake }}} 中的空间索引。"
---

# DROP SPATIAL INDEX

删除 {{{ .lake }}} 中的空间索引。

## 语法 {#syntax}

```sql
DROP SPATIAL INDEX [IF EXISTS] <index> ON [<database>.]<table>
```

## 示例 {#examples}

```sql
CREATE TABLE stores (
    store_id INT,
    store_name STRING,
    location GEOMETRY,
    SPATIAL INDEX location_idx (location)
) ENGINE = FUSE;

DROP SPATIAL INDEX location_idx ON stores;
```
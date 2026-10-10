---
title: ST_ISVALID
summary: OGC 仕様で定義されているとおり、GEOMETRY オブジェクトが幾何学的に有効な場合に TRUE を返します。
---

# ST_ISVALID

OGC 仕様で定義されているとおり、GEOMETRY オブジェクトが幾何学的に有効な場合に TRUE を返します。

## 構文 {#syntax}

```sql
ST_ISVALID(<geometry>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|--------------|------------------------------------------------------|
| `<geometry>` | GEOMETRY 式。 |

## 戻り値の型 {#return-type}

Boolean。

## 例 {#examples}

```sql
SELECT ST_ISVALID(TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'));

┌──────────────────────────────────────────────────────────┐
│ st_isvalid(to_geometry('polygon((0 0, 1 0, 1 1, 0 1, 0 0))')) │
├──────────────────────────────────────────────────────────┤
│ true                                                          │
└──────────────────────────────────────────────────────────┘

-- Self-intersecting polygon (bowtie shape) is invalid
SELECT ST_ISVALID(TO_GEOMETRY('POLYGON((0 0, 2 2, 2 0, 0 2, 0 0))'));

┌──────────────────────────────────────────────────────────────┐
│ st_isvalid(to_geometry('polygon((0 0, 2 2, 2 0, 0 2, 0 0))')) │
├──────────────────────────────────────────────────────────────┤
│ false                                                             │
└──────────────────────────────────────────────────────────────┘
```
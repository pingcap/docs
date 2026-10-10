---
title: ST_POINTN
summary: LineString 内の指定したインデックスにある Point を返します。
---

# ST_POINTN

LineString 内の指定したインデックスにある Point を返します。

## 構文 {#syntax}

```sql
ST_POINTN(<geometry_or_geography>, <index>)
```

## 引数 {#arguments}

| 引数    | 説明                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `<geometry_or_geography>` | 引数は、LineString を表す GEOMETRY または GEOGRAPHY 型の式である必要があります。 |
| `<index>`    | 返す Point のインデックスです。                                                 |

> **Note:**
>
> インデックスは 1 始まりで、負のインデックスは LineString の末尾からのオフセットとして使用されます。index が範囲外の場合、この関数はエラーを返します。

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_POINTN(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    ),
    1
  ) AS pipeline_pointn;

┌─────────────────┐
│ pipeline_pointn │
├─────────────────┤
│ POINT(1 1)      │
└─────────────────┘

SELECT
  ST_POINTN(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    ),
    -2
  ) AS pipeline_pointn;

┌─────────────────┐
│ pipeline_pointn │
├─────────────────┤
│ POINT(3 3)      │
└─────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_POINTN(
    ST_GEOGFROMWKT(
      'LINESTRING(1 1, 2 2, 3 3, 4 4)'
    ),
    2
  ) AS pipeline_pointn;

┌─────────────────┐
│ pipeline_pointn │
├─────────────────┤
│ POINT(2 2)      │
└─────────────────┘
```
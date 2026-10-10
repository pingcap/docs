---
title: ST_MAKEPOLYGON
summary: 穴のない Polygon を表す GEOMETRY または GEOGRAPHY オブジェクトを構築します。この関数は、指定された LineString を外側のループとして使用します。
---

# ST_MAKEPOLYGON

穴のない Polygon を表す GEOMETRY または GEOGRAPHY オブジェクトを構築します。この関数は、指定された LineString を外側のループとして使用します。

## 構文 {#syntax}

```sql
ST_MAKEPOLYGON(<geometry_or_geography>)
```

## エイリアス {#aliases}

- [ST_POLYGON](/tidb-cloud-lake/sql/st-polygon.md)

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は、GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_MAKEPOLYGON(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)'
    )
  ) AS pipeline_polygon;

┌────────────────────────────────┐
│        pipeline_polygon        │
├────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0)) │
└────────────────────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_MAKEPOLYGON(
    ST_GEOGFROMWKT(
      'LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)'
    )
  ) AS pipeline_polygon;

╭────────────────────────────────╮
│        pipeline_polygon        │
├────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0)) │
╰────────────────────────────────╯
```
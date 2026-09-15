---
title: ST_NPOINTS
summary: 返回 GEOMETRY 或 GEOGRAPHY 对象中的点数。
---

# ST_NPOINTS

返回 GEOMETRY 或 GEOGRAPHY 对象中的点数。

## 语法 {#syntax}

```sql
ST_NPOINTS(<geometry_or_geography>)
```

## 别名 {#aliases}

- [ST_NUMPOINTS](/tidb-cloud-lake/sql/st-numpoints.md)

## 参数 {#arguments}

| 参数    | 描述                                                 |
|--------------|-------------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 对象类型的表达式。 |

## 返回类型 {#return-type}

UInt8。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT ST_NPOINTS(TO_GEOMETRY('POINT(66 12)')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       1 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('MULTIPOINT((45 21),(12 54))')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       2 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('LINESTRING(40 60,50 50,60 40)')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       3 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('MULTILINESTRING((1 1,32 17),(33 12,73 49,87.1 6.1))')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       5 │
└─────────┘

SELECT ST_NPOINTS(TO_GEOMETRY('GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60,50 50,60 40),POINT(99 11))')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       8 │
└─────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT ST_NPOINTS(ST_GEOGFROMWKT('LINESTRING(40 60,50 50,60 40)')) AS npoints

┌─────────┐
│ npoints │
├─────────┤
│       3 │
└─────────┘
```
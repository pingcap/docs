---
title: ST_SETSRID
summary: 返回一个将其 SRID（空间参考系统标识符）设置为指定值的 GEOMETRY 对象。此函数只会更改 SRID，而不会影响对象的坐标。如果你还需要更改坐标以匹配新的 SRS（空间参考系统），请改用 ST_TRANSFORM。
---

# ST_SETSRID

返回一个将其 [SRID（空间参考系统标识符）](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) 设置为指定值的 GEOMETRY 对象。此函数只会更改 SRID，而不会影响对象的坐标。如果你还需要更改坐标以匹配新的 SRS（空间参考系统），请改用 [ST_TRANSFORM](/tidb-cloud-lake/sql/st-transform.md)。

## 语法 {#syntax}

```sql
ST_SETSRID(<geometry>, <srid>)
```

## 参数 {#arguments}

| 参数         | 描述                                                |
|--------------|-----------------------------------------------------|
| `<geometry>` | 该参数必须是 GEOMETRY 对象类型的表达式。            |
| `<srid>`     | 在返回的 GEOMETRY 对象中要设置的 SRID 整数型值。    |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SET GEOMETRY_OUTPUT_FORMAT = 'EWKT'

SELECT ST_SETSRID(TO_GEOMETRY('POINT(13 51)'), 4326) AS geometry

┌────────────────────────┐
│        geometry        │
├────────────────────────┤
│ SRID=4326;POINT(13 51) │
└────────────────────────┘

```
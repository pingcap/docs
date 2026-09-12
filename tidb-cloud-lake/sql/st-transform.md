---
title: ST_TRANSFORM
summary: 将 GEOMETRY 对象从一个空间参考系统 (SRS) 转换到另一个空间参考系统。如果你只需要更改 SRID 而不更改坐标（例如 SRID 不正确），请改用 ST_SETSRID。
---

# ST_TRANSFORM

将 GEOMETRY 对象从一个[空间参考系统 (SRS)](https://en.wikipedia.org/wiki/Spatial_reference_system)转换到另一个。如果你只需要更改 SRID 而不更改坐标（例如 SRID 不正确），请改用 [ST_SETSRID](/tidb-cloud-lake/sql/st-setsrid.md)。

## 语法 {#syntax}

```sql
ST_TRANSFORM(<geometry> [, <from_srid>], <to_srid>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<geometry>`  | 该参数必须是 GEOMETRY 对象类型的表达式。                                                                                               |
| `<from_srid>` | 可选的 SRID，用于标识输入 GEOMETRY 对象当前的 SRS。如果省略此参数，则使用输入 GEOMETRY 对象中指定的 SRID。 |
| `<to_srid>`   | 用于标识目标 SRS 的 SRID。该函数会将输入 GEOMETRY 对象转换为使用此 SRS 的新对象。                                         |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SET GEOMETRY_OUTPUT_FORMAT = 'EWKT'

SELECT ST_TRANSFORM(ST_GEOMFROMWKT('POINT(389866.35 5819003.03)', 32633), 3857) AS transformed_geom

┌───────────────────────────────────────────────┐
│                transformed_geom               │
├───────────────────────────────────────────────┤
│ SRID=3857;POINT(1489140.093766 6892872.19868) │
└───────────────────────────────────────────────┘

SELECT ST_TRANSFORM(ST_GEOMFROMWKT('POINT(4.500212 52.161170)'), 4326, 28992) AS transformed_geom

┌──────────────────────────────────────────────┐
│               transformed_geom               │
├──────────────────────────────────────────────┤
│ SRID=28992;POINT(94308.670475 464038.168827) │
└──────────────────────────────────────────────┘

```
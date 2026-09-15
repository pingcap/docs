---
title: ST_MAKEGEOMPOINT
summary: 构造一个 GEOMETRY 对象，该对象表示具有指定经度和纬度的 Point。
---

# ST_MAKEGEOMPOINT

构造一个 GEOMETRY 对象，该对象表示具有指定经度和纬度的 Point。

## 语法 {#syntax}

```sql
ST_MAKEGEOMPOINT(<longitude>, <latitude>)
```

## 别名 {#aliases}

- [ST_GEOM_POINT](/tidb-cloud-lake/sql/st-geom-point.md)

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|-----------------------------------------------|
| `<longitude>` | 表示经度的 Double 值。 |
| `<latitude>`  | 表示纬度的 Double 值。 |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SELECT
  ST_MAKEGEOMPOINT(
    7.0, 8.0
  ) AS pipeline_point;

┌────────────────┐
│ pipeline_point │
├────────────────┤
│ POINT(7 8)     │
└────────────────┘

SELECT
  ST_MAKEGEOMPOINT(
    -122.3061, 37.554162
  ) AS pipeline_point;

┌────────────────────────────┐
│       pipeline_point       │
├────────────────────────────┤
│ POINT(-122.3061 37.554162) │
└────────────────────────────┘
```
---
title: ST_MAKEPOINT
summary: 构造一个 GEOGRAPHY 对象，该对象表示具有指定经度和纬度的 Point。
---

# ST_MAKEPOINT

构造一个 GEOGRAPHY 对象，该对象表示具有指定经度和纬度的 Point。

## 语法 {#syntax}

```sql
ST_MAKEPOINT(<longitude>, <latitude>)
```

## 别名 {#aliases}

- [ST_POINT](/tidb-cloud-lake/sql/st-point.md)

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|-----------------------------------------------|
| `<longitude>` | 表示经度的 Double 值。 |
| `<latitude>`  | 表示纬度的 Double 值。 |

## 返回类型 {#return-type}

Geography。

## 示例 {#examples}

```sql
SELECT
  ST_ASWKT(
    ST_MAKEPOINT(
      7.0, 8.0
    )
  ) AS pipeline_point;

┌────────────────┐
│ pipeline_point │
├────────────────┤
│ POINT(7 8)     │
└────────────────┘

SELECT
  ST_ASWKT(
    ST_MAKEPOINT(
      -122.3061, 37.554162
    )
  ) AS pipeline_point;

╭────────────────────────────╮
│       pipeline_point       │
├────────────────────────────┤
│ POINT(-122.3061 37.554162) │
╰────────────────────────────╯
```
---
title: ST_MAKELINE
summary: 构造一个 GEOMETRY 或 GEOGRAPHY 对象，用于表示连接输入的两个 GEOMETRY 或 GEOGRAPHY 对象中各点的线。
---

# ST_MAKELINE

构造一个 GEOMETRY 或 GEOGRAPHY 对象，用于表示连接输入的两个 GEOMETRY 或 GEOGRAPHY 对象中各点的线。

## 语法 {#syntax}

```sql
ST_MAKELINE(<geometry_or_geography1>, <geometry_or_geography2>)
```

## 别名 {#aliases}

- [ST_MAKE_LINE](/tidb-cloud-lake/sql/st-make-line.md)

## 参数 {#arguments}

| 参数     | 描述                                                                                                 |
|---------------|-------------------------------------------------------------------------------------------------------------|
| `<geometry_or_geography1>` | 一个包含待连接点的 GEOMETRY 或 GEOGRAPHY 对象。该对象必须是 Point、MultiPoint 或 LineString。 |
| `<geometry_or_geography2>` | 一个包含待连接点的 GEOMETRY 或 GEOGRAPHY 对象。该对象必须是 Point、MultiPoint 或 LineString。 |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_MAKELINE(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    ),
    ST_GEOMETRYFROMWKT(
      'POINT(-104.874173 56.714538)'
    )
  ) AS pipeline_line;

┌───────────────────────────────────────────────────────┐
│                     pipeline_line                     │
├───────────────────────────────────────────────────────┤
│ LINESTRING(-122.3061 37.554162,-104.874173 56.714538) │
└───────────────────────────────────────────────────────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_MAKELINE(
    ST_GEOGFROMWKT(
      'POINT(-122.306100 37.554162)'
    ),
    ST_GEOGFROMWKT(
      'POINT(-104.874173 56.714538)'
    )
  ) AS pipeline_line;

╭───────────────────────────────────────────────────────╮
│                     pipeline_line                     │
├───────────────────────────────────────────────────────┤
│ LINESTRING(-122.3061 37.554162,-104.874173 56.714538) │
╰───────────────────────────────────────────────────────╯
```
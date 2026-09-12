---
title: TO_GEOMETRY
summary: 解析输入并返回 GEOMETRY 类型的值。
---

# TO_GEOMETRY

解析输入并返回 GEOMETRY 类型的值。

如果在解析过程中发生错误，`TRY_TO_GEOMETRY` 会返回 `NULL` 值。

## 语法 {#syntax}

```sql
TO_GEOMETRY(<string>, [<srid>])
TO_GEOMETRY(<binary>, [<srid>])
TO_GEOMETRY(<variant>, [<srid>])
TRY_TO_GEOMETRY(<string>, [<srid>])
TRY_TO_GEOMETRY(<binary>, [<srid>])
TRY_TO_GEOMETRY(<variant>, [<srid>])
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-----------------------------------------------------------------------------------------------------------|
| `<string>`  | 该参数必须是字符串表达式，格式可以是十六进制格式的 WKT、EWKT、WKB 或 EWKB，或 GeoJSON 格式。 |
| `<binary>`  | 该参数必须是 WKB 或 EWKB 格式的二进制表达式。 |
| `<variant>` | 该参数必须是 GeoJSON 格式的 JSON OBJECT。 |
| `<srid>`    | 要使用的 SRID 的整数值。 |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SELECT
  TO_GEOMETRY(
    'POINT(1820.12 890.56)'
  ) AS pipeline_geometry;

┌───────────────────────┐
│   pipeline_geometry   │
├───────────────────────┤
│ POINT(1820.12 890.56) │
└───────────────────────┘

SELECT
  TO_GEOMETRY(
    '0101000020797f000066666666a9cb17411f85ebc19e325641', 4326
  ) AS pipeline_geometry;

┌───────────────────────────────────────┐
│           pipeline_geometry           │
├───────────────────────────────────────┤
│ SRID=4326;POINT(389866.35 5819003.03) │
└───────────────────────────────────────┘

SELECT
  TO_GEOMETRY(
    FROM_HEX('0101000020797f000066666666a9cb17411f85ebc19e325641'), 4326
  ) AS pipeline_geometry;

┌───────────────────────────────────────┐
│           pipeline_geometry           │
├───────────────────────────────────────┤
│ SRID=4326;POINT(389866.35 5819003.03) │
└───────────────────────────────────────┘

SELECT
  TO_GEOMETRY(
    '{"coordinates":[[389866,5819003],[390000,5830000]],"type":"LineString"}'
  ) AS pipeline_geometry;

┌───────────────────────────────────────────┐
│             pipeline_geometry             │
├───────────────────────────────────────────┤
│ LINESTRING(389866 5819003,390000 5830000) │
└───────────────────────────────────────────┘

SELECT
  TO_GEOMETRY(
    PARSE_JSON('{"coordinates":[[389866,5819003],[390000,5830000]],"type":"LineString"}')
  ) AS pipeline_geometry;

┌───────────────────────────────────────────┐
│             pipeline_geometry             │
├───────────────────────────────────────────┤
│ LINESTRING(389866 5819003,390000 5830000) │
└───────────────────────────────────────────┘
```
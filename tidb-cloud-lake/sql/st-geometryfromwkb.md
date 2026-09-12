---
title: ST_GEOMETRYFROMWKB
summary: 解析 WKB(well-known-binary) 或 EWKB(extended well-known-binary) 输入，并返回 GEOMETRY 类型的值。
---

# ST_GEOMETRYFROMWKB

解析 [WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) 或 [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) 输入，并返回 GEOMETRY 类型的值。

## 语法 {#syntax}

```sql
ST_GEOMETRYFROMWKB(<string>, [<srid>])
ST_GEOMETRYFROMWKB(<binary>, [<srid>])
```

## 别名 {#aliases}

- [ST_GEOMFROMWKB](/tidb-cloud-lake/sql/st-geomfromwkb.md)
- [ST_GEOMETRYFROMEWKB](/tidb-cloud-lake/sql/st-geometryfromewkb.md)
- [ST_GEOMFROMEWKB](/tidb-cloud-lake/sql/st-geomfromewkb.md)

## 参数 {#arguments}

| 参数        | 描述                                                                           |
|-------------|--------------------------------------------------------------------------------|
| `<string>`  | 该参数必须是十六进制格式的 WKB 或 EWKB 字符串表达式。                          |
| `<binary>`  | 该参数必须是 WKB 或 EWKB 格式的二进制表达式。                                  |
| `<srid>`    | 要使用的 SRID 的整数值。                                                       |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SELECT
  ST_GEOMETRYFROMWKB(
    '0101000020797f000066666666a9cb17411f85ebc19e325641'
  ) AS pipeline_geometry;

┌────────────────────────────────────────┐
│            pipeline_geometry           │
├────────────────────────────────────────┤
│ SRID=32633;POINT(389866.35 5819003.03) │
└────────────────────────────────────────┘

SELECT
  ST_GEOMETRYFROMWKB(
    FROM_HEX('0101000020797f000066666666a9cb17411f85ebc19e325641'), 4326
  ) AS pipeline_geometry;

┌───────────────────────────────────────┐
│           pipeline_geometry           │
├───────────────────────────────────────┤
│ SRID=4326;POINT(389866.35 5819003.03) │
└───────────────────────────────────────┘
```
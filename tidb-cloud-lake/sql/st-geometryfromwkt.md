---
title: ST_GEOMETRYFROMWKT
summary: 解析 WKT(well-known-text) 或 EWKT(extended well-known-text) 输入，并返回 GEOMETRY 类型的值。
---

# ST_GEOMETRYFROMWKT

解析 [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) 或 [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) 输入，并返回 GEOMETRY 类型的值。

## 语法 {#syntax}

```sql
ST_GEOMETRYFROMWKT(<string>, [<srid>])
```

## 别名 {#aliases}

- [ST_GEOMFROMWKT](/tidb-cloud-lake/sql/st-geomfromwkt.md)
- [ST_GEOMETRYFROMEWKT](/tidb-cloud-lake/sql/st-geometryfromewkt.md)
- [ST_GEOMFROMEWKT](/tidb-cloud-lake/sql/st-geomfromewkt.md)
- [ST_GEOMFROMTEXT](/tidb-cloud-lake/sql/st-geomfromtext.md)
- [ST_GEOMETRYFROMTEXT](/tidb-cloud-lake/sql/st-geometryfromtext.md)

## 参数 {#arguments}

| 参数        | 描述                                                        |
|-------------|-------------------------------------------------------------|
| `<string>`  | 该参数必须是 WKT 或 EWKT 格式的字符串表达式。               |
| `<srid>`    | 要使用的 SRID 的整数型值。                                  |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SELECT
  ST_GEOMETRYFROMWKT(
    'POINT(1820.12 890.56)'
  ) AS pipeline_geometry;

┌───────────────────────┐
│   pipeline_geometry   │
├───────────────────────┤
│ POINT(1820.12 890.56) │
└───────────────────────┘

SELECT
  ST_GEOMETRYFROMWKT(
    'POINT(1820.12 890.56)', 4326
  ) AS pipeline_geometry;

┌─────────────────────────────────┐
│        pipeline_geometry        │
│             Geometry            │
├─────────────────────────────────┤
│ SRID=4326;POINT(1820.12 890.56) │
└─────────────────────────────────┘
```
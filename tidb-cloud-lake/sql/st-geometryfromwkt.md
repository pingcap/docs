---
title: ST_GEOMETRYFROMWKT
summary: WKT(well-known-text) または EWKT(extended well-known-text) の入力を解析し、GEOMETRY 型の値を返します。
---

# ST_GEOMETRYFROMWKT

[WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) または [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) の入力を解析し、GEOMETRY 型の値を返します。

## 構文 {#syntax}

```sql
ST_GEOMETRYFROMWKT(<string>, [<srid>])
```

## エイリアス {#aliases}

- [ST_GEOMFROMWKT](/tidb-cloud-lake/sql/st-geomfromwkt.md)
- [ST_GEOMETRYFROMEWKT](/tidb-cloud-lake/sql/st-geometryfromewkt.md)
- [ST_GEOMFROMEWKT](/tidb-cloud-lake/sql/st-geomfromewkt.md)
- [ST_GEOMFROMTEXT](/tidb-cloud-lake/sql/st-geomfromtext.md)
- [ST_GEOMETRYFROMTEXT](/tidb-cloud-lake/sql/st-geometryfromtext.md)

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-----------------------------------------------------------------|
| `<string>`  | 引数は、WKT または EWKT 形式の文字列表現である必要があります。 |
| `<srid>`    | 使用する SRID の整数値です。                           |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

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
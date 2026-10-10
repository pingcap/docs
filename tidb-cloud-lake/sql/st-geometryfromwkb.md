---
title: ST_GEOMETRYFROMWKB
summary: WKB(well-known-binary) または EWKB(extended well-known-binary) の入力を解析し、GEOMETRY 型の値を返します。
---

# ST_GEOMETRYFROMWKB

[WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) または [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) の入力を解析し、GEOMETRY 型の値を返します。

## 構文 {#syntax}

```sql
ST_GEOMETRYFROMWKB(<string>, [<srid>])
ST_GEOMETRYFROMWKB(<binary>, [<srid>])
```

## エイリアス {#aliases}

- [ST_GEOMFROMWKB](/tidb-cloud-lake/sql/st-geomfromwkb.md)
- [ST_GEOMETRYFROMEWKB](/tidb-cloud-lake/sql/st-geometryfromewkb.md)
- [ST_GEOMFROMEWKB](/tidb-cloud-lake/sql/st-geomfromewkb.md)

## 引数 {#arguments}

| 引数        | 説明                                                                 |
|-------------|----------------------------------------------------------------------|
| `<string>`  | 引数は、16進形式の WKB または EWKB の文字列表現である必要があります。 |
| `<binary>`  | 引数は、WKB または EWKB 形式のバイナリ式である必要があります。       |
| `<srid>`    | 使用する SRID の整数値です。                                         |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

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
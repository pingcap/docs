---
title: ST_GEOGRAPHYFROMWKT
summary: WKT(well-known-text) または EWKT(extended well-known-text) の入力を解析し、GEOGRAPHY 型の値を返します。
---

# ST_GEOGRAPHYFROMWKT

[WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) または [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) の入力を解析し、GEOGRAPHY 型の値を返します。

## 構文 {#syntax}

```sql
ST_GEOGRAPHYFROMWKT(<string>)
```

## エイリアス {#aliases}

- [ST_GEOGFROMWKT](/tidb-cloud-lake/sql/st-geogfromwkt.md)
- [ST_GEOGRAPHYFROMEWKT](/tidb-cloud-lake/sql/st-geographyfromewkt.md)
- [ST_GEOGRAPHYFROMTEXT](/tidb-cloud-lake/sql/st-geographyfromtext.md)
- [ST_GEOGFROMTEXT](/tidb-cloud-lake/sql/st-geogfromtext.md)

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-----------------------------------------------------------------|
| `<string>`  | 引数は、WKT または EWKT 形式の文字列表現である必要があります。 |

> **Note:**
>
> GEOGRAPHY 入力では、SRID 4326 のみがサポートされています。

## 戻り値の型 {#return-type}

Geography。

## 例 {#examples}

```sql
SELECT
  ST_ASWKT(
    ST_GEOGRAPHYFROMWKT(
      'POINT(1 2)'
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASEWKT(
    ST_GEOGRAPHYFROMWKT(
      'SRID=4326;POINT(1 2)'
    )
  ) AS pipeline_geography;

┌──────────────────────┐
│ pipeline_geography   │
├──────────────────────┤
│ SRID=4326;POINT(1 2) │
└──────────────────────┘
```
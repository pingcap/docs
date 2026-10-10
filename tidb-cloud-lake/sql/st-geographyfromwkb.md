---
title: ST_GEOGRAPHYFROMWKB
summary: WKB(well-known-binary) または EWKB(extended well-known-binary) の入力を解析し、GEOGRAPHY 型の値を返します。
---

# ST_GEOGRAPHYFROMWKB

[WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) または [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) の入力を解析し、GEOGRAPHY 型の値を返します。

## 構文 {#syntax}

```sql
ST_GEOGRAPHYFROMWKB(<string>)
ST_GEOGRAPHYFROMWKB(<binary>)
```

## エイリアス {#aliases}

- [ST_GEOGFROMWKB](/tidb-cloud-lake/sql/st-geogfromwkb.md)
- [ST_GEOGETRYFROMWKB](/tidb-cloud-lake/sql/st-geogetryfromwkb.md)
- [ST_GEOGFROMEWKB](/tidb-cloud-lake/sql/st-geogfromewkb.md)

## 引数 {#arguments}

| 引数        | 説明                                                                           |
|-------------|--------------------------------------------------------------------------------|
| `<string>`  | 引数は、16進形式の WKB または EWKB の文字列表現である必要があります。          |
| `<binary>`  | 引数は、WKB または EWKB 形式のバイナリ式である必要があります。                 |

> **Note:**
>
> GEOGRAPHY 入力では、SRID 4326 のみがサポートされています。

## 戻り値の型 {#return-type}

Geography。

## 例 {#examples}

```sql
SELECT
  ST_ASWKT(
    ST_GEOGRAPHYFROMWKB(
      '0101000020E6100000000000000000F03F0000000000000040'
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASWKT(
    ST_GEOGRAPHYFROMWKB(
      FROM_HEX('0101000000000000000000F03F0000000000000040')
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘
```
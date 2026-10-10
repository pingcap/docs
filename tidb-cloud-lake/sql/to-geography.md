---
title: TO_GEOGRAPHY
summary: 入力を解析し、GEOGRAPHY 型の値を返します。
---

# TO_GEOGRAPHY

入力を解析し、GEOGRAPHY 型の値を返します。

`TRY_TO_GEOGRAPHY` は、解析中にエラーが発生した場合に NULL 値を返します。

## 構文 {#syntax}

```sql
TO_GEOGRAPHY(<string>)
TO_GEOGRAPHY(<binary>)
TO_GEOGRAPHY(<variant>)
TRY_TO_GEOGRAPHY(<string>)
TRY_TO_GEOGRAPHY(<binary>)
TRY_TO_GEOGRAPHY(<variant>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------------------------------------------------------------|
| `<string>`  | 引数は、WKT または EWKT 形式の文字列表現である必要があります。         |
| `<binary>`  | 引数は、WKB または EWKB 形式のバイナリ表現である必要があります。       |
| `<variant>` | 引数は、GeoJSON 形式の JSON OBJECT である必要があります。              |

> **Note:**
>
> GEOGRAPHY 入力では、SRID 4326 のみがサポートされています。

## 戻り値の型 {#return-type}

Geography。

## 例 {#examples}

```sql
SELECT
  ST_ASWKT(
    TO_GEOGRAPHY(
      'POINT(1 2)'
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASWKT(
    TO_GEOGRAPHY(
      FROM_HEX('0101000000000000000000F03F0000000000000040')
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘

SELECT
  ST_ASWKT(
    TO_GEOGRAPHY(
      PARSE_JSON('{"type":"Point","coordinates":[1,2]}')
    )
  ) AS pipeline_geography;

┌────────────────────┐
│ pipeline_geography │
├────────────────────┤
│ POINT(1 2)         │
└────────────────────┘
```
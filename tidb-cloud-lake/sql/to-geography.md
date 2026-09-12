---
title: TO_GEOGRAPHY
summary: 解析输入并返回 GEOGRAPHY 类型的值。
---

# TO_GEOGRAPHY

解析输入并返回 GEOGRAPHY 类型的值。

如果在解析过程中发生错误，`TRY_TO_GEOGRAPHY` 会返回 `NULL` 值。

## 语法 {#syntax}

```sql
TO_GEOGRAPHY(<string>)
TO_GEOGRAPHY(<binary>)
TO_GEOGRAPHY(<variant>)
TRY_TO_GEOGRAPHY(<string>)
TRY_TO_GEOGRAPHY(<binary>)
TRY_TO_GEOGRAPHY(<variant>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------------------------------------------------------------|
| `<string>`  | 该参数必须是 WKT 或 EWKT 格式的字符串表达式。         |
| `<binary>`  | 该参数必须是 WKB 或 EWKB 格式的二进制表达式。         |
| `<variant>` | 该参数必须是 GeoJSON 格式的 JSON OBJECT。                   |

> **注意：**
>
> GEOGRAPHY 输入仅支持 SRID 4326。

## 返回类型 {#return-type}

Geography。

## 示例 {#examples}

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
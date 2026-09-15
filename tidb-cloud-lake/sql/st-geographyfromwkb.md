---
title: ST_GEOGRAPHYFROMWKB
summary: 解析 WKB(well-known-binary) 或 EWKB(extended well-known-binary) 输入，并返回一个 GEOGRAPHY 类型的值。
---

# ST_GEOGRAPHYFROMWKB

解析 [WKB(well-known-binary)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary) 或 [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) 输入，并返回一个 GEOGRAPHY 类型的值。

## 语法 {#syntax}

```sql
ST_GEOGRAPHYFROMWKB(<string>)
ST_GEOGRAPHYFROMWKB(<binary>)
```

## 别名 {#aliases}

- [ST_GEOGFROMWKB](/tidb-cloud-lake/sql/st-geogfromwkb.md)
- [ST_GEOGETRYFROMWKB](/tidb-cloud-lake/sql/st-geogetryfromwkb.md)
- [ST_GEOGFROMEWKB](/tidb-cloud-lake/sql/st-geogfromewkb.md)

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|--------------------------------------------------------------------------------|
| `<string>`  | 该参数必须是十六进制格式的 WKB 或 EWKB 字符串表达式。 |
| `<binary>`  | 该参数必须是 WKB 或 EWKB 格式的二进制表达式。 |

> **注意：**
>
> GEOGRAPHY 输入仅支持 SRID 4326。

## 返回类型 {#return-type}

Geography。

## 示例 {#examples}

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
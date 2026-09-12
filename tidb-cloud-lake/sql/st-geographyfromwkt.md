---
title: ST_GEOGRAPHYFROMWKT
summary: 解析 WKT(well-known-text) 或 EWKT(extended well-known-text) 输入，并返回一个 GEOGRAPHY 类型的值。
---

# ST_GEOGRAPHYFROMWKT

解析 [WKT(well-known-text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) 或 [EWKT(extended well-known-text)](https://postgis.net/docs/ST_GeomFromEWKT.html) 输入，并返回一个 GEOGRAPHY 类型的值。

## 语法 {#syntax}

```sql
ST_GEOGRAPHYFROMWKT(<string>)
```

## 别名 {#aliases}

- [ST_GEOGFROMWKT](/tidb-cloud-lake/sql/st-geogfromwkt.md)
- [ST_GEOGRAPHYFROMEWKT](/tidb-cloud-lake/sql/st-geographyfromewkt.md)
- [ST_GEOGRAPHYFROMTEXT](/tidb-cloud-lake/sql/st-geographyfromtext.md)
- [ST_GEOGFROMTEXT](/tidb-cloud-lake/sql/st-geogfromtext.md)

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-----------------------------------------------------------------|
| `<string>`  | 该参数必须是 WKT 或 EWKT 格式的字符串表达式。 |

> **注意：**
>
> GEOGRAPHY 输入仅支持 SRID 4326。

## 返回类型 {#return-type}

Geography。

## 示例 {#examples}

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
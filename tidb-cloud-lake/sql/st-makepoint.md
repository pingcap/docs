---
title: ST_MAKEPOINT
summary: 指定した経度と緯度を持つ Point を表す GEOGRAPHY オブジェクトを構築します。
---

# ST_MAKEPOINT

指定した経度と緯度を持つ Point を表す GEOGRAPHY オブジェクトを構築します。

## 構文 {#syntax}

```sql
ST_MAKEPOINT(<longitude>, <latitude>)
```

## エイリアス {#aliases}

- [ST_POINT](/tidb-cloud-lake/sql/st-point.md)

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|-----------------------------------------------|
| `<longitude>` | 経度を表す Double 値です。 |
| `<latitude>`  | 緯度を表す Double 値です。  |

## 戻り値の型 {#return-type}

Geography。

## 例 {#examples}

```sql
SELECT
  ST_ASWKT(
    ST_MAKEPOINT(
      7.0, 8.0
    )
  ) AS pipeline_point;

┌────────────────┐
│ pipeline_point │
├────────────────┤
│ POINT(7 8)     │
└────────────────┘

SELECT
  ST_ASWKT(
    ST_MAKEPOINT(
      -122.3061, 37.554162
    )
  ) AS pipeline_point;

╭────────────────────────────╮
│       pipeline_point       │
├────────────────────────────┤
│ POINT(-122.3061 37.554162) │
╰────────────────────────────╯
```
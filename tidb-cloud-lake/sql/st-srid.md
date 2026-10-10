---
title: ST_SRID
summary: GEOMETRY または GEOGRAPHY オブジェクトの SRID（空間参照系識別子）を返します。
---

# ST_SRID

GEOMETRY または GEOGRAPHY オブジェクトの SRID（空間参照系識別子）を返します。

## 構文 {#syntax}

```sql
ST_SRID(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

INT32。

> **Note:**
>
> - Geometry に SRID がない場合、デフォルト値 `0` が返されます。
> - Geography の SRID は常に `4326` です。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_SRID(
    TO_GEOMETRY(
      'POINT(-122.306100 37.554162)',
      1234
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          1234 │
└───────────────┘

SELECT
  ST_SRID(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│             0 │
└───────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_SRID(
    ST_GEOGFROMWKT(
      'POINT(1 2)'
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          4326 │
└───────────────┘
```
---
title: ST_DIMENSION
summary: ジオメトリオブジェクトの次元を返します。GEOMETRY または GEOGRAPHY オブジェクトの次元は次のとおりです。
---

# ST_DIMENSION

ジオメトリオブジェクトの次元を返します。GEOMETRY または GEOGRAPHY オブジェクトの次元は次のとおりです。

| 地理空間オブジェクト型       | 次元  |
|------------------------------|------------|
| 点 / マルチポイント           | 0          |
| 線ストリング / マルチ線ストリング | 1          |
| ポリゴン / マルチポリゴン       | 2          |

## 構文 {#syntax}

```sql
ST_DIMENSION(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

UInt8。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  0 │
└────────────────────┘

SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'LINESTRING(-124.20 42.00, -120.01 41.99)'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  1 │
└────────────────────┘

SELECT
  ST_DIMENSION(
    ST_GEOMETRYFROMWKT(
      'POLYGON((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.00))'
    )
  ) AS pipeline_dimension;

┌────────────────────┐
│ pipeline_dimension │
├────────────────────┤
│                  2 │
└────────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_DIMENSION(
    ST_GEOGFROMWKT(
      'LINESTRING(-124.20 42.00, -120.01 41.99)'
    )
  ) AS pipeline_dimension;

╭────────────────────╮
│ pipeline_dimension │
├────────────────────┤
│                  1 │
╰────────────────────╯
```
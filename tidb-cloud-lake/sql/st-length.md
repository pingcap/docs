---
title: ST_LENGTH
summary: GEOMETRY または GEOGRAPHY オブジェクト内の LineString のユークリッド長を返します。
---

# ST_LENGTH

GEOMETRY または GEOGRAPHY オブジェクト内の LineString のユークリッド長を返します。

## 構文 {#syntax}

```sql
ST_LENGTH(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry_or_geography>` | 引数は、linestring を含む GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

> **Note:**
>
> - `<geometry_or_geography>` が `LineString`、`MultiLineString`、または linestring を含む `GeometryCollection` でない場合は、0 を返します。
> - `<geometry_or_geography>` が `GeometryCollection` の場合は、コレクション内の linestring の長さの合計を返します。

## 戻り値の型 {#return-type}

Double。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_LENGTH(TO_GEOMETRY('POINT(1 1)')) AS length

┌─────────┐
│  length │
├─────────┤
│       0 │
└─────────┘

SELECT
  ST_LENGTH(TO_GEOMETRY('LINESTRING(0 0, 1 1)')) AS length

┌─────────────┐
│    length   │
├─────────────┤
│ 1.414213562 │
└─────────────┘

SELECT
  ST_LENGTH(
    TO_GEOMETRY('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))')
  ) AS length

┌─────────┐
│  length │
├─────────┤
│       0 │
└─────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_LENGTH(
    ST_GEOGFROMWKT(
      'LINESTRING(0 0, 1 0)'
    )
  ) AS length

╭──────────────────╮
│      length      │
├──────────────────┤
│ 111319.490793274 │
╰──────────────────╯
```
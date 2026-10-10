---
title: ST_ASEWKB
summary: GEOMETRY または GEOGRAPHY オブジェクトを EWKB(extended well-known-binary) 形式の表現に変換します。
---

# ST_ASEWKB

GEOMETRY または GEOGRAPHY オブジェクトを [EWKB(extended well-known-binary)](https://postgis.net/docs/ST_GeomFromEWKB.html) 形式の表現に変換します。

## 構文 {#syntax}

```sql
ST_ASEWKB(<geometry_or_geography>)
```

## 引数 {#arguments}

| 引数    | 説明                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | 引数は、GEOMETRY または GEOGRAPHY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

Binary。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT
  ST_ASEWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
    )
  ) AS pipeline_ewkb;

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        pipeline_ewkb                                       │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ 0102000020E61000000200000000000000006A18410000000060E3564100000000A07918410000000024ED5641 │
└────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  ST_ASEWKB(
    ST_GEOMETRYFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkb;

┌────────────────────────────────────────────────────┐
│                    pipeline_ewkb                   │
├────────────────────────────────────────────────────┤
│ 0101000020E61000006666666666965EC06666666666C64240 │
└────────────────────────────────────────────────────┘
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT
  ST_ASEWKB(
    ST_GEOGFROMWKT(
      'SRID=4326;POINT(-122.35 37.55)'
    )
  ) AS pipeline_ewkb;

╭────────────────────────────────────────────────────╮
│                    pipeline_ewkb                   │
├────────────────────────────────────────────────────┤
│ 0101000020E61000006666666666965EC06666666666C64240 │
╰────────────────────────────────────────────────────╯
```
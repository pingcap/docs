---
title: ST_GEOGPOINTFROMGEOHASH
summary: geohash の中心を表す点に対応する GEOGRAPHY オブジェクトを返します。
---

# ST_GEOGPOINTFROMGEOHASH

[geohash](https://en.wikipedia.org/wiki/Geohash) の中心を表す点に対応する GEOGRAPHY オブジェクトを返します。

## 構文 {#syntax}

```sql
ST_GEOGPOINTFROMGEOHASH(<geohash>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|---------------------------------|
| `<geohash>` | 引数は geohash である必要があります。 |

## 戻り値の型 {#return-type}

Geography。

## 例 {#examples}

```sql
SELECT
  ST_ASWKT(
    ST_GEOGPOINTFROMGEOHASH(
      's02equ0'
    )
  ) AS pipeline_geography;

╭──────────────────────────────────────────────╮
│              pipeline_geography              │
│                    String                    │
├──────────────────────────────────────────────┤
│ POINT(1.0004425048828125 2.0001983642578125) │
╰──────────────────────────────────────────────╯
```
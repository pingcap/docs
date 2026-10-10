---
title: ST_GEOMPOINTFROMGEOHASH
summary: geohash の中心を表す点に対応する GEOMETRY オブジェクトを返します。
---

# ST_GEOMPOINTFROMGEOHASH

[geohash](https://en.wikipedia.org/wiki/Geohash) の中心を表す点に対応する GEOMETRY オブジェクトを返します。

## 構文 {#syntax}

```sql
ST_GEOMPOINTFROMGEOHASH(<geohash>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|---------------------------------|
| `<geohash>` | 引数は geohash である必要があります。 |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

```sql
SELECT
  ST_GEOMPOINTFROMGEOHASH(
    's02equ0'
  ) AS pipeline_geometry;

┌──────────────────────────────────────────────┐
│               pipeline_geometry              │
│                   Geometry                   │
├──────────────────────────────────────────────┤
│ POINT(1.0004425048828125 2.0001983642578125) │
└──────────────────────────────────────────────┘
```
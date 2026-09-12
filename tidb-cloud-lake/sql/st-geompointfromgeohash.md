---
title: ST_GEOMPOINTFROMGEOHASH
summary: 返回一个 GEOMETRY 对象，表示 geohash 中心点对应的点。
---

# ST_GEOMPOINTFROMGEOHASH

返回一个 GEOMETRY 对象，表示 [geohash](https://en.wikipedia.org/wiki/Geohash) 中心点对应的点。

## 语法 {#syntax}

```sql
ST_GEOMPOINTFROMGEOHASH(<geohash>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|---------------------------------|
| `<geohash>` | 该参数必须是一个 geohash。 |

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

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
---
title: ST_AZIMUTH
summary: ある Point から別の Point への線分の方位角をラジアンで返します。方位角は正の Y 軸（北）から時計回りに測定されます。2 つの点が同一の場合は NULL を返します。
---

# ST_AZIMUTH

ある Point から別の Point への線分の方位角をラジアンで返します。方位角は正の Y 軸（北）から時計回りに測定されます。2 つの点が同一の場合は NULL を返します。

## 構文 {#syntax}

```sql
ST_AZIMUTH(<point1>, <point2>)
```

## 引数 {#arguments}

| 引数  | 説明                                          |
|------------|------------------------------------------------------|
| `<point1>` | Point 型の GEOMETRY 式（始点）。        |
| `<point2>` | Point 型の GEOMETRY 式（終点）。        |

> **Note:**
>
> 両方の引数は Point ジオメトリである必要があります。その他の型を指定するとエラーになります。

## 戻り値の型 {#return-type}

Double（NULL 可）。

## 例 {#examples}

```sql
-- Due north (along positive Y-axis): 0 radians
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(0 1)'));

┌────────┐
│ result │
├────────┤
│ 0.0    │
└────────┘

-- Due east: π/2 radians
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 0)'));

┌─────────────┐
│    result   │
├─────────────┤
│ 1.570796327 │
└─────────────┘

-- Due south: π radians
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 1)'), TO_GEOMETRY('POINT(0 0)'));

┌─────────────┐
│    result   │
├─────────────┤
│ 3.141592654 │
└─────────────┘

-- Identical points: NULL
SELECT ST_AZIMUTH(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(0 0)'));

┌────────┐
│ result │
├────────┤
│ NULL   │
└────────┘
```
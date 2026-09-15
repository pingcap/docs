---
title: ST_AZIMUTH
summary: 返回从一个 Point 到另一个 Point 的线段的方位角（以弧度表示），从正 Y 轴（北）开始按顺时针方向测量。如果两个点相同，则返回 NULL。
---

# ST_AZIMUTH

返回从一个 Point 到另一个 Point 的线段的方位角（以弧度表示），从正 Y 轴（北）开始按顺时针方向测量。如果两个点相同，则返回 NULL。

## 语法 {#syntax}

```sql
ST_AZIMUTH(<point1>, <point2>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------|------------------------------------------------------|
| `<point1>` | 类型为 Point 的 GEOMETRY 表达式（起点）。 |
| `<point2>` | 类型为 Point 的 GEOMETRY 表达式（目标点）。 |

> **注意：**
>
> 两个参数都必须是 Point 几何对象。其他类型会产生错误。

## 返回类型 {#return-type}

Double（可为空）。

## 示例 {#examples}

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
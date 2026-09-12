---
title: ST_HAUSDORFFDISTANCE
summary: 返回两个 GEOMETRY 对象之间的离散 Hausdorff 距离。它通过查找一个对象中任意顶点到另一个对象中最近顶点的最大距离，来衡量两个几何对象相距多远。
---

# ST_HAUSDORFFDISTANCE

返回两个 GEOMETRY 对象之间的离散 Hausdorff 距离。它通过查找一个对象中任意顶点到另一个对象中最近顶点的最大距离，来衡量两个几何对象相距多远。

## 语法 {#syntax}

```sql
ST_HAUSDORFFDISTANCE(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数          | 描述                 |
|---------------|----------------------|
| `<geometry1>` | 一个 GEOMETRY 表达式。 |
| `<geometry2>` | 一个 GEOMETRY 表达式。 |

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

```sql
SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('POINT(0 0)'),
  TO_GEOMETRY('POINT(0 1)')
);

┌────────┐
│ result │
├────────┤
│ 1.0    │
└────────┘

SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('LINESTRING(0 0, 1 0)'),
  TO_GEOMETRY('LINESTRING(0 1, 1 1)')
);

┌────────┐
│ result │
├────────┤
│ 1.0    │
└────────┘

SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
  TO_GEOMETRY('POLYGON((2 0, 3 0, 3 1, 2 1, 2 0))')
);

┌────────┐
│ result │
├────────┤
│ 2.0    │
└────────┘
```
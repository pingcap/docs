---
title: ST_MAKEPOLYGONORIENTED
summary: 从 LineString 输入创建 Polygon，并保留给定的顶点顺序。与 ST_MAKEPOLYGON 不同，此函数不会重新排序顶点以强制特定的环绕方向。
---

# ST_MAKEPOLYGONORIENTED

从 LineString 输入创建 Polygon，并保留给定的顶点顺序。与 [ST_MAKEPOLYGON](/tidb-cloud-lake/sql/st-makepolygon.md) 不同，此函数不会重新排序顶点以强制特定的环绕方向。

## 语法 {#syntax}

```sql
ST_MAKEPOLYGONORIENTED(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry>` | 类型为 LineString 的 GEOMETRY 表达式。必须至少包含 4 个点，且第一个点和最后一个点必须相同。 |

> **注意：**
>
> - 仅接受 LineString 输入。其他类型会产生错误。
> - LineString 必须构成有效的多边形（不能有自相交）。

## 返回类型 {#return-type}

Geometry。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(
  ST_MAKEPOLYGONORIENTED(TO_GEOMETRY('LINESTRING(0 0, 1 0, 1 2, 0 2, 0 0)'))
);

┌──────────────────────────────────┐
│             result               │
├──────────────────────────────────┤
│ POLYGON((0 0,1 0,1 2,0 2,0 0))  │
└──────────────────────────────────┘

-- Reversed winding order is preserved
SELECT ST_ASWKT(
  ST_MAKEPOLYGONORIENTED(TO_GEOMETRY('LINESTRING(0 0, 0 2, 1 2, 1 0, 0 0)'))
);

┌──────────────────────────────────┐
│             result               │
├──────────────────────────────────┤
│ POLYGON((0 0,0 2,1 2,1 0,0 0))  │
└──────────────────────────────────┘
```
---
title: H3_EDGE_ANGLE
summary: 返回 H3 六边形边的平均长度（以 grade 为单位）。
---

# H3_EDGE_ANGLE

返回 H3 六边形边的平均长度（以 grade 为单位）。

## 语法 {#syntax}

```sql
H3_EDGE_ANGLE(res)
```

## 示例 {#examples}

```sql
SELECT H3_EDGE_ANGLE(10);

┌───────────────────────┐
│   h3_edge_angle(10)   │
├───────────────────────┤
│ 0.0006822586214153981 │
└───────────────────────┘
```
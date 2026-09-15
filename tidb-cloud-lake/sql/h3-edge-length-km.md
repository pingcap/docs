---
title: H3_EDGE_LENGTH_KM
summary: 返回给定分辨率下六边形边长的平均值（单位为千米）。不包括五边形。
---

# H3_EDGE_LENGTH_KM

返回给定分辨率下六边形边长的平均值（单位为千米）。不包括五边形。

## 语法 {#syntax}

```sql
H3_EDGE_LENGTH_KM(res)
```

## 示例 {#examples}

```sql
SELECT H3_EDGE_LENGTH_KM(1);

┌──────────────────────┐
│ h3_edge_length_km(1) │
├──────────────────────┤
│    483.0568390711111 │
└──────────────────────┘
```
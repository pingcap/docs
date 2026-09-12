---
title: H3_EXACT_EDGE_LENGTH_RADS
summary: 计算此有向边的长度，单位为弧度。
---

# H3_EXACT_EDGE_LENGTH_RADS

计算此有向边的长度，单位为弧度。

## 语法 {#syntax}

```sql
H3_EXACT_EDGE_LENGTH_RADS(h3)
```

## 示例 {#examples}

```sql
SELECT H3_EXACT_EDGE_LENGTH_KM(1319695429381652479);

┌──────────────────────────────────────────────┐
│ h3_exact_edge_length_km(1319695429381652479) │
├──────────────────────────────────────────────┤
│                            8.267326832647143 │
└──────────────────────────────────────────────┘
```
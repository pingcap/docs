---
title: H3_EDGE_ANGLE
summary: グラード単位で H3 六角形の辺の平均長を返します。
---

# H3_EDGE_ANGLE

グラード単位で H3 六角形の辺の平均長を返します。

## 構文 {#syntax}

```sql
H3_EDGE_ANGLE(res)
```

## 例 {#examples}

```sql
SELECT H3_EDGE_ANGLE(10);

┌───────────────────────┐
│   h3_edge_angle(10)   │
├───────────────────────┤
│ 0.0006822586214153981 │
└───────────────────────┘
```
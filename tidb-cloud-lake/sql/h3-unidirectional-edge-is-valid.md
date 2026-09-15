---
title: H3_UNIDIRECTIONAL_EDGE_IS_VALID
summary: 判断提供的 H3Index 是否为有效的单向边索引。如果它是单向边，则返回 1；否则返回 0。
---

# H3_UNIDIRECTIONAL_EDGE_IS_VALID

判断提供的 H3Index 是否为有效的单向边索引。如果它是单向边，则返回 1；否则返回 0。

## 语法 {#syntax}

```sql
H3_UNIDIRECTIONAL_EDGE_IS_VALID(h3)
```

## 示例 {#examples}

```sql
SELECT H3_UNIDIRECTIONAL_EDGE_IS_VALID(1248204388774707199);

┌──────────────────────────────────────────────────────┐
│ h3_unidirectional_edge_is_valid(1248204388774707199) │
├──────────────────────────────────────────────────────┤
│ true                                                 │
└──────────────────────────────────────────────────────┘
```
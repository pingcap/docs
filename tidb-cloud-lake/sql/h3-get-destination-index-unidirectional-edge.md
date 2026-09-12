---
title: H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE
summary: 返回单向边 H3Index 的目标六边形索引。
---

# H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE

返回单向边 H3Index 的目标六边形索引。

## 语法 {#syntax}

```sql
H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(h3)
```

## 示例 {#examples}

```sql
SELECT H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(1248204388774707199);

┌────────────────────────────────────────────────────────────────────────┐
│ h3_get_destination_index_from_unidirectional_edge(1248204388774707199) │
├────────────────────────────────────────────────────────────────────────┤
│                                                     599686043507097599 │
└────────────────────────────────────────────────────────────────────────┘
```
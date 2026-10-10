---
title: H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE
summary: 単方向エッジ H3Index から終点の六角形インデックスを返します。
---

# H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE

単方向エッジ H3Index から終点の六角形インデックスを返します。

## 構文 {#syntax}

```sql
H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(h3)
```

## 例 {#examples}

```sql
SELECT H3_GET_DESTINATION_INDEX_FROM_UNIDIRECTIONAL_EDGE(1248204388774707199);

┌────────────────────────────────────────────────────────────────────────┐
│ h3_get_destination_index_from_unidirectional_edge(1248204388774707199) │
├────────────────────────────────────────────────────────────────────────┤
│                                                     599686043507097599 │
└────────────────────────────────────────────────────────────────────────┘
```
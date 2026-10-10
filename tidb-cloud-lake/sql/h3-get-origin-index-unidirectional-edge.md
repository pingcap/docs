---
title: H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE
summary: unidirectional edge H3Index から始点の六角形インデックスを返します。
---

# H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE

unidirectional edge H3Index から始点の六角形インデックスを返します。

## 構文 {#syntax}

```sql
H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(h3)
```

## 例 {#examples}

```sql
SELECT H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(1248204388774707199);

┌───────────────────────────────────────────────────────────────────┐
│ h3_get_origin_index_from_unidirectional_edge(1248204388774707199) │
├───────────────────────────────────────────────────────────────────┤
│                                                599686042433355775 │
└───────────────────────────────────────────────────────────────────┘
```
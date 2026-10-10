---
title: H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE
summary: 指定された単方向エッジ H3Index から、始点および終点の六角形インデックスを返します。
---

# H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE

指定された単方向エッジ H3Index から、始点および終点の六角形インデックスを返します。

## 構文 {#syntax}

```sql
H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE(h3)
```

## 例 {#examples}

```sql
SELECT H3_GET_INDEXES_FROM_UNIDIRECTIONAL_EDGE(1248204388774707199);

┌──────────────────────────────────────────────────────────────┐
│ h3_get_indexes_from_unidirectional_edge(1248204388774707199) │
├──────────────────────────────────────────────────────────────┤
│ (599686042433355775,599686043507097599)                      │
└──────────────────────────────────────────────────────────────┘
```
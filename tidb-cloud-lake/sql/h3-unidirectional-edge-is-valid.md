---
title: H3_UNIDIRECTIONAL_EDGE_IS_VALID
summary: 指定された H3Index が有効な単方向エッジインデックスかどうかを判定します。単方向エッジであれば 1 を返し、それ以外の場合は 0 を返します。
---

# H3_UNIDIRECTIONAL_EDGE_IS_VALID

指定された H3Index が有効な単方向エッジインデックスかどうかを判定します。単方向エッジであれば 1 を返し、それ以外の場合は 0 を返します。

## 構文 {#syntax}

```sql
H3_UNIDIRECTIONAL_EDGE_IS_VALID(h3)
```

## 例 {#examples}

```sql
SELECT H3_UNIDIRECTIONAL_EDGE_IS_VALID(1248204388774707199);

┌──────────────────────────────────────────────────────┐
│ h3_unidirectional_edge_is_valid(1248204388774707199) │
├──────────────────────────────────────────────────────┤
│ true                                                 │
└──────────────────────────────────────────────────────┘
```
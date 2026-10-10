---
title: CONTAINS
summary: 配列に特定の要素が含まれているかどうかを確認します。
---

# CONTAINS

配列に特定の要素が含まれているかどうかを確認します。

## 構文 {#syntax}

```sql
CONTAINS( <array>, <element> )
```

## エイリアス {#aliases}

- [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md)

## 例 {#examples}

```sql
SELECT ARRAY_CONTAINS([1, 2], 1), CONTAINS([1, 2], 1);

┌─────────────────────────────────────────────────┐
│ array_contains([1, 2], 1) │ contains([1, 2], 1) │
├───────────────────────────┼─────────────────────┤
│ true                      │ true                │
└─────────────────────────────────────────────────┘
```
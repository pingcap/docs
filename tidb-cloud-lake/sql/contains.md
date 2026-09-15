---
title: CONTAINS
summary: 检查数组是否包含特定元素。
---

# CONTAINS

检查数组是否包含特定元素。

## 语法 {#syntax}

```sql
CONTAINS( <array>, <element> )
```

## 别名 {#aliases}

- [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md)

## 示例 {#examples}

```sql
SELECT ARRAY_CONTAINS([1, 2], 1), CONTAINS([1, 2], 1);

┌─────────────────────────────────────────────────┐
│ array_contains([1, 2], 1) │ contains([1, 2], 1) │
├───────────────────────────┼─────────────────────┤
│ true                      │ true                │
└─────────────────────────────────────────────────┘
```
---
title: ARRAY_COUNT
summary: 统计数组中非 `NULL` 元素的数量。
---

# ARRAY_COUNT

统计数组中非 `NULL` 元素的数量。

## 语法 {#syntax}

```sql
ARRAY_COUNT(<array>)
```

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT ARRAY_COUNT([1, 2, 3]) AS cnt;

┌─────┐
│ cnt │
├─────┤
│   3 │
└─────┘
```

```sql
SELECT ARRAY_COUNT([1, NULL, 3]) AS cnt_with_null;

┌──────────────┐
│ cnt_with_null│
├──────────────┤
│            2 │
└──────────────┘
```

```sql
SELECT ARRAY_COUNT(['a', 'b', NULL]) AS cnt_text;

┌─────────┐
│ cnt_text│
├─────────┤
│       2 │
└─────────┘
```
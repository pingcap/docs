---
title: ARRAY_ANY
summary: 返回数组中第一个非 `NULL` 元素。等价于 `ARRAY_AGGREGATE(<array>, 'ANY')`。
---

# ARRAY_ANY

返回数组中第一个非 `NULL` 元素。等价于 `ARRAY_AGGREGATE(<array>, 'ANY')`。

## 语法 {#syntax}

```sql
ARRAY_ANY(<array>)
```

## 返回类型 {#return-type}

与数组元素类型相同。

## 示例 {#examples}

```sql
SELECT ARRAY_ANY(['a', 'b', 'c']) AS first_item;

┌────────────┐
│ first_item │
├────────────┤
│ a          │
└────────────┘
```

```sql
SELECT ARRAY_ANY([NULL, 'x', 'y']) AS first_non_null;

┌────────────────┐
│ first_non_null │
├────────────────┤
│ x              │
└────────────────┘
```

```sql
SELECT ARRAY_ANY([NULL, 10, 20]) AS first_number;

┌──────────────┐
│ first_number │
├──────────────┤
│           10 │
└──────────────┘
```
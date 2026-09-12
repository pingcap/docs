---
title: ARRAY_SORT
summary: 对数组中的元素进行排序。默认情况下，ARRAY_SORT 按升序排序，并将 NULL 值放在最后。使用显式变体可以控制排序顺序和 NULL 的放置位置。
---

# ARRAY_SORT

对数组中的元素进行排序。默认情况下，`ARRAY_SORT` 按升序排序，并将 `NULL` 值放在最后。使用显式变体可以控制排序顺序和 `NULL` 的放置位置。

## 语法 {#syntax}

```sql
ARRAY_SORT(<array>)
ARRAY_SORT_ASC_NULL_FIRST(<array>)
ARRAY_SORT_ASC_NULL_LAST(<array>)
ARRAY_SORT_DESC_NULL_FIRST(<array>)
ARRAY_SORT_DESC_NULL_LAST(<array>)
```

## 返回类型 {#return-type}

`ARRAY`

## 示例 {#examples}

```sql
SELECT ARRAY_SORT([3, 1, 2]) AS sort_default;

┌──────────────┐
│ sort_default │
├──────────────┤
│ [1,2,3]      │
└──────────────┘
```

```sql
SELECT ARRAY_SORT([NULL, 2, 1]) AS sort_with_nulls;

┌────────────────┐
│ sort_with_nulls│
├────────────────┤
│ [1,2,NULL]     │
└────────────────┘
```

```sql
SELECT ARRAY_SORT_ASC_NULL_FIRST([NULL, 2, 1]) AS asc_null_first;

┌────────────────┐
│ asc_null_first │
├────────────────┤
│ [NULL,1,2]     │
└────────────────┘
```

```sql
SELECT ARRAY_SORT_DESC_NULL_LAST([NULL, 2, 1]) AS desc_null_last;

┌────────────────┐
│ desc_null_last │
├────────────────┤
│ [2,1,NULL]     │
└────────────────┘

SELECT ARRAY_SORT_DESC_NULL_FIRST([NULL, 2, 1]) AS desc_null_first;

┌─────────────────┐
│ desc_null_first │
├─────────────────┤
│ [NULL,2,1]      │
└─────────────────┘
```
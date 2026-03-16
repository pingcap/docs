---
title: ARRAY_SORT
title_includes: ARRAY_SORT_ASC_NULL_FIRST, ARRAY_SORT_ASC_NULL_LAST, ARRAY_SORT_DESC_NULL_FIRST, ARRAY_SORT_DESC_NULL_LAST
---

Sorts the elements of an array. By default, `ARRAY_SORT` orders ascending and places `NULL` values last. Use the explicit variants to control order and `NULL` placement.

## Syntax

```sql
ARRAY_SORT(<array>)
ARRAY_SORT_ASC_NULL_FIRST(<array>)
ARRAY_SORT_ASC_NULL_LAST(<array>)
ARRAY_SORT_DESC_NULL_FIRST(<array>)
ARRAY_SORT_DESC_NULL_LAST(<array>)
```

## Return Type

`ARRAY`

## Examples

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

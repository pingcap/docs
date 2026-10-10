---
title: ARRAY_SORT
summary: 配列の要素をソートします。デフォルトでは、ARRAY_SORT は昇順で並べ替え、NULL 値を最後に配置します。順序と NULL の配置を制御するには、明示的なバリアントを使用します。
---

# ARRAY_SORT

配列の要素をソートします。デフォルトでは、`ARRAY_SORT` は昇順で並べ替え、`NULL` 値を最後に配置します。順序と `NULL` の配置を制御するには、明示的なバリアントを使用します。

## 構文 {#syntax}

```sql
ARRAY_SORT(<array>)
ARRAY_SORT_ASC_NULL_FIRST(<array>)
ARRAY_SORT_ASC_NULL_LAST(<array>)
ARRAY_SORT_DESC_NULL_FIRST(<array>)
ARRAY_SORT_DESC_NULL_LAST(<array>)
```

## 戻り値の型 {#return-type}

`ARRAY`

## 例 {#examples}

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
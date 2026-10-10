---
title: ARRAY
summary: 指定された式から配列リテラルを構築します。各引数は評価され、順番に格納されます。すべての要素は共通の型にキャスト可能である必要があります。
---

# ARRAY

指定された式から配列リテラルを構築します。各引数は評価され、順番に格納されます。すべての要素は共通の型にキャスト可能である必要があります。

## 構文 {#syntax}

```sql
ARRAY(<expr1>, <expr2>, ... )
```

## 戻り値の型 {#return-type}

`ARRAY`

## 例 {#examples}

```sql
SELECT ARRAY(1, 2, 3) AS arr_int;

┌─────────┐
│ arr_int │
├─────────┤
│ [1,2,3] │
└─────────┘
```

```sql
SELECT ARRAY('alpha', UPPER('beta')) AS arr_text;

┌───────────┐
│ arr_text  │
├───────────┤
│ ["alpha","BETA"] │
└───────────┘
```

```sql
SELECT ARRAY(1, NULL, 3) AS arr_with_null;

┌────────────────┐
│ arr_with_null  │
├────────────────┤
│ [1,NULL,3]     │
└────────────────┘
```
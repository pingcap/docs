---
title: ARRAY_TO_STRING
summary: 配列の文字列要素を区切り文字で連結して、1 つの文字列にします。`NULL` 要素はスキップされます。
---

# ARRAY_TO_STRING

配列の文字列要素を区切り文字で連結して、1 つの文字列にします。`NULL` 要素はスキップされます。

## 構文 {#syntax}

```sql
ARRAY_TO_STRING(<array_of_strings>, <delimiter>)
```

## 戻り値の型 {#return-type}

`STRING`

## 例 {#examples}

```sql
SELECT ARRAY_TO_STRING(['a', 'b', 'c'], ',') AS joined;

┌────────┐
│ joined │
├────────┤
│ a,b,c  │
└────────┘
```

```sql
SELECT ARRAY_TO_STRING([NULL, 'x', 'y'], '-') AS joined_no_nulls;

┌──────────────────┐
│ joined_no_nulls  │
├──────────────────┤
│ x-y              │
└──────────────────┘
```
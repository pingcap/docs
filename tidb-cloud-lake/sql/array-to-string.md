---
title: ARRAY_TO_STRING
summary: 将数组中的字符串元素连接为一个字符串，并使用分隔符分隔。`NULL` 元素会被跳过。
---

# ARRAY_TO_STRING

将数组中的字符串元素连接为一个字符串，并使用分隔符分隔。`NULL` 元素会被跳过。

## 语法 {#syntax}

```sql
ARRAY_TO_STRING(<array_of_strings>, <delimiter>)
```

## 返回类型 {#return-type}

`STRING`

## 示例 {#examples}

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
---
title: LOWER
summary: 返回一个将所有字符都转换为小写的字符串。
---

# LOWER

返回一个将所有字符都转换为小写的字符串。

## 语法 {#syntax}

```sql
LOWER(<str>)
```

## 别名 {#aliases}

- [LCASE](/tidb-cloud-lake/sql/lcase.md)

## 返回类型 {#return-type}

VARCHAR

## 示例 {#examples}

```sql
SELECT LOWER('Hello, DataLake!'), LCASE('Hello, DataLake!');

┌───────────────────────────────────────────────────────┐
│ lower('hello, datalake!') │ lcase('hello, datalake!') │
├───────────────────────────┼───────────────────────────┤
│ hello, datalake!          │ hello, datalake!          │
└───────────────────────────────────────────────────────┘
```
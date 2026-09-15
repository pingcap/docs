---
title: UPPER
summary: 返回一个将所有字符都转换为大写的字符串。
---

# UPPER

返回一个将所有字符都转换为大写的字符串。

## 语法 {#syntax}

```sql
UPPER(<str>)
```

## 别名 {#aliases}

- [UCASE](/tidb-cloud-lake/sql/ucase.md)

## 返回类型 {#return-type}

VARCHAR

## 示例 {#examples}

```sql
SELECT UPPER('Hello, Datalake!'), UCASE('Hello, Datalake!');

┌───────────────────────────────────────────────────────┐
│ upper('hello, datalake!') │ ucase('hello, datalake!') │
├───────────────────────────┼───────────────────────────┤
│ HELLO, DATALAKE!          │ HELLO, DATALAKE!          │
└───────────────────────────────────────────────────────┘
```
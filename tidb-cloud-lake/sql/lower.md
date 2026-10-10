---
title: LOWER
summary: すべての文字を小文字に変換した文字列を返します。
---

# LOWER

すべての文字を小文字に変換した文字列を返します。

## 構文 {#syntax}

```sql
LOWER(<str>)
```

## エイリアス {#aliases}

- [LCASE](/tidb-cloud-lake/sql/lcase.md)

## 戻り値の型 {#return-type}

VARCHAR

## 例 {#examples}

```sql
SELECT LOWER('Hello, DataLake!'), LCASE('Hello, DataLake!');

┌───────────────────────────────────────────────────────┐
│ lower('hello, datalake!') │ lcase('hello, datalake!') │
├───────────────────────────┼───────────────────────────┤
│ hello, datalake!          │ hello, datalake!          │
└───────────────────────────────────────────────────────┘
```
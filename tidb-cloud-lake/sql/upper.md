---
title: UPPER
summary: すべての文字を大文字に変換した文字列を返します。
---

# UPPER

すべての文字を大文字に変換した文字列を返します。

## 構文 {#syntax}

```sql
UPPER(<str>)
```

## エイリアス {#aliases}

- [UCASE](/tidb-cloud-lake/sql/ucase.md)

## 戻り値の型 {#return-type}

VARCHAR

## 例 {#examples}

```sql
SELECT UPPER('Hello, Datalake!'), UCASE('Hello, Datalake!');

┌───────────────────────────────────────────────────────┐
│ upper('hello, datalake!') │ ucase('hello, datalake!') │
├───────────────────────────┼───────────────────────────┤
│ HELLO, DATALAKE!          │ HELLO, DATALAKE!          │
└───────────────────────────────────────────────────────┘
```
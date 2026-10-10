---
title: BIN
summary: N のバイナリ値の文字列表現を返します。
---

# BIN

N のバイナリ値の文字列表現を返します。

## 構文 {#syntax}

```sql
BIN(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<expr>`  | 数値。 |

## 戻り値の型 {#return-type}

`VARCHAR`

## 例 {#examples}

```sql
SELECT BIN(12);
+---------+
| BIN(12) |
+---------+
| 1100    |
+---------+
```
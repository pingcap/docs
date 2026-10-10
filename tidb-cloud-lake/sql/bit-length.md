---
title: BIT_LENGTH
summary: 文字列の長さをビット単位で返します。
---

# BIT_LENGTH

文字列の長さをビット単位で返します。

## 構文 {#syntax}

```sql
BIT_LENGTH(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------| ----------- |
| `<expr>`  | 文字列です。 |

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT BIT_LENGTH('Word');
+----------------------------+
| SELECT BIT_LENGTH('Word'); |
+----------------------------+
| 32                         |
+----------------------------+
```
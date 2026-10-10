---
title: ASCII
summary: 文字列 str の最も左の文字の数値を返します。
---

# ASCII

文字列 str の最も左の文字の数値を返します。

## 構文 {#syntax}

```sql
ASCII(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<expr>`  | 文字列。 |

## 戻り値の型 {#return-type}

`TINYINT`

## 例 {#examples}

```sql
SELECT ASCII('2');
+------------+
| ASCII('2') |
+------------+
|         50 |
+------------+
```
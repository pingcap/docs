---
title: REVERSE
summary: 文字の順序を逆にした文字列 str を返します。
---

# REVERSE

文字の順序を逆にした文字列 str を返します。

## 構文 {#syntax}

```sql
REVERSE(<str>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------------|
| `<str>`   | 文字列値。 |

## 戻り値の型 {#return-type}

`VARCHAR`

## 例 {#examples}

```sql
SELECT REVERSE('abc');
+----------------+
| REVERSE('abc') |
+----------------+
| cba            |
+----------------+
```
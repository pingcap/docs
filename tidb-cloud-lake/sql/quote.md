---
title: QUOTE
summary: 文字列をクォートし、SQL 文で適切にエスケープされたデータ値として使用できる結果を生成します。
---

# QUOTE

文字列をクォートし、SQL 文で適切にエスケープされたデータ値として使用できる結果を生成します。

## 構文 {#syntax}

```sql
QUOTE(<str>)
```

## 例 {#examples}

```sql
SELECT QUOTE('Don\'t!');
+-----------------+
| QUOTE('Don't!') |
+-----------------+
| Don\'t!         |
+-----------------+

SELECT QUOTE(NULL);
+-------------+
| QUOTE(NULL) |
+-------------+
|        NULL |
+-------------+
```
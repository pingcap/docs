---
title: HUMANIZE_NUMBER
summary: 読みやすい数値を返します。
---

# HUMANIZE_NUMBER

読みやすい数値を返します。

## 構文 {#syntax}

```sql
HUMANIZE_NUMBER(x);
```

## 引数 {#arguments}

| 引数 | 説明           |
|-----------|----------------------------|
| x         | 数値の大きさ。 |

## 戻り値の型 {#return-type}

String。

## 例 {#examples}

```sql
SELECT HUMANIZE_NUMBER(1000 * 1000)
+-------------------------+
| HUMANIZE_NUMBER((1000 * 1000)) |
+-------------------------+
| 1 million               |
+-------------------------+
```
---
title: REPEAT
summary: 文字列 str を count 回繰り返した文字列を返します。count が 1 未満の場合は空文字列を返します。str または count が NULL の場合は NULL を返します。
---

# REPEAT

文字列 str を count 回繰り返した文字列を返します。count が 1 未満の場合は空文字列を返します。str または count が NULL の場合は NULL を返します。

## 構文 {#syntax}

```sql
REPEAT(<str>, <count>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<str>`   | 文字列です。 |
| `<count>` | 数値です。 |

## 例 {#examples}

```sql
SELECT REPEAT('datalake', 3);
+--------------------------+
| REPEAT('datalake', 3)    |
+--------------------------+
| datalakedatalakedatalake |
+--------------------------+

SELECT REPEAT('datalake', 0);
+-----------------------+
| REPEAT('datalake', 0) |
+-----------------------+
|                       |
+-----------------------+

SELECT REPEAT('datalake', NULL);
+--------------------------+
| REPEAT('datalake', NULL) |
+--------------------------+
|                     NULL |
+--------------------------+
```
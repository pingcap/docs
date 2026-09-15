---
title: QUOTE
summary: 为字符串添加引号，生成可在 SQL 语句中用作正确转义的数据值的结果。
---

# QUOTE

为字符串添加引号，生成可在 SQL 语句中用作正确转义的数据值的结果。

## 语法 {#syntax}

```sql
QUOTE(<str>)
```

## 示例 {#examples}

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
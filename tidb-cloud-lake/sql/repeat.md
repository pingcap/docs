---
title: REPEAT
summary: 返回一个由字符串 str 重复 count 次组成的字符串。如果 count 小于 1，则返回空字符串。如果 str 或 count 为 NULL，则返回 NULL。
---

# REPEAT

返回一个由字符串 str 重复 count 次组成的字符串。如果 count 小于 1，则返回空字符串。如果 str 或 count 为 NULL，则返回 NULL。

## 语法 {#syntax}

```sql
REPEAT(<str>, <count>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<str>`   | 字符串。 |
| `<count>` | 数字。 |

## 示例 {#examples}

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
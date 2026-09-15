---
title: OCTET_LENGTH
summary: OCTET_LENGTH() 是 LENGTH() 的同义词。
---

# OCTET_LENGTH

OCTET_LENGTH() 是 LENGTH() 的同义词。

## 语法 {#syntax}

```sql
OCTET_LENGTH(<str>)
```

## 示例 {#examples}

```sql
SELECT OCTET_LENGTH('datalake');
+--------------------------+
| OCTET_LENGTH('datalake') |
+--------------------------+
|                        8 |
+--------------------------+
```
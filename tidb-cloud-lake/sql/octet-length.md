---
title: OCTET_LENGTH
summary: OCTET_LENGTH() は LENGTH() の同義語です。
---

# OCTET_LENGTH

OCTET_LENGTH() は LENGTH() の同義語です。

## 構文 {#syntax}

```sql
OCTET_LENGTH(<str>)
```

## 例 {#examples}

```sql
SELECT OCTET_LENGTH('datalake');
+--------------------------+
| OCTET_LENGTH('datalake') |
+--------------------------+
|                        8 |
+--------------------------+
```
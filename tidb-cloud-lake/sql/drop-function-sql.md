---
title: DROP FUNCTION
summary: 外部関数を削除します。
---

# DROP FUNCTION

外部関数を削除します。

## 構文 {#syntax}

```sql
DROP FUNCTION [ IF EXISTS ] <function_name>
```

## 例 {#examples}

```sql
DROP FUNCTION a_plus_3;

SELECT a_plus_3(2);
ERROR 1105 (HY000): Code: 2602, Text = Unknown Function a_plus_3 (while in analyze select projection).
```
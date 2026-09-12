---
title: DROP FUNCTION
summary: 删除一个外部函数。
---

# DROP FUNCTION

删除一个外部函数。

## 语法 {#syntax}

```sql
DROP FUNCTION [ IF EXISTS ] <function_name>
```

## 示例 {#examples}

```sql
DROP FUNCTION a_plus_3;

SELECT a_plus_3(2);
ERROR 1105 (HY000): Code: 2602, Text = Unknown Function a_plus_3 (while in analyze select projection).
```
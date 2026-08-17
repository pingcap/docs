---
title: DROP FUNCTION
summary: Learn how to remove an external scalar or table function registration from TiDB Cloud Lake and verify that it is no longer callable.
---

# DROP FUNCTION

Removes an external scalar or table function registration. This statement does not stop or delete the external UDF Server.

## Syntax

```sql
DROP FUNCTION [ IF EXISTS ] <function_name>
```

## Examples

```sql
DROP FUNCTION a_plus_3;

SELECT a_plus_3(2);
ERROR 1105 (HY000): Code: 2602, Text = Unknown Function a_plus_3 (while in analyze select projection).
```

---
title: SHOW CREATE DATABASE
sidebar_position: 2
---

Shows the CREATE DATABASE statement that creates the named database.

## Syntax

```sql
SHOW CREATE DATABASE database_name
```

## Examples

```sql
SHOW CREATE DATABASE default;
+----------+---------------------------+
| Database | Create Database           |
+----------+---------------------------+
| default  | CREATE DATABASE `default` |
+----------+---------------------------+
```
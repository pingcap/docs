---
title: SHOW CREATE DATABASE
summary: 显示用于创建指定数据库的 CREATE DATABASE 语句。
---

# SHOW CREATE DATABASE

显示用于创建指定数据库的 CREATE DATABASE 语句。

## 语法 {#syntax}

```sql
SHOW CREATE DATABASE database_name
```

## 示例 {#examples}

```sql
SHOW CREATE DATABASE default;
+----------+---------------------------+
| Database | Create Database           |
+----------+---------------------------+
| default  | CREATE DATABASE `default` |
+----------+---------------------------+
```
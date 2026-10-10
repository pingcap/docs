---
title: SHOW CREATE DATABASE
summary: 指定したデータベースを作成する CREATE DATABASE 文を表示します。
---

# SHOW CREATE DATABASE

指定したデータベースを作成する CREATE DATABASE 文を表示します。

## 構文 {#syntax}

```sql
SHOW CREATE DATABASE database_name
```

## 例 {#examples}

```sql
SHOW CREATE DATABASE default;
+----------+---------------------------+
| Database | Create Database           |
+----------+---------------------------+
| default  | CREATE DATABASE `default` |
+----------+---------------------------+
```
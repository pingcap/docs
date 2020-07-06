---
title: USER_PRIVILEGES
summary: Learn the `USER_PRIVILEGES` information_schema table.
category: reference
---


# USER_PRIVILEGES

The `USER_PRIVILEGES` table provides information about global privileges. This information comes from the `mysql.user` system table:

{{< copyable "sql" >}}

```sql
desc USER_PRIVILEGES;
```

```
+----------------|--------------|------|------|---------|-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------|--------------|------|------|---------|-------+
| GRANTEE        | varchar(81)  | YES  |      | NULL    |       |
| TABLE_CATALOG  | varchar(512) | YES  |      | NULL    |       |
| PRIVILEGE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| IS_GRANTABLE   | varchar(3)   | YES  |      | NULL    |       |
+----------------|--------------|------|------|---------|-------+
4 rows in set (0.00 sec)
```




---
title: SET ROLE | TiDB SQL Statement Reference
summary: An overview of the usage of SET ROLE for the TiDB database.
category: reference
---

# SET ROLE

The statement `SET ROLE` is used to enable role(s) in current sessiom. User could use privileges of role(s) after enable them.  

## Synopsis

**SetRoleStmt:**

![SetRoleStmt](/media/sqlgram/SetRoleStmt.png)

**SetRoleOpt:**

![SetRoleOpt](/media/sqlgram/SetRoleOpt.png)

**SetDefaultRoleOpt:**

![SetDefaultRoleOpt](/media/sqlgram/SetDefaultRoleOpt.png)

## Examples

Create a user `'u1'@'%'` and three roles: `'r1'@'%'`, `'r2'@'%'` and `'r3'@'%'`.
Grant roles to `'u1'@'%'` and set `'r1'@'%'` as defualt role of `'u1'@'%'`.

{{< copyable "sql" >}}

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%'; 
SET DEFAULT ROLE 'r1' TO 'u1'@'%'; 
```

Login as `'u1'@'%'` and execute `SET ROLE` statement to enable all roles.

{{< copyable "sql" >}}

```sql
SET ROLE ALL;
SELECT CURRENT_ROLE();
```

```
+----------------------------+
| CURRENT_ROLE()             |
+----------------------------+
| `r1`@`%`,`r2`@`%`,`r3`@`%` |
+----------------------------+
1 row in set (0.000 sec)
```

Execute `SET ROLE` to enable `'r2'` and `'r3'`.

{{< copyable "sql" >}}

```sql
SET ROLE 'r2', 'r3';
SELECT CURRENT_ROLE();
```

```
+-------------------+
| CURRENT_ROLE()    |
+-------------------+
| `r2`@`%`,`r3`@`%` |
+-------------------+
1 row in set (0.000 sec)
```

Execute `SET ROLE` to enable default role(s).

{{< copyable "sql" >}}

```sql
SET ROLE DEFAULT;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| `r1`@`%`       |
+----------------+
1 row in set (0.000 sec)
```

Execute `SET ROLE` to cancel all enable role(s).

{{< copyable "sql" >}}

```sql
SET ROLE NONE;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
|                |
+----------------+
1 row in set (0.000 sec)
```

## See also

* [Role-Based Access Control](/role-based-access-control.md)
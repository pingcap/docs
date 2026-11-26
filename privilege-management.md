---
title: 权限管理
summary: 了解如何管理权限。
---

# 权限管理

TiDB 支持 MySQL 5.7 的权限管理系统，包括其语法和权限类型。同时也支持以下 MySQL 8.0 特性：

* SQL Roles，自 TiDB 3.0 起支持。
* Dynamic privileges，自 TiDB 5.1 起支持。

本文介绍与权限相关的 TiDB 操作、执行 TiDB 操作所需的权限，以及权限系统的实现。

## 与权限相关的操作 {#privilege-related-operations}

### 授予权限 {#grant-privileges}

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 语句用于向用户账户授予权限。

例如，使用以下语句为 `xxx` 用户授予对 `test` 数据库的读权限。

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

使用以下语句为 `xxx` 用户授予所有数据库上的所有权限：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

从 v8.5.6 开始，TiDB 支持与 MySQL 兼容的列级权限管理机制。你可以在指定表的特定列上授予或回收 `SELECT`、`INSERT`、`UPDATE` 和 `REFERENCES` 权限。更多信息，参见[列级权限管理](/column-privilege-management.md)。

默认情况下，如果 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 语句中指定的用户不存在，则会返回错误。此行为取决于是否指定了 [SQL mode](/system-variables.md#sql_mode) `NO_AUTO_CREATE_USER`：

```sql
SET sql_mode=DEFAULT;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT @@sql_mode;
```

```
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                                                |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM mysql.user WHERE user='idontexist';
```

```
Empty set (0.00 sec)
```

```sql
GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
```

```
ERROR 1105 (HY000): You are not allowed to create a user with GRANT
```

```sql
SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
```

```
Empty set (0.00 sec)
```

在下面的示例中，由于未设置 SQL Mode `NO_AUTO_CREATE_USER`，用户 `idontexist` 会被自动创建，且密码为空。**不建议**这样做，因为这会带来安全风险：如果用户名拼写错误，就会创建一个密码为空的新用户：

```sql
SET @@sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT @@sql_mode;
```

```
+-----------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                            |
+-----------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION |
+-----------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM mysql.user WHERE user='idontexist';
```

```
Empty set (0.00 sec)
```

```sql
GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
```

```
Query OK, 1 row affected (0.05 sec)
```

```sql
SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
```

```
+------------+------+-----------------------+
| user       | host | authentication_string |
+------------+------+-----------------------+
| idontexist | %    |                       |
+------------+------+-----------------------+
1 row in set (0.01 sec)
```

你可以在 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 中使用模糊匹配，为数据库授予权限。

```sql
GRANT ALL PRIVILEGES ON `te%`.* TO genius;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT user,host,db FROM mysql.db WHERE user='genius';
```

```
+--------|------|-----+
| user   | host | db  |
+--------|------|-----+
| genius | %    | te% |
+--------|------|-----+
1 row in set (0.00 sec)
```

在此示例中，由于 `te%` 中包含 `%`，因此所有以 `te` 开头的数据库都会被授予该权限。

### 回收权限 {#revoke-privileges}

[`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md) 语句使系统管理员能够从用户账户中回收权限。

`REVOKE` 语句与 `GRANT` 语句相对应：

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **Note:**
>
> 要回收权限，你需要使用精确匹配。如果找不到匹配结果，将显示错误：

```sql
REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
```

```
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

关于模糊匹配、转义、字符串和标识符：

```sql
GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
```

```
Query OK, 0 rows affected (0.00 sec)
```

此示例使用精确匹配来查找名为 `te%` 的数据库。注意，`%` 使用了 `\` 转义字符，因此 `%` 不会被视为通配符。

字符串使用单引号 (`''`) 括起来，而标识符使用反引号 (``) 括起来。请看下面的区别：

```sql
GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
```

```
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1
```

```sql
GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
```

```
Query OK, 0 rows affected (0.00 sec)
```

如果要使用特殊关键字作为表名，请使用反引号 (``) 将其括起来。例如：

```sql
CREATE TABLE `select` (id int);
```

```
Query OK, 0 rows affected (0.27 sec)
```

### 查看授予用户的权限 {#check-privileges-granted-to-users}

你可以使用 `SHOW GRANTS` 语句查看授予用户的权限。例如：

```sql
SHOW GRANTS; -- 显示当前用户的权限
```

```
+-------------------------------------------------------------+
| Grants for User                                             |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
+-------------------------------------------------------------+
```

```sql
SHOW GRANTS FOR 'root'@'%'; -- 显示特定用户的权限
```

例如，创建用户 `rw_user@192.168.%`，并授予该用户 `test.write_table` 表的写权限和全局读权限。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

查看 `rw_user@192.168.%` 用户的权限：

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;
```

```
+------------------------------------------------------------------+
| Grants for rw_user@192.168.%                                     |
+------------------------------------------------------------------+
| GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
| GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
+------------------------------------------------------------------+
```

### 动态权限 {#dynamic-privileges}

从 v5.1 起，TiDB 支持动态权限，这是借鉴自 MySQL 8.0 的特性。动态权限旨在通过对某些操作实现更细粒度的访问控制，来替代 `SUPER` 权限。例如，使用动态权限，系统管理员可以创建一个仅能执行 `BACKUP` 和 `RESTORE` 操作的用户账户。

动态权限包括：

* `BACKUP_ADMIN`
* `RESTORE_ADMIN`
* `SYSTEM_USER`
* `SYSTEM_VARIABLES_ADMIN`
* `ROLE_ADMIN`
* `CONNECTION_ADMIN`
* `PLACEMENT_ADMIN` 允许权限拥有者创建、修改和删除放置策略。
* `DASHBOARD_CLIENT` 允许权限拥有者登录 TiDB Dashboard。
* `RESTRICTED_TABLES_ADMIN` 当启用 SEM 时，允许权限拥有者查看系统表。
* `RESTRICTED_STATUS_ADMIN` 当启用 SEM 时，允许权限拥有者在 [`SHOW [GLOBAL|SESSION] STATUS`](/sql-statements/sql-statement-show-status.md) 中查看所有状态变量。
* `RESTRICTED_VARIABLES_ADMIN` 当启用 SEM 时，允许权限拥有者查看所有系统变量。
* `RESTRICTED_USER_ADMIN` 当启用 SEM 时，禁止 SUPER 用户回收拥有该权限的用户的访问权限。
* `RESTRICTED_CONNECTION_ADMIN` 允许权限拥有者终止 `RESTRICTED_USER_ADMIN` 用户的连接。此权限影响 `KILL` 和 `KILL TIDB` 语句。
* `RESTRICTED_REPLICA_WRITER_ADMIN` 允许权限拥有者在 TiDB 集群启用只读模式时，不受影响地执行写入或更新操作。详情参见 [`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520)。
* `AUDIT_ADMIN` 在 [Security Enhanced Mode (SEM)](https://docs.pingcap.com/tidb/stable/glossary/#security-enhanced-mode-sem) 未启用时，允许管理数据库审计日志，包括修改与审计日志相关的系统变量、手动轮转审计日志、创建或删除审计日志过滤器，以及创建、删除、启用或禁用审计日志过滤规则。此权限仅在提供数据库审计日志功能的产品中可用，包括 TiDB Self-Managed Enterprise Edition、{{{ .dedicated }}}、{{{ .premium }}} 和 {{{ .essential }}}。[{{{ .essential }}} 的数据库审计日志功能](https://docs.pingcap.com/tidbcloud/essential-database-audit-logging/?plan=essential)目前处于 Private Preview 阶段，需要申请访问。{{{ .starter }}} 不支持数据库审计日志。
* `RESTRICTED_AUDIT_ADMIN` 在 SEM 启用时，允许管理数据库审计日志。其管理的操作范围和适用产品与 `AUDIT_ADMIN` 相同。

要查看完整的动态权限列表，请执行 `SHOW PRIVILEGES` 语句。由于允许插件添加新权限，因此可分配的权限列表可能因你的 TiDB 安装而异。

## `SUPER` 权限 {#super-privilege}

- `SUPER` 权限允许用户执行几乎所有操作。默认情况下，只有 `root` 用户被授予此权限。将此权限授予其他用户时请谨慎。
- `SUPER` 权限在 [MySQL 8.0 中被视为已弃用](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#dynamic-privileges-migration-from-super)，可以用[动态权限](#dynamic-privileges)替代，以提供更细粒度的访问控制。

## TiDB 操作所需的权限 {#privileges-required-for-tidb-operations}

你可以在 `INFORMATION_SCHEMA.USER_PRIVILEGES` 表中查看 TiDB 用户的权限。例如：

```sql
SELECT * FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE grantee = "'root'@'%'";
```

```
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | Select                  | YES          |
| 'root'@'%' | def           | Insert                  | YES          |
| 'root'@'%' | def           | Update                  | YES          |
| 'root'@'%' | def           | Delete                  | YES          |
| 'root'@'%' | def           | Create                  | YES          |
| 'root'@'%' | def           | Drop                    | YES          |
| 'root'@'%' | def           | Process                 | YES          |
| 'root'@'%' | def           | References              | YES          |
| 'root'@'%' | def           | Alter                   | YES          |
| 'root'@'%' | def           | Show Databases          | YES          |
| 'root'@'%' | def           | Super                   | YES          |
| 'root'@'%' | def           | Execute                 | YES          |
| 'root'@'%' | def           | Index                   | YES          |
| 'root'@'%' | def           | Create User             | YES          |
| 'root'@'%' | def           | Create Tablespace       | YES          |
| 'root'@'%' | def           | Trigger                 | YES          |
| 'root'@'%' | def           | Create View             | YES          |
| 'root'@'%' | def           | Show View               | YES          |
| 'root'@'%' | def           | Create Role             | YES          |
| 'root'@'%' | def           | Drop Role               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | SHUTDOWN                | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | CONFIG                  | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
31 rows in set (0.00 sec)
```

### ALTER {#alter}

- 对于所有 `ALTER` 语句，用户必须拥有相应表的 `ALTER` 权限。
- 对于除 `ALTER...DROP` 和 `ALTER...RENAME TO` 之外的语句，用户必须拥有相应表的 `INSERT` 和 `CREATE` 权限。
- 对于 `ALTER...DROP` 语句，用户必须拥有相应表的 `DROP` 权限。
- 对于 `ALTER...RENAME TO` 语句，用户必须拥有重命名前表的 `ALTER` 和 `DROP` 权限，以及重命名后表的 `CREATE` 和 `INSERT` 权限。

> **Note:**
>
> 在 MySQL 5.7 文档中，用户对表执行 `ALTER` 操作需要 `INSERT` 和 `CREATE` 权限。但实际上，在 MySQL 5.7.25 中，这种情况下只需要 `ALTER` 权限。目前，TiDB 中的 `ALTER` 权限与 MySQL 的实际行为保持一致。

### BACKUP {#backup}

需要 `SUPER` 或 `BACKUP_ADMIN` 权限。

### CANCEL IMPORT JOB {#cancel-import-job}

取消其他用户创建的作业需要 `SUPER` 权限。否则，只能取消当前用户创建的作业。

### CREATE DATABASE {#create-database}

需要数据库的 `CREATE` 权限。

### CREATE INDEX {#create-index}

需要表的 `INDEX` 权限。

### CREATE TABLE {#create-table}

需要表的 `CREATE` 权限。

执行 `CREATE TABLE...LIKE...` 语句时，需要该表的 `SELECT` 权限。

### CREATE VIEW {#create-view}

需要 `CREATE VIEW` 权限。

> **Note:**
>
> 如果当前用户不是创建 View 的用户，则同时需要 `CREATE VIEW` 和 `SUPER` 权限。

### DROP DATABASE {#drop-database}

需要数据库的 `DROP` 权限。

### DROP INDEX {#drop-index}

需要表的 `INDEX` 权限。

### DROP TABLES {#drop-tables}

需要表的 `DROP` 权限。

### IMPORT INTO {#import-into}

需要目标表的 `SELECT`、`UPDATE`、`INSERT`、`DELETE` 和 `ALTER` 权限。若要导入存储在 TiDB 本地的文件，还需要 `FILE` 权限。

### LOAD DATA {#load-data}

需要表的 `INSERT` 权限。使用 `REPLACE INTO` 时，还需要 `DELETE` 权限。

### TRUNCATE TABLE {#truncate-table}

需要表的 `DROP` 权限。

### RENAME TABLE {#rename-table}

重命名前需要原表的 `ALTER` 和 `DROP` 权限，重命名后需要新表的 `CREATE` 和 `INSERT` 权限。

### ANALYZE TABLE {#analyze-table}

需要表的 `INSERT` 和 `SELECT` 权限。

### LOCK STATS {#lock-stats}

需要表的 `INSERT` 和 `SELECT` 权限。

### UNLOCK STATS {#unlock-stats}

需要表的 `INSERT` 和 `SELECT` 权限。

### SHOW {#show}

`SHOW CREATE TABLE` 需要该表上的任意一种权限。

`SHOW CREATE VIEW` 需要 `SHOW VIEW` 权限。

`SHOW GRANTS` 需要 `mysql` 数据库的 `SELECT` 权限。如果目标用户是当前用户，则 `SHOW GRANTS` 不需要任何权限。

`SHOW PROCESSLIST` 需要 `PROCESS` 权限，才能显示属于其他用户的连接。

`SHOW IMPORT JOB` 需要 `SUPER` 权限，才能显示其他用户的连接。否则，只显示当前用户创建的作业。

`SHOW STATS_LOCKED` 需要 `mysql.stats_table_locked` 表的 `SELECT` 权限。

### CREATE ROLE/USER {#create-role-user}

`CREATE ROLE` 需要 `CREATE ROLE` 权限。

`CREATE USER` 需要 `CREATE USER` 权限。

### DROP ROLE/USER {#drop-role-user}

`DROP ROLE` 需要 `DROP ROLE` 权限。

`DROP USER` 需要 `CREATE USER` 权限。

### ALTER USER {#alter-user}

需要 `CREATE USER` 权限。

### GRANT {#grant}

需要 `GRANT` 语句所授予权限对应的 `GRANT` 权限。

若要隐式创建用户，还需要额外的 `CREATE USER` 权限。

`GRANT ROLE` 需要 `SUPER` 或 `ROLE_ADMIN` 权限。

### REVOKE {#revoke}

需要 `GRANT` 权限以及 `REVOKE` 语句所针对的那些权限。

`REVOKE ROLE` 需要 `SUPER` 或 `ROLE_ADMIN` 权限。

### SET GLOBAL {#set-global}

设置全局变量需要 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限。

### ADMIN {#admin}

需要 `SUPER` 权限。

### SET DEFAULT ROLE {#set-default-role}

需要 `SUPER` 权限。

### KILL {#kill}

终止其他用户会话需要 `SUPER` 或 `CONNECTION_ADMIN` 权限。

### CREATE RESOURCE GROUP {#create-resource-group}

需要 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限。

### ALTER RESOURCE GROUP {#alter-resource-group}

需要 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限。

### DROP RESOURCE GROUP {#drop-resource-group}

需要 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限。

### CALIBRATE RESOURCE {#calibrate-resource}

需要 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限。

### SET RESOURCE GROUP {#set-resource-group}

当系统变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) 设置为 `ON` 时，执行该语句需要具有 `SUPER`、`RESOURCE_GROUP_ADMIN` 或 `RESOURCE_GROUP_USER` 权限。

## 权限系统的实现 {#implementation-of-the-privilege-system}

### 权限表 {#privilege-table}

以下 [`mysql` 系统表](/mysql-schema/mysql-schema.md) 比较特殊，因为所有与权限相关的数据都存储在这些表中：

- `mysql.user`（用户账户、全局权限）
- `mysql.db`（数据库级别权限）
- `mysql.tables_priv`（表级别权限）
- `mysql.columns_priv`（列级别权限；从 v8.5.6 开始支持）

这些表包含数据的生效范围和权限信息。例如，在 `mysql.user` 表中：

```sql
SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
```

```
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

在这条记录中，`Host` 和 `User` 表示来自任意主机（`%`）的 `root` 用户发起的连接请求可以被接受。`Select_priv` 和 `Insert_priv` 表示该用户具有全局 `Select` 和 `Insert` 权限。`mysql.user` 表中的生效范围是全局。

`mysql.db` 中的 `Host` 和 `User` 用于确定用户可以访问哪些数据库。其生效范围是数据库。

> **Note:**
>
> 建议仅通过提供的语法（如 `GRANT`、`CREATE USER` 和 `DROP USER`）来修改权限表。直接编辑底层权限表不会自动修改权限缓存，在执行 `FLUSH PRIVILEGES` 之前，可能会导致不可预测的行为。

### 连接验证 {#connection-verification}

当客户端发送连接请求时，TiDB server 会对登录操作进行验证。TiDB server 首先检查 `mysql.user` 表。如果存在一条 `User` 和 `Host` 与连接请求匹配的记录，TiDB server 接着会验证 `authentication_string`。

用户身份基于两部分信息：发起连接的主机 `Host` 和用户名 `User`。如果用户名非空，则必须对用户名进行精确匹配。

`User`+`Host` 可能会匹配 `user` 表中的多行。为处理这种场景，`user` 表中的行会先进行排序。客户端连接时，会逐行检查这些记录；第一条匹配的记录将用于验证。排序时，`Host` 的优先级高于 `User`。

### 请求验证 {#request-verification}

当连接成功后，请求验证过程会检查该操作是否具有相应权限。

对于与数据库相关的请求（`INSERT`、`UPDATE`），请求验证过程会先检查 `mysql.user` 表中的用户全局权限。如果已被授予该权限，则可以直接访问；否则，会继续检查 `mysql.db` 表。

`user` 表中的权限是全局权限，与默认数据库无关。例如，`user` 表中的 `DELETE` 权限可应用于任何行、表或数据库。

在 `db` 表中，空用户用于匹配匿名用户名。`User` 列不允许使用通配符。`Host` 和 `Db` 列的值可以使用 `%` 和 `_`，以进行模式匹配。

`user` 和 `db` 表中的数据在加载到内存时也会进行排序。

`tables_priv` 和 `columns_priv` 中 `%` 的使用方式类似，但 `Db`、`Table_name` 和 `Column_name` 列的值不能包含 `%`。这些表在加载时的排序方式也类似。

### 生效时间 {#time-of-effect}

当 TiDB 启动时，会将部分权限检查表加载到内存中，随后使用缓存的数据来验证权限。执行 `GRANT`、`REVOKE`、`CREATE USER`、`DROP USER` 等权限管理语句后，会立即生效。

使用 `INSERT`、`DELETE`、`UPDATE` 等语句手动修改 `mysql.user` 等表时，不会立即生效。这种行为与 MySQL 兼容，可以通过执行 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) 语句来更新权限缓存。

---
title: 权限
summary: 权限是执行某项操作的许可。用户必须具有特定权限，才能在 {{{ .lake }}} 中执行特定操作。例如，查询表时，用户需要具有该表的 `SELECT` 权限。类似地，要读取 stage 中的数据集，用户必须具有 `READ` 权限。
---

# 权限

权限是执行某项操作的许可。用户必须具有特定权限，才能在 {{{ .lake }}} 中执行特定操作。例如，查询表时，用户需要具有该表的 `SELECT` 权限。类似地，要读取 stage 中的数据集，用户必须具有 `READ` 权限。

在 {{{ .lake }}} 中，权限授予给角色。用户通过分配给他们的角色获得权限。

![Alt text](/media/tidb-cloud-lake/access-control-2.png)

## 管理权限 {#managing-privileges}

要管理角色的权限，请使用以下命令：

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [REVOKE](/tidb-cloud-lake/sql/revoke.md)
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

### 向角色授予权限 {#granting-privileges-to-roles}

要授予权限，请先创建一个角色，将权限授予该角色，然后再将该角色授予需要该权限的用户。在以下示例中，首先创建了一个名为 'writer' 的新角色，并向其授予 'default' schema 中对象的所有权限。随后，创建新用户 'david'，密码为 'abc123'，并将 'writer' 角色授予 'david'。最后，显示 'writer' 已被授予的权限。

```sql title='Example:'
-- Create a new role named 'writer'
CREATE ROLE writer;

-- Grant all privileges on all objects in the 'default' schema to the role 'writer'
GRANT ALL ON default.* TO ROLE writer;

-- Create a new user named 'david' with the password 'abc123' and set the default role
CREATE USER david IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'writer';

-- Grant the role 'writer' to the user 'david'
GRANT ROLE writer TO david;

-- Show the granted privileges for the role 'writer'
SHOW GRANTS FOR ROLE writer;

┌───────────────────────────────────────────────────────┐
│                      Grants                           │
├───────────────────────────────────────────────────────┤
│ GRANT ALL ON 'default'.'default'.* TO ROLE 'writer'   │
└───────────────────────────────────────────────────────┘
```

### 从角色中回收权限 {#revoking-privileges-from-roles}

在访问控制的上下文中，权限是从角色中回收的。在以下示例中，我们从角色 'writer' 中回收其在 'default' schema 中所有对象上的全部权限，然后显示角色 'writer' 已被授予的权限：

```sql title='Example (Continued):'
-- Revoke all privileges on all objects in the 'default' schema from role 'writer'
REVOKE ALL ON default.* FROM ROLE writer;

-- Show the granted privileges for the role 'writer'
SHOW GRANTS FOR ROLE writer;
```

## 访问控制权限 {#access-control-privileges}

{{{ .lake }}} 提供了一系列权限，使你能够对数据库对象进行细粒度控制。{{{ .lake }}} 权限可分为以下类型：

- 全局权限：这组权限适用于整个数据库管理系统，而不是系统中的特定对象。全局权限授予会影响数据库整体功能和管理的操作，例如创建或删除数据库、管理用户和角色，以及修改系统级设置。有关包含哪些权限，请参见[全局权限](#global-privileges)。

- 对象特定权限：对象特定权限包含不同的权限集，每一种都适用于特定的数据库对象。其中包括：
    - [表权限](#table-privileges)
    - [视图权限](#view-privileges)
    - [数据库权限](#database-privileges)
    - [会话策略权限](#session-policy-privileges)
    - [Stage 权限](#stage-privileges)
    - [UDF 权限](#udf-privileges)
    - [序列权限](#sequence-privileges)
    - [连接权限](#connection-privileges)
    - [存储过程权限](#procedure-privileges)
    - [Catalog 权限](#catalog-privileges)
    - [Share 权限](#share-privileges)

### 所有权限 {#all-privileges}

| 权限         | 对象类型                   | 描述                                                                                                                                        |
|:------------------|:------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| ALL               | 所有                           | 授予指定对象类型的所有权限。                                                                                                                       |
| APPLY MASKING POLICY | 全局, Masking Policy     | 附加、分离、描述或删除 masking policy。当在 *.* 上授予时，被授权者可以管理任何 masking policy。                                                     |
| APPLY ROW ACCESS POLICY | 全局, Row Access Policy | 向表添加或移除行访问策略，并允许对任何策略执行 DESCRIBE/DROP 操作。当在 *.* 上授予时，被授权者可以管理所有行访问策略。 |
| ALTER             | 全局, 数据库, 表, 视图 | 修改数据库、表、用户或 UDF。                                                                                                                       |
| CREATE            | 全局, 表                 | 创建表或 UDF。                                                                                                                                     |
| CREATE DATABASE   | 全局                        | 创建数据库或 UDF。                                                                                                                                 |
| CREATE WAREHOUSE  | 全局                        | 创建计算集群。                                                                                                                                     |
| CREATE CONNECTION | 全局                        | 创建连接。                                                                                                                                         |
| CREATE SEQUENCE   | 全局                        | 创建序列。                                                                                                                                         |
| CREATE PROCEDURE  | PROCEDURE                     | 创建存储过程。                                                                                                                                     |
| CREATE MASKING POLICY | 全局                    | 创建 masking policy。                                                                                                                              |
| CREATE ROW ACCESS POLICY | 全局                 | 创建行访问策略。                                                                                                                                   |
| DELETE            | 表                         | 删除表中的行或截断表中的行。                                                                                                                       |
| DROP              | 全局, 数据库, 表, 视图 | 删除数据库、表、视图或 UDF。撤销删除表。                                                                                                           |
| INSERT            | 表                         | 向表中插入行。                                                                                                                                     |
| SELECT            | 数据库, 表               | 从表中选择行。显示或使用数据库。                                                                                                                   |
| UPDATE            | 表                         | 修改表中的行。                                                                                                                                     |
| GRANT             | 全局                        | 向角色授予 / 从角色回收权限。                                                                                                                      |
| SUPER             | 全局, 表                 | 终止查询。设置全局配置。优化表。分析表。操作 stage（列出 stages、创建 stage、删除 stage）、catalog 或 share。 |
| USAGE             | 全局                        | “无权限”的同义词。                                                                                                                                 |
| CREATE ROLE       | 全局                        | 创建角色。                                                                                                                                         |
| DROP ROLE         | 全局                        | 删除角色。                                                                                                                                         |
| CREATE USER       | 全局                        | 创建 SQL 用户。                                                                                                                                    |
| DROP USER         | 全局                        | 删除 SQL 用户。                                                                                                                                    |
| WRITE             | Stage                         | 向 stage 写入。                                                                                                                                    |
| READ              | Stage                         | 读取 stage。                                                                                                                                       |
| USAGE             | UDF                           | 使用 udf。                                                                                                                                         |
| ACCESS CONNECTION | CONNECTION                    | 访问连接。                                                                                                                                         |
| ACCESS SEQUENCE   | SEQUENCE                      | 访问序列。                                                                                                                                         |
| ACCESS PROCEDURE  | PROCEDURE                     | 访问存储过程。                                                                                                                                     |

### 全局权限 {#global-privileges}

| 权限         | 描述                                                                                                       |
|:------------------|:------------------------------------------------------------------------------------------------------------------|
| ALL               | 授予指定对象类型的所有权限。                                                                                      |
| ALTER             | 添加或删除表列。修改 cluster key。对表重新执行 cluster。                                                          |
| CREATEROLE        | 创建角色。                                                                                                        |
| CREAT DATABASE    | 创建 DATABASE。                                                                                                   |
| CREATE WAREHOUSE  | 创建 WAREHOUSE。                                                                                                  |
| CREATE CONNECTION | 创建 CONNECTION。                                                                                                 |
| DROPUSER          | 删除用户。                                                                                                        |
| CREATEUSER        | 创建用户。                                                                                                        |
| DROPROLE          | 删除角色。                                                                                                        |
| SUPER             | 终止查询。设置或取消设置某项设置。操作 stage、catalog 或 share。调用函数。将 COPY INTO 到 stage。                |
| USAGE             | 仅连接到 {{{ .lake }}} 查询。                                                                                     |
| CREATE            | 创建 UDF。                                                                                                        |
| DROP              | 删除 UDF。                                                                                                        |
| ALTER             | 修改 UDF。修改 SQL 用户。                                                                                         |

### 表权限 {#table-privileges}

| 权限 | 描述                                                                                                      |
|:----------|:-----------------------------------------------------------------------------------------------------------------|
| ALL       | 授予指定对象类型的所有权限。                                                                                     |
| ALTER     | 添加或删除表列。修改 cluster key。对表重新执行 cluster。                                                         |
| CREATE    | 创建表。                                                                                                         |
| DELETE    | 删除表中的行。截断表。                                                                                           |
| DROP      | 删除或撤销删除表。恢复最近删除版本的表。                                                                         |
| INSERT    | 向表中插入行。COPY INTO 到表。                                                                                   |
| SELECT    | 从表中选择行。SHOW CREATE 表。DESCRIBE 表。                                                                      |
| UPDATE    | 修改表中的行。                                                                                                   |
| SUPER     | 优化或分析表。                                                                                                   |
| OWNERSHIP | 授予对数据库的完全控制权。任一时刻，特定对象上的此权限只能由单个角色持有。                                       |

### 视图权限 {#view-privileges}

| 权限 | 描述                                                            |
|:----------|:-----------------------------------------------------------------------|
| ALL       | 授予指定对象类型的所有权限                                             |
| ALTER     | 创建或删除视图。使用另一个 QUERY 修改现有视图。                        |
| DROP      | 删除视图。                                                             |

### 数据库权限 {#database-privileges}

请注意，一旦你对数据库具有以下任一权限，或对该数据库中的某个表具有任意权限，就可以使用 [USE DATABASE](/tidb-cloud-lake/sql/use-database.md) 命令来指定数据库。

| 权限 | 描述                                                                                                      |
|:----------|:-----------------------------------------------------------------------------------------------------------------|
| ALTER     | 重命名数据库。                                                                                                   |
| DROP      | 删除或撤销删除数据库。恢复最近删除版本的数据库。                                                                 |
| SELECT    | SHOW CREATE 数据库。                                                                                             |
| OWNERSHIP | 授予对数据库的完全控制权。任一时刻，特定对象上的此权限只能由单个角色持有。                                       |
| USAGE     | 允许使用 `USE <database>` 进入数据库，而不授予对其中任何对象的访问权限。                                         |

> Note:
>
> 1. 如果某个角色拥有数据库，则该角色可以访问该数据库中的所有表。

### 会话策略权限 {#session-policy-privileges}

| Privilege | Description |
| :--                 | :--                  |
| SUPER       |    终止查询。设置或取消设置某项设置。 |
| ALL   |  授予指定对象类型的所有权限。 |

### Stage 权限 {#stage-privileges}

| 权限 | 描述                                                                                                   |
|:----------|:--------------------------------------------------------------------------------------------------------------|
| WRITE     | 向 stage 写入。例如，copy into 到 stage、presign upload 或删除 stage                         |
| READ      | 读取 stage。例如，列出 stage、查询 stage、从 stage copy into 到表、presign download              |
| ALL       | 授予指定对象类型的 READ、WRITE 权限。                                                  |
| OWNERSHIP | 授予对 stage 的完全控制权。任一时刻，特定对象上的此权限只能由单个角色持有。 |

> Note:
>
> 1. 不检查 external location auth。

### UDF 权限 {#udf-privileges}

| 权限 | 描述                                                                                                 |
|:----------|:------------------------------------------------------------------------------------------------------------|
| USAGE     | 可以使用 UDF。例如，copy into 一个 stage、presign upload                                                   |
| ALL       | 为指定对象类型授予 READ、WRITE 权限。                                                                        |
| OWNERSHIP | 授予对 UDF 的完全控制权。在任意时刻，特定对象上的此权限只能由单个角色持有。                                  |

> 注意：
>
> 1. 如果 udf 已经被 constant fold，则不检查其 auth。
> 2. 如果 udf 是 insert 中的一个值，则不检查其 auth。

### Catalog 权限 {#catalog-privileges}

| 权限 | 描述                                              |
|:----------|:---------------------------------------------------------|
| SUPER     | SHOW CREATE catalog。创建或删除 catalog。                |
| ALL       | 为指定对象类型授予所有权限。                             |

### Share 权限 {#share-privileges}

可以使用相同的 SQL 权限模型（`GRANT`/`REVOKE`）对 share 对象授予和（权限）回收 share 权限。

### Connection 权限 {#connection-privileges}

| 权限         | 描述                                                                                                        |
|:------------------|:-------------------------------------------------------------------------------------------------------------------|
| Access Connection | 可以访问 Connection。                                                                                              |
| ALL               | 为指定对象类型授予访问 Connection 权限。                                                                        |
| OWNERSHIP         | 授予对 Connection 的完全控制权。在任意时刻，特定对象上的此权限只能由单个角色持有。                                |

### Sequence 权限 {#sequence-privileges}

| 权限       | 描述                                                                                                      |
|:----------------|:-----------------------------------------------------------------------------------------------------------------|
| Access Sequence | 可以访问 Sequence。（例如：Drop、Desc）                                                                          |
| ALL             | 为指定对象类型授予访问 Sequence 权限。                                                                        |
| OWNERSHIP       | 授予对 Sequence 的完全控制权。在任意时刻，特定对象上的此权限只能由单个角色持有。                                 |

### Procedure 权限 {#procedure-privileges}

| 权限        | 描述                                                                                                       |
|:-----------------|:------------------------------------------------------------------------------------------------------------------|
| Access Procedure | 可以访问 Procedure。（例如：Drop、Call、Desc）                                                                    |
| ALL              | 为指定对象类型授予访问 Procedure 权限。                                                                       |
| OWNERSHIP        | 授予对 Procedure 的完全控制权。在任意时刻，特定对象上的此权限只能由单个角色持有。                                |

### Masking Policy 权限 {#masking-policy-privileges}

除了全局 `CREATE MASKING POLICY` 和 `APPLY MASKING POLICY` 权限外，还可以为单个 masking policy 授予访问权限：

| 权限 | 描述                                                                                                                           |
|:----------|:--------------------------------------------------------------------------------------------------------------------------------------|
| APPLY     | 将 masking policy 附加到列或从列中分离，并允许对该 policy 执行 DESC/DROP 操作。                                                       |
| OWNERSHIP | 授予对 masking policy 的完全控制权。{{{ .lake }}} 会将 OWNERSHIP 授予创建该 policy 的角色，并在 policy 被删除时自动（权限）回收该权限。 |

### Row Access Policy 权限 {#row-access-policy-privileges}

Row access policy 采用相同的治理模型。除了全局 `CREATE ROW ACCESS POLICY` 和 `APPLY ROW ACCESS POLICY` 权限外，还可以在需要时按 policy 授予访问权限：

| 权限 | 描述                                                                                                                                        |
|:----------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| APPLY     | 将 row access policy 添加到表中或从表中移除，并允许对该 policy 执行 DESC/DROP 操作。                                                              |
| OWNERSHIP | 授予对 row access policy 的完全控制权。{{{ .lake }}} 会将 OWNERSHIP 授予创建者角色，并在 policy 被删除时自动（权限）回收该权限。 |

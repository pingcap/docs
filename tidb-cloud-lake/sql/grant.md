---
title: GRANT
summary: 为特定数据库对象授予权限、角色和所有权。这包括。
---

# GRANT

为特定数据库对象授予权限、角色和所有权。这包括：

- 向角色授予权限。
- 将角色分配给用户或其他角色。
- 将所有权转移给角色。

另请参阅：

- [REVOKE](/tidb-cloud-lake/sql/revoke.md)
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

> 使用 `GRANT` 修改权限或角色后，运行 [SYSTEM FLUSH PRIVILEGES](/tidb-cloud-lake/guides/privileges.md) 以立即将更新广播到每个查询节点。

## 语法 {#syntax}

### 授予权限 {#granting-privileges}

要了解什么是权限及其工作方式，请参阅 [权限](/tidb-cloud-lake/guides/privileges.md)。

> **注意：**
>
> 会创建所有权对象的 CREATE 类权限不能直接授予给用户。这些权限必须先授予给角色，然后再将该角色分配给用户。这包括：
>
> - CREATE
> - CREATE DATABASE
> - CREATE WAREHOUSE
> - CREATE CONNECTION
> - CREATE SEQUENCE
> - CREATE PROCEDURE
> - CREATE MASKING POLICY
> - CREATE ROW ACCESS POLICY
>
> 由于 `ALL` 包含这些 CREATE 权限，因此 `GRANT ALL ... TO USER` 也会失败。例如，`GRANT ALL ON *.* TO USER u1` 或 `GRANT CREATE DATABASE ON *.* TO USER u1` 都会失败。请改用：
>
> ```sql
> GRANT ALL ON *.* TO ROLE r1;
> GRANT ROLE r1 TO USER u1;
> ```

```sql
GRANT {
        schemaObjectPrivileges | ALL [ PRIVILEGES ] ON <privileges_level>
      }
TO ROLE <role_name>
```

其中：

```sql
schemaObjectPrivileges ::=
-- For TABLE
  { SELECT | INSERT }

-- For SCHEMA
  { CREATE | DROP | ALTER }

-- For USER
  { CREATE USER }

-- For ROLE
  { CREATE ROLE}

-- For STAGE
  { READ, WRITE }

-- For UDF
  { USAGE }

-- For MASKING POLICY (account-level privileges)
  { CREATE MASKING POLICY | APPLY MASKING POLICY }

-- For ROW ACCESS POLICY (account-level privileges)
  { CREATE ROW ACCESS POLICY | APPLY ROW ACCESS POLICY }
```

```sql
privileges_level ::=
    *.*
  | db_name.*
  | db_name.tbl_name
  | STAGE <stage_name>
  | UDF <udf_name>
  | MASKING POLICY <policy_name>
  | ROW ACCESS POLICY <policy_name>
```

### 授予 Masking Policy 权限 {#granting-masking-policy-privileges}

使用以下形式管理对单个 masking policy 的访问：

```sql
GRANT APPLY ON MASKING POLICY <policy_name> TO ROLE <role_name>
GRANT ALL [ PRIVILEGES ] ON MASKING POLICY <policy_name> TO ROLE <role_name>
GRANT OWNERSHIP ON MASKING POLICY <policy_name> TO ROLE '<role_name>'
```

- `CREATE MASKING POLICY` 允许角色创建新的 masking policy。
- `APPLY MASKING POLICY` 允许被授予者在结合适当的 `ALTER TABLE` 或 policy 命令时，对任意 masking policy 执行附加、分离、描述或删除操作。
- `GRANT APPLY ON MASKING POLICY ...` 授予被授权者管理特定 masking policy 的权限，而无需授予全局访问权限。
- OWNERSHIP 提供对 masking policy 的完全控制；{{{ .lake }}} 会自动向创建者角色授予新 policy 的 OWNERSHIP，并在 policy 被删除时回收该权限。

### 授予 Row Access Policy 权限 {#granting-row-access-policy-privileges}

使用以下形式管理对单个 row access policy 的访问：

```sql
GRANT APPLY ON ROW ACCESS POLICY <policy_name> TO ROLE <role_name>
GRANT ALL [ PRIVILEGES ] ON ROW ACCESS POLICY <policy_name> TO ROLE <role_name>
GRANT OWNERSHIP ON ROW ACCESS POLICY <policy_name> TO ROLE '<role_name>'
```

- `CREATE ROW ACCESS POLICY` 允许角色创建新的 row access policy。
- `APPLY ROW ACCESS POLICY` 授予将任意 row access policy 附加到表或从表分离的权限，同时也包括 DESCRIBE/DROP 命令。
- `GRANT APPLY ON ROW ACCESS POLICY ...` 将访问限制在特定的 row access policy 上。
- OWNERSHIP 提供对 row access policy 的完全控制；创建者角色会自动获得 OWNERSHIP，并在 policy 被删除时失去该权限。

### 授予角色 {#granting-role}

要了解什么是角色及其工作方式，请参阅 [角色](/tidb-cloud-lake/guides/roles.md)。

```sql
-- Grant a role to a user
GRANT ROLE <role_name> TO <user_name>

-- Grant a role to a role
GRANT ROLE <role_name> TO ROLE <role_name>
```

> **注意：**
>
> `default_role` 是用户属性——它在你执行 `CREATE USER` 或 `ALTER USER` 时设置，`GRANT`/`REVOKE` 不会修改它。因此，如果你之后回收了某个恰好是他人 `default_role` 的角色，该设置仍然保留，但角色成员关系已经不存在。请使用 `ALTER USER ... WITH DEFAULT_ROLE` 显式更新它。

### 授予所有权 {#granting-ownership}

要了解什么是所有权及其工作方式，请参阅 [所有权](/tidb-cloud-lake/guides/ownership.md)。

```sql
-- Grant ownership of a specific table within a database to a role
GRANT OWNERSHIP ON <database_name>.<table_name> TO ROLE '<role_name>'

-- Grant ownership of a stage to a role
GRANT OWNERSHIP ON STAGE <stage_name> TO ROLE '<role_name>'

-- Grant ownership of a user-defined function (UDF) to a role
GRANT OWNERSHIP ON UDF <udf_name> TO ROLE '<role_name>'
```

## 示例 {#examples}

### 示例 1：向角色授予权限 {#example-1-granting-privileges-to-a-role}

创建一个角色：

```sql
CREATE ROLE user1_role;
```

将 `default` 数据库中所有现有表的 `ALL` 权限授予角色 `user1_role`：

```sql
GRANT ALL ON default.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON 'default'.* TO ROLE 'user1_role'    |
+--------------------------------------------------+
```

将所有数据库的 `ALL` 权限授予角色 `user1_role`：

```sql
GRANT ALL ON *.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON 'default'.* TO ROLE 'user1_role'    |
| GRANT ALL ON *.* TO ROLE 'user1_role'            |
+--------------------------------------------------+
```

将名为 `s1` 的 stage 的 `ALL` 权限授予角色 `user1_role`：

```sql
GRANT ALL ON STAGE s1 TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON STAGE s1 TO ROLE 'user1_role'       |
+--------------------------------------------------+
```

将名为 `f1` 的 UDF 的 `ALL` 权限授予角色 `user1_role`：

```sql
GRANT ALL ON UDF f1 TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON UDF f1 TO ROLE 'user1_role'         |
+--------------------------------------------------+
```

### 示例 2：向角色授予特定权限 {#example-2-granting-specific-privileges-to-a-role}

将 `mydb` 数据库中所有现有表的 `SELECT` 权限授予角色 `role1`：

创建角色：

```sql
CREATE ROLE role1;
```

向角色授予权限：

```sql
GRANT SELECT ON mydb.* TO ROLE role1;
```

显示该角色的授权信息：

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

### 示例 3：将角色授予用户 {#example-3-granting-a-role-to-a-user}

创建一个用户：

```sql
CREATE USER user1 IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'role1';
```

角色 `role1` 的授权信息如下：

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

将角色 `role1` 授予用户 `user1`：

```sql
 GRANT ROLE role1 TO user1;
```

现在，用户 `user1` 的授权信息如下：

```sql
SHOW GRANTS FOR user1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT ROLE role1 TO 'user1'@'%'     |
+-------------------------------------+
```

### 示例 4：向角色授予所有权 {#example-4-granting-ownership-to-a-role}

```sql
-- Grant ownership of all tables in the 'finance_data' database to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.* TO ROLE 'data_owner';

-- Grant ownership of the table 'transactions' in the 'finance_data' schema to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.transactions TO ROLE 'data_owner';

-- Grant ownership of the stage 'ingestion_stage' to the role 'data_owner'
GRANT OWNERSHIP ON STAGE ingestion_stage TO ROLE 'data_owner';

-- Grant ownership of the user-defined function 'calculate_profit' to the role 'data_owner'
GRANT OWNERSHIP ON UDF calculate_profit TO ROLE 'data_owner';
```

### 示例 5：授予 Masking Policy 权限 {#example-5-granting-masking-policy-privileges}

```sql
-- Allow the current user to create masking policies
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;

-- Create a masking policy while assuming the security_admin role
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING -> '***';

-- Grant a role the ability to apply the policy when altering tables
GRANT APPLY ON MASKING POLICY email_mask TO ROLE pii_readers;

-- Review the masking policy privileges
SHOW GRANTS ON MASKING POLICY email_mask;
```

### 示例 6：授予 Row Access Policy 权限 {#example-6-granting-row-access-policy-privileges}

```sql
-- Allow the current role to create row access policies
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE row_policy_admin;

-- Define a row access policy while assuming the row_policy_admin role
CREATE ROW ACCESS POLICY rap_region AS (region STRING) RETURNS BOOLEAN -> region = 'APAC';

-- Allow a role to apply the policy when altering tables
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE apac_only;

-- Review the row access policy privileges
SHOW GRANTS ON ROW ACCESS POLICY rap_region;
```
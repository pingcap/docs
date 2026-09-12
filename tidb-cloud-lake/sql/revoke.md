---
title: REVOKE
summary: 回收特定数据库对象的权限、角色和所有权。这包括。
---

# REVOKE

回收特定数据库对象的权限、角色和所有权。这包括：

- 从角色回收权限。
- 从用户或其他角色中移除角色。

另请参阅：

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

> **Note:**
>
> 使用 `REVOKE` 修改权限或角色后，运行 [SYSTEM FLUSH PRIVILEGES](/tidb-cloud-lake/sql/system-flush-privileges.md) 以立即将更新广播到每个查询节点。

## 语法 {#syntax}

### 回收权限 {#revoking-privileges}

```sql
REVOKE {
        schemaObjectPrivileges | ALL [ PRIVILEGES ] ON <privileges_level>
       }
FROM ROLE <role_name>
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

### 回收 Masking Policy 权限 {#revoking-masking-policy-privileges}

```sql
REVOKE APPLY ON MASKING POLICY <policy_name> FROM ROLE <role_name>
REVOKE ALL [ PRIVILEGES ] ON MASKING POLICY <policy_name> FROM ROLE <role_name>
REVOKE OWNERSHIP ON MASKING POLICY <policy_name> FROM ROLE '<role_name>'
```

使用这些形式可以移除对单个 masking policy 的访问。全局 `CREATE MASKING POLICY` 和 `APPLY MASKING POLICY` 权限使用带有 `ON *.*` 的标准语法进行回收。

### 回收 Row Access Policy 权限 {#revoking-row-access-policy-privileges}

```sql
REVOKE APPLY ON ROW ACCESS POLICY <policy_name> FROM ROLE <role_name>
REVOKE ALL [ PRIVILEGES ] ON ROW ACCESS POLICY <policy_name> FROM ROLE <role_name>
REVOKE OWNERSHIP ON ROW ACCESS POLICY <policy_name> FROM ROLE '<role_name>'
```

使用这些形式可以回收对特定 row access policy 的访问。对全局 `CREATE ROW ACCESS POLICY` 和 `APPLY ROW ACCESS POLICY` 权限的回收，可通过针对 `ON *.*` 的标准语法完成。

### 回收角色 {#revoking-role}

```sql
-- Revoke a role from a user
REVOKE ROLE <role_name> FROM <user_name>

-- Revoke a role from a role
REVOKE ROLE <role_name> FROM ROLE <role_name>
```

## 示例 {#examples}

### 示例 1：从角色回收权限 {#example-1-revoking-privileges-from-a-role}

创建一个角色：

```sql
CREATE ROLE user1_role;
```

将 `default` 数据库中所有现有表的 `SELECT,INSERT` 权限授予角色 `user1_role`：

```sql
GRANT SELECT,INSERT ON default.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+---------------------------------------------------------+
| Grants                                                  |
+---------------------------------------------------------+
| GRANT SELECT,INSERT ON 'default'.* TO ROLE 'user1_role' |
+---------------------------------------------------------+
```

从角色 `user1_role` 回收 `INSERT` 权限：

```sql
REVOKE INSERT ON default.* FROM ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+---------------------------------------------------+
| Grants                                            |
+---------------------------------------------------+
| GRANT SELECT ON 'default'.* TO 'user1_role'       |
+---------------------------------------------------+
```

### 示例 2：从另一个角色回收权限 {#example-2-revoking-privileges-from-another-role}

将 `mydb` 数据库中所有现有表的 `SELECT,INSERT` 权限授予角色 `role1`：

创建角色：

```sql
CREATE ROLE role1;
```

向该角色授予权限：

```sql
GRANT SELECT,INSERT ON mydb.* TO ROLE role1;
```

显示该角色的授权信息：

```sql
SHOW GRANTS FOR ROLE role1;
+--------------------------------------------+
| Grants                                     |
+--------------------------------------------+
| GRANT SELECT,INSERT ON 'mydb'.* TO 'role1' |
+--------------------------------------------+
```

从角色 `role1` 回收 `INSERT` 权限：

```sql
REVOKE INSERT ON mydb.* FROM ROLE role1;
```

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

### 示例 3：从用户回收角色 {#example-3-revoking-a-role-from-a-user}

```sql
REVOKE ROLE role1 FROM USER user1;
```

```sql
SHOW GRANTS FOR user1;
```

> **提示：**
>
> 为什么在执行 revoke 后，`default_role` 仍然显示？
>
> `default_role` 是用户属性，不是授权。`REVOKE` 会移除角色成员关系，但不会重置 `default_role`。如下所示：
>
> ```sql
> CREATE ROLE analyst;
> CREATE USER bob IDENTIFIED BY 'password123' WITH DEFAULT_ROLE = 'analyst';
> GRANT ROLE analyst TO bob;
>
> DESC USER bob;
> +------+----------+----------------------+--------------+---------+
> | name | hostname | auth_type            | default_role | roles   |
> +------+----------+----------------------+--------------+---------+
> | bob  | %        | double_sha1_password | analyst      | analyst |
> +------+----------+----------------------+--------------+---------+
>
> REVOKE ROLE analyst FROM bob;
>
> DESC USER bob;
> +------+----------+----------------------+--------------+-------+
> | name | hostname | auth_type            | default_role | roles |
> +------+----------+----------------------+--------------+-------+
> | bob  | %        | double_sha1_password | analyst      |       |
> +------+----------+----------------------+--------------+-------+
> ```
>
> 注意，`roles` 现在为空，但 `default_role` 仍然保留。该用户不再拥有 `analyst` 的权限。要清理该属性，请执行 `ALTER USER bob WITH DEFAULT_ROLE = 'public'`。

### 示例 4：回收 Masking Policy 权限 {#example-4-revoking-masking-policy-privileges}

```sql
-- Remove per-policy access from a role
REVOKE APPLY ON MASKING POLICY email_mask FROM ROLE pii_readers;

-- Revoke the ability to create masking policies at the account level
REVOKE CREATE MASKING POLICY ON *.* FROM ROLE security_admin;
```

### 示例 5：回收 Row Access Policy 权限 {#example-5-revoking-row-access-policy-privileges}

```sql
-- Remove per-policy access from a role
REVOKE APPLY ON ROW ACCESS POLICY rap_region FROM ROLE apac_only;

-- Revoke the ability to create row access policies globally
REVOKE CREATE ROW ACCESS POLICY ON *.* FROM ROLE row_policy_admin;
```
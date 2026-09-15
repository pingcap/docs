---
title: CREATE USER
summary: 创建一个用于连接到 {{{ .lake }}} 的 SQL 用户。必须为用户授予适当的权限，才能访问数据库并执行操作。
---

# CREATE USER

创建一个用于连接到 {{{ .lake }}} 的 SQL 用户。必须为用户授予适当的权限，才能访问数据库并执行操作。

另请参阅：

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [ALTER USER](/tidb-cloud-lake/sql/alter-user.md)
- [DROP USER](/tidb-cloud-lake/sql/drop-user.md)

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] USER <name> IDENTIFIED [ WITH <auth_type> ] BY '<password>'
[ WITH MUST_CHANGE_PASSWORD = true | false ]
[ WITH SET PASSWORD POLICY = '<policy_name>' ]
[ WITH SET NETWORK POLICY = '<policy_name>' ]
[ WITH DEFAULT_ROLE = '<role_name>' ]
[ WITH DISABLED = true | false ]
```

**参数：**

- `<name>`：用户名（不能包含单引号、双引号、退格符或换页符）
- `<auth_type>`：认证类型 - `double_sha1_password`（默认）、`sha256_password` 或 `no_password`
- `MUST_CHANGE_PASSWORD`：当为 `true` 时，用户必须在首次登录时修改密码
- `DEFAULT_ROLE`：设置默认角色（角色必须被显式授予后才会生效）
- `DISABLED`：当为 `true` 时，用户将以禁用状态创建，且无法登录

## 示例 {#examples}

### 示例 1：跨所有数据库的完全访问权限 {#example-1-full-access-across-all-databases}

创建一个在所有数据库上都具有完整读写权限的用户：

```sql
-- Create a role with global access
CREATE ROLE full_access_role;
GRANT ALL ON *.* TO ROLE full_access_role;

-- Create the user and assign the role
CREATE USER admin_user IDENTIFIED BY 'SecurePass456!' WITH DEFAULT_ROLE = 'full_access_role';
GRANT ROLE full_access_role TO admin_user;
```

### 示例 2：跨所有数据库的只读访问权限 {#example-2-read-only-access-across-all-databases}

创建一个只能查询数据的用户，适用于仪表板或 BI 工具：

```sql
-- Create a read-only role
CREATE ROLE readonly_role;
GRANT SELECT ON *.* TO ROLE readonly_role;

-- Create the user
CREATE USER readonly_user IDENTIFIED BY 'ReadOnly789!' WITH DEFAULT_ROLE = 'readonly_role';
GRANT ROLE readonly_role TO readonly_user;
```

### 示例 3：单个数据库访问权限 {#example-3-single-database-access}

创建一个角色，授予数据库权限，并将该角色分配给用户：

```sql
-- Create a role and grant database privileges
CREATE ROLE data_analyst_role;
GRANT SELECT, INSERT ON default.* TO ROLE data_analyst_role;

-- Create a new user and assign the role
CREATE USER data_analyst IDENTIFIED BY 'secure_password123' WITH DEFAULT_ROLE = 'data_analyst_role';
GRANT ROLE data_analyst_role TO data_analyst;
```

验证角色和权限：

```sql
SHOW GRANTS FOR ROLE data_analyst_role;
+-----------------------------------------------------------------+
| Grants                                                          |
+-----------------------------------------------------------------+
| GRANT SELECT,INSERT ON 'default'.* TO ROLE  'data_analyst_role' |
+-----------------------------------------------------------------+
```

### 示例 4：使用不同认证类型创建用户 {#example-4-create-users-with-different-authentication-types}

```sql
-- Create user with default authentication
CREATE USER user1 IDENTIFIED BY 'abc123';

-- Create user with SHA256 authentication
CREATE USER user2 IDENTIFIED WITH sha256_password BY 'abc123';
```
---
title: PostgreSQL 身份验证和角色
summary: 了解如何在兼容 PostgreSQL 的 TiDB Cloud Starter 上管理数据库角色和权限。
---

# PostgreSQL 身份验证和角色

兼容 PostgreSQL 的 {{{ .starter }}} 支持数据库角色、角色属性、对象权限以及会话角色切换。

本页介绍数据库级别的身份验证和授权。TiDB Cloud 组织、项目和实例访问通过 TiDB Cloud Identity and Access Management 单独管理。

## 创建角色 {#create-a-role}

使用 `CREATE ROLE ... LOGIN` 创建可连接到数据库的角色。

```sql
CREATE ROLE app_user
LOGIN
PASSWORD 'SecurePass1';
```

不带 `LOGIN` 的角色可用作权限管理的组角色：

```sql
CREATE ROLE readonly;
```

将组角色授予登录角色：

```sql
GRANT readonly TO app_user;
```

## 修改角色 {#alter-a-role}

修改角色密码：

```sql
ALTER ROLE app_user
PASSWORD 'NewSecurePass1';
```

设置或取消设置选定的角色属性：

```sql
ALTER ROLE app_user CREATEDB;
ALTER ROLE app_user NOCREATEDB;

ALTER ROLE app_user BYPASSRLS;
ALTER ROLE app_user NOBYPASSRLS;
```

支持以下常见角色属性：

| 属性 | 说明 |
| --- | --- |
| `LOGIN` / `NOLOGIN` | 控制该角色是否可以连接。 |
| `CREATEDB` / `NOCREATEDB` | 控制该角色是否可以创建数据库。 |
| `BYPASSRLS` / `NOBYPASSRLS` | 控制该角色是否绕过行级安全策略。 |

仅将 `BYPASSRLS` 属性授予受信任的管理角色或服务角色。

## 授予表权限 {#grant-table-privileges}

授予表上的一个或多个权限：

```sql
GRANT SELECT, INSERT
ON todos
TO app_user;
```

授予所有受支持的表权限：

```sql
GRANT ALL
ON todos
TO app_user;
```

授予某个数据库模式中所有表的权限：

```sql
GRANT SELECT
ON ALL TABLES IN SCHEMA public
TO readonly;
```

## 回收表权限 {#revoke-table-privileges}

回收之前授予某个角色的权限：

```sql
REVOKE INSERT
ON todos
FROM app_user;
```

回收表上的所有权限：

```sql
REVOKE ALL
ON todos
FROM app_user;
```

## 授予数据库模式权限 {#grant-schema-privileges}

使用 `USAGE` 允许角色访问某个数据库模式中的对象：

```sql
GRANT USAGE
ON SCHEMA analytics
TO app_user;
```

授予在某个数据库模式中创建对象的权限：

```sql
GRANT CREATE
ON SCHEMA analytics
TO app_user;
```

在数据库模式上授予 `USAGE` 不会自动授予该数据库模式中表的权限。你需要单独授予所需的表权限。

例如：

```sql
GRANT USAGE
ON SCHEMA analytics
TO app_user;

GRANT SELECT
ON ALL TABLES IN SCHEMA analytics
TO app_user;
```

## 授予序列权限 {#grant-sequence-privileges}

序列权限会被强制执行。

例如：

```sql
GRANT USAGE, SELECT
ON SEQUENCE order_seq
TO app_user;
```

以下是相关的序列权限：

| 权限 | 用途 |
| --- | --- |
| `USAGE` | 允许执行常见的序列操作，例如 `nextval()`。 |
| `SELECT` | 允许在适用情况下读取当前序列值。 |
| `UPDATE` | 执行会更改序列值的操作（例如 `setval()`）所必需。 |

例如，授予重新定位序列的权限：

```sql
GRANT UPDATE
ON SEQUENCE order_seq
TO app_user;
```

> **Note:**
>
> 使用 `SERIAL` 或 `BIGSERIAL` 默认值的非超级用户角色，需要对底层序列具有 `USAGE` 或 `UPDATE` 权限，除非所有权或继承的权限已提供该授权。仅授予表上的 `INSERT` 权限是不够的。

## 授予未来对象的权限 {#grant-privileges-on-future-objects}

使用 `ALTER DEFAULT PRIVILEGES` 为当前角色后续创建的对象配置权限。

例如，为未来创建的表授予 `SELECT` 权限：

```sql
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT ON TABLES TO readonly;
```

对于显式创建的序列：

```sql
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_user;
```

序列的默认权限仅适用于使用 `CREATE SEQUENCE` 显式创建的序列。通过 `SERIAL` 或 `BIGSERIAL` 隐式创建的序列不会继承这些序列默认权限。

不支持 `ALTER DEFAULT PRIVILEGES ... ON FUNCTIONS`。

## 管理角色成员关系 {#manage-role-membership}

将一个角色授权给另一个角色：

```sql
GRANT readonly TO app_user;
```

回收成员关系：

```sql
REVOKE readonly FROM app_user;
```

## 在会话中切换角色 {#switch-roles-in-a-session}

使用 `SET ROLE` 切换到已授权给当前会话用户的角色：

```sql
SET ROLE app_user;
```

返回到原始的已认证角色：

```sql
RESET ROLE;
```

角色切换会被强制校验。你不能将 `SET ROLE` 切换到未授权给当前用户的角色。

检查当前角色和会话角色：

```sql
SELECT CURRENT_USER, SESSION_USER;
```

## 查看角色和权限 {#inspect-roles-and-privileges}

列出数据库角色：

```sql
SELECT
    rolname,
    rolcanlogin,
    rolcreatedb,
    rolbypassrls
FROM pg_roles
ORDER BY rolname;
```

列出角色成员关系：

```sql
SELECT
    member_role.rolname AS member,
    granted_role.rolname AS granted_role
FROM pg_auth_members AS m
JOIN pg_roles AS member_role
    ON member_role.oid = m.member
JOIN pg_roles AS granted_role
    ON granted_role.oid = m.roleid
ORDER BY member_role.rolname, granted_role.rolname;
```

列出表权限：

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
ORDER BY table_name, grantee, privilege_type;
```

## 删除角色 {#drop-a-role}

删除角色之前，请先处理依赖关系，例如该角色拥有的对象以及授予给它的权限。

例如：

```sql
REVOKE SELECT ON todos FROM app_user;
REVOKE USAGE ON SCHEMA public FROM app_user;
```

然后删除该角色：

```sql
DROP ROLE app_user;
```

## 行级安全 {#row-level-security}

数据库角色可以在行级安全策略中被引用。

例如：

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY app_user_todos
ON todos
FOR SELECT
TO app_user
USING (user_id = current_user);
```

有关完整的 RLS 语法和行为，请参见 [PostgreSQL 行级安全](/tidb-cloud/starter/pg-row-level-security.md)。
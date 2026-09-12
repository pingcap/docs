---
title: CREATE ROLE
summary: 创建一个新的角色用于访问控制。角色用于对权限进行分组，并且可以分配给用户或其他角色，从而在 {{{ .lake }}} 中提供一种灵活的权限管理方式。
---

# CREATE ROLE

创建一个新的角色用于访问控制。角色用于对权限进行分组，并且可以分配给用户或其他角色，从而在 {{{ .lake }}} 中提供一种灵活的权限管理方式。

## 语法 {#syntax}

```sql
CREATE ROLE [ IF NOT EXISTS ] <name>
```

**参数：**

- `IF NOT EXISTS`：仅当角色不存在时才创建该角色（推荐使用以避免错误）
- `<name>`：角色名称（不能包含单引号、双引号、退格符或换页符）

## 示例 {#examples}

```sql
-- Create a basic role
CREATE ROLE analyst;

-- Create role only if it doesn't exist (recommended)
CREATE ROLE IF NOT EXISTS data_viewer;
```

## 常见用法模式 {#common-usage-patterns}

### 只读分析师角色 {#read-only-analyst-role}

为需要对销售数据具有读访问权限的数据分析师创建一个角色：

```sql
-- Create the analyst role
CREATE ROLE sales_analyst;

-- Grant read permissions
GRANT SELECT ON sales_db.* TO ROLE sales_analyst;

-- Assign to users
GRANT ROLE sales_analyst TO 'alice';
GRANT ROLE sales_analyst TO 'bob';
```

### 数据库管理员角色 {#database-administrator-role}

为需要完全控制权限的管理员创建一个角色：

```sql
-- Create the admin role
CREATE ROLE sales_admin;

-- Grant full permissions on the database
GRANT ALL ON sales_db.* TO ROLE sales_admin;

-- Grant user management permissions
GRANT CREATE USER, CREATE ROLE ON *.* TO ROLE sales_admin;

-- Assign to admin users
GRANT ROLE sales_admin TO 'admin_user';
```

### 验证 {#verification}

```sql
-- Check what each role can do
SHOW GRANTS FOR ROLE sales_analyst;
SHOW GRANTS FOR ROLE sales_admin;

-- Check user permissions
SHOW GRANTS FOR 'alice';
SHOW GRANTS FOR 'admin_user';
```

## 另请参阅 {#see-also}

- [GRANT](/tidb-cloud-lake/sql/grant.md) - 授予权限和角色
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md) - 查看已授予的权限
- [DROP ROLE](/tidb-cloud-lake/sql/drop-role.md) - 删除角色
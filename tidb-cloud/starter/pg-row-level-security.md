---
title: PostgreSQL 行级安全
summary: 了解如何在兼容 PostgreSQL 的 TiDB Cloud Starter 上使用行级安全策略。
---

# PostgreSQL 行级安全

兼容 PostgreSQL 的 {{{ .starter }}} 支持兼容 PostgreSQL 的行级安全（RLS）。除角色对表拥有的权限外，RLS 还会进一步限制数据库角色可以查看、插入、修改或删除哪些行。

数据库会针对每个适用的查询评估 RLS 策略。因此，RLS 非常适合多租户应用程序以及其他需要按行进行访问控制的工作负载。

## 启用行级安全 {#enable-row-level-security}

使用 `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`：

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
```

启用 RLS 后，如果不存在适用的策略，则对于不会绕过 RLS 的角色，默认会拒绝访问。

要禁用 RLS：

```sql
ALTER TABLE todos DISABLE ROW LEVEL SECURITY;
```

## 对表所有者强制启用 RLS {#force-rls-for-the-table-owner}

默认情况下，表所有者会绕过 RLS 策略。

使用 `FORCE ROW LEVEL SECURITY` 可使表所有者也受这些策略约束：

```sql
ALTER TABLE todos FORCE ROW LEVEL SECURITY;
```

要恢复所有者的默认行为：

```sql
ALTER TABLE todos NO FORCE ROW LEVEL SECURITY;
```

即使启用了 `FORCE ROW LEVEL SECURITY`，超级用户和具有 `BYPASSRLS` 属性的角色仍会绕过 RLS。只有当表所有者不是超级用户且不具有 `BYPASSRLS` 时，`FORCE ROW LEVEL SECURITY` 才会使其受策略约束。

## 创建策略 {#create-a-policy}

使用 `CREATE POLICY` 定义 RLS 策略。

通用语法如下：

```sql
CREATE POLICY policy_name ON table_name
    [AS { PERMISSIVE | RESTRICTIVE }]
    [FOR { ALL | SELECT | INSERT | UPDATE | DELETE }]
    [TO role_name [, ...]]
    [USING (expression)]
    [WITH CHECK (expression)];
```

如果省略 `AS`，则该策略为 `PERMISSIVE`。

如果省略 `FOR`，则该策略适用于所有受支持的命令。

如果省略 `TO`，则该策略适用于 `PUBLIC`。

## `USING` 和 `WITH CHECK` {#using-and-with-check}

`USING` 和 `WITH CHECK` 的用途不同：

| 子句 | 用途 | 适用于 |
| --- | --- | --- |
| `USING` | 决定哪些现有行可见或可作为目标行。 | `SELECT`, `UPDATE`, `DELETE` |
| `WITH CHECK` | 验证新行或已修改行的值。 | `INSERT`, `UPDATE` |

每种操作使用的子句如下：

| 操作 | `USING` | `WITH CHECK` |
| --- | --- | --- |
| `SELECT` | 使用 | 不使用 |
| `INSERT` | 不使用 | 使用 |
| `UPDATE` | 使用 | 使用 |
| `DELETE` | 使用 | 不使用 |

对于 `UPDATE` 策略，如果省略 `WITH CHECK`，则也会使用 `USING` 表达式来验证修改后的行。

## 示例：按用户限制行 {#example-restrict-rows-by-user}

以下示例允许每个角色仅访问 `user_id` 与 `current_user` 匹配的行。

创建表：

```sql
CREATE TABLE todos (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    task TEXT NOT NULL,
    done BOOLEAN DEFAULT false
);
```

启用 RLS：

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
```

允许用户读取自己的行：

```sql
CREATE POLICY user_select
ON todos
FOR SELECT
USING (user_id = current_user);
```

允许用户为自己插入行：

```sql
CREATE POLICY user_insert
ON todos
FOR INSERT
WITH CHECK (user_id = current_user);
```

允许用户修改自己的行：

```sql
CREATE POLICY user_update
ON todos
FOR UPDATE
USING (user_id = current_user)
WITH CHECK (user_id = current_user);
```

允许用户删除自己的行：

```sql
CREATE POLICY user_delete
ON todos
FOR DELETE
USING (user_id = current_user);
```

## 示例：公开行和私有行 {#example-public-and-private-rows}

以下示例允许对该表具有 SELECT 权限的角色查看已发布的帖子，并允许作者查看自己未发布的帖子。

创建表并启用 RLS：

```sql
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    author TEXT,
    published BOOLEAN DEFAULT false,
    content TEXT
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

为已发布的帖子创建策略：

```sql
CREATE POLICY see_published
ON posts
FOR SELECT
USING (published = true);
```

为用户自己的帖子创建另一个策略：

```sql
CREATE POLICY see_own
ON posts
FOR SELECT
USING (author = current_user);
```

由于这两个策略默认都是宽松策略，因此具有 SELECT 权限的角色只要满足任一适用策略，就可以看到该行。

## 宽松策略和限制性策略 {#permissive-and-restrictive-policies}

### 宽松策略 {#permissive-policies}

同一命令的多个 `PERMISSIVE` 策略会使用 `OR` 组合。

例如：

```text
permissive_policy_1 OR permissive_policy_2 OR ...
```

至少必须有一个适用的宽松策略允许该行。

### 限制性策略 {#restrictive-policies}

当每个匹配的限制性策略都必须通过时，使用 `AS RESTRICTIVE`：

```sql
CREATE POLICY must_be_published
ON posts
AS RESTRICTIVE
FOR SELECT
USING (published = true);
```

限制性策略会使用 `AND` 组合，并在宽松结果之外额外应用：

```text
(permissive_policy_1 OR permissive_policy_2 OR ...)
AND restrictive_policy_1
AND restrictive_policy_2
AND ...
```

限制性策略本身不会授予访问权限。还必须至少有一个适用的宽松策略允许该行访问。

## 将策略应用到特定角色 {#apply-policies-to-specific-roles}

使用 `TO` 将策略限制为一个或多个角色。

例如：

```sql
CREATE POLICY support_read
ON tickets
FOR SELECT
TO support_agent
USING (status <> 'private');
```

没有显式 `TO` 子句的策略会应用于 `PUBLIC`。

## 修改策略 {#alter-a-policy}

使用 `ALTER POLICY` 修改角色或策略表达式：

```sql
ALTER POLICY see_own
ON posts
USING (author = current_user OR published = true);
```

## 删除策略 {#drop-a-policy}

使用 `DROP POLICY`：

```sql
DROP POLICY see_own ON posts;
```

如果希望在策略不存在时避免报错：

```sql
DROP POLICY IF EXISTS see_own ON posts;
```

## 绕过 RLS {#bypass-rls}

### `BYPASSRLS` 角色属性 {#bypassrls-role-attribute}

具有 `BYPASSRLS` 的角色会绕过 RLS 策略。

创建一个带有此属性的登录角色：

```sql
CREATE ROLE service_admin
LOGIN
PASSWORD 'SecurePass1'
BYPASSRLS;
```

之后可以授予或回收该属性：

```sql
ALTER ROLE service_admin BYPASSRLS;
ALTER ROLE service_admin NOBYPASSRLS;
```

仅向受信任的管理角色或服务角色授予 `BYPASSRLS`。

### 表所有者 {#table-owners}

默认情况下，表所有者会绕过 RLS。如果希望所有者也受策略约束，请使用 `FORCE ROW LEVEL SECURITY`。

### `SECURITY DEFINER` 函数 {#security-definer-functions}

`SECURITY DEFINER` 函数会以其所有者的权限执行。

例如：

```sql
CREATE FUNCTION list_all_posts()
RETURNS SETOF posts
LANGUAGE SQL
SECURITY DEFINER
AS $$
    SELECT * FROM posts
$$;
```

如果函数所有者可以绕过 RLS，则在函数内部执行的查询也可以绕过 RLS。

> **Warning:**
>
> 请谨慎使用 `SECURITY DEFINER` 函数。除非函数严格控制可访问的操作和行，否则不要将能够绕过 RLS 的函数暴露给不受信任的角色。

## 检查 RLS 策略 {#inspect-rls-policies}

使用 `pg_policies` 列出表上的策略：

```sql
SELECT
    policyname,
    cmd,
    permissive,
    roles,
    qual,
    with_check
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'todos'
ORDER BY policyname;
```

检查是否已启用或强制启用 RLS：

```sql
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE oid = 'public.todos'::regclass;
```

检查某个角色是否可以绕过 RLS：

```sql
SELECT
    rolname,
    rolbypassrls
FROM pg_roles
WHERE rolname = 'app_user';
```

## 安全注意事项 {#security-considerations}

使用 RLS 时：

- 对于正常的应用流量，使用专用的应用角色，而不是管理角色。
- 在向应用角色授予对受保护表的访问权限之前，先启用 RLS。
- 为应用所需的每种操作创建策略。
- 对于 `UPDATE` 策略，同时检查 `USING` 和 `WITH CHECK` 条件。
- 仅向受信任的角色授予 `BYPASSRLS`。
- 仔细审查 `SECURITY DEFINER` 函数，因为它们会以函数所有者的权限执行。
- 使用与应用相同的角色来测试 RLS 行为。
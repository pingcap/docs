---
title: PostgreSQL 系统目录
summary: 了解如何在兼容 PostgreSQL 的 TiDB Cloud Starter 中使用系统目录检查数据库对象。
---

# PostgreSQL 系统目录

兼容 PostgreSQL 的 {{{ .starter }}} 提供了 `pg_catalog` 关系和 `information_schema` 视图，用于检查数据库、数据库模式、表、列、索引、约束、函数、角色以及其他数据库对象。

## `pg_catalog` relations {#pg-catalog-relations}

以下是可用的常用 `pg_catalog` 关系：

| 关系 | 描述 |
| --- | --- |
| `pg_tables` | 用户表。 |
| `pg_views` | 视图。 |
| `pg_class` | 表、索引、序列和视图。 |
| `pg_attribute` | 表列。 |
| `pg_attrdef` | 列默认值。 |
| `pg_namespace` | 数据库模式。 |
| `pg_type` | 数据类型。 |
| `pg_index` | 索引元信息。 |
| `pg_indexes` | 索引定义，包括 `indexdef`。 |
| `pg_constraint` | 主键、外键、检查、唯一和非空约束。 |
| `pg_proc` | 函数和存储过程。 |
| `pg_trigger` | 触发器元信息。 |
| `pg_enum` | 枚举值。 |
| `pg_sequence` | 序列元信息。 |
| `pg_extension` | 在数据库中注册的扩展。 |
| `pg_collation` | 内置排序规则。 |
| `pg_roles` | 数据库角色。 |
| `pg_user` | 登录用户。 |
| `pg_auth_members` | 角色成员关系。 |
| `pg_db_role_setting` | 按角色设置的会话参数默认值。 |
| `pg_database` | 数据库。 |
| `pg_description` | 对象注释和描述。 |
| `pg_depend` | 对象依赖关系元信息。 |
| `pg_am` | 索引访问方法。 |
| `pg_stat_user_tables` | 用户表统计信息。 |
| `pg_inherits` | 表继承元信息。 |
| `pg_range` | 范围类型元信息。 |
| `pg_opclass` | 运算符类。 |
| `pg_policy` | 行级安全策略元信息。 |
| `pg_policies` | 可读的行级安全策略定义。 |
| `pg_settings` | 运行时参数。 |
| `pg_timezone_names` | 时区名称和 UTC 偏移。 |
| `pg_rewrite` | 视图使用的重写规则。 |
| `pg_aggregate` | 聚合函数元信息。 |

某些系统目录关系主要是为了兼容 PostgreSQL 而存在，即使对应的 PostgreSQL 功能并不受支持。不要仅凭某个系统目录关系存在，就认定底层 PostgreSQL 功能可用。

例如，逻辑复制并不受支持，即使某些与复制相关的系统目录对象可能存在。

## `information_schema` views {#information-schema-views}

以下 `information_schema` 视图可用：

| 视图 | 描述 |
| --- | --- |
| `tables` | 表和视图。 |
| `columns` | 表列，包括生成列元信息。 |
| `schemata` | 数据库模式。 |
| `sequences` | 序列。 |
| `routines` | 函数和存储过程。 |
| `table_constraints` | 主键、外键、检查和唯一约束。 |
| `key_column_usage` | 主键、唯一和外键约束中的列。 |
| `referential_constraints` | 外键关系。 |
| `check_constraints` | 检查约束。 |
| `constraint_column_usage` | 被约束引用的列。 |
| `table_privileges` | 表权限。 |
| `triggers` | 触发器定义、触发时机和方向。 |

> **Note:**
>
> `information_schema.views` 不可用。要列出视图，请查询 `pg_views`，或通过 `table_type = 'VIEW'` 过滤 `information_schema.tables`。

对于列的可空性，请使用 `information_schema.columns.is_nullable` 或 `pg_attribute.attnotnull`。

## 列出数据库模式中的表 {#list-tables-in-a-schema}

使用 `pg_tables`：

```sql
SELECT
    tablename AS table,
    tableowner AS owner,
    hasindexes AS indexed,
    hastriggers AS has_triggers
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

如需更具可移植性的查询，请使用 `information_schema.tables`：

```sql
SELECT
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

## 列出表的列 {#list-columns-of-a-table}

使用 `information_schema.columns`：

```sql
SELECT
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default,
    ordinal_position
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'my_table'
ORDER BY ordinal_position;
```

如需查看更底层的元信息，请查询 `pg_attribute`：

```sql
SELECT
    a.attname AS column_name,
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
    a.attnotnull AS not_null,
    a.attnum AS position
FROM pg_attribute AS a
JOIN pg_class AS c
    ON c.oid = a.attrelid
JOIN pg_namespace AS n
    ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relname = 'my_table'
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

## 查找表上的索引 {#find-indexes-on-a-table}

使用 `pg_indexes`：

```sql
SELECT
    indexname AS index_name,
    indexdef AS definition
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'my_table'
ORDER BY indexname;
```

如需更详细的索引元信息：

```sql
SELECT
    i.relname AS index_name,
    ix.indisunique AS is_unique,
    ix.indisprimary AS is_primary
FROM pg_index AS ix
JOIN pg_class AS t
    ON t.oid = ix.indrelid
JOIN pg_class AS i
    ON i.oid = ix.indexrelid
JOIN pg_namespace AS n
    ON n.oid = t.relnamespace
WHERE n.nspname = 'public'
  AND t.relname = 'my_table'
ORDER BY i.relname;
```

## 检查表约束 {#check-table-constraints}

对于常见约束，请使用 `information_schema`：

```sql
SELECT
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name,
    cc.check_clause
FROM information_schema.table_constraints AS tc
LEFT JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.constraint_schema = tc.constraint_schema
    AND kcu.table_schema = tc.table_schema
    AND kcu.table_name = tc.table_name
LEFT JOIN information_schema.check_constraints AS cc
    ON cc.constraint_name = tc.constraint_name
    AND cc.constraint_schema = tc.constraint_schema
WHERE tc.table_schema = 'public'
  AND tc.table_name = 'my_table'
ORDER BY tc.constraint_type, tc.constraint_name;
```

对于简洁的定义，请使用 `pg_constraint`：

```sql
SELECT
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'public.my_table'::regclass
ORDER BY contype, conname;
```

`pg_constraint` 还会暴露 not-null 约束。若要以 PostgreSQL 可移植的方式检查列是否可为空，建议优先使用 `information_schema.columns.is_nullable`。

## 查找外键 {#find-foreign-keys}

使用 `information_schema` 检查出站外键：

```sql
SELECT
    tc.constraint_name,
    kcu.column_name AS fk_column,
    referenced_kcu.table_name AS referenced_table,
    referenced_kcu.column_name AS referenced_column,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.constraint_schema = tc.constraint_schema
    AND kcu.table_schema = tc.table_schema
    AND kcu.table_name = tc.table_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
    AND rc.constraint_schema = tc.constraint_schema
JOIN information_schema.key_column_usage AS referenced_kcu
    ON referenced_kcu.constraint_name = rc.unique_constraint_name
    AND referenced_kcu.constraint_schema = rc.unique_constraint_schema
    AND referenced_kcu.ordinal_position = kcu.position_in_unique_constraint
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name = 'my_table'
ORDER BY tc.constraint_name;
```

## 列出函数和存储过程 {#list-functions-and-procedures}

使用 `information_schema.routines`：

```sql
SELECT
    routine_name,
    routine_type,
    data_type AS return_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

如需更多元信息，请查询 `pg_proc`：

```sql
SELECT
    p.proname AS function_name,
    format_type(p.prorettype, NULL) AS return_type,
    p.prokind AS kind
FROM pg_proc AS p
JOIN pg_namespace AS n
    ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
ORDER BY p.proname;
```

## 检查角色和权限 {#inspect-roles-and-privileges}

列出角色：

```sql
SELECT
    rolname,
    rolcanlogin,
    rolinherit,
    rolbypassrls
FROM pg_roles
ORDER BY rolname;
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

## 检查行级安全 {#inspect-row-level-security}

列出某个表的策略：

```sql
SELECT
    policyname AS policy,
    cmd AS command,
    roles AS applies_to,
    qual AS using_expression,
    with_check AS check_expression
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'my_table'
ORDER BY policyname;
```

检查是否已启用或强制启用行级安全：

```sql
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE oid = 'public.my_table'::regclass;
```

## 检查扩展 {#inspect-extensions}

列出当前数据库中已注册的扩展：

```sql
SELECT
    extname,
    extversion
FROM pg_extension
ORDER BY extname;
```

## 系统目录兼容性 {#system-catalog-compatibility}

PostgreSQL-compatible {{{ .starter }}} 实现了常见 PostgreSQL 工具和自省工作流所需的系统目录接口，但系统目录的内容和列可能与上游 PostgreSQL 不同。

具体来说：

- 并非所有上游 `pg_catalog` 或 `information_schema` 关系都可用。
- 某些系统目录关系出于兼容性而存在，即使底层 PostgreSQL 功能并不受支持。
- 某些系统目录关系仅暴露上游 PostgreSQL 列的一个子集。
- `information_schema.views` 不可用。
- 可以使用自定义排序规则，但不会列在 `pg_collation` 中。
- 触发器时机以及行级/语句级方向应从 `information_schema.triggers` 中读取。
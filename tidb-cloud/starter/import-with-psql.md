---
title: 从 PostgreSQL 迁移到兼容 PostgreSQL 的 TiDB Cloud Starter
summary: 了解如何使用 `psql` 和 `\copy` 将数据库模式和数据从 PostgreSQL 迁移到兼容 PostgreSQL 的 TiDB Cloud Starter 实例。
---

# 从 PostgreSQL 迁移到兼容 PostgreSQL 的 TiDB Cloud Starter

本文介绍如何将现有的 PostgreSQL 数据库迁移到兼容 PostgreSQL 的 {{{ .starter }}} 实例。

> **Note:**
>
> 兼容 PostgreSQL 的 {{{ .starter }}} 当前处于公测阶段。该预览版本适用于开发和评估，不建议用于生产负载。
>
> 在公测期间，兼容 PostgreSQL 的 {{{ .starter }}} 支持使用 `psql` 和 `\copy` 进行迁移。本指南使用 `pg_dump` 从源 PostgreSQL 数据库导出数据库模式和数据，并使用 `psql` 和 `\copy` 将其导入目标实例。

整体迁移流程如下：

1. 准备源数据库、目标实例和迁移工具。
2. 检查源 PostgreSQL 数据库的兼容性。
3. 导出并检查源数据库模式。
4. 将数据库模式导入兼容 PostgreSQL 的 {{{ .starter }}} 实例。
5. 使用 `psql` 和 `\copy` 迁移数据。
6. 验证迁移后的数据库模式和数据。

## 前提条件 {#prerequisites}

开始迁移前，请确保具备以下条件：

- 可以访问源 PostgreSQL 数据库。
- 一个兼容 PostgreSQL 的 {{{ .starter }}} 实例。
- 目标实例的连接字符串。要获取连接字符串，请在 TiDB Cloud 控制台中打开目标实例，点击 **Connect**，然后选择 **PostgreSQL CLI**。
- 运行迁移命令的机器能够通过网络访问源 PostgreSQL 数据库和目标实例。

迁移前，请先阅读[PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)和[PostgreSQL 扩展](/tidb-cloud/starter/pg-extensions-overview.md)。

## 准备工具 {#prepare-tools}

在执行迁移的机器上安装以下 PostgreSQL 客户端工具：

- `pg_dump`：从源 PostgreSQL 数据库导出数据库模式和数据。
- `psql`：将数据库模式和数据导入兼容 PostgreSQL 的 {{{ .starter }}} 实例。

建议使用与源 PostgreSQL 数据库相同主版本的 `pg_dump`。

## 检查 PostgreSQL 兼容性 {#check-postgresql-compatibility}

兼容 PostgreSQL 的 {{{ .starter }}} 支持常见的 PostgreSQL 工作负载，但某些 PostgreSQL 特性尚不支持或行为有所不同。迁移前，请检查源数据库是否依赖这些特性。

### 检查数据库角色和权限 {#check-database-roles-and-permissions}

如果你的应用使用了行级安全（RLS），请在源 PostgreSQL 数据库上运行以下查询，以识别被 RLS 策略引用的角色：

```sql
SELECT DISTINCT r AS policy_role
FROM pg_policies, unnest(roles) AS r
WHERE r <> 'public';
```

请确保在导入数据库模式之前，已在目标实例中创建所需的应用角色。

### 检查不受支持的数据库模式特性 {#check-unsupported-schema-features}

对源 PostgreSQL 数据库运行以下查询：

```sql
-- Table partitioning
SELECT count(*) AS partitioned_tables
FROM pg_partitioned_table;

-- Table inheritance
SELECT count(*) AS inherited_tables
FROM pg_inherits;

-- Foreign data wrappers
SELECT count(*) AS fdw_servers
FROM pg_foreign_server;

-- Logical replication publications
SELECT count(*) AS publications
FROM pg_publication;
```

如果这些查询中任意一个返回非零计数，请在迁移前检查受影响的对象。

兼容 PostgreSQL 的 {{{ .starter }}} 不支持表分区、表继承、外部数据封装器或逻辑复制。

### 检查延迟外键约束 {#check-deferred-foreign-key-constraints}

兼容 PostgreSQL 的 {{{ .starter }}} 不支持延迟外键强制检查。声明为 `DEFERRABLE` 的外键约束会被立即强制执行。

迁移前，请对源 PostgreSQL 数据库运行以下查询，以识别可延迟外键约束：

```sql
SELECT
    conrelid::regclass AS table_name,
    conname AS constraint_name
FROM pg_constraint
WHERE contype = 'f'
  AND condeferrable;
```

迁移前，请检查所有依赖延迟外键强制检查的应用事务。

### 检查扩展 {#check-extensions}

运行以下查询，列出源数据库中已安装的扩展：

```sql
SELECT extname
FROM pg_extension
ORDER BY extname;
```

将结果与[PostgreSQL 扩展](/tidb-cloud/starter/pg-extensions-overview.md)进行比较。

兼容 PostgreSQL 的 {{{ .starter }}} 无法安装自定义或第三方 PostgreSQL 扩展。迁移前，请移除或替换对不受支持扩展的依赖。

### 检查 PL/pgSQL {#check-pl-pgsql}

兼容 PostgreSQL 的 {{{ .starter }}} 支持常见的 PL/pgSQL 结构，但某些结构尚不支持。

以下查询可帮助识别可能需要修改的 PL/pgSQL 例程：

```sql
SELECT proname, prosrc
FROM pg_proc
WHERE prolang = (SELECT oid FROM pg_language WHERE lanname = 'plpgsql')
  AND (
    prosrc ~* '\m(WHILE|FOREACH|CURSOR|REFCURSOR)\M'
    OR prosrc ~* '\mEXCEPTION\s+WHEN\M'
    OR prosrc ~* '\mBEGIN\M.*\mBEGIN\M'
  );
```

迁移前，请检查所有匹配的例程。特别是：

- 不支持 `WHILE` 和 `FOREACH` 循环。
- 不支持游标和 `REFCURSOR` 操作。
- 使用 `BEGIN ... EXCEPTION` 的异常处理仅在 `DO` 块中受支持。
- 嵌套过程块仅在 `DO` 块中受支持。

更多兼容性细节，请参见[PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## 迁移完整数据库 {#migrate-a-full-database}

对于 PostgreSQL 数据库迁移，请先导入数据库模式，再导入数据。

> **Important:**
>
> 不要一次性将标准的完整 `pg_dump` 文件导入兼容 PostgreSQL 的 {{{ .starter }}}。标准 PostgreSQL 转储可能会在表数据加载完成后再添加主键和其他约束，而兼容 PostgreSQL 的 {{{ .starter }}} 可能无法为非空表添加主键。
>
> 应先在表为空时导入数据库模式，然后再导入数据。
>
> 此迁移方法不支持零停机迁移或逻辑复制。请为最终迁移和应用切换预留维护窗口。
>
> 对于最终迁移，请停止对源数据库的所有写入和数据库模式变更，并在导出数据库模式和数据之前等待所有进行中的操作完成。在迁移验证和应用切换完成之前，请保持源数据库不变。
>
> 你可以在不停写源库的情况下执行试迁移，但导出开始后发生的变更可能不会包含在目标数据库中。

### 第 1 步：导出数据库模式 {#step-1-export-the-schema}

以纯 SQL 格式导出源数据库模式：

```shell
pg_dump \
  --schema-only \
  --no-owner \
  --no-privileges \
  "<SOURCE_DATABASE_URL>" \
  > schema.sql
```

使用默认的纯 SQL 格式。此工作流不要使用自定义（`-Fc`）或目录（`-Fd`）格式。

### 步骤 2：检查并更新表结构 {#step-2-review-and-update-the-schema}

在导入 `schema.sql` 之前，先检查其中是否包含不受支持的 PostgreSQL 特性。

例如：

```shell
# Extensions
grep -i "CREATE EXTENSION" schema.sql

# Table partitioning
grep -Ei "PARTITION BY|PARTITION OF" schema.sql

# Table inheritance
grep -i "INHERITS" schema.sql

# Foreign data wrappers
grep -Ei "CREATE SERVER|CREATE FOREIGN TABLE" schema.sql

# Replication
grep -Ei "CREATE PUBLICATION|CREATE SUBSCRIPTION" schema.sql

# Rules
grep -i "CREATE RULE" schema.sql
```

在导入表结构之前，删除或改写不受支持的语句。

此外，还要检查表结构中是否包含不受支持的数据类型、索引访问方法、PL/pgSQL 构造和扩展。更多信息，请参见 [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

#### 行级安全 {#row-level-security}

在导出的表结构中保留行级安全（RLS）相关语句，包括 `ENABLE ROW LEVEL SECURITY`、`FORCE ROW LEVEL SECURITY` 和 `CREATE POLICY`。

在导入数据之前，请确保 `<TARGET_DATABASE_URL>` 中的角色具有所需的表权限。如果 RLS 策略适用于该角色，则每一行导入的数据都必须满足目标表的策略。否则，`COPY FROM STDIN` 会因 `new row violates row-level security policy` 而失败。

如果你需要导入会被这些策略拒绝的行，请让数据库管理员使用一个被授予权限可绕过 RLS 的独立迁移角色来执行导入。不要为了迁移而向应用角色授予 `BYPASSRLS`。迁移完成后，移除所有仅为迁移而授予的权限。

`pg_dump` 工具不会导出数据库角色。如果某个 RLS 策略引用了特定角色，请在导入表结构之前，先在目标实例中创建该角色。

例如：

```shell
psql "<TARGET_DATABASE_URL>" \
  -c "CREATE ROLE app_user LOGIN PASSWORD '<PASSWORD>'"
```

`--no-owner` 选项会省略对象所有权语句，`--no-privileges` 会省略 `GRANT` 和 `REVOKE` 语句。

在导入表结构和数据之后，为应用角色恢复所需的数据库模式、表和序列权限，以及角色成员关系。更多信息，请参见 [PostgreSQL 身份验证和角色](/tidb-cloud/starter/pg-auth-roles.md)。

#### SERIAL 和标识列 {#serial-and-identity-columns}

由 `pg_dump` 生成的表结构可能包含 PostgreSQL 特有的 `SERIAL` 默认值形式和标识列，这些内容在导入前需要调整。

对于 `SERIAL` 或 `BIGSERIAL` 默认值，请从 `nextval()` 表达式中移除 `::regclass` 类型转换。例如：

```sql
-- PostgreSQL dump output
DEFAULT nextval('public.users_id_seq'::regclass)

-- Compatible form
DEFAULT nextval('public.users_id_seq')
```

如果导出文件中包含通过 `ALTER TABLE ... ALTER COLUMN ... ADD GENERATED ... AS IDENTITY` 添加的标识列，请在导入表结构之前，将其改写为使用序列和 `DEFAULT nextval(...)` 表达式的形式。

### 步骤 3：导入表结构 {#step-3-import-the-schema}

使用 `psql` 将已检查的表结构导入到目标 PostgreSQL-compatible {{{ .starter }}} 实例中：

```shell
psql \
  "<TARGET_DATABASE_URL>" \
  -v ON_ERROR_STOP=1 \
  -f schema.sql
```

`ON_ERROR_STOP=1` 选项会使 `psql` 在导入出错时立即停止，从而更容易定位并修复不受支持的语句。

### 步骤 4：迁移数据 {#step-4-migrate-the-data}

表结构成功导入后，将数据从源 PostgreSQL 数据库流式传输到目标实例：

```shell
pg_dump \
  --data-only \
  --no-owner \
  --no-privileges \
  "<SOURCE_DATABASE_URL>" \
  | psql "<TARGET_DATABASE_URL>" -v ON_ERROR_STOP=1
```

默认情况下，普通 `pg_dump` 数据流使用 PostgreSQL `COPY` 语句。当该数据流通过管道传递给 `psql` 时，`COPY ... FROM stdin` 语句会通过 PostgreSQL wire 协议将数据导入 PostgreSQL-compatible {{{ .starter }}}。

PostgreSQL-compatible {{{ .starter }}} 支持 text 和 CSV 格式的 `COPY` 数据传输。不支持 binary `COPY`。

### 使用 `\copy` 迁移单个表 {#migrate-individual-tables-using-copy}

你也可以使用 `psql` 和 `\copy` 迁移单个表。

从源 PostgreSQL 数据库导出表：

```shell
psql "<SOURCE_DATABASE_URL>" \
  -c "\copy public.users TO 'users.csv' WITH (FORMAT csv, HEADER)"
```

将表导入目标实例：

```shell
psql "<TARGET_DATABASE_URL>" \
  -c "\copy public.users FROM 'users.csv' WITH (FORMAT csv, HEADER)"
```

导入数据之前，请确保目标表已经存在。

#### 恢复序列值 {#restore-sequence-values}

使用 `\copy` 迁移单个表时，序列值不会自动传输。

如果你的表使用了 `SERIAL`、`BIGSERIAL` 或显式创建的序列，请在导入数据后恢复序列状态，以防止后续插入时出现重复键错误。

在源端写入已停止的情况下，对源 PostgreSQL 数据库运行以下查询以获取序列状态：

```sql
SELECT last_value, is_called
FROM public.users_id_seq;
```

导入表数据后，使用 `setval()` 在目标实例中恢复序列状态。

例如，如果源序列的 `last_value = 3` 且 `is_called = true`，请运行：

```sql
SELECT setval('public.users_id_seq', 3, true);
```

请将其中的值替换为从源数据库获取到的实际 `last_value` 和 `is_called` 值。

对每个与已迁移表关联的序列重复此过程。

> **Note:**
>
> 不支持 SQL 级别的 `COPY (SELECT ...) TO STDOUT` 语法。请改用表形式的 `\copy`。

## 验证迁移后的数据 {#verify-the-migrated-data}

迁移完成后，在将应用流量切换到目标数据库之前，请先验证目标数据库。

### 验证表结构 {#verify-the-schema}

使用 `psql` 检查迁移后的表结构，并验证所需的表、索引、约束、序列、函数及其他对象是否存在。

例如：

```shell
psql "<TARGET_DATABASE_URL>" -c "\dt"
```

### 验证行数 {#verify-row-counts}

比较源数据库和目标数据库之间的行数。

例如：

```sql
SELECT count(*) FROM users;
SELECT count(*) FROM orders;
```

### 验证序列 {#verify-sequences}

如果你的应用使用序列、`SERIAL` 或 `BIGSERIAL`，请验证序列值是否与导入的数据一致。

例如：

```sql
SELECT last_value FROM users_id_seq;
SELECT max(id) FROM users;
```

### 验证你的应用 {#verify-your-application}

将你的应用连接到 PostgreSQL-compatible {{{ .starter }}} 实例，并运行应用测试套件。

请特别关注依赖 PostgreSQL 特性且这些特性不受支持或行为不同的应用逻辑。更多信息，请参见 [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## 限制 {#limitations}

规划迁移时，请注意以下限制：

- 在公测期间，PostgreSQL-compatible {{{ .starter }}} 支持使用 `psql` 配合 `pg_dump` `COPY` 数据流以及表形式的 `\copy` 进行迁移。
- 不支持 PostgreSQL 逻辑复制和流复制。对于最终迁移，请在导出表结构和数据之前停止源端写入，并在迁移验证和应用切换完成之前保持暂停状态。
- `COPY` 协议支持 text 和 CSV 格式。不支持 binary `COPY`。
- 不支持 SQL 级别的 `COPY (SELECT ...) TO STDOUT` 语法。对于单表迁移，请使用表形式的 `\copy`。
- 某些 PostgreSQL 数据库模式对象、数据类型、索引访问方法、扩展和 PL/pgSQL 构造不受支持或行为不同。迁移前请查看 [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。
- 迁移后的文本数据必须使用有效的 UTF-8 编码。
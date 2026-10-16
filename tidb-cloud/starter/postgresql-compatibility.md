---
title: PostgreSQL 兼容性
summary: 了解兼容 PostgreSQL 的 TiDB Cloud Starter 与 PostgreSQL 的兼容性，包括不支持的功能和行为差异。
---

# PostgreSQL 兼容性

兼容 PostgreSQL 的 {{{ .starter }}} 实例支持 PostgreSQL wire 协议（pgwire v3）、常见的 PostgreSQL SQL 语法以及应用模式。大多数 PostgreSQL 客户端、驱动和 ORM 都可以使用标准的 PostgreSQL 连接字符串进行连接。

但是，其实现与 PostgreSQL 并不完全相同。某些 PostgreSQL 功能不受支持或行为有所不同，尤其是那些依赖 PostgreSQL 特有的存储、复制、扩展或事务语义的功能。

> **Note:**
>
> 本页面介绍兼容 PostgreSQL 的 {{{ .starter }}} 实例的一般 PostgreSQL 兼容性。不适用于兼容 MySQL 的 TiDB 集群。
>
> 在公测期间，兼容性覆盖范围和行为可能会继续演进。在迁移生产工作负载之前，请验证你的应用所依赖的 PostgreSQL 功能。

## 支持的功能 {#supported-features}

兼容 PostgreSQL 的 {{{ .starter }}} 实例支持以下 PostgreSQL 功能：

+ **Wire protocol**：PostgreSQL wire 协议 v3，包括 Simple Query 和 Extended Query（`Parse`/`Bind`/`Describe`/`Execute`）。
+ **DDL**：表的 `CREATE`、`ALTER` 和 `DROP`；B-tree、GIN 和 HNSW 索引；视图；物化视图；数据库模式；序列；函数；触发器；类型；以及排序规则。
+ **DML**：带 `RETURNING` 的 `INSERT`、`UPDATE` 和 `DELETE`，以及 `INSERT ... ON CONFLICT`（upsert）。
+ **查询**：连接（inner、left、right、full outer、cross 和 lateral）、公用表表达式（CTEs）、递归 CTE、窗口函数、子查询以及集合操作（`UNION`、`INTERSECT` 和 `EXCEPT`）。
+ **事务**：`BEGIN`、`COMMIT`、`ROLLBACK`、保存点和 autocommit。
+ **数据类型**：Boolean、integer、bigint、double precision、numeric、text、varchar、bytea、timestamp/timestamptz、date、time、interval、UUID、JSON/JSONB、数组、serial/bigserial、vector、tsvector 和 tsquery。
+ **PL/pgSQL**：函数、存储过程、控制流和动态 `EXECUTE`，但有一些限制。不支持 `WHILE`、`FOREACH` 和游标。`EXCEPTION` 和嵌套块需要在 `DO` 块中使用。
+ **触发器**：`INSERT`、`UPDATE` 和 `DELETE` 上的 `BEFORE` 和 `AFTER` 触发器，但有一些限制。更多信息，参见[触发器](#triggers)。
+ **索引**：B-tree（默认）、GIN、部分索引、表达式索引、`CREATE INDEX CONCURRENTLY` 和 HNSW 向量索引。不支持 GiST、Hash、SP-GiST 和 BRIN 索引。

## 不支持的功能 {#unsupported-features}

以下 PostgreSQL 功能不受支持：

+ 表分区，包括 `RANGE`、`LIST` 和 `HASH` 分区。
+ 表继承。
+ Foreign data wrappers（FDW）。
+ 表空间。
+ 使用 `CREATE RULE` 创建的规则。
+ 逻辑复制。
+ 流复制。
+ 真正的 `SERIALIZABLE` 隔离。
+ `DEFERRABLE` 事务。
+ PostgreSQL 大对象（基于 OID 的大对象存储）。对于二进制数据，请改用 `BYTEA`。
+ `XML`、`CIDR` 和 `MACADDR` 数据类型。
+ PostgreSQL 范围类型，但 `INT4RANGE` 提供部分支持。
+ 除 PL/pgSQL 之外的过程语言，例如 PL/Python、PL/Perl 和 PL/v8。
+ PL/pgSQL `WHILE` 循环、`FOREACH` 循环和游标操作。
+ 自定义或第三方 PostgreSQL 扩展。

## 与 PostgreSQL 的差异 {#differences-from-postgresql}

### 事务隔离 {#transaction-isolation}

`READ COMMITTED` 是默认的事务隔离级别。支持 `READ COMMITTED` 和 `REPEATABLE READ`。

`READ UNCOMMITTED` 的行为与 `READ COMMITTED` 相同，这与 PostgreSQL 的行为一致。

不支持 PostgreSQL Serializable Snapshot Isolation（SSI）。如果你通过 PostgreSQL wire 协议请求 `SERIALIZABLE`，该事务会降级为 `REPEATABLE READ`，并返回一条警告。

例如：

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
SHOW transaction_isolation;
```

实际生效的隔离级别是 `REPEATABLE READ`。

如果你的应用依赖 PostgreSQL 的 `SERIALIZABLE` 语义，请根据需要审查并重新设计事务逻辑。显式行锁或数据库约束可以保护特定不变量，但它们并不能提供 PostgreSQL Serializable Snapshot Isolation（SSI）语义。

### 数据类型 {#data-types}

大多数常用的 PostgreSQL 数据类型都受支持，但以下类型存在兼容性差异：

| PostgreSQL 类型 | 行为 |
| --- | --- |
| `SMALLINT` / `INT2` | 可接受，并在内部存储为 32 位整数。不会强制执行 PostgreSQL `SMALLINT` 的取值范围（-32768 到 32767）。 |
| `REAL` / `FLOAT4` | 可接受，并在内部存储为 `DOUBLE PRECISION`。不会保留 PostgreSQL 单精度浮点语义。 |
| `CHAR(n)` / `CHARACTER(n)` | 可接受，并在内部存储为 `VARCHAR`。值不会像 PostgreSQL 那样用空格填充，因此与带空格填充的字符串进行比较时，结果可能不同。 |
| `INET` | 支持 IPv4 和 IPv6 主机或网络地址的相等比较和排序。不支持 PostgreSQL 特有的网络运算符和函数。 |
| `INT4RANGE` | 部分支持。支持相等（`=`）和重叠（`&&`）运算符。不支持包含运算符（`@>` 和 `<@`）。PostgreSQL 范围访问器函数（如 `upper()` 和 `isempty()`）不可用，或行为不符合预期。 |
| 复合类型 | 可以声明并使用文本字面量写入，但无法逐字段读取值。 |
| `BIT` / `VARBIT` | 可接受，但存在兼容性差异。值采用 `BYTEA` 语义，且不会强制执行声明的位长度。超长值会被保留，而不是被拒绝或截断。不支持 PostgreSQL 位字符串字面量，例如 `B'1010'`。 |
| 数组 | 支持一维数组。不支持多维数组。 |

以下 PostgreSQL 数据类型不受支持：

+ `XML`
+ `CIDR`
+ `MACADDR`
+ `MONEY`
+ `INT8RANGE`
+ `NUMRANGE`
+ `DATERANGE`
+ `TSRANGE`
+ `TSTZRANGE`

### DDL 和数据库模式行为 {#ddl-and-schema-behavior}

大多数常见的 PostgreSQL DDL 都受支持，但某些操作有所不同：

+ 支持 `CREATE TABLE AS` 和 `SELECT INTO`，但生成的表会包含一个额外的 `_rowid` 主键列，并且在 `SELECT *` 中可见。
+ `ALTER SEQUENCE` 仅支持与所有权相关的操作，例如 `OWNER TO` 和 `OWNED BY`。其他子句（包括 `RESTART`、`INCREMENT BY` 和 `RENAME TO`）不受支持。要修改序列的当前值，请使用 `setval()`。
+ `TRUNCATE` 仅支持基本的单表形式。不支持多表 `TRUNCATE` 以及 `CASCADE`、`RESTRICT`、`ONLY`、`RESTART IDENTITY` 和 `CONTINUE IDENTITY` 等可选子句。
+ 外键支持 `CASCADE`、`SET NULL`、`SET DEFAULT`、`RESTRICT` 和 `NO ACTION` 引用操作。
+ 外键依赖关系处理方式与 PostgreSQL 不同。删除被引用表时（包括使用 `CASCADE` 或 `RESTRICT`），可能会留下悬空的外键约束。这些约束可能导致针对 `pg_constraint` 和 `information_schema.referential_constraints` 的查询失败。为避免此问题，请先删除引用这些表的外键约束，再删除被引用表。
+ 不支持延迟外键强制检查。使用 `DEFERRABLE INITIALLY DEFERRED` 声明的外键约束会被接受，但会立即强制执行，而不是在事务提交时执行。依赖延迟外键检查的应用可能会遇到事务失败。
+ 支持枚举类型，但枚举值按标签文本排序，而不是按声明顺序排序。
+ 不支持 PostgreSQL 表分区和表继承。

> **Note:**
>
> 如果已经存在悬空的外键约束，请使用 `ALTER TABLE ... DROP CONSTRAINT` 删除该约束，或删除引用表。使用相同名称重新创建被引用表，并不会恢复原有的外键依赖关系。

### 索引 {#indexes}

支持 B-tree、GIN 和 HNSW 索引访问方法。

同时支持唯一索引、表达式索引、部分索引和 `CREATE INDEX CONCURRENTLY`。

以下 PostgreSQL 索引访问方法不受支持：

+ GiST
+ Hash
+ SP-GiST
+ BRIN

HNSW 是向量工作负载中受支持的近似最近邻索引类型。它还有额外的结构和查询形状要求。

TiDB Cloud 未提供的其他 pgvector 索引类型（例如 IVFFlat）不可用。

### `COPY` {#copy}

`COPY ... FROM STDIN` 支持通过 PostgreSQL wire 协议使用 text 和 CSV 格式。

以下 PostgreSQL `COPY` 能力不受支持：

+ Binary `COPY`
+ `COPY (SELECT ...) TO STDOUT`

### PL/pgSQL {#pl-pgsql}

PL/pgSQL 提供部分支持。支持变量、赋值、`SELECT INTO`、`IF`/`ELSIF`/`ELSE`、`FOR` 循环、`PERFORM`、`EXIT`、`CONTINUE`、`RAISE` 和动态 `EXECUTE` 等常见结构。

适用以下限制：

+ 不支持 `WHILE` 循环。
+ 不支持 `FOREACH` 循环。
+ 不支持游标和 `REFCURSOR` 操作。
+ 带有 `BEGIN ... EXCEPTION` 的异常处理仅在 `DO` 块中受支持。
+ 嵌套过程块仅在 `DO` 块中受支持。

> **Note:**
>
> 某些 PL/pgSQL 语句仅在调用函数时才会被验证，而不是在创建函数时验证。因此，即使函数包含不受支持的结构，`CREATE FUNCTION` 也可能成功。
>
> 为验证兼容性，请在创建后通过执行函数进行测试。

### 触发器 {#triggers}

支持 `INSERT`、`UPDATE` 和 `DELETE` 上的 `BEFORE` 和 `AFTER` 触发器，但存在以下兼容性差异：

+ `BEFORE` 触发器函数不能使用循环、PL/pgSQL `CASE` 语句、动态 `EXECUTE`、异常处理器或嵌套块。
+ `FOR EACH STATEMENT` 会被接受，但执行时采用逐行语义，而不是 PostgreSQL 的语句级语义。
+ 在 `AFTER` 触发器中，单独的 `RETURN NEW` 或 `RETURN OLD` 必须作为其所在行的唯一语句出现。

### 扩展 {#extensions}

兼容 PostgreSQL 的 {{{ .starter }}} 实例提供一组预定义的扩展和内置能力。

无法安装任意自定义或第三方 PostgreSQL 扩展。只有 TiDB Cloud 明确支持的扩展可用。

可用扩展列表及各扩展的特定限制，请参见[PostgreSQL 扩展](/tidb-cloud/starter/pg-extensions-overview.md)。

### 复制 {#replication}

不支持 PostgreSQL 逻辑复制和流复制。

某些 publication 和 replication-slot 系统目录对象或函数可能出于 PostgreSQL 兼容性而存在，但它们并不提供可用的复制或变更数据捕获（CDC）能力。不支持 `CREATE SUBSCRIPTION`。

### 系统目录和工具 {#system-catalogs-and-tooling}

兼容 PostgreSQL 的 {{{ .starter }}} 实例实现了常用的 `pg_catalog` 和 `information_schema` 对象，用于数据库模式自省。

其系统目录表面并不与 PostgreSQL 完全一致。某些系统目录视图、列、统计信息以及 PostgreSQL 特有的服务器函数不可用，或仅部分实现。

依赖 PostgreSQL 特有系统目录或统计信息行为的工具，在使用前应先进行验证。

## 迁移注意事项 {#migration-considerations}

在迁移现有的 PostgreSQL 应用程序之前，请先确认其工作负载是否依赖于以下不受支持或行为存在差异的特性，包括：

+ 表分区或表继承。
+ Foreign data wrappers。
+ 逻辑复制或流复制。
+ `SERIALIZABLE` 事务隔离。
+ 不受支持的 PostgreSQL 数据类型。
+ 不受支持的索引访问方法，包括 GiST、Hash、SP-GiST 和 BRIN。
+ 自定义或第三方 PostgreSQL 扩展。
+ 不受支持的 PL/pgSQL 特性，例如 `WHILE` 循环、`FOREACH` 循环、游标，以及函数体中的异常处理。

在迁移生产工作负载之前，请先检查并测试应用程序的数据库模式和查询。
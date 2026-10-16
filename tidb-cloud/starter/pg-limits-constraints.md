---
title: PostgreSQL 限制与约束
summary: 了解适用于 PostgreSQL-compatible TiDB Cloud Starter 的 SQL 引擎限制与约束。
---

# PostgreSQL 限制与约束

本文介绍适用于 PostgreSQL-compatible {{{ .starter }}} 的 SQL 引擎限制与约束。

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} 当前处于公测阶段。在公测期间，这些限制与约束可能会发生变化。

本页重点介绍 SQL 引擎行为。有关 PostgreSQL-compatible {{{ .starter }}} 的每月免费额度和产品级限制，请参见 [TiDB Cloud Starter 方案文档](/tidb-cloud/select-cluster-tier.md#postgresql-compatible-starter)。

## 引擎限制 {#engine-limits}

适用以下限制：

| 资源 | 限制 |
| --- | --- |
| 语句超时 | 默认 60 秒 |
| 空闲事务超时 | 默认 600 秒（10 分钟） |
| 视图嵌套深度 | 64 层 |
| 每个连接的待处理 portal 数 | 32 |
| 标识符长度 | 为兼容 PostgreSQL，报告为 63 字节；当前不强制执行 |
| 编码 | 仅支持 UTF-8 |
| `NUMERIC` 小数位数 | 最多 28 位 |

可以为当前会话修改语句超时。

例如：

```sql
SET statement_timeout = '120s';
```

将其设置为 `0` 可禁用当前会话的超时：

```sql
SET statement_timeout = 0;
```

## 字符编码 {#character-encoding}

PostgreSQL-compatible {{{ .starter }}} 以 UTF-8 存储文本。

服务器编码显示为：

```sql
SHOW server_encoding;
```

结果为：

```text
UTF8
```

请确保导入的文本数据是有效的 UTF-8。

## 标识符长度 {#identifier-length}

为兼容 PostgreSQL，PostgreSQL-compatible {{{ .starter }}} 报告的最大标识符长度为 63 字节。不过，当前并不会强制执行这一限制。

你可以使用以下语句查看报告值：

```sql
SHOW max_identifier_length;
```

结果为：

```text
63
```

与 PostgreSQL 不同，PostgreSQL-compatible {{{ .starter }}} 可以接受超过 63 字节的标识符，而不会自动将其截断。

为保证可移植性，建议将数据库模式、表、列、索引、约束、函数和角色名称控制在 63 字节以内。迁移到 PostgreSQL 时，较长的标识符可能会被截断，从而导致命名冲突或数据库模式迁移失败。

## 递归 CTE 限制 {#recursive-cte-limit}

递归公用表表达式最多支持 1,000 次迭代。

例如：

```sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n

    UNION ALL

    SELECT n + 1
    FROM numbers
    WHERE n < 100
)
SELECT *
FROM numbers;
```

## 数组约束 {#array-constraints}

支持一维数组。

不支持多维 PostgreSQL 数组。

例如：

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    tags TEXT[]
);
```

## COPY 约束 {#copy-constraints}

PostgreSQL `COPY` 协议支持文本和 CSV 数据。

| COPY 能力 | 支持情况 |
| --- | --- |
| 表形式 `COPY FROM` | 支持 |
| 表形式 `COPY TO STDOUT` | 支持 |
| 文本格式 | 支持 |
| CSV 格式 | 支持 |
| 二进制格式 | 不支持 |
| `COPY (SELECT ...) TO STDOUT` | 不支持 |

对于本地文件，请使用 `psql` 的 `\copy` 命令，这样由客户端读取文件并通过 PostgreSQL 连接传输数据。

## 事务约束 {#transaction-constraints}

默认隔离级别为 `READ COMMITTED`。

支持 `REPEATABLE READ`。

`READ UNCOMMITTED` 的行为与 `READ COMMITTED` 相同。

不支持 PostgreSQL Serializable Snapshot Isolation。如果通过 PostgreSQL wire 协议请求 `SERIALIZABLE`，实际生效的隔离级别为 `REPEATABLE READ`。

不支持 `DEFERRABLE` 事务语义。

## 索引约束 {#index-constraints}

支持的索引访问方法包括：

- B-tree
- GIN
- HNSW

以下 PostgreSQL 索引访问方法不受支持：

- GiST
- Hash
- SP-GiST
- BRIN

## HNSW 约束 {#hnsw-constraints}

HNSW 索引有额外要求。

具体包括：

- 一个 HNSW 索引包含一个向量列。
- 被索引列必须声明显式的向量维度，例如 `VECTOR(1024)`。
- 表必须具有单列主键。如果主键类型为 `INTEGER` 或 `BIGINT`，其值必须为非负数。
- 不支持部分 HNSW 索引。
- 查询必须使用兼容的距离运算符和查询形式，优化器才能使用 HNSW 索引。

不满足 HNSW 规划要求的查询会回退为精确扫描。

## 全文搜索约束 {#full-text-search-constraints}

PostgreSQL-compatible 全文搜索具有以下值得注意的约束：

- 仅支持文档中列出的文本搜索配置。
- 不支持使用 `:*` 标记进行前缀匹配。此前缀标记不会被拒绝，而是会被静默忽略，因此前缀查询会表现为精确匹配查询。例如，`to_tsquery('english', 'qui:*')` 会被解释为 `to_tsquery('english', 'qui')`，因此不会匹配 `quick`。在公测期间，请勿依赖前缀匹配。
- `tsquery` 表达式中的词素权重修饰符（例如 `:A`）也会被静默忽略。例如，`to_tsquery('english', 'qui:A')` 会在不带权重修饰符的情况下进行解释。请勿依赖这些修饰符进行加权查询匹配。
- `ts_headline()` 不会高亮中文汉字词项。
- `TSVECTOR` 值的最大大小为 1 MiB。

## PL/pgSQL 约束 {#pl-pgsql-constraints}

PL/pgSQL 支持常见变量、条件语句、`FOR` 循环、动态 SQL、`SELECT ... INTO`、DML `RETURNING ... INTO` 以及其他常见结构。

以下结构不受支持：

- `WHILE`
- `FOREACH`
- 游标操作
- `REFCURSOR`

仅在 `DO` 块中支持异常处理程序和嵌套过程块。

`BEFORE` 触发器函数还有额外的过程限制。

## Trigger 约束 {#trigger-constraints}

支持的触发器时机：

- `BEFORE`
- `AFTER`

支持的事件：

- `INSERT`
- `UPDATE`
- `DELETE`

接受 `FOR EACH STATEMENT`，但当前会按每行行为执行。需要可预测的触发器语义时，请使用 `FOR EACH ROW`。

## Sequence 约束 {#sequence-constraints}

创建 sequence 时，可以指定如下 sequence 选项：

- `START`
- `INCREMENT`
- `MINVALUE`
- `MAXVALUE`
- `CACHE`
- `CYCLE`

`ALTER SEQUENCE` 支持所有权操作，但不支持在 sequence 创建后修改这些生成选项。

使用 `setval()` 重新定位现有 sequence。

## 自定义类型约束 {#custom-type-constraints}

支持 enum 和 composite 类型，但在兼容性方面存在差异。composite 类型可以使用文本字面量进行声明和写入，但无法单独读取其字段。

对于 enum 类型，比较和排序基于标签文本，而不是声明顺序。

如果应用逻辑依赖 enum 顺序，请使用显式 rank，而不要依赖 enum 比较顺序。

## 排序规则约束 {#collation-constraints}

支持自定义排序规则，但有以下限制：

- 未显式指定自定义排序规则的文本使用按字节排序。
- 聚合和窗口 `ORDER BY` 表达式不会应用自定义排序规则顺序。
- 自定义排序规则未在 PostgreSQL 系统目录中得到完整表示。

## 系统目录约束 {#system-catalog-constraints}

兼容 PostgreSQL 的系统目录旨在支持常见的自省工作流，但与上游 PostgreSQL 并不完全相同。

具体来说：

- 并非每个上游系统目录关系或视图都可用。
- 某些系统目录关系仅公开上游 PostgreSQL 列的一部分。
- 某些目录对象可能出于兼容性而存在，即使对应的 PostgreSQL 功能并不受支持。
- `information_schema.views` 不可用。

## 扩展限制 {#extension-limits}

扩展和内置能力可能各自有其限制。

例如：

- 向量搜索具有 HNSW 索引和查询形状限制。
- 全文搜索具有分词器和查询限制。
- Parquet 导入仅支持文档中说明的 URL scheme 和类型映射。
- 仅支持由 TiDB Cloud 明确提供的扩展。
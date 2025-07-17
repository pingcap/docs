---
title: TiDB 特定函数
summary: 了解 TiDB 特定函数的用法。
---

# TiDB 特定函数

以下函数是 TiDB 扩展功能，不存在于 MySQL 中：

<CustomContent platform="tidb">

| 函数名 | 函数描述 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | 返回当前会话绑定的资源组名称。详见 [使用资源控制实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 在指定时间范围内读取最新数据。详见 [使用 `AS OF TIMESTAMP` 子句读取历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回当前的 [TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 解码二进制执行计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 将 TiDB 编码的键条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。这些编码的键可以在某些系统表和日志输出中找到。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 查询集群中一组 SQL digest 对应的规范化 SQL 语句（无格式和参数的形式）。 |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | 编码索引键。 |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | 编码记录键。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 获取查询字符串的 digest。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 检查你连接的 TiDB 实例是否为 DDL 所有者。DDL 所有者是代表集群中所有节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | 返回某个键的 [MVCC（多版本并发控制）](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) 信息。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 从 TiDB TSO 时间戳中提取物理时间戳。详见： [`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 提取 TiDB TSO 时间戳中的逻辑时间部分。 |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 查询行的校验和值。此函数只能在 FastPlan 过程中在 `SELECT` 语句中使用。即，可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 进行查询。详见：[单行数据完整性验证](/ticdc/ticdc-integrity-check.md)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 创建分片索引以分散索引热点。分片索引是以 `TIDB_SHARD` 函数作为前缀的表达式索引。|
| [`TIDB_VERSION()`](#tidb_version) | 返回带有额外构建信息的 TiDB 版本。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回数字的哈希值。此函数与 Vitess 的 `HASH` 函数兼容，旨在帮助从 Vitess 迁移数据。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 函数名 | 函数描述 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | 返回当前会话绑定的资源组名称。详见 [使用资源控制实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 在指定时间范围内读取最新数据。详见 [使用 `AS OF TIMESTAMP` 子句读取历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回当前的 [TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 解码二进制执行计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 将 TiDB 编码的键条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构。这些编码的键可以在某些系统表和日志输出中找到。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 查询集群中一组 SQL digest 对应的规范化 SQL 语句（无格式和参数的形式）。 |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | 编码索引键。 |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | 编码记录键。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 获取查询字符串的 digest。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 检查你连接的 TiDB 实例是否为 DDL 所有者。DDL 所有者是代表集群中所有节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 从 TiDB TSO 时间戳中提取物理时间戳。详见： [`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | 返回某个键的 [MVCC（多版本并发控制）](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) 信息。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 提取 TiDB TSO 时间戳中的逻辑时间部分。 |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 查询行的校验和值。此函数只能在 FastPlan 过程中在 `SELECT` 语句中使用。即，可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 进行查询。详见：[单行数据完整性验证](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 创建分片索引以分散索引热点。分片索引是以 `TIDB_SHARD` 函数作为前缀的表达式索引。|
| [`TIDB_VERSION()`](#tidb_version) | 返回带有额外构建信息的 TiDB 版本。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回数字的哈希值。此函数与 Vitess 的 `HASH` 函数兼容，旨在帮助从 Vitess 迁移数据。 |

</CustomContent>

## CURRENT_RESOURCE_GROUP

`CURRENT_RESOURCE_GROUP()` 函数用于显示当前会话绑定的资源组名称。当启用 [资源控制](/tidb-resource-control-ru-groups.md) 功能时，SQL 语句可用的资源会受到绑定资源组的资源配额限制。

当会话建立时，TiDB 默认会将会话绑定到登录用户绑定的资源组。如果用户未绑定任何资源组，则会话绑定到 `default` 资源组。会话建立后，默认不会更改绑定的资源组，即使通过 [修改绑定到用户的资源组](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information) 改变了用户的绑定资源组。若要更改当前会话的绑定资源组，可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)。

示例：

创建用户 `user1`，创建两个资源组 `rg1` 和 `rg2`，并将用户 `user1` 绑定到资源组 `rg1`：

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP rg1 RU_PER_SEC = 1000;
CREATE RESOURCE GROUP rg2 RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

使用 `user1` 登录并查看当前用户绑定的资源组：

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg1                      |
+--------------------------+
1 row in set (0.00 sec)
```

执行 `SET RESOURCE GROUP` 将当前会话的资源组设置为 `rg2`，然后再次查看当前用户绑定的资源组：

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg2                      |
+--------------------------+
1 row in set (0.00 sec)
```
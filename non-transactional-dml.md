---
title: 非事务性 DML 语句
summary: 了解 TiDB 中的非事务性 DML 语句。在牺牲原子性和隔离性的情况下，将一个 DML 语句拆分成多个语句依次执行，从而提升批量数据处理场景中的稳定性和易用性。
---

# 非事务性 DML 语句

本文档描述了 TiDB 中非事务性 DML 语句的使用场景、使用方法及限制。此外，还将说明其实现原理和常见问题。

非事务性 DML 语句是将一个 DML 语句拆分成多个 SQL 语句（即多个批次）依次执行的方式。它在提升批量数据处理性能和易用性的同时，牺牲了事务的原子性和隔离性。

通常，内存占用较大的事务需要拆分成多个 SQL 语句以绕过事务大小限制。非事务性 DML 将这一过程集成到 TiDB 内核中，实现相同效果。理解通过拆分 SQL 语句的非事务性 DML 语句的效果，有助于优化批量操作。可以使用 `DRY RUN` 语法预览拆分后的语句。

非事务性 DML 语句包括：

- `INSERT INTO ... SELECT`
- `REPLACE INTO .. SELECT`
- `UPDATE`
- `DELETE`

详细语法请参见 [`BATCH`](/sql-statements/sql-statement-batch.md)。

> **注意：**
>
> - 非事务性 DML 语句不保证语句的原子性和隔离性，不等同于原始的 DML 语句。
> - 将 DML 语句重写为非事务性 DML 后，不应假设其行为与原始语句完全一致。
> - 在使用非事务性 DML 前，需要分析拆分的语句是否会相互影响。

## 使用场景

在大数据处理场景中，常常需要对大量数据执行相同操作。如果直接用单个 SQL 语句执行，可能会超出事务大小限制，影响执行性能。

批量数据处理通常与线上应用操作没有时间或数据上的重叠。在没有并发操作的情况下，隔离（ACID 中的 I）是不必要的。如果批量数据操作是幂等的或易于重试，也不需要保证原子性。如果你的应用不需要数据隔离或原子性，可以考虑使用非事务性 DML。

非事务性 DML 主要用于绕过某些场景下的大事务大小限制。用一条语句完成本需手动拆分事务的任务，提升执行效率，减少资源消耗。

例如，为了删除过期数据，如果确保没有应用访问过期数据，可以用非事务性 DML 提高 `DELETE` 的性能。

## 前提条件

在使用非事务性 DML 语句前，请确保满足以下条件：

- 语句不需要原子性，允许部分行被修改，部分行保持不变。
- 语句是幂等的，或你已准备好根据错误信息对部分数据进行重试。如果系统变量 `tidb_redact_log = 1` 和 `tidb_nontransactional_ignore_error = 1`，则此语句必须是幂等的，否则部分失败时无法准确定位失败部分。
- 操作的数据没有其他并发写入，即不会被其他语句同时更新，否则可能出现遗漏写入、错误写入或多次修改同一行的情况。
- 语句不修改自己要读取的数据，否则后续批次会读取前一批写入的数据，容易导致意外结果。

    - 避免在非事务性 `INSERT INTO ... SELECT` 语句中同时修改同一表的分片列，否则多批次可能读取相同的行并多次插入：
        - 不建议使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id+1, value FROM t;`。
        - 推荐使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id, value FROM t;`。
        - 如果分片列 `id` 具有 `AUTO_INCREMENT` 属性，建议使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t(value) SELECT value FROM t;`。
    - 避免在非事务性 `UPDATE`、`INSERT ... ON DUPLICATE KEY UPDATE` 或 `REPLACE INTO` 语句中修改分片列：
        - 例如，非事务性 `UPDATE` 语句，拆分的 SQL 语句依次执行，前一批的修改在下一批提交后被读取，导致同一行数据被多次修改。
        - 这些语句不支持 `BATCH ON test.t.id LIMIT 10000 UPDATE t SET test.t.id = test.t.id-1;`。
        - 不建议使用 `BATCH ON test.t.id LIMIT 1 INSERT INTO t SELECT id+1, value FROM t ON DUPLICATE KEY UPDATE id = id + 1;`。
    - 分片列不应作为 Join 键。例如，以下示例使用 `test.t.id` 作为 Join 键，导致非事务性 `UPDATE` 多次修改同一行：

        ```sql
        CREATE TABLE t(id int, v int, key(id));
        CREATE TABLE t2(id int, v int, key(id));
        INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
        INSERT INTO t2 VALUES (1, 1), (2, 2), (4, 4);
        BATCH ON test.t.id LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
        SELECT * FROM t2; -- (4, 1) (4, 2) (4, 4)
        ```

- 语句符合 [`restrictions`](#restrictions)。
- 不建议对将被此 DML 语句读写的表进行并发 DDL 操作。

> **Warning:**
>
> 如果同时开启 `tidb_redact_log` 和 `tidb_nontransactional_ignore_error`，可能无法获取每个批次的完整错误信息，也不能只重试失败的批次。因此，两个系统变量同时开启时，非事务性 DML 语句必须是幂等的。

## 使用示例

### 使用非事务性 DML 语句

以下部分介绍非事务性 DML 语句的使用方法及示例：

创建表 `t`，结构如下：


```sql
CREATE TABLE t (id INT, v INT, KEY(id));
```

```sql
Query OK, 0 rows affected
```

向表 `t` 插入一些数据。


```sql
INSERT INTO t VALUES (1, 2), (2, 3), (3, 4), (4, 5), (5, 6);
```

```sql
Query OK, 5 rows affected
```

以下操作使用非事务性 DML 语句删除 `v` 列值小于 6 的行。此语句拆分为两个 SQL 语句，批次大小为 2，按 `id` 列分片执行。


```sql
BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6;
```

```sql
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 2              | all succeeded |
+----------------+---------------+
1 row in set
```

检查上述非事务性 DML 语句的删除结果。


```sql
SELECT * FROM t;
```

```sql
+----+---+
| id | v |
+----+---+
| 5  | 6 |
+----+---+
1 row in set
```

以下示例描述如何使用多表连接。首先，创建表 `t2` 并插入数据：

```sql
CREATE TABLE t2(id int, v int, key(id));
INSERT INTO t2 VALUES (1,1), (3,3), (5,5);
```

然后，通过连接表 `t` 和 `t2` 更新 `t2` 中的数据。注意需要指定分片列以及完整的数据库名、表名和列名（`test.t.id`）：

```sql
BATCH ON test.t._tidb_rowid LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
```

查询结果：

```sql
SELECT * FROM t2;
```

```sql
+----+---+
| id | v |
+----+---+
| 1  | 1 |
| 3  | 3 |
| 6  | 5 |
+----+---+
```

### 查看执行进度

在执行非事务性 DML 语句期间，可以使用 `SHOW PROCESSLIST` 查看进度。返回结果中的 `Time` 字段表示当前批次执行的耗时。日志和慢日志也会记录每个拆分语句的执行进度。例如：


```sql
SHOW PROCESSLIST;
```

```sql
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| Id   | User | Host               | db     | Command | Time | State      | Info                                                                                               |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
| 1203 | root | 100.64.10.62:52711 | test   | Query   | 0    | autocommit | /* job 506/500000 */ DELETE FROM `test`.`t1` WHERE `test`.`t1`.`_tidb_rowid` BETWEEN 2271 AND 2273 |
| 1209 | root | 100.64.10.62:52735 | <null> | Query   | 0    | autocommit | show full processlist                                                                              |
+------+------+--------------------+--------+---------+------+------------+----------------------------------------------------------------------------------------------------+
```

### 终止非事务性 DML 语句

可以使用 `KILL TIDB <processlist_id>` 来终止非事务性 DML 语句。TiDB 会取消当前正在执行的批次之后的所有批次。可以从日志中获取执行结果。

关于 `KILL TIDB` 的更多信息，请参见参考 [`KILL`](/sql-statements/sql-statement-kill.md)。

### 查询批次划分语句

在执行非事务性 DML 语句期间，系统会内部使用一条语句将 DML 语句拆分成多个批次。可以在此非事务性 DML 语句中添加 `DRY RUN QUERY` 来查询此批次划分语句。这样 TiDB 不会执行此查询及后续的 DML 操作。

例如，查询 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 执行期间的批次划分语句：


```sql
BATCH ON id LIMIT 2 DRY RUN QUERY DELETE FROM t WHERE v < 6;
```

```sql
+--------------------------------------------------------------------------------+
| query statement                                                                |
+--------------------------------------------------------------------------------+
| SELECT `id` FROM `test`.`t` WHERE (`v` < 6) ORDER BY IF(ISNULL(`id`),0,1),`id` |
+--------------------------------------------------------------------------------+
1 row in set
```

### 查询对应第一个和最后一个批次的语句

要查询非事务性 DML 语句中第一个和最后一个批次对应的实际 DML 语句，可以在此非事务性 DML 语句中添加 `DRY RUN`。这样 TiDB 只会拆分批次，不会执行这些 SQL 语句。由于批次数量可能较多，只会显示第一个和最后一个批次。

例如：

```sql
BATCH ON id LIMIT 2 DRY RUN DELETE FROM t WHERE v < 6;
```

```sql
+-------------------------------------------------------------------+
| split statement examples                                          |
+-------------------------------------------------------------------+
| DELETE FROM `test`.`t` WHERE (`id` BETWEEN 1 AND 2 AND (`v` < 6)) |
| DELETE FROM `test`.`t` WHERE (`id` BETWEEN 3 AND 4 AND (`v` < 6)) |
+-------------------------------------------------------------------+
2 rows in set
```

### 使用优化器提示

如果在 `DELETE` 语句中原本支持优化器提示，则在非事务性 `DELETE` 语句中也支持。提示的位置与普通 `DELETE` 语句相同：


```sql
BATCH ON id LIMIT 2 DELETE /*+ USE_INDEX(t)*/ FROM t WHERE v < 6;
```

## 最佳实践

为了使用非事务性 DML 语句，建议按照以下步骤操作：

1. 选择合适的 [`shard column`](#parameter-description)。推荐使用整数或字符串类型。
2. 在非事务性 DML 语句中添加 `DRY RUN QUERY`，手动执行查询，确认 DML 语句影响的数据范围大致正确。
3. 在非事务性 DML 语句中添加 `DRY RUN`，手动执行查询，检查拆分的语句和执行计划。注意以下几点：

    - 拆分的语句是否能读取到前一批写入的结果，可能引发异常。
    - 索引的选择性。
    - TiDB 自动选择的分片列是否会被修改。

4. 执行非事务性 DML 语句。
5. 如果出现错误，从错误信息或日志中获取具体失败的数据范围，进行重试或手动处理。

## 参数说明

| 参数 | 描述 | 默认值 | 必填 | 推荐值 |
| :-- | :-- | :-- | :-- | :-- |
| Shard column | 用于分片批次的列，例如上述非事务性 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `id` 列。 | TiDB 尝试自动选择分片列（不推荐）。 | 否 | 选择一个能满足 `WHERE` 条件且效率较高的列。 |
| Batch size | 用于控制每个批次的大小。拆分成的 SQL 语句数量即为 DML 操作的批次数，例如上述非事务性 DML 语句中的 `LIMIT 2`。批次越多，单个批次越小。 | N/A | 是 | 1000-1000000。批次过小或过大都会导致性能下降。 |

### 如何选择分片列

非事务性 DML 语句以某列作为数据拆分的依据，即分片列。为了提高执行效率，分片列应使用索引。不同索引和分片列带来的执行效率可能相差数十倍。在选择分片列时，建议考虑以下建议：

- 如果你了解应用的数据分布，根据 `WHERE` 条件，选择拆分后范围较小的列。
    - 理想情况下，`WHERE` 条件能利用分片列的索引，减少每批扫描的数据量。例如，有一张事务表记录每笔事务的开始和结束时间，你想删除所有结束时间在一个月前的事务记录。如果事务的开始时间有索引，且开始和结束时间相对接近，可以选择开始时间列作为分片列。
    - 在不理想的情况下，分片列的数据分布与 `WHERE` 条件完全无关，索引无法减少扫描范围。
- 存在聚簇索引时，建议使用主键（包括 `INT` 主键和 `_tidb_rowid`）作为分片列，以提升效率。
- 选择重复值较少的列。

你也可以选择不指定分片列。此时，TiDB 默认使用 `handle` 的第一个列作为分片列。但如果主键的第一个列类型不支持非事务性 DML（如 `ENUM`、`BIT`、`SET`、`JSON`），则会报错。可以根据应用需求选择合适的分片列。

### 如何设置批次大小

在非事务性 DML 语句中，批次越大，拆分的 SQL 语句越少，每个 SQL 执行越慢。最优批次大小依赖于工作负载。建议从 50000 开始。批次过小或过大都可能导致性能下降。

每个批次的信息存储在内存中，批次数过多会显著增加内存消耗。这也是为什么批次不能太小的原因。存储批次信息的最大内存限制与 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 相同，超出此限制会触发 [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610) 的配置行为。

## 限制

以下是对非事务性 DML 语句的硬性限制。如果不满足这些限制，TiDB 会报错。

- DML 语句不能包含 `ORDER BY` 或 `LIMIT` 子句。
- 不支持子查询或集合操作。
- 分片列必须有索引。索引可以是单列索引，也可以是联合索引的第一个列。
- 必须在 [`autocommit`](/system-variables.md#autocommit) 模式下使用。
- 在启用批量 DML 时不能使用。
- 在设置了 [`tidb_snapshot`](/read-historical-data.md) 时不能使用。
- 不能与 `prepare` 语句配合使用。
- 不支持 `ENUM`、`BIT`、`SET`、`JSON` 类型作为分片列。
- 不支持 [临时表](/temporary-tables.md)。
- 不支持 [公共表表达式](/develop/dev-guide-use-common-table-expression.md)。

## 控制批次执行失败

非事务性 DML 语句不满足原子性，部分批次可能成功，部分批次失败。系统变量 [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610) 控制非事务性 DML 语句的错误处理方式。

例外情况是，若第一批次失败，很可能语句本身有误，此时整个非事务性语句会直接返回错误。

## 工作原理

非事务性 DML 语句的工作原理是将 SQL 语句的自动拆分功能内置到 TiDB 中。没有非事务性 DML 时，你需要手动拆分 SQL 语句。理解非事务性 DML 的行为，可以将其视为用户脚本执行以下任务：

对于非事务性 DML `BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$`，$C$ 为拆分列，$N$ 为批次大小，$P$ 为过滤条件。

1. 根据原始语句的过滤条件 $P$ 和指定的拆分列 $C$，TiDB 查询满足 $P$ 的所有 $C$。TiDB 根据 $N$ 将这些 $C$ 分组为 $B_1 \dots B_k$，并在每个组中保留第一个和最后一个 $C$，记为 $S_i$ 和 $E_i$。此步骤执行的查询语句可通过 [`DRY RUN QUERY`](/non-transactional-dml.md#query-the-batch-dividing-statement) 查看。
2. $B_i$ 涉及的数据是满足 $P_i$：$C$ BETWEEN $S_i$ AND $E_i$ 的子集。可以用 $P_i$ 缩小每个批次需要处理的数据范围。
3. 对于 $B_i$，将上述条件嵌入到原始语句的 `WHERE` 条件中，即变为 WHERE ($P_i$) AND ($P$)。此步骤的执行结果可通过 [`DRY RUN`](/non-transactional-dml.md#query-the-statements-corresponding-to-the-first-and-the-last-batches) 查看。
4. 对所有批次依次执行新语句。每个分组的错误会被收集并合并，作为所有分组完成后的整个非事务性 DML 语句的结果返回。

## 与 batch-dml 的对比

batch-dml 是在执行 DML 语句期间，将事务拆分成多个事务提交的机制。

> **Note:**
>
> 不建议使用已废弃的 batch-dml。当 batch-dml 功能未正确使用时，存在数据索引不一致的风险。

非事务性 DML 语句尚不能完全取代所有 batch-dml 使用场景。它们的主要区别如下：

- 性能：当 [`shard column`](#how-to-select-a-shard-column) 高效时，非事务性 DML 的性能接近 batch-dml；当 shard column 效率较低时，性能明显低于 batch-dml。
- 稳定性：batch-dml 容易因不当使用导致数据索引不一致。非事务性 DML 不会引发数据索引不一致，但不当使用时，行为可能与原始语句不符，应用可能观察到异常行为。详见 [常见问题部分](#non-transactional-delete-has-exceptional-behavior-that-is-not-equivalent-to-ordinary-delete)。

## 常见问题

### 执行多表连接语句时出现 `Unknown column xxx in 'where clause'` 错误

当查询中的 `WHERE` 子句涉及除定义了 [shard column](#parameter-description) 的表之外的其他表时，会出现此错误。例如，以下 SQL 语句中，分片列为 `t2.id`，定义在表 `t2`，但 `WHERE` 子句涉及 `t2` 和 `t3`。

```sql
BATCH ON test.t2.id LIMIT 1 
INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2, t3 WHERE t2.id = t3.id
```

```sql
(1054, "Unknown column 't3.id' in 'where clause'")
```

出现此错误时，可以用 `DRY RUN QUERY` 打印确认查询语句，例如：

```sql
BATCH ON test.t2.id LIMIT 1 
DRY RUN QUERY INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2, t3 WHERE t2.id = t3.id
```

为避免此错误，可以将涉及其他表的条件移到 `JOIN` 的 `ON` 条件中，例如：

```sql
BATCH ON test.t2.id LIMIT 1 
INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2 JOIN t3 ON t2.id = t3.id
```

```
+----------------+---------------+
| number of jobs | job status    |
+----------------+---------------+
| 0              | all succeeded |
+----------------+---------------+
```

### 实际批次大小与指定批次大小不一致

在执行非事务性 DML 语句时，最后一个批次处理的数据可能少于指定的批次大小。

当**分片列存在重复值**时，每个批次会包含该批次最后一个元素的所有重复值，因此此批次的行数可能大于指定的批次大小。

此外，当存在其他并发写入时，每个批次处理的行数也可能与指定的批次大小不同。

### 执行过程中出现 `Failed to restore the delete statement, probably because of unsupported type of the shard column` 错误

分片列不支持 `ENUM`、`BIT`、`SET`、`JSON` 类型。建议指定新的分片列，推荐使用整数或字符串类型。

<CustomContent platform="tidb">

如果在选择的分片列不是上述不支持类型时出现此错误，可以 [获取支持](/support.md) 来自 PingCAP 或社区。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果在选择的分片列不是上述不支持类型时出现此错误，可以 [联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### 非事务性 `DELETE` 存在“异常”行为，不等同于普通 `DELETE`

非事务性 DML 语句不等同于原始的 DML 语句，可能存在以下原因：

- 存在其他并发写入。
- 非事务性 DML 语句修改了语句自身会读取的值。
- 每个批次执行的 SQL 语句可能导致不同的执行计划和表达式计算顺序，因此执行结果可能与原始语句不同。
- DML 语句包含非确定性操作。

## MySQL 兼容性

非事务性语句为 TiDB 特有，不兼容 MySQL。

## 相关链接

* [`BATCH`](/sql-statements/sql-statement-batch.md) 语法
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)

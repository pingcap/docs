---
title: 非事务型 DML 语句
summary: 了解 TiDB 中的非事务型 DML 语句。以牺牲原子性和隔离性为代价，将一个 DML 语句切分为多个语句依次执行，从而提升批量数据处理场景下的稳定性和易用性。
---

# 非事务型 DML 语句

本文档介绍了 TiDB 中非事务型 DML 语句的使用场景、使用方法和限制条件，并对其实现原理和常见问题进行了说明。

非事务型 DML 语句是将一个 DML 语句切分为多个 SQL 语句（即多个批次）依次执行。它以牺牲事务的原子性和隔离性为代价，提升了批量数据处理的性能和易用性。

通常，内存消耗较大的事务需要手动切分为多个 SQL 语句，以绕过事务大小限制。非事务型 DML 语句将这一过程集成到 TiDB 内核中，实现同样的效果。通过切分 SQL 语句，有助于理解非事务型 DML 语句的效果。可以使用 `DRY RUN` 语法预览切分后的语句。

非事务型 DML 语句包括：

- `INSERT INTO ... SELECT`
- `REPLACE INTO .. SELECT`
- `UPDATE`
- `DELETE`

详细语法参见 [`BATCH`](/sql-statements/sql-statement-batch.md)。

> **注意：**
>
> - 非事务型 DML 语句不保证语句的原子性和隔离性，并不等价于原始 DML 语句。
> - DML 语句被重写为非事务型 DML 语句后，不能假设其行为与原始语句一致。
> - 在使用非事务型 DML 前，需要分析切分后的语句是否会相互影响。

## 使用场景

在大数据处理场景下，通常需要对大量数据进行相同操作。如果直接使用单条 SQL 语句操作，事务大小可能超出限制，影响执行性能。

批量数据处理通常与在线应用操作在时间或数据上没有重叠。当不存在并发操作时，隔离性（ACID 中的 I）并非必需。如果批量数据操作是幂等的或易于重试，原子性也不是必须的。如果你的应用不需要数据隔离和原子性，可以考虑使用非事务型 DML 语句。

非事务型 DML 语句用于在特定场景下绕过大事务的大小限制。只需一条语句即可完成原本需要手动切分事务的任务，执行效率更高，资源消耗更少。

例如，删除过期数据时，如果你能确保没有应用会访问这些过期数据，可以使用非事务型 DML 语句提升 `DELETE` 的性能。

## 前提条件

在使用非事务型 DML 语句前，请确保满足以下条件：

- 语句不需要原子性，允许执行结果中部分行被修改，部分行未被修改。
- 语句是幂等的，或者你已准备好根据错误信息对部分数据进行重试。如果系统变量设置为 `tidb_redact_log = 1` 且 `tidb_nontransactional_ignore_error = 1`，则该语句必须是幂等的。否则，当语句部分失败时，无法准确定位失败部分。
- 待操作的数据没有其他并发写入，即不会被其他语句同时 update。否则，可能出现漏写、误写、同一行被多次 update 等异常结果。
- 语句不会 update 自身需要 read 的数据。否则，后续批次会 read 到前一批次写入的数据，容易导致异常结果。

    - 当在非事务型 `INSERT INTO ... SELECT` 语句中，从同一张表 select 并 update 时，避免 update 分片列。否则，多个批次可能会 read 到同一行并多次插入数据：
        - 不推荐使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id+1, value FROM t;`。
        - 推荐使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t SELECT id, value FROM t;`。
        - 如果分片列 `id` 有 `AUTO_INCREMENT` 属性，推荐使用 `BATCH ON test.t.id LIMIT 10000 INSERT INTO t(value) SELECT value FROM t;`。
    - 避免在非事务型 `UPDATE`、`INSERT ... ON DUPLICATE KEY UPDATE` 或 `REPLACE INTO` 语句中 update 分片列：
        - 例如，对于非事务型 `UPDATE` 语句，切分后的 SQL 语句依次执行。前一批次的 update 会被后一批次 read 到，导致同一行数据被多次 update。
        - 这些语句不支持 `BATCH ON test.t.id LIMIT 10000 UPDATE t SET test.t.id = test.t.id-1;`。
        - 不推荐使用 `BATCH ON test.t.id LIMIT 1 INSERT INTO t SELECT id+1, value FROM t ON DUPLICATE KEY UPDATE id = id + 1;`。
    - 分片列不应作为 Join 键。例如，以下示例将分片列 `test.t.id` 作为 Join 键，导致非事务型 `UPDATE` 语句多次 update 同一行：

        ```sql
        CREATE TABLE t(id int, v int, key(id));
        CREATE TABLE t2(id int, v int, key(id));
        INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
        INSERT INTO t2 VALUES (1, 1), (2, 2), (4, 4);
        BATCH ON test.t.id LIMIT 1 UPDATE t JOIN t2 ON t.id = t2.id SET t2.id = t2.id+1;
        SELECT * FROM t2; -- (4, 1) (4, 2) (4, 4)
        ```

- 语句满足[限制条件](#限制条件)。
- 不推荐对该 DML 语句需要 read 或写入的表并发执行 DDL 操作。

> **警告：**
>
> 如果同时开启了 `tidb_redact_log` 和 `tidb_nontransactional_ignore_error`，你可能无法获得每个批次的完整错误信息，也无法只重试失败的批次。因此，如果这两个系统变量都开启，非事务型 DML 语句必须是幂等的。

## 使用示例

### 使用非事务型 DML 语句

以下部分通过示例介绍非事务型 DML 语句的用法：

创建表 `t`，表结构如下：


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

以下操作使用非事务型 DML 语句，删除表 `t` 的 `v` 列值小于整数型 6 的行。该语句被切分为两条 SQL 语句，批次大小为 2，按 `id` 列分片执行。


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

查看上述非事务型 DML 语句的删除结果。


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

以下示例介绍多表 Join 的用法。首先创建表 `t2` 并插入数据：

```sql
CREATE TABLE t2(id int, v int, key(id));
INSERT INTO t2 VALUES (1,1), (3,3), (5,5);
```

然后通过 Join 表 `t` 和 `t2` update 表 `t2` 的数据。注意需要指定分片列，并带上完整的数据库名、表名和列名（`test.t.id`）：

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

在非事务型 DML 语句执行过程中，可以通过 `SHOW PROCESSLIST` 查看进度。返回结果中的 `Time` 字段表示当前批次的执行耗时。日志和慢日志也会记录整个非事务型 DML 执行过程中每个切分语句的进度。例如：


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

### 终止非事务型 DML 语句

要终止非事务型 DML 语句，可以使用 `KILL TIDB <processlist_id>`。此时 TiDB 会在当前批次执行完成后，取消后续所有批次。你可以从日志中获取执行结果。

关于 `KILL TIDB` 的更多信息，参见参考文档 [`KILL`](/sql-statements/sql-statement-kill.md)。

### 查询切分批次的语句

在非事务型 DML 语句执行过程中，内部会用一条语句将 DML 语句切分为多个批次。要查询该切分语句，可以在非事务型 DML 语句中添加 `DRY RUN QUERY`。此时 TiDB 不会执行该查询及后续 DML 操作。

以下语句用于查询 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 执行过程中的切分语句：


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

### 查询首尾批次对应的语句

要查询非事务型 DML 语句中首尾批次实际对应的 DML 语句，可以在该语句中添加 `DRY RUN`。此时 TiDB 只做批次切分，不执行这些 SQL 语句。由于批次数可能很多，不会全部展示，只展示首尾两个批次的语句。


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

### 使用优化器 Hint

如果原本在 `DELETE` 语句中支持优化器 Hint，则在非事务型 `DELETE` 语句中同样支持。Hint 的位置与普通 `DELETE` 语句一致：


```sql
BATCH ON id LIMIT 2 DELETE /*+ USE_INDEX(t)*/ FROM t WHERE v < 6;
```

## 最佳实践

使用非事务型 DML 语句时，推荐按照以下步骤操作：

1. 选择合适的[分片列](#参数说明)。推荐使用整数型或字符串类型。
2. 在非事务型 DML 语句中添加 `DRY RUN QUERY`，手动执行查询，确认 DML 语句影响的数据范围大致正确。
3. 在非事务型 DML 语句中添加 `DRY RUN`，手动执行查询，检查切分后的语句及执行计划。需要重点关注以下几点：

    - 切分后的语句是否会 read 到前一条语句写入的结果，可能导致异常。
    - 索引的选择性。
    - TiDB 自动选择的分片列是否会被 update。

4. 执行非事务型 DML 语句。
5. 如果报错，根据错误信息或日志获取具体失败的数据范围，进行重试或手动处理。

## 参数说明

| 参数 | 说明 | 默认值 | 是否必填 | 推荐值 |
| :-- | :-- | :-- | :-- | :-- |
| 分片列 | 用于批次分片的列，如上述非事务型 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `id` 列。 | TiDB 会尝试自动选择分片列（不推荐）。 | 否 | 选择能以最高效方式满足 `WHERE` 条件的列。 |
| 批次大小 | 用于控制每个批次的大小。批次数即 DML 操作被切分为的 SQL 语句数，如上述非事务型 DML 语句 `BATCH ON id LIMIT 2 DELETE FROM t WHERE v < 6` 中的 `LIMIT 2`。批次数越多，单批次越小。 | N/A | 是 | 1000-1000000。批次过小或过大都会导致性能下降。 |

### 如何选择分片列

非事务型 DML 语句会以某一列为数据分批的依据，即分片列。为获得更高的执行效率，分片列需要使用索引。不同索引和分片列带来的执行效率可能相差数十倍。选择分片列时，建议参考以下建议：

- 如果你了解应用数据分布，根据 `WHERE` 条件选择切分后数据范围较小的列。
    - 理想情况下，`WHERE` 条件能利用分片列的索引，减少每批次需要扫描的数据量。例如有一张记录事务起止时间的交易表，需要删除所有结束时间早于一个月前的交易记录。如果事务的起始时间有索引，且起止时间相近，则可以选择起始时间列作为分片列。
    - 非理想情况下，分片列的数据分布与 `WHERE` 条件完全无关，分片列的索引无法用于缩小数据扫描范围。
- 存在聚簇索引时，推荐使用主键（包括 `INT` 主键和 `_tidb_rowid`）作为分片列，执行效率更高。
- 选择重复值较少的列。

你也可以不指定分片列，此时 TiDB 默认使用 `handle` 的第一列作为分片列。但如果聚簇索引主键的第一列为非事务型 DML 语句不支持的数据类型（即 `ENUM`、`BIT`、`SET`、`JSON`），TiDB 会报错。你可以根据应用需求选择合适的分片列。

### 如何设置批次大小

在非事务型 DML 语句中，批次越大，切分出的 SQL 语句越少，每条 SQL 语句执行越慢。最优批次大小取决于具体 workload，建议从 50000 开始尝试。批次过小或过大都会导致执行效率下降。

每个批次的信息会存储在内存中，因此批次数过多会显著增加内存消耗，这也是批次不能过小的原因。非事务型语句用于存储批次信息的内存上限与 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 相同，超出该上限时的行为由配置项 [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610) 决定。

## 限制条件

以下为非事务型 DML 语句的硬性限制条件，不满足时 TiDB 会报错。

- DML 语句不能包含 `ORDER BY` 或 `LIMIT` 子句。
- 不支持子查询或集合操作。
- 分片列必须有索引。该索引可以是单列索引，也可以是联合索引的第一列。
- 必须在 [`autocommit`](/system-variables.md#autocommit) 模式下使用。
- 启用 batch-dml 时不能使用。
- 设置了 [`tidb_snapshot`](/read-historical-data.md) 时不能使用。
- 不能与 `prepare` 语句一起使用。
- 不支持将 `ENUM`、`BIT`、`SET`、`JSON` 类型作为分片列。
- 不支持[临时表](/temporary-tables.md)。
- 不支持 [Common Table Expression](/develop/dev-guide-use-common-table-expression.md)。

## 控制批次执行失败

非事务型 DML 语句不满足原子性，部分批次可能成功，部分批次可能失败。系统变量 [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610) 用于控制非事务型 DML 语句如何处理错误。

有一个例外：如果第一个批次失败，则很可能是语句本身有误，此时整个非事务型语句会直接报错。

## 实现原理

非事务型 DML 语句的工作原理是将 SQL 语句自动切分内置到 TiDB 中。如果没有非事务型 DML 语句，你需要手动切分 SQL 语句。理解非事务型 DML 语句的行为，可以将其类比为用户脚本完成如下任务：

对于非事务型 DML `BATCH ON $C$ LIMIT $N$ DELETE FROM ... WHERE $P$`，$C$ 为分片列，$N$ 为批次大小，$P$ 为过滤条件。

1. 根据原始语句的过滤条件 $P$ 和指定的分片列 $C$，TiDB 查询所有满足 $P$ 的 $C$。TiDB 按 $N$ 将这些 $C$ 分组为 $B_1 \dots B_k$，每个 $B_i$ 记录其首尾 $C$，分别为 $S_i$ 和 $E_i$。该步骤执行的查询语句可通过 [`DRY RUN QUERY`](/non-transactional-dml.md#查询切分批次的语句) 查看。
2. $B_i$ 涉及的数据是满足 $P_i$ 的子集：$C$ BETWEEN $S_i$ AND $E_i$。可以用 $P_i$ 缩小每个批次需要处理的数据范围。
3. 对于 $B_i$，TiDB 将上述条件嵌入原始语句的 `WHERE` 条件中，变为 WHERE ($P_i$) AND ($P$)。该步骤的执行结果可通过 [`DRY RUN`](/non-transactional-dml.md#查询首尾批次对应的语句) 查看。
4. 对所有批次，依次执行新语句。每个分组的错误会被收集和合并，所有分组完成后作为整个非事务型 DML 语句的结果返回。

## 与 batch-dml 的对比

batch-dml 是一种在 DML 语句执行过程中，将事务切分为多次事务提交的机制。

> **注意：**
>
> 不推荐使用已废弃的 batch-dml。batch-dml 功能使用不当时存在数据索引不一致的风险。

非事务型 DML 语句尚不能完全替代所有 batch-dml 的使用场景。两者主要区别如下：

- 性能：当[分片列](#如何选择分片列)高效时，非事务型 DML 语句的性能接近 batch-dml。当分片列效率较低时，非事务型 DML 语句的性能明显低于 batch-dml。

- 稳定性：batch-dml 易因使用不当导致数据索引不一致。非事务型 DML 语句不会导致数据索引不一致。但使用不当时，非事务型 DML 语句并不等价于原始语句，应用可能观察到异常行为。详见[常见问题](#非事务型-delete-存在与普通-delete-不等价的“异常”行为)。

## 常见问题

### 执行多表 Join 语句报错 `Unknown column xxx in 'where clause'`

当查询条件中拼接的 `WHERE` 涉及的表不包含[分片列](#参数说明)定义的表时，会报此错误。例如，以下 SQL 语句的分片列为 `t2.id`，定义在表 `t2`，但 `WHERE` 条件涉及表 `t2` 和 `t3`。

```sql
BATCH ON test.t2.id LIMIT 1 
INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2, t3 WHERE t2.id = t3.id
```

```sql
(1054, "Unknown column 't3.id' in 'where clause'")
```

如果遇到该错误，可以通过 `DRY RUN QUERY` 打印查询语句进行确认。例如：

```sql
BATCH ON test.t2.id LIMIT 1 
DRY RUN QUERY INSERT INTO t 
SELECT t2.id, t2.v, t3.id FROM t2, t3 WHERE t2.id = t3.id
```

为避免该错误，可以将涉及其他表的条件从 `WHERE` 移到 `JOIN` 的 `ON` 条件。例如：

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

### 非事务型 DML 语句使用表别名时报错 `Unknown column '<alias>.<column>' in 'where clause'`

执行非事务型 DML 语句时，TiDB 内部会构造一条用于切分批次的查询语句，再生成实际切分执行的语句。你可以分别通过 [`DRY RUN QUERY`](/non-transactional-dml.md#查询切分批次的语句) 和 [`DRY RUN`](/non-transactional-dml.md#查询首尾批次对应的语句) 查看这两类语句。

当前版本中，重写后的语句可能不会保留原始 DML 语句中的表别名。因此，如果你在 `WHERE` 条件或其他表达式中使用 `<alias>.<column>` 格式引用列，可能会报 `Unknown column` 错误。

例如，以下语句在某些情况下可能报错：

```sql
BATCH ON t_old.id LIMIT 5000
INSERT INTO t_new
SELECT * FROM t_old AS t
WHERE t.c1 IS NULL;
```

为避免此类错误，建议：

- 非事务型 DML 语句中避免使用表别名。例如，将 `t.c1` 改为 `c1` 或 `t_old.c1`。
- 指定[分片列](#参数说明)时不要使用表别名。例如，将 `BATCH ON t.id` 改为 `BATCH ON db.t_old.id` 或 `BATCH ON t_old.id`。
- 执行前使用 `DRY RUN QUERY` 或 `DRY RUN` 预览重写后的语句，确认是否符合预期。

### 实际批次大小与指定批次大小不一致

在非事务型 DML 语句执行过程中，最后一个批次需要处理的数据量可能小于指定的批次大小。

当**分片列存在重复值**时，每个批次会包含该批次分片列最后一个元素的所有重复值。因此，该批次的行数可能大于指定的批次大小。

此外，存在其他并发写入时，每个批次实际处理的行数也可能与指定批次大小不同。

### 执行时报错 `Failed to restore the delete statement, probably because of unsupported type of the shard column`

分片列不支持 `ENUM`、`BIT`、`SET`、`JSON` 类型。请尝试指定新的分片列。推荐使用整数型或字符串类型的列。

<CustomContent platform="tidb">

如果选择的分片列不是上述不支持的类型仍报错，请[联系 PingCAP 或社区获取支持](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果选择的分片列不是上述不支持的类型仍报错，请[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### 非事务型 `DELETE` 存在与普通 `DELETE` 不等价的“异常”行为

非事务型 DML 语句并不等价于该 DML 语句的原始形式，可能有如下原因：

- 存在其他并发写入。
- 非事务型 DML 语句 update 了自身会 read 的值。
- 每个批次执行的 SQL 语句由于 `WHERE` 条件变化，可能导致执行计划和表达式计算顺序不同，因此执行结果与原始语句不同。
- DML 语句包含非确定性操作。

## MySQL 兼容性

非事务型语句为 TiDB 特有，不兼容 MySQL。

## 参考文档

* [`BATCH`](/sql-statements/sql-statement-batch.md) 语法
* [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)
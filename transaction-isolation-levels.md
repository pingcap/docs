---
title: TiDB 事务隔离级别
summary: 了解 TiDB 中的事务隔离级别。
---

# TiDB 事务隔离级别

<CustomContent platform="tidb">

事务隔离是数据库事务处理的基础之一。隔离性是事务的四个关键属性之一（通常称为 [ACID](/glossary.md#acid)）。

</CustomContent>

<CustomContent platform="tidb-cloud">

事务隔离是数据库事务处理的基础之一。隔离性是事务的四个关键属性之一（通常称为 [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)）。

</CustomContent>

SQL-92 标准定义了四个事务隔离级别：Read Uncommitted、Read Committed、Repeatable Read 和 Serializable。详见下表：

| 隔离级别 | 脏写 | 脏读 | 模糊读 | 幻读 |
| :----------- | :------------ | :------------- | :----------| :-------- |
| READ UNCOMMITTED | 不可能 | 可能 | 可能 | 可能 |
| READ COMMITTED   | 不可能 | 不可能 | 可能 | 可能 |
| REPEATABLE READ  | 不可能 | 不可能 | 不可能 | 可能 |
| SERIALIZABLE     | 不可能 | 不可能 | 不可能 | 不可能 |

TiDB 实现了 Snapshot Isolation (SI) 一致性，出于兼容 MySQL 的考虑，将其标记为 `REPEATABLE-READ`。这与 [ANSI Repeatable Read 隔离级别](#difference-between-tidb-and-ansi-repeatable-read) 和 [MySQL Repeatable Read 级别](#difference-between-tidb-and-mysql-repeatable-read) 存在差异。

> **注意：**
>
> 从 TiDB v3.0 版本开始，事务的自动重试默认已禁用。不建议开启自动重试，因为可能会 **破坏事务的隔离级别**。详情请参阅 [Transaction Retry](/optimistic-transaction.md#automatic-retry)。
>
> 从 TiDB v3.0.8 版本开始，新创建的 TiDB 集群默认使用 [悲观事务模式](/pessimistic-transaction.md)。当前的读（`for update` 读）是 **非可重复读**。详情请参阅 [悲观事务模式](/pessimistic-transaction.md)。

## Repeatable Read 隔离级别

Repeatable Read 隔离级别只会看到事务开始之前已提交的数据，且永远不会看到未提交的数据或在事务执行期间由并发事务提交的变更。然而，事务中的语句会看到在其自身事务内执行的先前更新的效果，即使这些更新尚未提交。

对于在不同节点上运行的事务，开始和提交的顺序取决于从 PD 获取时间戳的顺序。

Repeatable Read 隔离级别的事务不能同时更新同一行。当提交时，如果发现该行在事务开始后被其他事务更新，则该事务会回滚。例如：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- 在悲观事务中，后续执行的 `update` 语句会等待锁，直到持有锁的事务提交或回滚并释放行锁。
commit;                         |
                                |               commit; -- 事务提交失败并回滚。悲观事务可以成功提交。
```

### Difference between TiDB and ANSI Repeatable Read

TiDB 的 Repeatable Read 隔离级别与 ANSI Repeatable Read 隔离级别不同，尽管它们共享相同的名称。根据 [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) 论文中的标准，TiDB 实现的是 Snapshot Isolation 级别。该隔离级别不允许严格的幻读（A3），但允许宽泛的幻读（P3）和写偏差。相比之下，ANSI Repeatable Read 允许幻读，但不允许写偏差。

### Difference between TiDB and MySQL Repeatable Read

TiDB 的 Repeatable Read 隔离级别与 MySQL 的不同。MySQL 的 Repeatable Read 在更新时不会检查当前版本是否可见，这意味着即使在事务开始后该行被更新，仍然可以继续更新。而 TiDB 的乐观事务在遇到事务开始后被更新的行时会回滚并重试。TiDB 的乐观并发控制中的事务重试可能会失败，导致事务最终失败；而在 TiDB 的悲观并发控制和 MySQL 中，更新事务可以成功。

## Read Committed 隔离级别

从 TiDB v4.0.0-beta 版本开始，TiDB 支持 Read Committed 隔离级别。

出于历史原因，目前主流数据库的 Read Committed 隔离级别本质上是 [Oracle 定义的一致性读](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)。为了适应这一情况，TiDB 中悲观事务的 Read Committed 隔离级别本质上也是一种一致性读行为。

> **注意：**
>
> Read Committed 隔离级别仅在 [悲观事务模式](/pessimistic-transaction.md) 中生效。在 [乐观事务模式](/optimistic-transaction.md) 中，将事务隔离级别设置为 `Read Committed` 不会生效，事务仍然使用 Repeatable Read。

从 v6.0.0 版本开始，TiDB 支持使用 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) 系统变量，在读写冲突较少的场景中优化时间戳获取。启用该变量后，TiDB 在执行 `SELECT` 时会尝试使用之前的有效时间戳读取数据。

- 如果在读取过程中没有遇到数据更新，结果会返回给客户端，`SELECT` 语句成功执行。
- 如果在读取过程中遇到数据更新：
    - 如果 TiDB 还未将结果返回给客户端，TiDB 会尝试获取新时间戳并重试该语句。
    - 如果 TiDB 已经向客户端发送了部分数据，TiDB 会向客户端报告错误。每次发送的数据量由 [`tidb_init_chunk_size`](/system-variables.md#tidb_init_chunk_size) 和 [`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size) 控制。

在使用 `READ-COMMITTED` 隔离级别、`SELECT` 语句较多且读写冲突较少的场景中，启用此变量可以避免获取全局时间戳的延迟和开销。

自 v6.3.0 版本起，TiDB 支持通过启用系统变量 [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630) 来优化点写冲突较少的时间戳获取。启用后，在执行点写语句时，TiDB 会尝试使用当前事务的有效时间戳读取和锁定数据。TiDB 在 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) 启用时，读取数据的方式相同。

目前，适用的点写语句类型包括 `UPDATE`、`DELETE` 和 `SELECT ...... FOR UPDATE`。点写语句指使用主键或唯一键作为过滤条件，最终执行操作符包含 `POINT-GET` 的写语句。目前，这三类点写语句的共同点是：先根据键值进行点查询。如果键存在，则锁定该键；如果不存在，则返回空集。

- 如果点写语句的整个读取过程未遇到数据版本更新，TiDB 会继续使用当前事务的时间戳锁定数据。
    - 如果在锁定过程中因旧时间戳发生写冲突，TiDB 会重试获取最新的全局时间戳。
    - 如果在锁定过程中未发生写冲突或其他错误，锁定成功。
- 如果在读取过程中遇到已更新的数据版本，TiDB 会尝试获取新时间戳并重试该语句。

在 `READ-COMMITTED` 隔离级别下，事务中存在大量点写语句但点写冲突较少时，启用此变量可以避免获取全局时间戳的延迟和开销。

## Difference between TiDB and MySQL Read Committed

MySQL 的 Read Committed 隔离级别在大多数情况下与一致性读功能一致，也存在例外，例如 [semi-consistent read](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)。这种特殊行为在 TiDB 中不支持。

## 查看和修改事务隔离级别

你可以通过以下方式查看和修改事务隔离级别。

查看当前会话的事务隔离级别：

```sql
SHOW VARIABLES LIKE 'transaction_isolation';
```

修改当前会话的事务隔离级别：

```sql
SET SESSION transaction_isolation = 'READ-COMMITTED';
```

关于配置和使用事务隔离级别的更多信息，请参阅以下文档：

- [The system variable `transaction_isolation`](/system-variables.md#transaction_isolation)
- [Isolation level](/pessimistic-transaction.md#isolation-level)
- [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)

---
title: 使用 `AS OF TIMESTAMP` 子句读取历史数据
summary: 学习如何使用 `AS OF TIMESTAMP` 语句子句读取历史数据。
---

# 使用 `AS OF TIMESTAMP` 子句读取历史数据

本文档介绍了如何在 TiDB 中使用 [`Stale Read`](/stale-read.md) 功能，通过 `AS OF TIMESTAMP` 子句读取历史数据，包括具体的使用示例和保存历史数据的策略。

TiDB 支持通过标准的 SQL 接口读取历史数据，即 `AS OF TIMESTAMP` SQL 子句，无需特殊的客户端或驱动程序。在数据被更新或删除后，可以使用此 SQL 接口读取更新或删除之前的历史数据。

> **Note:**
>
> 在读取历史数据时，即使当前表结构不同，TiDB 也会返回具有旧表结构的数据。

## 语法

你可以通过以下三种方式在 SQL 中使用 `AS OF TIMESTAMP` 子句：

- [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
- [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
- [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

如果你想指定一个精确的时间点，可以在 `AS OF TIMESTAMP` 子句中设置一个日期时间值或使用时间函数。日期时间的格式类似于 "2016-10-08 16:45:26.999"，毫秒为最小时间单位，但大多数情况下，秒级的时间单位足以指定日期时间，例如 "2016-10-08 16:45:26"。你也可以使用 `NOW(3)` 函数获取到毫秒级的当前时间。如果你想读取几秒前的数据，**建议**使用类似 `NOW() - INTERVAL 10 SECOND` 的表达式。

如果你想指定一个时间范围，可以在子句中使用 [`TIDB_BOUNDED_STALENESS()`](/functions-and-operators/tidb-functions.md#tidb_bounded_staleness) 函数。使用此函数时，TiDB 会在指定的时间范围内选择一个合适的时间戳。"合适"意味着在此时间戳之前没有开始但尚未提交的事务，也就是说，TiDB 可以在访问的副本上执行读操作，且读操作不会被阻塞。你需要用 `TIDB_BOUNDED_STALENESS(t1, t2)` 来调用此函数，`t1` 和 `t2` 是时间范围的两个端点，可以用日期时间值或时间函数来指定。

以下是一些 `AS OF TIMESTAMP` 子句的示例：

- `AS OF TIMESTAMP '2016-10-08 16:45:26'`：告诉 TiDB 读取 2016 年 10 月 8 日 16:45:26 时存储的最新数据。
- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND`：告诉 TiDB 读取 10 秒前存储的最新数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')`：告诉 TiDB 在 2016 年 10 月 8 日 16:45:26 到 16:45:29 的时间范围内，读取尽可能新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())`：告诉 TiDB 在 20 秒前到现在的时间范围内，读取尽可能新的数据。

> **Note:**
>
> 除了指定时间戳外，`AS OF TIMESTAMP` 子句最常用的场景是读取几秒前的数据。如果采用此方式，建议读取时间超过 5 秒的历史数据。
>
> 当你使用 Stale Read 时，需要为你的 TiDB 和 PD 节点部署 NTP 服务，以避免 TiDB 使用的指定时间戳超前于最新的 TSO 分配进度（例如，超前几秒的时间戳）或晚于 GC 安全点时间戳。当指定的时间戳超出服务范围时，TiDB 会返回错误。
>
> 为了减少延迟并提高 Stale Read 数据的时效性，你可以修改 TiKV 的 `advance-ts-interval` 配置项。详情请参见 [Reduce Stale Read latency](/stale-read.md#reduce-stale-read-latency)。

## 使用示例

本节介绍了不同的使用 `AS OF TIMESTAMP` 子句的方法，并配有多个示例。首先介绍如何准备恢复用的数据，然后展示如何在 `SELECT`、`START TRANSACTION READ ONLY AS OF TIMESTAMP` 和 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 中使用。

### 准备数据示例

为了准备恢复用的数据，首先创建一张表并插入几行数据：

```sql
create table t (c int);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
insert into t values (1), (2), (3);
```

```
Query OK, 3 rows affected (0.00 sec)
```

查看表中的数据：

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

查看当前时间：

```sql
select now();
```

```
+---------------------+
| now()               |
+---------------------+
| 2021-05-26 16:45:26 |
+---------------------+
1 row in set (0.00 sec)
```

更新某一行的数据：

```sql
update t set c=22 where c=2;
```

```
Query OK, 1 row affected (0.00 sec)
```

确认该行数据已更新：

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

### 使用 `SELECT` 语句读取历史数据

你可以使用 [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md) 语句，从过去的某个时间点读取数据。

```sql
select * from t as of timestamp '2021-05-26 16:45:26';
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **Note:**
>
> 当用一个 `SELECT` 语句读取多个表时，需要确保 TIMESTAMP EXPRESSION 的格式一致。例如，`select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;`。此外，必须在 `SELECT` 语句中为相关表指定 `AS OF` 信息，否则 `SELECT` 默认读取最新数据。

### 使用 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句读取历史数据

你可以使用 [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md) 语句，开启一个基于过去某个时间点的只读事务。该事务会读取该时间点的历史数据。

```sql
start transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

事务提交后，可以读取最新的数据。

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **Note:**
>
> 如果你用 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句开启事务，它是一个只读事务。在此事务中，写操作会被拒绝。

### 使用 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句读取历史数据

你可以使用 [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md) 语句，将下一次事务设置为基于指定时间点的只读事务。该事务会读取该时间点的历史数据。

```sql
set transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
begin;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

事务提交后，可以读取最新的数据。

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **Note:**
>
> 如果你用 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句开启事务，它是一个只读事务。在此事务中，写操作会被拒绝。
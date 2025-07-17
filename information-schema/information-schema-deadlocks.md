---
title: DEADLOCKS
summary: 了解 `DEADLOCKS` INFORMATION_SCHEMA 表。
---

# DEADLOCKS

`DEADLOCKS` 表显示了当前 TiDB 节点最近发生的若干死锁错误的信息。

```sql
USE INFORMATION_SCHEMA;
DESC deadlocks;
```

输出结果如下：

```sql
+-------------------------+---------------------+------+------+---------+-------+
| Field                   | Type                | Null | Key  | Default | Extra |
+-------------------------+---------------------+------+------+---------+-------+
| DEADLOCK_ID             | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME              | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE               | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID         | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)         | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                | YES  |      | NULL    |       |
| KEY                     | text                | YES  |      | NULL    |       |
| KEY_INFO                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK        | bigint(21) unsigned | NO   |      | NULL    |       |
+-------------------------+---------------------+------+------+---------+-------+
```

`DEADLOCKS` 表使用多行显示同一死锁事件，每行显示涉及该死锁事件的一个事务的信息。如果 TiDB 节点记录了多个死锁错误，每个错误通过 `DEADLOCK_ID` 列区分。相同的 `DEADLOCK_ID` 表示同一死锁事件。注意，`DEADLOCK_ID` **不保证全局唯一，也不会被持久化**。它仅在同一结果集中显示相同的死锁事件。

`DEADLOCKS` 表中每个列字段的含义如下：

* `DEADLOCK_ID`：死锁事件的 ID。当表中存在多个死锁错误时，可以用此列区分不同的死锁事件。
* `OCCUR_TIME`：死锁错误发生的时间。
* `RETRYABLE`：该死锁错误是否可重试。关于可重试死锁错误的描述，见 [Retryable deadlock errors](#retryable-deadlock-errors) 小节。
* `TRY_LOCK_TRX_ID`：尝试获取锁的事务 ID。此 ID 也是事务的 `start_ts`。
* `CURRENT_SQL_DIGEST`：当前在获取锁的事务中执行的 SQL 语句的 digest。
* `CURRENT_SQL_DIGEST_TEXT`：当前在获取锁的事务中执行的 SQL 语句的规范化形式。
* `KEY`：事务试图锁定的阻塞键。该字段的值以十六进制字符串显示。
* `KEY_INFO`：`KEY` 的详细信息。见 [`KEY_INFO`](#key_info) 小节。
* `TRX_HOLDING_LOCK`：当前持有锁并导致阻塞的事务 ID。此 ID 也是事务的 `start_ts`。

<CustomContent platform="tidb">

要调整 `DEADLOCKS` 表中可记录的最大死锁事件数，请调整 TiDB 配置文件中的 [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity) 配置。默认情况下，表中会记录最近 10 个死锁事件的信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

最近 10 个死锁事件的信息会被记录在 `DEADLOCKS` 表中。

</CustomContent>

> **Warning:**
>
> * 只有具有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能查询此表。
> * `CURRENT_SQL_DIGEST` 列中的信息（SQL digest）是由规范化 SQL 语句计算得出的哈希值。`CURRENT_SQL_DIGEST_TEXT` 列中的信息是从语句摘要表中内部查询得到的，因此可能找不到对应的语句。关于 SQL digest 和语句摘要表的详细描述，见 [Statement Summary Tables](/statement-summary-tables.md)。

## `KEY_INFO`

`KEY_INFO` 列显示 `KEY` 列的详细信息，信息以 JSON 格式显示。每个字段的描述如下：

* `"db_id"`：键所属的 schema 的 ID。
* `"db_name"`：键所属的 schema 的名称。
* `"table_id"`：键所属的表的 ID。
* `"table_name"`：键所属的表的名称。
* `"partition_id"`：键所在的分区 ID。
* `"partition_name"`：键所在的分区名称。
* `"handle_type"`：行键（存储一行数据的键）的句柄类型。可能的值如下：
    * `"int"`：句柄类型为 int，表示句柄是行 ID。
    * `"common"`：句柄类型不是 int64。当启用聚簇索引且主键非 int 时显示此类型。
    * `"unknown"`：当前不支持此句柄类型。
* `"handle_value"`：句柄值。
* `"index_id"`：索引键（存储索引的键）所属的索引 ID。
* `"index_name"`：索引键所属的索引名称。
* `"index_values"`：索引键中的索引值。

在上述字段中，如果某个字段的信息不适用或当前不可用，查询结果中会省略该字段。例如，行键信息不包含 `index_id`、`index_name` 和 `index_values`；索引键不包含 `handle_type` 和 `handle_value`；非分区表不显示 `partition_id` 和 `partition_name`；已删除表中的键信息无法获取 schema 信息（如 `table_name`、`db_id`、`db_name` 和 `index_name`），也无法区分表是否为分区表。

> **Note:**
>
> 如果一个键来自启用了分区的表，并且在查询过程中由于某些原因（例如，键所属的表已被删除）无法查询到该键所属的 schema 信息，`table_id` 字段中可能会出现该键所属的分区 ID。这是因为 TiDB 将不同分区的键编码方式与多个独立表的键编码方式相同。因此，当 schema 信息缺失时，TiDB 无法确认该键是属于未分区表还是某个分区的表。

## Retryable deadlock errors

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该小节不适用于 TiDB Cloud。

</CustomContent>

<CustomContent platform="tidb">

> **Note:**
>
> `DEADLOCKS` 表默认不收集可重试死锁错误的信息。如果希望表中收集此类信息，可以调整 TiDB 配置文件中的 [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable) 配置。

</CustomContent>

当事务 A 被已由事务 B 持有的锁阻塞，而事务 B 又被当前事务 A 直接或间接持有的锁阻塞时，就会发生死锁错误。在这种死锁中，可能存在两种情况：

+ 情况 1：事务 B 可能（直接或间接）被在事务 A 启动后、事务 A 被阻塞之前执行的某个语句生成的锁阻塞。
+ 情况 2：事务 B 也可能被事务 A 当前正在执行的语句阻塞。

在情况 1 中，TiDB 会向事务 A 的客户端报告死锁错误，并终止该事务。

在情况 2 中，事务 A 当前执行的语句会在 TiDB 中自动重试。例如，假设事务 A 执行以下语句：

```sql
UPDATE t SET v = v + 1 WHERE id = 1 OR id = 2;
```

事务 B 连续执行以下两个语句：

```sql
UPDATE t SET v = 4 WHERE id = 2;
UPDATE t SET v = 2 WHERE id = 1;
```

然后，如果事务 A 锁定了 `id = 1` 和 `id = 2` 的两行，且两个事务按以下顺序运行：

1. 事务 A 锁定 `id = 1` 的行。
2. 事务 B 执行第一个语句，锁定 `id = 2` 的行。
3. 事务 B 执行第二个语句，尝试锁定 `id = 1` 的行，此行被事务 A 阻塞。
4. 事务 A 尝试锁定 `id = 2` 的行，被事务 B 阻塞，形成死锁。

对于这种情况，由于阻塞其他事务的事务 A 的语句也是当前正在执行的语句，TiDB 会解决对当前语句的悲观锁（以便事务 B 可以继续执行），并重试当前语句。TiDB 内部使用 key hash 来判断是否为此情况。

当发生可重试死锁时，内部的自动重试不会导致事务错误，对客户端是透明的。但如果此类情况频繁发生，可能会影响性能。发生时，可以在 TiDB 日志中看到 `single statement deadlock, retry statement`。

## Example 1

假设表定义和初始数据如下：

```sql
CREATE TABLE t (id int primary key, v int);
INSERT INTO t VALUES (1, 10), (2, 20);
```

按以下顺序执行两个事务：

| Transaction 1                               | Transaction 2                               | 描述                     |
|--------------------------------------|--------------------------------------|----------------------|
| `BEGIN;`                             |                                      |                      |
|                                      | `BEGIN;`                             |                      |
| `UPDATE t SET v = 11 WHERE id = 1;`  |                                      |                      |
|                                      | `UPDATE t SET v = 21 WHERE id = 2;`  |                      |
| `UPDATE t SET v = 12 WHERE id = 2;`  |                                      | 事务 1 被阻塞。          |
|                                      | `UPDATE t SET v = 22 WHERE id = 1;`  | 事务 2 报死锁错误。      |

接下来，事务 2 报死锁错误。此时，查询 `DEADLOCKS` 表：

```sql
SELECT * FROM INFORMATION_SCHEMA.DEADLOCKS;
```

预期输出如下：

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

在 `DEADLOCKS` 表中生成了两行数据。两行的 `DEADLOCK_ID` 均为 `1`，表示这两行属于同一死锁错误。第一行显示在 `"7480000000000000355F728000000000000002"` 键上，ID 为 `"426812829645406216"` 的事务被 ID 为 `"426812829645406217"` 的事务阻塞。第二行显示在 `"7480000000000000355F728000000000000001"` 键上，ID 为 `"426812829645406217"` 的事务被 ID 为 `"426812829645406216"` 的事务阻塞，形成互相阻塞，构成死锁。

## Example 2

假设查询 `DEADLOCKS` 表，得到如下结果：

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809412 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812832017809413 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809413 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000003 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"3"} | 426812832017809414 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809414 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812832017809412 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

上述查询结果中的 `DEADLOCK_ID` 列显示，前两行共同代表一次死锁错误的信息，等待互相阻塞的两个事务形成死锁。后面三行共同代表另一场死锁错误的信息，形成环状等待的三个事务构成死锁。

## CLUSTER_DEADLOCKS

`CLUSTER_DEADLOCKS` 表返回整个集群中每个 TiDB 节点最近的死锁错误信息，是各节点 `DEADLOCKS` 表的合并信息。`CLUSTER_DEADLOCKS` 还增加了 `INSTANCE` 列，用于显示节点的 IP 地址和端口，以区分不同的 TiDB 节点。

注意，由于 `DEADLOCK_ID` 不保证全局唯一，在 `CLUSTER_DEADLOCKS` 表的查询结果中，需要结合 `INSTANCE` 和 `DEADLOCK_ID` 来区分不同死锁错误的信息。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_DEADLOCKS;
```

输出如下：

```sql
+-------------------------+---------------------+------+------+---------+-------+
| Field                   | Type                | Null | Key  | Default | Extra |
+-------------------------+---------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)         | YES  |      | NULL    |       |
| DEADLOCK_ID             | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME              | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE               | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID         | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)         | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                | YES  |      | NULL    |       |
| KEY                     | text                | YES  |      | NULL    |       |
| KEY_INFO                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK        | bigint(21) unsigned | NO   |      | NULL    |       |
+-------------------------+---------------------+------+------+---------+-------+
```
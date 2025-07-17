---
title: DATA_LOCK_WAITS
summary: 了解 `DATA_LOCK_WAITS` information_schema 表。
---

# DATA_LOCK_WAITS

`DATA_LOCK_WAITS` 表显示集群中所有 TiKV 节点的进行中的锁等待信息，包括悲观事务的锁等待信息以及被阻塞的乐观事务信息。

```sql
USE information_schema;
DESC data_lock_waits;
```

```
+------------------------+---------------------+------+------+---------+-------+
| Field                  | Type                | Null | Key  | Default | Extra |
+------------------------+---------------------+------+------+---------+-------+
| KEY                    | text                | NO   |      | NULL    |       |
| KEY_INFO               | text                | YES  |      | NULL    |       |
| TRX_ID                 | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_HOLDING_TRX_ID | bigint(21) unsigned | NO   |      | NULL    |       |
| SQL_DIGEST             | varchar(64)         | YES  |      | NULL    |       |
| SQL_DIGEST_TEXT        | text                | YES  |      | NULL    |       |
+------------------------+---------------------+------+------+---------+-------+
```

`DATA_LOCK_WAITS` 表中每个字段的含义如下：

* `KEY`：等待锁的键，十六进制形式。
* `KEY_INFO`：`KEY` 的详细信息。详见 [KEY_INFO](#key_info) 部分。
* `TRX_ID`：等待锁的事务的 ID。该 ID 也是事务的 `start_ts`。
* `CURRENT_HOLDING_TRX_ID`：当前持有锁的事务的 ID。该 ID 也是事务的 `start_ts`。
* `SQL_DIGEST`：当前阻塞在锁等待事务中的 SQL 语句的摘要。
* `SQL_DIGEST_TEXT`：当前阻塞在锁等待事务中的标准化 SQL 语句（不包含参数和格式化），对应 `SQL_DIGEST`。

> **Warning:**
>
> * 只有具有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能查询此表。
> * 目前，乐观事务的 `SQL_DIGEST` 和 `SQL_DIGEST_TEXT` 字段为 `null`（表示不可用）。作为变通方案，为了查明引起阻塞的 SQL 语句，可以将此表与 [`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) 连接，以获取所有乐观事务的 SQL 语句。
> * 在查询过程中，`DATA_LOCK_WAITS` 表中的信息是实时从所有 TiKV 节点获取的。目前，即使查询带有 `WHERE` 条件，信息采集仍会在所有 TiKV 节点上进行。如果你的集群规模较大且负载较高，查询此表可能会带来潜在的性能抖动风险。因此，请根据实际情况谨慎使用。
> * 不同 TiKV 节点中的信息不保证是同一时间的快照。
> * `SQL_DIGEST` 列中的信息（SQL 摘要）是由标准化 SQL 语句计算得出的哈希值。`SQL_DIGEST_TEXT` 列中的信息是从语句摘要表内部查询得到的，因此可能无法在内部找到对应的语句。关于 SQL 摘要和语句摘要表的详细说明，参见 [Statement Summary Tables](/statement-summary-tables.md)。

## `KEY_INFO`

`KEY_INFO` 列显示 `KEY` 列的详细信息，信息以 JSON 格式展示。每个字段的说明如下：

* `"db_id"`：键所属的 schema 的 ID。
* `"db_name"`：键所属的 schema 的名称。
* `"table_id"`：键所属的表的 ID。
* `"table_name"`：键所属的表的名称。
* `"partition_id"`：键所在的分区的 ID。
* `"partition_name"`：键所在的分区的名称。
* `"handle_type"`：行键（存储一行数据的键）的句柄类型。可能的值如下：
    * `"int"`：句柄类型为整数，表示句柄是行 ID。
    * `"common"`：句柄类型非 int64。当启用聚簇索引且主键非整数时显示此类型。
    * `"unknown"`：当前不支持此句柄类型。
* `"handle_value"`：句柄值。
* `"index_id"`：索引键（存储索引的键）所属的索引 ID。
* `"index_name"`：索引键所属的索引名称。
* `"index_values"`：索引键中的索引值。

在上述字段中，如果某个字段的信息不适用或当前不可用，查询结果中将省略该字段。例如，行键信息不包含 `index_id`、`index_name` 和 `index_values`；索引键不包含 `handle_type` 和 `handle_value`；非分区表不显示 `partition_id` 和 `partition_name`；已删除表中的键信息无法获取 schema 相关信息（如 `table_name`、`db_id`、`db_name` 和 `index_name`），也无法判断该表是否为分区表。

> **Note:**
>
> 如果一个键来自启用了分区的表，并且在查询过程中由于某些原因（例如，键所属的表已被删除）无法查询到该键所属的 schema 信息，`table_id` 字段中可能会出现该键所属的分区的 ID。这是因为 TiDB 将不同分区的键编码方式与多个独立表的键编码方式相同。因此，当 schema 信息缺失时，TiDB 无法确认该键是属于未分区表还是某个分区。

## Example

```sql
select * from information_schema.data_lock_waits\G
```

```
*************************** 1. row ***************************
                   KEY: 7480000000000000355F728000000000000001
              KEY_INFO: {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"}
                TRX_ID: 426790594290122753
CURRENT_HOLDING_TRX_ID: 426790590082449409
            SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
       SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
1 row in set (0.01 sec)
```

上述查询结果显示，ID 为 `426790594290122753` 的事务在执行一条摘要为 `38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821` 的 ``update `t` set `v` = `v` + ? where `id` = ?`` 语句时，试图对键 `"7480000000000000355F728000000000000001"` 获取悲观锁，但该键的锁被 ID 为 `426790590082449409` 的事务持有。

## See also

<CustomContent platform="tidb">

- [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Handle Transaction Errors](/develop/dev-guide-transaction-troubleshoot.md)

</CustomContent>
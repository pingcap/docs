---
title: TiCDC Behavior in Splitting UPDATE Events
summary: Introduce the behavior changes about whether TiCDC splits `UPDATE` events, including the reasons and the impact of these changes.
---

# TiCDC Behavior in Splitting UPDATE Events

## Split `UPDATE` events for MySQL sinks

Starting from v6.5.10, v7.5.2, and v8.2.0, when using the MySQL sink, any TiCDC node that receives a request for replicating a table will fetch the current timestamp `thresholdTS` from PD before starting the replication to the downstream. Based on the value of this timestamp, TiCDC decides whether to split `UPDATE` events:

- For transactions containing one or multiple `UPDATE` changes, if the transaction `commitTS` is less than `thresholdTS`, TiCDC splits the `UPDATE` event into a `DELETE` event and an `INSERT` event before writing them to the Sorter module.
- For `UPDATE` events with the transaction `commitTS` greater than or equal to `thresholdTS`, TiCDC does not split them. For more information, see GitHub issue [#10918](https://github.com/pingcap/tiflow/issues/10918).

> **Note:**
>
> In v8.1.0, when using MySQL Sink, TiCDC also decides whether to split `UPDATE` events based on the value of `thresholdTS`, but `thresholdTS` is obtained differently. Specifically, in v8.1.0, `thresholdTS` is the current timestamp fetched from PD at TiCDC startup, but this way might cause data inconsistency issues in multi-node scenarios. For more information, see GitHub issue [#11219](https://github.com/pingcap/tiflow/issues/11219).

This behavior change (that is, deciding whether to split `UPDATE` events based on `thresholdTS`) addresses the issue of downstream data inconsistencies caused by the potentially incorrect order of `UPDATE` events received by TiCDC, which can lead to an incorrect order of split `DELETE` and `INSERT` events.

Take the following SQL statements as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 1;
COMMIT;
```

In this example, the two `UPDATE` statements within the transaction have a sequential dependency on execution. The primary key `a` is changed from `2` to `3`, and then the primary key `a` is changed from `1` to `2`. After this transaction is executed, the records in the upstream database are `(2, 1)` and `(3, 2)`.

However, the order of `UPDATE` events received by TiCDC might differ from the actual execution order of the upstream transaction. For example:

```sql
UPDATE t SET a = 2 WHERE a = 1;
UPDATE t SET a = 3 WHERE a = 2;
```

- Before this behavior change, TiCDC writes these `UPDATE` events to the Sorter module and then splits them into `DELETE` and `INSERT` events. After the split, the actual execution order of these events in the downstream is as follows:

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    REPLACE INTO t VALUES (2, 1);
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    After the downstream executes the transaction, the records in the database are `(3, 2)`, which are different from the records in the upstream database (`(2, 1)` and `(3, 2)`), indicating a data inconsistency issue.

- After this behavior change, if the transaction `commitTS` is less than the `thresholdTS` fetched from PD when TiCDC starts replicating the corresponding table to the downstream, TiCDC splits these `UPDATE` events into `DELETE` and `INSERT` events before writing them to the Sorter module. After the sorting by the Sorter module, the actual execution order of these events in the downstream is as follows:

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (2, 1);
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    After the downstream executes the transaction, the records in the downstream database are the same as those in the upstream database, which are `(2, 1)` and `(3, 2)`, ensuring data consistency.

As you can see from the preceding example, splitting the `UPDATE` event into `DELETE` and `INSERT` events before writing them to the Sorter module ensures that all `DELETE` events are executed before `INSERT` events after the split, thereby maintaining data consistency regardless of the order of `UPDATE` events received by TiCDC.

> **Note:**
>
> After this behavior change, when using the MySQL sink, TiCDC does not split the `UPDATE` event in most cases. Consequently, there might be primary key or unique key conflicts during changefeed runtime, causing the changefeed to restart automatically. After the restart, TiCDC will split the conflicting `UPDATE` events into `DELETE` and `INSERT` events before writing them to the Sorter module. This ensures that all events within the same transaction are correctly ordered, with all `DELETE` events preceding `INSERT` events, thus correctly completing data replication.

## Split primary or unique key `UPDATE` events for non-MySQL sinks

### Transactions containing a single `UPDATE` change

Starting from v6.5.3, v7.1.1, and v7.2.0, when using a non-MySQL sink, for transactions that only contain a single update change, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits this event into `DELETE` and `INSERT` events. For more information, see GitHub issue [#9086](https://github.com/pingcap/tiflow/issues/9086).

This change primarily addresses the issue that TiCDC only outputs the new value without the old value by default when using the CSV and AVRO protocols. Due to this issue, when the primary key or non-null unique index value changes, the consumer can only receive the new value, making it impossible to process the value before the change (for example, delete the old value). Take the following SQL as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
UPDATE t SET a = 2 WHERE a = 1;
```

In this example, the primary key `a` is updated from `1` to `2`. If the `UPDATE` event is not split, the consumer can only obtain the new value `a = 2` and cannot obtain the old value `a = 1` when using the CSV and AVRO protocols. This might cause the downstream consumer to only insert the new value `2` without deleting the old value `1`.

### Transactions containing multiple `UPDATE` changes

Starting from v6.5.4, v7.1.2, and v7.4.0, for transactions containing multiple changes, if the primary key or non-null unique index value is modified in the `UPDATE` event, TiCDC splits the event into `DELETE` and `INSERT` events and ensures that all events follow the sequence of `DELETE` events preceding `INSERT` events. For more information, see GitHub issue [#9430](https://github.com/pingcap/tiflow/issues/9430).

This change primarily addresses the potential issue of primary key or unique key conflicts that consumers might encounter when writing data changes from the Kafka sink or other sinks to a relational database or performing a similar operation. This issue is caused by the potentially incorrect order of `UPDATE` events received by TiCDC.

Take the following SQL as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 1;
UPDATE t SET a = 1 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 3;
COMMIT;
```

In this example, by executing three SQL statements to swap the primary keys of two rows, TiCDC only receives two update change events, that is, changing the primary key `a` from `1` to `2` and changing the primary key `a` from `2` to `1`. If consumers directly write these two `UPDATE` events to the downstream, a primary key conflict will occur, leading to changefeed errors.

Therefore, TiCDC splits these two events into four events, that is, deleting records `(1, 1)` and `(2, 2)` and writing records `(2, 1)` and `(1, 2)`.

### Control whether to split primary or unique key `UPDATE` events

Starting from v6.5.10, v7.1.6, v7.5.3, and v8.1.1, when using a non-MySQL sink, TiCDC supports controlling whether to split primary or unique key `UPDATE` events via the `output-raw-change-event` parameter, as described in the GitHub issue [#11211]( https://github.com/pingcap/tiflow/issues/11211). The specific behavior of this parameter is as follows:

- When you set `output-raw-change-event = false`, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits the event into `DELETE` and `INSERT` events and ensures that all events follow the sequence of `DELETE` events preceding `INSERT` events.
- When you set `output-raw-change-event = true`, TiCDC does not split `UPDATE` events. Note that when the primary key of a table is a clustered index, updates to the primary key are still split into `DELETE` and `INSERT` events in TiDB, and such behavior is not affected by the `output-raw-change-event` parameter.

> **Note**
>
> In the following tables, UK/PK stands for primary key or unique key.

#### Release 6.5 compatibility

| Version | Protocol | Split UK/PK `UPDATE` events | Not split UK/PK `UPDATE` events  | Comments |
| -- | -- | -- | -- | -- |
| <= v6.5.2 | ALL | ✗ | ✓ |  |
| v6.5.3 / v6.5.4 | Canal/Open | ✗ | ✓ |  |
| v6.5.3 | CSV/Avro | ✗ | ✗ | Split but does not sort. See [#9086](https://github.com/pingcap/tiflow/issues/9658) |
| v6.5.4 | Canal/Open | ✗ | ✗ | Only split and sort transactions that contain multiple changes |
| v6.5.5 ～ v6.5.9 | ALL | ✓ | ✗ |
| \>= v6.5.10 | ALL | ✓ (Default value: `output-raw-change-event = false`) | ✓ (Optional: `output-raw-change-event = true`) | |

#### Release 7.1 compatibility

| Version | Protocol | Split UK/PK `UPDATE` events | Not split UK/PK `UPDATE` events  | Comments |
| -- | -- | -- | -- | -- |
| v7.1.0 | ALL | ✗ | ✓ |  |
| v7.1.1 | Canal/Open | ✗ | ✓ |  |
| v7.1.1 | CSV/Avro | ✗ | ✗ | Split but does not sort. See [#9086](https://github.com/pingcap/tiflow/issues/9658) |
| v7.1.2  ~ v7.1.5 | ALL | ✓ | ✗ |  |
| \>= v7.1.6 (not released yet) | ALL | ✓ (Default value: `output-raw-change-event = false`) | ✓ (Optional: `output-raw-change-event = true`)  | |

#### Release 7.5 compatibility

| Version | Protocol | Split UK/PK `UPDATE` events | Not split UK/PK `UPDATE` events  | Comments |
| -- | -- | -- | -- | -- |
| <= v7.5.2 | ALL | ✓ | ✗ |
| \>= v7.5.3 (not released yet) | ALL | ✓ (Default value:`output-raw-change-event = false`) | ✓  (Optional: `output-raw-change-event = true`) | |

#### Release 8.1 compatibility

| Version | Protocol | Split UK/PK `UPDATE` events | Not split UK/PK `UPDATE` events  | Comments |
| -- | -- | -- | -- | -- |
| v8.1.0 | ALL | ✓ | ✗ |
| \>= v8.1.1 (not released yet) | ALL | ✓ (Default value:`output-raw-change-event = false`) | ✓  (Optional: `output-raw-change-event = true`) | |

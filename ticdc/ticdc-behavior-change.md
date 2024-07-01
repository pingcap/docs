---
title: TiCDC Behavior Changes
summary: Introduce the behavior changes of TiCDC changefeed, including the reasons and the impact of these changes.
---

# TiCDC Behavior Changes

## Split `UPDATE` events into `DELETE` and `INSERT` events

### Transactions containing a single `UPDATE` change

Starting from v6.5.3, v7.1.1, and v7.2.0, when using a non-MySQL sink, for transactions that only contain a single update change, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits this event into `DELETE` and `INSERT` events. For more information, see GitHub issue [#9086](https://github.com/pingcap/tiflow/issues/9086).

This change primarily addresses the following issues:

* When using the CSV and AVRO protocols, only the new value is output without the old value. Therefore, when the primary key or non-null unique index value changes, the consumer can only receive the new value, making it impossible to process the value before the change (for example, delete the old value).
* When using the index value dispatcher to distribute data across different Kafka partitions based on the key, multiple consumer processes in the downstream consumer group consume Kafka topic partitions independently. Due to different consumption progress, data inconsistency might occur.

Take the following SQL as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
UPDATE t SET a = 2 WHERE a = 1;
```

In this example, the primary key `a` is updated from `1` to `2`. If the `UPDATE` event is not split:

* When using the CSV and AVRO protocols, the consumer only obtains the new value `a = 2` and cannot obtain the old value `a = 1`. This might cause the downstream consumer to only insert the new value `2` without deleting the old value `1`.
* When using the index value dispatcher, the event for inserting `(1, 1)` might be sent to Partition 0, and the `UPDATE` event `(2, 1)` might be sent to Partition 1. If the consumption progress of Partition 1 is faster than that of Partition 0, an error might occur due to the absence of corresponding data in the downstream. Therefore, TiCDC splits the `UPDATE` event into `DELETE` and `INSERT` events. The event for deleting `(1, 1)` is sent to Partition 0, and the event for writing `(2, 1)` is sent to Partition 1, ensuring that the events are consumed successfully regardless of the progress of the consumer.

### Transactions containing multiple `UPDATE` changes

Starting from v6.5.4, v7.1.2, and v7.4.0, for transactions containing multiple changes, if the primary key or non-null unique index value is modified in the `UPDATE` event, TiCDC splits the event into `DELETE` and `INSERT` events and ensures that all events follow the sequence of `DELETE` events preceding `INSERT` events. For more information, see GitHub issue [#9430](https://github.com/pingcap/tiflow/issues/9430).

This change primarily addresses the potential issue of primary key or unique key conflicts when using the MySQL sink to directly write these two events to the downstream, leading to changefeed errors. When using the Kafka sink or other sinks, you might encounter the same error if the consumer writes messages to a relational database or performs similar operation.

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

In this example, by executing three SQL statements to swap the primary keys of two rows, TiCDC only receives two update change events, that is, changing the primary key `a` from `1` to `2` and changing the primary key `a` from `2` to `1`. If the MySQL sink directly writes these two `UPDATE` events to the downstream, a primary key conflict might occur, leading to changefeed errors.

Therefore, TiCDC splits these two events into four events, that is, deleting records `(1, 1)` and `(2, 2)` and writing records `(2, 1)` and `(1, 2)`.

### MySQL sink

In v8.1.0, when using the MySQL sink, TiCDC fetches the current timestamp `thresholdTS` from PD at startup and decides whether to split `UPDATE` events based on the value of this timestamp:

- For transactions containing one or multiple `UPDATE` changes, if the transaction `commitTS` is less than `thresholdTS`, TiCDC splits the `UPDATE` event into a `DELETE` event and an `INSERT` event before writing them to the Sorter module.
- For `UPDATE` events with the transaction `commitTS` greater than or equal to `thresholdTS`, TiCDC does not split them. For more information, see GitHub issue [#10918](https://github.com/pingcap/tiflow/issues/10918).

This behavior change addresses the issue of downstream data inconsistencies caused by the potentially incorrect order of `UPDATE` events received by TiCDC, which can lead to an incorrect order of split `DELETE` and `INSERT` events.

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

- After this behavior change, if the transaction `commitTS` is less than the `thresholdTS` obtained by TiCDC at startup, TiCDC splits these `UPDATE` events into `DELETE` and `INSERT` events before writing them to the Sorter module. After the sorting by the Sorter module, the actual execution order of these events in the downstream is as follows:

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

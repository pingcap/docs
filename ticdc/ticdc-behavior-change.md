---
title: TiCDC Behavior Changes
summary: Introduce the behavior changes of TiCDC changefeed, including the reasons and the impact of these changes.
---

# TiCDC Behavior Changes

## Split update events into delete and insert events

### Transactions containing a single update change

Starting from v6.5.3, v7.1.1, and v7.2.0, when using a non-MySQL sink, for transactions that only contain a single update change, if the primary key or non-null unique index value is modified in the update event, TiCDC splits this event into delete and insert events. For more information, see GitHub issue [#9086](https://github.com/pingcap/tiflow/issues/9086).

This change primarily addresses the following issues:

* When using the CSV and AVRO protocols, only the new value is output without the old value. Therefore, when the primary key or non-null unique index value changes, the consumer can only receive the new value, making it impossible to process the value before the change (for example, delete the old value).
* When using the index value dispatcher to distribute data across different Kafka partitions based on the key, multiple consumer processes in the downstream consumer group consume Kafka topic partitions independently. Due to different consumption progress, data inconsistency might occur.

Take the following SQL as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
UPDATE t SET a = 2 WHERE a = 1;
```

In this example, the primary key `a` is updated from `1` to `2`. If the update event is not split:

* When using the CSV and AVRO protocols, the consumer only obtains the new value `a = 2` and cannot obtain the old value `a = 1`. This might cause the downstream consumer to only insert the new value `2` without deleting the old value `1`.
* When using the index value dispatcher, the event for inserting `(1, 1)` might be sent to Partition 0, and the update event `(2, 1)` might be sent to Partition 1. If the consumption progress of Partition 1 is faster than that of Partition 0, an error might occur due to the absence of corresponding data in the downstream. Therefore, TiCDC splits the update event into delete and insert events. The event for deleting `(1, 1)` is sent to Partition 0, and the event for writing `(2, 1)` is sent to Partition 1, ensuring that the events are consumed successfully regardless of the progress of the consumer.

### Transactions containing multiple update changes

Starting from v6.5.4, v7.1.2, and v7.4.0, for transactions containing multiple changes, if the primary key or non-null unique index value is modified in the update event, TiCDC splits the event into delete and insert events and ensures that all events follow the sequence of delete events preceding insert events. For more information, see GitHub issue [#9430](https://github.com/pingcap/tiflow/issues/9430).

This change primarily addresses the potential issue of primary key conflicts when using the MySQL sink to directly write these two events to the downstream, leading to changefeed errors.

Take the following SQL as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 1 WHERE a = 3;
UPDATE t SET a = 2 WHERE a = 1;
UPDATE t SET a = 3 WHERE a = 2;
COMMIT;
```

In this example, by executing three SQL statements to swap the primary keys of two rows, TiCDC only receives two update change events, that is, changing the primary key `a` from `1` to `2` and changing the primary key `a` from `2` to `1`. If the MySQL sink directly writes these two update events to the downstream, a primary key conflict might occur, leading to changefeed errors.

Therefore, TiCDC splits these two events into four events, that is, deleting records `(1, 1)` and `(2, 2)` and writing records `(2, 1)` and `(1, 2)`.

Starting from v8.1.0, when using MySQL Sink, TiCDC will fetch a current timestamp (recorded as `thresholdTs`) from PD at start. For update events with `commitTS` less than `thresholdTs`, it will be split into delete and insert events before being written into the Sorter. This can ensure that all events within the same transaction are sorted in the order in which the delete event precedes the insert event. For update events with `commitTS` greater than or equal to `thresholdTs`, TiCDC will not split them. For details, see GitHub issue [#10918](https://github.com/pingcap/tiflow/issues/10918).

This change is due to the fact that TiCDC cannot obtain the execution order between multiple update events within the same upstream transaction. For a transaction containing multiple update events, if the primary key or non-null unique index value is modified in the update event, and the events are split into delete events and insert events before sent to the downstream, this may cause data inconsistency problem.

Take the following SQL as an example:

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 1;
COMMIT;
```

In the above example, the execution order of the two SQL statements within the transaction has a sequential dependency relationship, that is, the primary key `a` is changed from `2` to `3`, and then the primary key `a` is changed from `1` to `2`. If the order of update events received by TiCDC is different from the actual execution order within the transaction, splitting them into delete and insert events and sending them downstream will cause data inconsistency.

For example, the sequence of update events that TiCDC may receive is as follows:

```sql
UPDATE t SET a = 2 WHERE a = 1;
UPDATE t SET a = 3 WHERE a = 2;
```

The actual sequence of events executed in downstream after TiCDC splits the above update events is as follows:

```sql
BEGIN;
DELETE FROM t WHERE a = 1;
REPLACE INTO t VALUES (2, 1);
DELETE FROM t WHERE a = 2;
REPLACE INTO t VALUES (3, 2);
COMMIT;
```

After executing the transaction in the upstream, the records should be `(3, 2)` and `(2, 2)`, while the records in the downstream will be `(3, 2)` after executing the transaction, which means data inconsistency problem happens.

Note that after this behavior change, TiCDC will not split update events in most cases when using MySQL Sink, so primary key or unique key conflicts may occur when changefeed is run. This problem will cause the changefeed to automatically restart. After the restart, the conflicting update events will be split into delete and insert events and written to the Sorter. At this time, it can be ensured that all events in the same transaction are in the order of the delete event before the insert event, which can guarantee data synchronization to process correctly.

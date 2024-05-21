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

In this example, by executing three SQL statements to swap the primary keys of two rows, TiCDC only receives two update change events, that is, changing the primary key `a` from `1` to `2` and changing the primary key `a` from `2` to `1`. If the MySQL sink directly writes these two update events to the downstream, a primary key conflict might occur, leading to changefeed errors.

Therefore, TiCDC splits these two events into four events, that is, deleting records `(1, 1)` and `(2, 2)` and writing records `(2, 1)` and `(1, 2)`.

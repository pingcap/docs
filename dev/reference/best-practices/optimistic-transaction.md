---
title: Optimistic Transaction Best Practices
summary: Learn the optimistic transaction in TiDB.
category: reference
---

# Optimistic Transaction Best Practices

This document introduces the principles of TiDB's optimistic locking mechanism, and provides best practices for optimistic transactions in various scenarios. This document assumes that you have a basic understanding of [TiDB architecture](/dev/architecture.md) and [Percolator](https://ai.google/research/pubs/pub36726), with the following core concepts:

- [ACID](/dev/glossary.md#ACID)
- [transaction](/dev/glossary.md#transaction)
- [optimistic transaction](/dev/glossary.md#optimistic-transaction)
- [pessimistic transaction](/dev/glossary.md#pessimistic-transaction)
- [explicit/implicit transaction](/dev/glossary.md#explicitimplicit-transaction)

## Principles of optimistic transactions

TiDB adopts Google's Percolator transaction model, a variant of two-phase commit (2PC) to ensure the correct completion of a distributed transaction. The procedure is as follows:

![2PC in TiDB](/media/best-practices/2pc-in-tidb.png)

1. The client begins a transaction.

    TiDB receives the start timestamp from PD and mark it as `start_ts`.

2. The client issues a read request.

    a. TiDB receives routing information (how data is distributed among TiKV nodes) from PD.

    b. TiDB receives the data of the `start_ts` version from TiKV.

3. The client issues a write request.

    **Data that meets consistency requirement is stored in the memory**.

4. The client issues a commit request.

5. TiDB begins 2PC to ensure the atomicity of distributed transactions and make data physically resides.

    a. TiDB selects a Primary Key from the data to be written.

    b. TiDB receives the information of data distribution in regions from PD, and groups all keys by region accordingly.

    c. TiDB sends prewrite requests to all TiKV nodes involved. TiKV checks the timestamp for conflict, and evaluates whether it is expired. Then, TiKV locks the data to be written.

    d. TiDB successfully receives all requests in the prewrite phase.

    e. TiDB receives a commit timestamp from PD and marks it as `commit_ts`.

    f. TiDB initiates the second commit to the TiKV nodes where Primary Key is located. TiKV checks the data, and clean the locks left in the prewrite phase.

    g. The second phase is successfully finished.

6. TiDB returns a message to inform the client that the transaction is successfully committed.

7. TiDB asynchronously cleans the locks left in this transaction.

## Advantages and disadvantages

From the process of transactions in TiDB above, it is clear that TiDB transactions have the following advantages:

* Simple to understand
* Implement cross-row transaction based on single-row transaction
* Decentralized lock management

However, TiDB transactions also have the following disadvantages:

* More RPCs
* Lack of a centralized timestamp manager
* Frequent OOM (out of memory)

## Transaction sizes

In optimistic locking mechanism, a transaction either too small or too large can impair the overall performance. To avoid potential problems, you can turn to the following solutions in application.

### Small transactions

TiDB uses the autocommit setting by default, which automatically issues a commit following each SQL statement. Therefore, each of the following three statements is treated as a transaction:

```sql
# original version with autocommit.
UPDATE my_table SET a = 'new_value' WHERE id = 1;
UPDATE my_table SET a = 'newer_value' WHERE id = 2;
UPDATE my_table SET a = 'newest_value' WHERE id = 3;
```

In this case, the transaction latency is increased because the two-phase commit requires two sequential rounds of distributed consensus. To improve the performance, you can use an explicit transaction instead, that is, to execute the above three statements within a transaction:

```sql
# improved version.
START TRANSACTION;
UPDATE my_table SET a = 'new_value' WHERE id = 1;
UPDATE my_table SET a = 'newer_value' WHERE id = 2;
UPDATE my_table SET a = 'newest_value' WHERE id = 3;
COMMIT;
```

Similarly, it is recommended to execute `INSERT` statement within an explicit transaction.

### Large transaction

Due to the requirement of 2PC, large transactions that modify data can leads to:

* OOM when excessive data is written in the memory
* More conflicts in the prewrite phase
* Long duration before transactions actually commit

Therefore, TiDB intentionally imposes some limits on transaction sizes:

* The total number of SQL statements in a transaction is no more than 5,000 (default)
* Each Key-Value entry is no more than 6 MiB
* The total number of Key-Value entries is no more than 300,000
* The total size of Key-Value entries is no more than 100 MiB

For each transaction, it is recommended to keep the number of SQL statements between 100 to 500 to achieve an optimal performance.

## Transaction conflicts

When two or more transactions execute concurrently, then there might be some conflicting operations. There are two main forms of conflicts:

* **Read-write conflict** occurs when a transaction reads the data which is written by the other transaction before committing.
* **Write-write conflict** occurs when two or more transactions doing write operations on the same key concurrently.

In TiDB's optimistic locking mechanism, the two-phase commit begins right after the client executes `COMMIT` statement. In other words, for optimistic transactions, the write-write conflict can be observed before the transactions are actually committed, which makes it more easily to be perceived by users.

### Default behavior for conflicting transactions

TiDB uses an optimistic mechanism for commits, so that changes can be written to the data before the commit actually occurs. In this sense, both types of conflicts are allowed in the prewrite phase. To illustrate this default behavior, assume there are two concurrent transactions A and B update the same row. Their execution results at different time points are as follows:

![Conflicting transactions](/media/best-practices/optimistic-transaction-table1.png)

This procedure is visualized as follows:

![Conflicting transactions analysis](/media/best-practices/optimistic-transaction-case1.png)

1. As shown above, `txnA` begins at `t1` and `txnB` begins at `t2`.

2. At `t3`, `txnB` updates the row (`id = 1`).

3. At `t4`, `txnA` updates the same row. Because conflict detection is only performed before the transactions actually commit, this operation successfully executed.

4. At `t5`, `txnB` commits successfully.

5. At `t6`, `txnA` tries to commit but TiDB responds with an error and informs the client to `try again later`.

### Automatic retry

TiDB uses optimistic locking by default whereas MySQL applies pessimistic locking. This means that MySQL checks for conflict during the execution of SQL statements, so there are few errors returned in heavy contention scenarios. In the same example above, the conflict is instantly observed when `txnA` updates data at `t4`.

For the convenience of MySQL users, TiDB provides a retry function that runs inside a transaction. If there is a conflict, TiDB retries the write operations automatically. You can set `tidb_disable_txn_auto_retry` and `tidb_retry_limit` to enable or disable this default function:

```toml
# Whether to disable automatic retry. ("on" by default)
tidb_disable_txn_auto_retry = off
# Set the maximum number of the retires. ("10" by default)
# When “tidb_retry_limit = 0”, automatic retry is completely disabled.
tidb_retry_limit = 10
```

You can enable automatic retry in either session level or global level:

1. Session level:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_disable_txn_auto_retry = off;
    set @@tidb_retry_limit = 10;
    ```

2. Global level:

    {{< copyable "sql" >}}

    ```sql
    set @@global.tidb_disable_txn_auto_retry = off;
    set @@global.tidb_retry_limit = 10;
    ```

### Limits of retry

TiDB automatically retries failed transactions by default, which might lead to lost updates. The reason can be observed with the procedures of retry below:

1. Allocate a new timestamp and mark it as `start_ts`.

2. Rollback the SQL statements that contain write operations.

3. Implement the two-phase commit.

It is noted that TiDB only retries write operations, which can lead to problems if there are `UPDATE` statements in the transaction:

1. When a transaction fails, TiDB retries it with the data in the new `start_ts` version.

2. If the `UPDATE` statements use other query results, the data might not be updated as expected.

The following instance illustrates this limit of automatic retry. Assume there are two session A and B update the same row concurrently, and their execution results at different time points are as follows:

![Automatic retry](/media/best-practices/optimistic-transaction-table2.png)

This instance is visualized as follows:

![Automatic retry analysis](/media/best-practices/optimistic-transaction-case2.png)

1. As shown, Session B begins `txn2` and Session A begins `txn2` at `t1`.

2. Both `txn1` and `txn2` update the same row at the same time.

3. At `t5`, Session B commits `txn2` successfully.

4. At `t8`, a conflict is detected when Session A commits `txn1`, so TiDB automatically retries it.
    a. TiDB receives a new `start_ts` (i.e. `t8'`).
    b. TiDB rolls back the statement `update tidb set name='pd' where id =1 and status=1`.
        i. No matching statement is found in the data of version `t8'`.
        ii. No data is updated, return to the upper layer.

5. TiDB considers that `txn1` is successfully retried, but the data is not updated as expected.

During retrying, TiDB receives a new timestamp to mark the beginning of the transaction. In this case, if the transaction updates data using other query results, a lost update might occur because the read repeatable isolation (also known as snapshot isolation) is violated. You can disable automatic retry to prevent lost updates.

### Conflict detection

For the optimistic transaction, it is important to detect whether there are write-write conflicts in the underlying data. Specifically, TiKV needs to read data for detection in the prewrite phase. To optimize this performance, the conflict detection is mainly performed in two layers:

* The TiDB layer. TiDB uses latches to prevent conflicting transactions. If a write-write conflict in the instance is observed after the primary write is issued, it is unnecessary to issue the subsequent writes to the TiKV.
* The TiKV layer. TiKV also uses latches to prevent conflicting transactions, which is performed in the prewrite phase.

The latches in the TiDB layer is disabled by default. The specific configuration items are as follows:

```toml
[txn-local-latches]
# Whether to enable the latches for transactions. Recommended
# to use latches when there are many local transaction conflicts.
enabled = false
# Controls the number of slots corresponding to Hash. ("204800" by default)
# It automatically adjusts upward to an exponential multiple of 2.
# Each slot occupies 32 Bytes of memory. If set too small,
# it might result in slower running speed and poor performance
# when data writing covers a relatively large range.
capacity = 2048000
```

The value of `capacity` mainly affects the accuracy of conflict detection. When performing conflict detection, only the hash value of each key is stored in the memory. Because the probability of collision when hashing is closely related to the probability of wrong detection, you can configure `capacity` to controls the number of slots and enhance the accuracy of conflict detection.

* The smaller the value of `capacity`, the smaller the occupied memory and the greater the probability of wrong detection.
* The larger the value of `capacity`, the larger the occupied memory and the smaller the probability of wrong detection.

When you confirm that there is no write-write conflict in the upcoming transactions, it is recommended to disable the function of conflict detection.

TiKV uses the built-in memory latches to prevent concurrent operations on the same key. But the memory lock in the TiKV layer is strictly performed and cannot be disabled. You can only configure `scheduler-concurrency` to control the number of slots that defined by the modulo operation:

```toml
# Controls the number of slots. ("2048000" by default）
scheduler-concurrency = 2048000
```

In addition, TiKV supports monitoring the time spent on waiting latches in Scheduler.

![Scheduler latch wait duration](/media/best-practices/optimistic-transaction-metric.png)

When `Scheduler latch wait duration` is high and there is no slow writes, it can be safely concluded that there are many write conflicts at this time.
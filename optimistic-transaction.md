---
title: TiDB Optimistic Transaction Model
summary: Learn the optimistic transaction model in TiDB.
aliases: ['/docs/dev/optimistic-transaction/','/docs/dev/reference/transactions/transaction-optimistic/','/docs/dev/reference/transactions/transaction-model/']
---

# TiDB Optimistic Transaction Model

This document introduces the principles of TiDB's optimistic transaction model and related features.

In TiDB's optimistic transaction model, write-write conflicts are detected only at the two-phase transactional commit.

> **Note:**
>
> Starting from v3.0.8, newly created TiDB clusters use the [pessimistic transaction model](/pessimistic-transaction.md) by default. However, this does not affect your existing cluster if you upgrade it from v3.0.7 or earlier to v3.0.8 or later. In other words, **only newly created clusters default to using the pessimistic transaction model**.

## Principles of optimistic transactions

To support distributed transactions, TiDB adopts two-phase commit (2PC) in optimistic transactions. The procedure is as follows:

![2PC in TiDB](/media/2pc-in-tidb.png)

1. The client begins a transaction.

    TiDB gets a timestamp (monotonically increasing in time and globally unique) from PD as the unique transaction ID of the current transaction, which is called `start_ts`. TiDB implements multi-version concurrency control, so `start_ts` also serves as the version of the database snapshot obtained by this transaction. This means that the transaction can only read the data from the database at `start_ts`.

2. The client issues a read request.

    1. TiDB receives routing information (how data is distributed among TiKV nodes) from PD.
    2. TiDB receives the data of the `start_ts` version from TiKV.

3. The client issues a write request.

    TiDB checks whether the written data satisfies constraints (to ensure the data types are correct, the NOT NULL constraint is met, etc.). **Valid data is stored in the private memory of this transaction in TiDB**.

4. The client issues a commit request.

5. TiDB begins 2PC, and persist data in store while guaranteeing the atomicity of transactions.

    1. TiDB selects a Primary Key from the data to be written.
    2. TiDB receives the information of Region distribution from PD, and groups all keys by Region accordingly.
    3. TiDB sends prewrite requests to all TiKV nodes involved. Then, TiKV checks whether there are conflict or expired versions. Valid data is locked.
    4. TiDB receives all requests in the prewrite phase and the prewrite is successful.
    5. TiDB receives a commit version number from PD and marks it as `commit_ts`.
    6. TiDB initiates the second commit to the TiKV node where Primary Key is located. TiKV checks the data, and clean the locks left in the prewrite phase.
    7. TiDB receives the message that reports the second phase is successfully finished.

6. TiDB returns a message to inform the client that the transaction is successfully committed.

7. TiDB asynchronously cleans the locks left in this transaction.

## Advantages and disadvantages

From the process of transactions in TiDB above, it is clear that TiDB transactions have the following advantages:

* Simple to understand
* Implement cross-node transaction based on single-row transaction
* Decentralized lock management

However, TiDB transactions also have the following disadvantages:

* Transaction latency due to 2PC
* In need of a centralized timestamp allocation service
* OOM (out of memory) when extensive data is written in the memory

## Transaction retries

In the optimistic transaction model, transactions might fail to be committed because of write–write conflict in heavy contention scenarios. TiDB uses optimistic concurrency control by default, whereas MySQL applies pessimistic concurrency control. This means that MySQL adds locks during SQL execution, and its Repeatable Read isolation level allows for non-repeatable reads, so commits generally do not encounter exceptions. To lower the difficulty of adapting applications, TiDB provides an internal retry mechanism.

### Automatic retry

If a write-write conflict occurs during the transaction commit, TiDB automatically retries the SQL statement that includes write operations. You can enable the automatic retry by setting `tidb_disable_txn_auto_retry` to `off` and set the retry limit by configuring `tidb_retry_limit`:

```toml
# Whether to disable automatic retry. ("on" by default)
tidb_disable_txn_auto_retry = off
# Set the maximum number of the retires. ("10" by default)
# When “tidb_retry_limit = 0”, automatic retry is completely disabled.
tidb_retry_limit = 10
```

You can enable the automatic retry in either session level or global level:

1. Session level:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_disable_txn_auto_retry = off;
    ```

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_retry_limit = 10;
    ```

2. Global level:

    {{< copyable "sql" >}}

    ```sql
    set @@global.tidb_disable_txn_auto_retry = off;
    ```

    {{< copyable "sql" >}}

    ```sql
    set @@global.tidb_retry_limit = 10;
    ```

> **Note:**
>
> The `tidb_retry_limit` variable decides the maximum number of retries. When this variable is set to `0`, none of the transactions automatically retries, including the implicit single statement transactions that are automatically committed. This is the way to completely disable the automatic retry mechanism in TiDB. After the automatic retry is disabled, all conflicting transactions report failures (including the `try again later` message) to the application layer in the fastest way.

### Limits of retry

By default, TiDB will not retry transactions because this might lead to lost updates and damaged [`REPEATABLE READ` isolation](/transaction-isolation-levels.md).

The reason can be observed from the procedures of retry:

1. Allocate a new timestamp and mark it as `start_ts`.
2. Retry the SQL statements that contain write operations.
3. Implement the two-phase commit.

In Step 2, TiDB only retries SQL statements that contain write operations. However, during retrying, TiDB receives a new version number to mark the beginning of the transaction. This means that TiDB retries SQL statements with the data in the new `start_ts` version. In this case, if the transaction updates data using other query results, the results might be inconsistent because the `REPEATABLE READ` isolation is violated.

If your application can tolerate lost updates, and does not require `REPEATABLE READ` isolation consistency, you can enable this feature by setting `tidb_disable_txn_auto_retry = off`.

## Conflict detection

As a distributed database, TiDB performs in-memory conflict detection in the TiKV layer, mainly in the prewrite phase. TiDB instances are stateless and unaware of each other, which means they cannot know whether their writes result in conflicts across the cluster. Therefore, conflict detection is performed in the TiKV layer.

The configuration is as follows:

```toml
# Controls the number of slots. ("2048000" by default）
scheduler-concurrency = 2048000
```

In addition, TiKV supports monitoring the time spent on waiting latches in scheduler.

![Scheduler latch wait duration](/media/optimistic-transaction-metric.png)

When `Scheduler latch wait duration` is high and there is no slow writes, it can be safely concluded that there are many write conflicts at this time.

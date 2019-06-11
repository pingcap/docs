---
title: Pessimistic Transactions
summary: Learn about TiDB pessimistic transaction mode.
category: reference
---

# TiDB Pessimistic Transaction Mode

By default, TiDB implements an optimistic transaction mode, where the commit might fail for a transaction because of transaction conflicts. To improve the commit success rate, you need to modify the application with an automatic retry logic. With the pessimistic transaction mode, you can avoid this potential issue without the need of adding any retry logic to your application.

> **Warning:**
>
> Pessimistic transactions are an **experimental** feature. It is *not recommended to apply it in the production environment*.

## Behaviors of the pessimistic transaction mode

Pessimistic transactions in TiDB behave similarly to those in MySQL. See the minor differences in [Known Restrictions](#known-restrictions).

- When you perform `SELECT FOR UPDATE` statements, transactions read the last committed data and apply a pessimistic lock on the modified data.

- When you perform `UPDATE/DELETE/INSERT` statements, transactions read the last committed data and place a pessimistic lock on the modified data.

- When a pessimistic lock is applied on a row of data, other write transactions attempting to modify the data are blocked and have to wait for the lock to be released.

- When a pessimistic lock is applied on a row of data, other transactions attempting to read the data are not blocked and can read the committed data.

- All the locks are released when the transaction is committed or rolled back.

- Deadlocks in concurrent transactions can be detected by the deadlock detector. A DEADLOCK error which is the same as that in MySQL is returned.

- TiDB supports both the optimistic transaction mode and pessimistic transaction mode in the same cluster. You can specify either mode for transaction execution.

## Methods to enable pessimistic transaction mode

The pessimistic transaction mode is disabled by default because it is currently an experimental feature. Before enabling it, you need to add the following setting in the configuration file:

```
[pessimistic-txn]
enable = true
```

When `enable` is set to `true`, the default transaction mode in TiDB is still optimistic. To enable the pessimistic transaction mode, choose any of the following methods that suits your needs:

- Use `BEGIN PESSIMISTIC;` statement to start the transaction in the pessimistic transaction mode. Write in comment style as `BEGIN /*!90000 PESSIMISTIC */;` to make it compatible with the MySQL syntax.

- Execute the `set @@tidb_txn_mode = 'pessimistic';` statement to allow all the transactions processed in this session to be in the pessimistic transaction mode.

- Enable the pessimistic transaction mode in the configuration file. This allows all transactions (except auto-committed single-statement ones) to adopt the pessimistic transaction mode.

    ```
    [pessimistic-txn]
    enable = true
    default = true
    ```

If the pessimistic transaction mode is enabled in the configuration file by default, use one of the following methods to adopt the optimistic transaction mode for the transaction:

- Use `BEGIN OPTIMISTIC;` statement to start the transaction in the optimistic transaction mode. Write in comment style as `BEGIN /*!90000 OPTIMISTIC */;` to make it compatible with the MySQL syntax.

- Execute `set @@tidb_txn_mode = 'optimistic';` statement to allow all the transactions processed in this session to be in the optimistic transaction mode.

## Enablement priority

The three methods to enable the transaction mode are ordered from highest priority to lowest as follows:

- Use `BEGIN PESSIMISTIC;` or `BEGIN OPTIMISTIC;`.

- Set the session variable `tidb_txn_mode`.

- Configure the parameter `default` in the configuration file. If you use a regular `BEGIN` statement and set the value of `tidb_txn_mode` to an empty string, then you can use `default` to determine whether to enable the pessimistic or optimistic transaction mode.

## Configuration parameter

The related configuration parameters are under the `[pessimistic-txn]` category. Besides `enable` and `default`, you can also configure the following parameters:

- `ttl`

    ```
    ttl = "30s"
    ```

     `ttl` is the timeout time for the lock of pessimistic transactions. Its default value is "30s" (30 seconds). You must set it to a value between 15~60 seconds, and a lower or higher value can result in an error.

    A transaction fails when its execution time exceeds `ttl`. If the value of `ttl` is set too high, the remaining pessimistic lock might block the write transaction for a long time when `tidb-server` is down. If set too low, the transaction might be rolled back by other transactions before it can finish execution.

- `max-retry-count`

    ```
    max-retry-count = 256
    ```

    A pessimistic transaction can automatically retry a single statement. You can specify the maximum retrying times by setting the parameter `max-retry-count` to avoid retrying a statement endlessly in some extreme cases. Normally, you do not need to modify this configuration.

## Known Restrictions

- TiDB does not support GAP Lock or Next Key Lock. When multiple rows of data are updated through range conditions in a pessimistic transaction, other transactions can insert data without being blocked in this range.

- TiDB does not support `SELECT LOCK IN SHARE MODE`.

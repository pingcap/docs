---
title: TiDB Pessimistic Transaction Mode
summary: Learn about TiDB pessimistic transaction mode.
category: reference
---

# TiDB Pessimistic Transaction Mode

By default, TiDB implements an optimistic transaction mode, where the commit might fail for a transaction because of transaction conflicts. To improve the commit success rate, you need to modify the application with an automatic retry logic. With the pessimistic transaction mode, you can avoid this potential issue without the need of adding any retry logic to your application.

> **Warning:**
>
> Up to now, the pessimistic transaction mode in TiDB is still an **experimental** feature. It is *not recommended to apply it in the production environment*.

## Behaviors of the Pessimistic Transaction Mode

Pessimistic transactions in TiDB behave similarly to those in MySQL. See the minor differences in [Known Restrictions](#known-restrictions).


- When you perform `SELECT FOR UPDATE` statements, transactions read the last committed data and apply a pessimistic lock on the modified data.

- When you perform `UPDATE/DELETE/INSERT` statements, transactions read the last committed data and place a pessimistic lock on the modified data.

- When a pessimistic lock is applied on a row of data, other write transactions attempting to modify the data are blocked and have to wait for the lock to be released.

- When a pessimistic lock is applied on a row of data, other transactions attempting to read the data are not blocked and can read the committed data.

- All the locks are released when the transaction is committed or rolled back.

- Deadlocks in concurrent transactions can be detected by the deadlock detector. A DEADLOCK error which is the same as that in MySQL is returned.

- TiDB supports both the optimistic transaction mode and pessimistic transaction mode in the same cluster.  You can specify either mode for transaction execution.

## Methods to Enable Pessimistic Transaction Mode

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

## Enablement Priority

- `BEGIN PESSIMISTIC;` and `BEGIN OPTIMISTIC;` are statements with the highest priority.

-  Session variable `tidb_txn_mode` has the second highest priority.

- You can configure the `default` file. If the transaction starts with `BEGIN` statement and the value of `tidb_txn_mode` is an empty string, the transaction mode is determined by the `default` in the configuration file.

## Configuration Parameter

The related configuration file is under the `[pessimistic-txn]` file. Besides the `enable` and `default` arguments, you can also configure the following arguments:

- `ttl`

    ```
    ttl = "30s"
    ```

    The default value of the pessimistic locking timeout `ttl` is 30s. The value configured must be between "15s" and "60s". Otherwise, the error will be reported.

    The transaction will fail if its execution time exceeds the value of `ttl`. If the timeout value is set too high, it might cause long waiting time of write transaction when `tidb-server` fails. If too low, the transaction might be rolled back due to the conflict with other transaction.

- `max-retry-count`

    ```
    max-retry-count = 256
    ```

    In the pessimistic transaction mode, the transaction can automatically retry a single statement. You can configure the maximum number of automatically retry to avoid the extreme case that the single statement is run endlessly. Normally you do not need to modify this configuration.


## Known Restrictions

- GAP Lock or Next Key Lock

  When the transaction sets the pessimistic lock on the rows in a scanned range to update, other transaction can still insert the new rows without being blocked.

- SELECT LOCK IN SHARE MODE

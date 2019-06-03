---
title: Pessimistic Transactional Model
summary: Learn how to start TiDB's pessimistic transaction model.
category: reference
---

# TiDB Pessimistic Transactional Model

TiDB implements optimistic transactional model by default. Problem might arise that the transaction fails to commit because of the conflict with other transaction. To solve this problem, generally you need to modify the application code and combine with automatic retry logic. But if you use pessimistic transactional model, you can avoid this potential issue  and the application can runs normally without modification and retry logic.


> **Warning:**
>
> Up to now, TiDB pessimistic transactional model is still **in testing**. **We do not recommend you to implement it in the production environment**.

## Pessimistic Locking in TiDB

Pessimistic locking in TiDB is mostly similar with that in MySQL, only with slight difference. For difference from MySQL, see [Lock Unsupported Yet](#Lock-Unsupported-Yet).


- Perform `SELECT FOR UPDATE` statement to read the recent committed record and place a pessimistic lock on it.

- Execute `UPDATE/DELETE/INSERT` statements to read the recent committed record and place a pessimistic lock on the record modified.

- When a row is placed on a pessimistic lock, other write transaction attempting to modify the row will be blocked and have to wait for the lock to be released.

- When a row is placed on a pessimistic lock, other transactions attempting to read this row will not be blocked and can read the committed record.

- All the locks will be released when the transaction is committed or rolled back.

- Deadlock occurred in the concurrent transactions will be detected by Deadlock Detector and a DEADLOCK `Error` which is the same as that in MySQL will be returned.

- You can choose the optimistic transactional model or pessimistic transactional model in TiDB by specifying the model to execute.

## How To Enable Pessimistic Transactional Model?

The pessimistic transactional model is disabled by default because it is in testing now. Before enabling this model, adding the following statements in the configuration file:

```
[pessimistic-txn]
enable = true
```

When `enable` is set to `true`, the default transaction model in TiDB is still the optimistic one. You can enable the pessimistic transaction model through the following methods:

- Use `BEGIN PESSIMISTIC;` statement to start the transaction and implement the pessimistic transactional model. Add the code comment like `BEGIN /*!90000 PESSIMISTIC */;` to make the transaction compatible with MySQL syntax.

- Execute `set @@tidb_txn_mode = 'pessimistic';` statement to allow the all the transactions of this session to implement the pessimistic transactional model.

- Default to pessimistic transactional model in the configuration file to make all the transactions, except the auto-committed single statement transaction, implement the pessimistic transactional model.

    ```
    [pessimistic-txn]
    enable = true
    default = true
    ```

If the default locking is pessimistic, use the following methods to enter the optimistic transactional model:

- Use `BEGIN OPTIMISTIC;` statement to start the transaction and implement the optimistic transactional model. You can add the code comment like `BEGIN /*!90000 OPTIMISTIC */;` to make the transaction compatible with MySQL syntax.

- Execute `set @@tidb_txn_mode = 'optimistic';` statement to allow the transaction of the current session to use the optimistic transactional model.

## Preference to Enabling the Model

- The preferred method is to use the `BEGIN PESSIMISTIC;` or `BEGIN OPTIMISTIC;` statement to implement the transactional model.

- You can also set the variable `tidb_txn_mode` of session.

- You can configure the `default` file. If the transaction starts with `BEGIN` statement and the value of `tidb_txn_mode` is an empty string, the transactional model is determined by the `default` in the configuration file.

## Configuration Parameter

The related configuration file is under the `[pessimistic-txn]` file. Besides the `enable` and `default` arguments, you can also configure the following arguments:

- `ttl`

    ```
    ttl = "30s"
    ```

The default value of the pessimistic locking timeout `ttl` is 30s. The value configured must be between "15s" and "60s". Otherwise, the error will be reported.

The transaction will fail if its execution time exceeds the value of `ttl`. If the timeout value is set too high, it might cause long waiting time of write transaction when `tidb-server` fails. If too low, a transaction might be rolled back due to the conflict with other transaction.

- `max-retry-count`

    ```
    max-retry-count = 256
    ```

In the pessimistic transactional model, the transaction can auto-retry a single statement. You can configure the maximum number of auto-retry to avoid the extreme case that the single statement is run endlessly. Normally you do not need to modify this configuration.


## Lock Unsupported Yet

- GAP Lock or Next Key Lock

  When the transaction sets the pessimistic lock on the rows in a scanned range to update, other transaction can still insert the new rows without being blocked.

- SELECT LOCK IN SHARE MODE
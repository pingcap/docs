---
title: Transactions
summary: Learn about transactions concepts for TiDB Cloud.
---

# Transactions

TiDB provides complete distributed transactions and the model has some optimizations on the basis of [Google Percolator](https://research.google.com/pubs/pub36726.html).

## Optimistic transaction mode

TiDB's optimistic transaction model does not detect conflicts until the commit phase. If there are conflicts, the transaction needs retry. But this model is inefficient if the conflict is severe, because operations before retry are invalid and need to repeat.

Assume that the database is used as a counter. High access concurrency might lead to severe conflicts, resulting in multiple retries or even timeouts. Therefore, in the scenario of severe conflicts, it is recommended to use the pessimistic transaction mode or to solve problems at the system architecture level, such as placing counter in Redis. Nonetheless, the optimistic transaction model is efficient if the access conflict is not very severe.

For more information, see [TiDB Optimistic Transaction Model](/optimistic-transaction.md).

## Pessimistic transaction mode

In TiDB, the pessimistic transaction mode has almost the same behavior as in MySQL. The transaction applies a lock during the execution phase, which avoids retries in conflict situations and ensures a higher success rate. By applying the pessimistic locking, you can also lock data in advance using `SELECT FOR UPDATE`.

However, if the application scenario has fewer conflicts, the optimistic transaction model has better performance.
For more information, see [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md).

## Transaction isolation levels

Transaction isolation is one of the foundations of database transaction processing. Isolation is one of the four key properties of a transaction (commonly referred as [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)).

TiDB implements Snapshot Isolation (SI) consistency, which it advertises as `REPEATABLE-READ` for compatibility with MySQL. This differs from the [ANSI Repeatable Read isolation level](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read) and the [MySQL Repeatable Read level](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read).

For more information, see [TiDB Transaction Isolation Levels](/transaction-isolation-levels.md).

### Non-transactional DML statements

A non-transactional DML statement is a DML statement split into multiple SQL statements (which is, multiple batches) to be executed in sequence. It enhances the performance and ease of use in batch data processing at the expense of transactional atomicity and isolation.

Usually, memory-consuming transactions need to be split into multiple SQL statements to bypass the transaction size limit. Non-transactional DML statements integrate this process into the TiDB kernel to achieve the same effect. It is helpful to understand the effect of non-transactional DML statements by splitting SQL statements. The `DRY RUN` syntax can be used to preview the split statements.

For more information, see [Non-Transactional DML Statements](/non-transactional-dml.md).
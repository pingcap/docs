---
title: Transaction overview
summary: A brief introduction to transactions in TiDB.
---

# Transaction overview

TiDB supports complete distributed transactions, providing [optimistic transactions](/optimistic-transaction.md) and [pessimistic transactions](/pessimistic-transaction.md) (introduced in TiDB 3.0) two transaction models. This article mainly introduces statements related to transactions, optimistic transactions and pessimistic transactions, transaction isolation levels, and optimistic transaction application-side retry and error handling.

## Common statement

This chapter introduces how to use transactions in TiDB. We will use the following example to demonstrate the control flow of a simple transaction:

Bob wants to transfer $20 to Alice, which includes at least two operations:

- Bob's account is reduced by $20.
- Alice's account is increased by $20.

Transactions can ensure that both of the above operations are executed successfully or both fail, and the money will not disappear or appear in vain.

Insert some sample data into the table using the `users` table in the [bookshop](/develop/dev-bookshop-schema-design.md) database

{{< copyable "sql" >}}

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

Now, we run the following transactions and explain what each statement means:

{{< copyable "sql" >}}

```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

After the above transaction is successful, the table should look like this:

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+

```

### Start transaction

To explicitly start a new transaction, either the `BEGIN` statement or the `START TRANSACTION` statement can be used, both have the same effect.

{{< copyable "sql" >}}

```sql
BEGIN;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

The default transaction mode of TiDB is pessimistic transaction. You can also explicitly specify to enable [optimistic transaction](/develop/dev-optimistic-and-pessimistic-transaction.md):

{{< copyable "sql" >}}

```sql
BEGIN OPTIMISTIC;
```

Enable [pessimistic transaction](/develop/dev-optimistic-and-pessimistic-transaction.md):

{{< copyable "sql" >}}

```sql
BEGIN PESSIMISTIC;
```

If the current session is in the middle of a transaction when the above statement is executed, the system will automatically submit the current transaction first, and then start a new transaction.

### Commit transaction

The `COMMIT` statement is used to commit all modifications made by TiDB in the current transaction.

{{< copyable "sql" >}}

```sql
COMMIT;
```

Before enabling optimistic transactions, make sure that your application can properly handle errors that may be returned by a `COMMIT` statement. If you are not sure how your application will handle it, it is recommended to use pessimistic transactions instead.

### Rollback transaction

The `ROLLBACK` statement is used to rollback and undo all modifications of the current transaction.

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

Returning to the previous transfer example, after using `ROLLBACK` to roll back the entire transaction, neither Alice nor Bob's balances have changed, and all modifications of the current transaction are canceled together.

{{< copyable "sql" >}}

```sql
TRUNCATE TABLE `users`;

INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (1, 'Alice', 100), (2, 'Bob', 200);

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+

BEGIN;
  UPDATE `users` SET `balance` = `balance` - 20 WHERE `nickname`='Bob';
  UPDATE `users` SET `balance` = `balance` + 20 WHERE `nickname`='Alice';
ROLLBACK;

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+
```

The transaction is also automatically rolled back if the client connection is aborted or closed.

## Transaction isolation level

The transaction isolation level is the basis of database transaction processing. The "I" in **ACID**, that is, Isolation, refers to the isolation of the transaction.

The SQL-92 standard defines four isolation levels: read uncommitted (`READ UNCOMMITTED`), read committed (`READ COMMITTED`), repeatable read (`REPEATABLE READ`), serializable (`SERIALIZABLE`). See the table below for details:

| Isolation Level  | Dirty Write  | Dirty Read   | Fuzzy Read   | Phantom      |
| ---------------- | ------------ | ------------ | ------------ | ------------ |
| READ UNCOMMITTED | Not Possible | Possible     | Possible     | Possible     |
| READ COMMITTED   | Not Possible | Not possible | Possible     | Possible     |
| REPEATABLE READ  | Not Possible | Not possible | Not possible | Possible     |
| SERIALIZABLE     | Not Possible | Not possible | Not possible | Not possible |

TiDB syntax supports setting two isolation levels: `READ COMMITTED` and `REPEATABLE READ`:

{{< copyable "sql" >}}

```sql
mysql> SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
ERROR 8048 (HY000): The isolation level 'READ-UNCOMMITTED' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
mysql> SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
ERROR 8048 (HY000): The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

TiDB implements Snapshot Isolation (SI) level consistency. Also known as "repeatable read" for consistency with MySQL. This isolation level is different from [ANSI Repeatable Read Isolation Level](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read) and [MySQL Repeatable Read Isolation Level](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read). For more details, please read [TiDB Transaction Isolation Levels](/transaction-isolation-levels.md).
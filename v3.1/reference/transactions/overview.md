---
title: Transactions
summary: Learn how to use the distributed transaction statements.
category: reference
---

# Transactions

TiDB supports distributed transactions. The statements that relate to transactions include the `Autocommit` variable, `START TRANSACTION`/`BEGIN`, `COMMIT` and `ROLLBACK`.

## Autocommit

Syntax:

```sql
SET autocommit = {0 | 1}
```

If you set the value of `autocommit` to 1, the status of the current Session is autocommit. If you set the value of `autocommit` to 0, the status of the current Session is non-autocommit. The value of `autocommit` is 1 by default.

When autocommit is enabled, statements are automatically committed immediately following their execution. When autocommit is disabled, statements are only committed when you execute `COMMIT` or as part of an [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). For example, executing `[BEGIN|START TRANSACTION]` implicitly commits the last transaction and starts a new transaction. This behavior is required for MySQL compatibility.

`autocommit` is also a System Variable. You can update the current Session or the Global value using the following variable assignment statement:

```sql
SET @@SESSION.autocommit = {0 | 1};
SET @@GLOBAL.autocommit = {0 | 1};
```

## START TRANSACTION, BEGIN

Syntax:

```sql
BEGIN;

START TRANSACTION;

START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

The three statements above are all statements that transactions start with, through which you can explicitly start a new transaction. If at this time, the current Session is in the process of a transaction, a new transaction is started after the current transaction is committed.

## COMMIT

Syntax:

```sql
COMMIT;
```

This statement is used to commit the current transaction, including all the updates between `BEGIN` and `COMMIT`.

## ROLLBACK

Syntax:

```sql
ROLLBACK;
```

This statement is used to roll back the current transaction and cancels all the updates between `BEGIN` and `COMMIT`.

## Explicit and implicit transaction

TiDB supports explicit transactions (`BEGIN/COMMIT`) and implicit transactions (`SET autocommit = 1`).

If you set the value of `autocommit` to 1 and start a new transaction through the `[BEGIN|START TRANSACTION]` statement, the autocommit is disabled before `COMMIT`/`ROLLBACK` which makes the transaction becomes explicit.

For DDL statements, the transaction is committed automatically and does not support rollback. If you run the DDL statement while the current Session is in the process of a transaction, the DDL statement is executed after the current transaction is committed.

## Transaction isolation level

TiDB **only supports** `SNAPSHOT ISOLATION`. You can set the isolation level of the current Session to `READ COMMITTED` using the following statement. However, TiDB is only compatible with the `READ COMMITTED` isolation level in syntax and transactions are still executed at the `SNAPSHOT ISOLATION` level.

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Lazy check of constraints

**Lazy check** means that by default TiDB will not check [primary key](/v3.1/reference/sql/constraints.md#primary-key) or [unique constraints](/v3.1/reference/sql/constraints.md#unique) when an `INSERT` statement is executed, but instead checks when the transaction is committed. In TiDB, the lazy check is performed for values written by ordinary `INSERT` statements.

For example:

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
START TRANSACTION;
INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
INSERT INTO t1 VALUES (2);
COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
```

The lazy check is important because if you perform a unique constraint check on every `INSERT` statement in a transaction, it can cause high network overhead. A batch check when the transaction is committed can greatly improve performance.

> **Note:**
>
> This optimization does not take effect for `INSERT IGNORE` and `INSERT ON DUPLICATE KEY UPDATE`, only for normal `INSERT` statements. The behavior can also be disabled by setting `tidb_constraint_check_in_place=TRUE`.

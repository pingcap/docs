---
title: Metadata Lock
summary: Introduce the concept, principles, and implementation details of metadata lock in TiDB.
---

# Metadata Lock

This document introduces the metadata lock in TiDB.

## Concept

TiDB uses the online asynchronous schema change algorithm to support changing metadata objects. When a transaction is executed, the transaction obtains the corresponding metadata snapshot on the transaction start time. If the metadata is changed during the transaction execution, to ensure the data consistency, TiDB returns an `Information schema is changed` error and the transaction fails to commit.

To solve the preceding problem, TiDB v6.3.0 introduces the metadata lock feature into the online DDL algorithm. To avoid DML statements errors as much as possible, TiDB coordinates the priority of DML statements and DDL statements in the process of changing table metadata and ensures that executing DDL statements wait for the DML statements with old version metadata can be committed.

## Scenarios

The metadata lock in TiDB applies to all DDL statements, such as:

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
- [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
- [`DROP PARTITION`](/partitioned-table.md#partition-management)
- [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
- [`EXCHANGE PARTITION`](/partitioned-table.md#partition-management)
- [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

Adding the metadata lock feature might have some performance impact on the execution of the DDL task in TiDB. To reduce the impact, the following lists some scenarios that do not require the metadata lock:

+ `SELECT` queries with auto-commit enabled
+ Stale Read is enabled
+ Access temporary tables

## Usage

To control whether to enable the metadata lock feature or not, you can use the system variable [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630).

## Principles

### Background

DDL operations in TiDB are the online DDL mode. During the execution of a DDL statement, the metadata version of the defined object needs to be modified and multiple minor version changes are required. The online asynchronous change of metadata algorithm only demonstrates that two adjacent minor versions are compatible, that is, between two adjacent metadata versions, operating between versions will not destroy the data consistency stored by the DDL change object.

When adding an index to a table, the status of the DDL statement changes as follows: None -> Delete Only, Delete Only -> Write Only, Write Only -> Write Reorg, Write Reorg -> Public.

The following commit process of transactions violates the preceding constraint:

| Transaction  | Version used by transaction  | Latest version in the cluster | Version difference |
|:-----|:-----------|:-----------|:----|
| txn1 | None       | None       | 0   |
| txn2 | DeleteOnly | DeleteOnly | 0   |
| txn3 | WriteOnly  | WriteOnly  | 0   |
| txn4 | None       | WriteOnly  | 2   |
| txn5 | WriteReorg | WriteReorg | 0   |
| txn6 | WriteOnly  | WriteReorg | 1   |
| txn7 | Public     | Public     | 0   |

In the preceding table, the metadata version used when `txn4` is committed is two versions different from the latest version in the cluster. This might cause data inconsistency.

### Implementation details

Introducing the metadata lock can ensure that the metadata versions used by all transactions in a TiDB cluster differ by at most one version. To achieve this goal, TiDB uses the following two rules:

- When executing a DML statement, TiDB records the metadata objects accessed by the DML statement in the transaction context, such as tables, views, and corresponding metadata versions.

- When executing a DDL statement to change status, the latest version of metadata is pushed to all TiDB nodes. If the difference between the metadata version used by all transactions related to this status change on a TiDB node, and the current metadata version is less than 2, the TiDB node acquires the metadata lock of the metadata object. The next status change can only be executed when all TiDB nodes in the cluster have obtained the metadata lock of the metadata object.

## Impact

- For DML statements, metadata lock does not cause DML statements to be blocked, thus the deadlock problem will not occur.
- After enabling the metadata lock and the metadata information of a metadata object in a transaction is determined at the first access and is not changed.
- For DDL statements, when changing metadata status, DDL statements might be blocked by transactions with old version metadata. The following is an example:

  | Session 1 | Session 2 |
  |:---------------------------|:----------|
  | `CREATE TABLE t (a INT);`  |           |
  | `INSERT INTO t VALUES(1);` |           |
  | `BEGIN;`                   |           |
  |                            | `ALTER TABLE t ADD COLUMN b INT;` |
  | `SELECT * FROM t;`<br/>(Use the current metadata version of table `t`. Return `(a=1，b=NULL)` and lock table `t`.)         |           |
  |                            | `ALTER TABLE t ADD COLUMN c INT;` (blocked by Session 1) |

  At the repeatable read isolation level, if a DDL that requires data changes is performed during the metadata process of determining a table from the start of the transaction, such as adding an index, or changing column types. It performs as the following:

  | Session 1                  | Session 2                                 |
  |:---------------------------|:------------------------------------------|
  | `CREATE TABLE t (a INT);`  |                                           |
  | `INSERT INTO t VALUES(1);` |                                           |
  | `BEGIN;`                   |                                           |
  |                            | `ALTER TABLE t ADD INDEX idx(a);`         |
  | `SELECT * FROM t;` (index `idx` is not available) |                                 |
  | `COMMIT;`                  |                                           |
  | `BEGIN;`                   |                                           |
  |                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
  | `SELECT * FROM t;` (return an error `Information schema is changed`) |             |

## Troubleshoot blocked DDLs

TiDB v6.3.0 introduces the `mysql.tidb_mdl_view` view to help you obtain the information of the current blocked DDL.

> **Note:**
>
> To select the `mysql.tidb_mdl_view` view, [`PROCESS` privilege](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) is required.

The following takes adding an index for table `t` as an example. Assume a DDL statement `ALTER TABLE t ADD INDEX idx(a)`:

```sql
SELECT * FROM mysql.tidb_mdl_view\G
*************************** 1. row ***************************
    JOB_ID: 141
   DB_NAME: test
TABLE_NAME: t
     QUERY: ALTER TABLE t ADD INDEX idx(a)
SESSION ID: 2199023255957
  TxnStart: 08-30 16:35:41.313(435643624013955072)
SQL_DIGESTS: ["begin","select * from `t`"]
1 row in set (0.02 sec)
```

From the preceding output, you can see that the transaction whose `SESSION ID` is `2199023255957` blocks the adding index DDL. `SQL_DIGEST` shows the SQL statements executed by this transaction, which is ``["begin","select * from `t`"]``. To make the blocked DDL continue to execute, you can use the following global `KILL` statement to kill the `2199023255957` transaction:

```sql
mysql> KILL 2199023255957;
Query OK, 0 rows affected (0.00 sec)
```

After killing the transaction, you can select the `mysql.tidb_mdl_view` view again. At this time, the preceding transaction is not shown in the output, which means the DDL is not blocked.

```sql
SELECT * FROM mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

---
title: Changefeed DDL Replication
summary: Learn about the DDL statements supported by TiCDC and some special cases.
---

# Changefeed DDL Replication

This document describes the rules and special cases of DDL replication in TiCDC.

## DDL allow list

Currently, TiCDC uses an allow list to determine whether to replicate a DDL statement. Only the DDL statements in the allow list are replicated to the downstream. The DDL statements not in the allow list are not replicated.

In addition, TiCDC determines whether to replicate a DDL statement to the downstream based on whether the table has a [valid index](/ticdc/ticdc-overview.md#valid-index) and whether the configuration item [`force-replicate`](/ticdc/ticdc-changefeed-config.md#force-replicate) is set to `true`. When `force-replicate=true`, the replication task attempts to forcibly [replicate tables without a valid index](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index).

The following is the allow list of DDL statements supported by TiCDC. The abbreviations in the table:

- Y: Replication to the downstream is supported in this condition.
- N: Replication to the downstream is not supported in this condition.

> **Note**
>
> - When the upstream table has no valid index and `force-replicate=true` is not configured, the table will not be replicated. However, subsequent DDL statements (including `CREATE INDEX`, `ADD INDEX`, and `ADD PRIMARY KEY`) that create a valid index on this table will be replicated, which might cause inconsistency between downstream and upstream table schemas and lead to subsequent data replication failure.
> - DDL statements (including `DROP INDEX` and `DROP PRIMARY KEY`) that drop the last valid index will not be replicated, causing subsequent data replication to fail.

| DDL | A valid index exists | A valid index does not exist and `force-replicate` is `false` (default) | A valid index does not exist and `force-replicate` is set to `true` |
|---|:---:|:---:| :---: |
| `CREATE DATABASE` | Y | Y | Y |
| `DROP DATABASE` | Y | Y | Y |
| `ALTER DATABASE CHARACTER SET` | Y | Y | Y |
| `CREATE INDEX` | Y | Y | Y |
| `ADD INDEX` | Y | Y | Y |
| `DROP INDEX` | Y | N | Y |
| `ADD PRIMARY KEY` | Y | Y | Y |
| `DROP PRIMARY KEY` | Y | N | Y |
| `CREATE TABLE` | Y | N | Y |
| `DROP TABLE` | Y | N | Y |
| `ADD COLUMN` | Y | N | Y |
| `DROP COLUMN` | Y | N | Y |
| `TRUNCATE TABLE` | Y | N | Y |
| `MODIFY COLUMN` | Y | N | Y |
| `RENAME TABLE` | Y | N | Y |
| `ALTER COLUMN DEFAULT VALUE` | Y | N | Y |
| `ALTER TABLE COMMENT` | Y | N | Y |
| `RENAME INDEX` | Y | N | Y |
| `ADD PARTITION` | Y | N | Y |
| `DROP PARTITION` | Y | N | Y |
| `TRUNCATE PARTITION` | Y | N | Y |
| `CREATE VIEW` | Y | N | Y |
| `DROP VIEW` | Y | N | Y |
| `ALTER TABLE CHARACTER SET` | Y | N | Y |
| `RECOVER TABLE` | Y | N | Y |
| `REBASE AUTO ID` | Y | N | Y |
| `ALTER TABLE INDEX VISIBILITY` | Y | N | Y |
| `EXCHANGE PARTITION` | Y | N | Y |
| `REORGANIZE PARTITION` | Y | N | Y |
| `ALTER TABLE TTL` | Y | N | Y |
| `ALTER TABLE REMOVE TTL` | Y | N | Y |

## DDL replication considerations

### Asynchronous execution of `ADD INDEX` and `CREATE INDEX` DDLs

When the downstream is TiDB, TiCDC executes `ADD INDEX` and `CREATE INDEX` DDL operations asynchronously to minimize the impact on changefeed replication latency. This means that, after replicating `ADD INDEX` and `CREATE INDEX` DDLs to the downstream TiDB for execution, TiCDC returns immediately without waiting for the completion of the DDL execution. This avoids blocking subsequent DML executions.

During the execution of the `ADD INDEX` or `CREATE INDEX` DDL operation in the downstream, when TiCDC executes the next DDL operation of the same table, this DDL operation might be blocked in the `queueing` state for a long time. This can cause TiCDC to repeatedly execute this DDL operation, and if retries take too long, it might lead to replication task failure. Starting from v8.4.0, if TiCDC has the `SUPER` permission of the downstream database, it periodically runs `ADMIN SHOW DDL JOBS` to check the status of asynchronously executed DDL tasks. TiCDC will wait for index creation to complete before proceeding with replication. Although this might increase replication latency, it avoids replication task failure.

> **Note:**
>
> - If the execution of certain downstream DMLs relies on indexes that have not completed replication, these DMLs might be executed slowly, thereby affecting TiCDC replication latency.
> - Before replicating DDLs to the downstream, if a TiCDC node crashes or if the downstream is performing other write operations, the DDL replication has an extremely low probability of failure. You can check the downstream to see whether that occurs.

### DDL replication considerations for renaming tables

Due to the lack of some context during the replication process, TiCDC has some constraints on the replication of `RENAME TABLE` DDLs.

#### Rename a single table in a DDL statement

If a DDL statement renames a single table, TiCDC only replicates the DDL statement when the old table name matches the filter rule. The following is an example.

Assume that the configuration file of your changefeed is as follows:

```toml
[filter]
rules = ['test.t*']
```

TiCDC processes this type of DDL as follows:

| DDL | Whether to replicate | Reason for the handling |
| --- | --- | --- |
| `RENAME TABLE test.t1 TO test.t2` | Replicate | `test.t1` matches the filter rule |
| `RENAME TABLE test.t1 TO ignore.t1` | Replicate | `test.t1` matches the filter rule |
| `RENAME TABLE ignore.t1 TO ignore.t2` | Ignore | `ignore.t1` does not match the filter rule |
| `RENAME TABLE test.n1 TO test.t1` | Report an error and exit the replication | `test.n1` does not match the filter rule, but `test.t1` matches the filter rule. This operation is illegal. In this case, refer to the error message for handling. |
| `RENAME TABLE ignore.t1 TO test.t1` | Report an error and exit the replication | Same reason as above. |

#### Rename multiple tables in a DDL statement

If a DDL statement renames multiple tables, TiCDC only replicates the DDL statement when the old database name, old table names, and the new database name all match the filter rule.

In addition, TiCDC does not support the `RENAME TABLE` DDL that swaps the table names. The following is an example.

Assume that the configuration file of your changefeed is as follows:

```toml
[filter]
rules = ['test.t*']
```

TiCDC processes this type of DDL as follows:

| DDL | Whether to replicate | Reason for the handling |
| --- | --- | --- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4` | Replicate | All database names and table names match the filter rule. |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2` | Replicate | The old database name, the old table names, and the new database name match the filter rule. |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;` | Report an error | The new database name `ignore` does not match the filter rule. |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3;` | Report an error | The `RENAME TABLE` DDL swaps the names of `test.t1` and `test.t3` in one DDL statement, which TiCDC cannot handle correctly. In this case, refer to the error message for handling. |

### DDL statement considerations

When executing cross-database DDL statements (such as `CREATE TABLE db1.t1 LIKE t2`) in the upstream, it is recommended that you explicitly specify all relevant database names in DDL statements (such as `CREATE TABLE db1.t1 LIKE db2.t2`). Otherwise, cross-database DDL statements might not be executed correctly in the downstream due to the lack of database name information.

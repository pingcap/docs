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

Although TiCDC usually replicates DDL statements in order, when the downstream is TiDB, TiCDC executes DDL operations for creating and adding indexes asynchronously. This means that, after replicating `ADD INDEX` and `CREATE INDEX` DDLs to the downstream TiDB cluster for execution, TiCDC returns immediately without waiting for DDL execution to complete. This minimizes the impact on changefeed replication latency and avoids blocking subsequent DML executions.

During the execution of the `ADD INDEX` or `CREATE INDEX` DDL operation in the downstream, when TiCDC executes the next DDL operation of the same table, this DDL operation might be blocked in the `queueing` state for a long time. This can cause TiCDC to repeatedly execute this DDL operation, and if retries take too long, it might lead to replication task failure. Starting from v8.4.0, if TiCDC has the `SUPER` permission of the downstream database, it periodically runs `ADMIN SHOW DDL JOBS` to check the status of asynchronously executed DDL tasks. TiCDC will wait for index creation to complete before proceeding with replication. Although this might increase replication latency, it avoids replication task failure.

> **Note:**
>
> - If the execution of certain downstream DMLs relies on indexes that have not completed replication, these DMLs might be executed slowly, thereby affecting TiCDC replication latency.
> - Before replicating DDLs to the downstream, if a TiCDC node crashes or if the downstream is performing other write operations, the DDL replication has an extremely low probability of failure. You can check the downstream to see whether that occurs.

### DDL replication considerations for renaming tables

TiCDC determines whether to replicate `RENAME TABLE` DDLs based on the database and table names before and after renaming and the filter rules. The following examples assume that the tables meet the replication requirements and that no additional DDL event filter rules are configured.

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
| `RENAME TABLE test.n1 TO test.t1` | Report an error and stop replication | The old table name `test.n1` does not match the filter rule, but the new table name `test.t1` matches the filter rule. This operation is invalid. In this case, refer to the error message for handling. |
| `RENAME TABLE ignore.t1 TO test.t1` | Report an error and stop replication | Same reason as above. |

These rules apply to both the classic and new architectures. If the old table name matches the filter rule but the new table name does not, TiCDC replicates the `RENAME TABLE` DDL and then stops replicating subsequent data changes for that table. If the old table name does not match but the new table name matches, TiCDC reports the `CDC:ErrSyncRenameTableFailed` error because replicating only the rename cannot backfill data that was not previously replicated for that table.

#### Rename multiple tables in a DDL statement

When a DDL statement renames multiple tables, the new architecture evaluates each rename step according to the single-table rename rules:

- If the old table name matches the filter rule, TiCDC replicates the corresponding rename step.
- If neither the old nor the new table name matches, TiCDC ignores that step.
- If the old table name does not match but the new table name does, the changefeed reports an error and replication stops.

In addition, the classic architecture requires the target database of each replicated rename step to be within the replication scope. It also does not support `RENAME TABLE` statements that swap table names.

Assume that the configuration file of your changefeed is as follows:

```toml
[filter]
rules = ['test.t*']
```

TiCDC processes this type of DDL as follows:

| DDL | Classic architecture | New architecture | Reason |
| --- | --- | --- | --- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4` | Replicate | Replicate | Both the old and new database and table names match the filter rule |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2` | Replicate | Replicate | In both architectures, the old table names match the filter rule. The classic architecture additionally requires the target database to be within the replication scope. After replicating the rename, TiCDC stops replicating subsequent data changes for the renamed tables |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22` | Report an error | Replicate | The target database `ignore` is not within the replication scope. After replicating the rename in the new architecture, TiCDC stops replicating `ignore.t1` and continues replicating `test.t22` |
| `RENAME TABLE test.t1 TO test.t2, ignore.t1 TO ignore.t2` | Replicate only the rename step of `test.t1` | Replicate only the rename step of `test.t1` | Neither `ignore.t1` nor `ignore.t2` matches the filter rule |
| `RENAME TABLE test.t1 TO test.t2, ignore.t1 TO test.t3` | Report an error | Report an error | `ignore.t1` does not match but `test.t3` matches the filter rule |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3` | Report an error | Replicate | The two table names are swapped through the temporary table name `test.t4`, and the new architecture preserves the order of each rename step |

In the new architecture, TiCDC coordinates the replication progress of all tables involved in a multi-table rename, but reconstructs the downstream SQL as multiple single-table `RENAME TABLE` statements. The MySQL sink executes multiple sub-statements separated by semicolons, while the Kafka and Pulsar sinks split them into single-table DDL messages. Therefore, downstream execution does not guarantee the atomicity of a single upstream multi-table rename statement. When using a temporary table name to swap table names, keep all mutually dependent steps and avoid removing any of them through filter rules.

### DDL statement considerations

When executing cross-database DDL statements (such as `CREATE TABLE db1.t1 LIKE t2`) in the upstream, it is recommended that you explicitly specify all relevant database names in DDL statements (such as `CREATE TABLE db1.t1 LIKE db2.t2`). Otherwise, cross-database DDL statements might not be executed correctly in the downstream due to the lack of database name information.

### Handling of DDL SQL text

TiCDC parses, formats, or rebuilds DDL SQL. Therefore, the SQL text replicated downstream is not guaranteed to exactly match the original upstream statement. Both the classic and new architectures normalize keyword case, identifier quotes, spaces, and some synonymous syntax, and both also handle TiDB-specific syntax for compatibility. DDLs such as `DROP TABLE`, `DROP VIEW`, and `EXCHANGE PARTITION` all have SQL rebuilding logic in both architectures.

The new architecture might also modify DDL SQL in the following ways. Except for MySQL sink rewrites specifically noted, these changes also affect the SQL field in message protocols that support DDL. The exact output format might vary by TiCDC version.

| DDL or scenario | SQL text handling in the new architecture | Applicable conditions |
| --- | --- | --- |
| Single-table rename | Uniformly rebuilt as `RENAME TABLE db.old_table TO db.new_table` with full database and table names | Includes `ALTER TABLE ... RENAME AS ...`, `ALTER TABLE ... RENAME TO ...`, and regular `RENAME TABLE ... TO ...`. It is also rewritten when table routing is not enabled |
| Multi-table rename | Rebuilt in the original order into multiple single-table `RENAME TABLE` statements, with each sub-statement ending with `;` | The MySQL sink receives the combined SQL; paths that output one table at a time, such as Kafka and Pulsar, split it into multiple messages |
| Batch table creation | Each split `CREATE TABLE` statement ends with `;` | The upstream batch table creation produces one DDL event containing multiple tables, and the downstream outputs it as single-table events |
| `CREATE TABLE ... LIKE ...` | Adds the missing database qualifier to the table referenced by `LIKE` | The original SQL does not qualify the database name of the referenced table, and the DDL metadata indicates that the referenced table and the target table are in different databases |
| `CREATE VIEW` and `CREATE OR REPLACE VIEW` | Rebuilds SQL using the view query stored by TiDB and the database and table metadata at the DDL time, and might add database qualifiers to table and column references, normalize identifier case, or add column aliases | When names in the view definition need to be parsed; table routing does not need to be enabled |
| Anonymous secondary indexes | Adds the upstream-generated index names for unnamed indexes in `ALTER TABLE ... ADD INDEX/KEY/...`, including multiple change operations in one `ALTER TABLE` | Processed only before the MySQL sink executes DDL on MySQL or TiDB, and does not apply to SQL in MQ messages |
| Databases, tables, or partitions whose names contain backticks | When rebuilding SQL, escapes backticks in names as two backticks | Includes scenarios such as rename, `DROP TABLE`, `DROP VIEW`, and `EXCHANGE PARTITION` that require SQL rebuilding |
| Table routing | Rewrites database names, table names, and related references according to routing rules, and regenerates SQL | `target-schema` or `target-table` is configured. For more information, see [DDL behavior of table routing](/ticdc/ticdc-table-routing.md#ddl-behavior) |

For example, assume that the current database is `db`, table routing is not enabled, and the following rename events are not filtered. The outputs for single-table rename are as follows. Statement-ending semicolons are omitted in the table.

| Upstream SQL | Classic architecture output | New architecture output |
| --- | --- | --- |
| `ALTER TABLE a RENAME AS b` | ``ALTER TABLE `a` RENAME AS `b` `` | ``RENAME TABLE `db`.`a` TO `db`.`b` `` |
| `ALTER TABLE a RENAME TO b` | ``ALTER TABLE `a` RENAME AS `b` `` | ``RENAME TABLE `db`.`a` TO `db`.`b` `` |
| `RENAME TABLE a TO b` | ``RENAME TABLE `a` TO `b` `` | ``RENAME TABLE `db`.`a` TO `db`.`b` `` |

For `RENAME TABLE a TO b, c TO d`, when output as single-table events, the first SQL in the classic architecture is ``RENAME TABLE `db`.`a` TO `db`.`b` ``, and in the new architecture it is ``RENAME TABLE `db`.`a` TO `db`.`b`;``. The trailing semicolon comes from the multi-table DDL splitting in the new architecture.

When developing downstream consumers or comparing the outputs of the classic and new architectures, parse the SQL and use the DDL type and database and table metadata to assess its meaning instead of comparing SQL text directly. Database names, table names, index names, and their letter case still need to be validated according to the specific scenario to avoid overlooking name resolution or table routing errors.

### Notes on using event filter rules to filter DDL events

If a filtered DDL statement involves table creation or deletion, TiCDC only filters out the DDL statement without affecting the replication behavior of DML statements. The following is an example.

Assume that the configuration file of your changefeed is as follows:

```toml
[filter]
rules = ['test.t*']

[[filter.event-filters]]
matcher = ["test.t1"] # This filter rule applies only to the t1 table in the test database.
ignore-event = ["create table", "drop table", "truncate table", "rename table"]
```

| DDL | DDL behavior | DML behavior | Explanation |
| --- | --- | --- | --- |
| `CREATE TABLE test.t1 (id INT, name VARCHAR(50));` | Ignore | Replicate | `test.t1` matches the event filter rule, so the `CREATE TABLE` event is ignored. The replication of DML events remains unaffected. |
| `CREATE TABLE test.t2 (id INT, name VARCHAR(50));` | Replicate | Replicate | `test.t2` does not match the event filter rule. |
| `CREATE TABLE test.ignore (id INT, name VARCHAR(50));` | Ignore | Ignore | `test.ignore` matches the event filter rule, so both DDL and DML events are ignored. |
| `DROP TABLE test.t1;` | Ignore | - | `test.t1` matches the event filter rule, so the `DROP TABLE` event is ignored. Because the table is deleted, TiCDC no longer replicates DML events for `t1`. |
| `TRUNCATE TABLE test.t1;` | Ignore | Replicate | `test.t1` matches the event filter rule, so the `TRUNCATE TABLE` event is ignored. The replication of DML events remains unaffected. |
| `RENAME TABLE test.t1 TO test.t2;` | Ignore | Replicate | `test.t1` matches the event filter rule, so the `RENAME TABLE` event is ignored. The replication of DML events remains unaffected. |
| `RENAME TABLE test.t1 TO test.ignore;` | Ignore | Ignore | `test.t1` matches the event filter rule, so the `RENAME TABLE` event is ignored. `test.ignore` matches the event filter rule, so both DDL and DML events are ignored. |

When using `ignore-sql` to filter multi-table rename operations, note that the matching input differs between the classic and new architectures. In the classic architecture, `ignore-sql` is matched against each SQL statement after splitting the operation into single-table DDL events. In the new architecture, `ignore-sql` is matched against the reconstructed SQL for the entire multi-table rename operation when event filter rules are applied to individual tables. If the `matcher` of the same event filter rule matches multiple tables, `ignore-sql` matching one rename step might also filter other rename steps covered by that rule. Before switching architectures, check the actual matching results of such filter rules.

> **Note:**
>
> - When replicating data to a database, use the event filter to filter DDL events with caution. Ensure that the upstream and downstream database schemas remain consistent during replication. Otherwise, TiCDC might report errors or cause undefined replication behavior.
> - For versions earlier than v6.5.8, v7.1.4, and v7.5.1, using the event filter to filter DDL events involving table creation or deletion affects DML replication. It is not recommended to use this feature in these versions.

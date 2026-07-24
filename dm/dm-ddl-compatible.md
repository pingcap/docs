---
title: Special Handling of DM DDLs
summary: Learn how DM parses and handles DDL statements according to the statement types.
---

# Special Handling of DM DDLs

When TiDB Data Migration (DM) migrates data, it parses the DDL statements and handles them according to the statement type and the current migration stage.

## Skip DDL statements

The following statements are not supported by DM, so DM skips them directly after parsing.

<table>
    <tr>
        <th>Description</th>
        <th>SQL</th>
    </tr>
    <tr>
        <td>transaction</td>
        <td><code>^SAVEPOINT</code></td>
    </tr>
    <tr>
        <td>skip all flush sqls</td>
        <td><code>^FLUSH</code></td>
    </tr>
    <tr>
        <td rowspan="3">table maintenance</td>
        <td><code>^OPTIMIZE\\s+TABLE</code></td>
    </tr>
    <tr>
        <td><code>^ANALYZE\\s+TABLE</code></td>
    </tr>
    <tr>
        <td><code>^REPAIR\\s+TABLE</code></td>
    </tr>
    <tr>
        <td>temporary table</td>
        <td><code>^DROP\\s+(\\/\\*\\!40005\\s+)?TEMPORARY\\s+(\\*\\/\\s+)?TABLE</code></td>
    </tr>
    <tr>
        <td rowspan="2">trigger</td>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?TRIGGER</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+TRIGGER</code></td>
    </tr>
    <tr>
        <td rowspan="3">procedure</td>
        <td><code>^DROP\\s+PROCEDURE</code></td>
    </tr>
    <tr>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?PROCEDURE</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+PROCEDURE</code></td>
    </tr>
    <tr>
        <td rowspan="3">view</td>
        <td><code>^CREATE\\s*(OR REPLACE)?\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?\\s+(SQL SECURITY DEFINER)?VIEW</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+VIEW</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?(SQL SECURITY DEFINER)?VIEW</code></td>
    </tr>
    <tr>
        <td rowspan="4">function</td>
        <td><code>^CREATE\\s+(AGGREGATE)?\\s*?FUNCTION</code></td>
    </tr>
    <tr>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?FUNCTION</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+FUNCTION</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+FUNCTION</code></td>
    </tr>
    <tr>
        <td rowspan="3">tableSpace</td>
        <td><code>^CREATE\\s+TABLESPACE</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+TABLESPACE</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+TABLESPACE</code></td>
    </tr>
    <tr>
        <td rowspan="3">event</td>
        <td><code>^CREATE\\s+(DEFINER\\s?=.+?)?EVENT</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+(DEFINER\\s?=.+?)?EVENT</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+EVENT</code></td>
    </tr>
    <tr>
        <td rowspan="7">account management</td>
        <td><code>^GRANT</code></td>
    </tr>
    <tr>
        <td><code>^REVOKE</code></td>
    </tr>
    <tr>
        <td><code>^CREATE\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^ALTER\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^RENAME\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+USER</code></td>
    </tr>
    <tr>
        <td><code>^DROP\\s+USER</code></td>
    </tr>
</table>

## Rewrite DDL statements

The following statements are rewritten before being replicated to the downstream.

|Original statement|Rewritten statement|
|-|-|
|`^CREATE DATABASE...`|`^CREATE DATABASE...IF NOT EXISTS`|
|`^CREATE TABLE...`|`^CREATE TABLE..IF NOT EXISTS`|
|`^DROP DATABASE...`|`^DROP DATABASE...IF EXISTS`|
|`^DROP TABLE...`|`^DROP TABLE...IF EXISTS`|
|`^DROP INDEX...`|`^DROP INDEX...IF EXISTS`|

## Multi-schema-change DDL statements

In some handling paths, such as replaying DDL statements recorded from gh-ost or pt-osc shadow tables during online DDL cut-over, DM might split a multi-schema-change `ALTER TABLE` statement into multiple standalone DDL statements. After the split, each generated DDL statement is applied independently to TiDB and to DM's schema tracker. Therefore, a statement that is accepted by the upstream as one atomic multi-change `ALTER TABLE` might fail after it is split if the generated DDL order is not independently executable. This does not necessarily mean that the original upstream DDL is invalid.

For example, some MySQL-compatible upstreams support replacing an existing index with the same name in one statement:

```sql
ALTER TABLE t ADD UNIQUE INDEX idx(c), DROP INDEX idx;
```

If DM splits or replays this statement as `ADD UNIQUE INDEX idx(c)` before `DROP INDEX idx`, the `ADD` statement fails because the old `idx` still exists. To avoid this issue, use DDL statements whose split execution order is valid on TiDB, such as dropping the old index and adding the new index as separate DDL statements in a safe order. If the migration task has already paused on such a DDL, use [`binlog replace`](/dm/handle-failed-ddl-statements.md) to replace it with equivalent TiDB-compatible DDL statements.

## Shard merge migration tasks

When DM merges and migrates tables in pessimistic or optimistic mode, the behavior of DDL replication is different from that in other scenarios. For details, refer to [Pessimistic Mode](/dm/feature-shard-merge-pessimistic.md) and [Optimistic Mode](/dm/feature-shard-merge-optimistic.md).

## Online DDL

The Online DDL feature also handles DDL events in a special way. For details, refer to [Migrate from Databases that Use GH-ost/PT-osc](/dm/feature-online-ddl.md).

---
title: Best Practices for Managing Indexes and Identifying Unused Indexes
summary: Learn the best practices for managing and optimizing indexes, identifying and removing unused indexes in TiDB.
---

# Best Practices for Managing Indexes and Identifying Unused Indexes

Indexes are essential for optimizing database query performance, reducing the need to scan large amounts of data. However, as applications evolve, business logic changes, and data volume grows, the original index design can also encounter issues, including the following:

- Unused indexes: these indexes are once relevant but are no longer selected by the query optimizer, consuming storage and adding unnecessary overhead to write operations.
- Inefficient indexes: some indexes are used by the optimizer but scan more data than expected, increasing disk I/O and slowing down query performance.

If left unaddressed, these indexing issues can cause higher storage costs, degraded performance, and operational inefficiencies. In a distributed SQL database like TiDB, indexing inefficiencies have an even greater impact due to the scale of distributed queries and the complexity of multi-node coordination. That is why regular index audits are crucial for keeping your database optimized.

Proactively identifying and optimizing indexes helps:

- Reduce storage overhead: removing unused indexes frees up disk space and reduces long-term storage costs.
- Improve write performance: write-heavy workloads (such as `INSERT`, `UPDATE`, and `DELETE`) perform better when unnecessary index maintenance is eliminated.
- Optimize query execution: efficient indexes reduce the number of rows scanned, improving query speed and response time.
- Streamline database management: fewer and well-optimized indexes simplify backups, recovery, and schema changes.

Because indexes evolve with changing business logic, regular index audits are a standard part of database maintenance. TiDB provides built-in observability tools to help you detect, evaluate, and optimize indexes safely and effectively.

TiDB v8.0.0 introduces the [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) table and the [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) table to help you track index usage patterns and make data-driven decisions.

This document describes the tools that you can use to detect and remove unused or inefficient indexes, thus improving TiDB's performance and stability.

## TiDB index optimization: a data-driven approach

Indexes are essential for query performance, but removing them without proper analysis can lead to unexpected regressions or even system instability. To ensure safe and effective index management, TiDB provides built-in observability tools that let you do the following:

- Track index usage in real-time: identify how often an index is accessed and whether it contributes to performance improvements.
- Detect unused indexes: locate indexes that have not been used since the database is last restarted.
- Assess index efficiency: evaluate whether an index filters data effectively or causes excessive I/O overhead.
- Safely test index removal: temporarily make an index invisible before deleting it to ensure no queries depend on it.

TiDB simplifies index optimization by introducing the following tools:

- `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`: monitors index usage patterns and query frequency.
- `sys.schema_unused_indexes`: lists indexes that have not been used since the database is last restarted.
- Invisible indexes: allows you to test the impact of removing an index before permanently deleting it.

By using these observability tools, you can confidently clean up redundant indexes without risking performance degradation.

## Track index usage using `TIDB_INDEX_USAGE`

Introduced in [TiDB v8.0.0](/releases/release-8.0.0.md), the `TIDB_INDEX_USAGE` system table provides real-time insights into how indexes are used, helping you optimize query performance and remove unnecessary indexes.

Specifically, you can use the `TIDB_INDEX_USAGE` system table to do the following:

- Detect unused indexes: identify indexes that have not been accessed by queries, helping determine which ones can be safely removed.
- Analyze index efficiency: track how frequently an index is used and whether it contributes to efficient query execution.
- Evaluate query patterns: understand how indexes affect read operations, data scans, and key-value (KV) requests.

Starting from [TiDB v8.4.0](/releases/release-8.4.0.md), the `TIDB_INDEX_USAGE` system table also includes primary keys in clustered tables, offering deeper visibility into index performance.

### Key metrics in `TIDB_INDEX_USAGE`

If you want to check the fields in the `TIDB_INDEX_USAGE` system table, run the following SQL statement:

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_INDEX_USAGE;
```

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

For explanations of these columns, see [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md).

### Identify unused and inefficient indexes using `TIDB_INDEX_USAGE`

This section describes how to identify unused and inefficient indexes using the `TIDB_INDEX_USAGE` system table.

- Unused indexes:

    - If `QUERY_TOTAL = 0`, the index has not been used by any queries.
    - If `LAST_ACCESS_TIME` shows a long time ago, the index might no longer be relevant.

- Inefficient indexes:

    - Large values in `PERCENTAGE_ACCESS_100` suggest full index scans, which might indicate an inefficient index.
    - Compare `ROWS_ACCESS_TOTAL` and `QUERY_TOTAL` to determine whether the index scans too many rows relative to its usage.

By using the `TIDB_INDEX_USAGE` system table, you can gain detailed insights into index performance, making it easier to remove unnecessary indexes and optimize query execution.

### Use `TIDB_INDEX_USAGE` effectively

The following points help you understand and use the `TIDB_INDEX_USAGE` system table correctly.

#### Data updates are delayed

To minimize performance impact, `TIDB_INDEX_USAGE` does not update instantly. Index usage metrics might be delayed by up to 5 minutes. Keep this latency in mind when you analyze queries.

#### Index usage data is not persisted

The `TIDB_INDEX_USAGE` system table stores data in memory of each TiDB instance, and is not persisted. When a TiDB node restarts, all index usage statistics from that node are cleared.

#### Track historical data

You can periodically export index usage snapshots using the following SQL statement:

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEX_USAGE INTO OUTFILE '/backup/index_usage_snapshot.csv';
```

This enables historical tracking by comparing snapshots over time, helping you detect trends in index usage and make more informed pruning decisions.

## Consolidate index usage data across TiDB nodes using `CLUSTER_TIDB_INDEX_USAGE`

Because TiDB is a distributed SQL database, query workloads are spread across multiple nodes. Each TiDB node tracks its own local index usage. For a global view of index performance, TiDB provides the [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) system table. This view consolidates index usage data from all TiDB nodes, ensuring that distributed query workloads are fully accounted for when optimizing indexing strategies.

Different TiDB nodes might experience different query workloads. An index that appears unused on some nodes might still be critical elsewhere. To segment index analysis by workload, run the following SQL statement:

```sql
SELECT INSTANCE, TABLE_NAME, INDEX_NAME, SUM(QUERY_TOTAL) AS total_queries
FROM INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE
GROUP BY INSTANCE, TABLE_NAME, INDEX_NAME
ORDER BY total_queries DESC;
```

This helps determine whether an index is truly unused across all nodes or only for specific instances, allowing you to make informed decisions on index removal.

### Key differences between `TIDB_INDEX_USAGE` and `CLUSTER_TIDB_INDEX_USAGE`

The following table shows the key differences between `TIDB_INDEX_USAGE` and `CLUSTER_TIDB_INDEX_USAGE`:

| Feature          | `TIDB_INDEX_USAGE`                                   | `CLUSTER_TIDB_INDEX_USAGE`                              |
| ---------------- | ---------------------------------------------------- | ------------------------------------------------------- |
| Scope            | Tracks index usage within a single database instance.         | Aggregates index usage across the entire TiDB cluster.   |
| Index tracking   | Data is local to each database instance.                      | Provides a centralized cluster-wide view.               |
| Primary use case | Debugs index usage at the database instance level.    | Analyzes global index patterns and multi-node behavior.  |

### Use `CLUSTER_TIDB_INDEX_USAGE` effectively

Because the `CLUSTER_TIDB_INDEX_USAGE` system table consolidates data from multiple nodes, consider the following:

- Delayed data updates

    To minimize performance impact, `CLUSTER_TIDB_INDEX_USAGE` does not update instantly. Index usage metrics might be delayed by up to 5 minutes. Keep this latency in mind when you analyze queries.

- Memory-based storage

    Like `TIDB_INDEX_USAGE`, this system table does not persist data across node restarts. If a node goes down, its recorded index usage data will be lost.

By using `CLUSTER_TIDB_INDEX_USAGE`, you can gain a global perspective on index behavior, ensuring indexing strategies are aligned with distributed query workloads.

## Identify unused indexes using `schema_unused_indexes`

Manually analyzing index usage data can be time-consuming. To simplify this process, TiDB provides [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md), a system view that lists indexes that have not been used since the database is last restarted.

This provides a quick way for you to do the following:

- Identify indexes that are no longer in use, reducing unnecessary storage costs.
- Speed up DML operations by eliminating indexes that add overhead to `INSERT`, `UPDATE`, and `DELETE` queries.
- Streamline index audits without needing to manually analyze query patterns.

By using `schema_unused_indexes`, you can quickly identify unnecessary indexes and reduce database overhead with minimal effort.

### How `schema_unused_indexes` works

The `schema_unused_indexes` view is derived from `TIDB_INDEX_USAGE`, meaning it automatically filters out indexes that have recorded zero query activity since the last TiDB restart.

To retrieve a list of unused indexes, run the following SQL statement:

```sql
SELECT * FROM sys.schema_unused_indexes;
```

A result similar to the following is returned:

```
+-----------------+---------------+--------------------+
| object_schema   | object_name   | index_name         |
+---------------- + ------------- + -------------------+
| bookshop        | users         | nickname           |
| bookshop        | ratings       | uniq_book_user_idx |
+---------------- + ------------- + -------------------+
```

### Considerations when using `schema_unused_indexes`

Take the following points into consideration when you use `schema_unused_indexes`.

#### Indexes are considered unused only since the last restart

- If a TiDB node restarts, the usage tracking data is reset.
- Ensure the system has been running long enough to capture a representative workload before relying on this data.

#### Not all unused indexes can be dropped immediately

Some indexes might be rarely used but still essential for specific queries, batch jobs, or reporting tasks. Before dropping an index, consider whether it supports the following:

- Rare but essential queries, for example, monthly reports, analytics
- Batch processing jobs that do not run daily
- Ad-hoc troubleshooting queries

If the index appears in important but infrequent queries, it is recommended to keep it or make it invisible first.

You can use [invisible indexes](#safely-test-index-removal-using-invisible-indexes) to safely test whether an index can be removed without impacting performance.

### Manually create the `schema_unused_indexes` view

For clusters upgraded from an earlier version to TiDB v8.0.0 or later, you must manually create the system schema and the included views.

For more information, see [Manually create the `schema_unused_indexes` view](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view).

## Safely test index removal using invisible indexes

Removing an index without proper validation can lead to unexpected performance issues, especially if the index is infrequently used but still critical for certain queries.

To mitigate this risk, TiDB provides invisible indexes, allowing you to temporarily disable an index without deleting it. By using invisible indexes, you can safely validate index removal decisions, ensuring a more controlled and predictable database optimization process.

### What are invisible indexes?

An invisible index remains in the database but is ignored by the TiDB optimizer. You can use [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md) to make an index invisible to test whether the index is truly unnecessary without permanently removing it.

Key benefits of invisible indexes are as follows:

- **Safe index testing**: queries will no longer use the index, but the related optimizer statistics are still maintained. You can quickly restore it at any time if needed.
- **Zero disruption to index storage**: the index remains intact, ensuring no need for costly re-creation.
- **Performance monitoring**: as a DBA, you can observe query behavior without the index before making a final decision.

### Make an index invisible

To make an index invisible without dropping it, run a SQL statement similar to the following:

```sql
ALTER TABLE bookshop.users ALTER INDEX nickname INVISIBLE;
```

After making the index invisible, observe the system's query performance:

- If performance remains unchanged, the index is likely unnecessary and can be safely removed.
- If query latency increases, the index might still be needed.

### Use invisible indexes effectively

- **Test during off-peak hours**: monitor performance impact in a controlled environment.
- **Use query monitoring tools**: analyze query execution plans before and after marking an index invisible.
- **Confirm over multiple workloads**: ensure that the index is not needed for specific reports or scheduled queries.

### How long can an index remain invisible?

- OLTP workloads: monitor for at least one week to account for daily variations.
- Batch processing or ETL workloads: allow one full reporting cycle, for example, a monthly financial report.
- Ad-hoc analytical queries: use query logs to confirm that the index is not needed before dropping it.

For safety, keep the index invisible for at least one full business cycle to ensure all workloads have been tested before making a final decision.

## Top five best practices for index optimization

To maintain high performance and efficient resource usage, regular index optimization is part of database maintenance. The following are the best practices for managing indexes effectively in TiDB:

1. **Monitor index usage regularly.**

    - Use [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) and [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) to track index usage activity.
    - Identify unused indexes using [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md), and evaluate whether they can be removed.
    - Monitor query execution plans to detect inefficient indexes that might cause excessive I/O.

2. **Validate before removing indexes.**

    - Use [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md) to make an index invisible to temporarily disable an index, and observe the impact before permanent deletion.
    - If query performance remains stable, proceed with index removal.
    - Ensure a sufficient observation period to account for all query patterns before making a final decision.

3. **Optimize existing indexes.**

    - Consolidating redundant indexes can reduce storage overhead and improve write performance. If multiple indexes serve similar queries, they might be candidates for merging into a single, more efficient index.

        - To find indexes with overlapping prefixes (which might indicate redundancy), run the following SQL statement:

            ```sql
            SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_NAME = 'your_table'
            ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, SEQ_IN_INDEX;
            ```

        - If two indexes have the same leading columns, consider merging them into a composite index instead.

    - Improve selectivity. Low-selectivity indexes (those filtering too many rows) can be optimized as follows:

        - Adding additional columns to improve filtering efficiency.
        - Changing index structure (for example, prefix indexes, composite indexes).

    - Analyze index selectivity. Use `PERCENTAGE_ACCESS_*` fields in `TIDB_INDEX_USAGE` to evaluate how well an index filters data.

4. **Be mindful of DML performance impact.**

    - Avoid excessive indexing. Each additional index increases overhead on `INSERT`, `UPDATE`, and `DELETE` operations.
    - Index only what is necessary for queries to minimize the maintenance cost on write-heavy workloads.

5. **Test and tune regularly.**

    - Perform index audits periodically, especially after significant workload changes.
    - Use TiDB's execution plan analysis tools to verify whether indexes are being used optimally.
    - When adding new indexes, test them in an isolated environment first to prevent unexpected regressions.

By following these best practices, you can ensure efficient query execution, reduce unnecessary storage overhead, and maintain optimal database performance.

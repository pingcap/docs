---
title: Index Best Practices
summary: This document summarizes best practices for using indexes in TiDB.
---

# Index Best Practices

Indexes are essential for optimizing database query performance, reducing the need to scan large amounts of data. However, as applications evolve, business logic changes, and data volume grows, indexing inefficiencies emerge, including the following:

- Unused indexes: these indexes are once relevant but are no longer selected by the query optimizer, consuming storage and adding unnecessary overhead to write operations.
- Inefficient indexes: some indexes are used by the optimizer but scan more data than expected, increasing disk I/O and slowing down query performance.

If left unaddressed, these indexing issues can cause higher storage costs, degraded performance, and operational inefficiencies. In a distributed SQL database like TiDB, indexing inefficiencies have an even greater impact due to the scale of distributed queries and the complexity of multi-node coordination. That is why regular index audits are crucial for maintaining an optimized database. 

Proactively identifying and optimizing indexes helps:

- Reduce storage overhead: removing unused indexes frees up disk space and reduces long-term storage costs.
- Improve write performance: write-heavy workloads (such as `INSERT`, `UPDATE`, and `DELETE`) perform better when unnecessary index maintenance is eliminated.
- Optimize query execution: efficient indexes reduce the number of rows scanned, improving query speed and response times.
- Streamline database management: fewer and well-optimized indexes simplify backups, recovery, and schema changes.

TiDB v8.0.0 introduces the [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) table and a view [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) to help DBAs and developers track index usage patterns and make data-driven decisions. This document explores the tools needed to detect and eliminate unused or inefficient indexes, improving TiDB's performance and stability.

## Making index optimization a habit

Because indexes evolve with changing business logic, regular index audits should be a standard part of database maintenance. TiDB provides built-in observability tools to help users detect, evaluate, and optimize indexes without risk.

The next section describes how `TIDB_INDEX_USAGE` and `schema_unused_indexes` help DBAs efficiently track and optimize indexes.

## TiDB index optimization: a data-driven approach

Indexes are essential for query performance, but removing them without proper analysis can lead to unexpected regressions or even system instability. To ensure safe and effective index management, TiDB provides built-in observability tools that allow you to:

- Track index usage in real-time: identify how often an index is accessed and whether it contributes to performance improvements.
- Detect unused indexes: locate indexes that have not been used since the database is last restarted.
- Assess index efficiency: evaluate whether an index filters data effectively or causes excessive I/O overhead.
- Safely test index removal: temporarily make an index invisible before deleting it to ensure no queries depend on it.

TiDB simplifies index optimization by introducing the following powerful tools:

- `TIDB_INDEX_USAGE`: monitors index usage patterns and query frequency.
- `schema_unused_indexes`: lists indexes that have not been used since the database is last restarted.
- Invisible indexes: allows you to test the impact of removing an index before permanently deleting it.

By using these observability tools, you can confidently clean up redundant indexes without risking performance degradation.

## Track index usage with `TIDB_INDEX_USAGE`

Introduced in [TiDB v8.0.0](/releases/release-8.0.0.md), the `TIDB_INDEX_USAGE` system table provides real-time insights into how indexes are used, helping you optimize query performance and remove unnecessary indexes.

This system table enables you to:

- Detect unused indexes: identify indexes that have not been accessed by queries, helping determine which ones can be safely removed.
- Analyze index efficiency: track how frequently an index is used and whether it contributes to efficient query execution.
- Evaluate query patterns: understand how indexes affect read operations, data scans, and key-value (KV) requests.

Starting from [TiDB v8.4.0](/releases/release-8.4.0.md), the table also includes primary keys in clustered tables, offering deeper visibility into index performance.

### Key metrics in `TIDB_INDEX_USAGE`

Run the following SQL statement to check the fields in `TIDB_INDEX_USAGE`:

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

The columns in the `TIDB_INDEX_USAGE` table are as follows:

* `TABLE_SCHEMA`: The name of the database to which the table containing the index belongs.
* `TABLE_NAME`: The name of the table containing the index.
* `INDEX_NAME`: The name of the index.
* `QUERY_TOTAL`: The total number of statements accessing the index.
* `KV_REQ_TOTAL`: The total number of KV requests generated when accessing the index.
* `ROWS_ACCESS_TOTAL`: The total number of rows scanned when accessing the index.
* `PERCENTAGE_ACCESS_0`: The number of times the row access ratio (the percentage of accessed rows out of the total number of rows in the table) is 0.
* `PERCENTAGE_ACCESS_0_1`: The number of times the row access ratio is between 0% and 1%.
* `PERCENTAGE_ACCESS_1_10`: The number of times the row access ratio is between 1% and 10%.
* `PERCENTAGE_ACCESS_10_20`: The number of times the row access ratio is between 10% and 20%.
* `PERCENTAGE_ACCESS_20_50`: The number of times the row access ratio is between 20% and 50%.
* `PERCENTAGE_ACCESS_50_100`: The number of times the row access ratio is between 50% and 100%.
* `PERCENTAGE_ACCESS_100`: The number of times the row access ratio is 100%.
* `LAST_ACCESS_TIME`: The time of the most recent access to the index.

### Identify unused and inefficient indexes using `TIDB_INDEX_USAGE`

Identify unused and inefficient indexes using `TIDB_INDEX_USAGE as follows:

- Unused indexes:

    - If `QUERY_TOTAL = 0`, the index has not been used by any queries.
    - If `LAST_ACCESS_TIME` is a long time ago, the index might no longer be relevant.

- Inefficient Indexes:

    - High values in `PERCENTAGE_ACCESS_100` suggest full index scans, which might indicate an inefficient index.
    - Comparing `ROWS_ACCESS_TOTAL / QUERY_TOTAL` helps determine whether the index scans too many rows relative to its usage.

By leveraging `TIDB_INDEX_USAGE`, you can gain detailed insights into index performance, making it easier to remove unnecessary indexes and optimize query execution.

### Handle index usage data efficiently

#### Delayed data updates

To minimize performance impact, `TIDB_INDEX_USAGE` does not update instantly. Index usage metrics might be delayed by up to 5 minutes, so you should account for this when analyzing queries.

#### Index usage data is not persisted

`TIDB_INDEX_USAGE` stores data in memory, meaning it does not persist across node restarts.

If a TiDB node is restarted, all index usage statistics from that node will be cleared.

#### Planned enhancements for historical tracking

TiDB is developing a Workload Repository to periodically take snapshots for index usage data, allowing you to review trends over time instead of relying only on real-time metrics.

Before this feature is available, you can periodically export index usage snapshots using the following:

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEX_USAGE INTO OUTFILE '/backup/index_usage_snapshot.csv';
```

This allows for historical tracking by comparing snapshots over time to detect trends in index usage and make more informed pruning decisions.

## Consolidate index usage data across TiDB nodes

Because TiDB is a distributed SQL database, query workloads are spread across multiple nodes. Each TiDB node tracks its own local index usage, but for a global view of index performance, TiDB provides the [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) system table.

This view consolidates index usage data from all TiDB nodes, ensuring that distributed query workloads are fully accounted for when optimizing indexing strategies.

Unlike `TIDB_INDEX_USAGE`, which provides insights at the node level, this cluster-wide view allows you to:

- Detect inconsistencies in index usage. For example, an index might be frequently used on some nodes but unused on others.
- Analyze global index patterns for distributed queries, ensuring indexing decisions reflect real-world workload distribution.
- Optimize indexing strategies across all nodes, improving query efficiency for multi-node deployments.

Different TiDB nodes may experience different query workloads, so an index that appears unused on some nodes may still be critical elsewhere. To segment index analysis by workload, run:

```sql
SELECT INSTANCE, TABLE_NAME, INDEX_NAME, SUM(QUERY_TOTAL) AS total_queries
FROM INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE
GROUP BY INSTANCE, TABLE_NAME, INDEX_NAME
ORDER BY total_queries DESC;
```

This helps determine whether an index is truly unused across all nodes or only for specific instances, allowing DBAs to make informed decisions on index removal.

### Key differences between `TIDB_INDEX_USAGE` and `CLUSTER_TIDB_INDEX_USAGE`

The following tables show the key differences between `TIDB_INDEX_USAGE` and `CLUSTER_TIDB_INDEX_USAGE`.

| Feature | `TIDB_INDEX_USAGE` | `CLUSTER_TIDB_INDEX_USAGE` |
| ------- | ------------------ | -------------------------- |
| Scope   | Tracks index usage within a single database                   | Aggregates index usage across the entire TiDB cluster   |
| Index Tracking   | Data is local to each database                       | Centralized cluster-wide view                           |
| Primary Use Case | Debugging index usage at the database instance level | Analyzing global index patterns and multi-node behavior |

### Using `CLUSTER_TIDB_INDEX_USAGE` effectively

Since this system table consolidates data from multiple nodes, consider the following:

- Delayed data updates

    The data is refreshed periodically to minimize performance impact. If index usage is analyzed immediately after a query execution, allow time for metrics to update.

- Memory-based storage

    Like `TIDB_INDEX_USAGE`, this system table does not persist data across node restarts. If a node goes down, its recorded index usage data will be lost.

-  Future enhancements for historical tracking

    TiDB is introducing a Workload Repository that will periodically snapshot index usage metrics, allowing you to analyze trends over time instead of relying solely on real-time data.

By leveraging `CLUSTER_TIDB_INDEX_USAGE`, you can gain a global perspective on index behavior, ensuring indexing strategies are aligned with distributed query workloads.

## Identify unused indexes with `schema_unused_indexes`

Manually analyzing index usage data can be time-consuming. To simplify this process, TiDB provides `schema_unused_indexes`, a system view that lists indexes that have not been used since the database is last restarted.

This provides a quick way for you to:

- Identify indexes that are no longer in use, reducing unnecessary storage costs.
- Speed up DML operations by eliminating indexes that add overhead to `INSERT`, `UPDATE`, and `DELETE` queries.
- Streamline index audits without needing to manually analyze query patterns.

### How `schema_unused_indexes` works

The `schema_unused_indexes` view is derived from `TIDB_INDEX_USAGE`, meaning it automatically filters out indexes that have recorded zero query activity since the last TiDB restart.

To retrieve a list of unused indexes, run the following SQL statement:

```sql
SELECT * FROM sys.schema_unused_indexes;
```

A result similar to the following is returned:

```
+-----------------+---------------+--------------------+
| `object_schema` | `object_name` | `index_name`       |
+---------------- + ------------- + -------------------+
| bookshop        | users         | nickname           |
| bookshop        | ratings       | uniq_book_user_idx |
+---------------- + ------------- + -------------------+
```

### Considerations when using `schema_unused_indexes`

#### Indexes are considered unused only since the last restart

- If a TiDB node restarts, the usage tracking data is reset.

- Ensure the system has been running long enough to capture a representative workload before relying on this data.

#### Not all unused indexes should be dropped immediately

Some indexes might be rarely used but still essential for specific queries, batch jobs, or reporting tasks. Before dropping an index, consider whether it supports the following:

- Rare but essential queries, for example, monthly reports, analytics
- Batch processing jobs that do not run daily
- Ad-hoc troubleshooting queries

If the index appears in important but infrequent queries, it is recommended to keep it or make it invisible first.

Use [invisible indexes](#safely-test-index-removal-with-invisible-indexes) to safely test whether an index can be removed without impacting performance.

By leveraging `schema_unused_indexes`, you can quickly identify unnecessary indexes and reduce database overhead with minimal effort.

### Manually create the `schema_unused_indexes` view

Because `TIDB_INDEX_USAGE` is cleared after a TiDB node restarts, ensure that the node has been running for a sufficient amount of time before making decisions.

For clusters upgraded from an earlier version to TiDB v8.0.0 or later, you must manually create the system schema and the included views. 

For more information, see [Manually create the `schema_unused_indexes` view](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view). 

## Safely test index removal with invisible indexes

Removing an index without proper validation can lead to unexpected performance issues, especially if the index is infrequently used but still critical for certain queries. To mitigate this risk, TiDB provides invisible indexes, allowing you to temporarily disable an index without deleting it.

### What are invisible indexes?

An invisible index remains in the database but is ignored by the TiDB optimizer. This allows you to test whether an index is truly unnecessary without permanently removing it.

Key benefits include:

- **Safe index testing**. Queries will no longer use the index, but it can be quickly restored if needed.
- **Zero disruption to index storage**. The index remains intact, ensuring no need for costly re-creation.
- **Performance monitoring**. As a DBA, you can observe query behavior without the index before making a final decision.

### Use invisible indexes in TiDB

To make an index invisible (without dropping it), use:

```sql
ALTER TABLE bookshop.users ALTER INDEX nickname INVISIBLE;
```

### Monitor query performance

After making the index invisible, observe the system's query performance:

- If performance remains unchanged, the index is likely unnecessary and can be safely removed.
- If query latency increases, the index might still be needed, and removal should be reconsidered.

### Best practices for using invisible indexes

- Test during off-peak hours – monitor performance impact in a controlled environment.
- Use query monitoring tools – analyze query execution plans before and after marking an index as invisible.
- Confirm over multiple workloads – ensure that the index is not needed for specific reports or scheduled queries.

By leveraging invisible indexes, you can validate index removal decisions without risk, ensuring a more controlled and predictable database optimization process.

### How long should an index remain invisible?

- OLTP workloads: monitor for at least one week to account for daily variations.
- Batch processing/ETL workloads: allow one full reporting cycle (for example, a monthly financial report run).
- Ad-hoc analytical queries: use query logs to confirm the index is not needed before dropping it.

For safety, keep the index invisible for at least one full business cycle to ensure all workloads have been tested before making a final decision.

## Summary and key takeaways

Effective index management is crucial for maintaining database performance in TiDB. By leveraging TiDB's built-in observability tools, you can easily identify, evaluate, and optimize indexes without risking system stability.

By following the following best practices, you can keep your databases optimized, reduce unnecessary resource consumption, and maintain peak query performance.

- Monitor index usage regularly

    - Use `TIDB_INDEX_USAGE` to track index query activity.
    - Use `CLUSTER_TIDB_INDEX_USAGE` for a cluster-wide view of index behavior.

- Identify Unused Indexes with Confidence

    - Use `schema_unused_indexes` to list indexes that have not been used since the last restart.
    - Be cautious—some indexes might be used infrequently but remain critical for specific queries.

- Safely test index removal with invisible indexes

    - Mark an index as `INVISIBLE` before dropping it to validate its necessity.
    - Restore visibility if query performance is negatively affected.

- Optimize indexes to reduce overhead

    - Avoid redundant or low-selectivity indexes that consume storage and slow down write operations.
    - Optimize index structures to improve query filtering efficiency.

- Prioritize ongoing index maintenance

    - Regularly audit indexes after schema changes, application updates, or workload shifts.
    - Use TiDB's execution plan analysis tools to ensure indexes are used effectively.

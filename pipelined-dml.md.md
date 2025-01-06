---
title: Pipelined DML
summary: Introduces the use cases, methods, limitations, and FAQs of Pipelined DML. Pipelined DML enhances TiDB's batch processing capabilities, allowing transaction sizes to bypass TiDB's memory limits.
---

# Pipelined DML

> **Warning:**
>
> Pipelined DML is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

This document introduces the use cases, methods, limitations, and common issues related to Pipelined DML.

## Overview

Pipelined DML is an experimental feature introduced in TiDB v8.0.0 to improve the performance of large-scale data write operations. When this feature is enabled, TiDB streams data directly to the storage layer during DML operations, instead of buffering it entirely in memory. This pipeline-like approach simultaneously reads data (input) and writes it to the storage layer (output), effectively resolving common challenges in large-scale DML operations as follows:

- Memory limits: traditional DML operations might encounter out-of-memory (OOM) errors when handling large datasets.
- Performance bottlenecks: large transactions are often inefficient and is prone to causing workload fluctuations.

With pipelined DML enabled, you can achieve the following:

- Perform large-scale data operations without being constrained by TiDB memory limits.
- Maintain smoother workload and lower operation latency.
- Keep transaction memory usage predictable, typically within 1 GiB.

It is recommended to enable Pipelined DML in the following scenarios:

- Processing data writes involving millions of rows or more
- Encountering memory insufficient errors during DML operations
- Experiencing noticeable workload fluctuations during large-scale data operations

Note that although Pipelined DML significantly reduces memory usage during transaction processing, you still need to configure a [reasonable memory threshold](/system-variables.md#tidb_mem_quota_query) (at least 2 GiB recommended) to ensure other components (such as executors) function properly during large-scale data operations.

## Limitations

Currently, Pipelined DML has the following limitations:

- Pipelined DML is currently incompatible with TiCDC, TiFlash, or BR. Avoid using Pipelined DML on tables associated with these components, as it might lead to issues such as blocking or OOM in these components.
- Pipelined DML is not suitable for scenarios with write conflicts, because it might lead to significant performance degradation or operation failures that require rollback.
- Make sure that the [metadata lock](/metadata-lock.md) is enabled during Pipelined DML operations.
- When executing DML statements with Pipelined DML enabled, TiDB checks the following conditions. If any condition is not met, TiDB falls back to standard DML execution and generates a warning:
    - Only [autocommit](/transaction-overview.md#autocommit) statements are supported.
    - Only `INSERT`, `UPDATE`, `REPLACE`, and `DELETE` statements are supported.
    - Target tables must not include [temporary tables](/temporary-tables.md) or [cached tables](/cached-tables.md).
    - When [foreign key constraints](/foreign-key.md) are enabled (`foreign_key_checks = ON`), target tables must not include foreign key relationships.
- When executing `INSERT IGNORE ... ON DUPLICATE KEY UPDATE` statements, conflicting updates might result in `Duplicate entry` errors.

## Usage

This section describes how to enable Pipelined DML and verify whether it takes effect.

### Enable Pipelined DML

You can enable Pipelined DML in one of the following methods:

- To enable Pipelined DML for the current session, set the [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) variable to `"bulk"`:

    ```sql
    SET tidb_dml_type = "bulk";
    ```

- To enable Pipelined DML for a specific statement, add the [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint in the statement.

    - Data archiving example:

        ```sql
        INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO target_table SELECT * FROM source_table;
        ```

    - Bulk data update example:

        ```sql
        UPDATE /*+ SET_VAR(tidb_dml_type='bulk') */ products
        SET price = price * 1.1
        WHERE category = 'electronics';
        ```

    - Bulk deletion example:

        ```sql
        DELETE /*+ SET_VAR(tidb_dml_type='bulk') */ FROM logs WHERE log_time < '2023-01-01';
        ```

### Verify Pipelined DML

After executing a DML statement, you can verify whether Pipelined DML is used for the statement execution by checking the [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-new-in-v409) variable:

```sql
SELECT @@tidb_last_txn_info;
```

If the `pipelined` field in the output is `true`, it indicates that Pipelined DML is successfully used.

## Best practices

- Increase the value of [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) slightly to ensure that memory usage for components such as executors does not exceed the limit. A value of at least 2 GiB is recommended. For environments with sufficient TiDB memory, you can increase this value further.
- In scenarios where data is inserted into new tables, the performance of Pipelined DML might be affected by hotspots. To achieve optimal performance, it is recommended to address hotspots in advance. For more information, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

## Related configurations

- The [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) system variable controls whether Pipelined DML is enabled at the session level.
- When [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) is set to `"bulk"`, the [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) configuration item behaves as if it is set to `false`.
- Transactions executed using Pipelined DML are not subject to the size limit specified by the TiDB configuration item [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit).
- For large transactions executed using Pipelined DML, transaction duration might increase. In such cases, the maximum TTL for the transaction lock is the larger value of [`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl) or 24 hours.
- If the execution time of a transaction exceeds the value set by [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610), garbage collection (GC) might force the transaction to roll back, causing it to fail.

## Monitor Pipelined DML

You can monitor the execution of Pipelined DML using the following methods:

- Check the [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-new-in-v409) system variable to get information about the last transaction executed in the current session, including whether Pipelined DML was used.
- Look for lines containing `"[pipelined dml]"` in TiDB logs to understand the execution process and progress of Pipelined DML, including the current stage and the amount of data written.
- View the `affected rows` field in the [`expensive query`](/identify-expensive-queries.md#expensive-query-log-example) logs to track the progress of long-running statements.
- Query the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table to view transaction execution progress. Pipelined DML is typically used for large transactions, so you can use this table to monitor their execution progress.

## FAQs

### Why wasn't my query executed using Pipelined DML?

When TiDB rejects to execute a statement using Pipelined DML, it generates a warning message accordingly. You can execute `SHOW WARNINGS;` to check the warning and identify the cause.

Common reasons:

- The DML statement is not autocommited.
- The statement involves unsupported table types, such as [temporary tables](/temporary-tables.md) or [cached tables](/cached-tables.md).
- The operation involves foreign keys, and foreign key checks are enabled.

### Does Pipelined DML affect the isolation level of transactions?

No. Pipelined DML only changes the data-writing mechanism during transactions and does not affect isolation guarantees of TiDB transactions.

### Why do I still encounter out-of-memory (OOM) errors after enabling Pipelined DML?

Even with Pipelined DML enabled, you might still encounter query termination caused by memory limit issues:

```
The query has been canceled due to exceeding the memory limit allowed for a single SQL query. Please try to narrow the query scope or increase the tidb_mem_quota_query limit, and then try again.
```

This error occurs because Pipelined DML only controls the memory usage by data during transaction execution. However, the total memory consumed during statement execution also includes memory used by other components, such as executors. If the total memory required exceeds TiDB memory limit, out-of-memory (OOM) errors might still occur.

In most cases, you can increase the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) to a higher value to resolve this issue. A value of at least 2 GiB is recommended. For SQL statements with complex operators or involving large datasets, you might need to increase this value further.

## Learn More

- [Batch Processing](/batch-processing.md)
- [TiDB Memory Control](/configure-memory-usage.md)
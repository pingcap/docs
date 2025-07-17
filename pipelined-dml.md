---
title: Pipelined DML
summary: 介绍 Pipelined DML 的使用场景、方法、限制以及常见问题。Pipelined DML 提升了 TiDB 的批量处理能力，允许事务大小绕过 TiDB 的内存限制。
---

# Pipelined DML

> **Warning:**
>
> Pipelined DML 是一个实验性功能。不建议在生产环境中使用此功能。该功能可能在未通知的情况下被更改或移除。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

本文档介绍了与 Pipelined DML 相关的使用场景、方法、限制以及常见问题。

## 概述

Pipelined DML 是在 TiDB v8.0.0 中引入的一个实验性功能，旨在提升大规模数据写入操作的性能。当启用此功能时，TiDB 在执行 DML 操作时会将数据直接流式传输到存储层，而不是全部缓存在内存中。这种类似流水线的方式在读取数据（输入）和写入存储层（输出）时同时进行，有效解决了以下常见的在大规模 DML 操作中遇到的问题：

- 内存限制：传统的 DML 操作在处理大数据集时可能会遇到内存溢出（OOM）错误。
- 性能瓶颈：大事务通常效率较低，容易引起工作负载波动。

启用 pipelined DML 后，你可以实现：

- 执行大规模数据操作而不受 TiDB 内存限制的约束。
- 保持工作负载的平稳，降低操作延迟。
- 使事务的内存使用保持可控，通常在 1 GiB 以内。

建议在以下场景中启用 Pipelined DML：

- 处理涉及数百万行或更多的数据写入。
- 在 DML 操作中遇到内存不足的错误。
- 在大规模数据操作中出现明显的工作负载波动。

注意，虽然 Pipelined DML 在事务处理过程中显著降低了内存使用，但你仍需配置一个[合理的内存阈值](/system-variables.md#tidb_mem_quota_query)（建议至少 2 GiB），以确保其他组件（如执行器）在大规模数据操作期间正常运行。

## 限制

目前，Pipelined DML 存在以下限制：

- Pipelined DML 目前与 TiCDC、TiFlash 或 BR 不兼容。避免在与这些组件相关的表上使用 Pipelined DML，否则可能导致这些组件出现阻塞或 OOM 等问题。
- Pipelined DML 不适用于存在写冲突的场景，因为可能导致性能大幅下降或操作失败需要回滚。
- 在进行 Pipelined DML 操作时，确保启用了[元数据锁](/metadata-lock.md)。
- 在启用 Pipelined DML 执行 DML 语句时，TiDB 会检查以下条件。如果任何条件不满足，TiDB 会回退到标准 DML 执行，并生成警告：
    - 仅支持 [autocommit](/transaction-overview.md#autocommit) 语句。
    - 仅支持 `INSERT`、`UPDATE`、`REPLACE` 和 `DELETE` 语句。
    - 目标表不能包含 [临时表](/temporary-tables.md) 或 [缓存表](/cached-tables.md)。
    - 当启用 [外键约束](/foreign-key.md)（`foreign_key_checks = ON`）时，目标表不能包含外键关系。
- 执行 `INSERT IGNORE ... ON DUPLICATE KEY UPDATE` 语句时，冲突的更新可能导致 `Duplicate entry` 错误。

## 使用方法

本节介绍如何启用 Pipelined DML 以及如何验证其是否生效。

### 启用 Pipelined DML

你可以通过以下方法之一启用 Pipelined DML：

- 为当前会话启用 Pipelined DML，将 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) 变量设置为 `"bulk"`：

    ```sql
    SET tidb_dml_type = "bulk";
    ```

- 在特定语句中启用 Pipelined DML，添加 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) 提示。

    - 数据归档示例：

        ```sql
        INSERT /*+ SET_VAR(tidb_dml_type='bulk') */ INTO target_table SELECT * FROM source_table;
        ```

    - 批量数据更新示例：

        ```sql
        UPDATE /*+ SET_VAR(tidb_dml_type='bulk') */ products
        SET price = price * 1.1
        WHERE category = 'electronics';
        ```

    - 批量删除示例：

        ```sql
        DELETE /*+ SET_VAR(tidb_dml_type='bulk') */ FROM logs WHERE log_time < '2023-01-01';
        ```

### 验证 Pipelined DML

在执行完 DML 语句后，可以通过检查 [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-new-in-v409) 变量，验证是否启用了 Pipelined DML：

```sql
SELECT @@tidb_last_txn_info;
```

如果输出中的 `pipelined` 字段为 `true`，表示成功使用 Pipelined DML。

## 最佳实践

- 略微增加 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 的值，以确保执行器等组件的内存使用不会超过限制。建议至少设置为 2 GiB。对于内存充足的环境，可以进一步提高此值。
- 在向新表插入数据的场景中，Pipelined DML 的性能可能会受到热点的影响。为了获得最佳性能，建议提前解决热点问题。更多信息请参见 [Troubleshoot Hotspot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)。

## 相关配置

<CustomContent platform="tidb">

- [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) 系统变量控制是否在会话层启用 Pipelined DML。
- 当 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) 设置为 `"bulk"` 时， [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600) 配置项表现为被设置为 `false`。
- 使用 Pipelined DML 执行的事务不受 TiDB 配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 指定的大小限制。
- 对于使用 Pipelined DML 执行的大事务，事务持续时间可能会增加。在这种情况下，事务锁的最大 TTL 为 [`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl) 和 24 小时中的较大值。
- 如果事务的执行时间超过 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610) 设置的值，垃圾回收（GC）可能会强制回滚事务，导致事务失败。

</CustomContent>

<CustomContent platform="tidb-cloud">

- [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) 系统变量控制是否在会话层启用 Pipelined DML。
- 当 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) 设置为 `"bulk"` 时， [`pessimistic-auto-commit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#pessimistic-auto-commit-new-in-v600) 配置项表现为被设置为 `false`。
- 使用 Pipelined DML 执行的事务不受 TiDB 配置项 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 指定的大小限制。
- 对于使用 Pipelined DML 执行的大事务，事务持续时间可能会增加。在这种情况下，事务锁的最大 TTL 为 [`max-txn-ttl`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#max-txn-ttl) 和 24 小时中的较大值。
- 如果事务的执行时间超过 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610) 设置的值，垃圾回收（GC）可能会强制回滚事务，导致事务失败。

</CustomContent>

## 监控 Pipelined DML

你可以通过以下方法监控 Pipelined DML 的执行情况：

- 查看 [`tidb_last_txn_info`](/system-variables.md#tidb_last_txn_info-new-in-v409) 系统变量，获取当前会话中最后一次事务的相关信息，包括是否使用了 Pipelined DML。
- 在 TiDB 日志中查找包含 `"[pipelined dml]"` 的行，以了解 Pipelined DML 的执行过程和进展，包括当前阶段和写入的数据量。
- 查看 [`expensive query`](https://docs.pingcap.com/tidb/stable/identify-expensive-queries#expensive-query-log-example) 日志中的 `affected rows` 字段，以跟踪长时间运行语句的进展。
- 查询 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表，查看事务执行进度。Pipelined DML 通常用于大事务，可以通过此表监控其执行情况。

## 常见问题解答

### 为什么我的查询没有使用 Pipelined DML 执行？

当 TiDB 拒绝使用 Pipelined DML 执行语句时，会生成相应的警告信息。你可以执行 `SHOW WARNINGS;` 来查看警告内容并确认原因。

常见原因：

- DML 语句未自动提交。
- 语句涉及不支持的表类型，例如 [临时表](/temporary-tables.md) 或 [缓存表](/cached-tables.md)。
- 操作涉及外键，并且启用了外键检查。

### Pipelined DML 会影响事务的隔离级别吗？

不会。Pipelined DML 只会改变事务中的数据写入机制，不会影响 TiDB 事务的隔离保证。

### 为什么启用 Pipelined DML 后仍然遇到内存溢出（OOM）错误？

即使启用了 Pipelined DML，你仍可能遇到因内存限制导致的查询终止：

```
The query has been canceled due to exceeding the memory limit allowed for a single SQL query. Please try to narrow the query scope or increase the tidb_mem_quota_query limit, and then try again.
```

此错误发生的原因是 Pipelined DML 仅控制事务执行期间数据的内存使用。而在语句执行过程中，其他组件（如执行器）也会占用内存。如果总的内存需求超过了 TiDB 的内存限制，就可能出现 OOM 错误。

在大多数情况下，你可以通过将系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 设置为更高的值来解决此问题。建议至少设置为 2 GiB。对于包含复杂操作符或涉及大数据集的 SQL 语句，可能需要进一步增加此值。

## 了解更多

<CustomContent platform="tidb">

- [Batch Processing](/batch-processing.md)
- [TiDB Memory Control](/configure-memory-usage.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Batch Processing](/batch-processing.md)
- [TiDB Memory Control](https://docs.pingcap.com/tidb/stable/configure-memory-usage)

</CustomContent>
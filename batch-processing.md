---
title: Batch Processing
summary: 介绍 TiDB 中的批处理功能，包括 Pipelined DML、非事务性 DML、`IMPORT INTO` 语句，以及已废弃的 batch-dml 特性。
---

# Batch Processing

批处理是在实际场景中常见且必不可少的操作。它能够高效处理大量数据集，用于数据迁移、批量导入、归档以及大规模更新等任务。

为了优化批处理操作的性能，TiDB 在其版本演进中引入了多项功能：

- 数据导入
    - `IMPORT INTO` 语句（在 TiDB v7.2.0 中引入，并在 v7.5.0 中正式发布）
- 数据插入、更新和删除
    - Pipelined DML（实验性功能，在 TiDB v8.0.0 中引入）
    - 非事务性 DML（在 TiDB v6.1.0 中引入）
    - batch-dml（已废弃）

本文档概述了这些功能的主要优势、限制和适用场景，帮助你选择最合适的方案以实现高效的批处理。

## 数据导入

`IMPORT INTO` 语句专为数据导入任务设计。它可以快速将 CSV、SQL 或 PARQUET 格式的数据导入到空的 TiDB 表中，无需单独部署 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)。

### 主要优势

- 极快的导入速度
- 相较于 TiDB Lightning 更加易用

### 限制

<CustomContent platform="tidb">

- 不提供事务性的 [ACID](/glossary.md#acid) 保证
- 受到多种使用限制

</CustomContent>

<CustomContent platform="tidb-cloud">

- 不提供事务性的 [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid) 保证
- 受到多种使用限制

</CustomContent>

### 适用场景

- 适用于数据迁移或恢复等数据导入场景。建议在适用情况下优先使用 `IMPORT INTO`，而非 TiDB Lightning。

更多信息请参见 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)。

## 数据插入、更新和删除

### Pipelined DML

Pipelined DML 是在 TiDB v8.0.0 中引入的实验性功能。在 v8.5.0 版本中，该功能得到了显著的性能提升。

#### 主要优势

- 在事务执行过程中将数据流式传输到存储层，而不是全部缓存在内存中，从而使事务大小不再受限于 TiDB 内存，支持超大规模数据处理
- 比标准 DML 实现更好的性能
- 可以通过系统变量启用，无需修改 SQL 语句

#### 限制

- 仅支持 [autocommit](/transaction-overview.md#autocommit) 的 `INSERT`、`REPLACE`、`UPDATE` 和 `DELETE` 语句。

#### 适用场景

- 适用于一般的批处理任务，如批量数据插入、更新和删除。

更多信息请参见 [Pipelined DML](/pipelined-dml.md)。

### 非事务性 DML 语句

非事务性 DML 在 TiDB v6.1.0 中引入。最初仅支持 `DELETE` 语句。从 v6.5.0 开始，`INSERT`、`REPLACE` 和 `UPDATE` 语句也支持此功能。

#### 主要优势

- 将单个 SQL 语句拆分为多个较小的语句，绕过内存限制
- 性能略优或与标准 DML 相当

#### 限制

- 仅支持 [autocommit](/transaction-overview.md#autocommit) 语句
- 需要修改 SQL 语句
- 对 SQL 语法有严格要求；部分语句可能需要重写
- 不具备完整的事务 ACID 保证；在失败时可能出现部分执行的情况

#### 适用场景

- 适用于批量数据插入、更新和删除的场景。鉴于其限制，建议在 Pipelined DML 不适用时考虑使用非事务性 DML。

更多信息请参见 [Non-transactional DML](/non-transactional-dml.md)。

### 已废弃的 batch-dml 特性

在 TiDB 4.0 之前的版本中提供的 batch-dml 功能现已废弃，不再推荐使用。该功能由以下系统变量控制：

- `tidb_batch_insert`
- `tidb_batch_delete`
- `tidb_batch_commit`
- `tidb_enable_batch_dml`
- `tidb_dml_batch_size`

由于可能导致数据和索引不一致而引发数据损坏或丢失的风险，这些变量已被废弃，计划在未来版本中移除。

**绝不建议** 在任何情况下使用已废弃的 batch-dml 功能。建议采用本文档中介绍的其他替代方案。
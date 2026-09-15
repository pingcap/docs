---
title: Fuse Engine 表
summary: "{{{ .lake }}} 使用 Fuse Engine 作为其默认存储引擎，提供类似 Git 的数据管理系统。"
---

# Fuse Engine 表

## 概述 {#overview}

{{{ .lake }}} 使用 Fuse Engine 作为其默认存储引擎，提供类似 Git 的数据管理系统，具备以下特性：

- **基于快照的架构**：可以查询和恢复任意时间点的数据，并保留数据变更历史以便恢复
- **高性能**：针对分析型负载进行了优化，支持自动索引和布隆过滤器
- **高效存储**：使用 Parquet 格式和高压缩率，以获得最佳存储效率
- **灵活配置**：支持自定义压缩、索引和存储选项
- **数据维护**：支持自动数据保留、快照管理和变更跟踪能力

## 何时使用 Fuse Engine {#when-to-use-fuse-engine}

适用于以下场景：

- **分析**：使用列式存储的 OLAP 查询
- **数据仓库**：大规模历史数据
- **时间旅行**：访问历史版本数据
- **云存储**：针对对象存储进行了优化

## 语法 {#syntax}

```sql
CREATE TABLE <table_name> (
  <column_definitions>
) [ENGINE = FUSE]
[CLUSTER BY (<expr> [, <expr>, ...] )]
[<Options>];
```

有关 `CREATE TABLE` 语法的更多详细信息，请参见 [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)。

## 参数 {#parameters}

以下是创建 Fuse Engine 表时的主要参数：

### `ENGINE` {#engine}

**说明：** 如果未显式指定引擎，{{{ .lake }}} 会默认使用 Fuse Engine 创建表，这等同于 `ENGINE = FUSE`。

### `CLUSTER BY` {#cluster-by}

**说明：** 指定由多个表达式组成的数据的排序方法。更多信息，请参见 [Cluster Key](/tidb-cloud-lake/sql/cluster-key.md)。

### `<Options>`

**说明：** Fuse Engine 提供了多种选项（不区分大小写），可用于自定义表属性。

- 详细信息请参见 [Fuse Engine 选项](#fuse-engine-options)。
- 多个选项之间使用空格分隔。
- 使用 [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#fuse-engine-options) 修改表选项。
- 使用 [SHOW CREATE TABLE](/tidb-cloud-lake/sql/show-create-table.md) 查看表选项。

## Fuse Engine 选项 {#fuse-engine-options}

以下是可用的 Fuse Engine 选项，按用途分组：

### `compression` {#compression}

- **语法：** `compression = '<compression>'`
- **说明：** 指定引擎的压缩方法。可选压缩方式包括 lz4、zstd、snappy 或 none。在对象存储中默认使用 zstd，在文件系统（fs）存储中默认使用 lz4。

### `snapshot_loc` {#snapshot-loc}

- **语法：** `snapshot_loc = '<snapshot_loc>'`
- **说明：** 以字符串格式指定位置参数，从而可以在不复制数据的情况下轻松共享表。

### `block_size_threshold` {#block-size-threshold}

- **语法：** `block_size_threshold = <n>`
- **说明：** 指定最大 block 大小（单位为字节）。默认值为 104,857,600 字节。

### `block_per_segment` {#block-per-segment}

- **语法：** `block_per_segment = <n>`
- **说明：** 指定一个 segment 中的最大 block 数量。默认值为 1,000。

### `row_per_block` {#row-per-block}

- **语法：** `row_per_block = <n>`
- **说明：** 指定一个文件中的最大行数。默认值为 1,000,000。

### `bloom_index_columns` {#bloom-index-columns}

- **语法：** `bloom_index_columns = '<column> [, <column> ...]'`
- **说明：** 指定用于 bloom index 的列。这些列的数据类型可以是 Map、Number、String、Date 或 Timestamp。如果未指定具体列，则默认会在所有受支持的列上创建 bloom index。`bloom_index_columns=''` 会禁用 bloom index。

### `bloom_index_type` {#bloom-index-type}

- **语法：** `bloom_index_type = 'xor8' | 'binary_fuse32'`
- **说明：** 指定 bloom index 使用的过滤算法。默认值为 `xor8`。对于点查负载较重的表，建议使用 `binary_fuse32`——它能提供更低的误判率，但代价是更大的索引大小（约为 `xor8` 的 4 倍）。

    请注意，`ALTER TABLE ... SET OPTIONS(bloom_index_type = ...)` 仅影响新写入的数据和重建后的 bloom index。现有的 `xor8` 索引文件和新的 `binary_fuse32` 索引文件可以在同一张表中共存。

    **示例：**

    ```sql
    -- Set bloom_index_type at table creation
    CREATE TABLE t (a INT) bloom_index_type = 'binary_fuse32';

    -- Change bloom_index_type for an existing table (affects new writes only)
    ALTER TABLE t SET OPTIONS(bloom_index_type = 'binary_fuse32');

    -- Revert to xor8
    ALTER TABLE t SET OPTIONS(bloom_index_type = 'xor8');
    ```

### `change_tracking` {#change-tracking}

- **语法：** `change_tracking = True / False`
- **说明：** 在 Fuse Engine 中将此选项设置为 `True` 后，可以为表跟踪变更。为表创建 stream 时，会自动将 `change_tracking` 设置为 `True`，并向表中引入额外的隐藏列作为变更跟踪元信息。更多信息，请参见 [Stream 工作原理](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md)。

### `data_retention_period_in_hours` {#data-retention-period-in-hours}

- **语法：** `data_retention_period_in_hours = <n>`
- **说明：** 指定表数据的保留小时数。最小值为 1 小时。最大值由 {{{ .lake }}} 服务配置决定；如果未指定，则默认值为 2,160 小时（90 天 x 24 小时）。

### `enable_auto_vacuum` {#enable-auto-vacuum}

- **语法：** `enable_auto_vacuum = 0 / 1`
- **说明：** 控制表是否在发生变异时自动触发 vacuum 操作。该选项既可以作为适用于所有表的全局设置，也可以在表级别进行配置。表级选项的优先级高于同名的会话/全局设置。启用后（设置为 1），在 INSERT 或 ALTER TABLE 等变异操作之后会自动触发 vacuum，并根据配置的数据保留策略清理表数据。

**示例：**

```sql
-- Set enable_auto_vacuum globally for all tables across all sessions
SET GLOBAL enable_auto_vacuum = 1;

-- Create a table with auto vacuum disabled (overrides global setting)
CREATE OR REPLACE TABLE t1 (id INT) ENABLE_AUTO_VACUUM = 0;
INSERT INTO t1 VALUES(1); -- Won't trigger vacuum despite global setting

-- Create another table that inherits the global setting
CREATE OR REPLACE TABLE t2 (id INT);
INSERT INTO t2 VALUES(1); -- Will trigger vacuum due to global setting

-- Enable auto vacuum for an existing table
ALTER TABLE t1 SET OPTIONS(ENABLE_AUTO_VACUUM = 1);
INSERT INTO t1 VALUES(2); -- Now will trigger vacuum

-- Table option takes precedence over global settings
SET GLOBAL enable_auto_vacuum = 0; -- Turn off globally
-- t1 will still vacuum because table setting overrides global
INSERT INTO t1 VALUES(3); -- Will still trigger vacuum
INSERT INTO t2 VALUES(2); -- Won't trigger vacuum anymore
```

### `data_retention_num_snapshots_to_keep` {#data-retention-num-snapshots-to-keep}

- **语法：** `data_retention_num_snapshots_to_keep = <n>`
- **说明：** 指定在 vacuum 操作期间要保留的快照数量。该选项既可以作为适用于所有表的全局设置，也可以在表级别进行配置。表级选项的优先级高于同名的会话/全局设置。设置后，vacuum 操作完成后只会保留指定数量的最新快照。该选项会覆盖 `data_retention_time_in_days` 设置。如果设置为 0，则会忽略此设置。此选项与 `enable_auto_vacuum` 设置配合使用，可对快照保留策略进行更细粒度的控制。

**示例：**

```sql
-- Set global retention to 10 snapshots for all tables across all sessions
SET GLOBAL data_retention_num_snapshots_to_keep = 10;

-- Create a table with custom snapshot retention (overrides global setting)
CREATE OR REPLACE TABLE t1 (id INT)
  enable_auto_vacuum = 1
  data_retention_num_snapshots_to_keep = 5;

-- Create another table that inherits the global setting
CREATE OR REPLACE TABLE t2 (id INT) enable_auto_vacuum = 1;

-- When vacuum is triggered:
-- t1 will keep 5 snapshots (table setting)
-- t2 will keep 10 snapshots (global setting)

-- Change global setting
SET GLOBAL data_retention_num_snapshots_to_keep = 20;

-- Table options still take precedence:
-- t1 will still keep only 5 snapshots
-- t2 will now keep 20 snapshots

-- Modify snapshot retention for an existing table
ALTER TABLE t1 SET OPTIONS(data_retention_num_snapshots_to_keep = 3);
-- Now t1 will keep 3 snapshots when vacuum is triggered
```

### `enable_schema_evolution` {#enable-schema-evolution}

- **语法：**

    `enable_schema_evolution = True / False`

- **说明：**

    控制在执行 `COPY INTO` 操作期间是否可以自动进行表结构演进。启用后（设置为 `True`），当负载 Parquet 文件且其 schema 中包含目标表中不存在的列时，{{{ .lake }}} 会自动将缺失的列添加到表中。现有行中缺失的值会填充为 `NULL`。更多信息，请参见 [Schema Evolution](/tidb-cloud-lake/guides/schema-evolution.md)。

**示例：**

```sql
-- Enable schema evolution for an existing table
ALTER TABLE invoices SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Create a new table with schema evolution enabled
CREATE OR REPLACE TABLE invoices (order_id INT) ENABLE_SCHEMA_EVOLUTION = true;
```
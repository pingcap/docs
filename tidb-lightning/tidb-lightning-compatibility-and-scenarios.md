---
title: TiDB Lightning 和 IMPORT INTO 与 TiCDC 及日志备份的兼容性
summary: 了解 IMPORT INTO 和 TiDB Lightning 与日志备份及 TiCDC 的兼容性。
---

# TiDB Lightning 和 IMPORT INTO 与 TiCDC 及日志备份的兼容性

本文档描述了 TiDB Lightning 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 与 [log backup](/br/br-pitr-guide.md) 以及 [TiCDC](/ticdc/ticdc-overview.md) 的兼容性，以及一些特殊使用场景。

## `IMPORT INTO` 与 TiDB Lightning 的关系

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 集成了 TiDB Lightning 的物理导入模式，但二者存在一些差异。详情请参见 [`IMPORT INTO` vs. TiDB Lightning](/tidb-lightning/import-into-vs-tidb-lightning.md)。

## 与日志备份和 TiCDC 的兼容性

- TiDB Lightning [逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md) 与日志备份和 TiCDC 兼容。

- TiDB Lightning [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md) 不兼容日志备份和 TiCDC。原因在于物理导入模式直接将源数据的编码 KV 对导入到 TiKV，导致 TiKV 在此过程中不会生成相应的变更日志。没有这些变更日志，相关数据无法通过日志备份进行备份，也无法被 TiCDC复制。

- 若要在集群中同时使用 TiDB Lightning 和 TiCDC，详见 [Compatibility with TiDB Lightning](/ticdc/ticdc-compatibility.md#compatibility-with-tidb-lightning)。

- `IMPORT INTO` 不兼容日志备份和 TiCDC。原因是 `IMPORT INTO` 也会将源数据的编码 KV 对直接导入到 TiKV。

## TiDB Lightning 逻辑导入模式的使用场景

如果 TiDB Lightning 逻辑导入模式能够满足你的应用性能需求，并且你的应用需要导入的表被备份或通过 TiCDC 进行下游复制，建议使用 TiDB Lightning 逻辑导入模式。

## TiDB Lightning 物理导入模式的使用场景

本节描述如何将 TiDB Lightning 与 [日志备份](/br/br-pitr-guide.md) 和 [TiCDC](/ticdc/ticdc-overview.md) 一起使用。

如果 TiDB Lightning 逻辑导入模式不能满足你的应用性能需求，且需要使用 TiDB Lightning 物理导入模式导入的表进行备份或下游复制，则推荐以下场景。

### 与日志备份配合使用

在此场景下，如果启用了 [PITR](/br/br-log-architecture.md#process-of-pitr)，在 TiDB Lightning 启动后，兼容性检查会报错。如果你确定这些表不需要备份，可以将 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)中的 `Lightning.check-requirements` 参数改为 `false`，然后重启导入任务。

使用 TiDB Lightning 物理导入模式导入的数据不能通过日志备份进行备份。如果需要备份表，建议在导入后进行表级快照备份，方法请参见 [Back up a table](/br/br-snapshot-manual.md#back-up-a-table)。

### 与 TiCDC 配合使用

短期内，使用 TiCDC 配合物理导入模式不兼容，因为 TiCDC 无法跟上 TiDB Lightning 物理导入模式的写入速度，可能导致集群复制延迟增加。

可以在不同场景下操作如下：

- 场景 1：表不需要被 TiCDC 下游复制。

    在此场景下，如果启用了 TiCDC changefeed，TiDB Lightning 启动后，兼容性检查会报错。如果你确定这些表不需要被备份或 [日志备份](/br/br-pitr-guide.md)，可以将 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)中的 `Lightning.check-requirements` 参数改为 `false`，然后重启导入任务。

- 场景 2：表需要被 TiCDC 下游复制。

    在此场景下，如果启用了 TiCDC changefeed，TiDB Lightning 启动后，兼容性检查会报错。你需要将上游 TiDB 集群中的 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)中的 `Lightning.check-requirements` 参数改为 `false`，然后重启导入任务。

    上游 TiDB 集群的导入任务完成后，使用 TiDB Lightning 在下游 TiDB 集群导入相同数据。如果下游存在 Redshift、Snowflake 等数据库，可以配置它们从云存储服务读取 CSV、SQL 或 Parquet 文件，然后将数据写入数据库。

## `IMPORT INTO` 的使用场景

本节描述如何将 `IMPORT INTO` 与 [日志备份](/br/br-pitr-guide.md) 和 [TiCDC](/ticdc/ticdc-overview.md) 一起使用。

### 与日志备份配合使用

在此场景下，如果启用了 [PITR](/br/br-log-architecture.md#process-of-pitr)，提交 `IMPORT INTO` 语句后，兼容性检查会报错。如果你确定这些表不需要备份，可以在该语句的 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 中加入 `DISABLE_PRECHECK`（在 v8.0.0 及以上版本引入），然后重新提交。这样，数据导入任务会忽略兼容性检查，直接导入数据。

使用 `IMPORT INTO` 导入的数据不能通过日志备份进行备份。如果需要备份表，建议在导入后进行表级快照备份，方法请参见 [Back up a table](/br/br-snapshot-manual.md#back-up-a-table)。

### 与 TiCDC 配合使用

可以在不同场景下操作如下：

- 场景 1：表不需要被 TiCDC 下游复制。

    在此场景下，如果启用了 TiCDC changefeed，提交 `IMPORT INTO` 语句后，兼容性检查会报错。如果你确定这些表不需要被 TiCDC 复制，可以在 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 中加入 `DISABLE_PRECHECK`（在 v8.0.0 及以上版本引入），然后重新提交。这样，数据导入任务会忽略兼容性检查，直接导入数据。

- 场景 2：表需要被 TiCDC 下游复制。

    在此场景下，如果启用了 TiCDC changefeed，提交 `IMPORT INTO` 语句后，兼容性检查会报错。你可以在 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 中加入 `DISABLE_PRECHECK`（在 v8.0.0 及以上版本引入），然后重新提交。这样，数据导入任务会忽略兼容性检查，直接导入数据。

    上游 TiDB 集群的导入任务完成后，使用 `IMPORT INTO` 在下游 TiDB 集群导入相同数据。如果下游存在 Redshift、Snowflake 等数据库，可以配置它们从云存储服务读取 CSV、SQL 或 Parquet 文件，然后将数据写入数据库。
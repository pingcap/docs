---
title: TiCDC Compatibility
summary: Learn about compatibility issues of TiCDC and how to handle them.
---

# TiCDC Compatibility

This section describes compatibility issues related to TiCDC and how to handle them.

## Compatibility with TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) provides two data import modes: [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md) and [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md). This section describes the compatibility of these modes with TiCDC and the steps to use TiDB Lightning and TiCDC together in a cluster.

In the logical import mode, TiDB Lightning imports data by executing SQL statements. This mode is compatible with TiCDC. To use TiDB Lightning's logical import mode with TiCDC for data replication, perform the following steps:

1. Create a changefeed. For more information, see [Create a replication task](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task).
2. Start TiDB Lightning and import data using the logical import mode. For more information, see [Use logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md).

In the physical import mode, TiDB Lightning imports data by inserting SST files into TiKV. TiCDC is not compatible with this mode and does not support replicating data imported through physical import mode. If you need to use both TiDB Lightning's physical import mode and TiCDC, choose one of the following solutions based on your downstream system:

- If the downstream is a TiDB cluster, perform the following steps:

    1. Use TiDB Lightning to import data into both the upstream and downstream TiDB clusters to ensure data consistency.
    2. Create a changefeed to replicate subsequent incremental data written through SQL. For more information, see [Create a replication task](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task).

- If the downstream is not a TiDB cluster, perform the following steps:

    1. Use the offline import tool provided by your downstream system to import TiDB Lightning's input files.
    2. Create a changefeed to replicate subsequent incremental data written through SQL. For more information, see [Create a replication task](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task).

## CLI and configuration file compatibility

* In TiCDC v4.0.0, `ignore-txn-commit-ts` is removed and `ignore-txn-start-ts` is added, which uses start_ts to filter transactions.
* In TiCDC v4.0.2, `db-dbs`/`db-tables`/`ignore-dbs`/`ignore-tables` are removed and `rules` is added, which uses new filter rules for databases and tables. For detailed filter syntax, see [Table Filter](/table-filter.md).
* Starting from TiCDC v6.2.0, `cdc cli` can directly interact with TiCDC server via TiCDC Open API. You can specify the address of the TiCDC server using the `--server` parameter. `--pd` is deprecated.
* Since v6.4.0, only the changefeed with the `SYSTEM_VARIABLES_ADMIN` or `SUPER` privilege can use the TiCDC Syncpoint feature.

## Handle compatibility issues

This section describes compatibility issues related to TiCDC and how to handle them.

### Incompatibility issue caused by using the TiCDC v5.0.0-rc `cdc cli` tool to operate a v4.0.x cluster

When using the `cdc cli` tool of TiCDC v5.0.0-rc to operate a v4.0.x TiCDC cluster, you might encounter the following abnormal situations:

- If the TiCDC cluster is v4.0.8 or an earlier version, using the v5.0.0-rc `cdc cli` tool to create a replication task might cause cluster anomalies and get the replication task stuck.

- If the TiCDC cluster is v4.0.9 or a later version, using the v5.0.0-rc `cdc cli` tool to create a replication task will cause the old value and unified sorter features to be unexpectedly enabled by default.

Solutions:

Use the `cdc` executable file corresponding to the TiCDC cluster version to perform the following operations:

1. Delete the changefeed created using the v5.0.0-rc `cdc cli` tool. For example, run the `tiup cdc:v4.0.9 cli changefeed remove -c xxxx --pd=xxxxx --force` command.
2. If the replication task is stuck, restart the TiCDC cluster. For example, run the `tiup cluster restart <cluster_name> -R cdc` command.
3. Re-create the changefeed. For example, run the `tiup cdc:v4.0.9 cli changefeed create --sink-uri=xxxx --pd=xxx` command.

> **Note:**
>
> This issue exists only when `cdc cli` is v5.0.0-rc. `cdc cli` tool of other v5.0.x versions is compatible with v4.0.x clusters.

### Compatibility notes for `sort-dir` and `data-dir`

The `sort-dir` configuration is used to specify the temporary file directory for the TiCDC sorter. Its functionalities might vary in different versions. The following table lists `sort-dir`'s compatibility changes across versions.

|  Version  |  `sort-engine` functionality  |  Note   |  Recommendation   |
|  :---  |    :---               |  :--    | :-- |
| v4.0.11 or an earlier v4.0 version, v5.0.0-rc | It is a changefeed configuration item and specifies temporary file directory for the `file` sorter and `unified` sorter. | In these versions, `file` sorter and `unified` sorter are **experimental features** and **NOT** recommended for the production environment. <br/><br/> If multiple changefeeds use the `unified` sorter as its `sort-engine`, the actual temporary file directory might be the `sort-dir` configuration of any changefeed, and the directory used for each TiCDC node might be different. | It is not recommended to use `unified` sorter in the production environment. |
| v4.0.12, v4.0.13, v5.0.0, and v5.0.1 |  It is a configuration item of changefeed or of `cdc server`. | By default, the `sort-dir` configuration of a changefeed does not take effect, and the `sort-dir` configuration of `cdc server` defaults to `/tmp/cdc_sort`. It is recommended to only configure `cdc server` in the production environment.<br /><br /> If you use TiUP to deploy TiCDC, it is recommended to use the latest TiUP version and set `sorter.sort-dir` in the TiCDC server configuration.<br /><br /> The `unified` sorter is enabled by default in v4.0.13, v5.0.0, and v5.0.1. If you want to upgrade your cluster to these versions, make sure that you have correctly configured `sorter.sort-dir` in the TiCDC server configuration. | You need to configure `sort-dir` using the `cdc server` command-line parameter (or TiUP). |
|  v4.0.14 and later v4.0 versions, v5.0.3 and later v5.0 versions, later TiDB versions | `sort-dir` is deprecated. It is recommended to configure `data-dir`.  |  You can configure `data-dir` using the latest version of TiUP. In these TiDB versions, `unified` sorter is enabled by default. Make sure that `data-dir` has been configured correctly when you upgrade your cluster. Otherwise, `/tmp/cdc_data` will be used by default as the temporary file directory. <br /><br /> If the storage capacity of the device where the directory is located is insufficient, the problem of insufficient hard disk space might occur. In this situation, the previous `sort-dir` configuration of changefeed will become invalid.| You need to configure `data-dir` using the `cdc server` command-line parameter (or TiUP).  |
| v6.0.0 and later versions | `data-dir` is used for saving the temporary files generated by TiCDC. | Starting from v6.0.0, TiCDC uses `db sorter` as the sort engine by default. `data-dir` is the disk directory for this engine.  | You need to configure `data-dir` using the `cdc server` command-line parameter (or TiUP).  |

### Compatibility with temporary tables

Since v5.3.0, TiCDC supports [global temporary tables](/temporary-tables.md#global-temporary-tables). Replicating global temporary tables to the downstream using TiCDC of a version earlier than v5.3.0 causes table definition error.

If the upstream cluster contains a global temporary table, the downstream TiDB cluster is expected to be v5.3.0 or a later version. Otherwise, an error occurs during the replication process.

### Compatibility with vector data types

Starting from v8.4.0, TiCDC supports replicating tables with [vector data types](/vector-search-data-types.md) to downstream (experimental).

When the downstream is Kafka or a storage service (such as Amazon S3, GCS, Azure Blob Storage, or NFS), TiCDC converts vector data types into string types before writing to the downstream.

When the downstream is a MySQL-compatible database that does not support vector data types, TiCDC fails to write DDL events involving vector types to the downstream. In this case, add the `has-vector-type=true` parameter to `sink-url`, which allows TiCDC to convert vector data types into the `LONGTEXT` type before writing.
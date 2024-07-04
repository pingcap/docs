---
title: TiFlash Upgrade Guide
summary: Learn the precautions when you upgrade TiFlash.
---

# TiFlash Upgrade Guide

This document describes the function changes and recommended actions that you need to learn when you upgrade TiFlash.

To learn the standard upgrade process, see the following documents:

- [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md)
- [Upgrade TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **Note:**
>
> - [FastScan](/tiflash/use-fastscan.md) is introduced in v6.2.0 as an experimental feature and becomes generally available (GA) in v7.0.0. It provides more efficient query performance at the cost of strong data consistency.
>
> - It is not recommended that you upgrade TiDB that includes TiFlash across major versions, for example, from v4.x to v6.x. Instead, you need to upgrade from v4.x to v5.x first, and then to v6.x.
>
> - v4.x is near the end of its life cycle. It is recommended that you upgrade to v5.x or later as soon as possible. For more information, see [TiDB Release Support Policy](https://www.pingcap.com/tidb-release-support-policy/).
>
> - PingCAP does not provide bug fixes for non-LTS versions, such as v6.0. It is recommended that you upgrade to v6.1 and later LTS versions whenever possible.
>

## Upgrade TiFlash using TiUP

To upgrade TiFlash from versions earlier than v5.3.0 to v5.3.0 or later, you must stop TiFlash and then upgrade it. When you upgrade TiFlash using TiUP, note the following:

- If the TiUP cluster version is v1.12.0 or later, you cannot stop TiFlash and then upgrade it. If the target version requires a TiUP cluster version of v1.12.0 or later, it is recommended that you first use `tiup cluster:v1.11.3 <subcommand>` to upgrade TiFlash to an intermediate version, perform an online upgrade of the TiDB cluster, upgrade the TiUP version, and then upgrade the TiDB cluster to the target version directly without stopping it.
- If the TiUP cluster version is earlier than v1.12.0, perform the following steps to upgrade TiFlash.

The following steps help you use TiUP to upgrade TiFlash without interrupting other components:

1. Stop the TiFlash instance:

    ```shell
    tiup cluster stop <cluster-name> -R tiflash
    ```

2. Upgrade the TiDB cluster without restarting it (only updating the files):

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline 
    ```

    For example:

    ```shell
    tiup cluster upgrade <cluster-name> v5.3.0 --offline
    ```

3. Reload the TiDB cluster. After the reload, the TiFlash instance is started and you do not need to manually start it.

    ```shell
    tiup cluster reload <cluster-name>
    ```

## From 5.x or v6.0 to v6.1

When you upgrade TiFlash from v5.x or v6.0 to v6.1, pay attention to the functional changes in TiFlash Proxy and dynamic pruning.

### TiFlash Proxy

TiFlash Proxy is upgraded in v6.1.0 (aligned with TiKV v6.0.0). The new version has upgraded the RocksDB version. After you upgrade TiFlash to v6.1, the data format is converted to the new version automatically.

In regular upgrades, the data conversion does not involve any risks. However, if you need to downgrade TiFlash from v6.1 to any earlier version in special scenarios (for example, testing or verification scenarios), the earlier version might fail to parse the new RocksDB configuration. As as result, TiFlash will fail to restart. It is recommended that you fully test and verify the upgrade process and prepare an emergency plan.

**Workaround for downgrading TiFlash in testing or other special scenarios**

You can forcibly scale in the target TiFlash node and then replicate data from TiKV again. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

### Dynamic pruning

If you do not enable [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) and will not use it in the future, you can skip this section.

- Newly installed TiDB v6.1.0: Dynamic pruning is enabled by default.

- TiDB v6.0 and earlier: Dynamic pruning is disabled by default. The setting of dynamic pruning after an upgrade inherits that of the previous version. That is, dynamic pruning will not be enabled (or disabled) automatically after an upgrade.

    After an upgrade, to enable dynamic pruning, set `tidb_partition_prune_mode` to `dynamic` and manually update GlobalStats of partitioned tables. For details, see [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode).

## From v5.x or v6.0 to v6.2

In TiDB v6.2, TiFlash upgrades its data storage format to the V3 version. Therefore, when you upgrade TiFlash from v5.x or v6.0 to v6.2, besides functional changes in [TiFlash Proxy](#tiflash-proxy) and [Dynamic pruning](#dynamic-pruning), you also need to pay attention to the functional change in PageStorage.

### PageStorage

By default, TiFlash v6.2.0 uses PageStorage V3 version [`format_version = 4`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). This new data format significantly reduces the peak write I/O traffic. In scenarios with high update traffic and high concurrency or heavy queries, it effectively relieves excessive CPU usage caused by TiFlash data GC. Meanwhile, compared with the earlier storage format, the V3 version significantly reduces space amplification and resource consumption.

- After an upgrade to v6.2.0, as new data is written to the existing TiFlash nodes, earlier data will be gradually converted to the new format.
- However, earlier data cannot be completely converted to the new format during the upgrade, because the conversion consumes a certain amount of system overhead (services are not affected, but you still need to pay attention). After the upgrade, it is recommended that you run the [`Compact` command](/sql-statements/sql-statement-alter-table-compact.md) to convert the data to the new format. The steps are as follows:

    1. Run the following command for each table containing TiFlash replicas:

        ```sql
        ALTER TABLE <table_name> COMPACT tiflash replica;
        ```

    2. Restart the TiFlash node.

You can check whether tables still use the old data format on Grafana: **TiFlash-Summary** > **Storage Pool** > **Storage Pool Run Mode**.

- Only V2: Number of tables using PageStorage V2 (including partitions)
- Only V3: Number of tables using PageStorage V3 (including partitions)
- Mix Mode: Number of tables with data format converted from PageStorage V2 to PageStorage V3 (including partitions)

**Workaround for downgrading TiFlash in testing or other special scenarios**

You can forcibly scale in the target TiFlash node and then replicate data from TiKV again. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

## From v6.1 to v6.2

When you upgrade TiFlash from v6.1 to v6.2, pay attention to the change in data storage format. For details, see [PageStorage](#pagestorage).

## From v6.x or v7.x to v7.3 with `storage.format_version = 5` configured

Starting from v7.3, TiFlash introduces a new DTFile version: DTFile V3 (experimental). This new DTFile version can merge multiple small files into a single larger file to reduce the total number of files. In v7.3, the default DTFile version is still V2. To use V3, you can set the [TiFlash configuration parameter](/tiflash/tiflash-configuration.md) `storage.format_version = 5`. After the setting, TiFlash can still read V2 DTFiles and will gradually rewrite existing V2 DTFiles to V3 DTFiles during subsequent data compaction.

After upgrading TiFlash to v7.3 and configuring TiFlash to use V3 DTFiles, if you need to revert TiFlash to an earlier version, you can use the DTTool offline to rewrite V3 DTFiles back to V2 DTFiles. For more information, see [DTTool Migration Tool](/tiflash/tiflash-command-line-flags.md#dttool-migrate).

## From v6.x or v7.x to v7.4 or a later version

Starting from v7.4, to reduce the read and write amplification generated during data compaction, TiFlash optimizes the data compaction logic of PageStorage V3, which leads to changes to some of the underlying storage file names. Therefore, after the upgrade to v7.4 or a later version, in-place downgrading to the original version is not supported.

**Workaround for downgrading TiFlash in testing or other special scenarios**

To downgrade TiFlash in testing or other special scenarios, you can forcibly scale in the target TiFlash node and then replicate data from TiKV again. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).
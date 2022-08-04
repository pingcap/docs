---
title: TiFlash v6.2.0 Upgrade Guide
summary: Learn the precautions when you upgrade TiFlash to v6.2.0.
---

# TiFlash v6.2.0 Upgrade Guide

This document describes the functional changes in TiFlash modules you need to pay attention to when you upgrade TiFlash from earlier versions to v6.2.0, and recommended actions for you to take.

To learn the standard upgrade process, see the following documents:

- [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md)
- [Upgrade TiDB in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **Note:**
> 
> - It is not recommended that you upgrade TiFlash across major versions, for example, from v4.x.x to v6.x.x. Instead, you need to upgrade from v4.x.x to v5.x.x first, and then to v6.x.x.
>
> - v4.x.x is near the end of its life cycle. Please upgrade to v5.x.x or later as soon as possible. For more information, see [TiDB Release Support Policy](https://en.pingcap.com/tidb-release-support-policy/).
>
> - As a non-LTS version, v6.0.0 will not release subsequent bug-fix versions. Please use v6.1.0 and later LTS versions whenever possible.
>
> - To upgrade TiFlash from versions earlier than V5.3.0 to V5.3.0 or later, you should stop TiFlash and then upgrade it. The following steps help you upgrade TiFlash without interrupting other components:
> 
>    - Stop the TiFlash instance: `tiup cluster stop <cluster-name> -R tiflash`
>    - Upgrade the TiDB cluster without restarting it (only updating the files): `tiup cluster upgrade <cluster-name> <version> --offline`
>    - Reload the TiDB cluster: `tiup cluster reload <cluster-name>`. After the reload, the TiFlash instance is started and you do not need to manually start it.

## From 5.x.x or v6.0.0 to v6.1.0

When you upgrade TiFlash from v5.x.x or v6.0.0 to v6.1.0, pay attention to the functional changes in TiFlash Proxy and dynamic pruning.

### TiFlash Proxy

TiFlash Proxy is upgraded in v6.1.0 (aligned with TiKV v6.0.0). The new version has upgraded the RocksDB version. After you upgrade TiFlash to v6.1.0, the data format is converted to the new version automatically.

In normal upgrades, the data conversion does not involve any risks. However, if you need to downgrade TiFlash from v6.1.0 to any earlier version in special scenarios (for example, testing or verification scenarios), note that the RocksDB configuration of the newer version might fail to be parsed. As as result, TiFlash will fail to restart. It is recommended that you fully test and verify the upgrade process and prepare an emergency plan.

**Workaround for downgrading TiFlash in testing or other special scenarios**

You can forcibly scale in the target TiFlash node and then replicate data. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

### Dynamic pruning

If you do not enable [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) and will not use it in the future, you can skip this section.

- Newly installed TiDB v6.1.0: Dynamic pruning is enabled by default.

- TiDB v6.0.0 and earlier: Dynamic pruning is disabled by default. The setting of dynamic pruning inherits the previous version after an upgrade. That is, dynamic pruning will not be enabled (or disabled) automatically after an upgrade.

    After an upgrade, to enable dynamic pruning, set `tidb_partition_prune_mode` to `dynamic` and manually update GlobalStats of partitioned tables. For details, see [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode).

## From v5.x.x or v6.0.0 to v6.2.0

In TiDB v6.2.0, TiFlash upgrades its data storage format to the V3 version. Therefore, when you upgrade TiFlash from v5.x.x or v6.0.0 to v6.2.0, besides functional changes in [TiFlash Proxy](#tiflash-proxy) and [Dynamic pruning](#dynamic-pruning), you also need to pay attention to the functional change in PageStorage.

### PageStorage

By default, TiFlash v6.2.0 uses PageStorage V3 version [`format_version = 4`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). This version significantly reduces the peak write I/O traffic and relieves excessive CPU usage caused by TiFlash data GC in scenarios with high update traffic and high concurrency or heavy queries.

- With more data written to the existing TiFlash nodes following the upgrade to v6.2.0, earlier data will be gradually converted to the new format.
- However, earlier data cannot be completely converted to the new format, because the conversion consumes certain amount of system overhead (services are not affected, but you still need to pay attention). After the upgrade, it is recommended that you run the [`Compact` command](/sql-statements/sql-statement-alter-table-compact.md) to convert the data to the new format. The steps are as follows:

    1. Run the following command to each table containing TiFlash replicas:

        ```sql
        ALTER TABLE <table_name> compact tiflash replica;
        ```

    2. Restart the TiFlash node.

You can check for tables using the old data format on Grafana in the following path: Tiflash summary > storage pool > Storage Pool Run Mode.

- Only V2: Number of tables using PageStorage V2 (including partitions)
- Only V3: Number of tables using PageStorage V3 (including partitions)
- Mix Mode: Number of tables with data format converted from PageStorage V2 to PageStorage V3 (including partitions)

**Workaround for downgrading TiFlash in testing or other special scenarios**

You can forcibly scale in the target TiFlash node and then replicate data. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

## From v6.1.0 to v6.2.0

When you upgrade TiFlash from v6.1.0 to v6.2.0, pay attention to the change in data storage format. For details, see [PageStorage](#pagestorage).

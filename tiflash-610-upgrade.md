---
title: TiFlash v6.1.0 Upgrade Guide
summary: Learn the precautions when you upgrade TiFlash to v6.1.0.
---

# TiFlash v6.1.0 Upgrade Guide

This document describes the changes in the TiFlash functional modules when upgraded to v6.1.0 and recommended actions for you to take.

To learn the standard upgrade process, see the following documents:

- [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md)
- [Upgrade TiDB in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

## Upgrade policies

It is not recommended that you upgrade TiFlash to v6.1.0 across major versions, for example, from v4.0.0 to v6.1.0. Instead, you need to upgrade earlier versions to v5.4.x or v6.0.0 first, and then to v6.1.0.

### Upgrade from v4.x.x to v5.x.x

v4.x.x is near the end of its life cycle. Please upgrade to v5.x.x or later as soon as possible.

### Upgrade from v5.x.x to v6.0.0

As a non-LTS version, v6.0.0 will not release subsequent bug-fix versions. Please use v6.1.0 and later LTS versions whenever possible.

### Upgrade from 5.x.x to v6.1.0

#### TiFlash Proxy

TiFlash Proxy is upgraded in v6.1.0 (aligned with TiKV v6.0.0). The new version has upgraded the RocksDB version. After you upgrade TiFlash to v6.1.0, the data format is converted to the new version automatically.

In normal upgrades, the data conversion does not involve any risks. However, if you need to downgrade TiFlash from v6.1.0 to any earlier version in special scenarios (for example, testing or verification scenarios), note that the RocksDB configuration of the newer version might fail to be parsed. As as result, TiFlash will fail to restart. It is recommended that you fully test and verify the upgrade process and prepare an emergency plan.

**Workaround for downgrading TiFlash in testing or other special scenarios**

You can forcibly scale in the target TiFlash node and then replicate data. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

#### Dynamic pruning

If you do not enable dynamic pruning and will not use it in the future, you can skip this section.

- Newly installed TiDB v6.1.0: Dynamic pruning is enabled by default.

- TiDB v6.0.0 and earlier: Dynamic pruning is disabled by default. The setting of dynamic pruning inherits the previous version after an upgrade. That is, dynamic pruning will not be enabled (or disabled) automatically after an upgrade.

    After an upgrade, to enable dynamic pruning, you need to manually update GlobalStats of partitioned tables. For details, see [Dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode).

#### TiFlash PageStorage

By default, TiFlash v6.1.0 upgrades PageStorage to the V3 version (`format_version=4`). This version significantly reduces the peak write I/O traffic and CPU usage caused by TiFlash data GC in scenarios with high concurrency and heavy queries.

- With more data written to the existing TiFlash nodes following the upgrade to v6.1.0, earlier data will be gradually converted to the new format.
- However, earlier data cannot be completely converted to the new format, because the conversion consumes certain amount of system overhead (services are not affected, but you still need to pay attention). After the upgrade, it is recommended that you run the [compaction](/sql-statements/sql-statement-alter-table-compact.md) command to convert the data to the new format. The steps are as follows:

    1. Run the following command to each table containing TiFlash replicas:

        ```
        alter table <table_name> compact tiflash replica;
        ```

    2. Restart the TiFlash node.

You can check for tables using the old data format on Grafana in the following path: Tiflash summary > storage pool > Storage Pool Run Mode.

**Workaround for downgrading TiFlash in testing or other special scenarios**

You can forcibly scale in the target TiFlash node and then replicate data. For detailed steps, see [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

### Upgrade v6.0.0 to v6.1.0

#### Dynamic pruning

If you do not enable dynamic pruning and will not use it in the future, you can skip this section.

For newly installed TiDB v6.0.0 and later, dynamic pruning is enabled by default. For versions earlier than v6.0.0, the setting of dynamic pruning inherits the previous version after an upgrade. That is, dynamic pruning will not be enabled (or disabled) automatically after an upgrade.

During an upgrade from v6.0.0 to v6.1.0, no special actions are required. However, note that GlobalStats of partitioned tables will be automatically updated.

#### TiFlash PageStorage

See TiFlash PageStorage description in the section [upgrade from v5.x.x to v6.1.0](#upgrade-from-5xx-to-v610).

#### TiFlash Proxy

See TiFlash Proxy description in the section [upgrade from v5.x.x to v6.1.0](#upgrade-from-5xx-to-v610).

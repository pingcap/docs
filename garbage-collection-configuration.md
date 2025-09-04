---
title: Garbage Collection Configuration
summary: Learn about GC configuration parameters.
aliases: ['/docs/dev/garbage-collection-configuration/','/docs/dev/reference/garbage-collection/configuration/']
---

# Garbage Collection Configuration

You can configure garbage collection (GC) using the following system variables:

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50): controls whether to enable garbage collection for TiKV.
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50): specifies the GC interval.
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50): specifies the time limit during which data is retained for each GC.
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50): specifies the number of threads in the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step of GC.
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50): specifies the way of scanning locks in the Resolve Locks step of GC.
* [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610): specifies the maximum time that active transactions block the GC safe point.

For more information about how to modify the value of a system variable, see [System variables](/system-variables.md).

## GC I/O limit

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is only applicable to TiDB Self-Managed. TiDB Cloud does not have a GC I/O limit by default.

</CustomContent>

TiKV supports the GC I/O limit. You can configure `gc.max-write-bytes-per-sec` to limit writes of a GC worker per second, and thus to reduce the impact on normal requests.

`0` indicates disabling this feature.

You can dynamically modify this configuration using tikv-ctl:

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## Changes in TiDB 5.0

In previous releases of TiDB, garbage collection was configured via the `mysql.tidb` system table. While changes to this table continue to be supported, it is recommended to use the system variables provided. This helps ensure that any changes to configuration can be validated, and prevent unexpected behavior ([#20655](https://github.com/pingcap/tidb/issues/20655)).

The `CENTRAL` garbage collection mode is no longer supported. The `DISTRIBUTED` GC mode (which has been the default since TiDB 3.0) will automatically be used in its place. This mode is more efficient, since TiDB no longer needs to send requests to each TiKV region to trigger garbage collection.

For information on changes in previous releases, refer to earlier versions of this document using the _TIDB version selector_ in the left hand menu.

## Changes in TiDB 6.1.0

Before TiDB v6.1.0, the transaction in TiDB does not affect the GC safe point. Starting from v6.1.0, TiDB considers the startTS of the transaction when calculating the GC safe point, to resolve the problem that the data to be accessed has been cleared. If the transaction is too long, the safe point will be blocked for a long time, which affects the application performance.

In TiDB v6.1.0, the system variable [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610) is introduced to control the maximum time that active transactions block the GC safe point. After the value is exceeded, the GC safe point is forwarded forcefully.

### GC in Compaction Filter

Based on the `DISTRIBUTED` GC mode, the mechanism of GC in Compaction Filter uses the compaction process of RocksDB, instead of a separate GC worker thread, to run GC. This new GC mechanism helps to avoid extra disk read caused by GC. Also, after clearing the obsolete data, it avoids a large number of left tombstone marks which degrade the sequential scan performance.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The following examples of modifying TiKV configurations are only applicable to TiDB Self-Managed. For TiDB Cloud, the mechanism of GC in Compaction Filter is enabled by default.

</CustomContent>

The following example shows how to enable the mechanism in the TiKV configuration file:

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

You can also enable this GC mechanism by modifying the configuration dynamically. See the following example:

{{< copyable "sql" >}}

```sql
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | false |
+------+-------------------+-----------------------------+-------+
```

{{< copyable "sql" >}}

```sql
set config tikv gc.enable-compaction-filter = true;
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | true  |
+------+-------------------+-----------------------------+-------+
```

<CustomContent platform="tidb">

> **Note:**
>
> When using the Compaction Filter mechanism, GC progress might be delayed, which can affect TiKV scan performance. If your workload contains a large number of coprocessor requests and you observe in the [**TiKV-Details > Coprocessor Detail**](/grafana-tikv-dashboard.md#coprocessor-detail) panel that the `next()` or `prev()` call count in **Total Ops Details** significantly exceeds three times the `processed_keys` calls, you can take the following actions:
> 
> - For TiDB versions before v7.1.3, it is recommended to disable Compaction Filter to speed up GC.
> - For TiDB versions from v7.1.3 to v7.5.6, TiDB automatically triggers compaction based on the number of redundant versions in each Region [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710) and the percentage of redundant versions [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) to improve Compaction Filter GC performance. In this case, adjust these configuration items instead of disabling Compaction Filter.
> - Starting from v7.5.7, [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710) and [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) are deprecated. TiDB now automatically triggers compaction based on [`gc.auto-compaction.redundant-rows-threshold`](/tikv-configuration-file.md#redundant-rows-threshold-new-in-v757-and-v900) and [`gc.auto-compaction.redundant-rows-percent-threshold`](/tikv-configuration-file.md#redundant-rows-percent-threshold-new-in-v757-and-v900). In this case, adjust these configuration items instead of disabling Compaction Filter.

</CustomContent>

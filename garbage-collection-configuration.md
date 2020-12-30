---
title: Garbage Collection Configuration
summary: Learn about GC configuration parameters.
aliases: ['/docs/dev/garbage-collection-configuration/','/docs/dev/reference/garbage-collection/configuration/']
---

# Garbage Collection Configuration

Garbage collection is configured via the following system variables:

* [`tikv_gc_enable`](/system-variables.md#tikv_gc_enable)
* [`tikv_gc_run_interval`](/system-variables.md#tikv_gc_run_interval)
* [`tikv_gc_life_time`](/system-variables.md#tikv_gc_life_time)
* [`tikv_gc_mode`](/system-variables.md#tikv_gc_mode)
* [`tikv_gc_concurrency`](/system-variables.md#tikv_gc_concurrency)
* [`tikv_gc_scan_lock_mode`](/system-variables.md#tikv_gc_scan_lock_mode)

In previous releases of TiDB, garbage collection was configured via the `mysql.tidb` table. While changes to this table continue to be supported, it is recommended to use the system variables provided.

## Notes on GC process changes

Since TiDB 3.0, some configuration options have changed with support for the distributed GC mode and concurrent Resolve Locks processing. The changes are shown in the following table:

| Version/Configuration          |  Resolve Locks          |  Do GC  |
|-------------------|---------------|----------------|
| 2.x               | Serial | Concurrent |
| 3.0 <br/> `tikv_gc_mode = centered` <br/> `tikv_gc_auto_concurrency = false` | Concurrent | Concurrent |
| 3.0 <br/> `tikv_gc_mode = centered` <br/> `tikv_gc_auto_concurrency = true` | Auto-concurrent | Auto-concurrent |
| 3.0 <br/> `tikv_gc_mode = distributed` <br/> `tikv_gc_auto_concurrency = false` | Concurrent | Distributed |
| 3.0 <br/> `tikv_gc_mode = distributed` <br/> `tikv_gc_auto_concurrency = true` <br/> (default) | Auto-concurrent | Distributed |

- Serial: requests are sent from TiDB Region by Region.
- Concurrent: requests are sent to each Region concurrently based on the number of threads specified by [`tikv_gc_concurrency`](/system-variables.md#tikv_gc_concurrency).
- Auto-concurrent: requests are sent to each Region concurrently with the number of TiKV nodes as concurrency value.
- Distributed: no need for TiDB to send requests to TiKV to trigger GC because each TiKV handles GC on its own.

In addition, if Green GC (experimental feature) is enabled, that is, setting the value of [`tikv_gc_scan_lock_mode`](/system-variables.md#tikv_gc_scan_lock_mode) to `PHYSICAL`, the processing of Resolve Lock is not affected by the concurrency configuration above.

## GC I/O limit

TiKV supports the GC I/O limit. You can configure `gc.max-write-bytes-per-sec` to limit writes of a GC worker per second, and thus to reduce the impact on normal requests.

`0` indicates disabling this feature.

You can dynamically modify this configuration using tikv-ctl:

{{< copyable "shell-regular" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB
```

## GC in Compaction Filter

Since v5.0.0-rc, TiDB introduces the mechanism of GC in Compaction Filter. Based on the distributed GC mode, the mechanism uses the compaction process of RocksDB, instead of a separate GC worker thread, to run GC. This new GC machanism helps to avoid extra disk read caused by GC. Also, after clearing the obsolete data, it avoids a large number of left tombstone marks which degrade the sequential scan performance. This GC mechanism is disabled by default. The following example shows how to enable the mechanism in the TiKV configuration file:

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

You can also enable this GC mechanism by modifying the configuration online. See the following example:

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

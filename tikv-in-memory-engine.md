---
title: TiKV MVCC In-Memory Engine
summary: Learn the applicable scenarios and working principles of the in-memory engine, and how to use the in-memory engine to accelerate queries for MVCC versions.
---

# TiKV MVCC In-Memory Engine

TiKV MVCC In-Memory Engine (IME) is primarily used to accelerate queries that need to scan a large number of MVCC historical versions, that is, [the total number of versions scanned (`total_keys`) is much greater than the number of versions processed (`processed_keys`)](/analyze-slow-queries.md#obsolete-mvcc-versions-and-excessive-keys).

TiKV MVCC in-memory engine is suitable for the following scenarios:

- The application that requires querying records that are frequently updated or deleted.
- The application that requires adjusting [`tidb_gc_life_time`](/garbage-collection-configuration.md#garbage-collection-configuration) to retain historical versions in TiDB for a longer period (for example, 24 hours).

## Implementation principles

The TiKV MVCC in-memory engine caches the latest written MVCC versions in memory, and implements an MVCC GC mechanism independent of TiDB. This allows it to quickly perform GC on MVCC versions in memory, reducing the number of versions scanned during queries, thereby lowering request latency and reducing CPU overhead.

The following diagram illustrates how TiKV organizes MVCC versions:

![IME caches recent versions to reduce CPU overhead](/media/tikv-ime-data-organization.png)

The preceding diagram shows two rows of records, each with 9 MVCC versions. The behavior comparison between enabling and not enabling the in-memory engine is as follows:

- On the left (in-memory engine disabled): the table records are stored in RocksDB in ascending order by the primary key, with all MVCC versions of the same row adjacent to each other.
- On the right (in-memory engine enabled): the data in RocksDB is the same as that on the left, but the in-memory engine caches the two latest MVCC versions for each of the two rows.
- When TiKV processes a scan request with a range of `[k1, k2]` and a start timestamp of `8`:
    - Without the in-memory engine (left), it needs to process 11 MVCC versions.
    - With the in-memory engine (right), it only processes 4 MVCC versions, reducing request latency and CPU consumption.
- When TiKV processes a scan request with a range of `[k1, k2]` and a start timestamp of `7`:
    - Because the required historical versions are missing in the in-memory engine (right), the cache becomes invalid, and TiKV falls back to reading data from RocksDB.

## Usage

To enable the TiKV MVCC in-memory engine (IME), you need to adjust the [TiKV configuration](/tikv-configuration-file.md#in-memory-engine-new-in-v850) and restart TiKV. The configuration details are as follows:

```toml
[in-memory-engine]
# This parameter is the switch for the in-memory engine feature, which is disabled by default. You can set it to true to enable it.
# It is recommended to configure at least 8 GiB of memory for the TiKV node, with 32 GiB or more for optimal performance.
# If the available memory for the TiKV node is insufficient, the in-memory engine will not be enabled even if this configuration item is set to true. In such cases, check the TiKV log file for messages containing "in-memory engine is disabled because" to learn why the in-memory engine is not enabled.
enable = false

# This parameter controls the memory size available to the in-memory engine.
# The default value is 10% of the system memory, and the maximum value is 5 GiB.
# You can manually adjust this configuration to allocate more memory.
# Note: When the in-memory engine is enabled, block-cache.capacity automatically decreases by 10%.
capacity = "5GiB"

# This parameter controls the time interval for the in-memory engine to GC the cached MVCC versions.
# The default value is 3 minutes, representing that GC is performed every 3 minutes on the cached MVCC versions.
# Decreasing the value of this parameter can increase the GC frequency, reduce the number of MVCC versions, but will increase CPU consumption for GC and increase the probability of in-memory engine cache miss.
gc-run-interval = "3m"

# This parameter controls the threshold for the in-memory engine to select and load Regions based on MVCC read amplification.
# The default value is 10, indicating that if reading a single row in a Region requires processing more than 10 MVCC versions, this Region might be loaded into the in-memory engine.
mvcc-amplification-threshold = 10
```

> **Note:**
>
> + The in-memory engine is disabled by default. After you enable it, you need to restart TiKV.
> + Except for `enable`, all the other configuration items can be dynamically adjusted.

### Automatic loading

After you enable the in-memory engine, TiKV automatically selects the Regions to load based on the read traffic and MVCC amplification of the Region. The specific process is as follows:

1. Regions are sorted based on the number of recent `next` (RocksDB Iterator next API) and `prev` (RocksDB Iterator prev API) calls.
2. Regions are filtered using the `mvcc-amplification-threshold` configuration parameter. The default value is `10`. MVCC amplification measures read amplification, calculated as (`next` + `prev`) / `processed_keys`.
3. The top N Regions with severe MVCC amplification are loaded, where N is determined based on memory estimation.

The in-memory engine also periodically evicts Regions. The process is as follows:

1. The in-memory engine evicts Regions with low read traffic or low MVCC amplification.
2. If memory usage reaches 90% of `capacity` and new Regions need to be loaded, then the in-memory engine selects and evicts Regions based on read traffic.

## Compatibility

+ [BR](/br/br-use-overview.md): the in-memory engine can be used alongside BR. However, during a BR restore, the Regions involved in the restore process are evicted from the in-memory engine. After the BR restore is complete, if the corresponding Regions remain hotspots, they will be automatically loaded by the in-memory engine.
+ [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md): the in-memory engine can be used alongside TiDB Lightning. However, when TiDB Lightning operates in physical import mode, it evicts the Regions involved in the restore process from the in-memory engine. Once the physical import is complete, if the corresponding Regions remain hotspots, they will be automatically loaded by the in-memory engine.
+ [Follower Read](/develop/dev-guide-use-follower-read.md) and [Stale Read](/develop/dev-guide-use-stale-read.md): the in-memory engine can be used alongside these two features. However, the in-memory engine can only accelerate coprocessor requests on the Leader, and cannot accelerate Follower Read and Stale Read operations.
+ [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md): the in-memory engine can be used alongside Flashback. However, Flashback invalidates the in-memory engine cache. After the Flashback process is complete, the in-memory engine will automatically load hotspot Regions.

## FAQ

### Can the in-memory engine reduce write latency and increase write throughput?

No. The in-memory engine can only accelerate read requests that scan a large number of MVCC versions.

### How to determine if the in-memory engine can improve my scenario?

You can execute the following SQL statement to check if there are slow queries with `Total_keys` much greater than `Process_keys`:

```sql
SELECT
    Time,
    DB,
    Index_names,
    Process_keys,
    Total_keys,
    CONCAT(
        LEFT(REGEXP_REPLACE(Query, '\\s+', ' '), 20),
        '...',
        RIGHT(REGEXP_REPLACE(Query, '\\s+', ' '), 10)
    ) as Query,
    Query_time,
    Cop_time,
    Process_time
FROM
    INFORMATION_SCHEMA.SLOW_QUERY
WHERE
    Is_internal = 0
    AND Cop_time > 1
    AND Process_keys > 0
    AND Total_keys / Process_keys >= 10
    AND Time >= NOW() - INTERVAL 10 MINUTE
ORDER BY Total_keys DESC
LIMIT 5;
```

Example:

The following result shows that queries with severe MVCC amplification exist on the `db1.tbl1` table. TiKV processes 1358517 MVCC versions and only returns 2 versions.

```
+----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
| Time                       | DB  | Index_names       | Process_keys | Total_keys | Query                             | Query_time         | Cop_time           | Process_time       |
+----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
| 2024-11-18 11:56:10.303228 | db1 | [tbl1:some_index] |            2 |    1358517 |  SELECT * FROM tbl1 ... LIMIT 1 ; | 1.2581352350000001 |         1.25651062 |        1.251837479 |
| 2024-11-18 11:56:11.556257 | db1 | [tbl1:some_index] |            2 |    1358231 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.252694002 |        1.251129038 |        1.240532546 |
| 2024-11-18 12:00:10.553331 | db1 | [tbl1:some_index] |            2 |    1342914 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.473941872 | 1.4720495900000001 | 1.3666103170000001 |
| 2024-11-18 12:01:52.122548 | db1 | [tbl1:some_index] |            2 |    1128064 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.058942591 |        1.056853228 |        1.023483875 |
| 2024-11-18 12:01:52.107951 | db1 | [tbl1:some_index] |            2 |    1128064 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.044847031 |        1.042546122 |        0.934768555 |
+----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
5 rows in set (1.26 sec)
```

### How can I check whether the TiKV MVCC in-memory engine is enabled?

You can check the TiKV configuration using the [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) statement. If the value of `in-memory-engine.enable` is `true`, it means that TiKV MVCC in-memory engine is enabled.

```sql
SHOW CONFIG WHERE Type='tikv' AND Name LIKE 'in-memory-engine\.%';
```

```
+------+-----------------+-----------------------------------------------+---------+
| Type | Instance        | Name                                          | Value   |
+------+-----------------+-----------------------------------------------+---------+
| tikv | 127.0.0.1:20160 | in-memory-engine.capacity                     | 5GiB    |
| tikv | 127.0.0.1:20160 | in-memory-engine.cross-check-interval         | 0s      |
| tikv | 127.0.0.1:20160 | in-memory-engine.enable                       | true    |
| tikv | 127.0.0.1:20160 | in-memory-engine.evict-threshold              | 4920MiB |
| tikv | 127.0.0.1:20160 | in-memory-engine.gc-run-interval              | 3m      |
| tikv | 127.0.0.1:20160 | in-memory-engine.load-evict-interval          | 5m      |
| tikv | 127.0.0.1:20160 | in-memory-engine.mvcc-amplification-threshold | 10      |
| tikv | 127.0.0.1:20160 | in-memory-engine.stop-load-threshold          | 4208MiB |
+------+-----------------+-----------------------------------------------+---------+
8 rows in set (0.00 sec)
```

### How can I monitor the TiKV MVCC in-memory engine?

You can check the [**In Memory Engine**](/grafana-tikv-dashboard.md#in-memory-engine) section on the **TiKV-Details** dashboard in Grafana.

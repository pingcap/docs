---
title: TiDB 8.5.6 Release Notes
summary: Understand the compatibility changes, improvements, and bug fixes in the TiDB 8.5.6 release.
---

# TiDB 8.5.6 Release Notes

Release Date: 2026-xx-xx

TiDB Version: 8.5.6

Try it out: [Quick Start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production Deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup) | [Download Offline Package](https://pingkai.cn/download#tidb-community)

## Feature Details

### 性能

- 外键检查支持共享锁（GA） [#66154](https://github.com/pingcap/tidb/issues/66154) @[you06](https://github.com/glorv) **tw@qiancai** <!--2085-->

    对子表进行写入时，支持用户通过设置参数 tidb_foreign_key_check_in_shared_lock 来指定在父表加共享锁实现外键约束检查，相比以前仅支持排它锁，现方案可降低锁冲突提升子表并发写入性能。

    在V8.5.6 中，该功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](/foreign-key.md)。

### Stability

- Support setting the maximum limit on resource usage for background tasks of resource control (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1933-->

    TiDB resource control can identify and lower the priority of background tasks. In certain scenarios, you might want to limit the resource consumption of background tasks, even when resources are available. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set the maximum percentage of resources that background tasks can consume. Each node will keep the resource usage of all background tasks below this percentage. This feature enables precise control over resource consumption for background tasks, further enhancing cluster stability.

    In v8.5.6, this feature is generally available (GA).

    For more information, see [User Documentation](https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-background-tasks).

### 可观测性

- 支持多维度、多粒度定义慢查询日志的触发规则（GA）[#62959](https://github.com/pingcap/tidb/issues/62959) @[zimulala](https://github.com/zimulala) **tw@lilin90** <!--2068-->

	当前 TiDB 定位慢查询语句的主要方法是设置系统变量 tidb_slow_log_threshold，该机制触发慢日志控制粒度粗（整个实例级别全局控制，不支持会话和SQL级别精细化控制）、触发条件仅执行时间（Query_time）一种，无法满足复杂场景慢日志抓取以精细化定位问题的需求。
	
	本功能通过设置 tidb_slow_log_rules 系统变量，支持用户在实例、会话、SQL级别定义多维度（如 Query_time、Digest、Mem_max、KV_total 等等）的慢查询日志抓取规则，实现更灵活的精细化控制。

	在 v8.5.6 中，该功能成为正式功能（GA）。
	
	更多信息，请参考 [用户文档](/identify-slow-queries.md)。

- TOP SQL 增加网络流量和逻辑IO 数据（GA）[#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87) **tw@qiancai** <!--2398-->

	当前 TiDB TOP SQL 中仅包含 CPU 的相关指标数据，在遇到复杂情况时不利于排查问题。
	
	本功能在 Top SQL 设置中增加开启 **TiKV 网络I0 采集（多维度）**，方便用户进一步查看指定 TiKV 实例的 Network Bytes、Logical IO Bytes 等指标，并按 By Query、By Table、By DB 或 By Region 维度进行聚合分析。

	在 v8.5.6 中，该功能成为正式功能（GA）。

    更多信息，请参考 [用户文档](/dashboard/top-sql.md)。

### SQL

- Support column-level privilege management [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) @[fzzf678](https://github.com/fzzf678) **tw@hfxsd** <!--2332-->

    Before v8.5.6, TiDB privilege control covers the database and table levels and does not support granting or revoking privileges on specific columns, unlike MySQL. As a result, you cannot restrict users to access only a subset of sensitive columns in a table.

    Starting from v8.5.6, TiDB supports column-level privilege management. You can use the `GRANT` and `REVOKE` statements to manage privileges on specific columns. TiDB performs privilege checks based on column-level privileges during query processing and execution plan construction, enabling finer-grained access control and better support for sensitive data isolation and the principle of least privilege.

    For more information, see the [user documentation](https://docs.pingcap.com/tidb/v8.5/column-privilege-management).
  
 - Support table aliases referenced in the `FOR UPDATE OF` clause [#65532](https://github.com/pingcap/tidb/pull/65532) @[cryo-zd](https://github.com/cryo-zd) **tw@lilin90** <!--2350-->

    Before v8.5.6, when a `SELECT ... FOR UPDATE OF <table>` statement referenced a table alias in the locking clause, TiDB could fail to resolve the alias correctly and return a `table not exists` error even though the alias was valid.

    Starting from v8.5.6, TiDB supports table aliases in the `FOR UPDATE OF` clause. TiDB can now correctly resolve the locking target from the `FROM` clause, including aliased tables, so that row locks are applied as expected. This improves MySQL compatibility and makes `SELECT ... FOR UPDATE OF` statements more reliable in queries that use table aliases.

    For more information, see the user documentation. 
  
### DB operations

- Support specifying the maximum number of nodes for Distributed eXecution Framework (DXF) tasks [#58937](https://github.com/pingcap/tidb/pull/58937) @[tangenta](https://github.com/tangenta) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--2406-->

    Before v8.5.6, TiDB does not provide a way to limit the number of nodes used by a distributed execution task. When you want to control resource usage for DXF, TiDB does not provide a dedicated option to constrain the maximum node count.

    Starting from v8.5.6, TiDB introduces the `tidb_max_dist_task_nodes` system variable to specify the maximum number of TiDB nodes used by a DXF task, enabling better resource control and workload-based tuning.

    For more information, see the [user documentation](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-new-in-v856).

### Data Migration

- (dup): release-9.0.0.md > # Data migration * Migrate sync-diff-inspector from `pingcap/tidb-tools` to `pingcap/tiflow` repository [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## Compatibility Changes

For TiDB clusters newly deployed in v8.5.5 (that is, not upgraded from versions earlier than v8.5.4), you can smoothly upgrade to v8.5.6. Most changes in v8.5.6 are safe for routine upgrades, but this release also includes several behavior changes, MySQL compatibility adjustments, system variable updates, configuration parameter updates, and system table changes. Before upgrading, make sure to carefully review this section.

### Behavior changes

### MySQL compatibility

- Starting from v8.5.6, TiDB supports the MySQL-compatible column-level privilege management mechanism. You can grant or revoke `SELECT`, `INSERT`, `UPDATE`, and `REFERENCES` privileges for specific columns at the table level. For more information, see [Column-Level Privilege Management](https://docs.pingcap.com/tidb/v8.5/column-privilege-management).

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_service_scope`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_service_scope-new-in-v740)   | Modified  | Starting from v8.5.6 and v9.0.0, the value of this variable is case-insensitive. TiDB converts the input value to lowercase for storage and comparison. |
| [`tidb_max_dist_task_nodes`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-new-in-v856)  | Newly added  | defines the maximum number of TiDB nodes that the Distributed eXecution Framework (DXF) tasks can use. The default value is `-1`, which indicates that automatic mode is enabled. In automatic mode, TiDB dynamically calculates the value as `min(3, tikv_nodes / 3)`, where `tikv_nodes` represents the number of TiKV nodes in the cluster.  |
| [`tidb_opt_join_reorder_through_sel`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_join_reorder_through_sel-new-in-v856)  | Newly added | improves join reorder optimization for certain multi-table join queries. If you set it to `ON` and safety conditions are met, the optimizer evaluates `Selection` conditions that appear between consecutive join operators together with join order candidates. During join tree reconstruction, the optimizer pushes these conditions to more appropriate positions whenever possible, allowing more tables to participate in join order optimization.  |
| [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-new-in-v856)  | Newly added | controls the maximum number of slow query log entries that can be written per TiDB node per second. <ul><li>A value of `0` means there is no limit on the number of slow query log entries written per second. </li><li>A value greater than `0` means TiDB writes at most the specified number of slow query log entries per second. Any excess log entries are discarded and not written to the slow query log file.</li></ul>|
| [`tidb_slow_log_rules`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_rules-new-in-v856)  | Newly added | defines the triggering rules for slow query logs. It supports combining multi-dimensional metrics to provide more flexible and fine-grained logging. |
|   |   |   |
|   |   |   |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|  | |  |
|  | |  |
|  | |  |

## Improvements

+ TiDB <!--tw@qiancai: 5 notes-->

    - Improve plan selection for queries with `IN` predicates on index prefix columns. TiDB can now use merge sort to preserve order for `ORDER BY ... LIMIT` queries, reducing unnecessary scans and improving performance. [#63449](https://github.com/pingcap/tidb/issues/63449) [#34882](https://github.com/pingcap/tidb/issues/34882) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd** <!--2414-->
    - Enhanced slow query log control by supporting [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules-new-in-v900) for targeted slow query log output based on combinations of multiple metrics, [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec-new-in-v900) for limiting the number of slow query log entries per second, and the [`WRITE_SLOW_LOG`](/identify-slow-queries.md#related-hint) hint for forcing specified SQL statements to be recorded in the slow query log [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala)
    - Enhanced [Top SQL](/dashboard/top-sql.md) for resource analysis by supporting Top `5`, `20`, or `100` queries, hotspot analysis sorted by CPU, network traffic, or logical I/O, and aggregated analysis by `Query`, `Table`, `DB`, or `Region` on TiKV instances [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)
    - 新增 DXF 的 max_node_count 配置项支持 [#66376](https://github.com/pingcap/tidb/pull/66376)@[D3Hunter](https://github.com/D3Hunter)
    - 调整部分 stats 相关日志为 warning 级别 [#58315](https://github.com/pingcap/tidb/pull/58315)@[hawkingrei](https://github.com/hawkingrei)
    - 调整 tidb_analyze_column_options 默认值为 all [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe)

+ TiKV <!--tw@qiancai: 4 notes-->

    - Add MVCC-read-aware load-based compaction to prioritize regions with heavy MVCC read overhead. [#19133](https://github.com/tikv/tikv/issues/19133) @[mittalrishabh](https://github.com/mittalrishabh)
    - Optimize stale-range cleanup during scaling by deleting stale keys directly instead of ingesting SST files, reducing latency impact. [#18042](https://github.com/tikv/tikv/issues/18042) @[LykxSassinator](https://github.com/LykxSassinator)
    - Make default gRPC raft connection and concurrency settings scale with CPU quota to improve resource utilization. [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - Add Top SQL support for collecting network traffic and logical I/O information to help diagnose SQL performance issues. [#18815](https://github.com/tikv/tikv/issues/18815) @[yibin87](https://github.com/yibin87)

+ PD <!--tw@Oreoxmt: 1 note-->

    - Return `404` instead of `200` when deleting a non-existent label [#10089](https://github.com/tikv/pd/issues/10089) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.5.7.md > Improvements> PD - Reduce unnecessary error logs [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM) <!--tw@lilin90: 2 notes-->

        - Support migrating data from MySQL 8.4 as a data source. The compatibility level for MySQL 8.4 is upgraded from "Incompatible" to "Experimental" [#11020](https://github.com/pingcap/tiflow/issues/11020) @[dveeden](https://github.com/dveeden)
        - 在 DM syncer 中新增外键因果依赖支持，确保多 worker 场景下行变更按照父表至子表的外键顺序执行 [#12552](https://github.com/pingcap/tiflow/pull/12552) @[OliverS929](https://github.com/OliverS929)

    + TiDB Lightning

    + Dumpling <!--tw@Oreoxmt: 1 note-->

        - Support exporting data from MySQL 8.4 by adopting the updated MySQL binary log terminology [#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden)

    + TiUP

## Bug Fixes

+ TiDB <!--tw@lilin90: the following 7 notes-->

    - Fix the issue that upgrading from release-8.5-20250606-v8.5.2 to upstream release-8.5 can skip PITR metadata upgrades and cause PITR operations to fail. [#66994](https://github.com/pingcap/tidb/issues/66994) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that after EXCHANGE PARTITION, non-unique or nullable unique global indexes on non-clustered partitioned tables can become inconsistent and return incomplete results. [#65289](https://github.com/pingcap/tidb/issues/65289) @[mjonss](https://github.com/mjonss)
    - Support column-level privileges in GRANT and REVOKE. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Improve the performance of privilege updates such as GRANT and REVOKE in deployments with large numbers of privilege entries. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that KILL QUERY incorrectly kills idle connections. [#65447](https://github.com/pingcap/tidb/issues/65447) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that column-level privilege checks can be incorrect for JOIN ... USING, NATURAL JOIN, and INSERT ... ON DUPLICATE KEY UPDATE. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Improve privilege-check performance for deployments with many column-level privilege entries. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) <!--tw@hfxsd: the following 8 notes-->
    - Add `cluster_id` to `mysql.tidb`, enabling external tools to determine whether two TiDB instances belong to the same cluster [#59476](https://github.com/pingcap/tidb/issues/59476) @[YangKeao](https://github.com/YangKeao)
    - Improve slow query log readability by outputting non-printable prepared statement arguments as hexadecimal values [#65383](https://github.com/pingcap/tidb/issues/65383) @[dveeden](https://github.com/dveeden)
    - Fix the issue that the value of `tidb_service_scope` is not converted to lowercase when set [#66749](https://github.com/pingcap/tidb/issues/66749) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that affinity tables are not displayed after TiDB restarts [#66284](https://github.com/pingcap/tidb/issues/66284) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the Stats Healthy metric displays inaccurately because system tables are not excluded from the stats cache [#64080](https://github.com/pingcap/tidb/issues/64080) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that statistics might not be updated due to abnormal updates of `modify_count` [#65426](https://github.com/pingcap/tidb/issues/65426) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that a pessimistic transaction might be unexpectedly rolled back due to a keep-alive mechanism failure when its first statement acquires locks in fair locking mode [#66571](https://github.com/pingcap/tidb/issues/66571) @[MyonKeminta](https://github.com/MyonKeminta)

+ TiKV <!--tw@Oreoxmt: 7 notes-->

    - Fix the issue that a memory leak occurs in crossbeam skiplist [#19285](https://github.com/tikv/tikv/issues/19285) @[ekexium](https://github.com/ekexium)
    - Fix the issue that global indexes on non-unique columns of partitioned tables might become inconsistent and return incorrect results in some cases [#19262](https://github.com/tikv/tikv/issues/19262) @[mjonss](https://github.com/mjonss)
    - Fix the issue that stalled coprocessor snapshot retrieval might occupy unified read pool workers until request deadlines expire, delaying other read requests [#18491](https://github.com/tikv/tikv/issues/18491) @[AndreMouche](https://github.com/AndreMouche)
    - Fix the issue that follower replica reads might remain blocked on disk-full TiKV nodes by rejecting read-index requests on disk-full followers [#19201](https://github.com/tikv/tikv/issues/19201) @[glorv](https://github.com/glorv)
    - Fix the issue that resolved-ts task backlogs might cause OOM when the resolved-ts worker is busy [#18359](https://github.com/tikv/tikv/issues/18359) @[overvenus](https://github.com/overvenus)
    - Fix the issue that long-tail follower read latency might occur during leader transfer by retrying read-index requests sooner and adding a dedicated retry interval setting [#18417](https://github.com/tikv/tikv/issues/18417) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that ingest latency spikes might occur in large clusters by increasing the default value of `rocksdb.max-manifest-file-size` from 128 MiB to 256 MiB [#18996](https://github.com/tikv/tikv/issues/18996) @[glorv](https://github.com/glorv)
    - (dup): release-5.1.4.md > Bug fixes> TiKV - Fix the rare data inconsistency issue when retrying a prewrite request in pessimistic transactions [#11187](https://github.com/tikv/tikv/issues/11187)

+ PD <!--tw@hfxsd: 2 notes-->

    - Fix a panic issue that might occur when executing `DISTRIBUTE TABLE` in scenarios with a large number of Merge Region operators [#10292](https://github.com/tikv/pd/pull/10292) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that configuring Store Limit might not take effect immediately [#10108](https://github.com/tikv/pd/issues/10108) @[okJiang](https://github.com/okJiang)

+ TiFlash <!--tw@hfxsd: 3 notes-->

    - Fix a potential data inconsistency issue between TiFlash and TiKV after executing a DDL statement to remove the `NOT NULL` constraint of a column [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the Raft throughput metric in the Grafana dashboard might display an abnormally large value [#10701](https://github.com/pingcap/tiflash/issues/10701) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix an issue that the Join result might be incorrect when the Runtime Filter is enabled and the Join Keys have inconsistent data types [#10699](https://github.com/pingcap/tiflash/issues/10699) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR) <!--tw@lilin90: 4 notes-->

        - 修复 log backup 的 flush_ts 可能为 0 的问题 [#19406](https://github.com/tikv/tikv/issues/19406) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 BR 在使用 GCP S3 API server 进行 multipart upload 时因缺少 `Content-Length` 头而失败的问题 [#19352](https://github.com/tikv/tikv/issues/19352) @[Leavrth](https://github.com/Leavrth)
        - 修复 BR `restore point` 可能长时间卡在 `waiting for schema info finishes reloading` 并在 15 分钟后超时失败的问题 [#66110](https://github.com/pingcap/tidb/issues/66110) @[kennytm](https://github.com/kennytm)
        - 修复 BR 在恢复带有 `SHARD_ROW_ID_BITS`、`PRE_SPLIT_REGIONS` 和 `merge_option` 属性的表时无法正确预分裂 Region 的问题 [#65060](https://github.com/pingcap/tidb/issues/65060) @[JoyC-dev](https://github.com/JoyC-dev)

    + TiCDC <!--tw@Oreoxmt: 4 notes-->

        - Fix the issue that changefeeds might repeatedly create invalid dispatchers after the server restarts [#4452](https://github.com/pingcap/ticdc/issues/4452) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the issue that table renaming operations cannot be performed normally when the upstream TiDB version is v8.1.x or earlier [#4392](https://github.com/pingcap/ticdc/issues/4392) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that TiKV might crash during data scanning when CDC is enabled [#19404](https://github.com/tikv/tikv/issues/19404) @[wk989898](https://github.com/wk989898)
        - Support Azure Managed Identity authentication for azblob sinks and fix the issue that uploads to cloud storage might get stuck [#3093](https://github.com/pingcap/ticdc/issues/3093) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Data Migration (DM) <!--tw@qiancai: 3 notes-->

        - 修复 DM 在 binlog rotate 事件时全局 checkpoint 位置未推进的问题 [#12525](https://github.com/pingcap/tiflow/pull/12525) @[OliverS929](https://github.com/OliverS929)
        - 修复含外键约束的表在 DM safe-mode 下的异常行为，移除 UPDATE 改写中多余的 DELETE 操作并避免触发外键级联 [#12541](https://github.com/pingcap/tiflow/pull/12541) @[OliverS929](https://github.com/OliverS929)
        - 修复 DM validator 对 UNSIGNED 列误报校验错误的问题 [#12555](https://github.com/pingcap/tiflow/pull/12555) @[OliverS929](https://github.com/OliverS929)

    + TiDB Lightning

    + Dumpling <!--tw@qiancai: 1 note-->

        - 修复 Dumpling 与 MySQL 8.4 的兼容性问题 [#65131](https://github.com/pingcap/tidb/pull/65131) @[dveeden](https://github.com/dveeden)

---
title: TiDB 8.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.1.0.
---

# TiDB 8.1.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.1.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

TiDB 8.1.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 7.5.0, 8.1.0 includes new features, improvements, and bug fixes released in [7.6.0-DMR](/releases/release-7.6.0.md) and [8.0.0-DMR](/releases/release-8.0.0.md). When you upgrade from 7.5.x to 8.1.0, you can download the [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v7.6-to-v8.1-en-release-notes.pdf) to view all release notes between the two LTS versions. The following table lists some highlights from 7.6.0 to 8.1.0:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="5">Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/br-snapshot-guide#restore-cluster-snapshots">Acceleration of cluster snapshot restore speed</a> (GA in v8.0.0)</td>
    <td>With this feature, BR can fully leverage the scale advantage of a cluster, enabling all TiKV nodes in the cluster to participate in the preparation step of data restores. This feature can significantly improve the restore speed of large datasets in large-scale clusters. Real-world tests show that this feature can saturate the download bandwidth, with the download speed improving by 8 to 10 times, and the end-to-end restore speed improving by approximately 1.5 to 3 times.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/ddl-v2">Achieve up to 10 times faster for creating tables in batch</a> (experimental, introduced in v7.6.0)</td>
    <td>With the implementation of the new DDL architecture in v7.6.0, the performance of batch table creation has witnessed a remarkable improvement, up to 10 times faster. This substantial enhancement drastically reduces the time needed for creating numerous tables. This acceleration is particularly noteworthy in SaaS scenarios, where the prevalence of high volumes of tables, ranging from tens to hundreds of thousands, is a common challenge.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Use Active PD Followers to enhance PD's Region information query service</a> (experimental, introduced in v7.6.0)</td>
    <td>TiDB v7.6.0 introduces an experimental feature "Active PD Follower", which allows PD followers to provide Region information query services. This feature improves the capability of the PD cluster to handle <code>GetRegion</code> and <code>ScanRegions</code> requests in clusters with a large number of TiDB nodes and Regions, thereby reducing the CPU pressure on the PD leader.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_dml_type-new-in-v800">Bulk DML for much larger transactions</a> (experimental, introduced in v8.0.0)</td>
    <td>Large batch DML jobs, such as extensive cleanup jobs, joins, or aggregations, can consume a significant amount of memory and have previously been limited at very large scales. Bulk DML (<code>tidb_dml_type = "bulk"</code>) is a new DML type for handling large batch DML tasks more efficiently while providing transaction guarantees and mitigating OOM issues. This feature differs from import, load, and restore operations when used for data loading.</td>
  </tr>
  <tr>
    <td>Enhance the stability of caching the schema information when there is a massive number of tables (experimental, introduced in v8.0.0)</td>
    <td>SaaS companies using TiDB as the system of record for their multi-tenant applications often need to store a substantial number of tables. In previous versions, handling table counts in the order of a million or more was feasible, but it had the potential to degrade the overall user experience. TiDB v8.0.0 improves the situation with the following enhancements:
  <ul>
    <li>Introduce a new <a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_schema_cache_size-new-in-v800">schema information caching system</a>, which provides a cache strategy based on the Least Recently Used (LRU) algorithm for table metadata. It prioritizes storing the metadata of frequently accessed tables in the cache, thereby reducing memory usage in scenarios with a large number of tables.</li>
    <li>Implement a <a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">priority queue</a> for <code>auto analyze</code>, making the process less rigid and enhancing stability across a wider array of tables.</li>
  </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="5">Reliability and availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/tidb-global-sort">Global Sort</a> (GA in v8.0.0) **tw@qiancai**</td>
    <td>The Global Sort feature aims to improve the stability and efficiency of <code>IMPORT INTO</code> and <code>CREATE INDEX</code>. By globally sorting the data to be processed, this feature improves the stability, controllability, and scalability of data writing to TiKV, consequently enhancing the user experience and service quality of data import and index creation. With global sorting enabled, each <code>IMPORT INTO</code> or <code>CREATE INDEX</code> statement now supports importing or adding indexes for up to 40 TiB of data.
</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/sql-plan-management#cross-database-binding">Cross-database SQL binding</a> (introduced in v7.6.0)</td>
    <td>When managing hundreds of databases with the same schema, it is often necessary to apply SQL bindings across these databases. For example, in SaaS or PaaS data platforms, each user typically operates separate databases with the same schema and runs similar SQL queries on them. In this case, it is impractical to bind SQL for each database one by one. TiDB v7.6.0 introduces cross-database SQL bindings that enable matching bindings across all schema-equivalent databases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/tiproxy-overview">Support TiProxy</a> (GA in v8.0.0)</td>
    <td>Full support for the TiProxy service, easily deployable via deployment tooling, to manage and maintain connections to TiDB so that they live through rolling restarts, upgrades, or scaling events.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.1/dm-compatibility-catalog">Data Migration (DM) officially supports MySQL 8.0</a> (GA in v7.6.0)</td>
    <td>Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).</td>
  </tr>
  <tr>
    <td>TiDB resource control supports <a href="https://docs.pingcap.com/tidb/v8.1/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">managing queries that consume more resources than expected</a> (GA) **tw@lilin90** </td>
    <td>Through the rules of resource groups, TiDB can automatically identify queries that consume more resources than expected, and then limit or cancel these queries. Even if the queries are not identified by the rules, you can still manually add query characteristics and take corresponding measures to reduce the impact of the sudden query performance problem on the entire database.</td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td>Support monitoring index usage statistics (introduced in v8.0.0)</td>
    <td>Proper index design is a crucial prerequisite to maintaining database performance. TiDB v8.0.0 introduces the <a href="https://docs.pingcap.com/tidb/v8.1/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> table and the <a href="https://docs.pingcap.com/tidb/v8.1/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a> view to provide usage statistics of indexes. This feature helps you assess the efficiency of indexes in the database and optimize the index design.</td>
  </tr>
  <tr>
    <td rowspan="3">Data Migration</td>
    <td>TiCDC supports <a href="https://docs.pingcap.com/tidb/v8.1/ticdc-simple-protocol">the Simple protocol</a> (introduced in v8.0.0)</td>
    <td>TiCDC introduces a new protocol, the Simple protocol. This protocol provides in-band schema tracking capabilities by embedding table schema information in DDL and BOOTSTRAP events.</td>
  </tr>
  <tr>
    <td>TiCDC supports <a href="https://docs.pingcap.com/tidb/v8.1/ticdc-debezium">the Debezium format protocol</a> (introduced in v8.0.0)</td>
    <td>TiCDC introduces a new protocol, the Debezium protocol. TiCDC can now publish data change events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
  <tr>
    <td>TiCDC supports <a href="https://docs.pingcap.com/tidb/v8.1/ticdc-client-authentication.md">client authentication</a> (introduced in v8.1.0) **tw@Oreoxmt**</td>
    <td>TiCDC supports client authentication using mutual Transport Layer Security (mTLS) or TiDB username and password. This feature enables CLI or OpenAPI clients to authenticate their connections to TiCDC.</td>
  </tr>
</tbody>
</table>

## Feature details

### Reliability

* Support managing queries that consume more resources than expected (GA) [#43691](https://github.com/pingcap/tidb/issues/43691) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1447-->

    Sudden SQL query performance problems can cause a decline in overall database performance, which is the most common challenge to database stability. The reasons for these problems are diverse, such as untested new SQL statements, drastic changes in data volume, and sudden changes in execution plans. These problems are difficult to avoid completely at the source. In earlier versions, TiDB has added the capability to manage queries that consume more resources than expected to quickly reduce the impact of sudden query performance problems. This feature becomes generally available in v8.1.0.

    You can set the maximum execution time for a query in a resource group. When the execution time of a query exceeds the set value, the priority of the query is automatically reduced or the query is canceled. You can also set immediately matching identified queries through text or execution plans within a period of time, to avoid excessive resource consumption during the identification phase when the concurrency of problematic queries is too high.

    TiDB also supports the manual marking of queries. By using the [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) command, you can mark queries based on the SQL text, SQL Digest, or execution plan. The queries that match the mark can be downgraded or canceled, achieving the purpose of adding a SQL blocklist.

    The automatic management capability of queries that consume more resources than expected provides users with an effective means to quickly mitigate the impact of query problems on overall performance before the root cause is identified, thereby improving the stability of the database.

    For more information, see [documentation](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

### SQL

* Support using more expressions to set default column values when creating a table (GA) [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala) **tw@hfxsd** <!--1794-->

    Before v8.0.0, when you create a table, the default value of a column is limited to strings, numbers, dates, and certain expressions. Starting from v8.0.0, you can use more expressions as the default column values. For example, you can set the default value of a column to `DATE_FORMAT`. This feature helps you meet more diverse requirements. In v8.1.0, this feature becomes GA.
    
    Starting from v8.1.0, you can use expressions as default values when adding columns by `ADD COLUMN`.

    For more information, see [documentation](/data-type-default-values.md#specify-expressions-as-default-values).

### DB operations

* Enable the TiDB Distributed eXecution Framework (DXF) by default to enhance the performance and stability of `ADD INDEX` or `IMPORT INTO` tasks in parallel execution [#52441](https://github.com/pingcap/tidb/issues/52441) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai**

    The DXF becomes generally available (GA) in v7.5.0, but it is disabled by default. This means that an `ADD INDEX` or `IMPORT INTO` task is executed only by one TiDB node by default.

    Starting from v8.1.0, TiDB enables this feature by default ([`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) defaults to `ON`). When enabled, the DXF can schedule multiple TiDB nodes to execute the same `ADD INDEX` or `IMPORT INTO` task in parallel, fully utilizing the resources of the TiDB cluster and greatly improving the performance of these tasks. In addition, you can linearly improve the performance of `ADD INDEX` and `IMPORT INTO` tasks by adding TiDB nodes and configuring [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) for the newly added nodes.

    For more information, see [documentation](/tidb-distributed-execution-framework.md).

### Security

* Enhance TiDB log desensitization (GA) [#52364](https://github.com/pingcap/tidb/issues/52364) @[xhebox](https://github.com/xhebox) **tw@hfxsd** <!--1817-->

    The enhanced TiDB log desensitization supports removing sensitive data when users view logs, implemented by marking SQL text information in log files. You can control whether to mark log information to enable secure use of TiDB logs in different scenarios, enhancing the security and flexibility of using log desensitization. To use this feature, set the system variable `tidb_redact_log` to `MARKER`, and then the SQL text in TiDB's runtime logs are marked. In addition, you can use the `collect-log` subcommand on the TiDB server to remove marked sensitive data from the logs and display the logs in a secure manner. You can also remove all markers and get the normal logs. This feature became generally available in v8.1.0.

    For more information, see [documentation](/system-variables.md#tidb_redact_log).

### Data migration

* Support the `IMPORT INTO ... FROM SELECT` syntax (GA) [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1791-->

    Before v8.0.0, importing query results into a target table could only be done using the `INSERT INTO ... SELECT` statement, which is relatively inefficient in some large dataset scenarios. In v8.0.0, TiDB introduces `IMPORT INTO ... FROM SELECT` as an experimental feature, which enables you to import the results of a `SELECT` query into an empty TiDB target table. It achieves up to 8 times the performance of `INSERT INTO ... SELECT` and significantly reduces the import time. In addition, you can use `IMPORT INTO ... FROM SELECT` to import historical data queried with [`AS OF TIMESTAMP`](/as-of-timestamp.md).

    In v8.1.0, the `IMPORT INTO ... FROM SELECT` syntax becomes generally available (GA), enriching the functionality scenarios of the `IMPORT INTO` statement.

    For more information, see [documentation](/sql-statements/sql-statement-import-into.md).

* TiDB Lightning simplifies conflict resolution strategies and supports handling conflicting data using the `replace` strategy (GA) [#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001) **tw@qiancai** <!--1795-->

    Before v8.0.0, TiDB Lightning has [one data conflict resolution strategy](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md#conflict-detection) for the logical import mode and [two data conflict resolution strategies](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection) for the physical import mode, which are not easy to understand and configure.

    In v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) parameter (experimental), and simplifies the configuration of this parameter. In addition, in the physical import mode, the `replace` strategy supports retaining the latest data and overwriting the old data when the import detects data with primary key or unique key conflicts. In v8.1.0, the capability to handle conflicting data with the `replace` strategy becomes generally available (GA).

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md).

* TiCDC supports client authentication [#10636](https://github.com/pingcap/tiflow/issues/10636) @[CharlesCheung96](https://github.com/CharlesCheung96) **tw@Oreoxmt** <!--1717-->

    In v8.1.0, TiCDC supports client authentication when you are using the TiCDC CLI or OpenAPI. This feature enables you to configure TiCDC to require client authentication using client certificates, thereby establishing mutual Transport Layer Security (mTLS). Additionally, you can configure authentication based on TiDB username and password.

    For more information, see [documentation](/ticdc/ticdc-client-authentication.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.0.0 to the current version (v8.1.0). If you are upgrading from v7.6.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|        |                              |      |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) | Modified | Changes the default value from `OFF` to `ON`. This means that Distributed eXecution Framework (DXF) is enabled by default, which fully utilizes the resources of the TiDB cluster and greatly improves the performance of `ADD INDEX` and `IMPORT INTO` tasks. If you want to upgrade a cluster with the DXF enabled to v8.1.0 or later, disable the DXF (by setting `tidb_enable_dist_task` to `OFF`) before the upgrade, which avoids `ADD INDEX` operations during the upgrade causing data index inconsistency. After the upgrade, you can manually enable the DXF. |
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) | Modified  | Changes the optional value from  "" or `background` to a string with a length of up to 64 characters, which enables you to control the service scope of each TiDB node more flexibly. Valid characters include digits `0-9`, letters `a-zA-Z`, underscores `_`, and hyphens `-`. The Distributed eXecution Framework (DXF) determines which TiDB nodes can be scheduled to execute distributed tasks based on the value of this variable. For specific rules, see [Task scheduling](/tidb-distributed-execution-framework.md#task-scheduling). |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Modified | Changes the default value from `9223372036854775807` to `10000` to quickly interrupt abnormal tasks so that you can make corresponding adjustments as soon as possible. This saves time and computational resources by avoiding the scenario where a large amount of conflicting data is discovered after the import, caused by abnormal data sources or incorrect table schema definitions. |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration) | Modified | Starting from v8.1.0, there is no need to configure `conflict.max-record-rows` manually, because TiDB Lightning automatically assigns the value of `conflict.max-record-rows` with the value of `conflict.threshold`, regardless of the user input. `conflict.max-record-rows` will be deprecated in a future release. |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### Others

## Offline package changes

## Deprecated features

* It is planned to redesign [the auto-evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
* The TiDB Lightning parameter `conflict.max-record-rows` is scheduled for deprecation in a future release and will be subsequently removed. This parameter will be replaced by `conflict.threshold`, which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
* Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Improvements

+ TiDB
  <!--tw@Oreoxmt 7 -->
    - Improve the MySQL compatibility of foreign keys displayed in the output of `SHOW CREATE TABLE` [#51837](https://github.com/pingcap/tidb/issues/51837) @[negachov](https://github.com/negachov)
    - Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Support adding multiple indexes concurrently in the ingest mode [#52596](https://github.com/pingcap/tidb/issues/52596) @[lance6716](https://github.com/lance6716)
    - Support configuring the system variable `tidb_service_scope` with various values, enhancing the utilization of the Distributed eXecution Framework [#52441](https://github.com/pingcap/tidb/issues/52441) @[ywqzzy](https://github.com/ywqzzy)
    - Enhance the handling of DNFs that are always `false` by directly ignoring such filter conditions [#40997](https://github.com/pingcap/tidb/issues/40997) @[hi-rustin](https://github.com/hi-rustin)
    - Do not support setting the system variable `tidb_auto_analyze_ratio` to `0` [#51582](https://github.com/pingcap/tidb/issues/51582) @[hi-rustin](https://github.com/hi-rustin)
    - Support using Optimizer Fix Controls to remove the limitation that the optimizer does not automatically select Index Merge when the query can select a single index scan method other than a full table scan [#52869](https://github.com/pingcap/tidb/issues/52869) @[time-and-fate](https://github.com/time-and-fate)
    - Add the `total_kv_read_wall_time` metric to the column `execution info` of Coprocessor operators [#28937](https://github.com/pingcap/tidb/issues/28937) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.1.5.md > Improvements> TiDB - Add a timeout mechanism for LDAP authentication to avoid the issue of resource lock (RLock) not being released in time [#51883](https://github.com/pingcap/tidb/issues/51883) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - (dup): release-6.5.9.md > Improvements> TiKV - Avoid performing IO operations on snapshot files in raftstore threads to improve TiKV stability [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)

+ PD
  <!--tw@qiancai 1 -->
    - 优化调度 operator 相关逻辑竞争锁的开销 [#7897](https://github.com/tikv/pd/issues/7897) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)
      <!--tw@hfxsd 2 -->
        - (dup): release-7.1.5.md > Improvements> Tools> Backup & Restore (BR) - Add PITR integration test cases to cover compatibility testing for log backup and adding index acceleration [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > Improvements> Tools> Backup & Restore (BR) - Remove the invalid verification for active DDL jobs when log backup starts [#52733](https://github.com/pingcap/tidb/issues/52733) @[Leavrth](https://github.com/Leavrth)
        - Add test cases to test compatibility between PITR and the acceleration of adding indexes feature [#51988](https://github.com/pingcap/tidb/issues/51988) @[Leavrth](https://github.com/Leavrth)
        - BR cleans up empty SST files during data recovery [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)

    + TiCDC
      <!--tw@hfxsd 2 -->
        - Improve memory stability during data recovery using redo log to reduce the probability of OOM [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Significantly improve the stability of data replication in transaction conflict scenarios, with up to 10 times performance improvement [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Dumpling

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Binlog

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB
  <!--tw@Oreoxmt 以下 12 条 -->
    - Fix the issue that executing SQL statements containing tables with multi-valued indexes might return the `Can't find a proper physical plan for this query` error [#49438](https://github.com/pingcap/tidb/issues/49438) @[qw4990](https://github.com/qw4990)
    - Fix the issue that auto analyze gets stuck after an OOM error occurs [#51993](https://github.com/pingcap/tidb/issues/51993) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that after using BR to restore a table that has no statistics, the statistics health is still 100% [#29769](https://github.com/pingcap/tidb/issues/29769) @[winoros](https://github.com/winoros)
    - Fix the issue that TiDB creates statistics for system tables during upgrade [#52040](https://github.com/pingcap/tidb/issues/52040) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that auto analyze is triggered before the initialization of statistics finishes [#52346](https://github.com/pingcap/tidb/issues/52346) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by auto analyze exceeds the limit [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the TiDB synchronously loading statistics mechanism retries to load empty statistics indefinitely and prints the `fail to get stats version for this histogram` log [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that expressions containing different collations might cause the query to panic when the new framework for collations is disabled [#52772](https://github.com/pingcap/tidb/issues/52772) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the `CPS by type` metric displays incorrect values [#52605](https://github.com/pingcap/tidb/issues/52605) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the null pointer error occurs when querying `INFORMATION_SCHEMA.TIKV_REGION_STATUS` [#52013](https://github.com/pingcap/tidb/issues/52013) @[JmPotato](https://github.com/JmPotato)
    - Fix the incorrect error message displayed when an invalid default value is specified for a column [#51592](https://github.com/pingcap/tidb/issues/51592) @[danqixu](https://github.com/danqixu)
    - Fix the issue that adding indexes in the ingest mode might cause inconsistent data index in some corner cases [#51954](https://github.com/pingcap/tidb/issues/51954) @[lance6716](https://github.com/lance6716)
  <!--tw@lilin90 以下 18 条 -->
    - 修复了恢复含有外键的表时，DDL 卡住的问题 [#51838](https://github.com/pingcap/tidb/issues/51838) @[YangKeao](https://github.com/YangKeao)
    - 修复了加索引期间 TiDB 网络隔离导致加索引失败的问题 [#51846](https://github.com/pingcap/tidb/issues/51846) @[ywqzzy](https://github.com/ywqzzy)
    - 修复了重命名索引后再添加同名索引时的报错问题 [#51431](https://github.com/pingcap/tidb/issues/51431) @[lance6716](https://github.com/lance6716)
    - 修复了添加索引期间升级集群导致的数据索引不一致问题 [#52411](https://github.com/pingcap/tidb/issues/52411) @[tangenta](https://github.com/tangenta)
    - 修复了开启分布式框架后为大数据量表添加索引不成功的问题 [#52640](https://github.com/pingcap/tidb/issues/52640) @[tangenta](https://github.com/tangenta)
    - 修复了并发添加索引时报 “文件不存在” 错误的问题 [#52475](https://github.com/pingcap/tidb/issues/52475) @[tangenta](https://github.com/tangenta)
    - 修复了添加索引失败后清理不掉临时数据的问题 [#52639](https://github.com/pingcap/tidb/issues/52639) @[lance6716](https://github.com/lance6716)
    - 修复了元数据锁在 plan cache 场景下未能阻止 DDL 推进的问题 [#51407](https://github.com/pingcap/tidb/issues/51407) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了执行 IMPORT INTO 大数据量任务时卡住的问题 [#52884](https://github.com/pingcap/tidb/issues/52884) @[lance6716](https://github.com/lance6716)
    - 修复了记录 GRPC 错误时 TIDB 意外重启的问题 [#52179](https://github.com/pingcap/tidb/issues/52179) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了 IndexHashJoin 在执行 Anti Left Outer Semi Join 计算时输出冗余数据的问题 [#52923](https://github.com/pingcap/tidb/issues/52923) @[yibin87](https://github.com/yibin87)
    - 修复了 HashJoin Probe 执行时间统计不精确的问题 [#52227](https://github.com/pingcap/tidb/issues/52227) @[windtalker](https://github.com/windtalker)
    - 修复了在分区裁剪模式为 static 情况下，使用 tablesample 返回错误结果的问题 [#52282](https://github.com/pingcap/tidb/issues/52282) @[tangenta](https://github.com/tangenta)
    - 修复 TTL 功能在非默认时区下的错误 [#51675](https://github.com/pingcap/tidb/issues/51675) @[lcwangchao](https://github.com/lcwangchao)
    - 修复监控面板中链接数的计算和显示错误 [#51889](https://github.com/pingcap/tidb/issues/51889) @[YangKeao](https://github.com/YangKeao)
    - 修复回滚改写分区 DDL 任务时，状态卡住的问题 [#51090](https://github.com/pingcap/tidb/issues/51090) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 lighting 导入后 TiDB 意外重启 [#52827](https://github.com/pingcap/tidb/issues/52827) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 TiDB `explain analyze` 结果中 `max_remote_stream` 显示不正确的问题 [#52646](https://github.com/pingcap/tidb/issues/52646) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.9.md > Bug fixes> TiDB - Fix the issue that querying the `TIDB_HOT_REGIONS` table might incorrectly return `INFORMATION_SCHEMA` tables [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.1.5.md > Bug fixes> TiDB - Fix the issue that the `EXPLAIN` statement might display incorrect column IDs in the result when statistics for certain columns are not fully loaded [#52207](https://github.com/pingcap/tidb/issues/52207) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.9.md > Bug fixes> TiDB - Fix the issue that the type returned by the `IFNULL` function is inconsistent with MySQL [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.5.md > Bug fixes> TiDB - Fix the issue that adding a unique index might cause TiDB to panic [#52312](https://github.com/pingcap/tidb/issues/52312) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - (dup): release-7.1.5.md > Bug fixes> TiKV - Fix the issue that resolve-ts is blocked when a stale Region peer ignores the GC message [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.9.md > Bug fixes> TiKV - Fix the issue that inactive Write Ahead Logs (WALs) in RocksDB might corrupt data [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)

+ PD
  <!--tw@qiancai 9 -->
    - 修复切换 PD 模式时 TSO 可能卡住的问题 [#7849](https://github.com/tikv/pd/issues/7849) @[JmPotato](https://github.com/JmPotato)
    - 修复 DR Auto Sync 监控状态显示的问题 [#7974](https://github.com/tikv/pd/issues/7974) @[lhy1024](https://github.com/lhy1024)
    - 修复检查 binary 版本时可能导致的 panic 问题 [#7978](https://github.com/tikv/pd/issues/7978) @[JmPotato](https://github.com/JmPotato)
    - 修复 TTL 参数类型转换错误的问题 [#7980](https://github.com/tikv/pd/issues/7980) @[HuSharp](https://github.com/HuSharp)
    - 修复两中心部署切换时 leader 无法迁移的问题 [#7992](https://github.com/tikv/pd/issues/7992) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - 修复 pd-ctl 标准错误重定向的问题 [#8022](https://github.com/tikv/pd/issues/8022) @[HuSharp](https://github.com/HuSharp)
    - 修复在生成 merge 调度时可能出现的 panic 问题 [#8049](https://github.com/tikv/pd/issues/8049) @[nolouch](https://github.com/nolouch)
    - 修复 `GetAdditionalInfo` 导致的 panic 问题 [#8079](https://github.com/tikv/pd/issues/8079) @[HuSharp](https://github.com/HuSharp)
    - 修复 scatter range 调度器监控显示的问题 [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-6.5.9.md > Bug fixes> PD - Fix the issue that the query result of `SHOW CONFIG` includes the deprecated configuration item `trace-region-flow` [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)
    - (dup): release-6.5.9.md > Bug fixes> PD - Fix the issue that the scaling progress is not correctly displayed [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash
  <!--tw@qiancai 2 -->
    - (dup): release-6.5.9.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic when you insert data to columns with invalid default values in non-strict `sql_mode` [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 在高并发读的情况下，可能返回瞬时不正确的结果的问题 [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，计算节点的本地缓存容量配置项的值修改后，上报 PD 的硬盘使用量不正确的问题 [#8920](https://github.com/pingcap/tiflash/issues/8920) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)
      <!--tw@hfxsd 7 -->
        - (dup): release-6.5.9.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR could not back up the `AUTO_RANDOM` ID allocation progress in a union clustered index that contains an `AUTO_RANDOM` column [#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that removing a log backup task after it is paused does not immediately restore the GC safepoint [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.1.5.md > Bug fixes> Tools> Backup & Restore (BR) - Fix a rare issue that special event timing might cause the data loss in log backup [#16739](https://github.com/tikv/tikv/issues/16739) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.1.5.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the global checkpoint of log backup is advanced ahead of the actual backup file write point due to TiKV restart, which might cause a small amount of backup data loss [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that redundant concurrency related information appears in the log during a full backup [#50837](https://github.com/pingcap/tidb/issues/50837) @[BornChanger](https://github.com/BornChanger)
        - Fix the issue that the Region fetched from PD does not have a Leader when restoring data by BR or importing data by TiDB Lightning in physical import mode [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth) 
        - Fix the issue that after pausing, stopping, and rebuilding the log backup task, the task status is normal, but the checkpoint does not advance [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR) 
        - Fix the unstable test case `TestClearCache` [#51671](https://github.com/pingcap/tidb/issues/51671) @[zxc111](https://github.com/zxc111)
        - Fix the unstable test case `TestGetMergeRegionSizeAndCount` [#52095](https://github.com/pingcap/tidb/issues/52095) @[3pointer](https://github.com/3pointer)
        - Fix the unstable integration test `br_tikv_outage` [#52673](https://github.com/pingcap/tidb/issues/52673) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the test case `TestGetTSWithRetry` takes too long to execute [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)

    + TiCDC
      <!--tw@hfxsd 7 -->
        - Fix the issue that calling the API (/api/v2/owner/resign) that evicts the TiCDC owner node causes the TiCDC task to restart unexpectedly [#10781](https://github.com/pingcap/tiflow/issues/10781) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that when the downstream Pulsar is stopped, removing the changefeed causes the normal TiCDC process to get stuck, which causes other changefeed processes to get stuck [#10629](https://github.com/pingcap/tiflow/issues/10629) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the **Ownership history** panel in Grafana is unstable [#10796](https://github.com/pingcap/tiflow/issues/10796) @[hongyunyan](https://github.com/hongyunyan)
        - Fix the issue that restarting PD might cause the TiCDC node to restart with an error [#10799](https://github.com/pingcap/tiflow/issues/10799) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that long latency in the PD disk IO causes significant latency in data replication [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the default value is not set according to the correct time zone [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that `DROP PRIMARY KEY` and `DROP UNIQUE KEY` statements are not replicated correctly [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.1.5.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC fails to execute the `Exchange Partition ... With Validation` DDL downstream after it is written upstream, causing the changefeed to get stuck [#10859](https://github.com/pingcap/tiflow/issues/10859) @[hongyunyan](https://github.com/hongyunyan)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning
      <!--tw@qiancai 4 -->
        - 修复了 lightning 导入时，因源文件存在不兼容的 SQL 而报 “no database selected” 的问题 [#51800](https://github.com/pingcap/tidb/issues/51800) @[lance6716](https://github.com/lance6716)
        - 修复了 lightning 在 server 模式下可能会打印敏感信息到日志的问题 [#36374](https://github.com/pingcap/tidb/issues/36374) @[kennytm](https://github.com/kennytm)
        - 修复了 lightning 导入期间报 “invalid store ID 0” 错误的问题 [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - 修复了 lighting 使用 replace 作为去重算法时报 “Unknown column in where clause” 错误的问题 [#52886](https://github.com/pingcap/tidb/issues/52886) @[lyzx2001](https://github.com/lyzx2001)
        - (dup): release-7.1.5.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning panics when importing an empty table of Parquet format [#52518](https://github.com/pingcap/tidb/issues/52518) @[kennytm](https://github.com/kennytm)

    + Dumpling

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Binlog

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Performance test

To learn about the performance of TiDB v8.1.0, you can refer to the [TPC-C performance test report](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-tpcc) and [Sysbench performance test report](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-sysbench) of the TiDB Dedicated cluster.

## Contributors

We would like to thank the following contributors from the TiDB community:

- [arturmelanchyk](https://github.com/arturmelanchyk) (First-time contributor)
- [CabinfeverB](https://github.com/CabinfeverB)
- [danqixu](https://github.com/danqixu) (First-time contributor)
- [imalasong](https://github.com/imalasong) (First-time contributor)
- [jiyfhust](https://github.com/jiyfhust)
- [negachov](https://github.com/negachov) (First-time contributor)
- [testwill](https://github.com/testwill)
- [yzhan1](https://github.com/yzhan1) (First-time contributor)
- [zxc111](https://github.com/zxc111) (First-time contributor)
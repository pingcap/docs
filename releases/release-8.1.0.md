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
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/br-snapshot-guide#restore-cluster-snapshots">Acceleration of cluster snapshot restore speed</a> (GA in v8.0.0)</td>
    <td>With this feature, BR can fully leverage the scale advantage of a cluster, enabling all TiKV nodes in the cluster to participate in the preparation step of data restores. This feature can significantly improve the restore speed of large datasets in large-scale clusters. Real-world tests show that this feature can saturate the download bandwidth, with the download speed improving by 8 to 10 times, and the end-to-end restore speed improving by approximately 1.5 to 3 times.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/ddl-v2">Achieve up to 10 times faster for creating tables in batch</a> (experimental, introduced in v7.6.0)</td>
    <td>With the implementation of the new DDL architecture in v7.6.0, the performance of batch table creation has witnessed a remarkable improvement, up to 10 times faster. This substantial enhancement drastically reduces the time needed for creating numerous tables. This acceleration is particularly noteworthy in SaaS scenarios, where the prevalence of high volumes of tables, ranging from tens to hundreds of thousands, is a common challenge.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Use Active PD Followers to enhance PD's Region information query service</a> (experimental, introduced in v7.6.0)</td>
    <td>TiDB v7.6.0 introduces an experimental feature "Active PD Follower", which allows PD followers to provide Region information query services. This feature improves the capability of the PD cluster to handle <code>GetRegion</code> and <code>ScanRegions</code> requests in clusters with a large number of TiDB nodes and Regions, thereby reducing the CPU pressure on the PD leader.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_dml_type-new-in-v800">Bulk DML for much larger transactions</a> (experimental, introduced in v8.0.0)</td>
    <td>Large batch DML jobs, such as extensive cleanup jobs, joins, or aggregations, can consume a significant amount of memory and have previously been limited at very large scales. Bulk DML (<code>tidb_dml_type = "bulk"</code>) is a new DML type for handling large batch DML tasks more efficiently while providing transaction guarantees and mitigating OOM issues. This feature differs from import, load, and restore operations when used for data loading.</td>
  </tr>
  <tr>
    <td>Enhance the stability of caching the schema information when there is a massive number of tables (experimental, introduced in v8.0.0)</td>
    <td>SaaS companies using TiDB as the system of record for their multi-tenant applications often need to store a substantial number of tables. In previous versions, handling table counts in the order of a million or more was feasible, but it had the potential to degrade the overall user experience. TiDB v8.0.0 improves the situation with the following enhancements:
  <ul>
    <li>Introduce a new <a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_schema_cache_size-new-in-v800">schema information caching system</a>, incorporating a lazy-loading Least Recently Used (LRU) cache for table metadata and more efficiently managing schema version changes.</li>
    <li>Implement a <a href="https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_enable_auto_analyze_priority_queue-new-in-v800">priority queue</a> for <code>auto analyze</code>, making the process less rigid and enhancing stability across a wider array of tables.</li>
  </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="5">Reliability and availability	</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tidb-global-sort">全局排序成为正式功能</a>（从 v8.0.0 开始 GA）**tw@qiancai**</td>
    <td>全局排序功能旨在提高 IMPORT INTO 和 CREATE INDEX 的稳定性与效率。通过将任务需要处理的数据进行全局排序，可以提高数据写入 TiKV 的稳定性、可控性和可扩展性，从而提供更好的数据导入与 DDL 任务的用户体验及更高质量的服务。目前已经支持 40 TiB 的数据进行导入或者添加索引。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/sql-plan-management#cross-database-binding">Cross-database SQL binding</a> (introduced in v7.6.0)</td>
    <td>When managing hundreds of databases with the same schema, it is often necessary to apply SQL bindings across these databases. For example, in SaaS or PaaS data platforms, each user typically operates separate databases with the same schema and runs similar SQL queries on them. In this case, it is impractical to bind SQL for each database one by one. TiDB v7.6.0 introduces cross-database SQL bindings that enable matching bindings across all schema-equivalent databases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tiproxy-overview">Support TiProxy</a> (GA in v8.0.0)</td>
    <td>Full support for the TiProxy service, easily deployable via deployment tooling, to manage and maintain connections to TiDB so that they live through rolling restarts, upgrades, or scaling events.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/dm-compatibility-catalog">Data Migration (DM) officially supports MySQL 8.0</a> (GA in v7.6.0)</td>
    <td>Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).</td>
  </tr>
  <tr>
    <td>TiDB resource control supports <a href="https://docs.pingcap.com/tidb/v8.1/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries">managing queries that consume more resources than expected</a> (GA) **tw@lilin90** </td>
    <td>Through the rules of resource groups, TiDB can automatically identify queries that consume more resources than expected, and then limit or cancel these queries. Even if the queries are not identified by the rules, you can still manually add query characteristics and take corresponding measures to reduce the sudden query performance problem's impact on the entire database.</td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td>Support monitoring index usage statistics (introduced in v8.0.0)</td>
    <td>Proper index design is a crucial prerequisite to maintaining database performance. TiDB v8.0.0 introduces the <a href="https://docs.pingcap.com/tidb/v8.1/information-schema-tidb-index-usage"><code>INFORMATION_SCHEMA.TIDB_INDEX_USAGE</code></a> table and the <a href="https://docs.pingcap.com/tidb/v8.1/sys-schema-unused-indexes"><code>sys.schema_unused_indexes</code></a> view to provide usage statistics of indexes. This feature helps you assess the efficiency of indexes in the database and optimize the index design.</td>
  </tr>
  <tr>
    <td rowspan="2">Data Migration</td>
    <td>TiCDC adds support for <a href="https://docs.pingcap.com/tidb/v8.1/ticdc-simple-protocol">the Simple protocol</a> (introduced in v8.0.0)</td>
    <td>TiCDC introduces a new protocol, the Simple protocol. This protocol provides in-band schema tracking capabilities by embedding table schema information in DDL and BOOTSTRAP events.</td>
  </tr>
  <tr>
    <td>TiCDC adds support for <a href="https://docs.pingcap.com/tidb/v8.1/ticdc-debezium">the Debezium format protocol</a> (introduced in v8.0.0)</td>
    <td>TiCDC introduces a new protocol, the Debezium protocol. TiCDC can now publish data change events to a Kafka sink using a protocol that generates Debezium style messages.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Performance

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Reliability

* Support managing queries that consume more resources than expected (GA) [#43691](https://github.com/pingcap/tidb/issues/43691) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1447-->

    Sudden SQL query performance problems can cause a decline in overall database performance, which is the most common challenge to database stability. The reasons for these problems are diverse, such as untested new SQL statements, drastic changes in data volume, and sudden changes in execution plans. These problems are difficult to avoid completely at the source. In earlier versions, TiDB has added the capability to manage queries that consume more resources than expected to quickly reduce the impact of sudden query performance problems. This feature becomes generally available in v8.1.0.

    You can set the maximum execution time for a query in a resource group. When the execution time of a query exceeds the set value, the priority of the query is automatically reduced or the query is canceled. You can also set immediately matching identified queries through text or execution plans within a period of time, to avoid excessive resource consumption during the identification phase when the concurrency of problematic queries is too high.

    TiDB also supports the manual marking of queries. By using the [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) command, you can mark queries based on the SQL text, SQL Digest, or execution plan. The queries that match the mark can be downgraded or canceled, achieving the purpose of adding a SQL blocklist.

    The automatic management capability of queries that consume more resources than expected provides users with an effective means to quickly mitigate the impact of query problems on overall performance before the root cause is identified, thereby improving the stability of the database.

    For more information, see [documentation](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

### Availability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### SQL

* Support using some expressions to set default column values when creating a table (GA) [#50936](https://github.com/pingcap/tidb/issues/50936) @[zimulala](https://github.com/zimulala)

    Before v8.0.0, when you create a table, the default value of a column is limited to strings, numbers, dates, and certain expressions. Starting from v8.0.0, you can use more expressions as the default column values. For example, you can set the default value of a column to `DATE_FORMAT`. This feature helps you meet more diverse requirements. In v8.1.0, this feature becomes GA.
    
    Starting from v8.1.0, you can use expressions as default values when adding columns by `ADD COLUMN`.

    For more information, see [documentation](/data-type-default-values.md#specify-expressions-as-default-values).

### DB operations

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Observability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Security

* Enhance TiDB log desensitization (GA) [#52364](https://github.com/pingcap/tidb/issues/52364) @[xhebox](https://github.com/xhebox) **tw@hfxsd** <!--1817-->

    The enhancement of TiDB log desensitization is based on marking SQL text information in log files, facilitating deleting of sensitive data when users view the logs. You can control whether to mark log information to enable secure use of TiDB logs in different scenarios, enhancing the security and flexibility of using log desensitization. To use this feature, set the system variable `tidb_redact_log` to `MARKER`. This marks the SQL text in TiDB logs. In addition, you can use the `collect-log` subcommand on the TiDB server to remove marked sensitive data from the logs and display the logs in a data-safe manner. You can also remove all markers and get the normal logs. This feature became generally available in v8.1.0.

    For more information, see [documentation](/system-variables.md#tidb_redact_log).

### Data migration

* IMPORT INTO ... FROM SELECT 语法成为正式功能（GA），丰富了 IMPORT INTO 功能场景 [#49883](https://github.com/pingcap/tidb/issues/49883) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1791-->

    在之前的 TiDB 版本中，将查询结果导入目标表只能通过 INSERT INTO ... SELECT 语句，但该语句在一些大数据量的场景中的导入效率较低。从 v8.0.0 开始，TiDB 新增支持通过 IMPORT INTO ... FROM SELECT 将 SELECT 的查询结果导入到一张空的 TiDB 目标表中，其性能最高可达 INSERT INTO ... SELECT 的 8 倍，可以大幅缩短导入所需的时间。

    此外，你还可以通过 IMPORT INTO ... FROM SELECT 导入使用 [AS OF TIMESTAMP](https://docs.pingcap.com/zh/tidb/dev/as-of-timestamp) 查询的历史数据。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/dev/sql-statement-import-into)。

* TiDB Lightning 简化冲突处理策略，同时支持以 replace 方式处理冲突数据的功能成为正式功能（GA）[#51036](https://github.com/pingcap/tidb/issues/51036) @[lyzx2001](https://github.com/lyzx2001)**tw@qiancai** <!--1795-->

    在之前的版本中，TiDB Lightning 逻辑导入模式有[一套数据冲突处理策略](https://docs.pingcap.com/zh/tidb/dev/tidb-lightning-logical-import-mode-usage#%E5%86%B2%E7%AA%81%E6%95%B0%E6%8D%AE%E6%A3%80%E6%B5%8B)，而物理导入模式有[两套数据冲突处理策略](https://docs.pingcap.com/zh/tidb/dev/tidb-lightning-physical-import-mode-usage#%E5%86%B2%E7%AA%81%E6%95%B0%E6%8D%AE%E6%A3%80%E6%B5%8B)，不易理解和配置。

    从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](https://docs.pingcap.com/zh/tidb/dev/tidb-lightning-physical-import-mode-usage#%E6%97%A7%E7%89%88%E5%86%B2%E7%AA%81%E6%A3%80%E6%B5%8B%E4%BB%8E-v800-%E5%BC%80%E5%A7%8B%E5%B7%B2%E8%A2%AB%E5%BA%9F%E5%BC%83)策略，支持通过 [conflict.strategy](https://docs.pingcap.com/zh/tidb/dev/tidb-lightning-configuration) 参数统一控制逻辑导入和物理导入模式的冲突检测策略，并简化了该参数的配置。此外，在物理导入模式下，当导入遇到主键或唯一键冲突的数据时，replace 策略支持保留最新的数据、覆盖旧的数据。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/dev/tidb-lightning-configuration)。

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
|        |                              |      |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### Others

## Offline package changes

## Deprecated features

## Improvements

## Bug fixes

## Performance test

To learn about the performance of TiDB v8.1.0, you can refer to the [TPC-C performance test report](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-tpcc) and [Sysbench performance test report](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-sysbench) of the TiDB Dedicated cluster.

## Contributors

We would like to thank the following contributors from the TiDB community:

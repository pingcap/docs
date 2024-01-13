---
title: TiDB 7.6.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.6.0.
---

# TiDB 7.6.0 Release Notes

Release date: xx xx, 202x

TiDB version: 7.6.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.6/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.6.0#version-list)

7.6.0 introduces the following key features and improvements:

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
    <td rowspan="4">Scalability and Performance<br></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/sql-plan-management#cross-database-binding">Cross-database SQL binding</a> {/* tw@Oreoxmt */}</td>
    <td>When managing hundreds of databases with the same schema, it is often necessary to apply SQL bindings across these schemas. For example, in SaaS or PaaS data platforms, each user typically operates separate databases with the same schema and runs similar SQL queries on them. In this case, it is impractical to bind SQL for each schema one by one. TiDB v7.6.0 introduces cross-database SQL bindings that enable matching bindings across all schema-equivalent databases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/br-snapshot-guide#restore-cluster-snapshots">Achieve up to 10 times faster for snapshot restore (experimental)</a> {/* tw@Oreoxmt */}</td>
    <td>BR v7.6.0 introduces an experimental coarse-grained Region scatter algorithm to prepare snapshot restores for clusters. In clusters with many TiKV nodes, this algorithm significantly improves cluster resource efficiency by more evenly distributing load across nodes and better utilizing per-node network bandwidth. In several real-world cases, this improvement accelerates restore speed by about up to 10 times.</td>
  </tr>
  <tr>
    <td><a href="">Achieve up to 10 times faster for creating tables in batch (experimental)</a>  {/* tw@hfxsd */}</td>
    <td>With the implementation of the new DDL architecture in v7.6.0, the performance of batch table creation has witnessed a remarkable improvement, up to 10 times faster. This substantial enhancement drastically reduces the time needed for creating numerous tables. This acceleration is particularly noteworthy in SaaS scenarios, where the prevalence of high volumes of tables, ranging from tens to hundreds of thousands, is a common challenge.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (experimental)</a>  {/* tw@Oreoxmt */}</td>
    <td>TiDB v7.6.0 introduces an experimental feature "Active PD Follower", which allows PD followers to provide Region information query services. This feature improves the capability of the PD cluster to handle GetRegion and ScanRegions requests in clusters with a large number of TiDB nodes and Regions, thereby reducing the CPU pressure on the PD leader.</td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and Availability<br></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy/tiproxy-overview">Support TiProxy (experimental)</a>  {/* tw@ran-huang */}</td>
    <td>Full support for the TiProxy service, easily deployable via deployment tooling, to manage and maintain connections to TiDB so that they live through rolling restarts, upgrades, or scaling events.</td>
  </tr>
  <tr>
    <td><a href="">Data Migration (DM) officially supports MySQL 8.0 (GA)</a>  {/* tw@hfxsd */}</td>
    <td>Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (experimental) [#7431](https://github.com/tikv/pd/issues/7431) @[CabinfeverB](https://github.com/CabinfeverB) **tw@Oreoxmt** <!--1667-->

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability, TiDB v7.6.0 supports using the Active PD Follower feature to enhance the scalability of PD's Region information query service. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).

### Performance

* BR improves snapshot restore speed by up to 10 times (experimental) [#33937](https://github.com/pingcap/tidb/issues/33937) @[3pointer](https://github.com/3pointer) **tw@Oreoxmt** <!--1647-->

    As a TiDB cluster scales up, it becomes increasingly crucial to quickly restore the cluster from failures to minimize business downtime. Before v7.6.0, the Region scattering algorithm is a primary bottleneck in performance restoration. In v7.6.0, BR optimizes the Region scattering algorithm, which quickly splits the restore task into a large number of small tasks and scatters them to all TiKV nodes in batches. The new parallel recovery algorithm fully utilizes the resources of each TiKV node, thereby achieving a rapid parallel recovery. In several real-world cases, the snapshot restore speed of the cluster is improved by about 10 times in large-scale Region scenarios.

    The new coarse-grained Region scatter algorithm is experimental. To use it, you can configure the `--granularity="coarse-grained"` parameter in the `br` command. You can also control the concurrency of download tasks on each TiKV node by setting the `--tikv-max-restore-concurrency` parameter. For example:

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --tikv-max-restore-concurrency 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
    ```

    For more information, see [documentation](/br/br-snapshot-guide.md#restore-cluster-snapshots).

* Support pushing down the following string functions to TiKV [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1607-->

    * `LOWER()`
    * `UPPER()`

    For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* Support pushing down the following JSON functions to TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) [#49345](https://github.com/pingcap/tidb/issues/49345) [#49392](https://github.com/pingcap/tidb/issues/49392) @[SeaRise](https://github.com/SeaRise) @[yibin87](https://github.com/yibin87) **tw@qiancai** <!--1608-->

    * `JSON_UNQUOTE()`
    * `JSON_ARRAY()`
    * `JSON_DEPTH()`
    * `JSON_VALID()`
    * `JSON_KEYS()`
    * `JSON_CONTAINS_PATH()`

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Improve the performance of creating tables by 10 times (experimental) [#49752](https://github.com/pingcap/tidb/issues/49752) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1408-->

    In previous versions, when migrating tens of thousands of tables from the upstream database to TiDB, it is time-consuming and inefficient for TiDB to create these tables. Starting from v7.6.0, TiDB introduces a new TiDB DDL V2 architecture. You can enable it by configuring the system variable [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-new-in-v760). Compared with previous versions, the new version of the DDL improves the performance of creating batch tables by 10 times, and significantly reduces time for creating tables.

    For more information, see [documentation](/ddl-v2.md).

* The optimizer enhances support for multi-valued indexes [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1405/1584-->

    Starting from v6.6.0, TiDB introduced [multi-value indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) to improve query performance for JSON data types. In v7.6.0, the optimizer enhances its support for multi-valued indexes and can correctly identify and utilize them to optimize queries in complex scenarios.

    * Statistics on multi-valued indexes are collected and applied by the optimizer for estimation. When a SQL statement might select multiple multi-valued indexes, the optimizer can identify the index with lower cost.
    * When there are multiple `member of` conditions connected by `OR`, the optimizer is able to match an effective index partial path for each DNF item (a `member of` condition) and combine multiple paths using Union to form an `Index Merge`. This allows more efficient condition filtering and data querying.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).

### Reliability

* Cross-database execution plan binding [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    When running SaaS services on TiDB, it is common practice to store data for each tenant in separate databases for easier data maintenance and management. This results in hundreds of databases with the same table and index definitions, and similar SQL statements. In such scenario, when you create an execution plan binding for a SQL statement, this binding usually applies to the SQL statements in other databases as well.

    For this scenario, TiDB v7.6.0 introduces the cross-database binding feature, which supports binding the same execution plan to SQL statements with the same schema, even if they are in different databases. When creating a cross-database binding, you need to use the wildcard `*` to represent the database name, as shown in the following example. After the binding is created, regardless of which database the tables `t1` and `t2` are in, TiDB will try to use this binding to generate an execution plan for any SQL statement with the same schema, which saves your effort to create a binding for each database.

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount FROM *.t1, *.t2 WHERE t1.id = t2.id;
    ```

    In addition, cross-database binding can effectively mitigate SQL performance issues caused by uneven distribution and rapid changes in user data and workload. SaaS providers can use cross-database binding to fix execution plans validated by users with large data volumes, thereby fixing execution plans for all users. For SaaS providers, this feature provides significant convenience and experience improvements.

    Due to the system overhead (less than 1%) introduced by cross-database binding, TiDB disables this feature by default. To use cross-database binding, you need to first enable the [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760) system variable.

    For more information, see [documentation](/sql-plan-management.md#cross-database-binding).

### Availability

* Support the proxy component TiProxy (experimental) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@ran-huang** <!--1596-->

    TiProxy is the official proxy component of TiDB, located between the client and TiDB server. It provides load balancing and connection persistence functions for TiDB, making the workload of the TiDB cluster more balanced and not affecting user access to the database during maintenance operations.

    - During maintenance operations such as rolling restarts, rolling upgrades, and scaling-in in a TiDB cluster, changes occur in the TiDB servers which result in interruptions in connections between clients and the TiDB servers. By using TiProxy, connections can be smoothly migrated to other TiDB servers during these maintenance operations so that clients are not affected.
    - Client connections to a TiDB server cannot be dynamically migrated to other TiDB servers. When the workload of multiple TiDB servers is unbalanced, it might result in a situation where the overall cluster resources are sufficient, but certain TiDB servers experience resource exhaustion leading to a significant increase in latency. To address this issue, TiProxy provides dynamic migration for connection, which allows connections to be migrated from one TiDB server to another without any impact on the clients, thereby achieving load balancing for the TiDB cluster.

    TiProxy has been integrated into TiUP, TiDB Operator, and TiDB Dashboard, making it easy to configure, deploy and maintain.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* `LOAD DATA` supports explicit transactions and rollbacks [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1422-->

    Compared with MySQL, the transactional behavior of the`LOAD DATA` statement varies in different TiDB versions before v7.6.0, so you might need to make additional adjustments when using this statement. Specifically, before v4.0.0, `LOAD DATA` commits every 20000 rows. From v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default and also supports committing every fixed number of rows by setting the [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) system variable. Starting from v7.0.0, `tidb_dml_batch_size` no longer takes effect on `LOAD DATA` and TiDB commits all rows in one transaction.

    Starting from v7.6.0, TiDB processes `LOAD DATA` in transactions in the same way as other DML statements, especially in the same way as MySQL. The `LOAD DATA` statement in a transaction no longer automatically commits the current transaction or starts a new transaction. Moreover, you can explicitly commit or roll back the `LOAD DATA` statement in a transaction. Additionally, the `LOAD DATA` statement is affected by the TiDB transaction mode setting (optimistic or pessimistic transaction). These improvements simplify the migration process from MySQL to TiDB and offer a more unified and controllable experience for data import.

    For more information, see [documentation](/sql-statements/sql-statement-load-data.md).

### DB operations

* `FLASHBACK CLUSTER` supports specifying a precise TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger/BornChanger) **tw@qiancai** <!--1615-->

    In TiDB v7.6.0, the flashback feature is more powerful and precise. It not only supports rolling back a cluster to a specified historical timestamp but also enables you to specify a precise recovery [TSO](/tso.md) using `FLASHBACK CLUSTER TO TSO`, thereby increasing flexibility in data recovery. For example, you can use this feature with TiCDC. After pausing data replication and conducting pre-online read-write tests in your downstream TiDB cluster, this feature allows the cluster to gracefully and quickly roll back to the paused TSO and continue to replicate data using TiCDC. This streamlines the pre-online validation process and simplifies data management.

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ````

    For more information, see [documentation](/sql-statements/sql-statement-flashback-cluster.md).

* Support automatically terminating long-running idle transactions [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt** <!--1598-->

    In scenarios where network disconnection or application failure occurs, `COMMIT`/`ROLLBACK` statements might fail to be transmitted to the database. This could lead to delayed release of database locks, causing transaction lock waits and a rapid increase in database connections. Such issues are common in test environments but can also occur occasionally in production environments, and they are sometimes difficult to diagnose promptly. To avoid these issues, TiDB v7.6.0 introduces the [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) system variable, which automatically terminates long-running idle transactions. When a user session in a transactional state remains idle for a duration exceeding the value of this variable, TiDB will terminate the database connection of the transaction and roll back it.

    For more information, see [documentation](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760).

* Simplify the syntax for creating execution plan bindings [#48876](https://github.com/pingcap/tidb/issues/48876) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    TiDB v7.6.0 simplifies the syntax for creating execution plan bindings. When creating an execution plan binding, you no longer need to provide the original SQL statement. TiDB identifies the original SQL statement based on the statement with hints. This improvement enhances the convenience of creating execution plan bindings. For example:

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    For more information, see [documentation](/sql-plan-management.md#create-a-binding-according-to-a-sql-statement).

* Support dynamically modifying the size limit of a single row record in TiDB [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1452-->

    Before v7.6.0, the size of a single row record in a transaction is limited by the TiDB configuration item [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). If the size limit is exceeded, TiDB returns the `entry too large` error. In this case, you need to manually modify the TiDB configuration file and restart TiDB to make the modification take effect. To reduce your management overhead, TiDB v7.6.0 introduces the system variable [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760), which supports dynamically modifying the value of the `txn-entry-size-limit` configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, TiDB limits the size of a row record in transactions to the value of this variable. This improvement enhances the flexibility for you to adjust system configurations without restarting TiDB.

    For more information, see [documentation](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760).

* The global sort feature becomes generally available (GA), improving the performance and stability of `ADD INDEX` and `IMPORT INTO` [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) @[D3Hunter](https://github.com/D3Hunter) **tw@ran-huang** <!--1580/1579-->

    Prior to v7.4.0, when executing tasks such as `ADD INDEX` or `IMPORT INTO` using the [Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md), due to limited local storage space in TiDB, only a portion of the data could be sorted locally before importing it into TiKV. The data imported into TiKV had a significant overlap range and required additional resources for processing, which reduced the performance and stability of TiKV.

    With the introduction of the global sort feature in v7.4.0, data can be temporarily stored in external storage (such as S3) for global sorting before being imported into TiKV. This improvement reduces resource consumption of TiKV and significantly improves the performance and stability of operations such as `ADD INDEX` and `IMPORT INTO`. This feature becomes GA in v7.6.0.

    For more information, see [documentation](/tidb-global-sort.md).

* BR restores system tables by default, such as user data [#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1570/1628-->

    Starting from v5.1.0, when you back up snapshots, BR automatically backs up system tables in the `mysql` schema, but does not restore these system tables by default. In v6.2.0, BR adds the parameter `--with-sys-table` to support restoring data in some system tables, providing more flexibility in operations.

    To further reduce your management overhead and provide more intuitive default behavior, starting from v7.6.0, BR enables the parameter `--with-sys-table` by default and supports restoring user data for the `cloud_admin` user. This means that BR restores some system tables by default during restoration, especially user account and table statistics data. This improvement makes backup and restore operations more intuitive, thereby reducing the burden of manual configuration and improving the overall operation experience.

    For more information, see [documentation](/br/br-snapshot-guide.md).

### Observability

* Enhance observability related to resource control [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1668-->

    As more and more users use resource groups to isolate application workloads, Resource Control provides enhanced data based on resource groups. This helps you monitor resource group workloads and settings, ensuring that you can quickly identify and accurately diagnose problems, including:

    * [Slow Queries](/identify-slow-queries.md): add the resource group name, RU consumption, and time for waiting for resources.
    * [Statement Summary Tables](/statement-summary-tables.md): add the resource group name, RU consumption, and time for waiting for resources.
    * In the system variable [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014), add a new entry `ru_consumption` to indicate the consumed [RU](/tidb-resource-control.md#what-is-request-unit-ru) by SQL statements. You can use this variable to get the resource consumption of the last statement in the session.
    * Add database metrics based on resource groups: QPS/TPS, execution time (P999/P99/P95), number of failures, number of connections.
    * Add the system table [`request_unit_by_group`](/mysql-schema.md#system-tables-related-to-resource-control) to record the history records of daily consumed resource units (RUs) of all resource groups.

    For more information, see [Identify Slow Queries](/identify-slow-queries.md), [Statement Summary Tables](/statement-summary-tables.md), and [Key Monitoring Metrics of Resource Control](/grafana-resource-control-dashboard.md).

### Data migration

* Data Migration (DM) support for migrating MySQL 8.0 becomes generally available (GA) [#10405](https://github.com/pingcap/tiflow/issues/10405) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd** <!--1617-->

    Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).

    For more information, see [documentation](/dm/dm-compatibility-catalog.md).

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (experimental) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1521/1525/1460-->

    Starting from v7.6.0, TiCDC supports replication of DDL statements with bi-directional replication configured. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the `PRIMARY` BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* TiCDC supports querying the downstream synchronization status of a changefeed [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1627-->

    Starting from v7.6.0, TiCDC introduces a new API `GET /api/v2/changefeed/{changefeed_id}/synced` to query the downstream synchronization status of a specified replication task (changefeed). By using this API, you can determine whether the upstream data received by TiCDC has been synchronized to the downstream system completely.

    For more information, see [documentation](/ticdc/ticdc-open-api-v2.md#query-whether-a-specific-replication-task-is-completed).

* TiCDC adds support for three-character delimiters with CSV output protocol [#9969](https://github.com/pingcap/tiflow/issues/9969) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987) **tw@hfxsd** <!--1653-->

    Starting from v7.6.0, you can specify the CSV output protocol delimiters as 1 to 3 characters long. With this change, you can configure TiCDC to generate file output using two character delimiters (such as `||` or `$^`) or three character delimiters (such as `|@|`) to separate fields in the output.

    For more information, see [documentation](/ticdc/ticdc-csv.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.5.0 to the current version (v7.6.0). If you are upgrading from v7.4.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)       |    Newly added       |    Sets the concurrency of the `scan` operation when executing the `ANALYZE` operation. The default value is `4`.  | 
| [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-new-in-v760)  |  Newly added  | Controls whether to enable [TiDB DDL V2](/ddl-v2.md). Set the value to `2` to enable it and `1` to disable it. The default value is `1`. When TiDB DDL V2 is enabled, DDL statements will be executed using TiDB DDL V2. The execution speed of DDL statements for creating tables is increased by 10 times compared with TiDB DDL V1. |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)  |  Newly added   | Controls whether to support creating `Global indexes` for partitioned tables. The default value is `OFF`. `Global index` is currently in the development stage. **It is not recommended to modify the value of this system variable**. |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) | Newly added | Controls the idle timeout for transactions in a user session. When a user session is in a transactional state and remains idle for a duration exceeding the value of this variable, TiDB will terminate the session. The default value `0` means unlimited. |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760) | Newly added | Dynamically modifies the TiDB configuration item [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). It limits the size of a single row of data in TiDB. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Modified | The algorithm used for compressing values in Titan, which takes value as the unit. Starting from TiDB v7.6.0, the default compression algorithm is `zstd`. |
| TiKV | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled) | Modified  |  Enables or disables Titan. For v7.5.0 and earlier versions, the default value is `false`. Starting from v7.6.0, the default value is `true` for only new clusters. Existing clusters upgraded to v7.6.0 or later versions will retain the original configuration. |
| TiKV | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760) | Newly added | Sets the specific times that TiKV initiates periodic full compaction. The default value `[]` means periodic full compaction is disabled by default. |
| TiKV | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760) | Newly added | Limits the maximum CPU usage rate for TiKV periodic full compaction. The default value is `0.1`. |
| TiKV | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) |  Newly added | Specifies the `zstd` dictionary compression size. The default value is `"0KB"`, which means to disable the `zstd` dictionary compression. |

### System tables

- Add a new system table [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) to display the information of all keywords supported by TiDB. **tw@Oreoxmt**
- In the system table [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md), add the following fields related to Resource Control:
    - `Resource_group`: the resource group that the statement is bound to.
    - `Request_unit_read`: the total read RUs consumed by the statement.
    - `Request_unit_write`: the total write RUs consumed by the statement.
    - `Time_queued_by_rc`: the total time that the statement waits for available resources.

## Offline package changes

## Deprecated features

* 实验特性 [执行计划的自动演进绑定](https://docs.pingcap.com/zh/tidb/stable/sql-plan-management#%E8%87%AA%E5%8A%A8%E6%BC%94%E8%BF%9B%E7%BB%91%E5%AE%9A-baseline-evolution) 将在 v8.0.0 被废弃，等同的功能将会在后续版本被重新设计。

* 废弃功能 2

## Improvements

+ TiDB

    - When a non-binary collation is set and the query condition includes `LIKE`, the optimizer generates an `IndexRangeScan` to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)
    <!--tw@Oreoxmt 12 条-->
    - 当使用非二进制排序规则并且查询条件中包含 `LIKE` 时，优化器可以生成 IndexRangeScan 以提高执行效率 [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.7.md > 改进提升> TiDB - 增强特定情况下 `OUTER JOIN` 转 `INNER JOIN` 的能力 [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - 增强了分布式框架任务在节点重启场景的均衡程度 [#47298](https://github.com/pingcap/tidb/issues/47298) @[ywqzzy](https://github.com/ywqzzy)
    - 允许多个快速加索引 DDL 任务排队，而非回退到普通加索引任务 [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    - 增强对于 ALTER TABLE ... ROW_FORMAT 的兼容 [#48754](https://github.com/pingcap/tidb/issues/48754) @[hawkingrei](https://github.com/hawkingrei)
    - 调整 CANCEL IMPORT JOB 为同步命令 [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    - 优化了空表加索引的速度 [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    - 在关联子查询的列没有被上层算子引用时，关联子查询可以被直接消除 [#45822](https://github.com/pingcap/tidb/issues/45822) @[King-Dylan](https://github.com/King-Dylan)
    - 支持非 binary collation 的列使用 LIKE 条件构造索引范围扫描 [#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138)  @[time-and-fate](https://github.com/time-and-fate)
    - exchange partition 操作会触发统计信息的维护更新 [#47354](https://github.com/pingcap/tidb/issues/47354) @[hi-rustin](https://github.com/hi-rustin)
    - TiDB 支持构建满足 FIPS 要求的 binary [#47948](https://github.com/pingcap/tidb/issues/47948) @[tiancaiamao](https://github.com/tiancaiamao)
    - 改进了 TiDB 处理部分类型转换的实现，修复一些相关问题 [#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao) @[lcwangchao](https://github.com/lcwangchao)
    - 在获取 schema 版本时，默认使用 kv timeout 特性进行读取，缓解 meta region leader 读取慢对于 schema 版本更新影响 [#48125](https://github.com/pingcap/tidb/pull/48125) @[cfzjywxk](https://github.com/cfzjywxk)

+ TiKV

    <!--tw@Oreoxmt 4 条-->
    - 增加查询异步任务的API endpoint `/async_tasks`. [#15759](https://github.com/tikv/tikv/issues/15759) @[YuJuncen](https://github.com/YuJuncen)
    - 给grpc监控增加优先级的标签，从而显示资源管理中的各个不同优先级的资源组的数据 @[bufferflies](https://github.com/bufferflies)
    - 支持动态调整参数`readpool.unified.max-tasks-per-worker`的值；支持根据优先级单独核算正在运行的任务数 [#16026](https://github.com/tikv/tikv/issues/16026) @[glorv](https://github.com/glorv)
    - 支持动态可调的GC线程数，默认值是1。[#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    <!--tw@Oreoxmt 1 条-->
    - 提升 PD TSO 在磁盘抖动时的可用性 [#7377](https://github.com/tikv/pd/issues/7377) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    <!--tw@Oreoxmt 4 条-->
    - (dup): release-6.5.7.md > 改进提升> TiFlash - 降低磁盘性能抖动对读取延迟的影响 [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 减少后台数据 GC 任务对读、写任务延迟的影响 [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 支持在存算分离架构下通过合并相同数据的读取操作，提升多并发下的数据扫描性能 [#6834](https://github.com/pingcap/tiflash/issues/6834) @[JinheLin](https://github.com/JinheLin)
    - 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8563](https://github.com/pingcap/tiflash/issues/8563) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化 join on 条件中仅包含 join key 等值条件时，semijoin及 leftouter    -semijoin 的执行性能 [#47424](https://github.com/pingcap/tidb/issues/47424) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.1.3.md > 改进提升> Tools> Backup & Restore (BR) - 新增 PITR 对 delete range 场景的集成测试，提升 PITR 稳定性 [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.7.md > 改进提升> Tools> Backup & Restore (BR) - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        <!--tw@Oreoxmt 2 条-->
        - (dup): release-7.1.3.md > 改进提升> Tools> TiCDC - 通过增加并行，优化了 TiCDC 同步数据到对象存储的性能 [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.1.3.md > 改进提升> Tools> TiCDC - 支持通过在 `sink-uri` 中设置 `content-compatible=true` 使 TiCDC Canal-JSON [兼容 Canal 官方输出的内容格式](/ticdc/ticdc-canal-json.md#兼容-canal-官方实现) [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)
        - Storage sink 中增加对分段上传到Amazon S3 的支持[#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 支持 TiCDC 构建 fips-ready 的 binary[#9962](https://github.com/pingcap/tiflow/issues/9962)@[lidezhu](https://github.com/lidezhu)
        - TiCDC 增加支持 mtls 的配置 `security.mtls`[#10015](https://github.com/pingcap/tiflow/issues/10015)@[zhangjinpeng87](https://github.com/zhangjinpeng87)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB

    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 TiDB panic 并报错 `invalid memory address or nil pointer dereference` 的问题 [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复当 DDL `jobID` 恢复为 0 时 TiDB 节点 panic 的问题 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复某些情况下相同的查询计划拥有不同的 `PLAN_DIGEST` 的问题 [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复 `UNION ALL` 第一个子节点是 DUAL Table 时，执行可能报错的问题 [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复当 `tidb_max_chunk_size` 值较小时，包含 CTE 的查询出现 `runtime error: index out of range [32] with length 32` 错误的问题 [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.6.md > 错误修复> TiDB - 修复使用 `AUTO_ID_CACHE=1` 时 Goroutine 泄漏的问题 [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复 MPP 计算 `COUNT(INT)` 时结果可能出错的问题 [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复当分区列类型为 `DATETIME` 时，执行 `ALTER TABLE ... LAST PARTITION` 失败的问题 [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复数据中包含后导空格时，在 `LIKE` 中使用 `_` 通配符可能会导致查询结果出错的问题 [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 `tidb_server_memory_limit` 导致内存长期压力较高时，TiDB CPU 利用率过高的问题 [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复 `ENUM` 类型列作为 join 键时，查询结果错误的问题 [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复当内存使用超限时包含公共表表达式 (CTE) 的查询非预期卡住的问题 [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 TiDB server 在使用企业插件审计日志时可能占用大量资源的问题 [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复特定情况下优化器将 TiFlash 选择路径错误转化为 DUAL Table 的问题 [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复包含递归 (`WITH RECURSIVE`) CTE 的 `UPDATE` 或 `DELETE` 语句可能会产生错误结果的问题 [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复包含 IndexHashJoin 算子的查询由于内存超过 `tidb_mem_quota_query` 而卡住的问题 [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在非严格模式下 (`sql_mode = ''`)，`INSERT` 过程中产生截断仍然会报错的问题 [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 CTE 查询在重试过程中可能会报错 `type assertion for CTEStorageMap failed` 的问题 [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在嵌套的 `UNION` 查询中 `LIMIT` 和 `OPRDERBY` 可能无效的问题 [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在解析 `ENUM` 或 `SET` 类型的非法值时会导致 SQL 语句报错的问题 [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复构造统计信息时因为 Golang 隐式转换算法导致统计信息误差过大的问题 [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复在某些时区下夏令时显示有误的问题 [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > 错误修复> TiDB - 修复在有大量表时，`AUTO_ID_CACHE=1` 的表可能造成 gRPC 客户端泄漏的问题 [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > 错误修复> TiDB - 修复 TiDB server 在优雅关闭 (graceful shutdown) 时可能 panic 的问题 [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    <!--tw@hfxsd 以下 24 条-->
    - 修复 `admin recover index` 在处理含 CommonHandle 的表时会 panic 的问题 [#47687](https://github.com/pingcap/tidb/issues/47687) @[Defined2014](https://github.com/Defined2014)
    - 修复 `ALTER TABLE t PARTITION BY` 时指定 placement rules 报错的问题 [#48631](https://github.com/pingcap/tidb/pull/48631) @[mjonss](https://github.com/mjonss)
    - 修复 `information_schema.CLUSTER_INFO` 中 `START_TIME` 列类型不合理的问题 [#45221](https://github.com/pingcap/tidb/issues/45221) @[dveeden](https://github.com/dveeden)
    - 修复 `information_schema. columns` 中 `EXTRA` 列类型不合理的问题 [#42030](https://github.com/pingcap/tidb/issues/42030) @[tangenta](https://github.com/tangenta)
    - 修复类似的 `IN (...)` 语句会生成不同 plan_digest 的问题 [#33559](https://github.com/pingcap/tidb/issues/33559) @[King-Dylan](https://github.com/King-Dylan)
    - 修复 `TIME` 类型转换为 `YEAR` 类型时的问题，修复后会返回表示时间的字符串，而不是混合 `TIME` 和当前时间的年份结果。[#48557](https://github.com/pingcap/tidb/issues/48557) @[YangKeao](https://github.com/YangKeao)
    - 修复了当 `tidb_enable_collect_execution_info` 关闭时 copr cache panic 的问题 [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    - 修复了 shuffleExec 意外退出导致 tidb 崩溃的问题 [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了静态 `calibrate resource` 依赖于 prometheus 数据的 bug [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    - 修复了在日期和大的 interval 做加法时的行为，使与 Mysql8.0 一致，此 PR 之后，1）带有无效前缀的 interval将被视为零值 2）带有字符串 "true" 的 interval 将被视为零值 [#49227](https://github.com/pingcap/tidb/issues/49227) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了对函数 ROW 的 null 类型推断问题 [#49015](https://github.com/pingcap/tidb/issues/49015) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了在某些情况下 `ilike` 函数的数据竞争问题 [#49677](https://github.com/pingcap/tidb/issues/49677) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了 StreamAgg 因为错误处理 ci 的而引起的结果不正确的问题[#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了表达式 `inet_ntoa()` 中的兼容性问题 [#46598](https://github.com/pingcap/tidb/issues/46598) @[solotzg](https://github.com/solotzg)
    - 修复了将字节转换为时间编码失败的问题 [#47346](https://github.com/pingcap/tidb/issues/47346) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了 deicmal 乘法运算时截断处理有误的错误结果问题 [#48332](https://github.com/pingcap/tidb/issues/48332) @[solotzg](https://github.com/solotzg)
    - 修复 CHECK 约束 ENFORCED 选项与 MySQL 8.0 不一致的错误 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 CHECK 约束的 DDL 卡住的问题 [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 DDL 快速加索引由于内存不足失败的问题 [#47862](https://github.com/pingcap/tidb/issues/47862) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复在集群升级过程中加索引可能导致数据与索引不一致的问题 [#47862](https://github.com/pingcap/tidb/issues/47862) @[zimulala](https://github.com/zimulala)
    - 修复 ADMIN CHECK 无法使用更新后的 `tidb_mem_quota_query` 变量的问题 [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    - 修复对外键的被引用列 ALTER TABLE 可能遇到的问题 [#49836](https://github.com/pingcap/tidb/issues/49836) [#47702](https://github.com/pingcap/tidb/issues/47702) @[yoshikipom](https://github.com/yoshikipom)
    - 修复某些场景下表达式索引不会发现“除以 0”错误的问题 [#50053](https://github.com/pingcap/tidb/issues/50053) @[lcwangchao](https://github.com/lcwangchao)
    - 缓解了表的数目过多时 TiDB 节点 OOM 的问题 [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    <!--tw@qiancai 以下 25 条-->
    - 修复了集群滚动重启时 DDL 卡在运行中状态的问题 [#50073](https://github.com/pingcap/tidb/issues/50073) @[tangenta](https://github.com/tangenta)
    - 修复使用 PointGet BatchPointGet 访问分区表的全局索引时，结果可能出错的问题 [#47539](https://github.com/pingcap/tidb/issues/47539) @[L-maple](https://github.com/L-maple)
    - 修复有虚拟列上索引时，可能无法选中 MPP 计划的问题 [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - 修复 Limit 可能无法推入 OR 类型的 Index Merge 的问题 [#48588](https://github.com/pingcap/tidb/issues/48588) @[AilinKid](https://github.com/AilinKid)
    - 修复 BR 导入后，mysql.bind_info 可能多出内置的 builtin 行的问题 [#46527](https://github.com/pingcap/tidb/issues/46527) @[qw4990](https://github.com/qw4990)
    - 修复 drop partition 时，统计信息更新行为不合理的问题 [#48182](https://github.com/pingcap/tidb/issues/48182) @[hi-rustin](https://github.com/hi-rustin)
    - 修复并发合并分区表全局统计信息可能结果出错的问题 [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - 修复有 PADDING SPACE 的列在使用 LIKE 函数构造索引范围查询时，结果可能出错的问题 [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)
    - 修复生成列可能触发对内存结构并发读写的问题 [#44919](https://github.com/pingcap/tidb/issues/44919) @[tangenta](https://github.com/tangenta)
    - 修复当指定不收集 TopN 时，统计信息仍然可能收集 1 个 TopN 的问题 [#49080](https://github.com/pingcap/tidb/issues/49080) @[hawkingrei](https://github.com/hawkingrei)
    - 修复不合法的优化器 hint 可能会导致合法 hint 不生效的问题 [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - 修复对 Hash 类型的分区表进行分区的增删重组以及 truncate 操作时，统计信息没有进行对应的维护操作的问题 [#48235](https://github.com/pingcap/tidb/issues/48235) [#48233](https://github.com/pingcap/tidb/issues/48233) [#48226](https://github.com/pingcap/tidb/issues/48226) [#48231](https://github.com/pingcap/tidb/issues/48231) @[hi-rustin](https://github.com/hi-rustin)
    - 修复设置统计信息自动更新的时间窗口后，时间窗口外仍然可能触发统计信息的问题 [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - 修复从分区表转为非分区表时，旧统计信息不会自动删除的问题 [#49547](https://github.com/pingcap/tidb/issues/49547) @[hi-rustin](https://github.com/hi-rustin)
    - 修复当 truncate 非分区表时，旧统计信息不会自动删除的问题 [#49663](https://github.com/pingcap/tidb/issues/49663) @[hi-rustin](https://github.com/hi-rustin)
    - 修复使用 STREAM_AGG() 等会强制排序的优化器 hint 时且选中 Index Merge 时，强制添加的 sort 可能会丢失的问题 [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - 修复统计信息直方图的边界包含 NULL 时，可能无法解析成可读字符串的问题 [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - 修复包含 group_concant(order by) 语法时，可能执行出错的问题 [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - 修复了在没有使用严格的 `SQL_MODE` 时，溢出错误在 `UPDATE`, `DELETE`, `INSERT` 仍然返回错误而非 Warning 的问题 [#49137](https://github.com/pingcap/tidb/issues/49137) @[YangKeao](https://github.com/YangKeao)
    - 修复了由 multi-valued index 和非 Binary 类型字符串组成的复合索引无法写入的问题 [#49680](https://github.com/pingcap/tidb/issues/49680) @[YangKeao](https://github.com/YangKeao)
    - 修复了复合的 Union 语句中 `limit` 无效的问题 [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - 修复了在使用分区表时 `BETWEEN ... AND ...` 条件查询出错误结果的问题 [#49842](https://github.com/pingcap/tidb/issues/49842) @[Defined2014](https://github.com/Defined2014)
    - 修复了无法在 `REPLACE INTO` 语句中使用 `hints` 的问题 [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - 修复了在使用 Hash 分区表时可能选中错误分区的问题 [#50044](https://github.com/pingcap/tidb/issues/50044) @[Defined2014](https://github.com/Defined2014)
    - 修复了使用 Mariadb J Connector 并配置启用压缩时发生连接错误的问题 [#49845](https://github.com/pingcap/tidb/issues/49845) @[onlyacat](https://github.com/onlyacat)

 + TiKV

    <!--tw@ran-huang 10 条-->
    - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点导致 panic 的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996) **tw@Oreoxmt** <!--1631-->
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复扩容时可能导致 DR Auto-Sync 的 joint state 超时问题 [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 Titan `blob-run-mode` 无法在线更新的问题 [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复 resolved-ts 可能被阻塞 2 小时的问题 [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 Resolved TS 可能被阻塞两小时的问题 [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.6.md > 错误修复> TiKV - 修复在 Flashback 时遇到 `notLeader` 或 `regionNotFound` 时卡住的问题 [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复如果 TiKV 运行极慢，在 Region Merge 之后可能 panic 的问题 [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - 修复 GC 进行扫描过期 lock 无法读取内存悲观锁的问题 [#15066](https://github.com/tikv/tikv/issues/15066) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复Titan监控中不正确的Blob文件大小，并修改部分参数的默认值------GC线程数默认改为1，压缩算法默认调整为ZSTD。 [#15971](https://github.com/tikv/tikv/issues/15971) @[Connor1996](https://github.com/Connor1996)
    - 修复TiCDC在同步大表时可能导致TiKV OOM的问题。[#16035](https://github.com/tikv/tikv/issues/16035) @[overvenus](https://github.com/overvenus)
    - 修复resolve ts可能被阻塞2个小时的问题。 [#11847](https://github.com/tikv/tikv/issues/11847) @[overvenus](https://github.com/overvenus)
    - 修复日志备份任务内存泄露的问题。修复日志备份任务开始但可能不能真正工作的问题。 [#16070](https://github.com/tikv/tikv/issues/16070) @[YuJuncen](https://github.com/YuJuncen)
    - 修复在处理decimal算术乘法截断的错误。 [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - 修复`cast_duration_as_time`可能返回错误结果的错误. [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - 修复巴西和埃及时区转换的错误。 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复gRPC threads可能在检查`is_shutdown`时出现的panic的错误。 [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)

    + PD

    <!--tw@ran-huang 1 条-->
    - 修复 PD 内 Etcd 健康检查没有移除过期地址的问题 [#7226](https://github.com/tikv/pd/issues/7226) @[iosmanthus](https://github.com/iosmanthus)
    - (dup): release-7.1.3.md > 错误修复> PD - 修复 PD Leader 切换且新 Leader 与调用方之间存在网络隔离时，调用方不能正常更新 Leader 信息的问题 [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.1.3.md > 错误修复> PD - 将 Gin Web Framework 的版本从 v1.8.1 升级到 v1.9.1 以修复部分安全问题 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - (dup): release-6.5.7.md > 错误修复> PD - 修复在不满足副本数量需求时，删除 orphan peer 的问题 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    <!--tw@ran-huang 11 条-->
    - (dup): release-6.5.7.md > 错误修复> TiFlash - 修复当查询遇到内存限制后发生内存泄漏的问题 [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-6.5.7.md > 错误修复> TiFlash - 修复在执行 `FLASHBACK DATABASE` 后 TiFlash 副本的数据仍会被 GC 回收的问题 [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.7.md > 错误修复> TiFlash - 修复慢查询导致内存使用显著增加的问题 [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - 修复在 `CREATE TABLE` `DROP TABLE` 频繁执行的场景下，部分 tiflash 副本数据无法通过 `RECOVER TABLE` 或 `FLASHBACK TABLE` 恢复的问题 [#1664](https://github.com/pingcap/tiflash/issues/1664) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在查询带有过滤条件类似 `ColumnRef in (Literal, Func...)` 时查询结果出错的问题 [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在 TiDB 执行并发 DDL 遇到冲突后 TiFlash panic 的问题 [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，可能无法正常选出对象存储数据 GC owner 的问题 [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复了 lowerUTF8/upperUTF8 不允许大小写字符占据不同字节数的 bug [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - 修复了 TiFlash 处理 enum 偏移量为 0 的问题 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - 修复了表达式 `inet_ntoa()` 中的兼容性问题 [#8211](https://github.com/pingcap/tiflash/issues/8211) @[solotzg](https://github.com/solotzg)
    - 修复了在 stream 读时扫描多个分区表可能导致潜在的 OOM 问题 [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    - 避免为成功执行的短查询打印过多的信息日志 [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - 修复了 TiFlash 在停止时可能崩溃的问题 [#8550](https://github.com/pingcap/tiflash/issues/8550) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了 greatest/leatest 函数在包含常量字符串参数时可能发生的随机无效内存访问问题 [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.1.3.md > 错误修复> Tools> Backup & Restore (BR) - 修复生成外部存储文件 URI 错误的问题 [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.7.md > 错误修复> Tools> Backup & Restore (BR) - 修复在任务初始化阶段出现与 PD 的连接错误导致日志备份任务虽然启动但无法正常工作的问题 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复某些场景下在同步 `DELETE` 语句时，`WHERE` 条件没有采用主键作为条件的问题 [#9812](https://github.com/pingcap/tiflow/issues/9812) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复 redo log 开启时，DDL 同步时间间隔过长的问题 [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复同步数据到对象存储时，可能会出现 TiCDC Server panic 的问题 [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.7.md > 错误修复> Tools> TiCDC - 修复 `kv-client` 初始化过程中可能出现数据竞争的问题 [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.1.3.md > 错误修复> Tools> TiCDC - 修复在某些特殊场景下，TiCDC 错误地关闭与 TiKV 的连接的问题 [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.6.md > 错误修复> Tools> TiCDC - 修复上游在执行有损 DDL 时，TiCDC Server 可能 panic 的问题 [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.7.md > 错误修复> Tools> TiCDC - 修复数据同步到下游 MySQL 时可能出现 `checkpoint-ts` 卡住的问题 [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Contributors

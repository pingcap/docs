---
title: TiDB 6.6.0 Release Notes
---

# TiDB 6.6.0 Release Notes

Release date: xx, 2023

TiDB version: 6.6.0-DMR

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.6/quick-start-with-tidb) | [Installation package](https://cn.pingcap.com/product-community/)

In v6.6.0-DMR, the key new features and improvements are as follows:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="2">SQL operations and compatibility<br /><br /><i>SEAMLESS to use</i></td>
    <td><a href="#foreign-key">Foreign Key</a></td>
    <td>Support MySQL-compatible foreign key constraints to maintain data consistency and improve data quality.</td>
  </tr>
  <tr>
    <td><a href="#multi-valued-index">Multi-valued index (experimental)</a></td>
    <td>Introduce MySQL-compatible multi-valued indexes and enhance the JSON type to improve TiDB's compatibility with MySQL 8.0.</td>
  </tr>
  <tr>
    <td>DB Operations<br /><br /><i>SMOOTH to use</i></td>
    <td><a href="#resource-group">Tenant resource group control (experimental)</a></td>
    <td>Support resource management based on resource groups, mapping database users to the corresponding resource groups and setting quotas for each resource group based on actual needs.</td>
  </tr>
  <tr>
    <td>Stability<br /><br /><i>RELIABLE to use</i></td>
    <td><a href="#binding-his-ga">Historical SQL binding</a></td>
    <td>Support binding historical execution plans and quickly binding execution plans on TiDB Dashboard.</td>
  </tr>
  <tr>
    <td rowspan="3">Performance<br /><br /><i>POWERFUL to use</i></td>
    <td><a href="#compression-exchange">TiFlash supports compression exchange</a></td>
    <td>TiFlash supports data compression to improve the efficiency of parallel data exchange.</td>
  </tr>
  <tr>
    <td><a href="#tiflash-stale-read">TiFlash supports stale read</a></td>
    <td>TiFlash supports the Stale Read feature, which can improve query performance in scenarios where real-time requirements are not restricted.</td>
  </tr>
  <tr>
    <td><a href="#dm-physical">DM support physical import (experimental)</a></td>
    <td>TiDB Data Migration (DM) integrates TiDB Lightning's Physical Import mode to improve the performance of full data migration, with performance being up to 10 times faster.</td>
  </tr>
</tbody>
</table>

## New features

### SQL

* <a name="foreign-key" style="text-decoration:none; color:inherit; cursor:default;">Support the MySQL-compatible foreign key constraints</a> <a href="https://github.com/pingcap/tidb/issues/18209" target="_blank" referrerpolicy="no-referrer-when-downgrade">#18209</a> <a href="https://github.com/crazycs520" target="_blank" referrerpolicy="no-referrer-when-downgrade">@crazycs520</a> **tw@Oreoxmt**

    TiDB v6.6.0 introduces the foreign key constraints feature, which is compatible with MySQL. This feature supports referencing within a table or between tables, constraints validation, and cascade operations. This feature helps to migrate applications to TiDB, maintain data consistency, improve data quality, and facilitate data modeling.

    For more information, see [documentation](/foreign-key.md).

* <a name="multi-valued-index" style="text-decoration:none; color:inherit; cursor:default;">Support the MySQL-compatible multi-valued index (experimental)</a> <a href="https://github.com/pingcap/tidb/issues/39592" target="_blank" referrerpolicy="no-referrer-when-downgrade">#39592</a> <a href="https://github.com/xiongjiwei" target="_blank" referrerpolicy="no-referrer-when-downgrade">@xiongjiwei</a> <a href="https://github.com/qw4990" target="_blank" referrerpolicy="no-referrer-when-downgrade">@qw4990</a> **tw@TomShawn**

    TiDB introduces the MySQL-compatible multi-valued index in v6.6.0. Filtering the values of an array in a JSON column is a common operation, but normal indexes cannot help speed up such an operation. Creating a multi-valued index on an array can greatly improve filtering performance. If an array in the JSON column has a multi-valued index, you can use the multi-value index to filter the retrieval conditions with `MEMBER OF()`, `JSON_CONTAINS()`, `JSON_OVERLAPS()` functions, thereby reducing much I/O consumption and improving operation speed.

    Introducing multi-valued indexes further enhances TiDB's support for the JSON data type and also improves TiDB's compatibility with MySQL 8.0.

    For details, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-index)

* Support rolling back DDL operations via the `FLASHBACK CLUSTER TO TIMESTAMP` statement [#14088](https://github.com/tikv/tikv/pull/14088) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato) **tw@ran-huang**

    The [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) statement supports restoring the entire cluster to a specified point in time within the Garbage Collection (GC) lifetime. In TiDB v6.6.0, this feature adds support for rolling back DDL operations. This can be used to quickly undo a DML or DDL misoperation on a cluster, roll back a cluster within minutes, and roll back a cluster multiple times on the timeline to determine when specific data changes occurred.

    For more information, see [documentation](/sql-statements/sql-statement-flashback-to-timestamp.md).

### Stability

* <a name="binding-his-ga" style="text-decoration:none; color:inherit; cursor:default;">Binding historical execution plans is GA</a> <a href="https://github.com/pingcap/tidb/issues/39199" target="_blank" referrerpolicy="no-referrer-when-downgrade">#39199</a> <a href="https://github.com/fzzf678" target="_blank" referrerpolicy="no-referrer-when-downgrade">@fzzf678</a> **tw@TomShawn**

    In v6.5.0, TiDB extends the binding targets in the [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) statements and supports creating bindings according to historical execution plans. In v6.6.0, this feature is GA. The selection of execution plans is not limited to the current TiDB node. Any historical execution plan generated by any TiDB node can be selected as the target of [SQL binding](/sql-statements/sql-statement-create-binding.md), which further improves the feature usability.

    For more information, see [documentation](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan).

* Add several optimizer hints [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent) **tw@TomShawn**

    TiDB adds several optimizer hints in v6.6.0 to control the execution plan selection of `LIMIT` operations.

    - [`ORDER_INDEX()`](/optimizer-hints.md#keep_ordert1_name-idx1_name--idx2_name-): tells the optimizer to use the specified index, to keep the order of the index when reading data, and generates plans similar to `Limit + IndexScan(keep order: true)`.
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_keep_ordert1_name-idx1_name--idx2_name-): tells the optimizer to use the specified index, not to keep the order of the index when reading data, and generates plans similar to `TopN + IndexScan(keep order: false)`.

    Continuously introducing optimizer hints provides users with more intervention methods, helps solve SQL performance issues, and improves the stability of overall performance.

* Support a stable wake-up model for pessimistic lock queues [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta) **tw@TomShawn**

    If an application encounters frequent single-point pessimistic lock conflicts, the existing wake-up mechanism cannot guarantee the time for transactions to acquire locks, which causes high long-tail latency and even lock acquisition timeout. Starting from v6.6.0, you can enable a stable wake-up model for pessimistic locks by setting the value of the system variable [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-new-in-v660) to `ON`. In this wake-up model, the wake-up sequence of a queue can be strictly controlled to avoid the waste of resources caused by invalid wake-ups. In scenarios with serious lock conflicts, the stable wake-up model can reduce long-tail latency and the P99 response time.

    For details, see [documentation](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-new-in-v660).

* Support dynamically managing the resource usage of DDL operations (experimental) [#38025](https://github.com/pingcap/tidb/issues/38025) @[hawkingrei](https://github.com/hawkingrei) **tw@ran-huang**

    TiDB v6.6.0 introduces resource management for DDL operations to reduce the impact of DDL changes on online applications by automatically controlling the CPU usage of these operations. This feature is effective only after the [DDL distributed parallel execution framework](/system-variables.md#tidb_ddl_distribute_reorg-new-in-v660) is enabled.

### Performance

* Batch aggregate data requests [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06) **tw@TomShawn**

    When TiDB sends a data request to TiKV, TiDB compiles the request into different sub-tasks according to the Region where the data is located, and each sub-task only processes the request of a single Region. When the data to be accessed is highly dispersed, even if the size of the data is not large, many sub-tasks will be generated, which in turn will generate many RPC requests and consume extra time. Starting from v6.6.0, TiDB supports partially merging data requests that are sent to the same TiKV instance, which reduces the number of sub-tasks and the overhead of RPC requests. In the case of high data dispersion and insufficient gRPC thread pool resources, batching requests can improve performance by more than 50%.

    This feature is enabled by default. You can set the batch size of requests using the system variable [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size).

* Remove the limit on `LIMIT` clauses [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw@shichun-0415**

    Starting from v6.6.0, TiDB plan cache supports caching queries containing `?` after `Limit`, such as `Limit ?` or `Limit 10, ?`. This feature allows more SQL statements to benefit from plan cache, thus improving execution efficiency.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* Support the distributed parallel execution framework for DDL operations (experimental) [#37125](https://github.com/pingcap/tidb/issues/37125) @[zimulala](https://github.com/zimulala) **tw@ran-huang**

    In previous versions, only one TiDB instance in the entire TiDB cluster was allowed to handle schema change tasks as a DDL owner. To further improve DDL concurrency, TiDB v6.6.0 introduces the distributed parallel execution framework for DDL, through which all TiDB instances in the cluster can concurrently execute the `StateWriteReorganization` phase of the same task to speed up DDL execution. This feature is controlled by the system variable [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-new-in-v660) and is currently only supported for `Add Index` operations.

### HTAP

* <a name="compression-exchange" style="text-decoration:none; color:inherit; cursor:default;">TiFlash supports data exchange with compression</a> <a href="https://github.com/pingcap/tiflash/issues/6620" target="_blank" referrerpolicy="no-referrer-when-downgrade">#6620</a> <a href="https://github.com/solotzg" target="_blank" referrerpolicy="no-referrer-when-downgrade">@solotzg</a> **tw@TomShawn**

    To cooperate with multiple nodes for computing, the TiFlash engine needs to exchange data among different nodes. When the size of the data to be exchanged is very large, the performance of data exchange might affect the overall computing efficiency. In v6.6.0, the TiFlash engine introduces a compression mechanism to compress the data that needs to be exchanged when necessary, and then to perform the exchange, thereby improving the efficiency of data exchange.

    For details, see [documentation]().

* <a name="tiflash-stale-read" style="text-decoration:none; color:inherit; cursor:default;">TiFlash supports the Stale Read feature</a> <a href="https://github.com/pingcap/tiflash/issues/4483" target="_blank" referrerpolicy="no-referrer-when-downgrade">#4483</a> <a href="https://github.com/hehechen" target="_blank" referrerpolicy="no-referrer-when-downgrade">@hehechen</a> **tw@qiancai**

   The Stale Read feature has been generally available (GA) since v5.1.1, which allows you to read historical data at a specific timestamp or within a specified time range. Stale read can reduce read latency and improve query performance by reading data from local TiKV replicas directly. Before v6.6.0, TiFlash does not support Stale Read. Even if a table has TiFlash replicas, Stale Read can only read its TiKV replicas.

   Starting from v6.6.0, TiFlash supports the Stale Read feature. When you query the historical data of a table using the [`AS OF TIMESTAMP`](/as-of-timestamp.md) syntax or the [`tidb_read_staleness`](/tidb-read-staleness.md) system variable, if the table has a TiFlash replica, the optimizer now can choose to read the corresponding data from the TiFlash replica, thus further improving query performance.

    For more information, see [documentation](/stale-read.md).

* Support pushing down the `regexp_replace` string function to TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**

### High availability

* Support configuring `SURVIVAL_PREFERENCE` for [placement rules in SQL](/placement-rules-in-sql.md) [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch) **tw@qiancai**

    `SURVIVAL_PREFERENCES` provides data survival preference settings to increase the disaster survivability of data. By specifying `SURVIVAL_PREFERENCE`, you can control the following:

    - For TiDB clusters deployed across cloud regions, when a cloud region fails, the specified databases or tables can survive in another cloud region.
    - For TiDB clusters deployed in a single cloud region, when an availability zone fails, the specified databases or tables can survive in another availability zone.

     For more information, see [documentation](/placement-rules-in-sql.md#survival-preference).

### Security

* TiFlash supports automatic rotations of TLS certificates [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy) **tw@qiancai**

    In v6.6.0, TiDB supports automatic rotations of TiFlash TLS certificates. For a TiDB cluster with encrypted data transmission between components enabled, when a TLS certificate of TiFlash expires and needs to be reissued with a new one, the new TiFlash TLS certificate can be automatically loaded without restarting the TiDB cluster. In addition, the rotation of a TLS certificate between components within a TiDB cluster does not affect the use of the TiDB cluster, which ensures high availability of the cluster.

    For more information, see [documentation](/enable-tls-between-components.md).

* TiDB Lightning supports accessing Amazon S3 data via AWS IAM role keys and session tokens [#4075](https://github.com/pingcap/tidb/issues/40750) @[okJiang](https://github.com/okJiang) **tw@qiancai**

    Before v6.6.0, TiDB Lightning only supports accessing S3 data via AWS IAM **user's access keys** (each access key consists of an access key ID and secret access key) so you cannot use a temporary session token to acess S3 data. Staring from v6.6.0, TiDB Lightning supports accessing S3 data via AWS IAM **role's access keys + session tokens** as well to improve the data security.

    For more information, see [documentation](/tidb-lightning-data-source#import-data-from-amazon-s3).

### DB operations

* <a name="resource-group" style="text-decoration:none; color:inherit; cursor:default;">Support resource control based on resource groups (experimental)</a> <a href="https://github.com/pingcap/tidb/issues/38825" target="_blank" referrerpolicy="no-referrer-when-downgrade">#38825</a> <a href="https://github.com/nolouch" target="_blank" referrerpolicy="no-referrer-when-downgrade">@nolouch</a> <a href="https://github.com/BornChanger" target="_blank" referrerpolicy="no-referrer-when-downgrade">@BornChanger</a> <a href="https://github.com/glorv" target="_blank" referrerpolicy="no-referrer-when-downgrade">@glorv</a> <a href="https://github.com/tiancaiamao" target="_blank" referrerpolicy="no-referrer-when-downgrade">@tiancaiamao</a> <a href="https://github.com/Connor1996" target="_blank" referrerpolicy="no-referrer-when-downgrade">@Connor1996</a> <a href="https://github.com/JmPotato" target="_blank" referrerpolicy="no-referrer-when-downgrade">@JmPotato</a> <a href="https://github.com/hnes" target="_blank" referrerpolicy="no-referrer-when-downgrade">@hnes</a> <a href="https://github.com/CabinfeverB" target="_blank" referrerpolicy="no-referrer-when-downgrade">@CabinfeverB</a> <a href="https://github.com/HuSharp" target="_blank" referrerpolicy="no-referrer-when-downgrade">@HuSharp</a> **tw@hfxsd**

    Now you can create resource groups for a TiDB cluster, bind different database users to corresponding resource groups, and set quotas for each resource group according to actual needs. When the cluster resources are limited, all resources used by sessions in the same resource group will be limited to the quota. In this way, even if a resource group is over-consumed, the sessions in other resource groups are not affected. TiDB provides a built-in view of the actual usage of resources on Grafana dashboards, assisting you to allocate resources more rationally.

    The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units.

    With this feature, you can:

    - Combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set read and write quotas, so as to achieve the maximum utilization of resources.
    - Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.

    In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

    In v6.6, you need to enable both TiDB's global variable [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) and the TiKV configuration item [`resource-control.enabled`](/tikv-configuration-file.md#resource_control) to enable resource control. Currently, the supported quota method is based on "[Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)". RU is TiDB's unified abstraction unit for system resources such as CPU and IO.

    For more information, see [documentation](/tidb-resource-control.md).

* Support configuring read-only storage nodes for resource-consuming tasks <a href="https://github.com/v01dstar">@v01dstar</a> **tw@Oreoxmt**

    In production environments, some read-only operations might consume a large number of resources regularly and affect the performance of the entire cluster, such as backups and large-scale data reading and analysis. TiDB v6.6.0 supports configuring read-only storage nodes for resource-consuming read-only tasks to reduce the impact on the online application. Currently, TiDB, TiSpark, and BR support reading data from read-only storage nodes. You can configure read-only storage nodes according to [steps](/readonly-nodes.md#steps) and specify where data is read through the system variable `tidb_replica_read`, the TiSpark configuration item `spark.tispark.replica_read`, or the br command line argument `--read-only`, to ensure the stability of cluster performance.

    For more information, see [documentation](/best-practices/readonly-nodes.md).

* Support dynamically modifying `store-io-pool-size` [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator) **tw@shichun-0415**

    The TiKV configuration item [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) specifies the allowable number of threads that process Raft I/O tasks, which can be adjusted when tuning TiKV performance. Before v6.6.0, this configuration item cannot be modified dynamically. Starting from v6.6.0, you can modify this configuration without restarting the server, which means more flexible performance tuning.

    For more information, see [documentation](/dynamic-config.md).

* Support specifying the SQL script executed upon TiDB cluster intialization [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo) **tw@shichun-0415**

    When you start a TiDB cluster for the first time, you can specify the SQL script to be executed by configuring the command line parameter `--initialize-sql-file`. You can use this feature when you need to perform such operations as modifying the value of a system variable, creating a user, or granting privileges.

    For more information, see [documentation](/tidb-configuration-file.md#initialize-sql-file-new-in-v660).

### Observability

* Support quickly creating SQL binding on TiDB Dashboard [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506) **tw@ran-huang**

    TiDB v6.6.0 supports creating SQL binding from statement history, which allows you to quickly bind a SQL statement to a specific plan on TiDB Dashboard.

    By providing a user-friendly interface, this feature simplifies the process of binding plans in TiDB, reduces the operation complexity, and improves the efficiency and user experience of the plan binding process.

    For more information, see [documentation](/dashboard/dashboard-statement-details.md#create-sql-binding).

* Add warning for caching execution plans @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    When an execution plan cannot be cached, TiDB indicates the reason in warning to make diagnostics easier. For example:

    ```sql
    mysql> PREPARE st FROM 'SELECT * FROM t WHERE a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> SET @a='1';
    Query OK, 0 rows affected (0.00 sec)

    mysql> EXECUTE st USING @a;
    Empty set, 1 warning (0.01 sec)

    mysql> SHOW WARNINGS;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```

    In the preceding example, the optimizer converts a non-INT type to an INT type, and the execution plan might change with the change of the parameter, so TiDB does not cache the plan.

    For more information, see [documentation](/sql-prepared-plan-cache.md#diagnostics-of-prepared-plan-cache).

* Add a `Warnings` field to the slow query log [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate) **tw@Oreoxmt**

    TiDB v6.6.0 adds a `Warnings` field to the slow query log to help diagnose performance issues. This field records warnings generated during the execution of a slow query. You can also view the warnings on the slow query page of TiDB Dashboard.

    For more information, see [documentation](/identify-slow-queries.md).

* Automatically capture the generation of SQL execution plans [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer) **tw@ran-huang**

    In the process of troubleshooting execution plan issues, `PLAN REPLAYER` can help preserve the scene and improve the efficiency of diagnosis. However, in some scenarios, the generation of some execution plans cannot be reproduced freely, which makes the diagnosis work more difficult.

    To address such issues, in TiDB v6.6.0, `PLAN REPLAYER` extends the capability of automatic capture. With the `PLAN REPLAYER CAPTURE` command, you can register the target SQL statement in advance and also specify the target execution plan at the same time. When TiDB detects the SQL statement or the execution plan that matches the registered target, it automatically generates and packages the `PLAN REPLAYER` information. When the execution plan is unstable, this feature can improve diagnostic efficiency.

    To use this feature, set the value of [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) to `ON`.

    For more information, see [documentation](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。

* Support persisting statements summary (experimental) [#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx) **tw@shichun-0415**

    Before v6.6.0, statements summary data is kept in memory and would be lost upon a TiDB server restart. Starting from v6.6.0, TiDB supports enabling statements summary persistence, which allows historical data to be written to disks on a regular basis. In the meantime, the result of queries on system tables will derive from disks, instead of memory. After TiDB restarts, all historical data remains available.

    For more information, see [documentation](/statement-summary-tables.md#persist-statements-summary).

### Ecosystem

* <a name="dm-physical" style="text-decoration:none; color:inherit; cursor:default;">TiDB Data Migration (DM) integrates with TiDB Lightning's physical import mode for up to a 10x performance boost for full migration (experimental)</a> <a href="https://github.com/lance6716" target="_blank" referrerpolicy="no-referrer-when-downgrade">@lance6716</a> **tw@ran-huang**

    In v6.6.0, DM's full migration capability integrates with TiDB Lightning's physical import mode, which enables DM to improve the performance of full data migration by up to 10 times, greatly reducing the migration time in large data volume scenarios.

    Before v6.6.0, for high data volume scenarios, you were required to configure TiDB Lightning's physical import task separately for fast full data migration, and then use DM for incremental data migration, which was a complex configuration. Starting from v6.6.0, you can migrate large data volumes without the need to configure TiDB Lightning's tasks; one DM task can accomplish the migration.

    For more information, see [documentation](/dm/dm-precheck.md#physical-import-check-items).

* TiDB Lightning adds a new configuration parameter "header-schema-match" to address the issue of mismatched column names between the source file and the target table <a href="https://github.com/dsdashun">@dsdashun</a>

    In v6.6.0, TiDB Lightning adds a new profile parameter `header-schema-match`. The default value is `true`, which means the first row of the source CSV file is treated as the column name, and consistent with that in the target table. If the field name in the CSV table header does not match the column name of the target table, you can set this configuration to `false`. TiDB Lightning will ignore the error and continue to import the data in the order of the columns in the target table.

    For more information, see [TiDB Lightning (Task)](tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

* TiDB Lightning supports enabling compressed transfers when sending key-value pairs to TiKV [#41163](https://github.com/pingcap/tidb/issues/41163) @[gozssky](https://github.com/gozssky) **tw@qiancai**

    Starting from v6.6.0, TiDB Lightning supports compressing locally encoded and sorted key-value pairs for network transfer when sending them to TiKV, thus reducing the amount of data transferred over the network and lowering the network bandwidth overhead. In the earlier TiDB versions before this feature is supported, TiDB Lightning requires relatively high network bandwidth and incurs high traffic charges in case of large data volume.

    This feature is disabled by default. To enable it, you can set the `compress-kv-pairs` configuration item of TiDB Lightning to "gzip" or "gz".

    For more information, see [documentation](/tidb-lightning-configuration#tidb-lightning-task).

* The TiKV-CDC tool is now GA and supports subscribing to data changes of RawKV [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou) @[haojinming](https://github.com/haojinming) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**

    TiKV-CDC is a CDC (Change Data Capture) tool for TiKV clusters. TiKV and PD can constitute a KV database when used without TiDB, which is called RawKV. TiKV-CDC supports subscribing to data changes of RawKV and replicating them to a downstream TiKV cluster in real time, thus enabling cross-cluster replication of RawKV.

    For more information, see [documentation](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc/).

* TiCDC supports scaling out a single table on Kafka changefeeds and distributing the changefeed to multiple TiCDC nodes [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus) **tw@Oreoxmt**

    Before v6.6.0, when a table in the upstream accepts a large amount of writes, the replication capability of this table cannot be scaled out, resulting in an increase in the replication latency. Starting from TiCDC v6.6.0. the changefeed of an upstream table can be distributed to multiple TiCDC nodes in a Kafka sink, which means the replication capability of a single table is scaled out.

    For more information, see [documentation](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes).

## Compatibility changes

### MySQL compatibility

* Support the MySQL-compatible foreign key constraint [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt**

    For more information, see the [SQL](#sql) section in v6.6.0 Release Notes and [documentation](/sql-statements/sql-statement-foreign-key.md).

* Support the MySQL-compatible multi-valued index [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) **tw@TomShawn**

    For more information, see the [SQL](#sql) section in v6.6.0 Release Notes and [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-index).

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
| `tidb_enable_amend_pessimistic_txn` | Deleted | Starting from v6.5.0, this variable is deprecated. Starting from v6.6.0, this variable and the `AMEND TRANSACTION` feature are deleted. TiDB will use [meta lock](/metadata-lock.md) to avoid the `Information schema is changed` error. |
| `tidb_enable_concurrent_ddl` | Deleted | This variable controls whether to allow TiDB to use concurrent DDL statements. When this variable is disabled, TiDB uses the old DDL execution framework, which provides limited support for concurrent DDL execution. Starting from v6.6.0, this variable is deleted and TiDB no longer supports the old DDL execution framework. |
| `tidb_ttl_job_run_interval` | Deleted | This variable is used to control the scheduling interval of TTL jobs in the background. Starting from v6.6.0, this variable is deleted, because TiDB provides the `TTL_JOB_INTERVAL` attribute for every table to control the TTL runtime, which is more flexible than `tidb_ttl_job_run_interval`. |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks) | Modified | This variable controls whether to enable the foreign key constraint check. The default value changes from `OFF` to `ON`, which means enabling the foreign key check by default. |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630) | Modified | This variable controls whether to enable the foreign key feature. The default value changes from `OFF` to `ON`, which means enabling foreign key by default. |
| `tidb_enable_general_plan_cache` | Modified | This variable controls whether to enable General Plan Cache. Starting from v6.6.0, this variable is renamed to [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache). |
| `tidb_general_plan_cache_size` | Modified | This variable controls the maximum number of execution plans that can be cached by General Plan Cache. Starting from v6.6.0, this variable is renamed to [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size). |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) | Modified | A new value option `learner` is added for this variable to specify the learner replicas with which TiDB reads data from read-only nodes. |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) | Modified | A new value option `prefer-leader` is added for this variable to improve the overall read availability of TiDB clusters. When this option is set, TiDB prefers to read from the leader replica. When the performance of the leader replica significantly decreases, TiDB automatically reads from follower replicas. |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | Modified | This variable is used to control the batch size of the Coprocessor Tasks of the `IndexLookUp` operator. `0` means to disable batch. Starting from v6.6.0, the default value is changed from `0` to `4`, which means 4 Coprocessor tasks will be batched into one task for each batch of requests. |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)  | Newly added |  This variable is used to specify the data compression mode of the MPP Exchange operator. This variable takes effect when TiDB selects the MPP execution plan with the version number `1`. The default value `UNSPECIFIED` means that TiDB automatically selects the `FAST` compression mode. |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660)  | Newly added |  This variable is used to specify different versions of the MPP execution plan. After a version is specified, TiDB selects the specified version of the MPP execution plan. The default value `UNSPECIFIED` means that TiDB automatically selects the latest version `1`. |
| [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-new-in-v660) | Newly added | This variable is used to control whether to enable distributed execution of the DDL reorg phase to improve the speed of this phase. The default value `OFF` means not to enable distributed execution of the DDL reorg phase by default. Currently, this variable takes effect only for `ADD INDEX`. |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit--new-in-v660) | Newly added | Controls whether Prepared Plan Cache caches execution plans that contain `COUNT` after `Limit`. The default value is `ON`, which means Prepared Plan Cache supports caching such execution plans. Note that Prepared Plan Cache does not support caching execution plans with a `COUNT` condition that counts a number greater than 10000. |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | Newly added | This variable controls whether to enable the [`PLAN REPLAYER CAPTURE` feature](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans). The default value `OFF` means to disable the `PLAN REPLAYER CAPTURE` feature. |
| [`tidb_enable_resource_control`](/system-variables.md#tidb-tidb_enable_resource_control-new-in-v660) | New  | Controls whether to enable the resource control feature. The default value is `OFF`. When this variable is set to `ON`, the TiDB cluster supports resource isolation of applications based on resource groups. |
| [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-new-in-v660) | Newly added | Controls whether to use enhanced pessimistic locking wake-up model for pessimistic transactions. The default value `OFF` means not to use such a wake-up model for pessimistic transactions by default. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV  | `enable-statistics` | Deleted | This configuration item specifies whether to enable RocksDB statistics. Starting from v6.6.0, this item is deleted. RocksDB statistics are enabled for all clusters by default to help diagnostics. For details, see [#13942](https://github.com/tikv/tikv/pull/13942). |
| TiKV | `storage.block-cache.shared` | Deleted | Starting from v6.6.0, this configuration item is deleted, and the block cache is enabled by default and cannot be disabled. For details, see [#12936](https://github.com/tikv/tikv/issues/12936). |
| TiKV | `storage.block-cache.block-cache-size` | Modified | Starting from v6.6.0, this configuration item is only used for calculating the default value of `storage.block-cache.capacity`. For details, see [#12936](https://github.com/tikv/tikv/issues/12936). |
| TiFlash |  [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)  |  Modified  |  Specifies the memory usage limit for the generated intermediate data in all queries. Starting from v6.6.0, the default value changes from `0` to `0.8`, which means the limit is 80% of the total memory. |
| TiCDC  | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)  |  Modified  | The path under which redo log backup is stored. Two more value options are added for `scheme`, GCS, and Azure. |
| TiDB | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660) | Newly added | Specifies the SQL script to be executed when the TiDB cluster is started for the first time. The default value is empty. |
| TiDB | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660) | Newly added | Controls whether to enable statements summary persistence. The default value is `false`, which means this feature is not enabled by default. |
| TiDB | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the maximum number of data files that can be persisted. `0` means no limit on the number of files. |
| TiDB | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the maximum number of days to keep persistent data files. |
| TiDB | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the maximum size of a persistent data file (in MiB). |
| TiDB | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the file to which persistent data is written. |
| TiKV | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) | Newly added | Whether to enable scheduling for user foreground read/write requests according to the Request Unit (RU) of the corresponding resource groups. The default value is `false`, which means to disable scheduling according to the RU of the corresponding resource groups. |
| PD  | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-new-in-v660) | Newly added | Controls whether to enable the GOGC tuner, which is disabled by default. |
| PD  | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-new-in-v660) | Newly added | The maximum memory threshold ratio for tuning GOGC. The default value is `0.6`. |
| PD  | [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-new-in-v660) | Newly added | The threshold ratio at which PD tries to trigger GC. The default value is `0.7`. |
| PD  | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-new-in-v660) | Newly added | The memory limit ratio for a PD instance. The value `0` means no memory limit. |
| TiCDC | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameter) | Newly added | Splits a table into multiple replication ranges based on the number of Regions, and these ranges can be replicated by multiple TiCDC nodes. The default value is `50000`. |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning-configuration#tidb-lightning-task) | Newly added | Controls whether to enable compression when sending KV pairs to TiKV in the physical import mode. The default value is empty, meaning that the compression is not enabled. |
| DM | `on-duplicate` |  Deleted | This configuration item controls the methods to resolve conflicts during the full import phase. In v6.6.0, new configuration items `on-duplicate-logical` and `on-duplicate-physical` are introduced to replace `on-duplicate`. |
| DM | [`import-mode`](/dm/task-configuration-file-full.md) |  Modified | The possible values of this configuration item are changed from `"sql"` and `"loader"` to `"logical"` and `"physical"`. The default value is `"logical"`, which means using TiDB Lightning's logical import mode to import data. |
| DM | [`checksum-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item controls whether DM performs `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after the import. The default value is `"required"`, which performs admin checksum after the import. If checksum fails, DM pauses the task and you need to manually handle the failure. |
| DM | [`disk-quota-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item sets the disk quota. It corresponds to the [`disk-quota` configuration](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) of TiDB Lightning. |
| DM | [`on-duplicate-logical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item controls how DM resolves conflicting data in the logical import mode. The default value is `"replace"`, which means using the new data to replace the existing data. |
| DM | [`on-duplicate-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item controls how DM resolves conflicting data in the physical import mode. The default value is `"none"`, which means not resolving conflicting data. `"none"` has the best performance, but might lead to inconsistent data in the downstream database. |
| DM | [`sorting-dir-physical`](/dm/task-configuration-file-full.md) | Newly added | The directory used for local KV sorting in the physical import mode. The default value is the same as the `dir` configuration. |
| sync-diff-inspector | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description) | Newly added | Controls whether to skip checking upstream and downstream data consistency when tables in the downstream do not exist in the upstream.  |
| TiSpark | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-configurations) | Newly added | Controls the type of replicas to be read. The value options are `leader`, `follower`, and `learner`. |
| TiSpark | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-configurations) | Newly added | Sets labels for the target TiKV node. |

### Others

- Support dynamically modifying [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530). This facilitate more flexible TiKV performance tuning.
- Remove the limit on `LIMIT` clauses, thus improving the execution performance.

## Deprecated features

## Improvements

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - Support limiting the global memory to alleviate the OOM problem (experimental) [#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    - Add the GC Tuner to alleviate the GC pressure (experimental) [#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)

+ TiFlash

    - Support an independent MVCC bitmap filter that decouples the MVCC filtering operations in the TiFlash data scanning process, which provides the foundation for future optimization of the data scanning process [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin] **tw@qiancai**
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - Optimize DM alert rules and content [#7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd**

         Previously, alerts similar to "DM_XXX_process_exits_with_error" were raised whenever a related error occured. But some alerts are caused by idle database connections, which can be recovered after reconnecting. To reduce this kind of alerts, DM divides errors into two types: automatically recoverable errors and unrecoverable errors:

        - For an error that is automatically recoverable, DM reports the alert only if the error occurs more than 3 times within 2 minutes.
        - For an error that is not automatically recoverable, DM maintains the original behavior and reports the alert immediately.

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Sync-diff-inspector

        - Add a new parameter `skip-non-existing-table` to control whether to skip checking upstream and downstream data consistency when tables in the downstream do not exist in the upstream [#692](https://github.com/pingcap/tidb-tools/issues/692) @[lichunzhu](https://github.com/lichunzhu) @[liumengya94](https://github.com/liumengya94) **tw@shichun-0415**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that when restoring log backup, hot Regions cause the restore to fail [#37207](https://github.com/pingcap/tidb/issues/37207) @[Leavrth](https://github.com/Leavrth)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning timeout hangs due to TiDB restart in some scenarios [#33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [贡献者 GitHub ID]()

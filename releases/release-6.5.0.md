---
title: TiDB 6.5.0 Release Notes
---

# TiDB 6.5.0 Release Notes

Release date: xx xx, 2022

TiDB version: 6.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.0#version-list)

TiDB 6.5.0 is a Long-Term Support Release (LTS).

相比于前一个 LTS (即 6.1.0 版本)，6.5.0 版本包含 [6.2.0-DMR](/releases/release-6.2.0.md)、[6.3.0-DMR](/releases/release-6.3.0.md)、[6.4.0-DMR](/releases/release-6.4.0.md) 中已发布的新功能、提升改进和错误修复，并引入了以下关键特性：

- 优化器代价模型 V2 GA
- TiDB 全局内存控制 GA
- 全局 hint 干预视图内查询的计划生成
- 满足密码合规审计需求 [密码管理](/password-management.md)
- TiDB 添加索引的速度提升为原来的 10 倍
- Flashback Cluster 功能兼容 TiCDC 和 PiTR
- 支持通过 `INSERT INTO SELECT` 语句[保存 TiFlash 查询结果](/tiflash/tiflash-results-materialization.md)（实验特性）
- 支持下推 JSON 抽取函数下推至 TiFlash
- 进一步增强索引合并[INDEX MERGE](/glossary.md#index-merge)功能

## New features

### SQL

* The performance of TiDB adding indexes is improved by 10 times [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) @[tangenta](https://github.com/tangenta) **tw@Oreoxmt**

    TiDB v6.3.0 introduces the [Add index acceleration](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) as an experimental feature to improve the speed of backfilling when creating an index. In v6.5.0, this feature becomes GA and is enabled by default and the performance improvement is expected to be 10 times faster than before. The acceleration feature is suitable for scenarios where a single SQL statement adds an index serially. When multiple SQL statements add indexes in parallel, only one of the SQL statements will be accelerated.

* Provide lightweight metadata lock to improve the DML success rate during DDL change [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016) **tw@Oreoxmt**

    TiDB v6.3.0 introduces [Metadata lock](/metadata-lock.md) as an experimental feature. To avoid the `Information schema is changed` error caused by DML statements, TiDB coordinates the priority of DMLs and DDLs during table metadata change, and makes executing DDLs wait for the DMLs with old metadata to commit. In v6.5.0, this feature becomes GA and is enabled by default. It is suitable for all types of DDLs change scenarios.

    For more information, see [User document](/metadata-lock.md).

* Support restoring a cluster to a specific point in time by using `FLASHBACK CLUSTER TO TIMESTAMP` [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)  **tw@Oreoxmt**

    TiDB v6.4.0 introduces the [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) statement as an experimental feature. You can use this statement to restore a cluster to a specific point in time within the Garbage Collection (GC) life time. In v6.5.0, this statement becomes GA. This feature helps you to easily undo DML misoperations, restore the original cluster in minutes, rollback data at different time points to determine the exact time when data changes, and it is compatible with PITR and TiCDC.

    For more information, see [User document](/sql-statements/sql-statement-flashback-to-timestamp.md).

* Fully support non-transactional DML statements including `INSERT`, `REPLACE`, `UPDATE`, and `DELETE` [#33485](https://github.com/pingcap/tidb/issues/33485) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt**

    In the scenarios of large data processing, a single SQL statement with a large transaction might have a negative impact on the cluster stability and performance. A non-transactional DML statement is a DML statement split into multiple SQL statements for internal execution. The split statements compromise transaction atomicity and isolation but greatly improve the cluster stability. TiDB supports non-transactional `DELETE` statements since v6.1.0, and v6.5.0 adds support for non-transactional `INSERT`, `REPLACE`, and `UPDATE` statements.

    For more information, see [Non-Transactional DML statements](/non-transactional-dml.md) and [`BATCH` syntax](/sql-statements/sql-statement-batch.md).

* Support time to live (TTL) (experimental feature) [#39262](https://github.com/pingcap/tidb/issues/39262)  @[lcwangchao](https://github.com/lcwangchao) **tw@ran-huang**

    TTL provides row-level data lifetime management. In TiDB, a table with the TTL attribute automatically checks data lifetime and deletes expired data at the row level. TTL is designed to help users clean up unnecessary data periodically and in a timely manner without affecting the online read and write workloads.

    For more information, refer to [user document](/time-to-live.md)

* Support saving TiFlash query results using the `INSERT INTO SELECT` statement (experimental) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi) **tw@qiancai**

    Starting from v6.5.0, TiDB supports pushing down the `SELECT` clause (analysis query) of the `INSERT INTO SELECT` statement to TiFlash. In this way, you can easily save the TiFlash query result to a TiDB table specified by `INSERT INTO` for further analysis, which takes effect as result caching (that is, result materialization). For example:

    ```sql
    INSERT INTO t2 SELECT Mod(x,y) FROM t1;
    ```

    During the experimental phase, this feature is disabled by default. To enable it, you can set the [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) system variable to `ON`. There are no special restrictions on the result table specified by `INSERT INTO` for this feature, and you are free to add a TiFlash replica to that result table or not. Typical usage scenarios of this feature include:

    - Run complex analysis queries using TiFlash
    - Reuse TiFlash query results or deal with highly concurrent online requests
    - Need a relatively small result set comparing with the input data size, recommended to be within 100MiB.

    For more information, see the [user documentation](/tiflash/tiflash-results-materialization.md).

### Security

* Support the password complexity policy [#38928](https://github.com/pingcap/tidb/issues/38928) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw@ran-huang**

    After you enable the password complexity policy for TiDB, when you set a password, TiDB checks the password length, the number of uppercase and lowercase letters, numbers, and special characters, whether the password matches the dictionary, and whether the password matches the username. This ensures that you set a secure password.

    TiDB provides the SQL function [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength) to validate the password strength.

    For more information, refer to [user document](/password-management.md#password-complexity-policy).

* Support the password expiration policy [#38936](https://github.com/pingcap/tidb/issues/38936) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw@ran-huang**

    TiDB supports the password expiration policy, including manual expiration, global-level automatic expiration, and account-level automatic expiration. After this policy is enabled, you must change your passwords periodically. This reduces the risk of password leakage due to long-term use and improve password security.

    For more information, refer to [user document](/password-management.md#password-expiration-policy).

* Support the password reuse policy [#38937](https://github.com/pingcap/tidb/issues/38937) @[keeplearning20221](https://github.com/keeplearning20221) **tw@ran-huang**

    TiDB supports the password reuse policy, including global-level password reuse policy and account-level password reuse policy. After this policy is enabled, you cannot use the passwords that you have used within a period or the most recent several passwords that you have used. This reduces the risk of password leakage due to repeated use of passwords and improves password security.

    For more information, refer to [user document](/password-management.md#password-reuse-policy).

* Support failed-login tracking and temporary account locking policy [#38938](https://github.com/pingcap/tidb/issues/38938) @[lastincisor](https://github.com/lastincisor) **tw@ran-huang**

    After this policy is enabled, if you log in to TiDB with incorrect passwords multiple times consecutively, the account is temporarily locked. After the lock time ends, the account is automatically unlocked.

    For more information, refer to [user document](/password-management.md#failed-login-tracking-and-temporary-account-locking-policy).

### Observability

* TiDB Dashboard 在 Kubernetes 环境支持独立 Pod 部署 [#1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @[SabaPing](https://github.com/SabaPing) **tw@shichun-0415

    TiDB v6.5.0 且 TiDB Operator v1.4.0 之后，在 Kubernetes 上支持将 TiDB Dashboard 作为独立的 Pod 部署。在 TiDB Operator 环境，可直接访问该 Pod 的 IP 来打开 TiDB Dashboard。

    独立部署 TiDB Dashboard 后，用户将获得这些收益：1. 该组件的计算将不会再对 PD 节点有压力，更好的保障集群运行；2. 如果 PD 节点因异常不可访问，也还可以继续使用 Dashboard 进行集群诊断；3. 在开放 TiDB Dashboard 到外网时，不用担心 PD 中的特权端口的权限问题，降低集群的安全风险。

    具体信息，参考 [TiDB Operator 部署独立的 TiDB Dashboard](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/get-started#部署独立的-tidb-dashboard)

### Performance

* 进一步增强索引合并 [INDEX MERGE](/glossary.md#index-merge) 功能 [#39333](https://github.com/pingcap/tidb/issues/39333) @[guo-shaoge](https://github.com/guo-shaoge) @[@time-and-fate](https://github.com/time-and-fate) @[hailanwhu](https://github.com/hailanwhu) **tw@TomShawn**

    新增了对在 WHERE 语句中使用 `AND` 联结的过滤条件的索引合并能力（v6.5 之前的版本只支持 `OR` 连接词的情况），TiDB 的索引合并至此可以覆盖更一般的查询过滤条件组合，不再限定于并集（`OR`）关系。当前版本仅支持优化器自动选择 “OR” 条件下的索引合并，用户须使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) Hint 来开启对于 AND 联结的索引合并。

    关于“索引合并”功能的介绍请参阅 [v5.4 release note](/release-5.4.0#性能), 以及优化器相关的[用户文档](/explain-index-merge.md)

* Support pushing down the following [JSON functions](/tiflash/tiflash-supported-pushdown-calculations.md) to TiFlash [#39458](https://github.com/pingcap/tidb/issues/39458) @[yibin87](https://github.com/yibin87) **tw@qiancai**

    * `->`
    * `->>`
    * `JSON_EXTRACT()`

    The JSON format provides a flexible way to model application design. Therefore, more and more applications are using the JSON format for data exchange and data storage. By pushing down JSON functions to TiFlash, you can improve the efficiency of analyzing data in the JSON type and use TiDB for more real-time analytics scenarios.

* Support pushing down the following [string functions](/tiflash/tiflash-supported-pushdown-calculations.md) to TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**

    * `regexp_like`
    * `regexp_instr`
    * `regexp_substr`

* Support the global Hint to interfere with the execution plan generation in [Views](/views.md) [#37887](https://github.com/pingcap/tidb/issues/37887) @[Reminiscent](https://github.com/Reminiscent) **tw@Oreoxmt**

    In some view access scenarios, you need to use Hints to interfere with the execution plan of the query in the view to achieve best performances. In v6.5.0, TiDB supports adding global Hints for the query blocks in the view, thus the Hints defined in the query can be effective in the view. This feature provides a way to inject Hints into complex SQL statements that contain nested views, enhances the execution plan control, and stabilizes the performance of complex statements. To use global Hints, you need to [name the query blocks](/optimizer-hints.md#step-1-define-the-query-block-name-of-the-view-using-the-qb_name-hint) and [specify Hint references](/optimizer-hints.md#step-2-add-the-target-hints).

    For more information, see [User document](/optimizer-hints.md#hints-that-take-effect-globally).

* Support pushing down the sorting operation of [partitioned-table](/partitioned-table.md) to TiKV [#26166](https://github.com/pingcap/tidb/issues/26166) @[winoros](https://github.com/winoros) **tw@qiancai**

   Although [partitioned table](/partitioned-table.md) has been GA since v6.1.0, TiDB is continually improving its performance. In v6.5.0, TiDB supports pushing down sort operations such as `ORDER BY` and `LIMIT` to TiKV for computation and filtering, which reduces network I/O overhead and improves SQL performance when you use partitioned tables.

* Optimizer introduces a more accurate Cost Model Version 2 [#35240](https://github.com/pingcap/tidb/issues/35240) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt**

    TiDB v6.2.0 introduces the [Cost Model Version 2](/cost-model.md#cost-model-version-2) as an experimental feature. This model uses a more accurate cost estimation method to help the optimizer choose the optimal execution plan. Especially when TiFlash is deployed, Cost Model Version 2 automatically chooses the appropriate storage engine and avoids manual intervention. After real scene testing for a period of time, this model becomes GA in v6.5.0. The newly created cluster uses Cost Model Version 2 by default. For clusters upgrade to v6.5.0, because Cost Model Version 2 might cause changes to query plans, you can set the [`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-new-in-v620) variable to use the new cost model after sufficient performance testing.

    Cost Model Version 2 becomes a generally available feature that significantly improves the overall capability of the TiDB optimizer and evolves towards a more powerful HTAP database.

    For more information, see [User document](/cost-model.md#cost-model-version-2).

* TiFlash 对获取表行数的操作进行针对优化 [#37165](https://github.com/pingcap/tidb/issues/37165) @[elsa0520](https://github.com/elsa0520)

    在数据分析的场景中，通过无过滤条件的 `count(*)` 获取表的实际行数是一个常见操作。 TiFlash 在新版本中优化了 `count(*)` 的改写，自动选择带有“非空”属性的数据类型最短的列进行计数， 可以有效降低 TiFlash 上发生的 I/O 数量，进而提升获取表行数的执行效率。

### Transaction

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### Stability

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiDB 全局内存控制 GA [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12) **tw@TomShawn**

    在 v6.5.0 中，TiDB 中主要的内存消耗都已经能被全局内存控制跟踪到， 当全局内存消耗接近 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 所定义的预设值时，TiDB 会尝试 GC 或取消 SQL 操作等手段限制内存使用，保证 TiDB 的稳定性。

    需要注意的是， 会话中事务所消耗的内存 (由配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 设置最大值) 如今会被内存管理模块跟踪： 当单个会话的内存消耗达到系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidbmemquotaquery) 所定义的阀值时，将会触发系统变量 [tidb-mem-oom-action](/system-variables.md#tidbmemoomaction-span-classversion-mark从-v610-版本开始引入span) 所定义的行为 (默认为 `CANCEL` ，即取消操作)。  为了保证行为向前兼容，当配置 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 为非默认值时， TiDB 仍旧会保证事务使用到这么大的内存而不被取消。

    对于运行 v6.5.0 及以上版本的客户，建议移除配置项 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)，取消对事务内存做单独的限制，转而由系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidbmemquotaquery) 和 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 对全局内存进行管理，从而提高内存的使用效率。

    更多信息，请参考[用户文档](/configure-memory-usage.md)。

### Ease of use

* Refine the execution information of the TiFlash `TableFullScan` operator in the `EXPLAIN ANALYZE` output   [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai**

    The `EXPLAIN ANALYZE` statement is used to print execution plans and runtime statistics. In v6.5.0, TiFlash has refined the execution information of the `TableFullScan` operator by adding the DMFile-related execution information. Now the TiFlash data scan status information is presented more intuitively, which helps you analyze TiFlash performance more easily.

    For more information, see [user documentation](sql-statements/sql-statement-explain-analyze.md).

* Support the output of execution plans in JSON format [#39261](https://github.com/pingcap/tidb/issues/39261) @[fzzf678](https://github.com/fzzf678) **tw@ran-huang**

    In v6.5, TiDB extends the output format of the execution plan. By using `EXPLAIN FORMAT=tidb_json <SQL_statement>`, you can output the SQL execution plan in JSON format. With this capability, SQL debugging tools and diagnostic tools can read the execution plan more conveniently and accurately, thus improving the ease of use of SQL diagnosis and tuning.

    For more information, see [user document](/sql-statements/sql-statement-explain.md).

### MySQL compatibility

* Support a high-performance and globally monotonic `AUTO_INCREMENT` [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao) **tw@Oreoxmt**

    TiDB v6.4.0 introduces the `AUTO_INCREMENT` MySQL compatibility mode as an experimental feature. This mode introduces a centralized auto-increment ID allocating service that ensures IDs monotonically increase on all TiDB instances. This feature makes it easier to sort query results by auto-increment IDs. In v6.5.0, this feature becomes GA. The insert TPS of a table using this feature is expected to exceed 20,000, and this feature supports elastic scaling to improve the write throughput of a single table and entire clusters. To use the MySQL compatibility mode, you need to set `AUTO_ID_CACHE` to `1` when creating a table. The following is an example:

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    For more information, see [User document](/auto-increment.md#mysql-compatibility-mode).

### Data migration

* Support exporting and importing SQL and CSV files in the following compression formats: gzip, snappy and zstd [#38514](https://github.com/pingcap/tidb/issues/38514) @[lichunzhu](https://github.com/lichunzhu) **tw@hfxsd**

    Dumpling supports exporting data to compressed SQL and CSV files in the following compression formats: gzip, snappy, and zstd. TiDB Lightning also supports importing compressed files in these formats.

    Previously, you had to provide large storage space for exporting or importing data to store the uncompressed CSV and SQL files, resulting in high storage costs. With the release of this feature, you can greatly reduce your storage costs by compressing the storage space.

    For more information, see [User document](/dumpling-overview.md#improve-export-efficiency-through-concurrency).

* Optimize binlog parsing capability [#924](https://github.com/pingcap/dm/issues/924) @[gmhdbjd](https://github.com/GMHDBJD) **tw@hfxsd**

    TiDB can filter out binlog events of the schemas and tables that are not in the migration task, thus improving the parsing efficiency and stability. This policy takes effect by default in v6.5.0. No additional configuration is required.

    Previously, even if only a few tables were migrated, the entire binlog file upstream had to be parsed. The binlog events of the tables in the binlog file that did not need to be migrated still had to be parsed, which was not efficient. Meanwhile, if the binlog events of the schemas and tables that are not in the migration task do not support parsing, the task will fail. By only parsing the binlog events of the tables in the migration task, the binlog parsing efficiency can be greatly improved and the task stability can be enhanced.

* The disk quota in TiDB Lightning is GA. It can prevent TiDB Lightning tasks from overwriting local disks [#446](https://github.com/pingcap/tidb-lightning/issues/446) @[buchuitoudegou](https://github.com/buchuitoudegou) **tw@hfxsd**

    You can configure disk quota for TiDB Lightning. When there is not enough disk quota, TiDB Lightning pauses the process of reading the source data and writing temporary files, and writes the sorted key-values to TiKV first, and then continues the import process after TiDB Lightning deletes the local temporary files.

    Previously, when TiDB Lightning imported data using physical mode, it would create a large number of temporary files on the local disk for encoding, sorting, and splitting the raw data. When your local disk ran out of space, TiDB Lightning would exit with an error due to failing to write to the file. With this feature, TiDB Lightning tasks can avoid overwriting the local disk.

    For more information, see [User document](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620).

* Continuous data validation in DM is GA [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd**

    In the process of migrating incremental data from upstream to downstream databases, there is a small probability that the flow of data causes errors or data loss. In scenarios that rely on strong data consistency, such as credit and securities businesses, you can perform a full volume checksum on the data after the data migration is complete to ensure data consistency. However, in some scenarios with incremental replication, upstream and downstream writes are continuous and uninterrupted because the upstream and downstream data is constantly changing, making it difficult to perform consistency checks on all the data in the tables.

    Previously, you needed to interrupt the business to do the full data verification, which would affect your business. Now, with this feature, you can perform incremental data verification without interrupting the business.

    For more information, see [User document](/dm/dm-continuous-data-validation.md).

### TiDB data share subscription

* TiCDC 支持输出 storage sink [tiflow#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu) **tw@shichun-0415**

    TiCDC 支持将 changed log 输出到 S3/Azure Blob Storage/NFS，以及兼容 S3 协议的存储服务中。Cloud Storage 价格便宜，使用方便。对于不希望使用 Kafka 的用户，可以选择使用 storage sink。 TiCDC 将 changed log 保存到文件，然后发送到 storage 中；消费程序定时从 storage 读取新产生的 changed log files 进行处理。

    Storage sink 支持 changed log 格式位 canal-json/csv，此外 changed log 从 TiCDC 同步到 storage 的延迟可以达到 xx，支持更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/12151/files)。

* TiCDC 支持两个或者多个 TiDB 集群之间相互复制 @[asddongmen](https://github.com/asddongmen) **tw@shichun-0415**

    TiCDC 支持在多个 TiDB 集群之间进行双向复制。 如果业务上需要 TiDB 多活，尤其是异地多活的场景，可以使用该功能作为 TiDB 多活的解决方案。只要为每个 TiDB 集群到其他 TiDB 集群的 TiCDC changefeed 同步任务配置 `bdr-mode = true` 参数，就可以实现多个 TIDB 集群之间的数据相互复制。更多信息，请参考[用户文档](/ticdc/ticdc/ticdc-bidirectional-replication.md).

* TiCDC 性能提升 **tw@shichun-0415

    在 TiDB 场景测试验证中， TiCDC 的性能得到了比较大提升，单台 TiCDC 节点能处理的最大行变更吞吐可以达到 30K rows/s，同步延迟降低到 10s，即使在常规的 TiKV/TiCDC 滚动升级场景同步延迟也小于 30s；在容灾场景测试中，打开 TiCDC Redo log 和 Sync point 后，吞吐 xx rows/s 时，容灾复制延迟可以保持在 x s。

### 部署及运维

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### Backup and restore

* TiDB 快照备份支持断点续传 [#38647](https://github.com/pingcap/tidb/issues/38647) @[Leavrth](https://github.com/Leavrth) **tw@shichun-0415

    TiDB 快照备份功能支持断点续传。当 BR 遇到对可恢复的错误时会进行重试，但是超过固定重试次数之后会备份退出。断点续传功能允许对持续更长时间的可恢复故障进行重试恢复，比如几十分钟的的网络故障。

    需要注意的是，如果你没有在 BR 退出后一个小时内完成故障恢复，那么还未备份的快照数据可能会被 GC 机制回收，而造成备份失败。更多信息，请参考[用户文档](/br/br-checkpoint.md)。

* PITR 性能大幅提升提升 **tw@shichun-0415

  PITR 恢复的日志恢复阶单台 TiKV 的恢复速度可以达到 xx MB/s，提升了 x 倍，恢复速度可扩展，有效地降低容灾场景的 RTO 指标；容灾场景的 RPO 优化到 5 min，在常规的集群运维，如滚动升级，单 TiKV 故障等场景下，可以达到 RPO = 5 min 目标。

* TiKV-BR 工具 GA, 支持 RawKV 的备份和恢复 [#67](https://github.com/tikv/migration/issues/67) @[pingyu](https://github.com/pingyu) @[haojinming](https://github.com/haojinming) **tw@shichun-0415**

    TiKV-BR 是一个 TiKV 集群的备份和恢复工具。TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。TiKV-BR 工具支持对使用 RawKV 的产品进行备份和恢复，也支持将 TiKV 集群中的数据从 `API V1` 备份为 `API V2` 数据， 以实现 TiKV 集群 [`api-version`](/tikv-configuration-file.md#api-version-从-v610-版本开始引入) 的升级。

    更多信息，请参考[用户文档](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/)。

## Compatibility changes

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) | 修改 | 该变量默认值从 `1` 修改为 `2`，表示默认使用 Cost Model Version 2 进行索引选择和算子选择。 |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-从-v630-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，表示默认开启元数据锁。 |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，表示默认开启创建索引加速功能。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) |  修改 | 该变量默认值由 `0` 修改为 `80%`，表示默认将 TiDB 实例的内存限制设为总内存的 80%。|
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650) | Newly added | Sets the global policy for automatic password expiration to require the user to change passwords periodically. The default value `0` indicates that the password never expires. |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-new-in-v650) | Newly added | This variable is read-only. It indicates whether to disconnect the client connection when the password is expired.|
| [`password_history`](/system-variables.md#password_history-new-in-v650) | Newly added | This variable is used to establish a password reuse policy that allows TiDB to limit password reuse based on the number of password changes. The default value `0` means disabling the password reuse policy based on the number of password changes. |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650) | Newly added | This variable is used to establish a password reuse policy that allows TiDB to limit password reuse based on time elapsed. The default value `0` means disabling the password reuse policy based on time elapsed. |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-new-in-v650) | Newly added | When this variable is set to a value other than 0, data written in this session is considered to be written by TiCDC. This variable can only be modified by TiCDC. Do not manually modify this variable in any case. |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-从-v650-版本开始引入) | 新增 | 这个变量用来设置索引合并进行交集操作时的最大并发度，仅在以动态裁剪模式访问分区表时有效。 |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) | 修改 | 在 v6.5.0 之前的版本中，该变量用来设置单条查询的内存使用限制。在 v6.5.0 及之后的版本中，该变量用来设置单个会话整体的内存使用限制。 |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-new-in-v650) | Newly added | This variable is used to configure the different cluster IDs in a [bi-directional replication](/ticdc/manage-ticdc.md#bi-directional-replication) cluster.|
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-new-in-v650) | Newly added | This variable is used to set the maximum number of rows that can be deleted in a single `DELETE` transaction in a TTL job. |
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-new-in-v650) | Newly added | This variable is used to limit the rate of `DELETE` statements in TTL jobs on each TiDB node. The value represents the maximum number of `DELETE` statements allowed per second in a single node in a TTL job. When this variable is set to `0`, no limit is applied. |
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-new-in-v650) | Newly added | This variable is used to set the maximum concurrency of TTL jobs on each TiDB node. |
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) | Newly added | This variable is used to control whether the TTL job is enabled. If it is set to `OFF`, all tables with TTL attributes automatically stops cleaning up expired data. |
| [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-new-in-v650) | Newly added | This variable is used to control the scheduling interval of the TTL job in the background. For example, if the current value is set to `1h0m0s`, each table with TTL attributes will clean up expired data once every hour. |
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650) | Newly added | This variable is used to control the start time of the scheduling window of the TTL job in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. |
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650) | Newly added | This variable is used to control the end time of the scheduling window of the TTL job in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. |
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-new-in-v650) | Newly added | This variable is used to set the `LIMIT` value of each `SELECT` statement used to scan expired data in a TTL job. |
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-new-in-v650) | Newly added | This variable is used to set the maximum concurrency of TTL scan jobs on each TiDB node. |
| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password matches the username. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled. The default value is `ON`. |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password matches the dictionary. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `2` (STRONG). The default value is `""`. |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) | Newly added | This variable controls whether to perform password complexity check. If this variable is set to `ON`, TiDB performs the password complexity check when you set a password. The default value is `OFF`. |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password length is sufficient. By default, the minimum password length is `8`. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled. The default value is `8`. |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password contains sufficient uppercase and lowercase letters. This variable takes effect only when [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger. The default value is `1`. |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password contains sufficient numbers. This variable takes effect only when [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger. The default value is `1`. |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) | Newly added | This variable controls the policy for the password complexity check. This variable takes effect only when [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650) is enabled. The default value is `1`. |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-new-in-v650) | Newly added | A check item in the password complexity check. It checks whether the password contains sufficient special characters. This variable takes effect only when [`validate_password.enable`](/system-variables.md#password_reuse_interval-new-in-v650) is enabled and [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger. The default value is `1`. |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) | Newly added | Determines whether TiDB disconnects the client connection when the password is expired. The default value is `true`, which means the client connection is disconnected when the password is expired. |
| TiDB | [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-从-v409-版本开始引入) | 废弃 | 自 v6.5.0 起，该配置项被废弃。请使用 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 系统变量进行设置。 |
| TiKV | [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval) | 修改 | 默认值从 `1s` 修改为 `200ms` |
|          |          |          |          |
|          |          |          |          |

### Others

## 废弃功能

即将于 v6.6.0 版本废弃 v4.0.7 版本引入的 Amending Transaction 机制，并使用[元数据锁](/metadata-lock.md) 替代。

## Improvements

+ TiDB

    - 对于 `bit` and `char` 类型的列，使 `INFORMATION_SCHEMA.COLUMNS` 的显示结果与 MySQL 一致 [#25472](https://github.com/pingcap/tidb/issues/25472) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - The default value of `cdc.min-ts-interval` has been changed from `1s` to `200ms` to reduce CDC latency [#12840](https://github.com/tikv/tikv/issues/12840) @[hicqu](https://github.com/hicqu)
    - Stop writing to Raft Engine when there is insufficient space to avoid exhausting disk space [#13642](https://github.com/tikv/tikv/issues/13642) @[jiayang-zheng](https://github.com/jiayang-zheng)
    - Support pushing down the `json_valid` function to TiKV [#13571](https://github.com/tikv/tikv/issues/13571) @[lizhenhuan](https://github.com/lizhenhuan)
    - Support backing up multiple ranges of data in a single backup request [#13701](https://github.com/tikv/tikv/issues/13701) @[Leavrth](https://github.com/Leavrth)
    - Support backing up data to the Asia Pacific region (ap-southeast-3) of AWS by updating the rusoto library [#13751](https://github.com/tikv/tikv/issues/13751) @[3pointer](https://github.com/3pointer)
    - Reduce pessimistic transaction conflicts [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)
    - Improve recovery performance by caching external storage objects [#13798](https://github.com/tikv/tikv/issues/13798) @[YuJuncen](https://github.com/YuJuncen)
    - The CheckLeader is run in a dedicated thread to reduce TiCDC replication latency [#13774](https://github.com/tikv/tikv/issues/13774) @[overvenus](https://github.com/overvenus)
    - Support pull model for Checkpoints [#13824](https://github.com/tikv/tikv/issues/13824) @[YuJuncen](https://github.com/YuJuncen)
    - Avoid spinning issues on the sender side by updating crossbeam-channel [#13815](https://github.com/tikv/tikv/issues/13815) @[sticnarf](https://github.com/sticnarf)
    - Support batch Coprocessor tasks processing in TiKV [#13849](https://github.com/tikv/tikv/issues/13849) @[cfzjywxk](https://github.com/cfzjywxk)
    - 故障恢复时通知 TiKV 唤醒休眠的 region 以减少等待时间 [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator)
    - 通过代码优化减少内存申请 [#13836](https://github.com/tikv/tikv/pull/13836) @[BusyJay](https://github.com/BusyJay)
    - 引入 raft extension 以提升代码可扩展性 [#13864](https://github.com/tikv/tikv/pull/13864) @[BusyJay](https://github.com/BusyJay)
    - 通过引入 `hint_min_ts` 加速 flashback [#13842](https://github.com/tikv/tikv/pull/13842)  @[JmPotato](https://github.com/JmPotato)
    - tikv-ctl 支持查询某个 key 范围中包含哪些 Region  [#13768](https://github.com/tikv/tikv/pull/13768) [@HuSharp](https://github.com/HuSharp)
    - 改进持续对特定行只加锁但不更新情况下的读写性能 [#13694](https://github.com/tikv/tikv/issues/13694) [@sticnarf](https://github.com/sticnarf)

+ PD

    - Optimize the granularity of locks to reduce lock contention and improve the handling capability of heartbeats under high concurrency [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)
    - Optimize scheduler performance for large-scale clusters and improve production speed of the scheduling policy [#5473](https://github.com/tikv/pd/issues/5473) @[bufferflies](https://github.com/bufferflies)
    - Improve the speed of loading Regions [#5606](https://github.com/tikv/pd/issues/5606) @[rleungx](https://github.com/rleungx)
    - Improve the performance of handling Region heartbeats [#5648](https://github.com/tikv/pd/issues/5648)@[rleungx](https://github.com/rleungx)
    - Add the function to automatically GC the tombstone store [#5348](https://github.com/tikv/pd/issues/5348) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Improve write performance in scenarios where there is no batch processing on the SQL side [#6404](https://github.com/pingcap/tiflash/issues/6404) @[lidezhu](https://github.com/lidezhu)
    - Add more details for TableFullScan in the `explain analyze` output [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + TiDB Dashboard

        - Add three new fields to the slow query page: "Is Prepared?"，"Is Plan from Cache?"，"Is Plan from Binding?" [#1451](https://github.com/pingcap/tidb-dashboard/issues/1451) @[shhdgit](https://github.com/shhdgit)

    + Backup & Restore (BR)

        - 优化清理备份日志数据是 BR 的内存使用 [#38869](https://github.com/pingcap/tidb/issues/38869) @[Leavrth](https://github.com/Leavrth)
        - 提升在恢复时的稳定性，允许 PD leader 切换的情况发生 [#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        - 日志备份的 tls 功能使用 openssl 协议，提升 tls 兼容性。[#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 采用并发的方式对数据进行编码，极大提升了同步到 kafka 的吞吐能力 [#7532](https://github.com/pingcap/tiflow/issues/7532) [#7543](https://github.com/pingcap/tiflow/issues/7543) [#7540](https://github.com/pingcap/tiflow/issues/7540) @[3AceShowHand](https://github.com/3AceShowHand) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - Improve the data replication performance for DM by not parsing the data of tables in the block list [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)
        - Improve the write efficiency of DM relay by using asynchronous write and batch write [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)
        - Optimize the error messages in DM precheck [#7621](https://github.com/pingcap/tiflow/issues/7621) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Improve the compatibility of `SHOW SLAVE HOSTS` for old MySQL versions [#5017](https://github.com/pingcap/tiflow/issues/5017) @[lyzx2001](https://github.com/lyzx2001)

## Bug fixes

+ TiDB

    - 修复 chunk reuse 功能部分情况下内存 chunk 被错误使用的问题 [#38917](https://github.com/pingcap/tidb/issues/38917) @[keeplearning20221](https://github.com/keeplearning20221)
    - 修复 `tidb_constraint_check_in_place_pessimistic` 可能被全局设置影响内部 session 的问题 [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    - 修复了 AUTO_INCREMENT 列无法和 Check 约束一起使用的问题 [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 'insert ignore into' 往 smallint 类型 auto increment 的列插入 string 类型数据会报错的问题 [#38483](https://github.com/pingcap/tidb/issues/38483) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了重命名分区表的分区列操作出现空指针报错的问题 [#38932](https://github.com/pingcap/tidb/issues/38932) @[mjonss](https://github.com/mjonss)
    - 修复了一个修改分区表的分区列导致 DDL 卡死的问题 [#38530](https://github.com/pingcap/tidb/issues/38530) @[mjonss](https://github.com/mjonss)
    - 修复了从 v4.0 升级到 v6.4 后 'admin show job' 操作崩溃的问题 [#38980](https://github.com/pingcap/tidb/issues/38980) @[tangenta](https://github.com/tangenta)
    - 修复了 `tidb_decode_key` 函数未正确处理分区表编码的问题 [#39304](https://github.com/pingcap/tidb/issues/39304) @[Defined2014](https://github.com/Defined2014)
    - 修复了 log rotate 时，grpc 的错误日志信息未被重定向到正确的日志文件的问题 [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - 修复了 `begin; select... for update;` 点查在 read engines 未配置 TiKV 时生成非预期执行计划的问题 [#39344](https://github.com/pingcap/tidb/issues/39344) @[Yisaer](https://github.com/Yisaer)
    - 修复了错误地下推 `StreamAgg` 到 TiFlash 导致结果错误的问题 [#39266](https://github.com/pingcap/tidb/issues/39266) @[fixdb](https://github.com/fixdb)

+ TiKV

    - 修复 raft engine ctl 中的错误 [#13108](https://github.com/tikv/tikv/issues/13108) @[tabokie](https://github.com/tabokie)
    - 修复 tikv-ctl 中 compact raft 命令的错误 [#13515](https://github.com/tikv/tikv/issues/13515) @[guoxiangCN](https://github.com/guoxiangCN)
    - 修复当启用 TLS 时 log backup 无法使用的问题 [#13851](https://github.com/tikv/tikv/issues/13851) @[YuJuncen](https://github.com/YuJuncen)
    - 修复对 Geometry 字段类型的支持 [#13651](https://github.com/tikv/tikv/issues/13651) @[dveeden](https://github.com/dveeden)
    - 修复当未使用 new collation 时 `like` 无法处理 `_` 中非 ASCII 字符的问题 [#13769](https://github.com/tikv/tikv/issues/13769) @[YangKeao](https://github.com/YangKeao)
    - 修复 tikv-ctl 执行 reset-to-version 时出现 segfault 的问题 [#13829](https://github.com/tikv/tikv/issues/13829) @[tabokie](https://github.com/tabokie)

+ PD

    - Fix the issue that the `balance-hot-region-scheduler` configuration is not persisted if not modified [#5701](https://github.com/tikv/pd/issues/5701)  @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that `rank-formula-version` does not retain the pre-upgrade configuration during the upgrade process [#5698](https://github.com/tikv/pd/issues/5698) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - Fix the issue that minor compaction does not work as expected after TiFlash restarts [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that TiFlash Open File OPS is too high [#6345](https://github.com/pingcap/tiflash/issues/6345) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - 修复清理备份日志数据时错误删除数据导致数据丢失的问题 [#38939](https://github.com/pingcap/tidb/issues/38939) @[Leavrth](https://github.com/Leavrth)
        - 修复在大于 6.1 版本关闭 new_collation 设置，仍然恢复失败的问题 [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)
        - 修复因非 s3 存储的不兼容请求导致备份 panic 的问题 [39545](https://github.com/pingcap/tidb/issues/39545) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - 修复 PD leader crash时 CDC 卡住的问题 [#7470](https://github.com/pingcap/tiflow/issues/7470) @[zeminzhou](https://github.com/zeminzhou)
        - 修复在执行drop table 时用户快速暂停恢复同步任务导致可能的数据丢失问题 [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)
        - 兼容上游开启 TiFlash 时版本兼容性问题 [#7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        - 修复下游网络出现故障导致cdc 卡住的问题 [#7706](https://github.com/pingcap/tiflow/issues/7706) @[hicqu](https://github.com/hicqu)
        - 修复用户快速删除、创建同名同步任务可能导致的数据丢失问题 [#7657](https://github.com/pingcap/tiflow/issues/7657) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - Fix the issue that a `task-mode:all` task cannot be started when the upstream database enables GTID mode but does not have any data [#7037](https://github.com/pingcap/tiflow/issues/7037) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that data is replicated for multiple times when a new DM worker is scheduled before the existing worker exits [#7658](https://github.com/pingcap/tiflow/issues/7658) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM precheck is not passed when the upstream database uses regular expression to grant privileges [#7645](https://github.com/pingcap/tiflow/issues/7645) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the memory leakage issue when TiDB Lightning imports a huge source data file [#39331](https://github.com/pingcap/tidb/issues/39331) @[dsdashun](https://github.com/dsdashun)
        - Fix the issue that TiDB Lightning cannot detect conflict correctly when importing data in parallel [#39476](https://github.com/pingcap/tidb/issues/39476) @[dsdashun](https://github.com/dsdashun)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [贡献者 GitHub ID](链接)

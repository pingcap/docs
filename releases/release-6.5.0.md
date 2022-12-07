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
- JSON 抽取函数下推至 TiFlash

## New features

### SQL

* TiDB 添加索引的性能提升为原来的 10 倍 [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037) @[tangenta](https://github.com/tangenta) **tw@Oreoxmt**

    TiDB v6.3.0 引入了[添加索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)作为实验特性，提升了添加索引回填过程的速度。该功能在 v6.5.0 正式 GA 并默认打开，预期大表添加索引的性能提升约为原来的 10 倍。添加索引加速适用于单条 SQL 语句串行添加索引的场景，在多条 SQL 并行添加索引时仅对其中一条添加索引的 SQL 语句生效。

* 提供轻量级元数据锁，提升 DDL 变更过程 DML 的成功率 [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016) **tw@Oreoxmt**

    TiDB v6.3.0 引入了[元数据锁](/metadata-lock.md)作为实验特性，通过协调表元数据变更过程中 DML 语句和 DDL 语句的优先级，让执行中的 DDL 语句等待持有旧版本元数据的 DML 语句提交，尽可能避免 DML 语句的 `Information schema is changed` 错误。该功能在 v6.5.0 正式 GA 并默认打开，适用于各类 DDL 变更场景。

    更多信息，请参考[用户文档](/metadata-lock.md)。

* 支持通过 `FLASHBACK CLUSTER TO TIMESTAMP` 命令将集群快速回退到特定的时间点 [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)  **tw@Oreoxmt**

    TiDB v6.4.0 引入了 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 语句作为实验特性，支持在 Garbage Collection (GC) life time 内快速回退整个集群到指定的时间点。该功能在 v6.5.0 正式 GA，适用于快速撤消 DML 误操作、支持集群分钟级别的快速回退、支持在时间线上多次回退以确定特定数据更改发生的时间，并兼容 PITR 和 TiCDC 等工具。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-flashback-to-timestamp.md)。

* 完整支持包含 `INSERT`、`REPLACE`、`UPDATE` 和 `DELETE` 的非事务 DML 语句 [#33485](https://github.com/pingcap/tidb/issues/33485) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt**

    在大批量的数据处理场景，单一大事务 SQL 处理可能对集群稳定性和性能造成影响。非事务 DML 语句将一个 DML 语句拆成多个 SQL 语句在内部执行。拆分后的语句将牺牲事务原子性和隔离性，但是对于集群的稳定性有很大提升。TiDB 从 v6.1.0 开始支持非事务 `DELETE` 语句，v6.5.0 新增对非事务 `INSERT`、`REPLACE` 和 `UPDATE` 语句的支持。

    更多信息，请参考[非事务 DML 语句](/non-transactional-dml.md) 和 [BATCH](/sql-statements/sql-statement-batch.md)。

* Support time to live (TTL) (experimental feature) [#39262](https://github.com/pingcap/tidb/issues/39262)  @[lcwangchao](https://github.com/lcwangchao) **tw@ran-huang**

    TTL provides row-level data lifetime management. In TiDB, a table with the TTL attribute automatically checks data lifetime and deletes expired data at the row level. TTL is designed to help users clean up unnecessary data periodically and in a timely manner without affecting the online read and write workloads.

    For more information, refer to [user document](/time-to-live.md)

* TiFlash 支持 `INSERT SELECT` 语句（实验功能） [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi) **tw@qiancai**

    用户可以指定 TiFlash 执行 `INSERT SELECT` 中的 `SELECT` 子句（分析查询），并将结果在此事务中写回到 TIDB 表中:

    ```sql
    insert into t2 select mod(x,y) from t1;
    ```

    用户可以方便地保存（物化）TiFlash 的计算结果以供下游步骤使用，可以起到结果缓存（物化）的效果。适用于以下场景：使用 TiFlash 做复杂分析，需重复使用计算结果或响应高并发的在线请求，计算性质本身聚合性好（相对输入数据，计算得出的结果集比较小，推荐 100MB 以内）。作为写入对象的 结果表本身没有特别限制，可以任意选择是否添加 TiFlash 副本。

    更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

### Security

* Support the password complexity policy [#38928](https://github.com/pingcap/tidb/issues/38928) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw@ran-huang**

    After you enable the password complexity policy for TiDB, when you set a password, TiDB checks the password length, the number of uppercase and lowercase letters, numbers, and special characters, whether the password matches the dictionary, and whether the password matches the username. This ensures that you set a secure password.

    TiDB provides the SQL function [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_validate-password-strength) to validate the password strength.

    For more information, refer to [user document](/password-management.md#password-complexity-policy).

* 支持密码过期策略 [#38936](https://github.com/pingcap/tidb/issues/38936) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw@ran-huang**

    TiDB 支持密码过期策略，包括：手动密码过期、全局级别自动密码过期、账户级别自动密码过期。启用密码过期策略功能后，用户必须定期修改密码，防止密码长期使用带来的泄露风险，提高密码安全性。

    更多信息，请参考[用户文档](/password-management.md#密码过期策略)

* 支持密码重用策略 [#38937](https://github.com/pingcap/tidb/issues/38937) @[keeplearning20221](https://github.com/keeplearning20221) **tw@ran-huang**

    TiDB 支持密码重用策略，包括：全局级别密码重用策略、账户级别密码重用策略。启用密码重用策略功能后，用户不允许使用最近一段时间使用过的密码，不允许使用最近几次使用过的密码，以此降低密码的重复使用带来的泄漏风险，提高密码安全性。

    更多信息，请参考[用户文档](/password-management.md#密码重用策略)

* 支持密码连续错误限制登录策略 [#38938](https://github.com/pingcap/tidb/issues/38938) @[lastincisor](https://github.com/lastincisor) **tw@ran-huang**

    TiDB 启用密码连续错误限制登录策略功能后，当用户登录时密码连续多次错误，此时该账户将被临时锁定，达到锁定时间后将自动解锁。

    更多信息，请参考[用户文档](/password-management.md#密码连续错误限制登录策略)

### Observability

* TiDB Dashboard 在 Kubernetes 环境支持独立 Pod 部署 [#1447](https://github.com/pingcap/tidb-dashboard/issues/1447) @[SabaPing](https://github.com/SabaPing) **tw@shichun-0415

    TiDB v6.5.0 且 TiDB Operator v1.4.0 之后，在 Kubernetes 上支持将 TiDB Dashboard 作为独立的 Pod 部署。在 TiDB Operator 环境，可直接访问该 Pod 的 IP 来打开 TiDB Dashboard。

    独立部署 TiDB Dashboard 后，用户将获得这些收益：1. 该组件的计算将不会再对 PD 节点有压力，更好的保障集群运行；2. 如果 PD 节点因异常不可访问，也还可以继续使用 Dashboard 进行集群诊断；3. 在开放 TiDB Dashboard 到外网时，不用担心 PD 中的特权端口的权限问题，降低集群的安全风险。

    具体信息，参考 [TiDB Operator 部署独立的 TiDB Dashboard](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/get-started#部署独立的-tidb-dashboard)

### Performance

* 进一步增强索引合并[INDEX MERGE](/glossary.md#index-merge)功能 [#39333](https://github.com/pingcap/tidb/issues/39333) @[guo-shaoge](https://github.com/guo-shaoge) @[@time-and-fate](https://github.com/time-and-fate) @[hailanwhu](https://github.com/hailanwhu) **tw@TomShawn**

    新增了对在 WHERE 语句中使用 `AND` 联结的过滤条件的索引合并能力（v6.5 之前的版本只支持 `OR` 连接词的情况），TiDB 的索引合并至此可以覆盖更一般的查询过滤条件组合，不再限定于并集（`OR`）关系。当前版本仅支持优化器自动选择 “OR” 条件下的索引合并，用户须使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) Hint 来开启对于 AND 联结的索引合并。

    关于“索引合并”功能的介绍请参阅 [v5.4 release note](/release-5.4.0#性能), 以及优化器相关的[用户文档](/explain-index-merge.md)

* 新增支持下推[JSON 函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#39458](https://github.com/pingcap/tidb/issues/39458) @[yibin87](https://github.com/yibin87) **tw@qiancai**

    * `->`
    * `->>`
    * `JSON_EXTRACT()`

    JSON 格式为应用设计提供了更灵活的建模方式，目前越来越多的应用采用 JSON 格式进行数据交换和数据存储。 把 JSON 函数下推至 TiFlash 可以加速对 JSON 类型数据的分析效率，拓展 TiDB 实时分析的应用场景。TiDB 将持续完善，在未来版本支持更多的 JSON 函数下推至 TiFlash。

* 新增支持下推[字符串函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai**

    * `regexp_like`
    * `regexp_instr`
    * `regexp_substr`

* 新增全局 Hint 干预[视图](/views.md)内查询的计划生成 [#37887](https://github.com/pingcap/tidb/issues/37887) @[Reminiscent](https://github.com/Reminiscent) **tw@Oreoxmt**

    当 SQL 语句中包含对视图的访问时，部分情况下需要用 Hint 对视图内查询的执行计划进行干预，以获得最佳性能。在 v6.5.0 中，TiDB 允许针对视图内的查询块添加全局 Hint，使查询中定义的 Hint 能够在视图内部生效。全局 Hint 由[查询块命名](/optimizer-hints.md#第-1-步使用-qb_name-hint-重命名视图内的查询块)和 [Hint 引用](/optimizer-hints.md#第-2-步添加实际需要的-hint)两部分组成。该特性为包含复杂视图嵌套的 SQL 提供 Hint 的注入手段，增强了执行计划控制能力，进而稳定复杂 SQL 的执行性能。

    更多信息，请参考[用户文档](/optimizer-hints.md#全局生效的-Hint)。

* [分区表](/partitioned-table.md)的排序操作下推至 TiKV [#26166](https://github.com/pingcap/tidb/issues/26166) @[winoros](https://github.com/winoros) **tw@qiancai**

    [分区表](/partitioned-table.md)在 v6.1.0 正式 GA， TiDB 持续提升分区表相关的性能。 在 v6.5.0 中， 排序操作如 `ORDER BY`, `LIMIT` 能够下推至 TiKV 进行计算和过滤，降低网络 I/O 的开销，提升了使用分区表时 SQL 的性能。

* 优化器代价模型 Cost Model Version 2 GA [#35240](https://github.com/pingcap/tidb/issues/35240) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt**

    TiDB v6.2.0 引入了代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2) 作为实验特性，通过更准确的代价估算方式，有利于最优执行计划的选择。尤其在部署了 TiFlash 的情况下，Cost Model Version 2 自动选择合理的存储引擎，避免过多的人工介入。经过一段时间真实场景的测试，这个模型在 v6.5.0 正式 GA。新创建的集群将默认使用 Cost Model Version 2。对于升级到 v6.5.0 的集群，由于 Cost Model Version 2 可能会改变原有的执行计划，在经过充分的性能测试之后，你可以通过设置变量 [`tidb_cost_model_version = 2`](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) 使用新的代价模型。

    Cost Model Version 2 的 GA，大幅提升了 TiDB 优化器的整体能力，并切实地向更加强大的 HTAP 数据库演进。

    更多信息，请参考[用户文档](/cost-model.md#cost-model-version-2)。

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

* 完善 EXPLAIN ANALYZE 输出的 TiFlash 的 TableFullScan 算子的统计信息 [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai**

    [`EXPLAIN ANALYZE`] 语句可以输出执行计划及运行时的统计信息。现有版本的统计信息中，TiFlash 的 TableFullScan 算子统计信息不完善。v6.5.0 版本对 TableFullScan 算子的统计信息进行完善，补充了 dmfile 相关的执行信息，可以更加清晰的展示 TiFlash 的数据扫描状态信息，方便进行性能分析。

    更多信息，请参考[用户文档](sql-statements/sql-statement-explain-analyze.md)。

* 执行计划支持 JSON 格式的打印 [#39261](https://github.com/pingcap/tidb/issues/39261) @[fzzf678](https://github.com/fzzf678) **tw@ran-huang**

    在新版本中，TiDB 扩展了执行计划的打印格式。 通过 `explain format = tidb_json <SQL语句> ` 能够将 SQL 的执行计划以 JSON 格式输出。借助这个能力，SQL 调试工具和诊断工具能够更方便准确地解读执行计划，进而提升 SQL 诊断调优的易用性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain.md)。

### MySQL compatibility

* 支持高性能、全局单调递增的 `AUTO_INCREMENT` 列属性 [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao) **tw@Oreoxmt**

    TiDB v6.4.0 引入了 `AUTO_INCREMENT` 的 MySQL 兼容模式作为实验特性，通过中心化分配自增 ID，实现了自增 ID 在所有 TiDB 实例上单调递增。使用该特性能够更容易地实现查询结果按自增 ID 排序。该功能在 v6.5.0 正式 GA。使用该功能的单表写入 TPS 预期超过 2 万，并支持通过弹性扩容提升单表和整个集群的写入吞吐。要使用 MySQL 兼容模式，你需要在建表时将 `AUTO_ID_CACHE` 设置为 `1`。

    ```sql
    CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
    ```

    更多信息，请参考[用户文档](/auto-increment.md#mysql-兼容模式)。

### Data migration

* 支持导出和导入压缩后的 CSV、SQL 文件 [#38514](https://github.com/pingcap/tidb/issues/38514) @[lichunzhu](https://github.com/lichunzhu) **tw@hfxsd**

    Dumpling 支持将数据导出为 SQL、CSV 的压缩文件，支持 gzip/snappy/zstd 三种压缩格式。Lightning 支持导入压缩后的 SQL、CSV 文件，支持gzip/snappy/zstd 三种压缩格式。

    之前用户导出数据或者导入数据都需要提供较大的存储空间，用于存储导出或者即将导入的非压缩后的 csv 、sql文件，导致存储成本增加。该功能发布后，通过压缩存储空间，可以大大降低用户的存储成本。

    更多信息，请参考[用户文档](https://github.com/pingcap/tidb/issues/38514)。

* 优化了 binlog 解析能力 [#无](无) @[gmhdbjd](https://github.com/GMHDBJD) **tw@hfxsd**

    可将不在迁移任务里的库、表对象的 binlog event 过滤掉不做解析，从而提升解析效率和稳定性。该策略在 6.5 版本默认生效，用户无需额外操作。

    原先用户仅迁移少数几张表，也需要解析上游整个 binlog 文件，即仍需要解析该 binlog 文件中不需要迁移的表的 binlog event，效率会比较低，同时如果不在迁移任务里的库表的 binlog event 不支持解析，还会导致任务失败。通过只解析在迁移任务里的库表对象的 binlog event 可以大大提升 binlog 解析效率，提升任务稳定性。

* Lightning 支持  disk quota 特性 GA，可避免 Lightning 任务写满本地磁盘 [#无](无) @[buchuitoudegou](https://github.com/buchuitoudegou) **tw@hfxsd**

    你可以为 TiDB Lightning 配置磁盘配额 (disk quota)。当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，优先将已经完成排序的 key-value 写入到 TiKV，TiDB Lightning 删除本地临时文件后，再继续导入过程。

    有这个功能之前，TiDB Lightning 在使用物理模式导入数据时，会在本地磁盘创建大量的临时文件，用来对原始数据进行编码、排序、分割。当用户本地磁盘空间不足时，TiDB Lightning 会由于写入文件失败而报错退出。

    更多信息，请参考[用户文档]( https://docs.pingcap.com/tidb/v6.4/tidb-lightning-physical-import-mode-usage#configure-disk-quota-new-in-v620)。

* GA DM 增量数据校验的功能 [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd**

    在将增量数据从上游迁移到下游数据库的过程中，数据的流转有小概率导致错误或者丢失的情况。对于需要依赖于强数据一致的场景，如信贷、证券等业务，你可以在数据迁移完成之后对数据进行全量校验，确保数据的一致性。然而，在某些增量复制的业务场景下，上游和下游的写入是持续的、不会中断的，因为上下游的数据在不断变化，导致用户难以对表里面的全部数据进行一致性校验。

    过去，需要中断业务，做全量数据校验，会影响用户业务。现在推出该功能后，在一些不可中断的业务场景，无需中断业务，通过该功能就可以实现增量数据校验。

    更多信息，请参考[用户文档]( https://docs.pingcap.com/tidb/v6.4/dm-continuous-data-validation)。

### TiDB data share subscription

* TiCDC 支持输出 storage sink [tiflow#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu) **tw@shichun-0415**

    TiCDC 支持将 changed log 输出到 S3/Azure Blob Storage/NFS，以及兼容 S3 协议的存储服务中。Cloud Storage 价格便宜，使用方便。对于不希望使用 Kafka 的用户，可以选择使用 storage sink。 TiCDC 将 changed log 保存到文件，然后发送到 storage 中；消费程序定时从 storage 读取新产生的 changed log files 进行处理。

    Storage sink 支持 changed log 格式位 canal-json/csv，此外 changed log 从 TiCDC 同步到 storage 的延迟可以达到 xx，支持更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/12151/files)。

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

    TiKV-BR 是一个 TiKV 集群的备份和恢复工具。TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。TiKV-BR 工具支持对使用 RawKV 的产品进行备份和恢复，也支持将 TiKV 集群中的数据从 `API V1` 备份为 `API V2` 数据， 以实现 TiKV 集群 [`api-version`](https://docs.pingcap.com/zh/tidb/v6.4/tikv-configuration-file#api-version-%E4%BB%8E-v610-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) 的升级。

    更多信息，请参考[用户文档]( https://tikv.org/docs/dev/concepts/explore-tikv-features/backup-restore/ )。

## Compatibility changes

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) | 修改 | 该变量默认值从 `1` 修改为 `2`，表示默认使用 Cost Model Version 2 进行索引选择和算子选择。 |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-从-v630-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，表示默认开启元数据锁。 |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) | 修改 | 该变量默认值从 `OFF` 修改为 `ON`，表示默认开启创建索引加速功能。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) |  修改 | 该变量默认值由 `0` 修改为 `80%`，表示默认将 TiDB 实例的内存限制设为总内存的 80%。|
| [`default_password_lifetime`](/system-variables.md#default_password_lifetime-从-v650-版本开始引入) | 新增 | 用于设置全局自动密码过期策略，要求用户定期修改密码。默认值为 `0` ，表示禁用全局自动密码过期策略 |
| [`disconnect_on_expired_password`](/system-variables.md#disconnect_on_expired_password-从-v650-版本开始引入) | 新增 | 该变量是一个只读变量，用来显示 TiDB 是否会直接断开密码已过期用户的连接 |
| [`password_history`](/system-variables.md#password_history-从-v650-版本开始引入) | 新增 | 基于密码更改次数的密码重用策略，不允许用户重复使用最近设置次数内使用过的密码。默认值为 `0`，表示禁用基于密码更改次数的密码重用策略 |
| [`password_reuse_interval`](/system-variables.md#password_reuse_interval-从-v650-版本开始引入) | 新增 | 基于经过时间限制的密码重用策略，不允许用户重复使用最近设置天数内使用过的密码。默认值为 `0`，表示禁用基于密码更改次数的密码重用策略 |
| [`tidb_cdc_write_source`](/system-variables.md#tidb_cdc_write_source-从-v650-版本开始引入) | 新增 | 当变量非 `0` 时，该 SESSION 写入的数据将被视为是由 TiCDC 写入的。这个变量仅由 TiCDC 设置，任何时候都不应该手动调整该变量。 |
| [`tidb_index_merge_intersection_concurrency`](/system-variables.md#tidb_index_merge_intersection_concurrency-从-v650-版本开始引入) | 新增 | 这个变量用来设置索引合并进行交集操作时的最大并发度，仅在以动态裁剪模式访问分区表时有效。 |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) | 修改 | 在 v6.5.0 之前的版本中，该变量用来设置单条查询的内存使用限制。在 v6.5.0 及之后的版本中，该变量用来设置单个会话整体的内存使用限制。 |
| [`tidb_source_id`](/system-variables.md#tidb_source_id-从-v650-版本开始引入) | 新增 | 设置在[双向复制](/ticdc/ticdc-bidirectional-replication.md)系统内不同集群的 ID。|
| [`tidb_ttl_delete_batch_size`](/system-variables.md#tidb_ttl_delete_batch_size-从-v650-版本开始引入) | 新增 | 这个变量用于设置 TTL 任务中单个删除事务中允许删除的最大行数。|
| [`tidb_ttl_delete_rate_limit`](/system-variables.md#tidb_ttl_delete_rate_limit-从-v650-版本开始引入) | 新增 | 这个变量用来对每个 TiDB 节点的 TTL 删除操作进行限流。其值代表了在 TTL 任务中单个节点每秒允许 `DELETE` 语句执行的最大次数。当此变量设置为 `0` 时，则表示不做限制。|
| [`tidb_ttl_delete_worker_count`](/system-variables.md#tidb_ttl_delete_worker_count-从-v650-版本开始引入) | 新增 | 这个变量用于设置每个 TiDB 节点上 TTL 删除任务的最大并发数。|
| [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-从-v650-版本开始引入) | 新增 | 这个变量用于控制是否启动 TTL 后台清理任务。如果设置为 `OFF`，所有具有 TTL 属性的表会自动停止清理过期数据。|
| [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-从-v650-版本开始引入) | 新增 | 这个变量用于控制 TTL 后台清理任务的调度周期。比如，如果当前值设置成了 `1h0m0s`，则代表每张设置了 TTL 属性的表会每小时清理一次过期数据。|
| [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-从-v650-版本开始引入) | 新增 | 这个变量用于控制 TTL 后台清理任务的调度窗口的起始时间。请谨慎调整此参数，过小的窗口有可能会造成过期数据的清理无法完成。|
| [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-从-v650-版本开始引入) | 新增 | 这个变量用于控制 TTL 后台清理任务的调度窗口的结束时间。请谨慎调整此参数，过小的窗口有可能会造成过期数据的清理无法完成。|
| [`tidb_ttl_scan_batch_size`](/system-variables.md#tidb_ttl_scan_batch_size-从-v650-版本开始引入) | 新增 | 这个变量用于设置 TTL 任务中用来扫描过期数据的每个 `SELECT` 语句的 `LIMIT` 的值。|
| [`tidb_ttl_scan_worker_count`](/system-variables.md#tidb_ttl_scan_worker_count-从-v650-版本开始引入) | 新增 | 这个变量用于设置每个 TiDB 节点 TTL 扫描任务的最大并发数。|

| [`validate_password.check_user_name`](/system-variables.md#validate_passwordcheck_user_name-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，设置的用户密码不允许密码与当前会话账户的用户名部分相同。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。默认值为 `ON` |
| [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，密码字典功能，设置的用户密码不允许包含字典中的单词。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 设置为 `2` (STRONG) 时，该变量才生效。默认值为空 |
| [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查的开关，设置为 `ON` 后，TiDB 才进行密码复杂度检查。默认值为 `OFF` |
| [`validate_password.length`](/system-variables.md#validate_passwordlength-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码最小长度。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。默认值为 8 |
| [`validate_password.mixed_case_count`](/system-variables.md#validate_passwordmixed_case_count-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码中大写字符和小写字符的最小数量。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 大于或等于 `1` (MEDIUM) 时，该变量才生效。默认值为 1 |
| [`validate_password.number_count`](/system-variables.md#validate_passwordnumber_count-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码中数字字符的最小数量。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 大于或等于 `1` (MEDIUM) 时，该变量才生效。默认值为 1 |
| [`validate_password.policy`](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查的强度，强度等级分为 `[0, 1, 2]` 。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。默认值为 1 |
| [`validate_password.special_char_count`](/system-variables.md#validate_passwordspecial_char_count-从-v650-版本开始引入) | 新增 | 密码复杂度策略检查项，限定了用户密码中特殊字符的最小数量。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 大于或等于 `1` (MEDIUM) 时，该变量才生效。默认值为 1 |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password`-从-v650-版本开始引入) | 新增 | 该配置用于控制 TiDB 服务端是否直接断开密码已过期用户的连接，默认值为 "true" ，表示 TiDB 服务端将直接断开密码已过期用户的连接 |
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
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - tikv-ctl 支持查询某个 key 范围中包含哪些 Region  [#13768](https://github.com/tikv/tikv/pull/13768) [@HuSharp](https://github.com/HuSharp)
    - 改进持续对特定行只加锁但不更新情况下的读写性能 [#13694](https://github.com/tikv/tikv/issues/13694) [@sticnarf](https://github.com/sticnarf)
+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 提升了 TiFlash 在 SQL 端没有攒批的场景的写入性能 [#6404](https://github.com/pingcap/tiflash/issues/6404) @[lidezhu](https://github.com/lidezhu)
    - 增加了 TableFullScan 的输出信息 [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + TiDB Dashboard

        - 在慢查询页面新增三个字段 `是否由 prepare 语句生成`，`查询计划是否来自缓存`，`查询计划是否来自绑定` 的描述。 [#1445](https://github.com/pingcap/tidb-dashboard/pull/1445/files) @[shhdgit](https://github.com/shhdgit)

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

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

    - 修复 chunk reuse 功能部分情况下内存 chunk 被错误使用的问题 [#38917](https://github.com/pingcap/tidb/issues/38917) @[keeplearning20221](https://github.com/keeplearning20221)
    - 修复 `tidb_constraint_check_in_place_pessimistic` 可能被全局设置影响内部 session 的问题 [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    - 修复了 AUTO_INCREMENT 列无法和 Check 约束一起使用的问题 [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 'insert ignore into' 往 smallint 类型 auto increment 的列插入 string 类型数据会报错的问题 [#38483](https://github.com/pingcap/tidb/issues/38483) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了重命名分区表的分区列操作出现空指针报错的问题 [#38932](https://github.com/pingcap/tidb/issues/38932) @[mjonss](https://github.com/mjonss)
    - 修复了一个修改分区表的分区列导致 DDL 卡死的问题 [#38530](https://github.com/pingcap/tidb/issues/38530) @[mjonss](https://github.com/mjonss)
    - 修复了从 v4.0 升级到 v6.4 后 'admin show job' 操作崩溃的问题 [#38980](https://github.com/pingcap/tidb/issues/38980) @[tangenta](https://github.com/tangenta)
    - 修复了 `tidb_decode_key` 函数未正确处理分区表编码的问题 [#39304](https://github.com/pingcap/tidb/issues/39304) @[Defined2014](https://github.com/Defined2014)
    - 修复了 log rotate 时，grpc 的错误日志信息未被重定向到正确的日志文件的问题 [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 修复 TiFlash 重启不能正确合并小文件的问题 [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)
    - 修复 TiFlash Open File OPS 过高的问题 [#6345](https://github.com/pingcap/tiflash/issues/6345) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

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

We would like to thank the following contributors from the TiDB community:

- [贡献者 GitHub ID](链接)

---
title: TiDB 7.4.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.4.0.
---

# TiDB 7.4.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.4.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.4/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.4.0#version-list)

7.4.0 introduces the following key features and improvements:

<!-- key feature placeholder-->

## Feature details

### Scalability

* TiDB introduces the ability to set the TiDB Service Scope to select the applicable TiDB nodes to perform concurrent `ADD INDEX` or `IMPORT INTO` tasks (experimental) [#46453](https://github.com/pingcap/tidb/pull/46453) @[ywqzzy](https://github.com/ywqzzy) **tw@hfxsd** <!--1505-->

    Executing `ADD INDEX` or `IMPORT INTO` tasks in parallel in a resource-intensive cluster can consume a large amount of TiDB node resources, which can lead to cluster performance degradation. TiDB v7.4.0 introduces the ability to set the TiDB Service Scope as an experimental feature. You can select a few existing TiDB nodes or set the TiDB Service Scope for new TiDB nodes, and all parallel `ADD INDEX` and `IMPORT INTO` tasks only run on these nodes. This mechanism can avoid performance impact on existing services.
    
    For details, see [user document](/system-variables.md#tidb_service_scope-new-in-v740).
### Performance

- note 1

* Introduce cloud storage-based global sort capability to improve the performance and stability of `ADD INDEX` and `IMPORT INTO` tasks in parallel execution [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) **tw@ran-huang** <!--1456-->

    Before v7.4.0, when executing tasks like `ADD INDEX` or `IMPORT INTO` in the distributed parallel execution framework, each TiDB node needs to allocate a significant amount of local disk space for sorting encoded index KV pairs and table data KV pairs. However, due to the lack of global sorting capability, there might be overlapping data between different TiDB nodes and within each individual node during the process. As a result, TiKV has to constantly perform compaction operations while importing these KV pairs into its storage engine, which impacts the performance and stability of `ADD INDEX` and `IMPORT INTO`.

    In v7.4.0, TiDB introduces the [Global Sort](/tidb-global-sort.md) feature. Instead of writing the encoded data locally and sorting it there, the data is now written to cloud storage for global sorting. Once sorted, both the indexed data and table data are imported into TiKV in parallel, thereby improving performance and stability.

    For details, see [user document](/tidb-global-sort.md)。

* Improve the performance of adding multiple indexes in a single SQL statement by optimizing parallel multi schema change [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@ran-huang** <!--1307-->

    Before v7.4.0, when you use parallel multi schema change to commit multiple `ADD INDEX` operations in a single SQL statement, the performance is the same as using multiple independent SQL statements for `ADD INDEX` operations. However, after optimization in v7.4.0, the performance of adding multiple indexes in a single SQL statement has been greatly improved.

    For details, see [user document](链接)。

### Reliability

* Introduce a configurable TiKV read timeout [#45380](https://github.com/pingcap/tidb/issues/45380) @[crazycs520](https://github.com/crazycs520) **tw@hfxsd** <!--1560-->

    Normally, TiKV processes requests very quickly, in a matter of milliseconds. However, when a TiKV node encounters disk I/O jitter or network latency, the request processing time can increase significantly. In versions earlier than v7.4.0, the timeout limit for TiKV requests was fixed and could not be adjusted, so TiDB had to wait for a timeout response when there was a problem with a TiKV node, which resulted in a noticeable impact on application query performance during jitter.
     
    TiDB v7.4.0 introduces a new system variable [`TIDB_KV_READ_TIMEOUT(N)`](/system-variables.md#tidb_kv_read_timeout-new-in-v740), which lets you customize the timeout for RPC read requests that TiDB sends to TiKV in a query statement. It means that when the request sent to a TiKV node is delayed due to disk or network issues, TiDB can time out faster and resend the request to other TiKV nodes, thus reducing query latency. If the requests time out for all TiKV nodes, TiDB will retry using the default timeout. This system variable also supports setting the timeout for TiDB to send TiKV RPC read requests in query statements via the hint [`TIDB_KV_READ_TIMEOUT(N)`](/optimizer-hints.md#tidb_kv_read_timeoutn) to set the timeout for TiDB to send TiKV RPC read requests in query statements. This enhancement gives TiDB the flexibility to adapt to unstable network or storage environments, improving query performance and enhancing the user experience.

    For details, see [user document](/system-variables.md#tidb_kv_read_timeout-new-in-v740).

* Add the option of optimizer mode [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1527-->

    In v7.4.0, TiDB introduces a new system variable [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740), which controls the estimation method used by the optimizer. The default value `moderate` maintains the previous behavior of the optimizer, where it uses runtime statistics to adjust estimations based on data modifications. If this variable is set to `determinate`, the optimizer generates execution plans solely based on statistics without considering runtime corrections.

    For long-term stable OLTP applications or situations where you are confident in the existing execution plans, it is recommended to switch to `determinate` mode after testing. This reduces potential plan changes.

    For details, see [user document](/system-variables.md#tidb_opt_objective-new-in-v740)。



* Enhance the ability to lock statistics [#issue号](链接) @[hi-rustin](https://github.com/hi-rustin) **tw@ran-huang** <!--1557-->

    In v7.4.0, TiDB has enhanced the ability to [lock statistics](/statistics.md#lock-statistics). Now, to ensure operational security, locking and unlocking statistics require the same privileges as collecting statistics. In addition, TiDB supports locking and unlocking statistics for specific partitions, providing greater flexibility. If you are confident in queries and execution plans in the database and want to prevent any changes from occurring, you can lock statistics to enhance stability.

    For details, see [user document](/statistics.md#锁定统计信息)。


### SQL

- note 1

- note 2

### DB operations

- note 1

- note 2

### Observability

* Support adding session connection IDs and session aliases to logs [#46071](https://github.com/pingcap/tidb/issues/46071) @[lcwangchao](https://github.com/lcwangchao) **tw@hfxsd** <!--无 FD 及用户文档，只提供 release notes-->
   
     When you're troubleshooting SQL execution problems, it's often necessary to correlate the contents of TiDB's component logs to pinpoint the root cause of the problem. Starting with v7.4.0, you can write session connection IDs (`CONNECTION_ID`) to session-related logs, including TiDB logs, slow query logs, and slow logs from the coprocessor on TiKV. You can correlate the contents of several types of logs based on session connection IDs to improve troubleshooting and diagnostic efficiency. 

     In addition, by setting the session-level system variable [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740), you can add custom identifiers to the logs mentioned above. With this ability to inject business identification information into the logs, you can correlate the contents of the logs with the business, build the link from the business to the logs, and reduce the difficulty of diagnostic work.     

- note 2

### Data migration

* Data Migration (DM) supports blocking incompatible (data-consistency-corrupting) DDL changes (experimental) [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1523-->

     Prior to v7.4.0, the Binlog Filter function using DM has a coarse granularity. For example, it can only filter DDL events with a large granularity such as `ALTER`, which is limited in some business scenarios. For example, you can only increase the precision of the decimal field type, but cannot decrease it.
     
     TiDB v7.4.0 introduces a new event name `incompatible DDL changes`, which is used to intercept DDLs whose changes will lead to data loss, data truncation, or loss of precision. It also reports error alerts, so that you can intervene in time to deal with them to avoid the impact on downstream business data.
     
     For details, see [user document](待补充).

* Support real-time update of checkpoint for continuous data validation [#issue号](链接) @[lichunzhu](https://github.com/lichunzhu) **tw@ran-huang** <!--1496-->

    Before v7.4.0, the continuous data validation feature is used to ensure the consistency of data replication from DM to downstream with upstream. This serves as the basis for cutting over business traffic from the upstream database to TiDB. However, due to various factors such as replication delay and waiting for re-validation of inconsistent data, the continuous validation checkpoint must be refreshed every few minutes. This is unacceptable for some business scenarios where the cutover time is limited to a few tens of seconds.

    With the introduction of real-time updating of checkpoint for continuous data validation, you can now provide the binlog position from the upstream database. Once the continuous validation program detects this binlog position in memory, it will immediately refresh the checkpoint instead of refreshing it every few minutes. Therefore, you can quickly perform cut-off operations based on this immediately updated checkpoint.

    For details, see [user document](链接)。
    
* Dumpling supports the user-defined terminator when exporting data to CSV files [#issue](https:// ) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1571-->

    Prior to v7.4.0, when Dumpling exported data to a CSV file, the default terminator is "\r\n", which could not be parsed by some downstream systems that could only parse the "\n" terminator , or had to be converted by a third-party tool to parse the CSV file. 
    
    Starting from v7.4.0, a new parameter `--csv-line-terminator` is introduced. This parameter allows you to pass in the required terminator when exporting data to a CSV file. This parameter supports `\r\n' and `\n'. The default terminator is `\r\n' to keep consistent with earlier versions.
     
    For details, see [user document](待补充).

* TiCDC supports replicating data to Pulsar [#9413](https://github.com/pingcap/tiflow/issues/9413) @[yumchina](https://github.com/yumchina) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1552-->

    TiCDC now supports seamless integration with Pulsar. Pulsar is a cloud-native and distributed message streaming platform that enhances your real-time data streaming experience. With this new capability, TiCDC provides you with the ability to easily capture and replicate TiDB changes to Pulsar, offering new possibilities for data processing and analytics capabilities. You can develop your own consumer applications that read and process newly generated change data from Pulsar to meet specific business needs. TiCDC currently supports replicating change data in the `canal-json` format.

    For details, see [user document](/ticdc/ticdc-sink-to-pulsar.md).


- TiCDC improves large message handling with claim check pattern [#9153](https://github.com/pingcap/tiflow/issues/9153) @[3AceShowHand](https://github.com/3AceShowHand) **tw@ran-huang** <!--1550 英文 comment 原文 https://internal.pingcap.net/jira/browse/FD-1550?focusedCommentId=149207&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-149207-->

    Before v7.4.0, TiCDC is unable to send large messages exceeding the maximum message size  (`max.message.bytes`) of Kafka to downstream. Starting from v7.4.0, when configuring a changefeed with Kafka as the downstream, you can specify an external storage location for storing the large message, and send a reference message containing the address of the large message in the external storage to Kafka. When consumers receive this reference message, they can retrieve the message content from the external storage address. 
    
    For details, see [user document]().

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.3.0 to the current version (v7.4.0). If you are upgrading from v7.2.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

* Starting with v7.4.0, TiDB is compatible with core MySQL 8.0 features, and `version()` returns the version prefixed with `8.0.11`.  

### Behavior changes

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
|    |   |    |  |

## Deprecated features

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

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

- [yumchina](https://github.com/yumchina)

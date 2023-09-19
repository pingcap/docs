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

### Performance

- note 1

* Introduce cloud-based global sorting capability to improve the performance and stability of parallel execution tasks such as `ADD INDEX` or `IMPORT INTO` [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) **tw@ran-huang** <!--1456-->

    Before v7.4.0, when executing distributed parallel execution framework tasks like `ADD INDEX` or `IMPORT INTO`, TiDB nodes need to prepare a large local disk for sorting encoded index KV pairs and table data KV pairs. Due to the inability to sort from a global perspective, there might be overlapping data between different TiDB nodes and within each node during import. This would cause TiKV to constantly perform compaction operations when importing these KV pairs into TiKV, reducing the performance and stability of `ADD INDEX` or `IMPORT INTO`.

    With the introduction of the global sorting feature in v7.4.0, the encoded data is now written to cloud storage instead of being written locally and sorted. Global sorting is performed in cloud storage, and then the indexed data and table data that have undergone global sorting are imported into TiKV in parallel, thereby improving performance and stability.

    For details, see [user document](/tidb-global-sort.md)。

* Optimize parallel multi schema change to improve the performance of adding multiple indexes in a single SQL statement [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@ran-huang** <!--1307-->

    Before v7.4.0, when you use parallel multi schema change to commit multiple `ADD INDEX` operations in a single SQL statement, the performance is the same as using multiple independent SQL statements for `ADD INDEX` operations. After optimization in v7.4.0, the performance of adding multiple indexes in a single SQL statement has been greatly improved.

    For details, see [user document](链接)。

### Reliability

- note 1

* Add the option of optimizer mode [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1527-->

    In v7.4.0, TiDB introduce a new system variable [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740), which controls the estimation method of the optimizer. The default value `moderate` maintains the previous behavior of the optimizer, where it uses runtime statistics to correct estimations based on data modifications. If this system variable is set to `determinate`, the optimizer generates execution plans solely based on statistics without considering runtime corrections.

    For long-term stable OLTP applications or situations where you are confident about existing execution plans, it is recommended to switch to `determinate` mode after testing. This reduces potential plan changes.

    For details, see [user document](/system-variables.md#tidb_opt_objective-new-in-v740)。



* Enhance the ability to lock statistics [#issue号](链接) @[hi-rustin](https://github.com/hi-rustin) **tw@ran-huang** <!--1557-->

    In v7.4.0, TiDB has enhanced the ability to lock [statistics](/statistics.md#lock-statistics). Now, to ensure operational security, locking and unlocking statistics require the same privileges as granting and collecting statistics. In addition, TiDB also supports locking and unlocking statistics information for specific partitions, improving flexibility. When you have confidence in queries and execution plans in the database and do not want any changes to occur, you can lock statistics to enhance stability.

    For details, see [user document](/statistics.md#锁定统计信息)。


### SQL

- note 1

- note 2

### DB operations

- note 1

- note 2

### Observability

- note 1

- note 2

### Data migration

- note 1

* Support real-time update of checkpoint for incremental data validation [#issue号](链接) @[lichunzhu](https://github.com/lichunzhu) **tw@ran-huang** <!--1496-->

    Before v7.4.0, the incremental data validation feature is used to determine whether the data replication from DM to downstream is consistent with upstream. This is used as the basis for cutting over business traffic from upstream database to TiDB. However, due to various factors such as replication delay and waiting for re-validation of inconsistent data, the incremental validation checkpoint must be refreshed every few minutes. This is unacceptable for some business scenarios where the cutover time is only a few tens of seconds.

    With the introduction of real-time updating of checkpoint for incremental data validation, you can pass in the binlog position filled in by the upstream database. Once the incremental validation program detects this binlog position in memory, it will immediately refresh the checkpoint instead of refreshing it every few minutes. Therefore, you can quickly perform cut-off operations based on this immediately returned checkpoint.

    For details, see [user document](链接)。
    
    


- TiCDC improves large message handling with claim check pattern [#9153](https://github.com/pingcap/tiflow/issues/9153) @[3AceShowHand](https://github.com/3AceShowHand) **tw@ran-huang** <!--1550 英文 comment 原文 https://internal.pingcap.net/jira/browse/FD-1550?focusedCommentId=149207&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-149207-->

    Before v7.4.0, TiCDC was not able to send large messages downstream to the Kafka broker that would have exceeded Kafkas maximum message size. Starting from v7.4.0, TiCDC allows for users to configure an external storage location where these large messages can be stored. Instead of the large message, a reference (or claim check) is used in the message and sent downstream to the Kafka broker. Message consumers can then retrieve the message content from the external storage location when needed. 
    
    See[documentation for further details]

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.3.0 to the current version (v7.4.0). If you are upgrading from v7.2.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

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

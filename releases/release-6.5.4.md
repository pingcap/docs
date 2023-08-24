---
title: TiDB 6.5.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.4.
---

# TiDB 6.5.4 Release Notes

Release date: xxxx, 2023

TiDB version: 6.5.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.4#version-list)

## Improvements

+ TiDB <!-- tw: Oreoxmt 1-->

    - Optimize the performance of `LOAD DATA` statements that contain assignment expressions [#46081](https://github.com/pingcap/tidb/issues/46081) @[gengliqi](https://github.com/gengliqi)
    - (dup): Optimize the performance of reading the dumped chunks from disk [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)

+ TiKV <!-- tw: Oreoxmt 9-->

    - (dup): Use gzip compression for `check_leader` requests to reduce traffic [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - (dup): Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get_region_read_progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    <!-- tw: ran-huang 1-->
    - Expose some RocksDB configurations in TiKV that allow users to disable features such as TTL and periodic compaction [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!-- tw: ran-huang 5-->

    (dup)- Support blocking the Swagger API by default when the Swagger server is not enabled [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    (dup)- Improve the high availability of etcd [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    (dup)- Reduce the memory consumption of `GetRegions` requests [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)
    - Support reusing HTTP connections [#6913](​https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)
    - Add a new `halt-scheduling` configuration item to suspend PD scheduling [#6493](https://github.com/tikv/pd/issues/6493) @[JmPotato](https://github.com/JmPotato)

+ TiFlash <!-- tw: ran-huang 3-->

    - Improve TiFlash write performance through IO batch optimization [#7735](https://github.com/pingcap/tiflash/issues/7735) @[lidezhu](https://github.com/lidezhu)
    - Improve TiFlash write performance by removing unnecessary fsync operations [#7736](https://github.com/pingcap/tiflash/issues/7736) @[lidezhu](https://github.com/lidezhu)
    - Limit the maximum length of the TiFlash coprocessor task queue to avoid excessive queuing of coprocessor tasks, which impacts TiFlash's service availability [#7747](https://github.com/pingcap/tiflash/issues/7747) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR) <!-- tw: ran-huang 3-->

        - Enhance support for connection reuse by setting `MaxIdleConns` and `MaxIdleConnsPerHost` parameters in the HTTP client [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - Improve fault tolerance of BR when it fails to connect to PD or external S3 storage [#42909](https://github.com/pingcap/tidb/issues/42909) @[Leavrth](https://github.com/Leavrth)
        - Add a new restore parameter `WaitTiflashReady`. When this parameter is enabled, the restore operation will be completed after TiFlash replicas are successfully replicated [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)

    + TiCDC <!-- tw: Oreoxmt 2-->

        - Refine the status message when TiCDC retries after a failure [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)
        - Optimize the way TiCDC handles messages that exceed the limit when synchronizing to Kafka by supporting only sending the primary key to the downstream [#9574](https://github.com/pingcap/tiflow/issues/9574) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): Storage Sink now supports hexadecimal encoding for HEX formatted data, making it compatible with AWS DMS format specifications [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Binlog

        - 

## Bug fixes

+ TiDB

    - 

+ TiKV

    <!-- tw: Oreoxmt 6-->
    - Fix the issue that the `ttl-check-poll-interval` configuration item does not take effect on RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - Fix the issue that Online Unsafe Recovery does not abort on timeout [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Region Merge might be blocked after executing `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - Fix the data inconsistency issue that might occur when one TiKV node is isolated and another node is restarted [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the QPS drops to zero in the sync-recover phase under the Data Replication Auto Synchronous mode [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - Fix the issue that encryption might cause data corruption during partial write [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
<!-- tw: ran-huang-->
    - Fix the issue of heartbeat storms by reducing the number of store heartbeat retries [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - Fix the issue that traffic control might not work when there is a high amount of pending compaction bytes [#14392](https://github.com/tikv/tikv/issues/14392) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV might consume more memory when the Old Value feature in TiCDC is enabled [#14815](https://github.com/tikv/tikv/issues/14815) @[YuJuncen](https://github.com/YuJuncen)

+ TiFlash

    - 

+ Tools

    + Backup & Restore (BR) <!-- tw: ran-huang 7-->

        - Fix the issue of restore failures by increasing the default values of the global parameters `TableColumnCountLimit` and `IndexLimit` used by BR to their maximum values [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of rewrite failures when processing ddl meta information in PITR [#43184](https://github.com/pingcap/tidb/issues/43184) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of panic caused by not checking function returns during PITR execution [#45853](https://github.com/pingcap/tidb/issues/45853) @[Leavrth](https://github.com/Leavrth) 
        - Fix the issue of obtaining invalid region ID when using S3-compatible storage other than AWS S3 [#41916](https://github.com/pingcap/tidb/issues/41916) [#42033](https://github.com/pingcap/tidb/issues/42033) @[3pointer](https://github.com/3pointer) 
        - Fix the potential error in fine-grained backup phase [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - (dup)- Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - (dup)- Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!-- tw: Oreoxmt 8-->

        - Fix the issue that the replication task might get stuck when the downstream encounters an error and retries [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the replication task fails due to short retry intervals when synchronizing to Kafka [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might cause synchronization write conflicts when modifying multiple unique key rows in one transaction on the upstream [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC might incorrectly synchronize rename DDL operations [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the replication task might get stuck when the downstream encounters a short-term failure [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272)[#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - (dup): Fix the panic issue that might occur when the TiCDC node status changes [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - (dup): Fix the issue that when Kafka Sink encounters errors it might indefinitely block changefeed progress [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - (dup): Fix the issue that when the downstream is Kafka, TiCDC queries the downstream metadata too frequently and causes excessive workload in the downstream [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - (dup): Fix the data inconsistency issue that might occur when some TiCDC nodes are isolated from the network [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): Fix the issue that the replication task might get stuck when the redo log is enabled and there is an exception downstream [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): Fix the issue that changefeeds would fail due to the temporary unavailability of PD [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - (dup): Fix the issue of too many downstream logs caused by frequently setting the downstream bidirectional replication-related variables when replicating data to TiDB or MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - (dup): Fix the issue that Avro protocol incorrectly identifies `Enum` type values [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - 

    + TiDB Binlog

        - 

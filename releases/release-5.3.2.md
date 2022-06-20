---
title: TiDB 5.3.2 Release Notes
---



# TiDB 5.3.2 Release Notes

Release Date: June xx, 2022

TiDB version: 5.3.2

## Compatibility change(s)

## Improvements

## Bug fixes

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#35498](https://github.com/pingcap/tidb/pull/35498)
    - ```release-note [#35405](https://github.com/pingcap/tidb/pull/35405)
    - ```release-note [#35398](https://github.com/pingcap/tidb/pull/35398)
    - ```release-note [#35384](https://github.com/pingcap/tidb/pull/35384)
    - ```release-note [#35371](https://github.com/pingcap/tidb/pull/35371)
    - Fixed an issue where extra datums may break binlog. [#35165](https://github.com/pingcap/tidb/pull/35165)
    - ```release-note [#34618](https://github.com/pingcap/tidb/pull/34618)
    - ```release-note [#34516](https://github.com/pingcap/tidb/pull/34516)
    - ```release-note [#34474](https://github.com/pingcap/tidb/pull/34474)
    - ```release-note [#34432](https://github.com/pingcap/tidb/pull/34432)
    - ```release-note [#34377](https://github.com/pingcap/tidb/pull/34377)
    - ```release-note [#34334](https://github.com/pingcap/tidb/pull/34334)
    - lightning: split and scatter regions in batches [#34257](https://github.com/pingcap/tidb/pull/34257)
    - ```release-note [#34225](https://github.com/pingcap/tidb/pull/34225)
    - Fix the issue that the table attributes don't support index and won't be updated when the partition changes [#34024](https://github.com/pingcap/tidb/pull/34024)
    - Fix a bug of duplicate primary key when insert record into table after incremental restoration. [#33987](https://github.com/pingcap/tidb/pull/33987)
    - ```release-note [#33960](https://github.com/pingcap/tidb/pull/33960)
    - ```release-note [#33942](https://github.com/pingcap/tidb/pull/33942)
    - ```release-note [#33913](https://github.com/pingcap/tidb/pull/33913)
    - Fix the issue that the schedulers won't be resumed after BR/Lightning exits abnormally. [#33815](https://github.com/pingcap/tidb/pull/33815)
    - Fix the issue that privilege-related operations may fail for upgraded clusters. [#33604](https://github.com/pingcap/tidb/pull/33604)
    - Fix the issue that NewCollationEnable config not checked during restoration. [#33533](https://github.com/pingcap/tidb/pull/33533)
    - Fix a bug that BR incremental restore return error by mistake caused by ddl job with empty query. [#33516](https://github.com/pingcap/tidb/pull/33516)
    - Fix the issue that BR not retry enough when region not consistency during restoration. [#33469](https://github.com/pingcap/tidb/pull/33469)
    - ```release-note [#33339](https://github.com/pingcap/tidb/pull/33339)
    - Fix a bug that caused BR get stuck when restore meets some unrecoverable error. [#33267](https://github.com/pingcap/tidb/pull/33267)
    - executor: fix wrong result of delete multiple tables using left join [#33122](https://github.com/pingcap/tidb/pull/33122)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32840](https://github.com/pingcap/tidb/pull/32840)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32798](https://github.com/pingcap/tidb/pull/32798)
    - Fix BR failure on backup rawkv. [#32792](https://github.com/pingcap/tidb/pull/32792)
    - Fix some connections and goroutines leak caused by not closed HTTP response body [#30600](https://github.com/pingcap/tidb/pull/30600)


+ TiKV/TiKV

    - Fix bug which causes frequent pd client reconnection [#12832](https://github.com/tikv/tikv/pull/12832)
    - Report bad health status if raftstore stops working. [#12817](https://github.com/tikv/tikv/pull/12817)
    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12745](https://github.com/tikv/tikv/pull/12745)
    - Fix tikv crash when conv empty string [#12692](https://github.com/tikv/tikv/pull/12692)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12653](https://github.com/tikv/tikv/pull/12653)
    - Fix a bug that sometimes generates a message with zero store id when doing follower read [#12529](https://github.com/tikv/tikv/pull/12529)
    - Add a new hidden config `s3_multi_part_size` to make backup can control the part size when upload big sst file to s3. [#12457](https://github.com/tikv/tikv/pull/12457)
    - Report bad health status if raftstore stops working. [#12447](https://github.com/tikv/tikv/pull/12447)
    - fix race between split check and destroy [#12405](https://github.com/tikv/tikv/pull/12405)
    - Fixes that successfully committed optimistic transactions may report false WriteConflict on network errors. [#12377](https://github.com/tikv/tikv/pull/12377)
    - fix tikv panic and peer unexpected destroy due to fake merge target [#12296](https://github.com/tikv/tikv/pull/12296)
    - Fix stale message cause panic [#12287](https://github.com/tikv/tikv/pull/12287)
    - Solve the problem of raft msg memory metrics overflow, which will cause intermittent packet loss and oom. [#12226](https://github.com/tikv/tikv/pull/12226)
    - Fix crash when profiling in Ubuntu 18.04. [#12213](https://github.com/tikv/tikv/pull/12213)
    - Fix logic of error string match in `bad-ssts`. [#12149](https://github.com/tikv/tikv/pull/12149)
    - Pass leader transferee to cdc observer to reduce TiCDC latency spike. [#12136](https://github.com/tikv/tikv/pull/12136)
    - Fix potential linearizability violation in replica reads. [#12119](https://github.com/tikv/tikv/pull/12119)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12085](https://github.com/tikv/tikv/pull/12085)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#12041](https://github.com/tikv/tikv/pull/12041)
    - None. [#11438](https://github.com/tikv/tikv/pull/11438)
    - None. [#11380](https://github.com/tikv/tikv/pull/11380)


+ PingCAP/TiFlash

    - Fix potential query error when select on a table with many delete operations [#4759](https://github.com/pingcap/tiflash/pull/4759)
    - Fix bug that TiFlash query will meet keepalive timeout error randomly. [#4731](https://github.com/pingcap/tiflash/pull/4731)
    - Avoid leaving data on tiflash node which doesn't corresponding to any region range [#4716](https://github.com/pingcap/tiflash/pull/4716)
    - Fix a bug that MPP tasks may leak threads forever [#4647](https://github.com/pingcap/tiflash/pull/4647)
    - Fix the problem that empty segments cannot be merged after gc [#4523](https://github.com/pingcap/tiflash/pull/4523)
    - Fix wrong result of cast(float as decimal) when overflow happens [#4387](https://github.com/pingcap/tiflash/pull/4387)
    - Fix the potential crash issue that occurs when TLS is enabled [#4369](https://github.com/pingcap/tiflash/pull/4369)
    - fix the problem that expired data was not recycled timely due to slow gc speed [#4254](https://github.com/pingcap/tiflash/pull/4254)
    - Fix the bug that canceled MPP query may cause tasks hang forever when local tunnel is enabled. [#4236](https://github.com/pingcap/tiflash/pull/4236)
    - Fix cast datetime to decimal wrong result bug [#4159](https://github.com/pingcap/tiflash/pull/4159)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4134](https://github.com/pingcap/tiflash/pull/4134)
    - Fix the bug that some exceptions are not handled properly [#4114](https://github.com/pingcap/tiflash/pull/4114)
    - Fix potential query error after add column under heavy read workload [#4027](https://github.com/pingcap/tiflash/pull/4027)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3936](https://github.com/pingcap/tiflash/pull/3936)
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb. [#3757](https://github.com/pingcap/tiflash/pull/3757)
    - Avoid false alert of `DB::Exception: Encode type of coprocessor response is not CHBlock` [#3740](https://github.com/pingcap/tiflash/pull/3740)
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart. [#3708](https://github.com/pingcap/tiflash/pull/3708)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3480](https://github.com/pingcap/tiflash/pull/3480)


+ PD

    - server: disable swagger server [#5177](https://github.com/tikv/pd/pull/5177)
    - Fix the issue that the hot region may cause panic due to no leader [#5040](https://github.com/tikv/pd/pull/5040)
    - None. [#4999](https://github.com/tikv/pd/pull/4999)
    - Fix the issue that scheduling cannot immediately start after PD leader transfers [#4969](https://github.com/tikv/pd/pull/4969)
    - Fix the issue that the removed tombstone store shows again after transferring the PD leader [#4958](https://github.com/tikv/pd/pull/4958)
    - Fix the corner case that may cause TSO fallback. [#4891](https://github.com/tikv/pd/pull/4891)
    - None. [#4847](https://github.com/tikv/pd/pull/4847)
    - Fix the issue that the label distribution has residual labels [#4831](https://github.com/tikv/pd/pull/4831)


+ Tools

    + PingCAP/TiCDC

        - Fix TiCDC incorrectly display stale metrics data on dashboard. [#5894](https://github.com/pingcap/tiflow/pull/5894)
        - Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note.

If you don't think this PR needs a release note then fill it with `None`. [#5678](https://github.com/pingcap/tiflow/pull/5678)
        - Fix a bug that after auto resume, DM will use more disk space. [#5636](https://github.com/pingcap/tiflow/pull/5636)
        - Fix a bug in redo log manager that flush log executed before writing logs [#5628](https://github.com/pingcap/tiflow/pull/5628)
        - Fix a bug that resolved ts moves too fast when part of tables are not maintained redo writer. [#5617](https://github.com/pingcap/tiflow/pull/5617)
        - Add uuid suffix to redo log file name to prevent name conflict, which may cause data loss. [#5613](https://github.com/pingcap/tiflow/pull/5613)
        - `Fix a bug that mysql sink may save a wrong checkpointTs`. [#5436](https://github.com/pingcap/tiflow/pull/5436)
        - Please add a release note.

Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note.

If you don't think this PR needs a release note then fill it with `None`. [#5419](https://github.com/pingcap/tiflow/pull/5419)
        - Fix DM can't replicate uppercase tables when the task has case-sensitive: false [#5308](https://github.com/pingcap/tiflow/pull/5308)
        - Fix an issue where TiCDC clusters may panic after an upgrade [#5304](https://github.com/pingcap/tiflow/pull/5304)
        - save table checkpoint after a DDL is filtered [#5292](https://github.com/pingcap/tiflow/pull/5292)
        - `None`. [#5226](https://github.com/pingcap/tiflow/pull/5226)
        - fix the issue that ticdc failed to start when connects to  multiple pd endpoints with tls-enabled and the 1st endpoint is not available [#5209](https://github.com/pingcap/tiflow/pull/5209)
        - fix tracker panic when pk of downstream table orders behind [#5178](https://github.com/pingcap/tiflow/pull/5178)
        - `None` [#5171](https://github.com/pingcap/tiflow/pull/5171)
        - fix tracker panic when pk of downstream table orders behind [#5165](https://github.com/pingcap/tiflow/pull/5165)
        - `Fix a bug that openapi may be stuck when pd is abnormal` [#5111](https://github.com/pingcap/tiflow/pull/5111)
        - send one heartbeat for successive skipped GTID when enable relay log [#5092](https://github.com/pingcap/tiflow/pull/5092)
        - fix bug of relay log may turn off after master reboot in v5.3.1 [#4877](https://github.com/pingcap/tiflow/pull/4877)
        - Syncer will use working directory of DM-worker rather than /tmp to write internal files, and clean it after task is stopped [#4804](https://github.com/pingcap/tiflow/pull/4804)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4682](https://github.com/pingcap/tiflow/pull/4682)
        - Fix a bug that sequence should not be replicated even if force-replication is true.
Fix data loss when upstream transaction conflicts during cdc reconnection. [#4666](https://github.com/pingcap/tiflow/pull/4666)
        - `None`. [#4650](https://github.com/pingcap/tiflow/pull/4650)
        - Please add a release note.
`None`. [#4647](https://github.com/pingcap/tiflow/pull/4647)
        - `None`. [#4345](https://github.com/pingcap/tiflow/pull/4345)


## Bug Fixes

+ PingCAP/TiDB

    - fix the problem that dumpling can't dump with --compress and s3 output directory. [#35356](https://github.com/pingcap/tidb/pull/35356)
    - Fix the data inconsistency caused by invalid usage of lazy existence check and untouch key optimization. [#30912](https://github.com/pingcap/tidb/pull/30912)
    - Fix the bug that sql got cancel if including json column joins char column. [#30777](https://github.com/pingcap/tidb/pull/30777)


+ PingCAP/TiFlash

    - Fix potential wrong result after a lot of insert and delete operations [#4967](https://github.com/pingcap/tiflash/pull/4967)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#4495](https://github.com/pingcap/tiflash/pull/4495)
    - Fix the issue that a query containing `JOIN` could be hung if an error was encountered [#4269](https://github.com/pingcap/tiflash/pull/4269)


## Compatibility Changes

+ PingCAP/TiDB

    - Fix an issue that REPLACE statement changing other rows when the auto ID is out of range [#32324](https://github.com/pingcap/tidb/pull/32324)


## Improvements

+ TiKV/TiKV

    - Delay in raft client to reduce syscalls and improve CPU efficiency [#11761](https://github.com/tikv/tikv/pull/11761)



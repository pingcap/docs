---
title: TiDB 5.4.1 Release Notes
category: Releases
---



# TiDB 5.4.1 Release Notes

Release Date: May xx, 2022

TiDB version: 5.4.1

## Improvements

+ PingCAP/TiDB

    - ```release-note [#33887](https://github.com/pingcap/tidb/issues/33887)


+ Tools

    + PingCAP/TiCDC

        - `None`. [#4784](https://github.com/pingcap/tiflow/issues/4784)

## Bug Fixes

+ PingCAP/TiDB

    - executor: fix CTE is block when query report error [#31302](https://github.com/pingcap/tidb/issues/31302)
    - planner: fix wrong range calculation for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)


+ PingCAP/TiFlash

    - Fix the potential crash issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#4437](https://github.com/pingcap/tiflash/issues/4437)
    - Fix the issue that a query containing `JOIN` could be hung if an error was encountered [#4195](https://github.com/pingcap/tiflash/issues/4195)


+ PD

    - Fix the issue that duration fields of dr-autosync cannot be set [#4651](https://github.com/tikv/pd/issues/4651)

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#27937](https://github.com/pingcap/tidb/issues/27937)
    - ```release-note [#34216](https://github.com/pingcap/tidb/issues/34216)
    - ```release-note [#34256](https://github.com/pingcap/tidb/issues/34256)
    - ```release-note [#33665](https://github.com/pingcap/tidb/issues/33665)
    - ```release-note [#34237](https://github.com/pingcap/tidb/issues/34237)
    - lightning: split and scatter regions in batches [#33618](https://github.com/pingcap/tidb/issues/33618)
    - ```release-note [#32459](https://github.com/pingcap/tidb/issues/32459)
    - ```release-note [#34099](https://github.com/pingcap/tidb/issues/34099)
    - ```release-note [#34213](https://github.com/pingcap/tidb/issues/34213)
    - ```release-note [#34180](https://github.com/pingcap/tidb/issues/34180)
    - ```release-note [#34139](https://github.com/pingcap/tidb/pull/34139)
    - Fix the problem of high use of reArrangeFallback cpu. [#30353](https://github.com/pingcap/tidb/issues/30353)
    - Fix the issue that the table attributes don't support index and won't be updated when the partition changes [#33929](https://github.com/pingcap/tidb/issues/33929)
    - ```release-note [#33801](https://github.com/pingcap/tidb/issues/33801)
    - Fix a bug of duplicate primary key when insert record into table after incremental restoration. [#33596](https://github.com/pingcap/tidb/issues/33596)
    - ```release-note [#33893](https://github.com/pingcap/tidb/issues/33893)
    - Fix the issue that the schedulers won't be resumed after BR/Lightning exits abnormally. [#33546](https://github.com/pingcap/tidb/issues/33546)
    - Fix the issue that privilege-related operations may fail for upgraded clusters. [#33588](https://github.com/pingcap/tidb/issues/33588)
    - fix bug #33509 [#33509](https://github.com/pingcap/tidb/issues/33509)
    - fix a bug that compress function may report error [#33397](https://github.com/pingcap/tidb/issues/33397)
    - Fix the issue that NewCollationEnable config not checked during restoration. [#33422](https://github.com/pingcap/tidb/issues/33422)
    - Fix a bug that BR incremental restore return error by mistake caused by ddl job with empty query. [#33322](https://github.com/pingcap/tidb/issues/33322)
    - Fix the issue that BR not retry enough when region not consistency during restoration. [#33419](https://github.com/pingcap/tidb/issues/33419)
    - Add retry to avoid precheck failure when query execution timeout [#31797](https://github.com/pingcap/tidb/issues/31797)
    - executor: fix wrong result of delete multiple tables using left join [#31321](https://github.com/pingcap/tidb/issues/31321)
    - Support multi k8s in grafana dashboards [#32593](https://github.com/pingcap/tidb/issues/32593)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - Fix the bug that locking with NOWAIT does not return immediately when encountering a lock. [#32754](https://github.com/pingcap/tidb/issues/32754)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32733](https://github.com/pingcap/tidb/issues/32733)
    - Fix BR failure on backup rawkv. [#32607](https://github.com/pingcap/tidb/issues/32607)
    - planner: make queries with the extra column `_tidb_rowid` can use PointGet [#31543](https://github.com/pingcap/tidb/issues/31543)
    - Fix the problem of tidb oom when exporting data using chunk rpc [#31981](https://github.com/pingcap/tidb/issues/31981)
    - fix date formate identifies '\n' as invalid separator [#32504](https://github.com/pingcap/tidb/pull/32504)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#28144](https://github.com/pingcap/tidb/issues/28144)
    - Fix a bug that caused region unbalanced after restoring. [#31034](https://github.com/pingcap/tidb/issues/31034)
    - Fixed a bug that turning on tidb_restricted_read_only won't automatically turn on tidb_super_read_only [#31745](https://github.com/pingcap/tidb/issues/31745)
    - fix greatest and least function with collation get wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    - fix load data will panic in some case [#31589](https://github.com/pingcap/tidb/issues/31589)
    - Fix a data race that may cause "invalid transaction" error when executing a query using index lookup join. [#30468](https://github.com/pingcap/tidb/issues/30468)

+ TiKV/TiKV

    - Fixes that successfully committed optimistic transactions may report false WriteConflict on network errors. [#34066](https://github.com/pingcap/tidb/issues/34066)
    - Fix panicking when replica read is enabled and there is a long time network condition [#12046](https://github.com/tikv/tikv/issues/12046)
    - fix tikv panic and peer unexpected destroy due to fake merge target [#12232](https://github.com/tikv/tikv/issues/12232)
    - Fix stale message cause panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - Solve the problem of raft msg memory metrics overflow, which will cause intermittent packet loss and oom. [#12160](https://github.com/tikv/tikv/issues/12160)
    - Fix crash when profiling in Ubuntu 18.04. [#9765](https://github.com/tikv/tikv/issues/9765)
    - metrics: support multi k8s in grafana dashboards. [#12104](https://github.com/tikv/tikv/issues/12104)
    - Fix potential linearizability violation in replica reads. [#12109](https://github.com/tikv/tikv/issues/12109)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12048](https://github.com/tikv/tikv/issues/12048)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#11940](https://github.com/tikv/tikv/issues/11940)
    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#11993](https://github.com/tikv/tikv/issues/11993)
    - Fix a potential panic (#11746) when snapshot files have been deleted but the peer's status is still Applying. [#11746](https://github.com/tikv/tikv/issues/11746)
    - fix potential high latency caused by destroying a peer [#10210](https://github.com/tikv/tikv/issues/10210)

+ PingCAP/TiFlash

    - fix potential data corruption for large indices [#4778](https://github.com/pingcap/tiflash/issues/4778)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - Fix potential query error when select on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - Fix bug that TiFlash query will meet keepalive timeout error randomly. [#4192](https://github.com/pingcap/tiflash/issues/4192)
    - Avoid leaving data on tiflash node which doesn't corresponding to any region range [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - Fix a bug that MPP tasks may leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - Fix the problem that empty segments cannot be merged after gc [#4511](https://github.com/pingcap/tiflash/issues/4511)
    - Fix wrong result of cast(float as decimal) when overflow happens [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - fix the problem that expired data was not recycled timely due to slow gc speed [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - Fix the bug that canceled MPP query may cause tasks hang forever when local tunnel is enabled. [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - Fix bug that enable elastic thread pool may introduce memory leak. [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - Fix memory leak when a query is cancelled. [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - metrics: support multi-k8s in grafana dashboards [#4129](https://github.com/pingcap/tiflash/issues/4129)
    - metrics: support multi-k8s in grafana dashboards [#4129](https://github.com/pingcap/tiflash/issues/4129)
    - Fix cast datetime to decimal wrong result bug [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - Avoid the potential of crash when apply snapshot under heavy ddl scenario [#4072](https://github.com/pingcap/tiflash/issues/4072)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - Fix cast to decimal overflow bug [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - fix error result for function `in` [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - fix date format identifies '\n' as invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - Fix potential query error after add column under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)

+ PD

    - None. [#4805](https://github.com/tikv/pd/issues/4805)
    - Fix the issue that the label distribution has residual labels [#4825](https://github.com/tikv/pd/issues/4825)
    - metrics: support multi-k8s in grafana dashboards [#4673](https://github.com/tikv/pd/issues/4673)
    - None. [#4808](https://github.com/tikv/pd/issues/4808)

+ Tools

    + PingCAP/TiCDC

        - save table checkpoint after a DDL is filtered [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - Fix TiCDC incorrectly display stale metrics data on dashboard. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - Fix a bug that no data is return by `query-status` when upstream doesn't turn on binlog [#5121](https://github.com/pingcap/tiflow/issues/5121)
        - `None`. [#5197](https://github.com/pingcap/tiflow/issues/5197)
        - Fix a bug that checkpoint flushing will be called too frequently [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - fix tracker panic when pk of downstream table orders behind [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - `None`. [#5136](https://github.com/pingcap/tiflow/issues/5136)
        - send one heartbeat for successive skipped GTID when enable relay log [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - fix DML construct error issue caused by `rename tables` DDL. [#5059](https://github.com/pingcap/tiflow/issues/5059)
        - Fix a rare likelihood that replication be stuck if the owner is changed when the new scheduler is enabled (disabled by default). [#4963](https://github.com/pingcap/tiflow/issues/4963)
        - `None`. [#4858](https://github.com/pingcap/tiflow/issues/4858)
        - Syncer will use working directory of DM-worker rather than /tmp to write internal files, and clean it after task is stopped [#4107](https://github.com/pingcap/tiflow/issues/4107)
        - Fix that there're lot of log of "checkpoint has no change, skip sync flush checkpoint" and performance may drop [#4619](https://github.com/pingcap/tiflow/issues/4619)
        - Fix stale metrics caused by owner changes. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - Fix ErrProcessorDuplicateOperations when new scheduler is enabled (disabled by default) [#4769](https://github.com/pingcap/tiflow/issues/4769)
        - fix the issue that ticdc failed to start when connects to  multiple pd endpoints with tls-enabled and the 1st endpoint is not available [#4777](https://github.com/pingcap/tiflow/issues/4777)
        - fix `Canal-JSON` meet `unsigned` SQL Type and nullable, which cause CDC server panic. [#4736](https://github.com/pingcap/tiflow/issues/4736)
        - Fix checkpoint metrics when tables are being scheduled. [#4714](https://github.com/pingcap/tiflow/issues/4714)
        - metrics: support multi-k8s in grafana dashboards [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - Fix a bug that sequence should not be replicated even if force-replication is true. [#4552](https://github.com/pingcap/tiflow/issues/4552)
        - fix `Canal-JSON` meet `unsigned` SQL typed in `string`, which cause CDC server panic. [#4635](https://github.com/pingcap/tiflow/issues/4635)
        - `None`. [#4554](https://github.com/pingcap/tiflow/issues/4554)
        - Please add a release note.
`None`. [#4565](https://github.com/pingcap/tiflow/issues/4565)
        - Fix a bug that long varchar will report error of "Column length too big..." [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - `None`. [#4607](https://github.com/pingcap/tiflow/issues/4607)
        - `None`. [#4588](https://github.com/pingcap/tiflow/issues/4588)
        - `None`. [#4561](https://github.com/pingcap/tiflow/issues/4561)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - allow user set the configuration of Kafka producer dial/write/read timeout [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#4287](https://github.com/pingcap/tiflow/issues/4287)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic. [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - None. [#4353](https://github.com/pingcap/tiflow/issues/4353)
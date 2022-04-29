---
title: TiDB 5.4.1 Release Notes
category: Releases
---



# TiDB 5.4.1 Release Notes

Release Date: April 29, 2022

TiDB version: 5.4.1

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#34335](https://github.com/pingcap/tidb/pull/34335)
    - ```release-note [#34317](https://github.com/pingcap/tidb/pull/34317)
    - ```release-note [#34302](https://github.com/pingcap/tidb/pull/34302)
    - ```release-note [#34271](https://github.com/pingcap/tidb/pull/34271)
    - ```release-note [#34268](https://github.com/pingcap/tidb/pull/34268)
    - lightning: split and scatter regions in batches [#34258](https://github.com/pingcap/tidb/pull/34258)
    - ```release-note [#34253](https://github.com/pingcap/tidb/pull/34253)
    - ```release-note [#34245](https://github.com/pingcap/tidb/pull/34245)
    - ```release-note [#34226](https://github.com/pingcap/tidb/pull/34226)
    - ```release-note [#34189](https://github.com/pingcap/tidb/pull/34189)
    - ```release-note [#34139](https://github.com/pingcap/tidb/pull/34139)
    - Fix the problem of high use of reArrangeFallback cpu. [#34063](https://github.com/pingcap/tidb/pull/34063)
    - Fix the issue that the table attributes don't support index and won't be updated when the partition changes [#34025](https://github.com/pingcap/tidb/pull/34025)
    - ```release-note [#34019](https://github.com/pingcap/tidb/pull/34019)
    - Fix a bug of duplicate primary key when insert record into table after incremental restoration. [#33988](https://github.com/pingcap/tidb/pull/33988)
    - ```release-note [#33961](https://github.com/pingcap/tidb/pull/33961)
    - Fix the issue that the schedulers won't be resumed after BR/Lightning exits abnormally. [#33816](https://github.com/pingcap/tidb/pull/33816)
    - Fix the issue that privilege-related operations may fail for upgraded clusters. [#33605](https://github.com/pingcap/tidb/pull/33605)
    - fix bug #33509 [#33577](https://github.com/pingcap/tidb/pull/33577)
    - fix a bug that compress function may report error [#33557](https://github.com/pingcap/tidb/pull/33557)
    - Fix the issue that NewCollationEnable config not checked during restoration. [#33532](https://github.com/pingcap/tidb/pull/33532)
    - Fix a bug that BR incremental restore return error by mistake caused by ddl job with empty query. [#33517](https://github.com/pingcap/tidb/pull/33517)
    - Fix the issue that BR not retry enough when region not consistency during restoration. [#33470](https://github.com/pingcap/tidb/pull/33470)
    - Add retry to avoid precheck failure when query execution timeout [#33148](https://github.com/pingcap/tidb/pull/33148)
    - executor: fix wrong result of delete multiple tables using left join [#33123](https://github.com/pingcap/tidb/pull/33123)
    - Support multi k8s in grafana dashboards [#32953](https://github.com/pingcap/tidb/pull/32953)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32841](https://github.com/pingcap/tidb/pull/32841)
    - Fix the bug that locking with NOWAIT does not return immediately when encountering a lock. [#32812](https://github.com/pingcap/tidb/pull/32812)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32799](https://github.com/pingcap/tidb/pull/32799)
    - Fix BR failure on backup rawkv. [#32793](https://github.com/pingcap/tidb/pull/32793)
    - planner: make queries with the extra column `_tidb_rowid` can use PointGet [#32704](https://github.com/pingcap/tidb/pull/32704)
    - Fix the problem of tidb oom when exporting data using chunk rpc [#32578](https://github.com/pingcap/tidb/pull/32578)
    - fix date formate identifies '\n' as invalid separator [#32504](https://github.com/pingcap/tidb/pull/32504)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#32390](https://github.com/pingcap/tidb/pull/32390)
    - Fix a bug that caused region unbalanced after restoring. [#32129](https://github.com/pingcap/tidb/pull/32129)
    - Fixed a bug that turning on tidb_restricted_read_only won't automatically turn on tidb_super_read_only [#31842](https://github.com/pingcap/tidb/pull/31842)
    - fix greatest and least function with collation get wrong result [#31838](https://github.com/pingcap/tidb/pull/31838)
    - fix load data will panic in some case [#31774](https://github.com/pingcap/tidb/pull/31774)
    - Fix a data race that may cause "invalid transaction" error when executing a query using index lookup join. [#31351](https://github.com/pingcap/tidb/pull/31351)


+ TiKV/TiKV

    - Fixes that successfully committed optimistic transactions may report false WriteConflict on network errors. [#12378](https://github.com/tikv/tikv/pull/12378)
    - Fix panicking when replica read is enabled and there is a long time network condition [#12310](https://github.com/tikv/tikv/pull/12310)
    - fix tikv panic and peer unexpected destroy due to fake merge target [#12295](https://github.com/tikv/tikv/pull/12295)
    - Fix stale message cause panic [#12285](https://github.com/tikv/tikv/pull/12285)
    - Solve the problem of raft msg memory metrics overflow, which will cause intermittent packet loss and oom. [#12227](https://github.com/tikv/tikv/pull/12227)
    - Fix crash when profiling in Ubuntu 18.04. [#12208](https://github.com/tikv/tikv/pull/12208)
    - metrics: support multi k8s in grafana dashboards. [#12138](https://github.com/tikv/tikv/pull/12138)
    - Fix potential linearizability violation in replica reads. [#12121](https://github.com/tikv/tikv/pull/12121)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12086](https://github.com/tikv/tikv/pull/12086)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#12042](https://github.com/tikv/tikv/pull/12042)
    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#12001](https://github.com/tikv/tikv/pull/12001)
    - Fix a potential panic (#11746) when snapshot files have been deleted but the peer's status is still Applying. [#11905](https://github.com/tikv/tikv/pull/11905)
    - fix potential high latency caused by destroying a peer [#11881](https://github.com/tikv/tikv/pull/11881)


+ PingCAP/TiFlash

    - fix potential data corruption for large indices [#4790](https://github.com/pingcap/tiflash/pull/4790)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#4776](https://github.com/pingcap/tiflash/pull/4776)
    - Fix potential query error when select on a table with many delete operations [#4760](https://github.com/pingcap/tiflash/pull/4760)
    - Fix bug that TiFlash query will meet keepalive timeout error randomly. [#4729](https://github.com/pingcap/tiflash/pull/4729)
    - Avoid leaving data on tiflash node which doesn't corresponding to any region range [#4717](https://github.com/pingcap/tiflash/pull/4717)
    - Fix a bug that MPP tasks may leak threads forever [#4642](https://github.com/pingcap/tiflash/pull/4642)
    - Fix the problem that empty segments cannot be merged after gc [#4522](https://github.com/pingcap/tiflash/pull/4522)
    - Fix wrong result of cast(float as decimal) when overflow happens [#4388](https://github.com/pingcap/tiflash/pull/4388)
    - fix the problem that expired data was not recycled timely due to slow gc speed [#4255](https://github.com/pingcap/tiflash/pull/4255)
    - Fix the bug that canceled MPP query may cause tasks hang forever when local tunnel is enabled. [#4237](https://github.com/pingcap/tiflash/pull/4237)
    - Fix bug that enable elastic thread pool may introduce memory leak. [#4231](https://github.com/pingcap/tiflash/pull/4231)
    - Fix memory leak when a query is cancelled. [#4230](https://github.com/pingcap/tiflash/pull/4230)
    - metrics: support multi-k8s in grafana dashboards [#4213](https://github.com/pingcap/tiflash/pull/4213)
    - metrics: support multi-k8s in grafana dashboards [#4206](https://github.com/pingcap/tiflash/pull/4206)
    - Fix cast datetime to decimal wrong result bug [#4160](https://github.com/pingcap/tiflash/pull/4160)
    - Avoid the potential of crash when apply snapshot under heavy ddl scenario [#4143](https://github.com/pingcap/tiflash/pull/4143)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4135](https://github.com/pingcap/tiflash/pull/4135)
    - Fix the bug that some exceptions are not handled properly [#4115](https://github.com/pingcap/tiflash/pull/4115)
    - Fix cast to decimal overflow bug [#4082](https://github.com/pingcap/tiflash/pull/4082)
    - fix error result for function `in` [#4078](https://github.com/pingcap/tiflash/pull/4078)
    - fix date format identifies '\n' as invalid separator [#4060](https://github.com/pingcap/tiflash/pull/4060)
    - Fix potential query error after add column under heavy read workload [#4028](https://github.com/pingcap/tiflash/pull/4028)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3919](https://github.com/pingcap/tiflash/pull/3919)


+ PD

    - None. [#4849](https://github.com/tikv/pd/pull/4849)
    - Fix the issue that the label distribution has residual labels [#4826](https://github.com/tikv/pd/pull/4826)
    - metrics: support multi-k8s in grafana dashboards [#4717](https://github.com/tikv/pd/pull/4717)
    - None. [#4664](https://github.com/tikv/pd/pull/4664)


+ Tools

    + PingCAP/TiCDC

        - save table checkpoint after a DDL is filtered [#5290](https://github.com/pingcap/tiflow/pull/5290)
        - Fix TiCDC incorrectly display stale metrics data on dashboard. [#5260](https://github.com/pingcap/tiflow/pull/5260)
        - Fix a bug that no data is return by `query-status` when upstream doesn't turn on binlog [#5241](https://github.com/pingcap/tiflow/pull/5241)
        - `None`. [#5227](https://github.com/pingcap/tiflow/pull/5227)
        - Fix a bug that checkpoint flushing will be called too frequently [#5201](https://github.com/pingcap/tiflow/pull/5201)
        - fix tracker panic when pk of downstream table orders behind [#5167](https://github.com/pingcap/tiflow/pull/5167)
        - `None`. [#5137](https://github.com/pingcap/tiflow/pull/5137)
        - send one heartbeat for successive skipped GTID when enable relay log [#5093](https://github.com/pingcap/tiflow/pull/5093)
        - fix DML construct error issue caused by `rename tables` DDL. [#5079](https://github.com/pingcap/tiflow/pull/5079)
        - Fix a rare likelihood that replication be stuck if the owner is changed when the new scheduler is enabled (disabled by default). [#5000](https://github.com/pingcap/tiflow/pull/5000)
        - `None`. [#4869](https://github.com/pingcap/tiflow/pull/4869)
        - Syncer will use working directory of DM-worker rather than /tmp to write internal files, and clean it after task is stopped [#4805](https://github.com/pingcap/tiflow/pull/4805)
        - Fix that there're lot of log of "checkpoint has no change, skip sync flush checkpoint" and performance may drop [#4801](https://github.com/pingcap/tiflow/pull/4801)
        - Fix stale metrics caused by owner changes. [#4800](https://github.com/pingcap/tiflow/pull/4800)
        - Fix ErrProcessorDuplicateOperations when new scheduler is enabled (disabled by default) [#4789](https://github.com/pingcap/tiflow/pull/4789)
        - fix the issue that ticdc failed to start when connects to  multiple pd endpoints with tls-enabled and the 1st endpoint is not available [#4779](https://github.com/pingcap/tiflow/pull/4779)
        - fix `Canal-JSON` meet `unsigned` SQL Type and nullable, which cause CDC server panic. [#4745](https://github.com/pingcap/tiflow/pull/4745)
        - Fix checkpoint metrics when tables are being scheduled. [#4729](https://github.com/pingcap/tiflow/pull/4729)
        - metrics: support multi-k8s in grafana dashboards [#4709](https://github.com/pingcap/tiflow/pull/4709)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4683](https://github.com/pingcap/tiflow/pull/4683)
        - Fix a bug that sequence should not be replicated even if force-replication is true. [#4667](https://github.com/pingcap/tiflow/pull/4667)
        - fix `Canal-JSON` meet `unsigned` SQL typed in `string`, which cause CDC server panic. [#4657](https://github.com/pingcap/tiflow/pull/4657)
        - `None`. [#4649](https://github.com/pingcap/tiflow/pull/4649)
        - Please add a release note.
`None`. [#4648](https://github.com/pingcap/tiflow/pull/4648)
        - Fix a bug that long varchar will report error of "Column length too big..." [#4646](https://github.com/pingcap/tiflow/pull/4646)
        - `None`. [#4615](https://github.com/pingcap/tiflow/pull/4615)
        - `None`. [#4595](https://github.com/pingcap/tiflow/pull/4595)
        - `None`. [#4575](https://github.com/pingcap/tiflow/pull/4575)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4533](https://github.com/pingcap/tiflow/pull/4533)
        - allow user set the configuration of Kafka producer dial/write/read timeout [#4521](https://github.com/pingcap/tiflow/pull/4521)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#4513](https://github.com/pingcap/tiflow/pull/4513)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4509](https://github.com/pingcap/tiflow/pull/4509)
        - `None`. [#4466](https://github.com/pingcap/tiflow/pull/4466)
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic. [#4438](https://github.com/pingcap/tiflow/pull/4438)
        - None. [#4431](https://github.com/pingcap/tiflow/pull/4431)


## Improvements

+ PingCAP/TiDB

    - ```release-note [#34067](https://github.com/pingcap/tidb/pull/34067)


+ Tools

    + PingCAP/TiCDC

        - `None`. [#4828](https://github.com/pingcap/tiflow/pull/4828)


## Bug Fixes

+ PingCAP/TiDB

    - executor: fix CTE is block when query report error [#33190](https://github.com/pingcap/tidb/pull/33190)
    - planner: fix wrong range calculation for Nulleq function on Enum values [#32496](https://github.com/pingcap/tidb/pull/32496)


+ PingCAP/TiFlash

    - Fix the potential crash issue that occurs when TLS is enabled [#4689](https://github.com/pingcap/tiflash/pull/4689)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#4496](https://github.com/pingcap/tiflash/pull/4496)
    - Fix the issue that a query containing `JOIN` could be hung if an error was encountered [#4270](https://github.com/pingcap/tiflash/pull/4270)


+ PD

    - Fix the issue that duration fields of dr-autosync cannot be set [#4660](https://github.com/tikv/pd/pull/4660)



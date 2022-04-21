---
title: TiDB 5.3.1 Release Notes
category: Releases
---



# TiDB 5.3.1 Release Notes

Release Date: April 21, 2022

TiDB version: 5.3.1

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#34115](https://github.com/pingcap/tidb/pull/34115)
    - ```release-note [#34080](https://github.com/pingcap/tidb/pull/34080)
    - executor: fix CTE race case by avoiding reopen iterInTbl [#34032](https://github.com/pingcap/tidb/pull/34032)
    - Fix the issue that the table attributes don't support index and won't be updated when the partition changes [#34024](https://github.com/pingcap/tidb/pull/34024)
    - ```release-note [#34017](https://github.com/pingcap/tidb/pull/34017)
    - Fix the problem of high use of reArrangeFallback cpu. [#34005](https://github.com/pingcap/tidb/pull/34005)
    - ```release-note [#33999](https://github.com/pingcap/tidb/pull/33999)
    - Fix a bug of duplicate primary key when insert record into table after incremental restoration. [#33987](https://github.com/pingcap/tidb/pull/33987)
    - ```release-note [#33960](https://github.com/pingcap/tidb/pull/33960)
    - ```release-note [#33942](https://github.com/pingcap/tidb/pull/33942)
    - ```release-note [#33913](https://github.com/pingcap/tidb/pull/33913)
    - ```release-note [#33905](https://github.com/pingcap/tidb/pull/33905)
    - fix duplicate elementID allocation to make sure gc work for partition table [#33855](https://github.com/pingcap/tidb/pull/33855)
    - ```release-note [#33826](https://github.com/pingcap/tidb/pull/33826)
    - Fix the issue that the schedulers won't be resumed after BR/Lightning exits abnormally. [#33815](https://github.com/pingcap/tidb/pull/33815)
    - expression: fix the wrong rounding behavior of Decimal [#33672](https://github.com/pingcap/tidb/pull/33672)
    - Fix the issue that privilege-related operations may fail for upgraded clusters. [#33604](https://github.com/pingcap/tidb/pull/33604)
    - Fix the issue that query result might be wrong when using dynamic partition pruning mode with index join. [#33581](https://github.com/pingcap/tidb/pull/33581)
    - fix bug #33509 [#33576](https://github.com/pingcap/tidb/pull/33576)
    - Fix the issue that NewCollationEnable config not checked during restoration. [#33533](https://github.com/pingcap/tidb/pull/33533)
    - Fix a bug that BR incremental restore return error by mistake caused by ddl job with empty query. [#33516](https://github.com/pingcap/tidb/pull/33516)
    - Fix the issue that BR not retry enough when region not consistency during restoration. [#33469](https://github.com/pingcap/tidb/pull/33469)
    - ```release-note [#33339](https://github.com/pingcap/tidb/pull/33339)
    - Fix a bug that caused BR get stuck when restore meets some unrecoverable error. [#33267](https://github.com/pingcap/tidb/pull/33267)
    - fix a bug that selection can not be pushed down when having clause above aggregation [#33183](https://github.com/pingcap/tidb/pull/33183)
    - fix builtin func `subtime` get a wrong result [#33128](https://github.com/pingcap/tidb/pull/33128)
    - executor: fix wrong result of delete multiple tables using left join [#33122](https://github.com/pingcap/tidb/pull/33122)
    - lightning: tolerate tikv node address changes during importing [#33106](https://github.com/pingcap/tidb/pull/33106)
    - Fix a bug that reading from a table with generated column may get wrong result.
It happens when all the following conditions hold:
- A UnionScan executor is used
- The query comes with a filter condition on the generated column
- No row from the first batch of the chunk rows match the filter condition [#33103](https://github.com/pingcap/tidb/pull/33103)
    - Fixed explicit partition selection in subselects. [#32932](https://github.com/pingcap/tidb/pull/32932)
    - Enable partition pruning for RANGE COLUMNS partitioning on IN conditions and string type columns [#32926](https://github.com/pingcap/tidb/pull/32926)
    - fix Timediff builtin func [#32908](https://github.com/pingcap/tidb/pull/32908)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32840](https://github.com/pingcap/tidb/pull/32840)
    - Fix the bug that locking with NOWAIT does not return immediately when encountering a lock. [#32811](https://github.com/pingcap/tidb/pull/32811)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32798](https://github.com/pingcap/tidb/pull/32798)
    - Fix BR failure on backup rawkv. [#32792](https://github.com/pingcap/tidb/pull/32792)
    - add a scannedKeys in indexWorker, let pushLimited supports partition table [#32731](https://github.com/pingcap/tidb/pull/32731)
    - fix date formate identifies '\n' as invalid separator [#32503](https://github.com/pingcap/tidb/pull/32503)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#32389](https://github.com/pingcap/tidb/pull/32389)
    - fix `alter column set default` wrongly updates the schema [#32264](https://github.com/pingcap/tidb/pull/32264)
    - Fix a bug that caused region unbalanced after restoring. [#32128](https://github.com/pingcap/tidb/pull/32128)
    - Fixed a bug that turning on tidb_restricted_read_only won't automatically turn on tidb_super_read_only [#31841](https://github.com/pingcap/tidb/pull/31841)
    - fix greatest and least function with collation get wrong result [#31837](https://github.com/pingcap/tidb/pull/31837)
    - Fix the crash or error when generating an empty mpp task list. [#31695](https://github.com/pingcap/tidb/pull/31695)
    - ```release-note [#31667](https://github.com/pingcap/tidb/pull/31667)
    - Fix index join bug caused by innerWorker panic [#31614](https://github.com/pingcap/tidb/pull/31614)
    - Fix double column value are different with MySQL after changing column type from float to double [#31572](https://github.com/pingcap/tidb/pull/31572)
    - planner: make queries with the extra column `_tidb_rowid` can use PointGet [#31552](https://github.com/pingcap/tidb/pull/31552)
    - Fix a data race that may cause "invalid transaction" error when executing a query using index lookup join. [#31350](https://github.com/pingcap/tidb/pull/31350)
    - Fix a panic that may happen when using `on duplicate key update`. [#31344](https://github.com/pingcap/tidb/pull/31344)
    - Fix the bug that lighting return error if gcs url starts with gs:// [#31169](https://github.com/pingcap/tidb/pull/31169)
    - ```release-note [#30999](https://github.com/pingcap/tidb/pull/30999)
    - Fix a bug that the `mysql_stmt_field_count` returned to mysql client is incorrect in prepare protocal when handling union statement. [#30997](https://github.com/pingcap/tidb/pull/30997)
    - make tidb-lightning pre-check output message clearer [#30888](https://github.com/pingcap/tidb/pull/30888)
    - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30876](https://github.com/pingcap/tidb/pull/30876)
    - Fix the but that lightning doesn't report error if s3 storage path not exist. [#30714](https://github.com/pingcap/tidb/pull/30714)
    - planner: regard NULL as point when accessing composite index [#30614](https://github.com/pingcap/tidb/pull/30614)
    - fix a bug when reducing order by clause for the index which leads to the wrong result. [#30552](https://github.com/pingcap/tidb/pull/30552)
    - The TiDB server now maps a user to an entry in the mysql.user table more consistently. [#30450](https://github.com/pingcap/tidb/pull/30450)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#30172](https://github.com/pingcap/tidb/pull/30172)
    - lightning: fix log doesn't output to stdout when passing `--log-file="-"` [#29939](https://github.com/pingcap/tidb/pull/29939)


+ TiKV/TiKV

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
    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#12000](https://github.com/tikv/tikv/pull/12000)
    - Increase the size of write batch for raftlog GC to speed up GC. [#11971](https://github.com/tikv/tikv/pull/11971)
    - Fixes the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11913](https://github.com/tikv/tikv/pull/11913)
    - Fix a potential panic (#11746) when snapshot files have been deleted but the peer's status is still Applying. [#11908](https://github.com/tikv/tikv/pull/11908)
    - fix potential high latency caused by destroying a peer [#11880](https://github.com/tikv/tikv/pull/11880)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11857](https://github.com/tikv/tikv/pull/11857)
    - ```release-note [#11805](https://github.com/tikv/tikv/pull/11805)
    - Fix wrong `any_value` result when there are regions returning empty result [#11744](https://github.com/tikv/tikv/pull/11744)
    - update procfs to 0.12.0 [#11726](https://github.com/tikv/tikv/pull/11726)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#11637](https://github.com/tikv/tikv/pull/11637)
    - Please add a release note.
None [#11632](https://github.com/tikv/tikv/pull/11632)
    - Please add a release note.
If you don't think this PR needs a release note then fill it with None.
If this PR will be picked to release branch, then a release note is probably required. [#11616](https://github.com/tikv/tikv/pull/11616)
    - Fix panic when cgroup controller is not mounted [#11582](https://github.com/tikv/tikv/pull/11582)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11568](https://github.com/tikv/tikv/pull/11568)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11564](https://github.com/tikv/tikv/pull/11564)
    - Fix resolved ts lag increased after stoping a tikv [#11537](https://github.com/tikv/tikv/pull/11537)
    - Fix connection abort when too many raft entries are batched into one messages [#11535](https://github.com/tikv/tikv/pull/11535)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11513](https://github.com/tikv/tikv/pull/11513)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11456](https://github.com/tikv/tikv/pull/11456)
    - Do not panic when RocksDB flush or compaction hits disk capacity [#11428](https://github.com/tikv/tikv/pull/11428)
    - make tikv-ctl detect raft db correctly [#11413](https://github.com/tikv/tikv/pull/11413)
    - Fix incorrect by-instance gRPC average duration. [#11330](https://github.com/tikv/tikv/pull/11330)


+ PingCAP/TiFlash

    - fix error result for function `in` [#4076](https://github.com/pingcap/tiflash/pull/4076)
    - Fix cast to decimal overflow bug [#4073](https://github.com/pingcap/tiflash/pull/4073)
    - fix date format identifies '\n' as invalid separator [#4059](https://github.com/pingcap/tiflash/pull/4059)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3936](https://github.com/pingcap/tiflash/pull/3936)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3918](https://github.com/pingcap/tiflash/pull/3918)
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb. [#3757](https://github.com/pingcap/tiflash/pull/3757)
    - Avoid false alert of `DB::Exception: Encode type of coprocessor response is not CHBlock` [#3740](https://github.com/pingcap/tiflash/pull/3740)
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart. [#3708](https://github.com/pingcap/tiflash/pull/3708)
    - Fixed the inconsistent behavior of CastStringAsDecimal between tiflash and tidb/tikv. [#3680](https://github.com/pingcap/tiflash/pull/3680)
    - Fix potential data inconsistency after altering a primary key column to a larger int data type [#3570](https://github.com/pingcap/tiflash/pull/3570)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3480](https://github.com/pingcap/tiflash/pull/3480)
    - Fix tiflash randomly crash when a mpp query is killed. [#3451](https://github.com/pingcap/tiflash/pull/3451)


+ PD

    - None. [#4663](https://github.com/tikv/pd/pull/4663)
    - - fix a bug that operate steps may contain unnecessary or empty JointConsensus steps in certain conditions 
- fix a bug when demoting single voter directly [#4552](https://github.com/tikv/pd/pull/4552)
    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4435](https://github.com/tikv/pd/pull/4435)
    - Improve DR_STATE file content format [#4386](https://github.com/tikv/pd/pull/4386)
    - Fix data race when updating replication mode configuration [#4370](https://github.com/tikv/pd/pull/4370)
    - Fix the issue that the RLock is not released [#4358](https://github.com/tikv/pd/pull/4358)


## Compatibility Changes

+ PingCAP/TiDB

    - Fix the issue that system variable `max_allowed_packet` does not work. [#34056](https://github.com/pingcap/tidb/pull/34056)


## Bug Fixes

+ PingCAP/TiDB

    - executor: fix CTE is block when query report error [#33189](https://github.com/pingcap/tidb/pull/33189)
    - Fix the issue that "rename column" fails when changing column type concurrently. [#33036](https://github.com/pingcap/tidb/pull/33036)
    - Fixed an issue where partition table pruning might not work after server restart (for list partition table) [#32771](https://github.com/pingcap/tidb/pull/32771)
    - planner: fix wrong range calculation for Nulleq function on Enum values [#32495](https://github.com/pingcap/tidb/pull/32495)
    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31448](https://github.com/pingcap/tidb/pull/31448)
    - Fix the bug that lightning will skip some precheck items when restart [#31183](https://github.com/pingcap/tidb/pull/31183)
    - Fix the error that if tidb-lightning doesn't has permission to access mysql.tidb, it will generate kv with wrong format. [#31152](https://github.com/pingcap/tidb/pull/31152)
    - Fix concurrent column type changes(with changing data) that cause schema and data inconsistencies. [#31071](https://github.com/pingcap/tidb/pull/31071)
    - Add a new config to control whether support incremental import. [#30926](https://github.com/pingcap/tidb/pull/30926)
    - executor: fix pipelined window invalid memory address [#30460](https://github.com/pingcap/tidb/pull/30460)
    - Fix the problem that window function may return different results when using transaction or not. [#30392](https://github.com/pingcap/tidb/pull/30392)
    - Fix wrong flen for CastAsString funtion [#30058](https://github.com/pingcap/tidb/pull/30058)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#30016](https://github.com/pingcap/tidb/pull/30016)


+ PingCAP/TiFlash

    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC [#3625](https://github.com/pingcap/tiflash/pull/3625)


+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4577](https://github.com/tikv/pd/pull/4577)
    - Fix incomplete replicate file [#4394](https://github.com/tikv/pd/pull/4394)
    - Fix panic issue after TiKV node scales in [#4382](https://github.com/tikv/pd/pull/4382)



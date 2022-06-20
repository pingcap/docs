---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 Release Notes

Release Date: June xx, 2022

TiDB version: 5.3.2

## __unsorted

+ PingCAP/TiDB

    - release-note [#34722](https://github.com/pingcap/tidb/issues/34722)
    - release-note [#33892](https://github.com/pingcap/tidb/issues/33892)
    - release-note [#34906](https://github.com/pingcap/tidb/issues/34906)
    - release-note [#35340](https://github.com/pingcap/tidb/issues/35340)
    - release-note [#29283](https://github.com/pingcap/tidb/issues/29283)
    - Fixed an issue where extra datums may break binlog. [#33608](https://github.com/pingcap/tidb/issues/33608)
    - release-note [#34447](https://github.com/pingcap/tidb/issues/34447)
    - release-note [#34320](https://github.com/pingcap/tidb/issues/34320)
    - release-note [#34417](https://github.com/pingcap/tidb/issues/34417)
    - release-note [#33509](https://github.com/pingcap/tidb/issues/33509)
    - release-note [#34350](https://github.com/pingcap/tidb/issues/34350)
    - release-note [#27937](https://github.com/pingcap/tidb/issues/27937)
    - lightning: split and scatter regions in batches [#33618](https://github.com/pingcap/tidb/issues/33618)
    - release-note [#34213](https://github.com/pingcap/tidb/issues/34213)
    - Fix the issue that the table attributes don't support index and won't be updated when the partition changes [#33929](https://github.com/pingcap/tidb/issues/33929)
    - Fix a bug of duplicate primary key when insert record into table after incremental restoration. [#33596](https://github.com/pingcap/tidb/issues/33596)
    - release-note [#33893](https://github.com/pingcap/tidb/issues/33893)
    - release-note [#33335](https://github.com/pingcap/tidb/issues/33335)
    - release-note [#33908](https://github.com/pingcap/tidb/issues/33908)
    - Fix the issue that the schedulers won't be resumed after BR/Lightning exits abnormally. [#33546](https://github.com/pingcap/tidb/issues/33546)
    - Fix the issue that privilege-related operations may fail for upgraded clusters. [#33588](https://github.com/pingcap/tidb/issues/33588)
    - Fix the issue that NewCollationEnable config not checked during restoration. [#33422](https://github.com/pingcap/tidb/issues/33422)
    - Fix a bug that BR incremental restore return error by mistake caused by ddl job with empty query. [#33322](https://github.com/pingcap/tidb/issues/33322)
    - Fix the issue that BR not retry enough when region not consistency during restoration. [#33419](https://github.com/pingcap/tidb/issues/33419)
    - release-note [#33310](https://github.com/pingcap/tidb/issues/33310)
    - Fix a bug that caused BR get stuck when restore meets some unrecoverable error. [#33200](https://github.com/pingcap/tidb/issues/33200)
    - executor: fix wrong result of delete multiple tables using left join [#31321](https://github.com/pingcap/tidb/issues/31321)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32733](https://github.com/pingcap/tidb/issues/32733)
    - Fix BR failure on backup rawkv. [#32607](https://github.com/pingcap/tidb/issues/32607)
    - Fix some connections and goroutines leak caused by not closed HTTP response body [#30571](https://github.com/pingcap/tidb/issues/30571)


+ TiKV/TiKV

    - Fix bug which causes frequent pd client reconnection [#12345](https://github.com/tikv/tikv/issues/12345)
    - Report bad health status if raftstore stops working. [#12398](https://github.com/tikv/tikv/issues/12398)
    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12739](https://github.com/tikv/tikv/issues/12739)
    - Fix tikv crash when conv empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12615](https://github.com/tikv/tikv/issues/12615)
    - Fix a bug that sometimes generates a message with zero store id when doing follower read [#12478](https://github.com/tikv/tikv/issues/12478)
    - Add a new hidden config `s3_multi_part_size` to make backup can control the part size when upload big sst file to s3. [#12457](https://github.com/pingcap/tidb/issues/30087)
    - Report bad health status if raftstore stops working. [#12398](https://github.com/tikv/tikv/issues/12398)
    - fix race between split check and destroy [#12368](https://github.com/tikv/tikv/issues/12368)
    - Fixes that successfully committed optimistic transactions may report false WriteConflict on network errors. [#34066](https://github.com/pingcap/tidb/issues/34066)
    - fix tikv panic and peer unexpected destroy due to fake merge target [#12232](https://github.com/tikv/tikv/issues/12232)
    - Fix stale message cause panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - Solve the problem of raft msg memory metrics overflow, which will cause intermittent packet loss and oom. [#12160](https://github.com/tikv/tikv/issues/12160)
    - Fix crash when profiling in Ubuntu 18.04. [#9765](https://github.com/tikv/tikv/issues/9765)
    - Fix logic of error string match in `bad-ssts`. [#12329](https://github.com/tikv/tikv/issues/12329)
    - Pass leader transferee to cdc observer to reduce TiCDC latency spike. [#12111](https://github.com/tikv/tikv/issues/12111)
    - Fix potential linearizability violation in replica reads. [#12109](https://github.com/tikv/tikv/issues/12109)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12048](https://github.com/tikv/tikv/issues/12048)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#11940](https://github.com/tikv/tikv/issues/11940)
    - None. [#10540](https://github.com/tikv/tikv/issues/10540)
    - None. [#11374](https://github.com/tikv/tikv/issues/11374)


+ PingCAP/TiFlash

    - Fix potential query error when select on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - Fix bug that TiFlash query will meet keepalive timeout error randomly. [#4192](https://github.com/pingcap/tiflash/issues/4192)
    - Avoid leaving data on tiflash node which doesn't corresponding to any region range [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - Fix a bug that MPP tasks may leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - Fix the problem that empty segments cannot be merged after gc [#4511](https://github.com/pingcap/tiflash/issues/4511)
    - Fix wrong result of cast(float as decimal) when overflow happens [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - Fix the potential crash issue that occurs when TLS is enabled [#23144](https://github.com/grpc/grpc/issues/23144)
    - fix the problem that expired data was not recycled timely due to slow gc speed [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - Fix the bug that canceled MPP query may cause tasks hang forever when local tunnel is enabled. [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - Fix cast datetime to decimal wrong result bug [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4093](https://github.com/pingcap/tics/issues/4093)
    - Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - Fix potential query error after add column under heavy read workload [#3967](https://github.com/pingcap/tics/issues/3967)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3557](https://github.com/pingcap/tics/issues/3557)
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb. [#3475](https://github.com/pingcap/tics/issues/3475)
    - Avoid false alert of `DB::Exception: Encode type of coprocessor response is not CHBlock` [#3713](https://github.com/pingcap/tiflash/issues/3713)
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart. [#3615](https://github.com/pingcap/tiflash/issues/3615)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3447](https://github.com/pingcap/tics/issues/3447)


+ PD

    - server: disable swagger server [#4932](https://github.com/tikv/pd/issues/4932)
    - Fix the issue that the hot region may cause panic due to no leader [#5005](https://github.com/tikv/pd/issues/5005)
    - None. [#4946](https://github.com/tikv/pd/issues/4946)
    - Fix the issue that scheduling cannot immediately start after PD leader transfers [#4769](https://github.com/tikv/pd/issues/4769)
    - Fix the issue that the removed tombstone store shows again after transferring the PD leader [#4941](https://github.com/tikv/pd/issues/4941)
    - Fix the corner case that may cause TSO fallback. [#4884](https://github.com/tikv/pd/issues/4884)
    - None. [#4805](https://github.com/tikv/pd/issues/4805)
    - Fix the issue that the label distribution has residual labels [#4825](https://github.com/tikv/pd/issues/4825)


+ Tools

    + PingCAP/TiCDC

        - Fix TiCDC incorrectly display stale metrics data on dashboard. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note. If you don't think this PR needs a release note then fill it with `None`. [#4287](https://github.com/pingcap/tiflow/issues/4287)
        - Fix a bug that after auto resume, DM will use more disk space. [#3734](https://github.com/pingcap/tiflow/issues/3734)
        - Fix a bug in redo log manager that flush log executed before writing logs [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix a bug that resolved ts moves too fast when part of tables are not maintained redo writer. [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Add uuid suffix to redo log file name to prevent name conflict, which may cause data loss. [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - `Fix a bug that mysql sink may save a wrong checkpointTs`. [#5107](https://github.com/pingcap/tiflow/issues/5107)
        - Please add a release note. Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note. If you don't think this PR needs a release note then fill it with `None`. [#5344](https://github.com/pingcap/tiflow/issues/5344)
        - Fix DM can't replicate uppercase tables when the task has case-sensitive: false [#5255](https://github.com/pingcap/tiflow/issues/5255)
        - Fix an issue where TiCDC clusters may panic after an upgrade [#5266](https://github.com/pingcap/tiflow/issues/5266)
        - save table checkpoint after a DDL is filtered [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - `None`. [#4464](https://github.com/pingcap/tiflow/issues/4464)
        - fix the issue that ticdc failed to start when connects to  multiple pd endpoints with tls-enabled and the 1st endpoint is not available [#4777](https://github.com/pingcap/tiflow/issues/4777)
        - fix tracker panic when pk of downstream table orders behind [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - `None` [#2792](https://github.com/pingcap/tiflow/issues/2792)
        - fix tracker panic when pk of downstream table orders behind [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - `Fix a bug that openapi may be stuck when pd is abnormal` [#4778](https://github.com/pingcap/tiflow/issues/4778)
        - send one heartbeat for successive skipped GTID when enable relay log [#5063](https://github.com/pingcap/tiflow/issues/5063)
        - fix bug of relay log may turn off after master reboot in v5.3.1 [#4803](https://github.com/pingcap/tiflow/issues/4803)
        - Syncer will use working directory of DM-worker rather than /tmp to write internal files, and clean it after task is stopped [#4107](https://github.com/pingcap/tiflow/issues/4107)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - Fix a bug that sequence should not be replicated even if force-replication is true. Fix data loss when upstream transaction conflicts during cdc reconnection. [#4552](https://github.com/pingcap/tiflow/issues/4552)
        - `None`. [#4554](https://github.com/pingcap/tiflow/issues/4554)
        - Please add a release note. `None`. [#4565](https://github.com/pingcap/tiflow/issues/4565)
        - `None`. [#4135](https://github.com/pingcap/tiflow/issues/4135)



## Compatibility Changes

+ TiDB

    - Fix an issue that REPLACE statement changing other rows when the auto ID is out of range [#29483](https://github.com/pingcap/tidb/issues/29483)


## Improvements

+ TiDB

    -

+ TiKV

    - Delay in raft client to reduce syscalls and improve CPU efficiency [#11309](https://github.com/tikv/tikv/issues/11309)

+ PD

    -

+ TiDB Dashboard

    -

+ TiFlash

    -

+ Tools

    + Backup & Restore (BR)

        -

    + TiCDC

        -

    + Dumpling

        -

    + TiDB Binlog

        -

    + TiDB Data Migration (DM)

        -

    + TiDB Lightning

        -


## Bug Fixes

+ TiDB

    - fix the problem that dumpling can't dump with --compress and s3 output directory. [#30534](https://github.com/pingcap/tidb/issues/30534)
    - Fix the data inconsistency caused by invalid usage of lazy existence check and untouch key optimization. [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the bug that sql got cancel if including json column joins char column. [#29401](https://github.com/pingcap/tidb/issues/29401)

+ TiKV

    -

+ PD

    -

+ TiDB Dashboard

    -

+ TiFlash

    - Fix potential wrong result after a lot of insert and delete operations [#4956](https://github.com/pingcap/tiflash/issues/4956)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#4437](https://github.com/pingcap/tiflash/issues/4437)
    - Fix the issue that a query containing `JOIN` could be hung if an error was encountered [#4195](https://github.com/pingcap/tiflash/issues/4195)

+ Tools

    + Backup & Restore (BR)

        -

    + TiCDC

        -

    + Dumpling

        -

    + TiDB Binlog

        -

    + TiDB Data Migration (DM)

        -

    + TiDB Lightning

        -

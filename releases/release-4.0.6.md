---
title: TiDB 4.0.6 Release Notes
---

# TiDB 4.0.6 Release Notes

Release date: September 9, 2020

TiDB version: 4.0.6

## Improvements

+ TiDB

    - Replace error code and message with standard error [#19888](https://github.com/pingcap/tidb/pull/19888)
    - Table: improve the write performance of partition table [#19649](https://github.com/pingcap/tidb/pull/19649)
    - Optimize the performance of encoding plan. [#19279](https://github.com/pingcap/tidb/pull/19279)
    - Record more RPC runtime information in cop runtime stats [#19264](https://github.com/pingcap/tidb/pull/19264)

+ PD

    - Dashboard: update to v2020.09.08.1 [#2928](https://github.com/pingcap/pd/pull/2928)
    - metrics: add more metrics for region and store heartbeat [#2891](https://github.com/tikv/pd/pull/2891)
    - Change back to the original way to control the low space threshold [#2875](https://github.com/pingcap/pd/pull/2875)
    - Support standard error code [#2918](https://github.com/tikv/pd/pull/2918) [#2911](https://github.com/tikv/pd/pull/2911) [#2913](https://github.com/tikv/pd/pull/2913) [#2915](https://github.com/tikv/pd/pull/2915) [#2912](https://github.com/tikv/pd/pull/2912) [#2907](https://github.com/tikv/pd/pull/2907) [#2906](https://github.com/tikv/pd/pull/2906) [#2903](https://github.com/tikv/pd/pull/2903) [#2806](https://github.com/tikv/pd/pull/2806) [#2900](https://github.com/tikv/pd/pull/2900) [#2902](https://github.com/tikv/pd/pull/2902)

+ TiFlash

    - Add some metrics about apply Region snapshots and ingest SST files [#1088](https://github.com/pingcap/tics/pull/1088)
    - Fix the problem that CN check doesn't work on https_port and metrics_port [#1064](https://github.com/pingcap/tics/pull/1064)## Bug Fixes

+ TiDB

    - Fix issue of tikv_cop_wait time in metric profile. [#19881](https://github.com/pingcap/tidb/pull/19881)
    - Fix wrong result of `SHOW GRANTS` [#19834](https://github.com/pingcap/tidb/pull/19834)
    - Fix incorrect query result for `!= all (subq)`. [#19831](https://github.com/pingcap/tidb/pull/19831)
    - Forbidden creating table in metrics_schema and performance_schema [#19792](https://github.com/pingcap/tidb/pull/19792)
    - Fix bug of converting enum and set [#19778](https://github.com/pingcap/tidb/pull/19778)
    - Add privilege check for `SHOW STATS_META`, `SHOW STATS_BUCKET`. [#19760](https://github.com/pingcap/tidb/pull/19760)
    - Expression: fix unmatched column lengths errors caused by `builtinGreatestStringSig` and `builtinLeastStringSig` [#19758](https://github.com/pingcap/tidb/pull/19758)
    - Fallback vectorize control expressions [#19749](https://github.com/pingcap/tidb/pull/19749)
    - Executor: fix errors in Apply when the type of correlation column is `bit` [#19692](https://github.com/pingcap/tidb/pull/19692)
    - Fix issue of query processlist and cluster_log bug in mysql8 client. [#19690](https://github.com/pingcap/tidb/pull/19690)
    - Fix issue of same type plans with different plan digest. [#19684](https://github.com/pingcap/tidb/pull/19684)
    - Forbidden changing decimal to int [#19682](https://github.com/pingcap/tidb/pull/19682)
    - Executor: fix the issue that `SELECT ... INTO OUTFILE` returns runtim… [#19672](https://github.com/pingcap/tidb/pull/19672)
    - Expression: fix incorrect implementation in `builtinRealIsFalseSig` [#19670](https://github.com/pingcap/tidb/pull/19670)
    - Fix check partition expression miss the parentheses expression [#19614](https://github.com/pingcap/tidb/pull/19614)
    - Fix an query error when there is an Apply upon HashJoin [#19611](https://github.com/pingcap/tidb/pull/19611)
    - Fix incorrect result of vectorized casting real as time [#19594](https://github.com/pingcap/tidb/pull/19594)
    - Fix `SHOW GRANTS` can show grants for not existed user. [#19588](https://github.com/pingcap/tidb/pull/19588)
    - Fix an query error when there is an Apply upon IndexLookupJoin [#19566](https://github.com/pingcap/tidb/pull/19566)
    - Fix wrong results when convert apply to hash join on partition table. [#19546](https://github.com/pingcap/tidb/pull/19546)
    - Executor: fix incorrect results when there is an IndexLookUp under the inner side of an Apply [#19508](https://github.com/pingcap/tidb/pull/19508)
    - Fix unexpected panic when using view [#19491](https://github.com/pingcap/tidb/pull/19491)
    - Fix incorrect result of anti-semi-join query [#19477](https://github.com/pingcap/tidb/pull/19477)
    - Drop stats should delete topn. [#19465](https://github.com/pingcap/tidb/pull/19465)
    - Fix wrong result caused by mistaken usage of batch point get. [#19460](https://github.com/pingcap/tidb/pull/19460)
    - Fix a bug that can't find column in indexLookupJoin with virtual generated column [#19439](https://github.com/pingcap/tidb/pull/19439)
    - Fix the different plans between select and update query. [#19403](https://github.com/pingcap/tidb/pull/19403)
    - Fix data race for tiflash work index in region cache [#19362](https://github.com/pingcap/tidb/pull/19362)
    - Bug fix for logarithm functions [#19291](https://github.com/pingcap/tidb/pull/19291)
    - Fix unexpected error when spilling disk. [#19272](https://github.com/pingcap/tidb/pull/19272)
    - Make single partition table support index join on the inner side. [#19197](https://github.com/pingcap/tidb/pull/19197)
    - Fix wrong hash key for decimal [#19188](https://github.com/pingcap/tidb/pull/19188)

+ TiFlash

    - Fix the issue that TiFlash throw exceptions after modifying column nullable attribute [#1081](https://github.com/pingcap/tics/pull/1081)
    - Fix the issue that after renaming the primary key column in previous versions, TiFlash may not start after upgrading to v4.0.4/v4.0.5 [#1072](https://github.com/pingcap/tics/pull/1072)
    - Fix wrong result of FROM_UNIXTIME when input is NULL [#1047](https://github.com/pingcap/tics/pull/1047)
    - Fix the issue that TiFlash is not available after users applied unsupported column data type modifications [#1009](https://github.com/pingcap/tics/pull/1009)

## Others

+ TiDB

    - Fix the issue that  will raise no regions error when table range end key and region endKey are same. [#19895](https://github.com/pingcap/tidb/pull/19895)
    - Fix an issue that unexpect sucess partition alter [#19891](https://github.com/pingcap/tidb/pull/19891)
    - Support adjust the concurrency on union executor. [#19886](https://github.com/pingcap/tidb/pull/19886)
    - Fix wrong default max allowed packet for push downed expression. [#19876](https://github.com/pingcap/tidb/pull/19876)
    - Fix wrong behavior for `max/min` on ENUM/SET column. [#19869](https://github.com/pingcap/tidb/pull/19869)
    - Add sql digest for process list. [#19829](https://github.com/pingcap/tidb/pull/19829)
    - Switch to pessimistic txn mode for autocommit statement retry [#19796](https://github.com/pingcap/tidb/pull/19796)
    - Fix read failure from system tables `tiflash_segments` and `tiflash_tables` when some tiflash node is down [#19748](https://github.com/pingcap/tidb/pull/19748)
    - Executor: fix file exists errors in tests for `select into outfile` [#19725](https://github.com/pingcap/tidb/pull/19725)
    - Support %r, %T data format in Str_to_date() [#19693](https://github.com/pingcap/tidb/pull/19693)
    - Support out join in broadcast join [#19664](https://github.com/pingcap/tidb/pull/19664)
    - Fix wrong result for aggregation count(col) [#19628](https://github.com/pingcap/tidb/pull/19628)
    - `SELECT INTO OUTFILE` now requires the FILE privilege. [#19577](https://github.com/pingcap/tidb/pull/19577)
    - Not needed, this PR just adds a test case. [#19559](https://github.com/pingcap/tidb/pull/19559)
    - Executor: rename test files for `select into outfile` to avoid `file exists error` [#19551](https://github.com/pingcap/tidb/pull/19551)
    - Support stddev_pop function. [#19541](https://github.com/pingcap/tidb/pull/19541)
    - Avoid DDL retry taking too long [#19488](https://github.com/pingcap/tidb/pull/19488)
    - Allow `alter table db.t1 add constraint fk foreign key (c2) references t2(c1)` like statements without first executing `use db` [#19471](https://github.com/pingcap/tidb/pull/19471)
    - Fix INFORMATION_SCHEMA.CLUSTER_HARDWARE dose not have raid0 devices information [#19457](https://github.com/pingcap/tidb/pull/19457)
    - Invalid SQL statements (dispatch errors) have been changed from an Error to an Info message in the server log file. [#19454](https://github.com/pingcap/tidb/pull/19454)
    - Fix a runtime error in `TRUNCATE` [#19445](https://github.com/pingcap/tidb/pull/19445)
    - Add `TiDB-Runtime` dashboard [#19396](https://github.com/pingcap/tidb/pull/19396)
    - Ddl: exit add index on generated column with `case-when` expression parse error [#19395](https://github.com/pingcap/tidb/pull/19395)
    - Fix issue 19371 - PREPARE statement FROM @Var (where Var contains uppercase characters fail) [#19378](https://github.com/pingcap/tidb/pull/19378)
    - Improve compatibility for ALTER TABLE algorithms [#19364](https://github.com/pingcap/tidb/pull/19364)
    - Fix a schema charset modification panic bug in an uppercase schema. [#19302](https://github.com/pingcap/tidb/pull/19302)
    - Planner: encode insert/delete/update plan in slow log plan field. [#19269](https://github.com/pingcap/tidb/pull/19269)
    - Fix inconsistence of Plan between information_schema.statements_summary and explain, which contains tikv/tiflash info. [#19159](https://github.com/pingcap/tidb/pull/19159)

+ TiKV

    - Optimize QPS drop when doing UnsafeDestroyRange [#8627](https://github.com/tikv/tikv/pull/8627)
    - Fix the estimation error for a non-index column with collation enabled. [#8620](https://github.com/tikv/tikv/pull/8620)
    - Error-code: support to generate metafile [#8619](https://github.com/tikv/tikv/pull/8619)
    - Add perf statistics for cf scan detail [#8618](https://github.com/tikv/tikv/pull/8618)
    - Fix the deadlock between the PD client thread and other threads calling PD sync requests. [#8612](https://github.com/tikv/tikv/pull/8612)
    - Fix a panic issue if a TiKV runs very slow during conf change. [#8497](https://github.com/tikv/tikv/pull/8497)
    - Add perf context panel for grafana template [#8467](https://github.com/tikv/tikv/pull/8467)
    - Update jemalloc to 5.2.1 [#8463](https://github.com/tikv/tikv/pull/8463)
    - Fix the issue that green GC may miss locks during transferring regions. [#8460](https://github.com/tikv/tikv/pull/8460)
    - Support float CPU quota in cgroup. [#8427](https://github.com/tikv/tikv/pull/8427)

+ PD

    - Add `initial-cluster-token` configuration to avoid different clusters communicate during bootstrap [#2922](https://github.com/pingcap/pd/pull/2922)
    - Fix the unit of store limit rate when the mode is auto [#2826](https://github.com/pingcap/pd/pull/2826)
    - Fix the issue that some scheduler persist config without solving error [#2818](https://github.com/tikv/pd/pull/2818)
    - fix empty http response in scheduler [#2871](https://github.com/tikv/pd/pull/2871) [#2874](https://github.com/tikv/pd/pull/2874)

+ TiFlash

    - `Do not optimize applying snapshot by multi-thread when raftstore.snap-handle-pool-size is 0` [#1086](https://github.com/pingcap/tics/pull/1086)
    - `Fix bug causes segment fault while computing table sync status` [#1077](https://github.com/pingcap/tics/pull/1077)
    - For invalid collation, treated as `utf8mb4_bin` in TiFlash [#1069](https://github.com/pingcap/tics/pull/1069)
    - Added some Grafana panels about write stall, and added some settings to avoid write stall. [#1051](https://github.com/pingcap/tics/pull/1051)

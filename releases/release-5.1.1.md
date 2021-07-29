---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

Release Date: July 30, 2021

TiDB version: 5.1.1

## Compatibility change

+ TiDB

    - For users upgrading from TiDB 4.0, the value of tidb_multi_statement_mode is now OFF. It is recommended to use the multi-statement feature of your client library instead, see the documentation on tidb_multi_statement_mode for additional details. [#25751](https://github.com/pingcap/tidb/pull/25751)
    - exec: access the table_storage_stats need super privilege [#26352](https://github.com/pingcap/tidb/pull/26352)
    - Accessing information_schema.user_privileges will now requires the SELECT privilege on mysql.user in order to show other user's privileges. [#26311](https://github.com/pingcap/tidb/pull/26311)
    - Reading from the table information_schema.cluster_hardware now requires the CONFIG privilege.
    - Reading from the table information_schema.cluster_info now requires the Process privilege.
    - Reading from the table information_schema.cluster_load now requires the Process privilege.
    - Reading from the table information_schema.cluster_systeminfo now requires the Process privilege.
    - Reading from the table information_schema.cluster_log now requires the Process privilege. [#26297](https://github.com/pingcap/tidb/pull/26297)
    - Reading from the table information_schema.cluster_config now requires the CONFIG privilege. [#26150](https://github.com/pingcap/tidb/pull/26150)
    - Improve the MySQL compatibility of str_to_date for %b/%M/%r/%T [#25768](https://github.com/pingcap/tidb/pull/25768)

## Feature enhancements

+ TiDB Dashboard

    - TiDB Dashboard: Add OIDC based SSO support [#3883](https://github.com/tikv/pd/pull/3883)

+ TiFlash

    - Support the `HAVING()` function in DAG requests

## Improvements

+ TiDB

    - Announce the general availability (GA) of the Stale Read feature
    - avoid alloc for paramMarker in buildValuesListOfInsert [#26076](https://github.com/pingcap/tidb/pull/26076)
    - planner: support stable result mode [#25995](https://github.com/pingcap/tidb/pull/25995)
    - Enable the pushdown of builtin function json_unquote() to TiKV. [#26265](https://github.com/pingcap/tidb/pull/26265)
    - store/copr: support retry for mpp query [#26480](https://github.com/pingcap/tidb/pull/26480)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26225](https://github.com/pingcap/tidb/pull/26225)
    - Forbid creating view from stale query [#26200](https://github.com/pingcap/tidb/pull/26200)
    - planner/core: thoroughly push down count-distinct agg in the MPP mode. [#26194](https://github.com/pingcap/tidb/pull/26194)
    - mpp: check the tiflash availabilities before launching mpp queries. [#26192](https://github.com/pingcap/tidb/pull/26192)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25874](https://github.com/pingcap/tidb/pull/25874)
    - Do not allow setting read timestamp to a future time. [#25763](https://github.com/pingcap/tidb/pull/25763)
    - Log warnings when agg function can not be pushdown in explain statement [#25737](https://github.com/pingcap/tidb/pull/25737)
    - Add cluster information of evicted count. [#25587](https://github.com/pingcap/tidb/pull/25587)    - Enable the pushdown of builtin function json_unquote() to TiKV. [#26265](https://github.com/pingcap/tidb/pull/26265)
    - store/copr: support retry for mpp query [#26480](https://github.com/pingcap/tidb/pull/26480)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26225](https://github.com/pingcap/tidb/pull/26225)
    - Forbid creating view from stale query [#26200](https://github.com/pingcap/tidb/pull/26200)
    - planner/core: thoroughly push down count-distinct agg in the MPP mode. [#26194](https://github.com/pingcap/tidb/pull/26194)
    - mpp: check the tiflash availabilities before launching mpp queries. [#26192](https://github.com/pingcap/tidb/pull/26192)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25874](https://github.com/pingcap/tidb/pull/25874)
    - Do not allow setting read timestamp to a future time. [#25763](https://github.com/pingcap/tidb/pull/25763)
    - Log warnings when agg function can not be pushdown in explain statement [#25737](https://github.com/pingcap/tidb/pull/25737)
    - Add cluster information of evicted count. [#25587](https://github.com/pingcap/tidb/pull/25587)

+ TiKV

    - Make the prewrite requests as idempotent as possible to reduce the chance of undetermined errors [#10586](https://github.com/tikv/tikv/pull/10586)
    - Prevent the risk of stack overflow when handling many expired commands [#10502](https://github.com/tikv/tikv/pull/10502)
    - Avoid excessive commit request retrying by not updating `max_ts` using the Stale Read request's `start_ts` [#10451](https://github.com/tikv/tikv/pull/10451)
    - Handle read ready and write ready separately to reduce read latency [#10592](https://github.com/tikv/tikv/pull/10592)
    - Reduce the impact on data import speed when the I/O rate limiting is enabled [#10390](https://github.com/tikv/tikv/pull/10390)
    - Improve the load balance between Raft gRPC connections [#10495](https://github.com/tikv/tikv/pull/10495)

+ Tools

    + TiCDC

        - Remove `file sorter` [#2327](https://github.com/pingcap/ticdc/pull/2327)
        - Better err msg when PD endpoint missing certificate [#2186](https://github.com/pingcap/ticdc/pull/2186)

    + TiDB Lightning

        - Add retry for restoring schemas [#1294](https://github.com/pingcap/br/pull/1294)

    + Dumpling

        - Always split tables using _tidb_rowid when the upstream is a TiDB v3.x cluster, which helps reduce TiDB's memory [#308](https://github.com/pingcap/dumpling/pull/308)
        - Reduce dumpling accessing database and information_schema usage and improve dumpling's stability. [#315](https://github.com/pingcap/dumpling/pull/315)

## Bug fixes

+ TiDB

    - amend transactions correctly when "modify column" needs reorg data with tidb_enable_amend_pessimistic_txn=on. [#26273](https://github.com/pingcap/tidb/pull/26273)
    - fix incompatible last_day func behavior in sql mode [#26001](https://github.com/pingcap/tidb/pull/26001)
    - Make sure limit outputs no more columns than its child [#25980](https://github.com/pingcap/tidb/pull/25980)
    - Fix the issue that committing pessimistic transactions may report write-conflict errors. [#25973](https://github.com/pingcap/tidb/pull/25973)
    - planner: handle other-conditions from subqueries correctly when constructing IndexJoin [#25819](https://github.com/pingcap/tidb/pull/25819)
    - Fix the bug that successful optimistic transactions may report commit errors. [#25803](https://github.com/pingcap/tidb/pull/25803)
    - Fix incorrect result of set type for merge join [#25695](https://github.com/pingcap/tidb/pull/25695)
    - Fix the bug that index keys in a pessimistic transaction may be repeatedly committed. [#26482](https://github.com/pingcap/tidb/pull/26482)
    - planner: fix the risk of integer overflow when locating partitions [#26471](https://github.com/pingcap/tidb/pull/26471)
    - ddl: fix cast date as timestamp will write invalid value [#26395](https://github.com/pingcap/tidb/pull/26395)
    - Fix copt-cache metrics, it will display the number of hits/miss/evict on Grafana. [#26344](https://github.com/pingcap/tidb/pull/26344)
    - fix the bug of annoying logs caused by telemetry [#26284](https://github.com/pingcap/tidb/pull/26284)
    - fix a bug on the query range of prefix index [#26262](https://github.com/pingcap/tidb/pull/26262)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26239](https://github.com/pingcap/tidb/pull/26239)
    - planner/core: fix duplicate enum items [#26202](https://github.com/pingcap/tidb/pull/26202)
    - executor: fix a bug that cte.iterOutTbl did not close correctly [#26148](https://github.com/pingcap/tidb/pull/26148)
    - load: fix load data with non-utf8 can succeed [#26144](https://github.com/pingcap/tidb/pull/26144)
    - fix unsigned int window function error [#26027](https://github.com/pingcap/tidb/pull/26027)
    - Fix the issue that TiDB may panic when resolving async-commit locks. [#25862](https://github.com/pingcap/tidb/pull/25862)
    - Make Stale Read fully support prepare statement [#25800](https://github.com/pingcap/tidb/pull/25800)
    - Fix the issue that ODBC-styled literal(like {d '2020-01-01'}...) cannot be used as the expression. [#25578](https://github.com/pingcap/tidb/pull/25578)
    - fix the bug about unnecessary error when run tidb only [#25555](https://github.com/pingcap/tidb/pull/25555)

+ TiKV

    - Fix duration calculation panics on certain platforms [#10569](https://github.com/tikv/tikv/pull/10569)
    - Fix unencoded keys of `batch_get_command` in load-base-split [#10565](https://github.com/tikv/tikv/pull/10565)
    - Fix online changing `resolved-ts.advance-ts-interval` can't take effect immediately [#10494](https://github.com/tikv/tikv/pull/10494)
    - Fix follower meta corruption in rare cases with more than 4 replicas [#10486](https://github.com/tikv/tikv/pull/10486)
    - Fix panic when building a snapshot twice with encryption enabled [#10464](https://github.com/tikv/tikv/pull/10464)
    - Fix wrong `tikv_raftstore_hibernated_peer_state` metric [#10432](https://github.com/tikv/tikv/pull/10432)
    - Fix the wrong arguments type of `json_unquote` [#10428](https://github.com/tikv/tikv/pull/10428)
    - Fix the bug that index keys in a pessimistic transaction may be repeatedly committed [#10586](https://github.com/tikv/tikv/pull/10586)
    - Fix `ReadIndex` command returning stale result right after leader is transferred [#10474](https://github.com/tikv/tikv/pull/10474)

+ PD

    - Reduce the conflict due to multiple scheduler running in same time [#3857](https://github.com/tikv/pd/pull/3857)
    - Fix the issue that the scheduler may appear again even if we have already executed the delete operation [#3824](https://github.com/tikv/pd/pull/3824)

+ TiFlash

    - Fix the potential panic issue that occurs when running table scan tasks
    - Fix a bug that TiFlash raises error about `duplicated region` when handling DAQ request
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the potential panic issue that occures when executing `DateFormat` function
    - Fix the potential memory leak issue that occurs when executing MPP tasks
    - Fix the issue of unexpected results when executing aggregation functions `COUNT` or `COUNT DISTINCT`
    - Fix a potential bug that TiFlash can not restore data when deployed on multi disks
    - Fix the issue that TiDB Dashboard can not display disk information of TiFlash correctly
    - Fix the potential panic issue that occures when deconstructing `SharedQueryBlockInputStream`
    - Fix the potential panic issue that occures when deconstructing `MPPTask`
    - Fix the potential data inconsistency after synchronizing data via snapshot

+ Tools

    + TiCDC

        - Fix support for new collation [#2306](https://github.com/pingcap/ticdc/pull/2306)
        - Fix minor runtime panic risk [#2300](https://github.com/pingcap/ticdc/pull/2300)
        - Fix potential DDL loss when owner crashes while executing DDL [#2290](https://github.com/pingcap/ticdc/pull/2290)
        - Fix trying to resolve locks prematurely [#2266](https://github.com/pingcap/ticdc/pull/2266)
        - Fix a bug that could cause data losses if a TiCDC node is killed immediately after a table migration [#2033](https://github.com/pingcap/ticdc/pull/2033)
        - Fix changefeed update to properly handle --sort-dir and --start-ts. [#1921](https://github.com/pingcap/ticdc/pull/1921)

    + Backup & Restore

        - Fix incorrectly calculating the size of data to restore [#1285](https://github.com/pingcap/br/pull/1285)
        - Fix missed DDL events when restoring from cdclog [#1094](https://github.com/pingcap/br/pull/1094)

    + TiDB Lightning

        - Fix parquet parser for decimal type [#1272](https://github.com/pingcap/br/pull/1272)
        - Fix integer overflows when calculating key intervals [#1294](https://github.com/pingcap/br/pull/1294)

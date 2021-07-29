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

    - Support OIDC SSO. By setting the OIDC-compatible SSO services (such as Okta and Auth0), users can log into TiDB Dashboard without entering the SQL password. [#3883](https://github.com/tikv/pd/pull/3883)

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
        - Improve the error message returned when a PD endpoint misses the certificate [#1973](https://github.com/pingcap/ticdc/issues/1973)

    + TiDB Lightning

        - Add a retry mechanism for restoring schemas [#1294](https://github.com/pingcap/br/pull/1294)

    + Dumpling

        - Always split tables using `_tidb_rowid` when the upstream is a TiDB v3.x cluster, which helps reduce TiDB's memory usage [#295](https://github.com/pingcap/dumpling/issues/295)
        - Reduce the frequency of accessing the database metadata to improve Dumpling's performance and stability [#315](https://github.com/pingcap/dumpling/pull/315)

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

    - Fix the issue that the duration calculation might panic on certain platforms [#10569](https://github.com/tikv/tikv/pull/10569)
    - Fix the issue that Load Base Split mistakenly uses the unencoded keys of `batch_get_command` [#10565](https://github.com/tikv/tikv/pull/10565)
    - Fix the issue that changing the `resolved-ts.advance-ts-interval` configuration online cannot take effect immediately [#10494](https://github.com/tikv/tikv/pull/10494)
    - Fix the issue of follower metadata corruption in rare cases with more than 4 replicas [#10486](https://github.com/tikv/tikv/pull/10486)
    - Fix the panic issue that occurs when building a snapshot twice if encryption is enabled [#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    - Fix the wrong `tikv_raftstore_hibernated_peer_state` metric [#10432](https://github.com/tikv/tikv/pull/10432)
    - Fix the wrong arguments type of the `json_unquote()` function in the coprocessor [#10176](https://github.com/tikv/tikv/issues/10176)
    - Fix a bug that the index keys in a pessimistic transaction might be repeatedly committed [#10586](https://github.com/tikv/tikv/pull/10586)
    - Fix the issue that the `ReadIndex` request returns stale result right after the leader is transferred [#10474](https://github.com/tikv/tikv/pull/10474)

+ PD

    - Fix the issue the expected scheduling cannot be generated when the conflict occurs due to multiple schedulers running at the same time [#3857](https://github.com/tikv/pd/pull/3857)
    - Fix the issue that the scheduler might appear again even if the scheduler is already deleted [#3824](https://github.com/tikv/pd/pull/3824)

+ TiFlash

    - Fix the potential panic issue that occurs when running table scan tasks
    - Fix a bug that TiFlash raises the error about `duplicated region` when handling DAQ requests
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the potential panic issue that occurs when executing the `DateFormat` function
    - Fix the potential memory leak issue that occurs when executing MPP tasks
    - Fix the issue of unexpected results when executing the aggregation functions `COUNT` or `COUNT DISTINCT`
    - Fix a potential bug that TiFlash cannot restore data when deployed on multiple disks
    - Fix the issue that TiDB Dashboard cannot display the disk information of TiFlash correctly
    - Fix the potential panic issue that occurs when deconstructing `SharedQueryBlockInputStream`
    - Fix the potential panic issue that occurs when deconstructing `MPPTask`
    - Fix the potential issue of data inconsistency after synchronizing data via snapshot

+ Tools

    + TiCDC

        - Fix the support for the new collation feature [#2301](https://github.com/pingcap/ticdc/issues/2301)
        - Fix the issue that an unsynchronized access to a shared map at runtime might cause panic [#2300](https://github.com/pingcap/ticdc/pull/2300)
        - Fix the potential DDL loss issue that occurs when the owner crashes while executing the DDL statement [#2290](https://github.com/pingcap/ticdc/pull/2290)
        - Fix the issue of trying to resolve locks in TiDB prematurely [#2266](https://github.com/pingcap/ticdc/pull/2266)
        - Fix a bug that might cause data loss if a TiCDC node is killed immediately after a table migration [#2033](https://github.com/pingcap/ticdc/pull/2033)
        - Fix the handling logic of `changefeed update` to `--sort-dir` and `--start-ts` [#1921](https://github.com/pingcap/ticdc/pull/1921)

    + Backup & Restore

        - Fix the issue that the size of the data to restore is incorrectly calculated [#1285](https://github.com/pingcap/br/pull/1285)
        - Fix the issue of missed DDL events that occurs when restoring from cdclog [#1094](https://github.com/pingcap/br/pull/1094)

    + TiDB Lightning

        - Fix parquet parser for decimal type [#1272](https://github.com/pingcap/br/pull/1272)
        - Fix the issue of integer overflow when calculating key intervals [#1294](https://github.com/pingcap/br/pull/1294)

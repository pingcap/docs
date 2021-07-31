---
title: TiDB 5.1.1 Release Notes
category: Releases
---



# TiDB 5.1.1 Release Notes

Release Date: July 31, 2021

TiDB version: 5.1.1

## __unsorted

+ PingCAP/TiDB

    - New system variable tidb_enable_auto_increment_in_generated to allow generated columns and expression indexes that use auto incremented columns (This breaks compatibility with MySQL which does not allow this) [#26702](https://github.com/pingcap/tidb/pull/26702)
    - Fix then bug if the CTE is referenced more than once. [#26661](https://github.com/pingcap/tidb/pull/26661)
    - planner: fix CTE bug when MergeJoin is used [#26658](https://github.com/pingcap/tidb/pull/26658)
    - Fix a bug 'select for update' does not correctly lock the data when a normal table join a partition table. [#26631](https://github.com/pingcap/tidb/pull/26631)
    - Fix a panic when select for update on a normal table join a partition table [#26563](https://github.com/pingcap/tidb/pull/26563)
    - Fix the bug that index keys in a pessimistic transaction may be repeatedly committed. [#26482](https://github.com/pingcap/tidb/pull/26482)
    - store/copr: support retry for mpp query [#26480](https://github.com/pingcap/tidb/pull/26480)
    - planner: fix the risk of integer overflow when locating partitions [#26471](https://github.com/pingcap/tidb/pull/26471)
    - ddl: fix cast date as timestamp will write invalid value [#26395](https://github.com/pingcap/tidb/pull/26395)
    - exec: access the table_storage_stats need super privilege [#26352](https://github.com/pingcap/tidb/pull/26352)
    - Fix copt-cache metrics, it will display the number of  hits/miss/evict on Grafana. [#26344](https://github.com/pingcap/tidb/pull/26344)
    - Accessing information_schema.user_privileges will now requires the SELECT privilege on mysql.user in order to show other user's privileges. [#26311](https://github.com/pingcap/tidb/pull/26311)
    - Reading from the table information_schema.cluster_hardware now requires the CONFIG privilege.
- Reading from the table information_schema.cluster_info now requires the Process privilege.
- Reading from the table information_schema.cluster_load now requires the Process privilege.
- Reading from the table information_schema.cluster_systeminfo now requires the Process privilege.
- Reading from the table information_schema.cluster_log now requires the Process privilege. [#26297](https://github.com/pingcap/tidb/pull/26297)
    - fix the bug of annoying logs caused by telemetry [#26284](https://github.com/pingcap/tidb/pull/26284)
    - Enable the pushdown of builtin function json_unquote() to TiKV. [#26265](https://github.com/pingcap/tidb/pull/26265)
    - fix a bug on the query range of prefix index [#26262](https://github.com/pingcap/tidb/pull/26262)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26239](https://github.com/pingcap/tidb/pull/26239)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26225](https://github.com/pingcap/tidb/pull/26225)
    - planner/core: fix duplicate enum items [#26202](https://github.com/pingcap/tidb/pull/26202)
    - Forbid creating view from stale query [#26200](https://github.com/pingcap/tidb/pull/26200)
    - planner/core: thoroughly push down count-distinct agg in the MPP mode. [#26194](https://github.com/pingcap/tidb/pull/26194)
    - mpp: check the tiflash availabilities before launching mpp queries. [#26192](https://github.com/pingcap/tidb/pull/26192)
    - Reading from the table information_schema.cluster_config now requires the CONFIG privilege. [#26150](https://github.com/pingcap/tidb/pull/26150)
    - executor: fix a bug that cte.iterOutTbl did not close correctly [#26148](https://github.com/pingcap/tidb/pull/26148)
    - load: fix load data with non-utf8 can succeed [#26144](https://github.com/pingcap/tidb/pull/26144)
    - fix unsigned int window function error [#26027](https://github.com/pingcap/tidb/pull/26027)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25874](https://github.com/pingcap/tidb/pull/25874)
    - Fix the issue that TiDB may panic when resolving async-commit locks. [#25862](https://github.com/pingcap/tidb/pull/25862)
    - Make Stale Read fully support prepare statement [#25800](https://github.com/pingcap/tidb/pull/25800)
    - Improve the MySQL compatibility of str_to_date for %b/%M/%r/%T [#25768](https://github.com/pingcap/tidb/pull/25768)
    - Do not allow setting read timestamp to a future time. [#25763](https://github.com/pingcap/tidb/pull/25763)
    - Log warnings when agg function can not be pushdown in explain statement [#25737](https://github.com/pingcap/tidb/pull/25737)
    - Add cluster information of evicted count. [#25587](https://github.com/pingcap/tidb/pull/25587)
    - Fix the issue that ODBC-styled literal(like {d '2020-01-01'}...) cannot be used as the expression. [#25578](https://github.com/pingcap/tidb/pull/25578)
    - fix the bug about unnecessary error when run tidb only [#25555](https://github.com/pingcap/tidb/pull/25555)


+ TiKV/TiKV

    - Database restored from BR or Lightning Local-backend is now smaller, should be matching the original cluster size when backed up. [#10644](https://github.com/tikv/tikv/pull/10644)
    - Make prewrite as idempotent as possible to reduce the chance of undetermined errors. [#10586](https://github.com/tikv/tikv/pull/10586)
    - Fix duration calculation panics on certain platforms [#10569](https://github.com/tikv/tikv/pull/10569)
    - Fix unencoded keys of `batch_get_command` in load-base-split [#10565](https://github.com/tikv/tikv/pull/10565)
    - Prevent the risk of stack overflow when handling many expired commands. [#10502](https://github.com/tikv/tikv/pull/10502)
    - Fix online changing `resolved-ts.advance-ts-interval` can't take effect immediately [#10494](https://github.com/tikv/tikv/pull/10494)
    - - fix follower meta corruption in rare cases with more than 4 replicas [#10486](https://github.com/tikv/tikv/pull/10486)
    - ```release-note [#10466](https://github.com/tikv/tikv/pull/10466)
    - Avoid panic when building a snapshot twice if encryption enabled [#10464](https://github.com/tikv/tikv/pull/10464)
    - Not use the stale read request's `start_ts` to update `max_ts` to avoid commit request keep retrying [#10451](https://github.com/tikv/tikv/pull/10451)
    - Fix wrong tikv_raftstore_hibernated_peer_state metric. [#10432](https://github.com/tikv/tikv/pull/10432)
    - copr: fix the wrong arguments type of json_unquote [#10428](https://github.com/tikv/tikv/pull/10428)
    - ```release-note [#10382](https://github.com/tikv/tikv/pull/10382)


+ PD

    - TiDB Dashboard: Add OIDC based SSO support [#3883](https://github.com/tikv/pd/pull/3883)
    - Reduce the conflict due to multiple scheduler running in same time [#3857](https://github.com/tikv/pd/pull/3857)
    - Fix the issue that the scheduler may appear again even if we have already executed the delete operation [#3824](https://github.com/tikv/pd/pull/3824)


## Bug Fixes

+ PingCAP/TiDB

    - Keep the overflow check logic same with mysql [#26725](https://github.com/pingcap/tidb/pull/26725)
    - Fix #26147 that `tidb` returns an `unknow` error with no message while it should return the error that contains `pd is timeout`. [#26682](https://github.com/pingcap/tidb/pull/26682)
    - Fix wrong charset and collation for case when function [#26673](https://github.com/pingcap/tidb/pull/26673)
    - Fix the case that TiDB would return the wrong result when the children of the UNION contain pure NULL values [#26572](https://github.com/pingcap/tidb/pull/26572)
    - Fix the issue that greatest(datetime) union null returns empty string [#26566](https://github.com/pingcap/tidb/pull/26566)
    - amend transactions correctly when "modify column" needs reorg data with tidb_enable_amend_pessimistic_txn=on. [#26273](https://github.com/pingcap/tidb/pull/26273)
    - fix incompatible last_day func behavior in sql mode [#26001](https://github.com/pingcap/tidb/pull/26001)
    - Make sure limit outputs no more columns than its child [#25980](https://github.com/pingcap/tidb/pull/25980)
    - Fix the issue that committing pessimistic transactions may report write-conflict errors. [#25973](https://github.com/pingcap/tidb/pull/25973)
    - planner: handle other-conditions from subqueries correctly when constructing IndexJoin [#25819](https://github.com/pingcap/tidb/pull/25819)
    - Fix the bug that successful optimistic transactions may report commit errors. [#25803](https://github.com/pingcap/tidb/pull/25803)
    - Fix incorrect result of set type for merge join [#25695](https://github.com/pingcap/tidb/pull/25695)


## Improvements

+ PingCAP/TiDB

    - Trigger auto-analyze based on histogram row count [#26708](https://github.com/pingcap/tidb/pull/26708)
    - planner: update the correlation adjustment rule about Limit/TopN for TableScan [#26654](https://github.com/pingcap/tidb/pull/26654)
    - planner: push TopN down when N is less than a specific variable [#26646](https://github.com/pingcap/tidb/pull/26646)
    - avoid alloc for paramMarker in buildValuesListOfInsert [#26076](https://github.com/pingcap/tidb/pull/26076)
    - planner: support stable result mode [#25995](https://github.com/pingcap/tidb/pull/25995)


+ TiKV/TiKV

    - - separate read write ready to reduce read latency [#10592](https://github.com/tikv/tikv/pull/10592)


## Compatibility Changes

+ PingCAP/TiDB

    - For users upgrading from TiDB 4.0, the value of tidb_multi_statement_mode is now OFF. It is recommended to use the multi-statement feature of your client library instead, see the documentation on tidb_multi_statement_mode for additional details. [#25751](https://github.com/pingcap/tidb/pull/25751)



---
title: TiDB 5.0.3 Release Notes
category: Releases
---



# TiDB 5.0.3 Release Notes

Release Date: July 22, 2021

TiDB version: 5.0.3

## __unsorted

+ tidb

    - Fix copt-cache metrics, it will display the number of  hits/miss/evict on Grafana. [#26343](https://github.com/pingcap/tidb/pull/26343)
    - Accessing information_schema.user_privileges will now requires the SELECT privilege on mysql.user in order to show other user's privileges. [#26310](https://github.com/pingcap/tidb/pull/26310)
    - fix a bug on the query range of prefix index  [#26261](https://github.com/pingcap/tidb/pull/26261)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26238](https://github.com/pingcap/tidb/pull/26238)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26224](https://github.com/pingcap/tidb/pull/26224)
    - TiDB now supports the mysql system variable init_connect and associated functionality. [#26072](https://github.com/pingcap/tidb/pull/26072)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25873](https://github.com/pingcap/tidb/pull/25873)
    - planner: check filter condition in func convertToPartialTableScan [#25806](https://github.com/pingcap/tidb/pull/25806)


+ tikv

    - Fix duration calculation panics on certain platforms [#10571](https://github.com/tikv/tikv/pull/10571)
    - - fix follower meta corruption in rare cases with more than 4 replicas [#10500](https://github.com/tikv/tikv/pull/10500)
    - Ensure panic output is flushed to the log [#10487](https://github.com/tikv/tikv/pull/10487)
    - ```release-note [#10361](https://github.com/tikv/tikv/pull/10361)
    - Add Read duration and throughput metrics for TiKV [#10356](https://github.com/tikv/tikv/pull/10356)


## enhancement

+ tidb

    - avoid alloc for paramMarker in buildValuesListOfInsert [#26075](https://github.com/pingcap/tidb/pull/26075)


## bug-fix

+ tidb

    - fix incompatible last_day func behavior in sql mode [#26000](https://github.com/pingcap/tidb/pull/26000)
    - Fix panic when 'select ... for update' works on a join operation and the join uses partition table [#25845](https://github.com/pingcap/tidb/pull/25845)



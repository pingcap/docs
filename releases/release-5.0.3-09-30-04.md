---
title: TiDB 5.0.3 Release Notes
category: Releases
---



# TiDB 5.0.3 Release Notes

Release Date: July 22, 2021

TiDB version: 5.0.3

## __unsorted

+ tidb

    - No release note [#26364](https://api.github.com/repos/pingcap/tidb/pulls/26364)
    - Fix copt-cache metrics, it will display the number of  hits/miss/evict on Grafana. [#26343](https://api.github.com/repos/pingcap/tidb/pulls/26343)
    - Accessing information_schema.user_privileges will now requires the SELECT privilege on mysql.user in order to show other user's privileges. [#26310](https://api.github.com/repos/pingcap/tidb/pulls/26310)
    - fix a bug on the query range of prefix index  [#26261](https://api.github.com/repos/pingcap/tidb/pulls/26261)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26238](https://api.github.com/repos/pingcap/tidb/pulls/26238)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26224](https://api.github.com/repos/pingcap/tidb/pulls/26224)
    - No release note [#26134](https://api.github.com/repos/pingcap/tidb/pulls/26134)
    - TiDB now supports the mysql system variable init_connect and associated functionality. [#26072](https://api.github.com/repos/pingcap/tidb/pulls/26072)
    - No release note [#25990](https://api.github.com/repos/pingcap/tidb/pulls/25990)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25873](https://api.github.com/repos/pingcap/tidb/pulls/25873)
    - planner: check filter condition in func convertToPartialTableScan [#25806](https://api.github.com/repos/pingcap/tidb/pulls/25806)


+ tikv

    - Fix duration calculation panics on certain platforms [#10571](https://api.github.com/repos/tikv/tikv/pulls/10571)
    - - fix follower meta corruption in rare cases with more than 4 replicas [#10500](https://api.github.com/repos/tikv/tikv/pulls/10500)
    - No Release Note [#10496](https://api.github.com/repos/tikv/tikv/pulls/10496)
    - Ensure panic output is flushed to the log [#10487](https://api.github.com/repos/tikv/tikv/pulls/10487)
    - ```release-note [#10361](https://api.github.com/repos/tikv/tikv/pulls/10361)
    - Add Read duration and throughput metrics for TiKV [#10356](https://api.github.com/repos/tikv/tikv/pulls/10356)


## enhancement

+ tidb

    - avoid alloc for paramMarker in buildValuesListOfInsert [#26075](https://api.github.com/repos/pingcap/tidb/pulls/26075)


## bug-fix

+ tidb

    - fix incompatible last_day func behavior in sql mode [#26000](https://api.github.com/repos/pingcap/tidb/pulls/26000)
    - Fix panic when 'select ... for update' works on a join operation and the join uses partition table [#25845](https://api.github.com/repos/pingcap/tidb/pulls/25845)



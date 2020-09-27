---
title: TiDB 4.0.7 Release Notes
---

# TiDB 4.0.7 Release Notes

Release date: September 29, 2020

TiDB version: 4.0.7

## New Features

+ PD

    - Add `GetAllMembers` function to get pd member info in PD client [#2980](https://github.com/pingcap/pd/pull/2980)

+ TiDB Dashboard

    - Support to generate metrics relationship graph [#760](https://github.com/pingcap-incubator/tidb-dashboard/pull/760)

## Improvements

+ TiDB

    - Add more runtime information for join executor [#20093](https://github.com/pingcap/tidb/pull/20093)
    - Add coprocessor cache hit ratio in explain analyze [#19972](https://github.com/pingcap/tidb/pull/19972)
    - Support push ROUND function to TiFlash [#19967](https://github.com/pingcap/tidb/pull/19967)
    - Add default value of CMSketch for Analyze [#19927](https://github.com/pingcap/tidb/pull/19927)

+ TiKV

    - Support JSON log format [#8382](https://github.com/tikv/tikv/pull/8382)

+ PD

    - Make counter inc when operator finished rather than operator added [#2983](https://github.com/pingcap/pd/pull/2983)
    - Set the `make-up-replica` operator to high priority [#2977](https://github.com/pingcap/pd/pull/2977)

+ TiFlash

    - Improve error handling of Region meta change happened during read in progress

+ Tools

    + TiCDC

        - Support to translate to more execution efficient SQLs in MySQL sink when the old value feature is enabled. [#955](https://github.com/pingcap/ticdc/pull/955)

    + Backup & Restore (BR)

        - Add retry when backup connection was broken [#508](https://github.com/pingcap/br/pull/508)

    + TiDB Lightning

        - TiDB Lightning's log level can be dynamically updated via HTTP [#393](https://github.com/pingcap/tidb-lightning/pull/393)

## Bug Fixes

+ TiDB

    - Solve vectorization bug from and/or/COALESCE due to shortcut [#20092](https://github.com/pingcap/tidb/pull/20092)
    - Fix issue of plan digest is same when cop task store is different [#20076](https://github.com/pingcap/tidb/pull/20076)
    - Fix wrong behavior for `!= any()` [#20062](https://github.com/pingcap/tidb/pull/20062)
    - Fix issue query slow_query error when slow-log file not exist [#20051](https://github.com/pingcap/tidb/pull/20051)
    - Fix unexpected retry region request when context cancel [#20031](https://github.com/pingcap/tidb/pull/20031)
    - Fix issue querying cluster_slow_query time type in streaming request bug [#19943](https://github.com/pingcap/tidb/pull/19943)
    - Fix a bug that DML using caseWhen may cause schema change [#20095](https://github.com/pingcap/tidb/pull/20095)
    - Fix log desensitization bug in prestmt [#20048](https://github.com/pingcap/tidb/pull/20048)
    - Fix panic tidb-server doesn't release table lock [#20020](https://github.com/pingcap/tidb/pull/20020)
    - Fix incorrect error message of inserting enum & set [#19950](https://github.com/pingcap/tidb/pull/19950)
    - Fix the behavior of rewrite ScalarFunction IsTure [#19903](https://github.com/pingcap/tidb/pull/19903)
    - Fix CLUSTER_INFO system table may not work after PD is scaled-in or out [#20026](https://github.com/pingcap/tidb/pull/20026)
    - Avoid unnecessary warnings/errors when folding constants in control expr [#19910](https://github.com/pingcap/tidb/pull/19910)

+ TiKV

    - Fix status service shutdown when TLS handshake failed [#8649](https://github.com/tikv/tikv/pull/8649)
    - Fix potential undefined behaviors [#7782](https://github.com/tikv/tikv/pull/7782)
    - Fix possible panic of generating snap when doing UnsafeDestroyRange [#8681](https://github.com/tikv/tikv/pull/8681)

+ PD

    - Fix the bug that pd might panic If some regions have no leader when `balance-region` enabled [#2994](https://github.com/pingcap/pd/pull/2994)
    - Fix the statistical deviation of region size and region keys after region merge [#2985](https://github.com/pingcap/pd/pull/2985)

+ TiFlash

    - Fix wrong result of right outer join

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that caused the TiDB config changed after restoring [#509](https://github.com/pingcap/br/pull/509)

    + Dumpling

        - Fix the problem that dumpling fails to parse metadata when some variables are `NULL` [#150](https://github.com/pingcap/dumpling/pull/150)

## Others

+ TiDB

    - Update stats per table to avoid OOM [#20013](https://github.com/pingcap/tidb/pull/20013)
    - Refine error message desensitization [#20004](https://github.com/pingcap/tidb/pull/20004)
    - Accept connections from clients using connectors from MySQL 8.0 [#19959](https://github.com/pingcap/tidb/pull/19959)

+ PD

    - Update the dependency of errors [#3003](https://github.com/pingcap/pd/pull/3003)
    - Fix error hot statistic metrics [#2991](https://github.com/pingcap/pd/pull/2991)
    - Improvement:  make counter inc when operator finished rather than operator add [#2983](https://github.com/pingcap/pd/pull/2983)
    - Add GetMemberInfo() function to get pd member info [#2980](https://github.com/pingcap/pd/pull/2980)
    - Set the `make-up-replica` operator to high priority [#2977](https://github.com/pingcap/pd/pull/2977)
    - Fix miss err in `redirectSchedulerDelete` [#2974](https://github.com/pingcap/pd/pull/2974)

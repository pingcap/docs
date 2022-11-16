---
title: TiDB 5.3.4 Release Note
---

# TiDB 5.3.4 Release Note

Release date: xx, xx, 2022

TiDB version: 5.3.4

## Compatibility changes

## Improvements

+ TiDB

    <!--sql-infra owner: @Defined2014-->

    <!--executor owner: @zanmato1984-->

    <!--transaction owner: @cfzjywxk-->

    <!--planner owner: @qw4990-->

+ TiKV

    <!--owner: @v01dstar-->

    - (dup) Reload TLS certificate automatically for each update to improve availability [#12546](https://github.com/tikv/tikv/issues/12546)

+ PD

    <!--owner: @nolouch-->

+ TiFlash

    <!--compute owner: @zanmato1984-->

    <!--storage owner: @flowbehappy-->

+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Lightning

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->

## Bug fixes

+ TiDB

    <!--sql-infra owner: @Defined2014-->

    - (dup) Fix the issue that the Region cache is not cleaned up in time when the Region is merged[#37141](https://github.com/pingcap/tidb/issues/37141)
    - (dup) Fix the issue that TiDB writes wrong data due to the wrong encoding of the ENUM or SET column [#32302](https://github.com/pingcap/tidb/issues/32302)
    - (dup) Fix the issue that database-level privileges are incorrectly cleaned up [#38363](https://github.com/pingcap/tidb/issues/38363)
    - (dup) Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [#38293](https://github.com/pingcap/tidb/issues/38293)
    - (dup) Fix the issue that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - change date_add and date_sub string_(int/string/real/decimal) function return type to string [#36394](https://github.com/pingcap/tidb/issues/36394)
    - fix(parser): restore table option INSERT_METHOD should use WriteKeyWord [#38368](https://github.com/pingcap/tidb/issues/38368)
    - fix authentication with MySQL 5.1 and older clients [#29725](https://github.com/pingcap/tidb/issues/29725)

    <!--executor owner: @zanmato1984-->

    - (dup) Fix wrong results of `GREATEST` and `LEAST` when passing in unsigned `BIGINT` arguments [#30101](https://github.com/pingcap/tidb/issues/30101)
    - (dup) Fix the issue that the result of `concat(ifnull(time(3))` in TiDB is different from that in MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)
    - avoid sum from avg overflow [#29952](https://github.com/pingcap/tidb/issues/29952)
    - add an unit test case for unreasonable invoking Close [#30587](https://github.com/pingcap/tidb/issues/27125)
    - HashJoinExec checks the buildError even if the probeSide is empty [#30289](https://github.com/pingcap/tidb/issues/30289)
    - expression: resize the result for IfXXSig [#37414](https://github.com/pingcap/tidb/issues/37414)
    - change date_add and date_sub string_(int/string/real/decimal) function return type to string. [#27573](https://github.com/pingcap/tidb/issues/27573)
    - fix hashjoin goleak [#39026](https://github.com/pingcap/tidb/issues/39026)
    - fix: the results of tikv and tiflash are different [#37258](https://github.com/pingcap/tidb/issues/37258)

    <!--transaction owner: @cfzjywxk-->

    <!--planner owner: @qw4990-->

    - (dup) Fix the issue that the EXECUTE might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)
    - (dup) Fix the issue that `GROUP CONCAT` with `ORDER BY` might fail when the `ORDER BY` clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216)
    - Fix the issue that set wrong length and width for Decimal and Real when using plan-cache [#29565](https://github.com/pingcap/tidb/issues/29565)
    - add an unit test case for unreasonable invoking Close [#27125](https://github.com/pingcap/tidb/issues/27125)

+ TiKV

    <!--owner: @v01dstar-->

+ PD

    <!--owner: @nolouch-->

    - (dup) Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) Fix inaccurate Stream timeout and accelerate leader switchover [#5207](https://github.com/tikv/pd/issues/5207)

+ TiFlash

    <!--compute owner: @zanmato1984-->

    - fix: the results of tikv and tiflash are different [#5849](https://github.com/pingcap/tiflash/issues/5849)
    - fix inconsistent result before deleting some rows [#6127](https://github.com/pingcap/tiflash/issues/6127)

    <!--storage owner: @flowbehappy-->

    - Fix an invalid default value cause bootstrap failed [#3157](https://github.com/pingcap/tiflash/issues/3157)
+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

      - use white list for retryable error [#6698](https://github.com/pingcap/tiflow/issues/6698)

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Lightning

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->

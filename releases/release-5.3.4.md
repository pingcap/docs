---
title: TiDB 5.3.4 Release Note
---

# TiDB 5.3.4 Release Note

Release date: xx, xx, 2022

TiDB version: 5.3.4

## Improvements

+ TiKV

    <!--owner: @v01dstar-->

    - (dup) Reload TLS certificate automatically for each update to improve availability [#12546](https://github.com/tikv/tikv/issues/12546)

## Bug fixes

+ TiDB

    <!--sql-infra owner: @Defined2014-->

    - (dup) Fix the issue that the Region cache is not cleaned up in time when the Region is merged[#37141](https://github.com/pingcap/tidb/issues/37141)
    - (dup) Fix the issue that TiDB writes wrong data due to the wrong encoding of the ENUM or SET column [#32302](https://github.com/pingcap/tidb/issues/32302)
    - (dup) Fix the issue that database-level privileges are incorrectly cleaned up [#38363](https://github.com/pingcap/tidb/issues/38363)
    - (dup) Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [#38293](https://github.com/pingcap/tidb/issues/38293)
    - (dup) Fix the issue that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - Fix return type to string for `adddate` and `subdate` functions [#36394](https://github.com/pingcap/tidb/issues/36394)
    - Fix restore table option `INSERT_METHOD` incompatible with MySQL [#38368](https://github.com/pingcap/tidb/issues/38368)
    - Fix authentication with MySQL 5.1 and older clients [#29725](https://github.com/pingcap/tidb/issues/29725)

    <!--executor owner: @zanmato1984-->

    - (dup) Fix wrong results of `GREATEST` and `LEAST` when passing in unsigned `BIGINT` arguments [#30101](https://github.com/pingcap/tidb/issues/30101)
    - (dup) Fix the issue that the result of `concat(ifnull(time(3))` in TiDB is different from that in MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix the issue that avg() returns error `ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.` when querying from TiFlash [#29952](https://github.com/pingcap/tidb/issues/29952)
    - Fix the issue that sql returns `ERROR 1105 (HY000): close of nil channel` when using HashJoinExec [#30289](https://github.com/pingcap/tidb/issues/30289)
    - Fix the different return type of date_add and date_sub between TiDB and MySQL. Change date_add and date_sub string_(int/string/real/decimal) function return type to string [#27573](https://github.com/pingcap/tidb/issues/27573)
    - Fix the problem that tikv and tiflash return different results when query logical operations [#37258](https://github.com/pingcap/tidb/issues/37258)

    <!--transaction owner: @cfzjywxk-->

    - (dup) Fix the issue explain analyze with DML executors may respond to the client before the transaction commit has finished [#37373](https://github.com/pingcap/tidb/issues/37373)
    - Fix the issue that the region cache after merging many regions is not cleared properly [#37174](https://github.com/pingcap/tidb/issues/37174)

    <!--planner owner: @qw4990-->

    - (dup) Fix the issue that the EXECUTE might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)
    - (dup) Fix the issue that `GROUP CONCAT` with `ORDER BY` might fail when the `ORDER BY` clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216)
    - Fix the issue that wrong length and width are set for Decimal and Real when using plan-cache [#29565](https://github.com/pingcap/tidb/issues/29565)

+ PD

    <!--owner: @nolouch-->

    - (dup) Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) Fix the issue that the TiFlash learner replica might not be created in specific scenarios [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) Fix inaccurate Stream timeout and accelerate leader switchover [#5207](https://github.com/tikv/pd/issues/5207)

+ TiFlash

    <!--compute owner: @zanmato1984-->

    - Fix the issue that logical operators return wrong results when the argument type is UInt8  [#6127](https://github.com/pingcap/tiflash/issues/6127)

    <!--storage owner: @flowbehappy-->

    - Fix the issue that TiFlash crash due to using `0.0` as the integer's default value. E.g. `i` int(11) NOT NULL DEFAULT '0.0' [#3157](https://github.com/pingcap/tiflash/issues/3157)

+ Tools

    + Dumpling

    <!--owner: @niubell-->

        - Fix the issue that dumpling can't dump with `--compress` option and s3 output directory [#30534](https://github.com/pingcap/tidb/issues/30534)

    + TiCDC

    <!--owner: @nongfushanquan-->

        - Fix a issue that causes MySQL related error not reported to owner in time [#6698](https://github.com/pingcap/tiflow/issues/6698)

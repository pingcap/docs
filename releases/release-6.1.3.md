---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 Release Notes

Release date: xx, xx, 2022

TiDB version: 6.1.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.3#version-list)

## Improvements

- PD

    <!--owner: nolouch -->

    - Optimize the lock granularity and improve the processing ability of heartbeat under high concurrency [#5586](https://github.com/tikv/pd/issues/5586) @[rleungx](https://github.com/rleungx)

- Tools

    - TiCDC

    <!--owner: @nongfushanquan-->

        - Enable transaction split and disable safeMode of a changefeed in TiCDC by defult [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)
        - Improve kakfa protocol encoder performance [#7540](https://github.com/pingcap/tiflow/issues/7540), [#7532](https://github.com/pingcap/tiflow/issues/7532), [#7543](https://github.com/pingcap/tiflow/issues/7543) @[sdojjy](https://github.com/sdojjy) @[3AceShowHand](https://github.com/3AceShowHand)

## Bug fixes

+ TiDB

    <!--sql-infra and tidb owner: bb7133-->

    - (dup) Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup) Fix the issue of the wrong query result that occurs when the mistakenly pushed-down conditions are discarded by Join Reorder [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)
    - Fix the issue that `get_lock()` cannot hold for more than 10 minutes [#38706](https://github.com/pingcap/tidb/issues/38706) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the auto-increment column cannot be used with check constraint [#38894](https://github.com/pingcap/tidb/issues/38894) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the gPRC log is output to a wrong file [#38941](https://github.com/pingcap/tidb/issues/38941) @[xhebox](https://github.com/xhebox)
    - Fix the issue that TiFlash sync status is nor removed from etcd when a table is truncated or dropped [#37168](https://github.com/pingcap/tidb/issues/37168) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that data files can be accessed unrestrainedly via data source name injection (CVE-2022-3023) [#38541](https://github.com/pingcap/tidb/issues/38541) @[lance6716](https://github.com/lance6716)

    <!--executor owner: zanmato1984-->

    - Fix the issue that function `str_to_date` returns wrong result under the `NO_ZERO_DATE` SQL Mode [#39146](https://github.com/pingcap/tidb/issues/39146) @[mengxin9014](https://github.com/mengxin9014)

    <!--planner owner: qw4990-->

    - Fix the issue that statistics collecting tasks in the background might panic [#35421](https://github.com/pingcap/tidb/issues/35421) @[lilinghai](https://github.com/lilinghai)

    <!--transaction owner: cfzjywxk-->

    - (dup) Fix the issue that in some scenarios the pessimistic lock is incorrectly added to the non-unique secondary index [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

- PD

    <!--owner: nolouch -->

    - (dup) Fix inaccurate Stream timeout and accelerate leader switchover [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiKV

    <!--owner: tonyxuqqi-->

    - (dup) Fix abnormal Region competition caused by expired lease during snapshot acquisition [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ TiFlash

    <!--compute owner: zanmato1984 -->

    - (dup) Fix the issue that logical operators return wrong results when the argument type is UInt8 [#6127](https://github.com/pingcap/tiflash/issues/6127)
    - (dup) Fix the issue that wrong data input for `CAST(value AS DATETIME)` causing high TiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)

    <!--storage owner: flowbehappy -->

    - Fix the issue that heavy write pressure could generate too many column files in delta layer. [#6361](https://github.com/pingcap/tiflash/issues/6361) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that column files in delta layer cannot be compacted after restart tiflash [#6159](https://github.com/pingcap/tiflash/issues/6159) @[lidezhu](https://github.com/lidezhu)

+ Tools

    + Backup & Restore (BR)

    <!--owner: @3pointer-->

        - Fix the issue that fail to restore when use old collation framework in databases or tables [#39150](https://github.com/pingcap/tidb/issues/39150) @[MoCuishle28](https://github.com/MoCuishle28)

    + Dumpling

    <!--owner: @niubell-->

    + TiCDC

    <!--owner: @nongfushanquan-->

        - Fix an issue that causes data lost when pause and resume changefeed while executing DDL. [#7682](https://github.com/pingcap/tiflow/issues/7682) @[asddongmen](https://github.com/asddongmen)

    + TiDB Binlog

    <!--owner: @niubell-->

    + TiDB Data Migration (DM)

    <!--owner: @niubell-->

        - (dup) Fix the issue that when `collation_compatible` is set to `"strict"`, DM might generate SQL with duplicated collations [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - Fix sometime DM task is stopped with error "Unknown placement policy" [#7493](https://github.com/pingcap/tiflow/issues/7493) @[lance6716](https://github.com/lance6716)
        - Fix in some cases relay log file may re-pull from upstream [#7719](https://github.com/pingcap/tiflow/pull/7719) @[liumengya94](https://github.com/liumengya94)
        - Fix when DM worker exits a new worker may be scheduled too quickly and write duplicated data [#7745](https://github.com/pingcap/tiflow/pull/7745) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

    <!--owner: @niubell-->

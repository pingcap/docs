---
title: TiDB 6.1.1 Release Notes
category: Releases
---



# TiDB 6.1.1 Release Notes

Release Date: August 23, 2022

TiDB version: 6.1.1

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#37295](https://github.com/pingcap/tidb/pull/37295)
    - ```release-note [#37280](https://github.com/pingcap/tidb/pull/37280)
    - ```release-note [#37268](https://github.com/pingcap/tidb/pull/37268)
    - ```release-note [#37231](https://github.com/pingcap/tidb/pull/37231)
    - ```release-note [#37093](https://github.com/pingcap/tidb/pull/37093)
    - ```release-note [#36931](https://github.com/pingcap/tidb/pull/36931)
    - ```release-note [#36881](https://github.com/pingcap/tidb/pull/36881)
    - ```release-note [#36874](https://github.com/pingcap/tidb/pull/36874)
    - ```release-note [#36810](https://github.com/pingcap/tidb/pull/36810)
    - ```release-note [#36723](https://github.com/pingcap/tidb/pull/36723)
    - ```release-note [#36719](https://github.com/pingcap/tidb/pull/36719)
    - ```release-note [#36710](https://github.com/pingcap/tidb/pull/36710)
    - ```release-note [#36629](https://github.com/pingcap/tidb/pull/36629)
    - ```release-note [#36620](https://github.com/pingcap/tidb/pull/36620)
    - ```release-note [#36595](https://github.com/pingcap/tidb/pull/36595)
    - ```release-note [#36528](https://github.com/pingcap/tidb/pull/36528)
    - ```release-note [#36447](https://github.com/pingcap/tidb/pull/36447)
    - ```release-note [#36418](https://github.com/pingcap/tidb/pull/36418)
    - ```release-note [#36408](https://github.com/pingcap/tidb/pull/36408)
    - ```release-note [#36144](https://github.com/pingcap/tidb/pull/36144)
    - ```release-note [#36140](https://github.com/pingcap/tidb/pull/36140)
    - ```release-note [#36135](https://github.com/pingcap/tidb/pull/36135)
    - ```release-note [#36134](https://github.com/pingcap/tidb/pull/36134)
    - ```release-note [#36133](https://github.com/pingcap/tidb/pull/36133)
    - ```release-note [#36132](https://github.com/pingcap/tidb/pull/36132)
    - ```release-note [#36129](https://github.com/pingcap/tidb/pull/36129)
    - ```release-note [#36126](https://github.com/pingcap/tidb/pull/36126)
    - ```release-note [#36120](https://github.com/pingcap/tidb/pull/36120)
    - ```release-note [#36119](https://github.com/pingcap/tidb/pull/36119)
    - ```release-note [#36104](https://github.com/pingcap/tidb/pull/36104)
    - ```release-note [#36096](https://github.com/pingcap/tidb/pull/36096)
    - ```release-note [#35932](https://github.com/pingcap/tidb/pull/35932)
    - ```release-note [#35774](https://github.com/pingcap/tidb/pull/35774)
    - ```release-note [#35772](https://github.com/pingcap/tidb/pull/35772)
    - ```release-note [#35761](https://github.com/pingcap/tidb/pull/35761)
    - ```release-note [#35724](https://github.com/pingcap/tidb/pull/35724)
    - ```release-note [#35697](https://github.com/pingcap/tidb/pull/35697)
    - ```release-note [#35655](https://github.com/pingcap/tidb/pull/35655)
    - ```release-note [#35520](https://github.com/pingcap/tidb/pull/35520)
    - ```release-note [#35495](https://github.com/pingcap/tidb/pull/35495)
    - ```release-note [#35472](https://github.com/pingcap/tidb/pull/35472)
    - ```release-note [#35467](https://github.com/pingcap/tidb/pull/35467)
    - ```release-note [#35466](https://github.com/pingcap/tidb/pull/35466)
    - ```release-note [#35387](https://github.com/pingcap/tidb/pull/35387)
    - ```release-note [#35189](https://github.com/pingcap/tidb/pull/35189)
    - Fixed an issue where extra datums may break binlog. [#35168](https://github.com/pingcap/tidb/pull/35168)
    - ```release-note [#35060](https://github.com/pingcap/tidb/pull/35060)


+ TiKV/TiKV

    - remove call_option to avoid  deadlock(RWR). [#13267](https://github.com/tikv/tikv/pull/13267)
    - None. [#13260](https://github.com/tikv/tikv/pull/13260)
    - Fix potential deadlock in `RpcClient` when two read locks are interleaved by a write lock. [#13225](https://github.com/tikv/tikv/pull/13225)
    - Fix a bug that regions may be overlapped if raftstore is too busy [#13176](https://github.com/tikv/tikv/pull/13176)
    - Make max_subcompactions dynamically changeable [#13146](https://github.com/tikv/tikv/pull/13146)
    - fix the bug that the consume should be refresh if region heartbeat send failed. [#13136](https://github.com/tikv/tikv/pull/13136)
    - Fix possible QPS drop due to high commit log duration [#13089](https://github.com/tikv/tikv/pull/13089)
    - In the new backup organization structure, we will see:

./br backup --pd "127.0.0.1:2379" -s "s3://backup/20220621" 
  - After br command finished, we will have the structure below.
➜  backup tree .
.
└── 20220621
    ├── backupmeta
    ├── store1
    │   └── backup-xxx.sst
    ├── store100
    │   └── backup-yyy.sst
    ├── store2
    │   └── backup-zzz.sst
    ├── store3
    ├── store4
    └── store5 [#13066](https://github.com/tikv/tikv/pull/13066)
    - Fix encryption keys not cleaned up when Raft Engine is enabled [#13003](https://github.com/tikv/tikv/pull/13003)
    - Please add a release note.

Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note.

If you don't think this PR needs a release note then fill it with None.
If this PR will be picked to release branch, then a release note is probably required. [#12912](https://github.com/tikv/tikv/pull/12912)
    - support log backup function to achieve point-in-time recovery. [#12894](https://github.com/tikv/tikv/pull/12894)
    - Fix possible panic when source peer catch up logs by snapshot in merge [#12875](https://github.com/tikv/tikv/pull/12875)
    - Fix potential panic when a peer is being split and destroyed at the same time [#12865](https://github.com/tikv/tikv/pull/12865)
    - Fix bug which causes frequent pd client reconnection [#12835](https://github.com/tikv/tikv/pull/12835)
    - Fix tikv crash when conv empty string [#12695](https://github.com/tikv/tikv/pull/12695)
    - Support encode metrics response with gzip to reduce the http body size [#12647](https://github.com/tikv/tikv/pull/12647)
    - Fix serialized format of ReadableSize [#12637](https://github.com/tikv/tikv/pull/12637)


+ PingCAP/TiFlash

    - fix the problem that there may be some obsolete data left in storage which cannot be deleted [#5677](https://github.com/pingcap/tiflash/pull/5677)
    - Fix a panic issue in parallel aggregation when an exception is thrown. [#5439](https://github.com/pingcap/tiflash/pull/5439)
    - Reduce unnecessary CPU usage in some edge cases [#5424](https://github.com/pingcap/tiflash/pull/5424)
    - Fix a bug that TiFlash can not work in a cluster using ipv6 [#5395](https://github.com/pingcap/tiflash/pull/5395)
    - Fix the issue that format throw data truncated error [#5339](https://github.com/pingcap/tiflash/pull/5339)


+ PD

    - None. [#5425](https://github.com/tikv/pd/pull/5425)
    - grpc: fix the wrong error handler [#5378](https://github.com/tikv/pd/pull/5378)
    - grpc: fix the wrong error handler [#5376](https://github.com/tikv/pd/pull/5376)
    - None. [#5350](https://github.com/tikv/pd/pull/5350)
    - Fix the issue that the online process is not accurate when having invalid label settings. [#5344](https://github.com/tikv/pd/pull/5344)
    - None. [#5320](https://github.com/tikv/pd/pull/5320)
    - None. [#5145](https://github.com/tikv/pd/pull/5145)
    - Fix the issue that `/regions/replicated` may return the wrong status [#5115](https://github.com/tikv/pd/pull/5115)


+ Tools

    + PingCAP/TiCDC

        - Fix a bug that may cause cdc server panic if it received a http request before cdc server fully started. [#6844](https://github.com/pingcap/tiflow/pull/6844)
        - Fix a bug that relay goroutine and upstream connections may leak when relay meet error [#6812](https://github.com/pingcap/tiflow/pull/6812)
        - Log DML start ts when MySQL sink meets error. [#6789](https://github.com/pingcap/tiflow/pull/6789)
        - `None`. [#6759](https://github.com/pingcap/tiflow/pull/6759)
        - `None`. [#6750](https://github.com/pingcap/tiflow/pull/6750)
        - `None`. [#6723](https://github.com/pingcap/tiflow/pull/6723)
        - `None`. [#6716](https://github.com/pingcap/tiflow/pull/6716)
        - `None` [#6662](https://github.com/pingcap/tiflow/pull/6662)
        - `None`. [#6657](https://github.com/pingcap/tiflow/pull/6657)
        - ```release-note [#6634](https://github.com/pingcap/tiflow/pull/6634)
        - `None`. [#6586](https://github.com/pingcap/tiflow/pull/6586)
        - `None`. [#6545](https://github.com/pingcap/tiflow/pull/6545)
        - `None`. [#6532](https://github.com/pingcap/tiflow/pull/6532)
        - `None`. [#6523](https://github.com/pingcap/tiflow/pull/6523)
        - `None`. [#6505](https://github.com/pingcap/tiflow/pull/6505)
        - `None`. [#6482](https://github.com/pingcap/tiflow/pull/6482)
        - Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note.

If you don't think this PR needs a release note then fill it with `None`. [#6431](https://github.com/pingcap/tiflow/pull/6431)
        - `None`. [#6428](https://github.com/pingcap/tiflow/pull/6428)
        - Fix TiCDC panic issue when disable the old value of changefeed [#6416](https://github.com/pingcap/tiflow/pull/6416)
        - `None`. [#6414](https://github.com/pingcap/tiflow/pull/6414)
        - Fix ddl sink panic when changefeed syncpoint is enable. [#6395](https://github.com/pingcap/tiflow/pull/6395)
        - `None`. [#6386](https://github.com/pingcap/tiflow/pull/6386)
        - `None`. [#6373](https://github.com/pingcap/tiflow/pull/6373)
        - `None`. [#6354](https://github.com/pingcap/tiflow/pull/6354)
        - use `net.JoinHostPort` to generate host-port part of URI to support ipv6 address. [#6342](https://github.com/pingcap/tiflow/pull/6342)
        - Fix a bug that start DM-worker and `kill` it immediately will not let process stop. [#6292](https://github.com/pingcap/tiflow/pull/6292)
        - Fix a data race in black hole sink. [#6229](https://github.com/pingcap/tiflow/pull/6229)
        - `None`. [#6199](https://github.com/pingcap/tiflow/pull/6199)
        - Fix the problem that TiCDC cannot correctly recognize the ipv6 address in SinkURI [#6150](https://github.com/pingcap/tiflow/pull/6150)
        - `None`. [#6140](https://github.com/pingcap/tiflow/pull/6140)
        - `None`. [#6090](https://github.com/pingcap/tiflow/pull/6090)
        - Fix the wrong maximum compatible version number [#6040](https://github.com/pingcap/tiflow/pull/6040)
        - Fix the issue of the possible data race that might occur when multiple functions are executing concurrently, some calling Result() and writing into some variables that other functions are trying to read. #4811 [#5961](https://github.com/pingcap/tiflow/pull/5961)
        - `fix a bug that get tables without using quote schema name`. [#5938](https://github.com/pingcap/tiflow/pull/5938)
        - Fix a bug that causes get changefeeds api does not well after cdc server restart. [#5875](https://github.com/pingcap/tiflow/pull/5875)
        - `None`. [#5872](https://github.com/pingcap/tiflow/pull/5872)
        - `None`. [#5839](https://github.com/pingcap/tiflow/pull/5839)
        - `None`. [#5810](https://github.com/pingcap/tiflow/pull/5810)
        - `None`. [#5653](https://github.com/pingcap/tiflow/pull/5653)


## Improvements

+ PingCAP/TiDB

    - ```release-note [#37283](https://github.com/pingcap/tidb/pull/37283)


## Bug Fixes

+ PingCAP/TiDB

    - ```release-note [#36938](https://github.com/pingcap/tidb/pull/36938)
    - ```release-note [#36785](https://github.com/pingcap/tidb/pull/36785)
    - ```release-note [#36391](https://github.com/pingcap/tidb/pull/36391)


+ PingCAP/TiFlash

    - Fix the TiFlash crash issue that occurs after dropping a column of a table with clustered indexes under some situations. [#5193](https://github.com/pingcap/tiflash/pull/5193)



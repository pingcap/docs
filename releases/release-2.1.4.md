---
title: TiDB 2.1.4 Release Notes
aliases: ['/docs/dev/releases/release-2.1.4/','/docs/dev/releases/2.1.4/']
---

# TiDB 2.1.4 Release Notes

On February 15, 2019, TiDB 2.1.4 is released. The corresponding TiDB Ansible 2.1.4 is also released. Compared with TiDB 2.1.3, this release has greatly improved the stability, the SQL optimizer, statistics, and the execution engine.

## TiDB

+ SQL Optimizer/Executor
    - Fix the issue that the `VALUES` function does not handle the FLOAT type correctly [#9223](https://github.com/pingcap/tidb/pull/9223)
    - Fix the wrong result issue when casting Float to String in some cases [#9227](https://github.com/pingcap/tidb/pull/9227)
    - Fix the wrong result issue of the `FORMAT` function in some cases [#9235](https://github.com/pingcap/tidb/pull/9235)
    - Fix the panic issue when handling the Join query in some cases [#9264](https://github.com/pingcap/tidb/pull/9264)
    - Fix the issue that the `VALUES` function does not handle the ENUM type correctly [#9280](https://github.com/pingcap/tidb/pull/9280)
    - Fix the wrong result issue of `DATE_ADD`/`DATE_SUB` in some cases [#9284](https://github.com/pingcap/tidb/pull/9284)
+ Server
    - Optimize the “reload privilege success” log and change it to the DEBUG level [#9274](https://github.com/pingcap/tidb/pull/9274)
+ DDL
    - Change `tidb_ddl_reorg_worker_cnt` and `tidb_ddl_reorg_batch_size` to global variables [#9134](https://github.com/pingcap/tidb/pull/9134)
    - Fix the bug caused by adding an index to a generated column in some abnormal conditions [#9289](https://github.com/pingcap/tidb/pull/9289)

## TiKV

- Fix the duplicate write issue when closing TiKV [#4146](https://github.com/tikv/tikv/pull/4146)
- Fix the abnormal result issue of the event listener in some cases [#4132](https://github.com/tikv/tikv/pull/4132)

## Tools

+ Lightning
    - Optimize the memory usage [#107](https://github.com/pingcap/tidb-lightning/pull/107), [#108](https://github.com/pingcap/tidb-lightning/pull/108)
    - Remove the chunk separation of dump files to avoid an extra parsing of dump files [#109](https://github.com/pingcap/tidb-lightning/pull/109)
    - Limit the I/O concurrency of reading dump files, to avoid performance degradation caused by too many cache misses [#110](https://github.com/pingcap/tidb-lightning/pull/110)
    - Support importing data in batches for a single table, to improve import stability [#110](https://github.com/pingcap/tidb-lightning/pull/113)
    - Enable auto compactions in the import mode in TiKV [#4199](https://github.com/tikv/tikv/pull/4199)
    - Support disabling the TiKV periodic Level-1 compaction parameter, because the Level-1 compaction is automatically executed in the import mode when the TiKV cluster version is 2.1.4 or later [#119](https://github.com/pingcap/tidb-lightning/pull/119)
    - Limit the number of import engines to avoid consuming too much importer disk space [#119](https://github.com/pingcap/tidb-lightning/pull/119)
+ Support splitting chunks using the TiDB statistics in sync-diff-inspector [#197](https://github.com/pingcap/tidb-tools/pull/197)
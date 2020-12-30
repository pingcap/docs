---
title: TiDB 5.0 RC Release Notes
---

# TiDB 5.0 RC Release Notes

Release date: December 31, 2020

TiDB version: 5.0.0-rc

## New Features

+ TiDB

    - Support collation `utf8mb4_unicode_ci` and `utf8_unicode_ci`
        - [project](https://github.com/pingcap/tidb/issues/17596)
        - [document](https://docs.pingcap.com/tidb/dev/character-set-and-collation#new-framework-for-collations)
    - Support error/info log desensitization
        - [project](https://github.com/pingcap/tidb/issues/18566)
        - [document](https://github.com/pingcap/tidb/blob/master/errno/logredaction.md)
    - Support Invisible Indexes
        - [project](https://github.com/pingcap/tidb/issues/9246)
        - [document](https://github.com/pingcap/tidb/pull/15366)
    - Support Async commit. Async Commit is an optimization that reduces commit latency, by returning success to the user when all prewrites have succeeded. (Experimental)
        - [project](https://github.com/tikv/tikv/projects/34)
        - [document](https://github.com/pingcap/docs-cn/pull/5181)
    - Support clustered Index. Clustered indexes provide TiDB the ability to organize tables in a way that can improve the performance of certain queries. (Experimental)
        - [project](https://github.com/pingcap/tidb/projects/45)
        - [document](https://docs.pingcap.com/tidb/dev/clustered-indexes)
    - Support `LIST PARTITION` and `LIST COLUMNS PARTITION` table (Experimental)
        - [project](https://github.com/pingcap/tidb/issues/20678)
        - [document](https://docs.pingcap.com/zh/tidb/dev/partitioned-table#list-%E5%88%86%E5%8C%BA) // TODO: use english doc.
    - Improve the Accuracy and Robustness of Index Selection (Experimental)
        - [#21817](https://github.com/pingcap/tidb/pull/21817)
        - [document](https://github.com/pingcap/docs-cn/pull/5164)

+ TiKV

    - Support dynamically changing auto-tuned mode of RocksDB rate limiter

+ TiFlash

    - Support limiting the memory usage of DeltaIndex
    - Support limiting the IO write throughput of background data management tasks, to lower the impact of foreground tasks

## Improvements

+ TiDB

    - Improve the executor runtime information collection
        - [issue](https://github.com/pingcap/tidb/issues/18663)
        - [document](https://docs.pingcap.com/zh/tidb/stable/sql-statement-explain-analyze#explain-analyze)
    - Optimize the Performance of Bulk Deletion
        - [issue](https://github.com/pingcap/tidb/issues/18028)

+ TiKV

    - Enable compaction guard by default, to split rocksdb SST files at TiKV region boundaries, to reduce overall compaction I/O

+ TiFlash

    - Add a thread pool that queues coprocessor tasks, to ease the memory pressure caused by large concurrent coprocessor handling

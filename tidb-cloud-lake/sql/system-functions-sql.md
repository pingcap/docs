---
title: 系统函数
summary: 本页提供 {{{ .lake }}} 中与系统相关的函数参考信息。这些函数可帮助你分析和监控 {{{ .lake }}} 部署的内部存储和性能相关方面。
---

# 系统函数

本页提供 {{{ .lake }}} 中与系统相关的函数参考信息。这些函数可帮助你分析和监控 {{{ .lake }}} 部署的内部存储和性能相关方面。

## 表元信息函数 {#table-metadata-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [CLUSTERING_INFORMATION](/tidb-cloud-lake/sql/clustering-information.md) | 返回表的聚簇信息 | `CLUSTERING_INFORMATION('default', 'mytable')` |

## 存储层函数 {#storage-layer-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) | 返回表的快照信息 | `FUSE_SNAPSHOT('default', 'mytable')` |
| [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md) | 返回表的 segment 信息 | `FUSE_SEGMENT('default', 'mytable')` |
| [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md) | 返回表的 block 信息 | `FUSE_BLOCK('default', 'mytable')` |
| [FUSE_COLUMN](/tidb-cloud-lake/sql/fuse-column.md) | 返回表的列信息 | `FUSE_COLUMN('default', 'mytable')` |

## 存储优化函数 {#storage-optimization-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [FUSE_STATISTIC](/tidb-cloud-lake/sql/fuse-statistic.md) | 返回表的统计信息 | `FUSE_STATISTIC('default', 'mytable')` |
| [FUSE_ENCODING](/tidb-cloud-lake/sql/fuse-encoding.md) | 返回表的编码信息 | `FUSE_ENCODING('default', 'mytable')` |
| [FUSE_VIRTUAL_COLUMN](/tidb-cloud-lake/sql/fuse-virtual-column.md) | 返回虚拟列信息 | `FUSE_VIRTUAL_COLUMN('default', 'mytable')` |
| [FUSE_TIME_TRAVEL_SIZE](/tidb-cloud-lake/sql/fuse-time-travel-size.md) | 返回时间旅行存储信息 | `FUSE_TIME_TRAVEL_SIZE('default', 'mytable')` |
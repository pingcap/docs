---
title: Cluster Key
summary: 本页按功能组织，全面概述了 {{{ .lake }}} 中的 cluster key 操作，便于参考。
---

# Cluster Key

本页按功能组织，全面概述了 {{{ .lake }}} 中的 cluster key 操作，便于参考。

## cluster key 管理 {#cluster-key-management}

| 命令 | 描述 |
|---------|-------------|
| [SET CLUSTER KEY](/tidb-cloud-lake/sql/set-cluster-key.md) | 为表创建或替换 cluster key |
| [ALTER CLUSTER KEY](/tidb-cloud-lake/sql/alter-cluster-key.md) | 修改现有的 cluster key |
| [DROP CLUSTER KEY](/tidb-cloud-lake/sql/drop-cluster-key.md) | 从表中移除 cluster key |
| [RECLUSTER TABLE](/tidb-cloud-lake/sql/recluster-table.md) | 基于 cluster key 重新组织表数据 |

## 相关主题 {#related-topics}

- [Cluster Key](/tidb-cloud-lake/guides/cluster-key-performance.md)

> **注意：**
>
> {{{ .lake }}} 中的 cluster key 用于在表中以物理方式组织数据，通过将相关数据放置在一起以提升查询性能。
---
title: TiDB 7.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.3.0.
---

# TiDB 7.3.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.3.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.3.0#version-list)

7.3.0 introduces the following major feature as generally available. The rest of the release (detailed in the Details section) was a series of enhancements to query stability in TiDB server and TiFlash. These are more miscellaneous in nature and not user-facing so they are not included in this section dedicated to release highlights:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/stable/partitioned-raft-kv#partitioned-raft-kv">Partitioned Raft KV GA</a></td>
    <td>Every key region will store its key-value data in its own isolated LSM tree (RocksDB).
This drastically improves write performance, reduces I/O amplication, speeds up scale-in/-out operations, and is a huge step toward TiDB handling beyond PB-scale workloads per cluster.
    </td>
  </tr>
</tbody>
</table>

## Feature details

### Performance

- note 1

- note 2

### Reliability

- note 1

- note 2

### SQL

- note 1

- note 2

### DB operations

- note 1

- note 2

### Observability

- note 1

- note 2

### Data migration

- note 1

- note 2

## Compatibility changes

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### Behavior changes

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
| TiDB Lightning | `send-kv-pairs` | 废弃 | 从 7.2 版本开始 TiDB Lightning 配置文件的参数 "send-kv-pairs" 不再生效，由新的参数 "send-kv-size" 代替。该新参数用于指定 KV 键值对的大小阈值，单位为 KiB 或 MiB，默认值为 "16 KiB"。当 KV 键值对的大小达到设定的阈值时，它们将立即发送到 TiKV，避免在导入大宽表等一些场景因为 Lightning 节点内存积累键值对过多导致 OOM 的问题。**tw@hfxsd** <!--1420--> |
| TiDB Lightning | `send-kv-size` | 新增 | 从 7.2 版本开始在 Lightning 配置文件 "[tikv-importer]" 这个 Session 中引入 `send-kv-size` 参数，用于设置发单次送到 TiKV 的 KV pairs 的大小。当 KV 键值对的大小达到设定的阈值时，它们将被 Lightning 立即发送到 TiKV，避免在导入大宽表的时候 Lightning 节点因为内存积累键值对过多导致 OOM 的问题。通过调整 "send-kv-size" 参数，你可以在内存使用和导入速度之间找到平衡，提高导入过程的稳定性和效率。**tw@hfxsd** <!--1420-->|
| Data Migration | `strict-optimistic-shard-mode` | 新增 | 用于兼容历史版本 2.0 分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断，在多个表的 DDL变更有依赖关系的场景，可以及时中断，用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|

## Deprecated features

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @xuyifangreeneyes
    - 支持分区表下推 TopN 算子，减少该情况下 indexLookUp 和 IndexMerge 算子回表次数，提升相关 SQL 执行性能 [#26166](https://github.com/pingcap/tidb/issues/26166) [#41028](https://github.com/pingcap/tidb/issues/41028)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Contributor GitHub ID](链接)
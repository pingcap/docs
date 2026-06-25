---
title: TiDB-X-CLOUD.202510.1 Release Notes
summary: Learn about the features for the TiDB-X-CLOUD.202510.1 kernel.
---

# TiDB-X-CLOUD.202510.1 Release Notes

Release date: April 28, 2026

TiDB X kernel version: `TiDB-X-CLOUD.202510.1`

{{{ .premium }}} is in public preview starting from April 28, 2026, using the `TiDB-X-CLOUD.202510.1` kernel.

In `TiDB-X-CLOUD.202510.1`:

- `202510` indicates that the baseline code branch of this kernel version was created in October 2025, which is different from the release date.
- `1` indicates that it is the first patch release built from the `TiDB-X-CLOUD.202510` baseline branch.

The `TiDB-X-CLOUD.202510.1` kernel is based on the TiDB v8.5.0 kernel, which means it supports most of the features and improvements of the [TiDB v8.5.0](/release-notes/release-8.5.0.md) kernel.

In addition, compared with the [TiDB v8.5.0](/release-notes/release-8.5.0.md) kernel, the `TiDB-X-CLOUD.202510.1` kernel introduces the following features:

## New TiDB X architecture

* Introduce the TiDB X architecture, which is a cloud-native shared-storage architecture that makes cloud-native object storage the backbone of TiDB.

    This architecture enables elastic scalability, predictable performance, and optimized total cost of ownership (TCO) for AI-era workloads.

    TiDB X represents a fundamental evolution from the shared-nothing architecture of [classic TiDB](/tidb-architecture.md) to a cloud-native shared-storage architecture. By transitioning from a shared-nothing to a shared-storage architecture, TiDB X addresses the physical limitations of coupled nodes to achieve the following technical objectives:

    - **Accelerated scaling**: Improving scaling performance by up to 10x by eliminating the need for physical data migration.
    - **Task isolation**: Ensuring zero interference between background maintenance tasks (such as compaction) and online transactional traffic.
    - **Resource elasticity**: Implementing a true "pay-as-you-go" model where compute resources scale independently of storage volume.

    For more information, see [TiDB X Architecture](/tidb-cloud/tidb-x-architecture.md).

## Performance features

* Support redistributing data of a specific table (experimental) [#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)

    PD automatically schedules data to be distributed as evenly as possible across all TiKV nodes in a cluster. However, this automatic scheduling focuses on the cluster as a whole. In some cases, even if the cluster-wide data distribution is balanced, the data of a specific table might still be unevenly distributed across TiKV nodes.

    Starting from v8.5.4, you can use the [`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidb/v8.5/sql-statement-show-table-distribution/) statement to check how the data of a specific table is distributed across all TiKV nodes. If the data distribution is unbalanced, you can use the [`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table) statement to redistribute the table's data (experimental) to improve load balancing.

    Note that redistributing the data of a specific table is a one-time task with a timeout limit. If the distribution task is not completed before the timeout, it will automatically exit.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table).

* Support `ANALYZE` embedded in DDL statements [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

    This feature applies to the following types of DDL statements:

    - DDL statements that create new indexes: [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
    - DDL statements that reorganize existing indexes: [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) and [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

    When you enable this feature, TiDB automatically runs an `ANALYZE` (statistics collection) operation before the new or reorganized index becomes visible to users. This prevents inaccurate optimizer estimates and potential plan changes caused by temporarily unavailable statistics after index creation or reorganization.

     For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/ddl_embedded_analyze).

## Observability features

* Add storage engine identifiers to statement summary tables and slow query logs [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw)

    When both TiKV and TiFlash are deployed in a cluster, users often need to filter SQL statements by storage engine during database diagnostics and performance optimization. For example, if TiFlash is under high load, users might need to identify SQL statements running on TiFlash to locate potential causes. To meet this need, starting from v8.5.5, TiDB adds storage engine identifier fields to statement summary tables and slow query logs.

    New fields in [statement summary tables](/statement-summary-tables.md):

    * `STORAGE_KV`: `1` indicates that the SQL statement accesses TiKV.
    * `STORAGE_MPP`: `1` indicates that the SQL statement accesses TiFlash.

    New fields in [slow query logs](/identify-slow-queries.md):

    * `Storage_from_kv`: `true` indicates that the SQL statement accesses TiKV.
    * `Storage_from_mpp`: `true` indicates that the SQL statement accesses TiFlash.

    This feature simplifies workflows in certain diagnostics and performance optimization scenarios and improves issue identification efficiency.

    For more information, see [Statement Summary Tables](/statement-summary-tables.md) and [Identify Slow Queries](/identify-slow-queries.md).

## Limitations

Because of the architectural differences between TiDB X and classic TiDB, the `TiDB-X-CLOUD.202510.1` kernel does not support the following storage features of the TiDB v8.5.0 kernel:

- [TiKV MVCC In-Memory Engine (IME)](/tikv-in-memory-engine.md)
- [Follower Read](/follower-read.md)

To learn more about the limitations, see [Limited SQL features on TiDB Cloud](/tidb-cloud/limited-sql-features.md).
---
title: TiDB-X-CLOUD.202510.1 Release Notes
summary: Learn about the features for the TiDB-X-CLOUD.202510.1 kernel.
---

# TiDB-X-CLOUD.202510.1 Release Notes

**Release date**: April 28, 2026

**Applicable TiDB Cloud plan**: {{{ .premium }}}

**TiDB X kernel version**: `TiDB-X-CLOUD.202510.1`

{{{ .premium }}} is available in public preview starting April 28, 2026, using the `TiDB-X-CLOUD.202510.1` kernel.

In `TiDB-X-CLOUD.202510.1`:

- `202510` indicates that the baseline code branch of this kernel version was created in October 2025, which is different from the release date.
- `1` indicates that it is the first patch release built from the `TiDB-X-CLOUD.202510` baseline branch.

The `TiDB-X-CLOUD.202510.1` kernel is based on the [TiDB v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) kernel and includes most of the features and improvements introduced in TiDB v8.5.0.

In addition, compared with the [TiDB v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) kernel, the `TiDB-X-CLOUD.202510.1` kernel introduces the following features:

## New TiDB X architecture

* Introduce the TiDB X architecture, which is a cloud-native shared-storage architecture that makes cloud-native object storage the backbone of TiDB.

    This architecture enables elastic scalability, predictable performance, and optimized total cost of ownership (TCO) for AI-era workloads.

    TiDB X represents a fundamental evolution from the shared-nothing architecture of [classic TiDB](https://docs.pingcap.com/tidbcloud/tidb-architecture/?plan=premium) to a cloud-native shared-storage architecture. By transitioning from a shared-nothing to a shared-storage architecture, TiDB X addresses the physical limitations of coupled nodes to achieve the following technical objectives:

    - **Accelerated scaling**: Improving scaling performance by up to 10x by eliminating the need for physical data migration.
    - **Task isolation**: Ensuring zero interference between background maintenance tasks (such as compaction) and online transactional traffic.
    - **Resource elasticity**: Implementing a true "pay-as-you-go" model where compute resources scale independently of storage volume.

    For more information, see [TiDB X Architecture](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/?plan=premium).

## Performance features

* Support redistributing data of a specific table (experimental) [#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)

    PD automatically schedules data to be distributed as evenly as possible across all TiKV nodes in a cluster. However, this automatic scheduling focuses on the cluster as a whole. In some cases, even if the cluster-wide data distribution is balanced, the data of a specific table might still be unevenly distributed across TiKV nodes.

   Now you can use the [`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidbcloud/sql-statement-show-table-distribution/?plan=premium) statement to check how the data of a specific table is distributed across all TiKV nodes. If the data distribution is unbalanced, you can use the [`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidbcloud/sql-statement-distribute-table/?plan=premium) statement to redistribute the table's data (experimental) to improve load balancing.

    Note that redistributing the data of a specific table is a one-time task with a timeout limit. If the distribution task is not completed before the timeout, it will automatically exit.

    For more information, see [documentation](https://docs.pingcap.com/tidbcloud/sql-statement-distribute-table/?plan=premium).

* Support `ANALYZE` embedded in DDL statements [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

    This feature applies to the following types of DDL statements:

    - DDL statements that create new indexes: [`ADD INDEX`](https://docs.pingcap.com/tidbcloud/sql-statement-add-index/?plan=premium)
    - DDL statements that reorganize existing indexes: [`MODIFY COLUMN`](https://docs.pingcap.com/tidbcloud/sql-statement-modify-column/?plan=premium) and [`CHANGE COLUMN`](https://docs.pingcap.com/tidbcloud/sql-statement-change-column/?plan=premium)

    When you enable this feature, TiDB automatically runs an `ANALYZE` (statistics collection) operation before the new or reorganized index becomes visible to users. This prevents inaccurate optimizer estimates and potential plan changes caused by temporarily unavailable statistics after index creation or reorganization.

     For more information, see [documentation](https://docs.pingcap.com/tidbcloud/ddl_embedded_analyze/?plan=premium).

## Limitations

Because of the architectural differences between TiDB X and classic TiDB, the TiDB X kernel does not support the following storage features of the classic TiDB kernel:

- [TiKV MVCC In-Memory Engine (IME)](https://docs.pingcap.com/tidb/v8.5/tikv-in-memory-engine)
- [Follower Read](https://docs.pingcap.com/tidb/v8.5/follower-read)

To learn more about the limitations, see [Limited SQL features on TiDB X Instances](https://docs.pingcap.com/tidbcloud/limited-sql-features-tidb-x/?plan=premium).
---
title: Table-Level Data Affinity
summary: Learn how to configure affinity constraints for tables or partitions to control Region replica distribution and how to view the scheduling status.
---

# Table-Level Data Affinity <span class="version-mark">New in v8.5.5</span>

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. It might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

Table-level data affinity is a PD mechanism for scheduling data distribution at the table level. This mechanism controls how Leader and Voter replicas for Regions of the same table or partition are distributed across a TiKV cluster.

When you enable PD affinity scheduling and set the `AFFINITY` option of a table to `table` or `partition`, PD groups Regions belonging to the same table or partition into the same affinity group. During scheduling, PD prioritizes placing the Leader and Voter replicas of these Regions on the same subset of a few TiKV nodes. This reduces network latency caused by cross-node access during queries, thereby improving query performance.

## Limitations

Before using table-level data affinity, note the following limitations:

- This feature does not take effect in [PD Microservices Mode](/pd-microservices.md).
- This feature does not work with [Temporary tables](/temporary-tables.md) and [views](/views.md).
- After data affinity is configured for a [partitioned table](/partitioned-table.md), **modifying the table partitioning scheme is not supported**, including adding, dropping, reorganizing, or swapping partitions. To change the partitioning scheme, you must first remove the affinity configuration for that table.
- **Evaluate disk capacity in advance for large data volumes**: after affinity is enabled, PD prioritizes scheduling Regions of a table or partition to the same subset of a few TiKV nodes. For tables or partitions with large data volumes, this might significantly increase disk usage on these nodes. It is recommended to evaluate disk capacity and monitor it in advance.
- Data affinity affects only the distribution of Leader and Voter replicas. If a table has Learner replicas (such as TiFlash), their distribution is not affected by affinity settings.

## Prerequisites

PD affinity scheduling is disabled by default. Before setting affinity for tables or partitions, you must enable and configure this feature.

1. Set the PD configuration item [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-new-in-v855) to a value greater than `0` to enable affinity scheduling.

    For example, the following command sets the value to `4`, allowing PD to run up to four affinity scheduling tasks concurrently:

    ```bash
    pd-ctl config set schedule.affinity-schedule-limit 4
    ```

2. (Optional) Modify the PD configuration item [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-new-in-v855) as needed. The default value is `256` MiB. It controls the size threshold for automatically merging adjacent small Regions within the same affinity group. Setting it to `0` disables the automatic merging of adjacent small Regions within affinity groups.

## Usage

This section describes how to configure affinity for tables or partitions and how to view affinity scheduling status.

### Configure table or partition affinity

You can configure table or partition affinity using the `AFFINITY` option in `CREATE TABLE` or `ALTER TABLE` statements.

| Affinity level | Scope | Effect |
|---|---|---|
| `AFFINITY='table'` | Non-partitioned table | Enables affinity for the table. PD creates a single affinity group for all Regions of the table. |
| `AFFINITY='partition'` | Partitioned table | Enables affinity for each partition in the table. PD creates a separate affinity group for the Regions of each partition. For example, for a table with four partitions, PD creates four independent affinity groups. |
| `AFFINITY=''` or `AFFINITY='none'` | Tables configured with `AFFINITY='table'` or `AFFINITY='partition'` | Disables affinity for the table or partitions. When you disable affinity, PD deletes the corresponding affinity group for the target table or partition, so Regions of that table or partition are no longer subject to affinity scheduling constraints. Automatic Region splitting in TiKV reverts to the default behavior within a maximum of 10 minutes. |

**Examples**

Enable affinity when creating a non-partitioned table:

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
```

Enable affinity for each partition when creating a partitioned table:

```sql
CREATE TABLE tp1 (a INT)
  AFFINITY = 'partition'
  PARTITION BY HASH(a) PARTITIONS 4;
```

Enable affinity for an existing non-partitioned table:

```sql
CREATE TABLE t2 (a INT);
ALTER TABLE t2 AFFINITY = 'table';
```

Disable table affinity:

```sql
ALTER TABLE t1 AFFINITY = '';
```

### View affinity information

You can view table or partition affinity information in the following ways:

- Execute the [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md) statement. In the `Status` column, you can view tables or partitions with affinity enabled and their scheduling status. The meanings of the values in the `Status` column are as follows:

    - `Pending`: PD has not started affinity scheduling for the table or partition, such as when Leaders or Voters are not yet determined.
    - `Preparing`: PD is scheduling Regions to meet affinity requirements.
    - `Stable`: all Regions have reached the target distribution.

- Query the [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md) table and check the `TIDB_AFFINITY` column for the affinity level of a table.
- Query the [`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md) table and check the `TIDB_AFFINITY` column for the affinity level of a partition.

## Notes

- **Automatic splitting of Regions**: when a Region belongs to an affinity group and affinity is in effect, automatic splitting of that Region is disabled by default to avoid the creation of too many Regions that could weaken the affinity effect. Automatic splitting is triggered only when the Region size exceeds four times the value of [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-new-in-v855). Note that splits triggered by components other than TiKV or PD (such as manual splits triggered by [`SPLIT TABLE`](/sql-statements/sql-statement-split-region.md)) are not subject to this restriction.

- **Degradation and expiration mechanism**: if the TiKV nodes hosting the target Leaders or Voters in an affinity group become unavailable (for example, due to node failure or insufficient disk space), if a Leader is evicted, or if there is a conflict with existing placement rules, PD marks the affinity group as degraded. During degradation, affinity scheduling for the corresponding table or partition is paused.

    - If the affected nodes recover within 10 minutes, PD resumes scheduling based on the original affinity settings.
    - If the affected nodes do not recover within 10 minutes, the affinity group is marked as expired. At this point, PD restores normal scheduling behavior (the status in [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md) returns to `Pending`), and automatically updates Leaders and Voters in the affinity group to re-enable affinity scheduling.

## Related statements and configurations

- `AFFINITY` option in [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) and [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)
- [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md)
- PD configuration items: [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-new-in-v855) and [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-new-in-v855)
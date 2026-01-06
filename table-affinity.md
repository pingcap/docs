```markdown
title: Table-Level Data Affinity
summary: Control Region replica distribution and view scheduling status by configuring affinity constraints for tables or partitions.
---

# Table-Level Data Affinity <span class="version-mark">Introduced in v8.5.5 and v9.0.0</span>

> **WARNING:**
>
> This feature is experimental and not recommended for production environments. It may change or be removed without prior notice. If you find any bugs, please report them by opening an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

Table-level data affinity is a data distribution scheduling mechanism at the table level within PD, used to control the distribution of Region Leader and Voter replicas for the same table or partition across the TiKV cluster.

When PD data affinity scheduling is enabled and the `AFFINITY` option for a table is set to `table` or `partition`, PD groups Regions of the same table or partition into the same affinity group. During scheduling, PD prioritizes placing the Leader and Voter replicas of these Regions on the same minority of TiKV nodes. This reduces network latency caused by cross-node access during queries, thereby improving query performance.

## Usage Limitations

Before using table-level data affinity, please note the following limitations:

- This feature is not effective in [PD Microservices Mode](/pd-microservices.md).
- [Temporary tables](/temporary-tables.md) and [views](/views.md) do not support configuring data affinity.
- After configuring data affinity for a [partitioned table](/partitioned-table.md), **modifying the table's partitioning scheme is not supported**, including adding, deleting, reorganizing, or swapping partitions. To adjust partitioning configurations, you must first remove the affinity settings for that table.
- **Evaluate disk capacity in advance for large data volumes**: After enabling data affinity, PD prioritizes scheduling Regions for a table or partition to the same minority of TiKV nodes. For tables or partitions with large data volumes, this may significantly increase the disk usage on these nodes. It is recommended to evaluate disk capacity and monitor it in advance.
- Data affinity scheduling only affects the distribution of Leader and Voter replicas. If a table has Learner replicas (e.g., TiFlash), the distribution of Learner replicas is not affected by the affinity configuration.

## Prerequisites

The PD affinity scheduling feature is disabled by default. Before setting the affinity for tables or partitions, you must enable and configure this feature.

1. Set the PD configuration item [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-从-v855-和-v900-版本开始引入) to a value greater than `0` to enable PD's affinity scheduling.

    For example, execute the following command to set this configuration item to `4`, which means PD can execute up to 4 affinity scheduling tasks concurrently:

    ```bash
    pd-ctl config set schedule.affinity-schedule-limit 4
    ```

2. (Optional) Set the PD configuration item [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-从-v855-和-v900-版本开始引入) as needed (default value is `256` MiB). This controls the threshold for automatically merging adjacent small Regions within the same affinity group. Setting it to `0` disables the automatic merging of adjacent small Regions within affinity groups.

## Usage

This section describes how to configure affinity for tables or partitions and how to view affinity scheduling status.

### Configuring Table or Partition Affinity

You can configure table or partition affinity using the `AFFINITY` option in `CREATE TABLE` or `ALTER TABLE` statements.

| Affinity Level | Scope | Effect |
|---|---|---|
| `AFFINITY='table'` | Non-partitioned table | Enables affinity for the table. PD creates one affinity group for all Regions of this table. |
| `AFFINITY='partition'` | Partitioned table | Enables affinity for each partition of the table. PD creates separate affinity groups for Regions corresponding to **each partition** of the table. For example, if a table has 4 partitions, PD will create 4 independent affinity groups for this table. |
| `AFFINITY=''` or `AFFINITY='none'` | Tables with `AFFINITY='table'` or `AFFINITY='partition'` set | Disables affinity for the table or partitions. After setting this, PD deletes the corresponding affinity group for the table or partition. Regions of the table or partition will no longer be subject to affinity scheduling constraints. Automatic Region splitting in TiKV will revert to the default state within a maximum of 10 minutes. |

**Examples**:

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

### Viewing Affinity

You can view table or partition affinity information in the following ways:

- Execute the [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md) statement. In the `Status` column, you can view tables or partitions with affinity enabled and their scheduling status. The meanings of the values in the `Status` column are as follows:

    - `Pending`: PD has not yet performed affinity scheduling for this table or partition, for example, when Leaders or Voters are not yet determined.
    - `Preparing`: PD is scheduling Regions to meet affinity requirements.
    - `Stable`: All Regions have reached the target distribution.

- Query the `TIDB_AFFINITY` column of the [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md) table to view the affinity level of tables.
- Query the `TIDB_AFFINITY` column of the [`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md) table to view the affinity level of partitions.

## Notes

- **Automatic Region Splitting**: When a Region belongs to an affinity group and affinity is effective, the Region will not split automatically by default to avoid the creation of too many Regions that might affect the affinity effect. Automatic splitting is triggered only when the Region size exceeds four times the value of [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-从-v855-和-v900-版本开始引入). It is important to note that Region splits triggered manually (e.g., by executing [`SPLIT TABLE`](/sql-statements/sql-statement-split-region.md)) or automatically by non-TiKV or PD components are not subject to this restriction.

- **Degradation and Expiration Mechanism**: If the TiKV nodes hosting the target Leader or Voters in an affinity group are in an unavailable state (e.g., node downtime or insufficient disk space), if the Leader is evicted, or if there is a conflict with existing placement rules, PD will mark the affinity group as degraded. During degradation, affinity scheduling for the corresponding table or partition will be paused.

    - If the affected nodes recover within 10 minutes, PD will continue scheduling according to the original affinity settings.
    - If recovery does not occur within 10 minutes, the affinity group will be marked as expired. At this point, PD will first restore normal scheduling behavior (the status in [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md) will return to `Pending`), and then automatically update the Leaders and Voters within the affinity group to re-enable affinity scheduling.

## Related Statements and Configurations

- `AFFINITY` option in [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) or [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)
- [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md)
- PD Configuration Items: [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-从-v855-和-v900-版本开始引入) and [`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-从-v855-和-v900-版本开始引入)
```
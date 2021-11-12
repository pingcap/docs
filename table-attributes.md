---
title: Table Attributes
summary: Introduce how to use TiDB `ATTRIBUTES`.
---

# Table Attributes

Table attributes feature is introduced in TiDB v5.3.0. Using this feature, you can add specific attributes to a table or partition to perform the operations corresponding to the attributes. For example, you can use table attributes to control the Region merge behavior.

> **Note:**
>
> - Currently, TiDB only supports adding the `merge_option` attribute to a table or partition to control the Region merge behavior.
> - When you use TiDB Binlog or TiCDC to perform replication or use BR to perform incremental backup, the replication or backup operations skip the DDL statement that sets table attributes. To use table attributes in the downstream or in the backup cluster, you need to manually execute the DDL statement in the downstream or in the backup cluster.

## Usage

The table attribute is in the form of `key=value`. Multiple attributes are separated by commas. In the following examples, `t` is the name of the table to be modified, `p` is the name of the partition to be modified. Items in `[]` are optional.

+ Set attributes for a table or partition:

    ```sql
    alter table t [partition p ]attributes[=]'key=value[, key1=value1...]';
    ```

+ Reset attributes for a table or partition:

    ```sql
    alter table t [partition p ]attributes[=]default;
    ```

+ See the attributes of all tables and partitions:

    ```sql
    select * from information_schema.attributes;
    ```

+ See the attribute configured to a table or partition:

    ```sql
    select * from information_schema.attributes where id='schema/t[/p]';
    ```

+ See all tables and partitions that have a specific attribute:

    ```sql
    select * from information_schema.attributes where attributes like '%key%';
    ```

## Attribute override rules

The attribute configured to a table takes effect on all partitions of the table. However, there is one exception: If the table and partition are configured with the same attribute but different attribute values, the partition attribute overrides the table attribute. For example, suppose that the table `t` is configured with the `key=value` attribute, and the partition `p` is configured with `key=value1`.

```sql
alter table t attributes[=]'key=value';
alter table t partition p attributes[=]'key=value1';
```

In this case, `key=value1` is the attribute that actually takes effect on the `p1` partition.

## Region merging control through the table attribute

### User scenarios

If there is a write hotspot or read hotspot, you can use table attributes to control the Region merge behavior. You can first add the `merge_option` attribute to a table or partition and then set its value to `deny`. The two scenarios are as follows.

#### Write hotspot on a newly created table or partition

If a hotspot problem occurs when writing data to a newly created table or partition, it is necessary to avoid the problem by splitting and scattering regions. However, if there is a certain time interval between the split and scatter operation and writes, it is impossible to truly avoid the write hotspot. This is because the split operation regarding the new table or partition produces empty regions, so if the time interval occurs, the regions might be merged. In this case, you can solve this merging issue by adding the `merge_option` attribute to the table or partition and setting its value to `deny`.

#### Periodic read hotspot in read-only scenarios

Suppose that in a read-only scenario, you try to reduce the periodic read hotspot that occurs on a table or partition by manually splitting Regions, and you do not want the manually split Regions to be merged after the hotspot issue is resolved. In this case, you can add the `merge_option` attribute to the table or partition and set its value to `deny`.

### Usage

+ Prevent the Regions of a table from merging:

    ```sql
    alter table t attributes[=]'merge_option=deny';
    ```

+ Allow merging Regions belonging to a table:

    ```sql
    alter table t attributes[=]'merge_option=allow';
    ```

+ Reset attributes of a table:

    ```sql
    alter table t attributes[=]default；
    ```

+ Block to merge Regions belonging to a partition:

    ```sql
    alter table t partition p attributes[=]'merge_option=deny';
    ```

+ Allow merging Regions belonging to a partition:

    ```sql
    alter table t partition p attributes[=]'merge_option=allow';
    ```

+ See all tables or partitions configured the `merge_option` attribution:

    ```sql
    select * from information_schema.attributes where attributes like '%merge_option%';
    ```

### Attribute override rules

```sql
alter table t attributes[=]'merge_option=deny';
alter table t partition p attributes[=]'merge_option=allow';
```

When the above two attributes are configured at the same time, the Regions belonging to the partition `p` can actually be merged. When the attribute of the partition is reset, the partition `p` inherits the attribute from the table `t`, and the Regions cannot be merged.

> **Note:**
>
> - If only the attribute of a table exists at present, even though the `merge_option=allow` attribute is configured, a partition still split multiple regions according to the actual number of partitions by default. To merge all regions, you need to [reset attributes of the table](#usage).
> - When using the `merge_option` attribute, you need to pay attention to the PD configuration parameter [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval). Suppose that the `merge_option` attribute is not configured. In this case, if Regions meet conditions, Regions can be merged after the interval specified by `split-merge-interval`. If the `merge_option` attribute is configured, TiKV decides whether to merge Regions after the specified interval according to the `merge_option` configuration.
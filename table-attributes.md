---
title: Table Attribute
summary: Introduce how to use TiDB `ATTRIBUTES`.
---

# Table Attribute

Table attribute is a new feature introduced from TiDB 5.3.0 version. This feature is used to add specific attributes to a table or partition to perform the operations corresponding to the attributes. For example, you can take control of merging regions by using the table attribute.

> **Note:**
>
> - Currently, TiDB only supports adding the `merge_option` attribute to a table or partition to take control of merging regions.
> - When performing data replication through TiDB Binlog or TiCDC or incremental backup through BR, the replication and backup skip the DDL statement that sets the table attribute. To use the table attribute in the downstream or backup cluster, you need to manually run the DDL statement in the downstream or backup cluster.

## Usage

The table attribute is in `key=value` form. If there are multiple attributes, you need to use commas to separate them. The examples are as follows, where `t` is the name of the table to be modified, `p` is the name of the partition to be modified. For the items in `[]`, it is optional to fill them in.

+ Set attributes of a table or partition:

    ```sql
    alter table t [partition p ]attributes[=]'key=value[, key1=value1...]';
    ```

+ Reset attributes of a table or partition:

    ```sql
    alter table t [partition p ]attributes[=]default;
    ```

+ See all attributes of tables and partitions:

    ```sql
    select * from information_schema.attributes;
    ```

+ See the attributes configured to a table or partition:

    ```sql
    select * from information_schema.attributes where id='schema/t[/p]';
    ```

+ See all tables and partitions that have specific attributes:

    ```sql
    select * from information_schema.attributes where attributes like '%key%';
    ```

## Attribute override rules

The attribute configured for a table takes effect on all partitions of the table. However, there is one exception: If the table and partition are configured with the same attribute but different attribute values, the partition attribute overrides the table attribute. For example, suppose that the table `t` is configured with the `key=value` attribute, and the partition `p` is configured with `key=value1`.

```sql
alter table t attributes[=]'key=value';
alter table t partition p attributes[=]'key=value1';
```

In this case, the attribute taking actual effect on the partition `p` is `key=value1`.

## Region merging control through the table attribute

### Usage scenario

If there is write hotspot or read hotspot, you can use the table attribute to take control of merging regions by adding the `merge_option` attribute to a table or partition and setting its value to `deny`. The followings are two usage scenarios.

#### Write hotspot on a newly created table or partition

If a hotspot problem occurs when writing data to a newly created table or partition, it is necessary to avoid the problem by splitting and scattering regions. However, if there is a certain time interval between the split and scatter operation and writes, it is impossible to truly avoid the write hotspot. This is because the split operation regarding the new table or partition produces empty regions, so if the time interval occurs, the regions might be merged. In this case, you can solve this merging issue by adding the `merge_option` attribute to the table or partition and setting its value to `deny`.

#### Periodic read hotspot in a read-only scenario

Suppose that you reduce the periodic read hotspot that occurred to a table or partition by manually splitting regions in a read-only scenario, and you do not want the manually splitted regions to be merged after the hotspot problem is solved. In this case, you can add the `merge_option` attribute to the table or partition and set its value to `deny`.

### Usage

+ Block to merge regions belonging to a table:

    ```sql
    alter table t attributes[=]'merge_option=deny';
    ```

+ Allow merging regions belonging to a table:

    ```sql
    alter table t attributes[=]'merge_option=allow';
    ```

+ Reset attributes of a table:

    ```sql
    alter table t attributes[=]default；
    ```

+ Block to merge regions belonging to a partition:

    ```sql
    alter table t partition p attributes[=]'merge_option=deny';
    ```

+ Allow merging regions belonging to a partition:

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

When the above two attributes are configured at the same time, the regions belonging to the actual partition `p` can be merged. When the attribute of a partition is reset, the partition `p` inherits the attribute from the table `t`, and the regions cannot be merged.

> **Note:**
>
> - If only the attribute of a table exists at present, even though the `merge_option=allow` attribute is configured, a partition still split multiple regions according to the actual number of partitions by default. To merge all regions, you need to [reset attributes of the table](#usage).
> - When using the `merge_option` attribute, you need to pay attention to the PD configuration parameter [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval). Suppose that the `merge_option` attribute is not configured. In this case, if regions meet conditions, regions can be merged after the time specified by `split-merge-interval`. If the `merge_option` attribute is configured, its configuration decides whether to merge regions after the specified time.
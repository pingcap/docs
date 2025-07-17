---
title: Table Attributes
summary: 了解如何使用 TiDB 的 table attribute 功能。
---

# Table Attributes

Table Attributes 功能在 TiDB v5.3.0 版本中引入。使用该功能，你可以为表或分区添加特定属性，以执行对应属性的操作。例如，你可以使用 table attributes 来控制 Region 合并行为。

<CustomContent platform="tidb">

目前，TiDB 仅支持向表或分区添加 `merge_option` 属性，以控制 Region 合并行为。`merge_option` 属性只是处理热点问题的一部分。更多信息，请参考 [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

目前，TiDB 仅支持向表或分区添加 `merge_option` 属性，以控制 Region 合并行为。`merge_option` 属性只是处理热点问题的一部分。

</CustomContent>

> **Note:**
>
> 当你使用 TiCDC 进行复制或使用 BR 进行增量备份时，复制或备份操作会跳过设置表属性的 DDL 语句。若要在下游或备份集群中使用表属性，你需要手动在下游或备份集群中执行相应的 DDL 语句。

## 使用方法

表属性的格式为 `key=value`。多个属性之间用逗号分隔。在以下示例中，`t` 表示要修改的表名，`p` 表示要修改的分区名。`[]` 中的内容为可选项。

+ 为表或分区设置属性：

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] 'key=value[, key1=value1...]';
    ```

+ 重置表或分区的属性：

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] DEFAULT;
    ```

+ 查看所有表和分区的属性：

    ```sql
    SELECT * FROM information_schema.attributes;
    ```

+ 查看某个表或分区配置的属性：

    ```sql
    SELECT * FROM information_schema.attributes WHERE id='schema/t[/p]';
    ```

+ 查看所有具有特定属性的表和分区：

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%key%';
    ```

## 属性覆盖规则

配置在表上的属性对该表的所有分区生效，但有一个例外：如果表和分区配置了相同的属性但属性值不同，则分区的属性会覆盖表的属性。例如，假设表 `t` 配置了 `key=value` 属性，而分区 `p` 配置了 `key=value1`。

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

在这种情况下，`key=value1` 才是实际在 `p` 分区上生效的属性。

## 使用表属性控制 Region 合并行为

### 用户场景

如果存在写入热点或读取热点，可以使用表属性控制 Region 合并行为。你可以先为表或分区添加 `merge_option` 属性，然后将其值设置为 `deny`。具体场景如下。

#### 新创建的表或分区出现写入热点

当在新创建的表或分区写入数据时出现热点问题，通常需要进行 Region 拆分和分散操作。然而，如果拆分/分散操作与写入操作之间存在一定时间间隔，这些操作实际上并不能真正避免写入热点。因为在创建表或分区时执行的拆分会产生空的 Region，如果时间间隔存在，拆分的 Region 可能会被合并。为应对这种情况，你可以为表或分区添加 `merge_option` 属性，并将其值设置为 `deny`。

#### 只读场景下的周期性读取热点

假设在只读场景中，你试图通过手动拆分 Region 来减少周期性读取热点，并且不希望在热点问题解决后手动拆分的 Region 被合并。在这种情况下，可以为表或分区添加 `merge_option` 属性，并将其值设置为 `deny`。

### 使用方法

+ 阻止表的 Region 合并：

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=deny';
    ```

+ 允许合并属于某个表的 Region：

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=allow';
    ```

+ 重置表的属性：

    ```sql
    ALTER TABLE t ATTRIBUTES DEFAULT;
    ```

+ 阻止分区的 Region 合并：

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

+ 允许分区的 Region 合并：

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
    ```

+ 查看配置了 `merge_option` 属性的所有表或分区：

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%merge_option%';
    ```

### 属性覆盖规则

```sql
ALTER TABLE t ATTRIBUTES 'merge_option=deny';
ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
```

当同时配置上述两个属性时，属于分区 `p` 的 Region 实际上可以被合并。当分区的属性被重置后，分区 `p` 会继承表 `t` 的属性，此时 Region 不会被合并。

<CustomContent platform="tidb">

> **Note:**
>
> - 对于有分区的表，如果只在表级别配置了 `merge_option` 属性，即使设置为 `merge_option=allow`，表仍会根据实际分区数被拆分成多个 Region。若要合并所有 Region，需要 [重置表的属性](#usage)。
> - 使用 `merge_option` 属性时，需要注意 PD 配置参数 [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)。假设未配置 `merge_option` 属性，在满足条件的情况下，Region 会在 `split-merge-interval` 指定的时间间隔后被合并。如果配置了 `merge_option` 属性，PD 会根据 `merge_option` 配置决定是否在指定时间后合并 Region。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - 对于有分区的表，如果只在表级别配置了 `merge_option` 属性，即使设置为 `merge_option=allow`，表仍会根据实际分区数被拆分成多个 Region。若要合并所有 Region，需要 [重置表的属性](#usage)。
> - 假设未配置 `merge_option` 属性，在满足条件的情况下，Region 会在一小时后被合并。如果配置了 `merge_option` 属性，PD 会根据 `merge_option` 配置决定是否在一小时后合并 Region。

</CustomContent>
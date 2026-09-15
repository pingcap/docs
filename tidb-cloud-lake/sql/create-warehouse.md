---
title: CREATE WAREHOUSE
summary: 为计算资源创建一个新的计算集群。
---

# CREATE WAREHOUSE

为计算资源创建一个新的计算集群。

## 语法 {#syntax}

```sql
CREATE WAREHOUSE [ IF NOT EXISTS ] <warehouse_name>
    [ WITH ] warehouse_size = <size>
    [ WITH ] auto_suspend = <nullable_unsigned_number>
    [ WITH ] initially_suspended = <bool>
    [ WITH ] auto_resume = <bool>
    [ WITH ] max_cluster_count = <nullable_unsigned_number>
    [ WITH ] min_cluster_count = <nullable_unsigned_number>
    [ WITH ] comment = '<string_literal>'
    [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] )
```

| 参数            | 描述                                                                                  |
| --------------- | ------------------------------------------------------------------------------------- |
| `IF NOT EXISTS` | 可选。如果指定了该选项，当计算集群已存在时，命令会成功返回且不做任何更改。            |
| warehouse_name  | 3–63 个字符，只能包含 `A-Z`、`a-z`、`0-9` 和 `-`。                                     |

## 选项 {#options}

| 选项                  | 类型 / 值                                                                               | 默认值        | 描述                                                                                                                                          |
| --------------------- | --------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `WAREHOUSE_SIZE`      | `XSmall`, `Small`, `Medium`, `Large`, `XLarge`, `2XLarge`–`6XLarge`（不区分大小写）    | `Small`       | 控制计算规模。                                                                                                                                 |
| `AUTO_SUSPEND`        | `NULL`、`0` 或 ≥300 秒                                                                  | `600` 秒      | 自动挂起前的空闲超时时间。`0`/`NULL` 表示永不挂起；小于 300 的值会被拒绝。                                                                     |
| `INITIALLY_SUSPENDED` | 布尔值                                                                                  | `FALSE`       | 如果为 `TRUE`，则计算集群在创建后会保持挂起状态，直到被显式恢复。                                                                              |
| `AUTO_RESUME`         | 布尔值                                                                                  | `TRUE`        | 控制传入查询是否会自动唤醒计算集群。                                                                                                            |
| `MAX_CLUSTER_COUNT`   | `NULL` 或非负整数                                                                       | `0`           | 自动扩展集群数的上限。`0` 表示禁用自动扩展。                                                                                                    |
| `MIN_CLUSTER_COUNT`   | `NULL` 或非负整数                                                                       | `0`           | 自动扩展集群数的下限；应当 ≤ `MAX_CLUSTER_COUNT`。                                                                                               |
| `COMMENT`             | 字符串                                                                                  | 空            | 由 `SHOW WAREHOUSES` 展示的自由文本。                                                                                                           |
| `TAG`                 | 键值对：`TAG ( key1 = 'value1', key2 = 'value2' )`                                      | 无            | 用于分类和组织的资源标签（类似 AWS tags）。可用于成本分摊、环境标识或团队归属。                                                                  |

- 选项可以按任意顺序出现，也可以重复出现（以后面的值为准）。
- `AUTO_SUSPEND`、`MAX_CLUSTER_COUNT` 和 `MIN_CLUSTER_COUNT` 接受 `= NULL`，以将其重置为 `0`。

## 示例 {#examples}

以下示例创建了一个启用自动扩展并带有自定义设置的 XLarge 计算集群 (Warehouse)：

```sql
CREATE WAREHOUSE IF NOT EXISTS 'etl-wh'
    WITH warehouse_size = XLarge
    auto_suspend = 600
    initially_suspended = TRUE
    auto_resume = FALSE
    max_cluster_count = 4
    min_cluster_count = 2
    comment = 'Nightly ETL warehouse'
    TAG (environment = 'production', team = 'data-engineering', cost_center = 'analytics');
```

以下示例创建了一个基础的 Small 计算集群：

```sql
CREATE WAREHOUSE 'my-warehouse'
    WITH warehouse_size = Small;
```
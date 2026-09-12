---
title: ALTER WAREHOUSE
summary: 暂停、恢复或修改现有计算集群的设置。
---

# ALTER WAREHOUSE

暂停、恢复或修改现有计算集群 (Warehouse) 的设置。

## 语法 {#syntax}

```sql
-- Suspend or resume a warehouse
ALTER WAREHOUSE <warehouse_name> { SUSPEND | RESUME }

-- Modify warehouse settings
ALTER WAREHOUSE <warehouse_name>
    SET [ warehouse_size = <size> ]
    [ auto_suspend = <nullable_unsigned_number> ]
    [ auto_resume = <bool> ]
    [ max_cluster_count = <nullable_unsigned_number> ]
    [ min_cluster_count = <nullable_unsigned_number> ]
    [ comment = '<string_literal>' ]

ALTER WAREHOUSE <warehouse_name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WAREHOUSE <warehouse_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WAREHOUSE <warehouse_name> RENAME TO <new_name>
```

| 参数 | 描述 |
| --------- | ---------------------------------------------------------------------------- |
| `SUSPEND` | 立即暂停该计算集群。 |
| `RESUME`  | 立即恢复该计算集群。 |
| `SET`     | 修改一个或多个计算集群选项。未指定的字段保持不变。 |

## 选项 {#options}

`SET` 子句接受与 [CREATE WAREHOUSE](/tidb-cloud-lake/sql/create-warehouse.md) 相同的选项：

| 选项              | 类型 / 值                                                       | 描述                                                          |
| ------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `WAREHOUSE_SIZE`    | `XSmall`, `Small`, `Medium`, `Large`, `XLarge`, `2XLarge`–`6XLarge` | 修改计算规模。 |
| `AUTO_SUSPEND`      | `NULL`, `0`, 或 ≥300 秒                                        | 自动暂停前的空闲超时时间。`NULL` 会禁用自动暂停。 |
| `AUTO_RESUME`       | 布尔值                                                             | 控制传入查询是否会自动唤醒该计算集群。 |
| `MAX_CLUSTER_COUNT` | `NULL` 或非负整数型                                      | 自动扩缩容集群数的上限。 |
| `MIN_CLUSTER_COUNT` | `NULL` 或非负整数型                                      | 自动扩缩容集群数的下限。 |
| `COMMENT`           | 字符串                                                              | 自由格式的文本描述。 |

- 对于数值选项，可以使用 `NULL` 将其重置为 `0`。
- 如果提供了 `SET` 但未指定任何选项，会报错。
- `SET TAG` 用于添加或修改一个或多个标签。多个标签可以在同一条语句中使用逗号分隔进行设置。
- `UNSET TAG` 按键移除一个或多个标签。不存在的标签键会被静默忽略。
- `RENAME TO` 要求该计算集群处于已暂停状态，并且使用与 `CREATE` 相同的命名规则。

## 示例 {#examples}

暂停一个计算集群：

```sql
ALTER WAREHOUSE 'my-wh' SUSPEND;
```

恢复一个计算集群：

```sql
ALTER WAREHOUSE 'my-wh' RESUME;
```

修改计算集群设置：

```sql
ALTER WAREHOUSE 'my-wh'
    SET warehouse_size = Large
    auto_resume = TRUE
    comment = 'Serving tier';
```

禁用自动暂停：

```sql
ALTER WAREHOUSE 'my-wh' SET auto_suspend = NULL;
```

管理标签：

```sql
ALTER WAREHOUSE 'wh-hot' SET TAG environment = 'production';
ALTER WAREHOUSE 'wh-hot' SET TAG environment = 'staging', owner = 'john', cost_center = 'eng';
ALTER WAREHOUSE 'wh-hot' UNSET TAG environment;
ALTER WAREHOUSE 'wh-hot' UNSET TAG environment, owner, cost_center;
```
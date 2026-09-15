---
title: GET_LINEAGE
summary: 返回表、视图、stage 或列的上游或下游血缘。返回结果中的每一行表示血缘路径中的一个源到目标关系。
---

# GET_LINEAGE

返回表、视图、stage 或列的上游或下游血缘。返回结果中的每一行表示血缘路径中的一个源到目标关系。

## 语法 {#syntax}

```sql
GET_LINEAGE(
    '<object_name>',
    '<object_domain>',
    '<direction>'
    [, <distance> ]
)
```

## 参数 {#arguments}

| 参数 | 描述 |
|----------|-------------|
| `object_name` | 起始对象。对于表或视图，使用 `[catalog.]database.object`；对于 stage，使用 `stage_name`；对于列，使用 `[catalog.]database.object.column`。如果名称中省略了 catalog 或 database，则使用当前会话中的值。 |
| `object_domain` | 对象类型：`TABLE`、`VIEW`、`STAGE` 或 `COLUMN`。 |
| `direction` | `UPSTREAM` 表示向数据源方向追踪；`DOWNSTREAM` 表示向消费方方向追踪。 |
| `distance` | 可选，表示要遍历的最大跳数，取值范围为 `1` 到 `5`。默认值为 `5`。 |

参数按位置传递。

## 输出列 {#output-columns}

| 列 | 类型 | 描述 |
|--------|------|-------------|
| `source_object_catalog` | Nullable(String) | 包含源对象的 catalog；对于 stage 为 `NULL`。 |
| `source_object_database` | Nullable(String) | 包含源对象的数据库；对于 stage 为 `NULL`。 |
| `source_object_name` | Nullable(String) | 源对象名称。 |
| `source_object_domain` | Nullable(String) | 源对象的域：`TABLE`、`VIEW` 或 `STAGE`。 |
| `source_column_name` | Nullable(String) | 列血缘中的源列；否则为 `NULL`。 |
| `source_status` | String | `ACTIVE`，或者当源列具有脱敏策略时为 `MASKED`。 |
| `target_object_catalog` | Nullable(String) | 包含目标对象的 catalog；对于 stage 为 `NULL`。 |
| `target_object_database` | Nullable(String) | 包含目标对象的数据库；对于 stage 为 `NULL`。 |
| `target_object_name` | Nullable(String) | 目标对象名称。 |
| `target_object_domain` | Nullable(String) | 目标对象的域：`TABLE`、`VIEW` 或 `STAGE`。 |
| `target_column_name` | Nullable(String) | 列血缘中的目标列；否则为 `NULL`。 |
| `target_status` | String | `ACTIVE`，或者当目标列具有脱敏策略时为 `MASKED`。 |
| `distance` | Int32 | 与请求对象之间的跳数。直接关系的距离为 `1`。 |
| `process` | Nullable(String) | 以 JSON 格式表示的元信息，描述创建该关系的操作，例如其查询 ID、查询文本、用户、时间和血缘类型。 |

## 示例 {#examples}

本节提供用于追踪血缘的查询示例。

### 查找上游表 {#find-upstream-tables}

以下查询返回 `agg_customer_sales` 最多两跳的上游关系：

```sql
SELECT
    distance,
    source_object_catalog,
    source_object_database,
    source_object_name,
    source_object_domain,
    target_object_database,
    target_object_name
FROM GET_LINEAGE(
    'lineage_demo.agg_customer_sales',
    'TABLE',
    'UPSTREAM',
    2
)
ORDER BY distance;
```

### 查找下游列 {#find-downstream-columns}

以下查询追踪 `fact_orders.amount` 被使用的位置：

```sql
SELECT
    distance,
    source_object_name,
    source_column_name,
    target_object_name,
    target_column_name
FROM GET_LINEAGE(
    'lineage_demo.fact_orders.amount',
    'COLUMN',
    'DOWNSTREAM',
    5
)
ORDER BY distance, target_object_name, target_column_name;
```

## 使用说明 {#usage-notes}

- 如果对象存在但没有已记录的血缘，函数不会返回任何行。
- 结果会根据当前角色可见的对象范围进行过滤。
- Stage 关系仅支持对象级别；暂存文件中的字段不会作为稳定列返回。
- 系统对象和 `information_schema` 对象不会被记录为血缘源。
- 外部 catalog 对象会作为终止端点返回，不会继续遍历。
- 对于在启用血缘之前已存在的视图，可使用 [`REFRESH LINEAGE`](/tidb-cloud-lake/sql/refresh-lineage.md) 回填血缘。
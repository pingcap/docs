---
title: 数据血缘
summary: 了解如何在 {{{ .lake }}} 中启用和探索数据血缘。
---

# 数据血缘

数据血缘展示了数据如何从源对象流向目标对象。你可以使用它来理解依赖关系、评估变更影响、排查数据管道问题，以及将派生列追溯到其来源。

{{{ .lake }}} 会记录对象级和列级两种关系：

- **上游血缘** 用于识别为某个对象提供数据的表、视图或 stage。
- **下游血缘** 用于识别消费某个对象数据的对象。
- **列血缘** 用于将源列映射到派生出的目标列。

![Table and column lineage in {{{ .lake }}}](/media/tidb-cloud-lake/data-lineage.png)

## 启用数据血缘 {#enable-data-lineage}

{{{ .lake }}} 会为支持 **Lineage** 标签页的计算集群 (Warehouse) 管理血缘配置（**Data** > **Databases** > **databaseName** > **tableName**）。

## 生成血缘 {#generate-lineage}

启用血缘后，{{{ .lake }}} 会自动记录由以下操作创建的关系，例如 `CREATE TABLE ... AS SELECT`、`CREATE VIEW`、`INSERT ... SELECT`、多表 `INSERT`、`REPLACE`、`MERGE` 和 `COPY`。对于 stream，系统会将其解析为其底层表。

以下示例会创建一条两跳的血缘路径：

```sql
CREATE OR REPLACE DATABASE lineage_demo;

CREATE OR REPLACE TABLE lineage_demo.fact_orders (
    order_id BIGINT,
    customer_id BIGINT,
    amount DECIMAL(12, 2),
    order_time TIMESTAMP
);

CREATE OR REPLACE TABLE lineage_demo.agg_customer_sales AS
SELECT
    customer_id,
    sum(amount) AS total_amount,
    count(*) AS order_count,
    max(order_time) AS last_order_time
FROM lineage_demo.fact_orders
GROUP BY customer_id;

CREATE OR REPLACE TABLE lineage_demo.customer_segments AS
SELECT
    customer_id,
    total_amount,
    order_count,
    if(total_amount >= 1000, 'high_value', 'standard') AS segment,
    now() AS updated_at
FROM lineage_demo.agg_customer_sales;
```

## 探索血缘 {#explore-lineage}

在 {{{ .lake }}} 中，在 Database Explorer 中打开一个表或视图，然后选择 **Lineage** 标签页。图中会显示上游和下游对象；如果列血缘可用，还会显示列之间的连接关系。

如需使用 SQL 获取血缘信息，请使用 [`GET_LINEAGE`](/tidb-cloud-lake/sql/get-lineage.md) 表函数：

```sql
SELECT
    distance,
    source_object_database,
    source_object_name,
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

对于列级血缘，请限定列名并使用 `COLUMN` 域：

```sql
SELECT
    distance,
    source_object_name,
    source_column_name,
    target_object_name,
    target_column_name
FROM GET_LINEAGE(
    'lineage_demo.customer_segments.segment',
    'COLUMN',
    'UPSTREAM',
    2
)
ORDER BY distance;
```

## 刷新现有视图的血缘 {#refresh-lineage-for-existing-views}

在启用血缘之后创建的视图会被自动跟踪。对于已经包含视图的部署，在启用血缘后，可以先预览缺失或过期的关系，然后再刷新它们：

```sql
REFRESH LINEAGE FOR ALL VIEWS DRY RUN;
REFRESH LINEAGE FOR ALL VIEWS;
```

刷新操作会为 `default` catalog 中的所有视图校正血缘信息。它只会报告需要变更或无法处理的视图；未发生变化的视图不会显示。该命令需要全局 `SUPER` 权限。有关输出详情，请参见 [`REFRESH LINEAGE`](/tidb-cloud-lake/sql/refresh-lineage.md)。

## 限制 {#limitations}

- `GET_LINEAGE` 最多只能遍历五跳。
- 系统对象和 `information_schema` 对象不会作为血缘源被纳入。
- stage 会参与对象级血缘，但暂存文件字段无法提供稳定的列级映射。
- 外部 catalog 对象可以作为端点出现，但不会跨越外部 catalog 边界继续遍历。
- 结果仅包含当前角色可见的对象。
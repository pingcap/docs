---
title: 物化视图
summary: 物化视图会将查询结果以物理方式存储。在创建物化视图时，TiDB Cloud Lake 会对源表启用变更跟踪。
---

# 物化视图

物化视图会将查询结果以物理方式存储。它定义在 `default` catalog 中的一张持久化 FUSE 表之上。在创建物化视图时，{{{ .lake }}} 会对源表启用变更跟踪。

与逻辑视图不同，物化视图可以通过显式刷新来持久化其源表中的变更。即使物理存储落后于源表，读也能保持一致。在第一次刷新之前，{{{ .lake }}} 会根据源表计算该定义。当源表存在尚未刷新的变更时，{{{ .lake }}} 会使用 **read fix**：在读取时，将已持久化的物化视图数据与所需的源表增量数据进行联合体，并对该增量应用视图定义。因此，查询会返回当前结果，而不是过期的物化数据。

## 限制 {#limitations}

- 定义必须是基于且仅基于一张基表的简单 `SELECT ... FROM ... [WHERE ...] [GROUP BY ...]` 查询。不支持 Join、子查询、集合操作以及非确定性函数。
- 聚合仅支持 `sum`、`min`、`max`、`avg`、`count` 和 `approx_count_distinct`。不支持 `DISTINCT`、`FILTER`、窗口函数以及带排序的聚合形式。
- 源必须是 `default` catalog 中的持久化 FUSE 基表。物化视图不能将其他视图或不同表引擎的表作为源。
- 物化视图是只读的。请使用 `REFRESH MATERIALIZED VIEW` 来维护其内容；不支持 `INSERT`、`UPDATE`、`DELETE`、`TRUNCATE` 和普通的 `ALTER TABLE` 操作。

## 创建物化视图 {#create-a-materialized-view}

```sql
CREATE [ OR REPLACE ] MATERIALIZED VIEW [ IF NOT EXISTS ]
  [ <catalog_name>. ][ <database_name>. ]<view_name>
  [ ( <column_name>, ... ) ]
  [ CLUSTER BY ( <expr>, ... ) ]
  [ COMMENT = '<comment>' ]
  [ <fuse_table_option> = <value> ... ]
AS <query>
```

`CLUSTER BY` 需要显式列列表，并且可以引用非聚合输出列或 `GROUP BY` 键。可选的 Fuse 表选项用于控制物理存储布局；支持的选项请参见 [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)。

创建操作会记录定义，但不会同步地填充物理存储。请运行 `REFRESH MATERIALIZED VIEW` 以物化初始数据。

```sql
CREATE TABLE orders (
  order_id INT,
  customer_id INT,
  amount DECIMAL(10, 2),
  paid BOOLEAN
);

CREATE MATERIALIZED VIEW paid_orders_by_customer
  (customer_id, total_amount, order_count)
  CLUSTER BY (customer_id)
  COMMENT = 'Paid-order totals by customer'
AS
SELECT customer_id, sum(amount), count(*)
FROM orders
WHERE paid
GROUP BY customer_id;

REFRESH MATERIALIZED VIEW paid_orders_by_customer;
```

`CREATE OR REPLACE` 会替换现有的物化视图。若名称已存在，`IF NOT EXISTS` 不会执行任何操作。

## 刷新物化视图 {#refresh-a-materialized-view}

```sql
REFRESH MATERIALIZED VIEW [ <catalog_name>. ][ <database_name>. ]<view_name>
```

第一次刷新会将源数据物化。后续刷新会对仅追加的变更进行增量地处理。如果源表存在 `UPDATE`、`DELETE` 或 `TRUNCATE` 变更，{{{ .lake }}} 会根据当前源状态重建物化视图，以确保结果正确。

## 修改物理布局 {#change-physical-layout}

对于支持的维护操作，请使用专用的 `ALTER MATERIALIZED VIEW` 语法：

```sql
ALTER MATERIALIZED VIEW <view_name> CLUSTER BY ( <expr>, ... );
ALTER MATERIALIZED VIEW <view_name> DROP CLUSTER KEY;
ALTER MATERIALIZED VIEW <view_name> RECLUSTER [ FINAL ] [ LIMIT <n> ];
ALTER MATERIALIZED VIEW <view_name> SET OPTIONS ( <option> = <value>, ... );
ALTER MATERIALIZED VIEW <view_name> UNSET OPTIONS ( <option>, ... );
ALTER MATERIALIZED VIEW <view_name> COMMENT = '<comment>';
```

例如，在刷新前设置一个布局选项：

```sql
ALTER MATERIALIZED VIEW paid_orders_by_customer SET OPTIONS (row_per_block = 2);
REFRESH MATERIALIZED VIEW paid_orders_by_customer;
```

物化视图不支持 `RECLUSTER WHERE`。如需修改定义，请使用 `CREATE OR REPLACE MATERIALIZED VIEW`；`ALTER VIEW` 不适用。

## 查看和删除定义 {#view-and-remove-definitions}

```sql
SHOW MATERIALIZED VIEWS
  [ { FROM | IN } <database_name> ]
  [ LIKE '<pattern>' | WHERE <expr> ];

SHOW CREATE MATERIALIZED VIEW
  [ <catalog_name>. ][ <database_name>. ]<view_name>;

DROP MATERIALIZED VIEW [ IF EXISTS ]
  [ <catalog_name>. ][ <database_name>. ]<view_name>;
```

```sql
SHOW MATERIALIZED VIEWS LIKE 'paid_orders%';
SHOW CREATE MATERIALIZED VIEW paid_orders_by_customer;
DROP MATERIALIZED VIEW IF EXISTS paid_orders_by_customer;
```

## 访问控制要求 {#access-control-requirements}

要查询、刷新、修改、查看或删除物化视图，用户需要对其源表具有 `SELECT` 权限（或具有提供等效访问能力的所有权）。权限会根据当前源表标识进行检查，因此源表重命名不会改变这一要求。
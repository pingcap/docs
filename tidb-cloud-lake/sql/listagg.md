---
title: LISTAGG
summary: 将多行中的值连接为一个字符串，并使用指定的分隔符分隔。此操作可以通过两种不同的函数类型执行：- 聚合函数：连接会在整个结果集的所有行上进行。- 窗口函数：连接会在结果集的每个分区内进行，分区由 `PARTITION BY` 子句定义。
---

# LISTAGG

将多行中的值连接为一个字符串，并使用指定的分隔符分隔。此操作可以通过两种不同的函数类型执行：

- 聚合函数：连接会在整个结果集的所有行上进行。
- 窗口函数：连接会在结果集的每个分区内进行，分区由 `PARTITION BY` 子句定义。

## 语法 {#syntax}

```sql
-- Aggregate Function
LISTAGG([DISTINCT] <expr> [, <delimiter>])
  [WITHIN GROUP (ORDER BY <order_by_expr>)]

-- Window Function
LISTAGG([DISTINCT] <expr> [, <delimiter>])
  [WITHIN GROUP (ORDER BY <order_by_expr>)]
  OVER ([PARTITION BY <partition_expr>])
```

| 参数                            | 描述                                                                                              |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| `DISTINCT`                      | 可选。连接前移除重复值。                                                                          |
| `<expr>`                        | 要连接的表达式（通常是列或表达式）。                                                              |
| `<delimiter>`                   | 可选。用于分隔每个连接值的字符串。如果省略，默认为空字符串。                                      |
| `ORDER BY <order_by_expr>`      | 定义值连接时的顺序。                                                                              |
| `PARTITION BY <partition_expr>` | 将行划分为多个分区，以便在每个组内分别执行聚合。                                                  |

## 别名 {#aliases}

- [STRING_AGG](/tidb-cloud-lake/sql/string-agg.md)
- [GROUP_CONCAT](/tidb-cloud-lake/sql/group-concat.md)

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

在此示例中，我们有一张客户订单表。每个订单都属于某个客户，我们希望创建一个列表，列出每个客户购买过的所有产品。

```sql
CREATE TABLE orders (
  customer_id INT,
  product_name VARCHAR
);

INSERT INTO orders (customer_id, product_name) VALUES
(1, 'Laptop'),
(1, 'Mouse'),
(1, 'Laptop'),
(2, 'Phone'),
(2, 'Headphones');
```

以下示例将 `LISTAGG` 用作聚合函数，并结合 GROUP BY 将每个客户购买的所有产品连接为一个字符串：

```sql
SELECT
  customer_id,
  LISTAGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name) AS product_list
FROM orders
GROUP BY customer_id;
```

```sql
┌─────────────────────────────────────────┐
│   customer_id   │      product_list     │
├─────────────────┼───────────────────────┤
│               2 │ Headphones, Phone     │
│               1 │ Laptop, Laptop, Mouse │
└─────────────────────────────────────────┘
```

以下示例将 `LISTAGG` 用作窗口函数，因此每一行都会保留其原始明细，同时还会显示该客户分组的完整产品列表：

```sql
SELECT
  customer_id,
  product_name,
  LISTAGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name)
    OVER (PARTITION BY customer_id) AS product_list
FROM orders;
```

```sql
┌────────────────────────────────────────────────────────────┐
│   customer_id   │   product_name   │      product_list     │
├─────────────────┼──────────────────┼───────────────────────┤
│               2 │ Phone            │ Headphones, Phone     │
│               2 │ Headphones       │ Headphones, Phone     │
│               1 │ Laptop           │ Laptop, Laptop, Mouse │
│               1 │ Mouse            │ Laptop, Laptop, Mouse │
│               1 │ Laptop           │ Laptop, Laptop, Mouse │
└────────────────────────────────────────────────────────────┘
```
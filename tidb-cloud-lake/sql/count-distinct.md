---
title: COUNT_DISTINCT
summary: 聚合函数。
---

# COUNT_DISTINCT

聚合函数。

`count(distinct ...)` 函数用于计算一组值中唯一值的数量。

如果希望在较少内存和时间开销下，从大型数据集中获得估算结果，可以考虑使用 [APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/approx-count-distinct.md)。

> **注意：**
>
> 不统计 `NULL` 值。

## 语法 {#syntax}

```sql
COUNT(distinct <expr> ...)
UNIQ(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|--------------------------------------------------|
| `<expr>`  | 任意表达式，参数个数范围为 [1, 32] |

## 返回类型 {#return-type}

UInt64

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE products (
  id INT,
  name VARCHAR,
  category VARCHAR,
  price FLOAT
);

INSERT INTO products (id, name, category, price)
VALUES (1, 'Laptop', 'Electronics', 1000),
       (2, 'Smartphone', 'Electronics', 800),
       (3, 'Tablet', 'Electronics', 600),
       (4, 'Chair', 'Furniture', 150),
       (5, 'Table', 'Furniture', 300);
```

**查询演示：统计不同类别的数量**

```sql
SELECT COUNT(DISTINCT category) AS unique_categories
FROM products;
```

**结果**

```sql
| unique_categories |
|-------------------|
|         2         |
```
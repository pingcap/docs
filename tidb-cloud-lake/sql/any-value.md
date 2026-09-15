---
title: ANY_VALUE
summary: 聚合函数。
---

# ANY_VALUE

聚合函数。

`ANY_VALUE()` 函数从输入表达式中返回一个任意的非 `NULL` 值。当你在 `GROUP BY` 查询中需要选择一个未分组或未聚合的列时，可以使用该函数。

> **别名：** `ANY()` 返回与 `ANY_VALUE()` 相同的结果，并且为了兼容性仍然可用。

## 语法 {#syntax}

```sql
ANY_VALUE(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<expr>`  | 任意表达式 |

## 返回类型 {#return-type}

`<expr>` 的类型。如果所有值都是 `NULL`，则返回值为 `NULL`。

> **注意：**
>
> - `ANY_VALUE()` 是非确定性的，在不同执行中可能返回不同的值。
> - 如需可预测的结果，请改用 `MIN()` 或 `MAX()`。

## 示例 {#example}

**示例数据：**

```sql
CREATE TABLE sales (
  region VARCHAR,
  manager VARCHAR,
  sales_amount DECIMAL(10, 2)
);

INSERT INTO sales VALUES
  ('North', 'Alice', 15000.00),
  ('North', 'Alice', 12000.00),
  ('South', 'Bob', 20000.00);
```

**问题：** 以下查询会失败，因为 `manager` 不在 GROUP BY 中：

```sql
SELECT region, manager, SUM(sales_amount)  -- ❌ Error
FROM sales GROUP BY region;
```

**旧方法：** 将 `manager` 添加到 GROUP BY 中，但这会产生比所需更多的分组，并影响性能：

```sql
SELECT region, manager, SUM(sales_amount)
FROM sales GROUP BY region, manager;  -- ❌ Poor performance due to extra grouping
```

**更好的解决方案：** 使用 `ANY_VALUE()` 选择 `manager`：

```sql
SELECT
  region,
  ANY_VALUE(manager) AS manager,  -- ✅ Works
  SUM(sales_amount) AS total_sales
FROM sales
GROUP BY region;
```

**结果：**

```text
| region | manager | total_sales |
|--------|---------|-------------|
| North  | Alice   | 27000.00    |
| South  | Bob     | 20000.00    |
```
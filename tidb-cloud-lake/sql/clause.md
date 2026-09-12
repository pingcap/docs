---
title: WITH 子句
summary: WITH 子句是位于 SELECT 语句主体之前的可选子句，用于定义一个或多个 CTE（公共表表达式），以便在该语句的后续部分中引用。
---

# WITH 子句

WITH 子句是位于 SELECT 语句主体之前的可选子句，用于定义一个或多个 CTE（公共表表达式），以便在该语句的后续部分中引用。

## 语法 {#syntax}

### 基本 CTE {#basic-cte}

```sql
[ WITH
    cte_name1 [ ( cte_column_list ) ] AS ( SELECT ... )
  [ , cte_name2 [ ( cte_column_list ) ] AS ( SELECT ... ) ]
  [ , cte_nameN [ ( cte_column_list ) ] AS ( SELECT ... ) ]
]
SELECT ...
```

### 递归 CTE {#recursive-cte}

```sql
[ WITH [ RECURSIVE ]
    cte_name1 ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause )
  [ , cte_name2 ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause ) ]
  [ , cte_nameN ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause ) ]
]
SELECT ...
```

其中：

- `anchorClause`：`SELECT anchor_column_list FROM ...`
- `recursiveClause`：`SELECT recursive_column_list FROM ... [ JOIN ... ]`

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `cte_name` | CTE 名称必须遵循标准标识符规则 |
| `cte_column_list` | CTE 中各列的名称 |
| `anchor_column_list` | 递归 CTE 的锚定子句中使用的列 |
| `recursive_column_list` | 递归 CTE 的递归子句中使用的列 |

## 示例 {#examples}

### 基本 CTE {#basic-cte}

```sql
WITH high_value_customers AS (
    SELECT customer_id, customer_name, total_spent
    FROM customers
    WHERE total_spent > 10000
)
SELECT c.customer_name, o.order_date, o.order_amount
FROM high_value_customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC;
```

### 多个 CTE {#multiple-ctes}

```sql
WITH
  regional_sales AS (
    SELECT region, SUM(sales_amount) as total_sales
    FROM sales_data
    GROUP BY region
  ),
  top_regions AS (
    SELECT region, total_sales
    FROM regional_sales
    WHERE total_sales > 1000000
  )
SELECT r.region, r.total_sales
FROM top_regions r
ORDER BY r.total_sales DESC;
```

### 递归 CTE {#recursive-cte}

```sql
WITH RECURSIVE countdown AS (
    -- Anchor clause: starting point
    SELECT 10 as num

    UNION ALL

    -- Recursive clause: repeat until condition
    SELECT num - 1
    FROM countdown
    WHERE num > 1  -- Stop condition
)
SELECT num FROM countdown
ORDER BY num DESC;
```

## 使用说明 {#usage-notes}

- CTE 是临时的具名结果集，仅在查询执行期间存在
- 在同一个 WITH 子句中，CTE 名称必须唯一
- CTE 可以引用同一个 WITH 子句中先前定义的 CTE
- 递归 CTE 必须同时包含锚定子句和递归子句，并通过 UNION ALL 连接
- 使用递归 CTE 时，必须指定 RECURSIVE 关键字
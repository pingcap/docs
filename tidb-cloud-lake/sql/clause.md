---
title: WITH 句
summary: WITH 句は、SELECT 文の本体の前に置くことができるオプションの句であり、文の後続部分で参照できる 1 つ以上の CTE（共通テーブル式）を定義します。
---

# WITH 句

WITH 句は、SELECT 文の本体の前に置くことができるオプションの句であり、文の後続部分で参照できる 1 つ以上の CTE（共通テーブル式）を定義します。

## 構文 {#syntax}

### 基本 CTE {#basic-cte}

```sql
[ WITH
    cte_name1 [ ( cte_column_list ) ] AS ( SELECT ... )
  [ , cte_name2 [ ( cte_column_list ) ] AS ( SELECT ... ) ]
  [ , cte_nameN [ ( cte_column_list ) ] AS ( SELECT ... ) ]
]
SELECT ...
```

### 再帰 CTE {#recursive-cte}

```sql
[ WITH [ RECURSIVE ]
    cte_name1 ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause )
  [ , cte_name2 ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause ) ]
  [ , cte_nameN ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause ) ]
]
SELECT ...
```

以下のとおりです。

- `anchorClause`: `SELECT anchor_column_list FROM ...`
- `recursiveClause`: `SELECT recursive_column_list FROM ... [ JOIN ... ]`

## パラメーター {#parameters}

| Parameter | 説明 |
|-----------|-------------|
| `cte_name` | CTE 名は標準の識別子ルールに従う必要があります |
| `cte_column_list` | CTE 内のカラム名 |
| `anchor_column_list` | 再帰 CTE のアンカー句で使用されるカラム |
| `recursive_column_list` | 再帰 CTE の再帰句で使用されるカラム |

## 例 {#examples}

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

### 複数の CTE {#multiple-ctes}

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

### 再帰 CTE {#recursive-cte}

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

## 使用上の注意 {#usage-notes}

- CTE は一時的な名前付き結果セットであり、クエリの実行中にのみ存在します
- CTE 名は同じ WITH 句内で一意である必要があります
- CTE は、同じ WITH 句内で先に定義された CTE を参照できます
- 再帰 CTE では、UNION ALL で接続されたアンカー句と再帰句の両方が必要です
- 再帰 CTE を使用する場合は、RECURSIVE キーワードが必要です
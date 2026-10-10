---
title: LAST_VALUE
summary: ウィンドウフレーム内の最後の値を返します。
---

# LAST_VALUE

ウィンドウフレーム内の最後の値を返します。

関連情報:

- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md)
- [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md)

## 構文 {#syntax}

```sql
LAST_VALUE(expression) [ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
    [ window_frame ]
)
```

**引数:**

- `expression`: 必須。最後の値を返す対象のカラムまたは式です。
- `PARTITION BY`: 任意。行をパーティションに分割します。
- `ORDER BY`: 必須。ウィンドウ内の並び順を決定します。
- `window_frame`: 任意。ウィンドウフレームを定義します。デフォルトは `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` です。

**Notes:**

- 並び替えられたウィンドウフレーム内の最後の値を返します。
- `IGNORE NULLS` を使用して null 値をスキップでき、`RESPECT NULLS` を使用するとデフォルトの動作を維持します。
- パーティション内の真の最後の行が必要な場合は、現在の行より後で終わるフレーム（たとえば `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`）を使用します。
- 各グループの最新の値や、先読みウィンドウ内の直近の値を見つけるのに便利です。

## 例 {#examples}

```sql
-- Sample order data
CREATE OR REPLACE TABLE orders_window_demo (
    customer VARCHAR,
    order_id INT,
    order_time TIMESTAMP,
    amount INT,
    sales_rep VARCHAR
);

INSERT INTO orders_window_demo VALUES
    ('Alice', 1001, to_timestamp('2024-05-01 09:00:00'), 120, 'Erin'),
    ('Alice', 1002, to_timestamp('2024-05-01 11:00:00'), 135, NULL),
    ('Alice', 1003, to_timestamp('2024-05-02 14:30:00'), 125, 'Glen'),
    ('Bob',   1004, to_timestamp('2024-05-01 08:30:00'),  90, NULL),
    ('Bob',   1005, to_timestamp('2024-05-01 20:15:00'), 105, 'Kai'),
    ('Bob',   1006, to_timestamp('2024-05-03 10:00:00'),  95, NULL),
    ('Carol', 1007, to_timestamp('2024-05-04 09:45:00'),  80, 'Lily');
```

**例 1. 各 customer パーティション内の最新の注文**

```sql
SELECT customer,
       order_id,
       order_time,
       LAST_VALUE(order_id) OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS last_order_for_customer
FROM orders_window_demo
ORDER BY customer, order_time;
```

結果:

```
customer | order_id | order_time           | last_order_for_customer
---------+----------+----------------------+-------------------------
Alice    |     1001 | 2024-05-01 09:00:00  |                    1003
Alice    |     1002 | 2024-05-01 11:00:00  |                    1003
Alice    |     1003 | 2024-05-02 14:30:00  |                    1003
Bob      |     1004 | 2024-05-01 08:30:00  |                    1006
Bob      |     1005 | 2024-05-01 20:15:00  |                    1006
Bob      |     1006 | 2024-05-03 10:00:00  |                    1006
Carol    |     1007 | 2024-05-04 09:45:00  |                    1007
```

**例 2. 各 customer 内で 12 時間先まで先読みする**

```sql
SELECT customer,
       order_id,
       order_time,
       amount,
       LAST_VALUE(amount) OVER (
           PARTITION BY customer
           ORDER BY order_time
           RANGE BETWEEN CURRENT ROW AND INTERVAL 12 HOUR FOLLOWING
       ) AS last_amount_next_12h
FROM orders_window_demo
ORDER BY customer, order_time;
```

結果:

```
customer | order_id | order_time           | amount | last_amount_next_12h
---------+----------+----------------------+--------+----------------------
Alice    |     1001 | 2024-05-01 09:00:00  |    120 |                  135
Alice    |     1002 | 2024-05-01 11:00:00  |    135 |                  135
Alice    |     1003 | 2024-05-02 14:30:00  |    125 |                  125
Bob      |     1004 | 2024-05-01 08:30:00  |     90 |                  105
Bob      |     1005 | 2024-05-01 20:15:00  |    105 |                  105
Bob      |     1006 | 2024-05-03 10:00:00  |     95 |                   95
Carol    |     1007 | 2024-05-04 09:45:00  |     80 |                   80
```

**例 3. 最後の sales rep を前方に走査するときに null をスキップする**

```sql
SELECT customer,
       order_id,
       sales_rep,
       LAST_VALUE(sales_rep) RESPECT NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS last_rep_respect,
       LAST_VALUE(sales_rep) IGNORE NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS last_rep_ignore
FROM orders_window_demo
ORDER BY customer, order_id;
```

結果:

```
customer | order_id | sales_rep | last_rep_respect | last_rep_ignore
---------+----------+-----------+------------------+-----------------
Alice    |     1001 | Erin      | Glen             | Glen
Alice    |     1002 | NULL      | Glen             | Glen
Alice    |     1003 | Glen      | Glen             | Glen
Bob      |     1004 | NULL      | NULL             | Kai
Bob      |     1005 | Kai       | NULL             | Kai
Bob      |     1006 | NULL      | NULL             | Kai
Carol    |     1007 | Lily      | Lily             | Lily
```
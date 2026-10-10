---
title: FIRST_VALUE
summary: ウィンドウフレーム内の最初の値を返します。
---

# FIRST_VALUE

ウィンドウフレーム内の最初の値を返します。

関連情報:

- [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md)
- [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md)

## 構文 {#syntax}

```sql
FIRST_VALUE(expression) [ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
    [ window_frame ]
)
```

**引数:**

- `expression`: 必須。最初の値を返す対象のカラムまたは式です。
- `PARTITION BY`: 任意。行をパーティションに分割します。
- `ORDER BY`: 必須。ウィンドウ内の並び順を決定します。
- `window_frame`: 任意。ウィンドウフレームを定義します。デフォルトは `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` です。

**Notes:**

- 並び替えられたウィンドウフレーム内の最初の値を返します。
- `IGNORE NULLS` を使用して null 値をスキップでき、`RESPECT NULLS` を使用するとデフォルトの動作を維持します。
- デフォルトの range フレームではなく行ベースの意味論が必要な場合は、明示的なウィンドウフレーム（たとえば `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`）を指定してください。
- 各グループまたは時間ウィンドウ内で最も早い値や最小の値を見つけるのに役立ちます。

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

**例 1. 顧客ごとの最初の購入**

```sql
SELECT customer,
       order_id,
       order_time,
       amount,
       FIRST_VALUE(amount) OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS first_order_amount
FROM orders_window_demo
ORDER BY customer, order_time;
```

結果:

```
customer | order_id | order_time           | amount | first_order_amount
---------+----------+----------------------+--------+--------------------
Alice    |     1001 | 2024-05-01 09:00:00  |    120 |                120
Alice    |     1002 | 2024-05-01 11:00:00  |    135 |                120
Alice    |     1003 | 2024-05-02 14:30:00  |    125 |                120
Bob      |     1004 | 2024-05-01 08:30:00  |     90 |                 90
Bob      |     1005 | 2024-05-01 20:15:00  |    105 |                 90
Bob      |     1006 | 2024-05-03 10:00:00  |     95 |                 90
Carol    |     1007 | 2024-05-04 09:45:00  |     80 |                 80
```

**例 2. 直近 24 時間内の最初の注文**

```sql
SELECT customer,
       order_id,
       order_time,
       FIRST_VALUE(order_id) OVER (
           PARTITION BY customer
           ORDER BY order_time
           RANGE BETWEEN INTERVAL 1 DAY PRECEDING AND CURRENT ROW
       ) AS first_order_in_24h
FROM orders_window_demo
ORDER BY customer, order_time;
```

結果:

```
customer | order_id | order_time           | first_order_in_24h
---------+----------+----------------------+--------------------
Alice    |     1001 | 2024-05-01 09:00:00  |               1001
Alice    |     1002 | 2024-05-01 11:00:00  |               1001
Alice    |     1003 | 2024-05-02 14:30:00  |               1003
Bob      |     1004 | 2024-05-01 08:30:00  |               1004
Bob      |     1005 | 2024-05-01 20:15:00  |               1004
Bob      |     1006 | 2024-05-03 10:00:00  |               1006
Carol    |     1007 | 2024-05-04 09:45:00  |               1007
```

**例 3. null をスキップして最初に名前が付いている営業担当者を見つける**

```sql
SELECT customer,
       order_id,
       sales_rep,
       FIRST_VALUE(sales_rep) RESPECT NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
       ) AS first_rep_respect,
       FIRST_VALUE(sales_rep) IGNORE NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
       ) AS first_rep_ignore
FROM orders_window_demo
ORDER BY customer, order_id;
```

結果:

```
customer | order_id | sales_rep | first_rep_respect | first_rep_ignore
---------+----------+-----------+-------------------+------------------
Alice    |     1001 | Erin      | Erin              | Erin
Alice    |     1002 | NULL      | Erin              | Erin
Alice    |     1003 | Glen      | Erin              | Erin
Bob      |     1004 | NULL      | NULL              | NULL
Bob      |     1005 | Kai       | NULL              | Kai
Bob      |     1006 | NULL      | NULL              | Kai
Carol    |     1007 | Lily      | Lily              | Lily
```
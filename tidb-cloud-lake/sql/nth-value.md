---
title: NTH_VALUE
summary: ウィンドウフレーム内の指定した位置 (N) にある値を返します。
---

# NTH_VALUE

ウィンドウフレーム内の指定した位置 (N) にある値を返します。

関連情報:

- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md)
- [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md)

## 構文 {#syntax}

```sql
NTH_VALUE(
    expression,
    n
)
[ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY order_expression
    [ window_frame ]
)
```

**引数:**

- `expression`: 必須。評価するカラムまたは式です。
- `n`: 必須。返す値の位置番号 (1 始まり) です。
- `IGNORE NULLS`: 任意。位置を数える際に null 値をスキップします。
- `RESPECT NULLS`: 任意。位置を数える際に null 値を含めます（デフォルト）。
- `window_frame`: 任意。ウィンドウフレームを定義します。デフォルトは `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` です。

**注意:**

- `n` は正の整数である必要があります。`n = 1` は `FIRST_VALUE` と同等です。
- 指定した位置がフレーム内に存在しない場合は `NULL` を返します。
- `ROWS BETWEEN ...` と組み合わせることで、位置をパーティション全体で評価するか、またはそれまでに見えた行に対して評価するかを制御できます。
- ウィンドウフレームの構文については、[Window Frame Syntax](/tidb-cloud-lake/sql/window-functions-overview.md#basic-syntax) を参照してください。

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

**2 番目の注文を見つけ、2 番目の営業担当者に対する null の扱いを示します:**

```sql
SELECT customer,
       order_id,
       order_time,
       NTH_VALUE(order_id, 2) OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS second_order_so_far,
       NTH_VALUE(sales_rep, 2) RESPECT NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS second_rep_respect,
       NTH_VALUE(sales_rep, 2) IGNORE NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS second_rep_ignore
FROM orders_window_demo
ORDER BY customer, order_time;
```

結果:

```
customer | order_id | order_time           | second_order_so_far | second_rep_respect | second_rep_ignore
---------+----------+----------------------+---------------------+--------------------+-------------------
Alice    |     1001 | 2024-05-01 09:00:00  |                NULL | NULL               | NULL
Alice    |     1002 | 2024-05-01 11:00:00  |                1002 | NULL               | NULL
Alice    |     1003 | 2024-05-02 14:30:00  |                1002 | NULL               | Glen
Bob      |     1004 | 2024-05-01 08:30:00  |                NULL | NULL               | NULL
Bob      |     1005 | 2024-05-01 20:15:00  |                1005 | Kai                | Kai
Bob      |     1006 | 2024-05-03 10:00:00  |                1005 | Kai                | Kai
Carol    |     1007 | 2024-05-04 09:45:00  |                NULL | NULL               | NULL
```
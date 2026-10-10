---
title: LISTAGG
summary: 指定した区切り文字で複数行の値を 1 つの文字列に連結します。この操作は 2 種類の関数タイプで実行できます。- Aggregate Function: 連結は結果セット全体のすべての行に対して行われます。- Window Function: 連結は `PARTITION BY` 句で定義された結果セット内の各パーティションごとに行われます。
---

# LISTAGG

指定した区切り文字で複数行の値を 1 つの文字列に連結します。この操作は、次の 2 種類の関数タイプで実行できます。

- Aggregate Function: 連結は結果セット全体のすべての行に対して行われます。
- Window Function: 連結は、`PARTITION BY` 句で定義された結果セット内の各パーティションごとに行われます。

## 構文 {#syntax}

```sql
-- Aggregate Function
LISTAGG([DISTINCT] <expr> [, <delimiter>])
  [WITHIN GROUP (ORDER BY <order_by_expr>)]

-- Window Function
LISTAGG([DISTINCT] <expr> [, <delimiter>])
  [WITHIN GROUP (ORDER BY <order_by_expr>)]
  OVER ([PARTITION BY <partition_expr>])
```

| パラメータ | 説明 |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| `DISTINCT`                      | 任意。連結する前に重複する値を削除します。                                          |
| `<expr>`                        | 連結する式です（通常はカラムまたは式）。                              |
| `<delimiter>`                   | 任意。連結された各値を区切る文字列です。省略した場合のデフォルトは空文字列です。 |
| `ORDER BY <order_by_expr>`      | 値を連結する順序を定義します。                                           |
| `PARTITION BY <partition_expr>` | 行をパーティションに分割し、各グループ内で個別に集計を実行します。                 |

## エイリアス {#aliases}

- [STRING_AGG](/tidb-cloud-lake/sql/string-agg.md)
- [GROUP_CONCAT](/tidb-cloud-lake/sql/group-concat.md)

## 戻り値の型 {#return-type}

文字列です。

## 例 {#examples}

この例では、顧客の注文テーブルがあります。各注文は 1 人の顧客に属しており、各顧客が購入したすべての商品の一覧を作成したいとします。

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

次の例では、`LISTAGG` を `GROUP BY` とともに集計関数として使用し、各顧客が購入したすべての商品を 1 つの文字列に連結しています。

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

次の例では、`LISTAGG` をウィンドウ関数として使用しているため、各行は元の詳細を保持したまま、その顧客グループ全体の商品一覧も表示します。

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
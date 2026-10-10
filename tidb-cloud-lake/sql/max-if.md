---
title: MAX_IF
summary: 接尾辞 `_IF` は任意の集計関数名に追加できます。この場合、集計関数は追加の引数、つまり条件を受け取ります。
---

# MAX_IF

## MAX_IF {#max-if}

接尾辞 `_IF` は任意の集計関数名に追加できます。この場合、集計関数は追加の引数、つまり条件を受け取ります。

```sql
MAX_IF(<column>, <cond>)
```

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE sales (
  id INT,
  salesperson_id INT,
  product_id INT,
  revenue FLOAT
);

INSERT INTO sales (id, salesperson_id, product_id, revenue)
VALUES (1, 1, 1, 1000),
       (2, 1, 2, 2000),
       (3, 1, 3, 3000),
       (4, 2, 1, 1500),
       (5, 2, 2, 2500);
```

**クエリのデモ: ID 1 の営業担当者の最大売上を検索する**

```sql
SELECT MAX_IF(revenue, salesperson_id = 1) AS max_revenue_salesperson_1
FROM sales;
```

**結果**

```sql
| max_revenue_salesperson_1 |
|---------------------------|
|           3000            |
```
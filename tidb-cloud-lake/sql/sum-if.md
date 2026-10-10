---
title: SUM_IF
summary: 接尾辞 -If は任意の集約関数名に付加できます。この場合、集約関数は追加の引数である条件を受け取ります。
---

# SUM_IF

## SUM_IF {#sum-if}

接尾辞 -If は任意の集約関数名に付加できます。この場合、集約関数は追加の引数である条件を受け取ります。

```
SUM_IF(<column>, <cond>)
```

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE order_data (
  id INT,
  customer_id INT,
  amount FLOAT,
  status VARCHAR
);

INSERT INTO order_data (id, customer_id, amount, status)
VALUES (1, 1, 100, 'Completed'),
       (2, 2, 50, 'Completed'),
       (3, 3, 80, 'Cancelled'),
       (4, 4, 120, 'Completed'),
       (5, 5, 75, 'Cancelled');
```

**クエリ例: Completed の注文の合計金額を計算する**

```sql
SELECT SUM_IF(amount, status = 'Completed') AS total_amount_completed
FROM order_data;
```

**結果**

```sql
| total_amount_completed |
|------------------------|
|         270.0          |
```
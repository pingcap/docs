---
title: COUNT_IF
summary: 接尾辞 `_IF` は任意の集約関数名の末尾に追加できます。この場合、集約関数は追加の引数、つまり条件を受け取ります。
---

# COUNT_IF

## COUNT_IF {#count-if}

接尾辞 `_IF` は任意の集約関数名の末尾に追加できます。この場合、集約関数は追加の引数、つまり条件を受け取ります。

```sql
COUNT_IF(<column>, <cond>)
```

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE orders (
  id INT,
  customer_id INT,
  status VARCHAR,
  total FLOAT
);

INSERT INTO orders (id, customer_id, status, total)
VALUES (1, 1, 'completed', 100),
       (2, 2, 'completed', 200),
       (3, 1, 'pending', 150),
       (4, 3, 'completed', 250),
       (5, 2, 'pending', 300);
```

**クエリのデモ: 完了した注文数をカウントする**

```sql
SELECT COUNT_IF(status, status = 'completed') AS completed_orders
FROM orders;
```

**結果**

```sql
| completed_orders |
|------------------|
|        3         |
```
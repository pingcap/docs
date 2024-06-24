---
title: Vector Column
summary: 
---

# Vector Column

> **Note**
>
> The vector search feature is currently in beta and only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## Basic Usage

### Create a Table with Vector Column

```sql
tidb> CREATE TABLE vector_table (id INT PRIMARY KEY, doc TEXT, embedding VECTOR(3));
Query OK, 0 rows affected (0.51 sec)
```

### Insert Vector Data

```sql
tidb> INSERT INTO vector_table VALUES (1, 'apple', '[1,1,1]'),
(2, 'banana', '[1,1,2]'),
(3, 'dog', '[2, 2, 2]');

Query OK, 3 rows affected (0.30 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

### Query Vector Data

```sql
tidb> SELECT * FROM vector_table;
+----+--------+-----------+
| id | doc    | embedding |
+----+--------+-----------+
|  1 | apple  | [1,1,1]   |
|  2 | banana | [1,1,2]   |
|  3 | dog    | [2,2,2]   |
+----+--------+-----------+
3 rows in set (0.29 sec)
```

## Vector Functions

TiDB Vector Search supports the following vector distance functions:

- `Vec_L1_Distance` (Manhattan Distance)
- `Vec_L2_Distance` (Squared Euclidean)
- `Vec_Cosine_Distance` (Cosine Distance)
- `Vec_Negative_Inner_Product` (Negative Inner Product)

```sql
SELECT vec_cosine_distance('[1,1,1]', '[1,2,3]');
SELECT vec_l1_distance('[1,1,1]', '[1,2,3]');
SELECT vec_l2_distance('[1,1,1]', '[1,2,3]');
SELECT vec_negative_inner_product('[1,1,1]', '[1,2,3]');
```

Other available vector functions:

```sql
-- Get dimensions
SELECT vec_dims('[1, 1, 1]');

-- Transform between vector and text
SELECT vec_from_text('[1,1,1]');
SELECT vec_as_text('[1,1,1]');

-- Euclidean norm
SELECT vec_l2_norm('[1,2,3]')
```

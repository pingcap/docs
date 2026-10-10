---
title: system.indexes
summary: 作成されたインデックスに関する情報を含みます。
---

# system.indexes

> **Note:**
>
> v1.1.50 で導入されました。

作成されたインデックスに関する情報を含みます。

関連情報: [SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md)

```sql
CREATE TABLE t1(a int,b int);

CREATE AGGREGATING INDEX idx1 AS SELECT SUM(a), b FROM default.t1 WHERE b > 3 GROUP BY b;

SELECT * FROM system.indexes;

+----------+-------------+------------------------------------------------------------+----------------------------+
| name     | type        | definition                                                 | created_on                 |
+----------+-------------+------------------------------------------------------------+----------------------------+
| test_idx | AGGREGATING | SELECT b, SUM(a) FROM default.t1 WHERE (b > 3) GROUP BY b  | 2023-05-17 11:53:54.474377 |
+----------+-------------+------------------------------------------------------------+----------------------------+
```
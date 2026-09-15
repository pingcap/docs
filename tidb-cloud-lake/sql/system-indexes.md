---
title: system.indexes
summary: 包含已创建索引的信息。
---

# system.indexes

> **注意：**
>
> 于 v1.1.50 中引入。

包含已创建索引的信息。

另请参阅：[SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md)

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
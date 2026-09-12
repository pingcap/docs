---
title: CREATE AGGREGATING INDEX
summary: 在 {{{ .lake }}} 中创建一个新的聚合索引。
---

# CREATE AGGREGATING INDEX

在 {{{ .lake }}} 中创建一个新的聚合索引。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] AGGREGATING INDEX <index_name> AS SELECT ...
```

- 创建聚合索引时，其使用范围仅限于标准的[聚合函数](/tidb-cloud-lake/_index.md)（例如 AVG、SUM、MIN、MAX、COUNT 和 GROUP BY）。请注意，不支持 GROUPING SETS、[窗口函数](/tidb-cloud-lake/_index.md)、[LIMIT](/tidb-cloud-lake/sql/select.md#limit-clause) 和 [ORDER BY](/tidb-cloud-lake/sql/select.md#order-by-clause)，否则会报错：`Currently create aggregating index just support simple query, like: SELECT ... FROM ... WHERE ... GROUP BY ...`。

- 创建聚合索引时定义的查询过滤作用域，应与实际查询的作用域一致，或覆盖实际查询的作用域。

- 要确认聚合索引是否对某个查询生效，可以使用 [EXPLAIN](/tidb-cloud-lake/sql/explain.md) 命令分析该查询。

## 示例 {#examples}

以下示例为查询 "SELECT MIN(a), MAX(c) FROM agg" 创建了一个名为 *my_agg_index* 的聚合索引：

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;
```
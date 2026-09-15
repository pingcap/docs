---
title: SET CLUSTER KEY
summary: 在创建表时设置 cluster key。
---

# SET CLUSTER KEY

在创建表时设置 cluster key。

cluster key 用于通过将数据在物理上聚集在一起来提升查询性能。例如，当你将某一列设置为表的 cluster key 时，表数据将按照你设置的列在物理上进行有序的排列。如果你的大多数查询都按该列进行过滤，这将最大化查询性能。

> **Note:**
>
> 对于字符串列，cluster 统计信息仅使用前 8 个字节。你可以使用 substring 来提供足够的基数。

另请参阅：

* [ALTER CLUSTER KEY](/tidb-cloud-lake/sql/alter-cluster-key.md)
* [DROP CLUSTER KEY](/tidb-cloud-lake/sql/drop-cluster-key.md)

## 语法 {#syntax}

```sql
CREATE TABLE <name> ... CLUSTER BY ( <expr1> [ , <expr2> ... ] )
```

## 示例 {#examples}

以下命令创建按列进行聚集的表：

```sql
CREATE TABLE t1(a int, b int) CLUSTER BY(b,a);

CREATE TABLE t2(a int, b string) CLUSTER BY(SUBSTRING(b, 5, 6));
```
---
title: DROP CLUSTER KEY
summary: 删除表的 cluster key。
---

# DROP CLUSTER KEY

删除表的 cluster key。

另请参阅：[ALTER CLUSTER KEY](/tidb-cloud-lake/sql/alter-cluster-key.md)

## 语法 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <name> DROP CLUSTER KEY
```

## 示例 {#examples}

此命令会删除表 *test* 的 cluster key：

```sql
ALTER TABLE test DROP CLUSTER KEY
```
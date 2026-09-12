---
title: DROP AGGREGATING INDEX
summary: 删除现有的聚合索引。请注意，删除聚合索引并不会移除关联的存储块。若要同时删除这些块，请使用 VACUUM TABLE 命令。若要禁用聚合索引功能，请将 enable_aggregating_index_scan 设置为 0。
---

# DROP AGGREGATING INDEX

删除现有的聚合索引。请注意，删除聚合索引并不会移除关联的存储块。若要同时删除这些块，请使用 [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md) 命令。若要禁用聚合索引功能，请将 `enable_aggregating_index_scan` 设置为 0。

## 语法 {#syntax}

```sql
DROP AGGREGATING INDEX <index_name>
```

## 示例 {#examples}

以下示例删除了一个名为 *my_agg_index* 的聚合索引：

```sql
DROP AGGREGATING INDEX my_agg_index;
```
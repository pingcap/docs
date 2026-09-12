---
title: DROP WAREHOUSE
summary: 删除一个 warehouse，并释放与其关联的资源。
---

# DROP WAREHOUSE

删除一个 warehouse，并释放与其关联的资源。

## 语法 {#syntax}

```sql
DROP WAREHOUSE [ IF EXISTS ] <warehouse_name>
```

| 参数 | 描述 |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IF EXISTS`    | 可选。如果指定了该选项，当计算集群 (Warehouse) 不存在时，命令会静默成功。如果未指定，当计算集群不存在时，命令会失败。 |
| warehouse_name | 要删除的计算集群名称。 |

## 示例 {#examples}

删除一个 warehouse：

```sql
DROP WAREHOUSE my_warehouse;
```

仅当 warehouse 存在时才删除：

```sql
DROP WAREHOUSE IF EXISTS my_warehouse;
```
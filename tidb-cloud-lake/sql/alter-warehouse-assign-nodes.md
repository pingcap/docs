---
title: ALTER WAREHOUSE ASSIGN NODES
summary: "了解如何在 {{{ .lake }}} 中使用 ALTER WAREHOUSE ASSIGN NODES 命令，将节点分配给计算集群中的一个或多个集群。"
---

# ALTER WAREHOUSE ASSIGN NODES

将节点分配给计算集群 (Warehouse) 中的一个或多个集群。

> **注意：**
>
> 此命令需要系统管理支持和企业版许可证。

## 语法 {#syntax}

```sql
ALTER WAREHOUSE <warehouse_name> ASSIGN NODES
(
    ASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name>
    [ , ASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name> , ... ]
)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `<warehouse_name>` | 目标计算集群。 |
| `<node_count>` | 要分配的节点数量。 |
| `FROM '<node_group>'` | 可选的节点组选择器。 |
| `<cluster_name>` | 计算集群内部的目标集群。 |

## 示例 {#example}

```sql
ALTER WAREHOUSE etl_wh ASSIGN NODES
(
    ASSIGN 2 NODES FOR c1,
    ASSIGN 1 NODES FROM 'default' FOR c2
);
```
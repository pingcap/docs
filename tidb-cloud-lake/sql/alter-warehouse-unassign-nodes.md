---
title: ALTER WAREHOUSE UNASSIGN NODES
summary: "了解如何在 {{{ .lake }}} 中使用 ALTER WAREHOUSE UNASSIGN NODES 命令，从计算集群中的一个 warehouse 内的集群移除已分配的节点。"
---

# ALTER WAREHOUSE UNASSIGN NODES

从计算集群 (Warehouse) 中的一个或多个集群移除已分配的节点。

> **注意：**
>
> 此命令需要系统管理支持和企业版许可证。

## 语法 {#syntax}

```sql
ALTER WAREHOUSE <warehouse_name> UNASSIGN NODES
(
    UNASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name>
    [ , UNASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name> , ... ]
)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `<warehouse_name>` | 目标 warehouse。 |
| `<node_count>` | 要移除的节点数量。 |
| `FROM '<node_group>'` | 可选的节点组选择器。 |
| `<cluster_name>` | 计算集群中的目标集群。 |

## 示例 {#example}

```sql
ALTER WAREHOUSE etl_wh UNASSIGN NODES
(
    UNASSIGN 1 NODES FOR c1,
    UNASSIGN 1 NODES FROM 'default' FOR c2
);
```
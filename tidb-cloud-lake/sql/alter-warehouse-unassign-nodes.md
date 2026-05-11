---
title: ALTER WAREHOUSE UNASSIGN NODES
summary: "Learn how to use the ALTER WAREHOUSE UNASSIGN NODES command to remove assigned nodes from clusters in a warehouse in {{{ .lake }}}."
---

# ALTER WAREHOUSE UNASSIGN NODES

Removes assigned nodes from one or more clusters in a warehouse.

> **Note:**
>
> This command requires system management support and an enterprise license.

## Syntax

```sql
ALTER WAREHOUSE <warehouse_name> UNASSIGN NODES
(
    UNASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name>
    [ , UNASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name> , ... ]
)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<warehouse_name>` | The target warehouse. |
| `<node_count>` | Number of nodes to remove. |
| `FROM '<node_group>'` | Optional node group selector. |
| `<cluster_name>` | The target cluster inside the warehouse. |

## Example

```sql
ALTER WAREHOUSE etl_wh UNASSIGN NODES
(
    UNASSIGN 1 NODES FOR c1,
    UNASSIGN 1 NODES FROM 'default' FOR c2
);
```

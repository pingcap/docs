---
title: ALTER WAREHOUSE UNASSIGN NODES
summary: "{{{ .lake }}} の Warehouse 内のクラスターから割り当て済みノードを削除するための ALTER WAREHOUSE UNASSIGN NODES コマンドの使用方法を学びます。"
---

# ALTER WAREHOUSE UNASSIGN NODES

Warehouse 内の 1 つ以上のクラスターから割り当て済みノードを削除します。

> **Note:**
>
> このコマンドには system management support と enterprise license が必要です。

## 構文 {#syntax}

```sql
ALTER WAREHOUSE <warehouse_name> UNASSIGN NODES
(
    UNASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name>
    [ , UNASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name> , ... ]
)
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|-----------|-------------|
| `<warehouse_name>` | 対象の Warehouse。 |
| `<node_count>` | 削除するノード数。 |
| `FROM '<node_group>'` | オプションのノードグループセレクター。 |
| `<cluster_name>` | Warehouse 内の対象クラスター。 |

## 例 {#example}

```sql
ALTER WAREHOUSE etl_wh UNASSIGN NODES
(
    UNASSIGN 1 NODES FOR c1,
    UNASSIGN 1 NODES FROM 'default' FOR c2
);
```
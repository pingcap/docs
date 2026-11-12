---
title: ALTER WAREHOUSE UNASSIGN NODES
summary: "{{{ .lake }}} の Warehouse 内のクラスターから割り当て済みノードを削除するための ALTER WAREHOUSE UNASSIGN NODES コマンドの使い方を学びます。"
---

# ALTER WAREHOUSE UNASSIGN NODES <!--Corresponding EN commit: e193d27f71bd790a28465eacb9c1b5141db672a8-->

Warehouse 内の 1 つ以上のクラスターから、割り当て済みノードを削除します。

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
| `FROM '<node_group>'` | 任意のノードグループセレクター。 |
| `<cluster_name>` | Warehouse 内の対象クラスター。 |

## 例 {#example}

```sql
ALTER WAREHOUSE etl_wh UNASSIGN NODES
(
    UNASSIGN 1 NODES FOR c1,
    UNASSIGN 1 NODES FROM 'default' FOR c2
);
```
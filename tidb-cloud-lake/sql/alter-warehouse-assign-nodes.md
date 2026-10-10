---
title: ALTER WAREHOUSE ASSIGN NODES
summary: " {{{ .lake }}} の Warehouse 内のクラスターにノードを割り当てるための ALTER WAREHOUSE ASSIGN NODES コマンドの使用方法を学びます。"
---

# ALTER WAREHOUSE ASSIGN NODES

Warehouse 内の 1 つ以上のクラスターにノードを割り当てます。

> **Note:**
>
> このコマンドを使用するには、システム管理のサポートとエンタープライズライセンスが必要です。

## 構文 {#syntax}

```sql
ALTER WAREHOUSE <warehouse_name> ASSIGN NODES
(
    ASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name>
    [ , ASSIGN <node_count> NODES [ FROM '<node_group>' ] FOR <cluster_name> , ... ]
)
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|-----------|-------------|
| `<warehouse_name>` | 対象の Warehouse。 |
| `<node_count>` | 割り当てるノード数。 |
| `FROM '<node_group>'` | オプションのノードグループセレクター。 |
| `<cluster_name>` | Warehouse 内の対象クラスター。 |

## 例 {#example}

```sql
ALTER WAREHOUSE etl_wh ASSIGN NODES
(
    ASSIGN 2 NODES FOR c1,
    ASSIGN 1 NODES FROM 'default' FOR c2
);
```
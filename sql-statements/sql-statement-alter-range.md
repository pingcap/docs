---
title: ALTER RANGE
summary: TiDBにおけるALTER RANGEの使用方法の概要。
---

# 範囲変更 {#alter-range}

現在、 `ALTER RANGE`ステートメントは、TiDB の特定の配置ポリシーの範囲を変更する場合にのみ使用できます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

```ebnf+diagram
AlterRangeStmt ::=
    'ALTER' 'RANGE' Identifier PlacementPolicyOption
```

`ALTER RANGE` 、以下の 2 つのパラメータをサポートしています。

-   `global` : クラスター内のすべてのデータの範囲を示します。
-   `meta` : TiDB に格納されている内部メタデータの範囲を示します。

## 例 {#examples}

```sql
CREATE PLACEMENT POLICY `deploy111` CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 1, "+region=us-west-1": 1}';
CREATE PLACEMENT POLICY `five_replicas` FOLLOWERS=4;

ALTER RANGE global PLACEMENT POLICY = "deploy111";
ALTER RANGE meta PLACEMENT POLICY = "five_replicas";
```

上記の例では、2 つの配置ポリシー ( `deploy111`と`five_replicas` ) を作成し、異なる領域の制約を指定した後、 `deploy111`配置ポリシーをクラスタ範囲内のすべてのデータに適用し、 `five_replicas`配置ポリシーをメタデータ範囲に適用しています。

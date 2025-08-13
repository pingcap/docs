---
title: ALTER RANGE
summary: TiDB の ALTER RANGE の使用法の概要。
---

# 範囲の変更 {#alter-range}

現在、 `ALTER RANGE`ステートメントは、TiDB 内の特定の配置ポリシーの範囲を変更するためにのみ使用できます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

```ebnf+diagram
AlterRangeStmt ::=
    'ALTER' 'RANGE' Identifier PlacementPolicyOption
```

`ALTER RANGE`次の 2 つのパラメータをサポートします。

-   `global` : クラスター内のすべてのデータの範囲を示します。
-   `meta` : TiDB に保存されている内部メタデータの範囲を示します。

## 例 {#examples}

```sql
CREATE PLACEMENT POLICY `deploy111` CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 1, "+region=us-west-1": 1}';
CREATE PLACEMENT POLICY `five_replicas` FOLLOWERS=4;

ALTER RANGE global PLACEMENT POLICY = "deploy111";
ALTER RANGE meta PLACEMENT POLICY = "five_replicas";
```

上記の例では、2 つの配置ポリシー ( `deploy111`と`five_replicas` ) を作成し、異なるリージョンの制約を指定してから、配置ポリシー`deploy111`クラスター範囲内のすべてのデータに適用し、配置ポリシー`five_replicas`メタデータ範囲に適用します。

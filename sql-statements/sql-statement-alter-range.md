---
title: ALTER RANGE
summary: An overview of the usage of ALTER RANGE for TiDB.
---

# 範囲を変更する {#alter-range}

現在、 `ALTER RANGE`ステートメントは、TiDB の特定の配置ポリシーの範囲を変更するためにのみ使用できます。

## あらすじ {#synopsis}

```ebnf+diagram
AlterRangeStmt ::=
    'ALTER' 'RANGE' Identifier PlacementPolicyOption
```

`ALTER RANGE`次の 2 つのパラメータをサポートします。

-   `global` : クラスター内のすべてのデータの範囲を示します。
-   `meta` : TiDB に格納される内部メタデータの範囲を示します。

## 例 {#examples}

```sql
CREATE PLACEMENT POLICY `deploy111` CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 1, "+region=us-west-1": 1}';
CREATE PLACEMENT POLICY `five_replicas` FOLLOWERS=4;

ALTER RANGE global PLACEMENT POLICY = "deploy111";
ALTER RANGE meta PLACEMENT POLICY = "five_replicas";
```

前の例では、2 つの配置ポリシー ( `deploy111`および`five_replicas` ) を作成し、さまざまなリージョンの制約を指定してから、 `deploy111`配置ポリシーをクラスター範囲内のすべてのデータに適用し、 `five_replicas`配置ポリシーをメタデータ範囲に適用します。

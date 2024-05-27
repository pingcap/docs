---
title: Eliminate Max/Min
summary: Max/Min関数を排除するためのルールを紹介します。
---

# 最大/最小を排除 {#eliminate-max-min}

SQL 文に`max` `min`関数が含まれている場合、クエリ オプティマイザは`max`最適化ルールを適用して`max` `min`の集計関数を TopN 演算子に変換しようとします。このようにして、TiDB はインデックスを通じてクエリ`min`より効率的に実行できます。

この最適化ルールは`min` `select`ステートメント内の`max`関数の数に応じて次の 2 つのタイプに分けられます。

-   [`max` / `min`関数が1つだけのステートメント](#one-maxmin-function)
-   [複数の`max` / `min`関数を持つステートメント](#multiple-maxmin-functions)

## <code>max</code> / <code>min</code>機能1つ {#one-code-max-code-code-min-code-function}

SQL ステートメントが次の条件を満たす場合、このルールが適用されます。

-   ステートメントには、 `max`または`min`の 1 つの集計関数のみが含まれます。
-   集計関数には関連する`group by`句がありません。

例えば：

```sql
select max(a) from t
```

最適化ルールは、ステートメントを次のように書き換えます。

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

列`a`にインデックスがある場合、または列`a`が複合インデックスのプレフィックスである場合、インデックスの助けを借りて、新しい SQL ステートメントは 1 行のデータのみをスキャンして最大値または最小値を見つけることができます。この最適化により、テーブル全体のスキャンが回避されます。

例のステートメントには次の実行プランがあります。

```sql
mysql> explain select max(a) from t;
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
| id                           | estRows | task      | access object           | operator info                       |
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
| StreamAgg_13                 | 1.00    | root      |                         | funcs:max(test.t.a)->Column#4       |
| └─Limit_17                   | 1.00    | root      |                         | offset:0, count:1                   |
|   └─IndexReader_27           | 1.00    | root      |                         | index:Limit_26                      |
|     └─Limit_26               | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|       └─IndexFullScan_25     | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, desc, stats:pseudo |
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
5 rows in set (0.00 sec)
```

## 複数の<code>max</code> / <code>min</code>関数 {#multiple-code-max-code-code-min-code-functions}

SQL ステートメントが次の条件を満たす場合、このルールが適用されます。

-   ステートメントには複数の集計関数が含まれており、それらはすべて`max`または`min`関数です。
-   集計関数には関連する`group by`句がありません。
-   各`max` `min`の列には、順序を維持するためのインデックスがあります。

例えば：

```sql
select max(a) - min(a) from t
```

最適化ルールは、まず列`a`に順序を保持するためのインデックスがあるかどうかを確認します。ある場合、SQL ステートメントは 2 つのサブクエリの直積として書き換えられます。

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

書き換えにより、オプティマイザは`max`関数を`min`つだけ持つステートメントのルールを 2 つのサブクエリにそれぞれ適用できます。ステートメントは次のように書き換えられます。

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同様に、列`a`順序を保持するインデックスがある場合、最適化された実行では、テーブル全体ではなく 2 行のデータのみがスキャンされます。ただし、列`a`に順序を保持するインデックスがない場合、このルールにより 2 回のフル テーブル スキャンが発生しますが、書き換えが行われない場合は 1 回のフル テーブル スキャンのみが必要です。したがって、このような場合にはこのルールは適用されません。

最終的な実行計画は次のようになります。

```sql
mysql> explain select max(a)-min(a) from t;
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
| id                                 | estRows | task      | access object           | operator info                       |
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
| Projection_17                      | 1.00    | root      |                         | minus(Column#4, Column#5)->Column#6 |
| └─HashJoin_18                      | 1.00    | root      |                         | CARTESIAN inner join                |
|   ├─StreamAgg_45(Build)            | 1.00    | root      |                         | funcs:min(test.t.a)->Column#5       |
|   │ └─Limit_49                     | 1.00    | root      |                         | offset:0, count:1                   |
|   │   └─IndexReader_59             | 1.00    | root      |                         | index:Limit_58                      |
|   │     └─Limit_58                 | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|   │       └─IndexFullScan_57       | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, stats:pseudo       |
|   └─StreamAgg_24(Probe)            | 1.00    | root      |                         | funcs:max(test.t.a)->Column#4       |
|     └─Limit_28                     | 1.00    | root      |                         | offset:0, count:1                   |
|       └─IndexReader_38             | 1.00    | root      |                         | index:Limit_37                      |
|         └─Limit_37                 | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|           └─IndexFullScan_36       | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, desc, stats:pseudo |
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
12 rows in set (0.01 sec)
```

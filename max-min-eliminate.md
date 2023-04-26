---
title: Eliminate Max/Min
summary: Introduce the rules for eliminating Max/Min functions.
---

# 最大/最小を削除 {#eliminate-max-min}

SQL ステートメントに`max`関数が含まれている場合、クエリ オプティマイザーは、 `max` / `min`最適化`min`を適用して、 `max` / `min`集計関数を TopN 演算子に変換しようとします。このようにして、TiDB はインデックスを介してより効率的にクエリを実行できます。

この最適化ルールは、 `select`ステートメントの`max` / `min`関数の数に応じて、次の 2 つのタイプに分けられます。

-   [`max` / <code>min</code>関数が 1 つだけのステートメント](#one-maxmin-function)
-   [複数の`max` / <code>min</code>関数を含むステートメント](#multiple-maxmin-functions)

## 1つの<code>max</code> / <code>min</code>機能 {#one-code-max-code-code-min-code-function}

SQL ステートメントが次の条件を満たす場合、このルールが適用されます。

-   このステートメントには、 `max`または`min`である 1 つの集計関数のみが含まれています。
-   集計関数には、関連する`group by`節がありません。

例えば：

{{< copyable "" >}}

```sql
select max(a) from t
```

最適化ルールは、ステートメントを次のように書き換えます。

{{< copyable "" >}}

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

列`a`にインデックスがある場合、または列`a`が何らかの複合インデックスのプレフィックスである場合、新しい SQL ステートメントはインデックスを使用して、1 行のデータのみをスキャンすることで最大値または最小値を見つけることができます。この最適化により、フル テーブル スキャンが回避されます。

ステートメントの例には、次の実行計画があります。

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

-   ステートメントには複数の集計関数が含まれています。これらはすべて`max`または`min`の関数です。
-   関連する`group by`節を持たない集約関数はありません。
-   各`max` / `min`関数の列には、順序を保持するためのインデックスがあります。

例えば：

{{< copyable "" >}}

```sql
select max(a) - min(a) from t
```

最適化ルールは、最初に列`a`にその順序を維持するためのインデックスがあるかどうかを確認します。はいの場合、SQL ステートメントは 2 つのサブクエリのデカルト積として書き直されます。

{{< copyable "" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

書き換えにより、オプティマイザは`max`関数を`min`つしか持たないステートメントのルールを 2 つのサブクエリにそれぞれ適用できます。その後、ステートメントは次のように書き直されます。

{{< copyable "" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同様に、列`a`にその順序を保持するためのインデックスがある場合、最適化された実行では、テーブル全体ではなく 2 行のデータのみがスキャンされます。ただし、列`a`にその順序を保持するためのインデックスがない場合、このルールでは 2 回のフル テーブル スキャンが行われますが、再書き込みされていない場合、実行に必要なフル テーブル スキャンは 1 回だけです。したがって、そのような場合、この規則は適用されません。

最終的な実行計画は次のとおりです。

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

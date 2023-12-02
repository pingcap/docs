---
title: Eliminate Max/Min
summary: Introduce the rules for eliminating Max/Min functions.
---

# 最大値/最小値の削除 {#eliminate-max-min}

SQL ステートメントに`max` / `min`関数が含まれている場合、クエリ オプティマイザーは`max` / `min`最適化ルールを適用して、 `max` / `min`集計関数をTopN 演算子に変換しようとします。このように、TiDB はインデックスを使用してクエリをより効率的に実行できます。

この最適化ルールは、 `select`ステートメント内の`max` / `min`関数の数に応じて、次の 2 種類に分けられます。

-   [`max` / `min`関数が 1 つだけあるステートメント](#one-maxmin-function)
-   [複数の`max` / `min`関数を含むステートメント](#multiple-maxmin-functions)

## 1つの<code>max</code> / <code>min</code>関数 {#one-code-max-code-code-min-code-function}

SQL ステートメントが次の条件を満たす場合、このルールが適用されます。

-   ステートメントには、集約関数が 1 つだけ ( `max`または`min`含まれています。
-   集計関数には関連する`group by`句がありません。

例えば：

```sql
select max(a) from t
```

最適化ルールはステートメントを次のように書き換えます。

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

列`a`にインデックスがある場合、または列`a`が複合インデックスのプレフィックスである場合、インデックスの助けを借りて、新しい SQL ステートメントは 1 行のデータのみをスキャンすることで最大値または最小値を見つけることができます。この最適化により、テーブル全体のスキャンが回避されます。

ステートメントの例には次の実行プランがあります。

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

-   ステートメントには複数の集計関数が含まれており、それらはすべて`max`または`min`の関数です。
-   どの集約関数にも関連する`group by`句はありません。
-   各`max` / `min`関数の列には、順序を維持するためのインデックスがあります。

例えば：

```sql
select max(a) - min(a) from t
```

最適化ルールはまず、列`a`に順序を維持するためのインデックスがあるかどうかを確認します。 「はい」の場合、SQL ステートメントは 2 つのサブクエリのデカルト積として書き換えられます。

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

書き換えにより、オプティマイザは`max` / `min`関数を 1 つだけ含むステートメントのルールを 2 つのサブクエリにそれぞれ適用できます。このステートメントは次のように書き換えられます。

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同様に、列`a`に順序を保存するインデックスがある場合、最適化された実行ではテーブル全体ではなく 2 行のデータのみがスキャンされます。ただし、列`a`に順序を保持するインデックスがない場合、このルールにより 2 回のテーブル全体のスキャンが行われますが、書き換えられない場合、実行に必要なテーブル全体のスキャンは 1 回だけです。したがって、このような場合には、このルールは適用されません。

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

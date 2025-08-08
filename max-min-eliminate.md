---
title: Eliminate Max/Min
summary: Max/Min関数を排除するための規則を紹介します。
---

# 最大/最小を排除 {#eliminate-max-min}

SQL文に`max` `min`関数が含まれている場合、クエリオプティマイザは`max`最適化ルールを適用して、 `max` / `min`集計関数をTopN演算子に変換しようとします。これにより、TiDBはインデックスを通じてクエリ`min`より効率的に実行できます。

この最適化ルールは`min` `select`ステートメント内の`max`関数の数に応じて次の 2 つのタイプに分けられます。

-   [`max` / `min`関数が1つだけあるステートメント](#one-maxmin-function)
-   [複数の`max` / `min`関数を含むステートメント](#multiple-maxmin-functions)

## 1つの<code>max</code> / <code>min</code>関数 {#one-code-max-code-code-min-code-function}

SQL ステートメントが次の条件を満たす場合、このルールが適用されます。

-   ステートメントには、 `max`または`min`集計関数が 1 つだけ含まれています。
-   集計関数には関連する`group by`節がありません。

例えば：

```sql
select max(a) from t
```

最適化ルールにより、ステートメントは次のように書き換えられます。

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

列`a`インデックスが設定されている場合、または列`a`複合インデックスのプレフィックスになっている場合、インデックスの助けを借りて、新しいSQL文は1行のデータのみをスキャンすることで最大値または最小値を見つけられます。この最適化により、フルテーブルスキャンが回避されます。

この例のステートメントには次の実行プランがあります。

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
-   各`max`関数の列には順序を維持するためのインデックス`min`あります。

例えば：

```sql
select max(a) - min(a) from t
```

最適化ルールはまず、列`a`順序を維持するためのインデックスがあるかどうかを確認します。インデックスがある場合、SQL文は2つのサブクエリの直積として書き換えられます。

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

この書き換えにより、オプティマイザは2つのサブクエリにそれぞれ`max`関数を`min`つだけ含む文のルールを適用できます。その結果、文は次のように書き換えられます。

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同様に、列`a`順序を保持するインデックスがある場合、最適化された実行ではテーブル全体ではなく、2行のデータのみがスキャンされます。しかし、列`a`に順序を保持するインデックスがない場合、このルールではフルテーブルスキャンが2回実行されますが、書き換えが行われない限り、フルテーブルスキャンは1回で済みます。したがって、このような場合にはこのルールは適用されません。

最終的な実行プランは次のようになります。

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

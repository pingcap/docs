---
title: Eliminate Max/Min
summary: Introduce the rules for eliminating Max/Min functions.
---

# 最大/最小を排除する {#eliminate-max-min}

SQLステートメントに`max`関数が含まれている場合、クエリ`min`は`min`最適化ルールを適用して`min`集計関数を`max`演算子に変換しようとし`max` 。このようにして、TiDBはインデックスを介してより効率的にクエリを実行できます。

この最適化ルールは、 `min`ステートメントの`max`関数の数に応じて、次の2 `select`のタイプに分けられます。

-   [`max` / <code>min</code>関数が1つしかないステートメント](#one-maxmin-function)
-   [複数の`max` / <code>min</code>関数を持つステートメント](#multiple-maxmin-functions)

## 1つの<code>max</code> / <code>min</code>関数 {#one-code-max-code-code-min-code-function}

SQLステートメントが次の条件を満たす場合、このルールが適用されます。

-   ステートメントには、 `max`または`min`の1つの集計関数のみが含まれています。
-   集計関数には、関連する`group by`句はありません。

例えば：

{{< copyable "" >}}

```sql
select max(a) from t
```

最適化ルールは、ステートメントを次のように書き直します。

{{< copyable "" >}}

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

列`a`にインデックスがある場合、または列`a`が複合インデックスのプレフィックスである場合、インデックスを使用して、新しいSQLステートメントは1行のデータのみをスキャンすることで最大値または最小値を見つけることができます。この最適化により、全表スキャンが回避されます。

サンプルステートメントには、次の実行プランがあります。

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

## 複数<code>max</code> / <code>min</code>関数 {#multiple-code-max-code-code-min-code-functions}

SQLステートメントが次の条件を満たす場合、このルールが適用されます。

-   ステートメントには、すべて`max`つまたは`min`の関数である複数の集計関数が含まれています。
-   どの集計関数にも関連する`group by`節はありません。
-   各`max`関数の列には、順序を保持するためのインデックスがあり`min` 。

例えば：

{{< copyable "" >}}

```sql
select max(a) - min(a) from t
```

最適化ルールは、最初に列`a`にその順序を保持するためのインデックスがあるかどうかをチェックします。はいの場合、SQLステートメントは2つのサブクエリのデカルト積として書き直されます。

{{< copyable "" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

書き換えにより、オプティマイザは、2つのサブクエリにそれぞれ`min`関数が`max`つしかないステートメントのルールを適用できます。次に、ステートメントは次のように書き直されます。

{{< copyable "" >}}

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同様に、列`a`にその順序を保持するためのインデックスがある場合、最適化された実行は、テーブル全体ではなく、2行のデータのみをスキャンします。ただし、列`a`に順序を保持するためのインデックスがない場合、このルールは2回の全表スキャンになりますが、書き換えがない場合、実行に必要なのは1回の全表スキャンのみです。したがって、このような場合、このルールは適用されません。

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

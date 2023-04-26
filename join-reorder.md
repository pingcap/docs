---
title: Introduction to Join Reorder
summary: Use the Join Reorder algorithm to join multiple tables in TiDB.
---

# 結合したテーブルの再配置の概要 {#introduction-to-join-reorder}

実際のアプリケーション シナリオでは、複数のテーブルを結合するのが一般的です。結合の実行効率は、各テーブルが結合する順序に関連付けられています。

例えば：

{{< copyable "" >}}

```sql
SELECT * FROM t1, t2, t3 WHERE t1.a=t2.a AND t3.a=t2.a;
```

このクエリでは、次の 2 つの順序でテーブルを結合できます。

-   t1 は t2 に参加し、次に t3 に参加します
-   t2 は t3 に参加し、次に t1 に参加します

t1 と t3 はデータ量と分布が異なるため、これら 2 つの実行順序は異なるパフォーマンスを示す可能性があります。

したがって、オプティマイザには結合順序を決定するためのアルゴリズムが必要です。現在、TiDB では次の 2 つの結合したテーブルの再配置アルゴリズムが使用されています。

-   貪欲なアルゴリズム: 結合に参加しているすべてのノードの中で、TiDB は行数が最も少ないテーブルを選択して、他の各テーブルとの結合結果をそれぞれ推定し、結合結果が最小のペアを選択します。その後、TiDB は、すべてのノードが結合を完了するまで、次のラウンドのために他のノードを選択して結合する同様のプロセスを続けます。
-   動的プログラミング アルゴリズム: 結合に参加しているすべてのノード間で、TiDB は可能なすべての結合順序を列挙し、最適な結合順序を選択します。

## 例: 結合したテーブルの再配置の貪欲なアルゴリズム {#example-the-greedy-algorithm-of-join-reorder}

例として、前述の 3 つのテーブル (t1、t2、および t3) を取り上げます。

まず、TiDB は結合操作に参加するすべてのノードを取得し、ノードを行番号の昇順に並べ替えます。

![join-reorder-1](/media/join-reorder-1.png)

その後、行数が最も少ないテーブルが選択され、他の 2 つのテーブルとそれぞれ結合されます。出力結果セットのサイズを比較することにより、TiDB は結果セットが小さいペアを選択します。

![join-reorder-2](/media/join-reorder-2.png)

その後、TiDB は次の選択ラウンドに入ります。 4 つのテーブルを結合しようとすると、TiDB は引き続き出力結果セットのサイズを比較し、結果セットが小さいペアを選択します。

この場合、3 つのテーブルのみが結合されるため、TiDB は最終的な結合結果を取得します。

![join-reorder-3](/media/join-reorder-3.png)

## 例: 結合したテーブルの再配置の動的計画法アルゴリズム {#example-the-dynamic-programming-algorithm-of-join-reorder}

前述の 3 つのテーブル (t1、t2、および t3) を再度例に取ると、動的計画法アルゴリズムはすべての可能性を列挙できます。したがって、 `t1`のテーブル (行数が最も少ないテーブル) から開始する必要がある貪欲なアルゴリズムと比較すると、動的計画法アルゴリズムは次のように結合順序を列挙できます。

![join-reorder-4](/media/join-reorder-4.png)

この選択が欲張りアルゴリズムよりも優れている場合、動的計画法アルゴリズムはより適切な結合順序を選択できます。

すべての可能性が列挙されるため、動的計画法のアルゴリズムはより多くの時間を消費し、統計の影響を受けやすくなります。

## 結合したテーブルの再配置アルゴリズムの選択 {#selection-of-the-join-reorder-algorithms}

TiDB 結合したテーブルの再配置アルゴリズムの選択は、 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold)変数によって制御されます。 結合したテーブルの再配置に参加しているノードの数がこのしきい値よりも多い場合、TiDB は貪欲なアルゴリズムを使用します。それ以外の場合、TiDB は動的計画法アルゴリズムを使用します。

## 結合したテーブルの再配置アルゴリズムの制限 {#limitations-of-join-reorder-algorithms}

現在の結合したテーブルの再配置アルゴリズムには、次の制限があります。

-   結果セットの計算方法によって制限されるため、アルゴリズムは最適な結合順序を選択することを保証できません。
-   結合したテーブルの再配置アルゴリズムの Outer Join のサポートは、 [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)システム変数によって制御されます。
-   現在、動的計画法のアルゴリズムは、外部結合に対して結合したテーブルの再配置を実行できません。

現在、結合順序を強制するために`STRAIGHT_JOIN`構文が TiDB でサポートされています。詳細については、 [構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)を参照してください。

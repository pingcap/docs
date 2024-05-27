---
title: Explain Statements Using Index Merge
summary: TiDB の `EXPLAIN` ステートメントによって返される実行プラン情報について学習します。
---

# インデックスマージを使用したステートメントの説明 {#explain-statements-using-index-merge}

インデックス マージは、TiDB v4.0 で導入されたテーブルへのアクセス方法です。この方法を使用すると、TiDB オプティマイザーはテーブルごとに複数のインデックスを使用し、各インデックスによって返された結果をマージできます。シナリオによっては、この方法によりテーブル全体のスキャンが回避され、クエリの効率が向上します。

TiDB のインデックス マージには、交差型と結合型の 2 種類があります。前者は`AND`式に適用され、後者は`OR`式に適用されます。結合型のインデックス マージは、TiDB v4.0 で実験的機能として導入され、v5.4.0 で GA になりました。交差型は TiDB v6.5.0 で導入され、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントが指定されている場合にのみ使用できます。

## インデックスのマージを有効にする {#enable-index-merge}

v5.4.0 以降の TiDB バージョンでは、インデックス マージはデフォルトで有効になっています。その他の状況で、インデックス マージが有効になっていない場合は、この機能を有効にするために変数[`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)を`ON`に設定する必要があります。

```sql
SET session tidb_enable_index_merge = ON;
```

## 例 {#examples}

```sql
CREATE TABLE t(a int, b int, c int, d int, INDEX idx_a(a), INDEX idx_b(b), INDEX idx_c(c), INDEX idx_d(d));
```

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a = 1 OR b = 1;

+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 19.99    | root      |               | data:Selection_6                     |
| └─Selection_6           | 19.99    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
EXPLAIN SELECT /*+ USE_INDEX_MERGE(t) */ * FROM t WHERE a > 1 OR b > 1;
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_8                  | 5555.56 | root      |                         | type: union                                    |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 5555.56 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

前述のクエリでは、フィルター条件は`OR`コネクターとして使用する`WHERE`句です。インデックス マージを使用しない場合、テーブルごとに 1 つのインデックスしか使用できません。 `a = 1`インデックス`a`にプッシュダウンすることはできません。また、 `b = 1`をインデックス`b`にプッシュダウンすることもできません。 `t`に大量のデータが存在する場合、フル テーブル スキャンは非効率的です。このようなシナリオに対処するために、TiDB ではテーブルにアクセスするためのインデックス マージが導入されています。

上記のクエリでは、オプティマイザはテーブルにアクセスするためにユニオンタイプのインデックス マージを選択します。インデックス マージにより、オプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスによって返された結果をマージして、上記の出力の後者の実行プランを生成できます。

出力では、 `IndexMerge_8`演算子の`operator info` `type: union`情報は、この演算子がユニオン型インデックス マージであることを示しています。3 つの子ノードがあります`IndexRangeScan_5`と`IndexRangeScan_6` 、範囲に従って条件を満たす`RowID`をスキャンし、次に`TableRowIDScan_7`演算子は、これらの`RowID`に従って条件を満たすすべてのデータを正確に読み取ります。

`IndexRangeScan` / `TableRangeScan`などの特定のデータ範囲に対して実行されるスキャン操作の場合、結果の`operator info`列には、 `IndexFullScan` / `TableFullScan`などの他のスキャン操作と比較して、スキャン範囲に関する追加情報が含まれます。上記の例では、 `IndexRangeScan_5`演算子の`range:(1,+inf]` 、演算子が 1 から正の無限大までデータをスキャンすることを示します。

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- Does not use index merge

+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                             | estRows | task      | access object           | operator info                               |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_19                 | 1.11    | root      |                         |                                             |
| ├─IndexRangeScan_16(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo |
| └─Selection_18(Probe)          | 1.11    | cop[tikv] |                         | gt(test.t.a, 1), gt(test.t.b, 1)            |
|   └─TableRowIDScan_17          | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+

EXPLAIN SELECT /*+ USE_INDEX_MERGE(t, idx_a, idx_b, idx_c) */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- Uses index merge
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_9                  | 1.11    | root      |                         | type: intersection                             |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo    |
| └─TableRowIDScan_8(Probe)     | 1.11    | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

前述の例から、フィルター条件は`AND`コネクタとして使用する`WHERE`句であることがわかります。インデックス マージが有効になる前は、オプティマイザーは 3 つのインデックス ( `idx_a` 、 `idx_b` 、または`idx_c` ) のうち 1 つしか選択できません。

フィルタ条件の選択性が低い場合、オプティマイザは対応するインデックスを直接選択して、理想的な実行効率を実現します。ただし、データ分布が次の 3 つの条件をすべて満たす場合は、交差型インデックス マージの使用を検討できます。

-   テーブル全体のデータサイズが大きく、テーブル全体を直接読み取るのは非効率的です。
-   3 つのフィルタ条件のそれぞれについて、それぞれの選択性は非常に高いため、単一のインデックスを使用する`IndexLookUp`の実行効率は理想的ではありません。
-   3 つのフィルター条件の全体的な選択性は低いです。

交差型インデックス マージを使用してテーブルにアクセスする場合、オプティマイザはテーブルで複数のインデックスを使用することを選択し、各インデックスによって返された結果をマージして、前の例の出力の`IndexMerge`後ろの実行プランを生成します`IndexMerge_9`の`operator info`演算子の`type: intersection`情報は、この演算子が交差型インデックス マージであることを示しています。実行プランのその他の部分は、前のユニオン型インデックス マージの例と同様です。

> **注記：**
>
> -   インデックスマージ機能は、v5.4.0 からデフォルトで有効になっています。つまり、 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)は`ON`です。
>
> -   SQL ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用すると、 `tidb_enable_index_merge`の設定に関係なく、オプティマイザにインデックス マージを強制的に適用させることができます。フィルタリング条件にプッシュダウンできない式が含まれている場合にインデックス マージを有効にするには、SQL ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用する必要があります。
>
> -   オプティマイザがクエリ プランに単一インデックス スキャン メソッド (フル テーブル スキャン以外) を選択できる場合、オプティマイザはインデックス マージを自動的に使用しません。オプティマイザがインデックス マージを使用するには、オプティマイザ ヒントを使用する必要があります。v8.1.0 以降では、 [オプティマイザー修正コントロール 52869](/optimizer-fix-controls.md#52869-new-in-v810)設定することでこの制限を解除できます。この制限を解除すると、オプティマイザはより多くのクエリでインデックス マージを自動的に選択できるようになりますが、オプティマイザが最適な実行プランを無視する可能性があります。したがって、この制限を解除する前に、実際の使用ケースで十分なテストを実施して、パフォーマンスの低下が発生しないことを確認することをお勧めします。
>
> -   インデックスマージは現時点では[一時テーブル](/temporary-tables.md)ではサポートされていません。
>
> -   交差型インデックス マージは、オプティマイザによって自動的に選択されません。選択されるようにするには、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントを使用して**テーブル名とインデックス名**を指定する必要があります。

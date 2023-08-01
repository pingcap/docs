---
title: Explain Statements Using Index Merge
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# インデックス マージを使用した Explain ステートメント {#explain-statements-using-index-merge}

インデックス マージは、テーブルにアクセスするために TiDB v4.0 で導入された方法です。この方法を使用すると、TiDB オプティマイザーはテーブルごとに複数のインデックスを使用し、各インデックスから返された結果をマージできます。一部のシナリオでは、この方法によりテーブル全体のスキャンが回避され、クエリがより効率的になります。

TiDB のインデックスマージには、交差型と共用型の 2 種類があります。前者は`AND`式に適用され、後者は`OR`式に適用されます。 Union タイプのインデックス マージは、実験的機能として TiDB v4.0 に導入され、v5.4.0 で GA になりました。交差タイプは TiDB v6.5.0 で導入され、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントが指定されている場合にのみ使用できます。

## インデックスのマージを有効にする {#enable-index-merge}

v5.4.0 以降の TiDB バージョンでは、インデックスのマージがデフォルトで有効になっています。その他の状況で、インデックスのマージが有効になっていない場合は、変数[`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)から`ON`を設定してこの機能を有効にする必要があります。

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

前述のクエリでは、フィルター条件は、コネクタとして`OR`を使用する`WHERE`句です。インデックスのマージを使用しない場合、テーブルごとに使用できるインデックスは 1 つだけです。 `a = 1`インデックス`a`にプッシュダウンすることはできません。 `b = 1`インデックス`b`にプッシュダウンすることもできません。 `t`に大量のデータが存在する場合、フル テーブル スキャンは非効率的です。このようなシナリオに対処するために、テーブルにアクセスするためにインデックス マージが TiDB に導入されました。

前述のクエリの場合、オプティマイザはテーブルにアクセスするために共用体タイプのインデックス マージを選択します。インデックスのマージにより、オプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスから返された結果をマージし、前の出力で後の実行プランを生成できます。

出力では、 `IndexMerge_8`演算子のうち`operator info`の`type: union`情報は、この演算子が共用体タイプのインデックス マージであることを示しています。 3 つの子ノードがあります。 `IndexRangeScan_5`と`IndexRangeScan_6`範囲に従って条件を満たす`RowID`秒をスキャンし、 `TableRowIDScan_7`オペレーターはこれら`RowID`秒に従って条件を満たすすべてのデータを正確に読み取ります。

`IndexRangeScan` / `TableRangeScan`などの特定のデータ範囲に対して実行されるスキャン操作の場合、結果の`operator info`列には、 `IndexFullScan` / `TableFullScan`などの他のスキャン操作と比較して、スキャン範囲に関する追加情報が含まれます。上記の例では、 `IndexRangeScan_13`演算子の`range:(1,+inf]` 、演算子が 1 から正の無限大までデータをスキャンすることを示します。

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

前の例から、フィルター条件は`AND`コネクタとして使用する`WHERE`句であることがわかります。インデックスのマージが有効になる前は、オプティマイザは 3 つのインデックス ( `idx_a` 、 `idx_b` 、または`idx_c` ) の 1 つだけを選択できます。

いずれかのフィルター条件の選択性が低い場合、オプティマイザーは対応するインデックスを直接選択して、理想的な実行効率を実現します。ただし、データ分布が次の 3 つの条件をすべて満たす場合は、交差型インデックス マージの使用を検討できます。

-   テーブル全体のデータサイズは大きく、テーブル全体を直接読み込むのは非効率です。
-   3 つのフィルター条件のそれぞれについて、それぞれの選択性が非常に高いため、単一のインデックスを使用した`IndexLookUp`の実行効率は理想的ではありません。
-   3 つのフィルター条件の全体的な選択性は低くなります。

交差タイプのインデックス マージを使用してテーブルにアクセスする場合、オプティマイザはテーブルで複数のインデックスを使用することを選択し、各インデックスから返された結果をマージして、前の出力例の後半`IndexMerge`の実行プランを生成できます。 `operator info` of `IndexMerge_9`演算子の`type: intersection`情報は、この演算子が交差タイプのインデックス マージであることを示します。実行プランの他の部分は、前述の共用体タイプのインデックスのマージの例と似ています。

> **ノート：**
>
> -   インデックス マージ機能は、v5.4.0 からデフォルトで有効になっています。つまり、 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)は`ON`です。
>
> -   SQL ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)使用すると、 `tidb_enable_index_merge`の設定に関係なく、オプティマイザにインデックス マージを強制的に適用できます。フィルター条件にプッシュダウンできない式が含まれている場合にインデックス マージを有効にするには、SQL ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用する必要があります。
>
> -   オプティマイザがクエリ プランに対して単一インデックス スキャン方法 (フル テーブル スキャン以外) を選択できる場合、オプティマイザは自動的にインデックス マージを使用しません。オプティマイザーがインデックスのマージを使用するには、オプティマイザー ヒントを使用する必要があります。
>
> -   現時点では、インデックス マージは[一時配列テーブル](/temporary-tables.md)ではサポートされていません。
>
> -   交差タイプのインデックス マージは、オプティマイザによって自動的に選択されません。テーブル名とインデックス名を選択するには、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントを使用して**テーブル名とインデックス名を**指定する必要があります。

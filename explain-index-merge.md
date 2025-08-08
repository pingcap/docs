---
title: Explain Statements Using Index Merge
summary: TiDB の EXPLAIN` ステートメントによって返される実行プラン情報について学習します。
---

# インデックスマージを使用したステートメントの説明 {#explain-statements-using-index-merge}

インデックスマージは、TiDB v4.0で導入されたテーブルアクセス手法です。この手法により、TiDBオプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスから返される結果をマージすることができます。場合によっては、この手法によってテーブル全体のスキャンが回避され、クエリの効率が向上します。

TiDBのインデックスマージには、交差型と結合型の2種類があります。前者は`AND`式に適用され、後者は`OR`番目の式に適用されます。結合型のインデックスマージは、TiDB v4.0で実験的機能として導入され、v5.4.0でGAとなりました。交差型はTiDB v6.5.0で導入され、 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)ヒントが指定された場合にのみ使用できます。

## インデックスのマージを有効にする {#enable-index-merge}

TiDBバージョンv5.4.0以降では、インデックスマージはデフォルトで有効になっています。それ以外の状況でインデックスマージが有効になっていない場合は、変数[`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)を`ON`に設定してこの機能を有効にする必要があります。

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

上記のクエリでは、フィルター条件は`OR`コネクターとして使用する`WHERE`句です。インデックスマージがない場合、テーブルごとに1つのインデックスしか使用できません。 `a = 1`インデックス`a`にプッシュダウンすることはできません。同様に、 `b = 1`インデックス`b`にプッシュダウンすることもできません。 `t`に膨大な量のデータが存在する場合、フルテーブルスキャンは非効率的です。このようなシナリオに対処するために、TiDBではテーブルへのアクセスにインデックスマージが導入されています。

上記のクエリでは、オプティマイザはテーブルにアクセスするためにユニオン型のインデックスマージを選択します。インデックスマージにより、オプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスから返された結果をマージして、上記の出力の後者の実行プランを生成することができます。

出力において、 `IndexMerge_8`演算子の`operator info`の`type: union`情報は、この演算子がユニオン型インデックスマージであることを示しています。この演算子には3つの子ノードがあります。7と`IndexRangeScan_6` `IndexRangeScan_5`範囲に従って条件を満たす`RowID`をスキャンし、その後、 `TableRowIDScan_7`演算子はこれらの`RowID`に基づいて条件を満たすすべてのデータを正確に読み取ります。

`IndexRangeScan` / `TableRangeScan`ように特定のデータ範囲に対して実行されるスキャン演算の場合、結果の`operator info`列には、 `IndexFullScan` / `TableFullScan`のような他のスキャン演算と比較して、スキャン範囲に関する追加情報が含まれます。上記の例では、 `IndexRangeScan_5`演算子の`range:(1,+inf]` 、演算子が 1 から正の無限大までデータをスキャンすることを示しています。

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

上の例から、フィルター条件は`AND`コネクタとして使用する`WHERE`句であることがわかります。インデックスマージが有効になる前は、オプティマイザーは3つのインデックス（ `idx_a` 、 `idx_b` 、または`idx_c` ）のうち1つしか選択できません。

フィルタ条件のいずれかの選択性が低い場合、オプティマイザは対応するインデックスを直接選択し、理想的な実行効率を実現します。ただし、データ分布が以下の3つの条件をすべて満たす場合は、交差型インデックスマージの使用を検討できます。

-   テーブル全体のデータサイズが大きく、テーブル全体を直接読み取るのは非効率的です。
-   3 つのフィルタ条件のそれぞれについて、それぞれの選択性は非常に高いため、単一のインデックスを使用した`IndexLookUp`の実行効率は理想的ではありません。
-   3 つのフィルター条件の全体的な選択性は低いです。

交差型インデックスマージを使用してテーブルにアクセスする場合、オプティマイザはテーブルに対して複数のインデックスを使用し、各インデックスから返される結果をマージして、前述の出力例の`IndexMerge`の実行プランを生成することができます。7 `IndexMerge_9`の演算子の`operator info`の情報`type: intersection`は、この演算子が交差型インデックスマージであることを示しています。実行プランのその他の部分は、前述のユニオン型インデックスマージの例と同様です。

> **注記：**
>
> -   インデックスマージ機能はv5.4.0からデフォルトで有効になっています。つまり、 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)は`ON`なります。
>
> -   SQLヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)使用すると、 `tidb_enable_index_merge`設定に関係なく、オプティマイザにインデックスマージを強制的に適用させることができます。フィルタリング条件にプッシュダウンできない式が含まれている場合にインデックスマージを有効にするには、SQLヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)使用する必要があります。
>
> -   オプティマイザがクエリプランに対して単一インデックススキャン方式（フルテーブルスキャン以外）を選択できる場合、オプティマイザはインデックスマージを自動的には使用しません。オプティマイザがインデックスマージを使用するには、オプティマイザヒントを使用する必要があります。v8.1.0以降では、 [オプティマイザー修正制御 52869](/optimizer-fix-controls.md#52869-new-in-v810)設定することでこの制限を解除できます。この制限を解除すると、オプティマイザはより多くのクエリでインデックスマージを自動的に選択できるようになりますが、最適な実行プランを無視してしまう可能性があります。したがって、この制限を解除する前に、実際のユースケースで十分なテストを実施し、パフォーマンスの低下が発生しないことを確認することをお勧めします。
>
> -   現時点では、インデックスマージは[一時テーブル](/temporary-tables.md)ではサポートされていません。
>
> -   交差型インデックスのマージは、オプティマイザによって自動的に選択されません。選択されるには、ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用して**テーブル名とインデックス名**を指定する必要があります。

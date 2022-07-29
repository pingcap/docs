---
title: Explain Statements Using Index Merge
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# インデックスマージを使用してステートメントを説明する {#explain-statements-using-index-merge}

`IndexMerge`は、テーブルにアクセスするためにTiDBv4.0で導入されたメソッドです。このメソッドを使用すると、TiDBオプティマイザーはテーブルごとに複数のインデックスを使用し、各インデックスによって返された結果をマージできます。一部のシナリオでは、このメソッドは全表スキャンを回避することでクエリをより効率的にします。

```sql
mysql> EXPLAIN SELECT * from t where a = 1 or b = 1;
+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 8000.00  | root      |               | data:Selection_6                     |
| └─Selection_6           | 8000.00  | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
mysql> set @@tidb_enable_index_merge = 1;
mysql> explain select * from t use index(idx_a, idx_b) where a > 1 or b > 1;
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                             | estRows | task      | access object           | operator info                                  |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_16                  | 6666.67 | root      |                         |                                                |
| ├─IndexRangeScan_13(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_14(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_15(Probe)     | 6666.67 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+--------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

上記のクエリでは、フィルタ条件は`OR`をコネクタとして使用する`WHERE`句です。 `IndexMerge`がないと、テーブルごとに1つのインデックスしか使用できません。 `a = 1`をインデックス`a`にプッシュダウンすることはできません。どちらもインデックス`b = 1`にプッシュダウンすることはできませ`b` 。 `t`に大量のデータが存在する場合、全表スキャンは非効率的です。このようなシナリオを処理するために、テーブルにアクセスするために`IndexMerge`がTiDBに導入されています。

`IndexMerge`を使用すると、オプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスによって返された結果をマージして、上の図の後者`IndexMerge`の実行プランを生成できます。ここで、 `IndexMerge_16`オペレーターには3つの子ノードがあり、そのうち`IndexRangeScan_13`と`IndexRangeScan_14`は、範囲スキャンの結果に基づいて条件を満たす`RowID`をすべて取得し、 `TableRowIDScan_15`オペレーターは、これらの`RowID`に従って条件を満たすすべてのデータを正確に読み取ります。 。

`IndexRangeScan`などの特定の範囲のデータに対して実行されるスキャン操作の場合、結果の`TableRangeScan`列には、 `operator info` / `IndexFullScan`などの他のスキャン操作と比較したスキャン範囲に関する追加情報が含まれ`TableFullScan` 。上記の例では、 `IndexRangeScan_13`演算子の`range:(1,+inf]`は、演算子が1から正の無限大までデータをスキャンすることを示しています。

> **ノート：**
>
> -   インデックスマージ機能は、v5.4.0からデフォルトで有効になっています。つまり、 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)は`ON`です。
>
> -   SQLヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用すると、 `tidb_enable_index_merge`の設定に関係なく、オプティマイザにインデックスマージを適用させることができます。フィルタリング条件にプッシュダウンできない式が含まれている場合にインデックスマージを有効にするには、SQLヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用する必要があります。
>
> -   インデックスマージは、選言標準形（ `or`で接続された式）のみをサポートし、連言標準形（ `and`で接続された式）をサポートしません。
>
> -   インデックスマージは、現時点では[tempoarayテーブル](/temporary-tables.md)ではサポートされていません。

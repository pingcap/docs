---
title: Explain Statements Using Index Merge
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# インデックス マージを使用したステートメントの説明 {#explain-statements-using-index-merge}

`IndexMerge`は、テーブルにアクセスするために TiDB v4.0 で導入された方法です。この方法を使用すると、TiDB オプティマイザーはテーブルごとに複数のインデックスを使用し、各インデックスから返された結果をマージできます。一部のシナリオでは、この方法を使用すると、テーブル全体のスキャンが回避されるため、クエリがより効率的になります。

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

上記のクエリでは、フィルター条件は`OR`を結合子として使用する`WHERE`句です。 `IndexMerge`がない場合、テーブルごとに 1 つのインデックスしか使用できません。 `a = 1`をインデックス`a`にプッシュダウンすることはできません。どちらも`b = 1`をインデックス`b`にプッシュすることはできません。 `t`に大量のデータが存在する場合、全表スキャンは非効率的です。このようなシナリオを処理するために、テーブルにアクセスするために`IndexMerge`が TiDB に導入されました。

`IndexMerge`を指定すると、オプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスによって返された結果をマージして、上の図の後者`IndexMerge`の実行計画を生成できます。ここで、 `IndexMerge_16`演算子は 3 つの子ノードを持ち、そのうち`IndexRangeScan_13`と`IndexRangeScan_14`は範囲スキャンの結果に基づいて条件を満たすすべての`RowID`を取得し、 `TableRowIDScan_15`演算子はこれらの`RowID`に従って条件を満たすすべてのデータを正確に読み取ります。 .

`IndexRangeScan` / `TableRangeScan`などの特定の範囲のデータに対して実行されるスキャン操作の場合、結果の`operator info`列には、 `IndexFullScan` / `TableFullScan`などの他のスキャン操作と比較して、スキャン範囲に関する追加情報が含まれます。上記の例では、 `IndexRangeScan_13`演算子の`range:(1,+inf]`は、演算子が 1 から正の無限大までデータをスキャンすることを示します。

> **ノート：**
>
> -   インデックス マージ機能は、v5.4.0 からデフォルトで有効になっています。つまり、 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)は`ON`です。
>
> -   `tidb_enable_index_merge`の設定に関係なく、SQL ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用して、オプティマイザーにインデックス マージを強制的に適用させることができます。フィルター条件にプッシュ ダウンできない式が含まれている場合にインデックス マージを有効にするには、SQL ヒント[`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用する必要があります。
>
> -   インデックス マージは、論理和正規形 ( `or`で接続された式) のみをサポートし、論理和正規形 ( `and`で接続された式) はサポートしません。
>
> -   現時点では、インデックス マージは[一時テーブル](/temporary-tables.md)ではサポートされていません。

---
title: Index Selection
summary: TiDBクエリ最適化に最適なインデックスを選択してください。
---

# インデックス選択 {#index-selection}

ストレージエンジンからのデータ読み込みは、SQL実行において最も時間のかかるステップの一つです。現在、TiDBは様々なストレージエンジンとインデックスからのデータ読み込みをサポートしています。クエリ実行のパフォーマンスは、適切なインデックスを選択できるかどうかに大きく左右されます。

このドキュメントでは、テーブルにアクセスするためのインデックスの選択方法と、インデックス選択を制御するための関連方法について説明します。

## アクセステーブル {#access-tables}

インデックス選択を導入する前に、TiDBがテーブルにアクセスする方法、それぞれのアクセス方法がどのような場合にトリガーされるのか、それぞれの方法によってどのような違いが生じるのか、そしてそれぞれのメリットとデメリットは何なのかを理解することが重要です。

### テーブルにアクセスするための演算子 {#operators-for-accessing-tables}

| オペレーター                   | トリガー条件                                          | 適用可能なシナリオ                                           | 説明                                                                                                                                                               |
| :----------------------- | :---------------------------------------------- | :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PointGet / BatchPointGet | 1つ以上の単一ポイント範囲内のテーブルにアクセスする場合。                   | どのようなシナリオでも                                         | トリガーされた場合、通常は最も高速な演算子と考えられています。これは、コプロセッサインターフェースを呼び出すのではなく、kvgetインターフェースを直接呼び出して計算を実行するためです。                                                                    |
| TableReader                 | なし                                              | どのようなシナリオでも                                         | この TableReader オペレーターは TiKV 用です。一般的に、TiKVレイヤーからテーブルデータを直接スキャンするオペレーターの中で最も効率が悪いと考えられています。 `_tidb_rowid`列に範囲クエリがある場合、またはテーブルにアクセスするための他のオペレーターが選択できない場合にのみ選択できます。 |
| TableReader                 | テーブルはTiFlashノード上に複製されます。                        | 読み込む列の数は少ないが、評価する行の数は多い。                            | この TableReader 演算子はTiFlash用です。TiFlashは列ベースのストレージです。列数が少なく行数が多い場合、この演算子を選択することをお勧めします。                                                                          |
| IndexReader               | テーブルには1つ以上のインデックスがあり、計算に必要な列はインデックスに含まれています。    | インデックスに対してより狭い範囲のクエリを実行する場合、またはインデックス付き列に順序要件がある場合。 | 複数の指標が存在する場合は、コスト見積もりに基づいて適切な指標が選択されます。                                                                                                                          |
| IndexLookupReader        | テーブルには1つ以上のインデックスがあり、計算に必要な列がインデックスに完全に含まれていない。 | IndexReaderと同じです。                                   | インデックスは計算列を完全にカバーしていないため、TiDBはインデックスを読み取った後にテーブルから行を取得する必要があります。これはIndexReaderオペレーターと比較して追加のコストがかかります。                                                           |
| IndexMerge                | テーブルには複数のインデックス、または複数値インデックスが存在する。              | 複数値インデックスまたは複数のインデックスが使用される場合。                      | 演算子を使用するには、[オプティマイザのヒント](/optimizer-hints.md)を指定するか、コスト見積もりに基づいてオプティマイザにこの演算子を自動的に選択させることができます。詳細については、[インデックスマージを使用した説明文](/explain-index-merge.md)を参照してください。 |

> **注記：**
>
> TableReader演算子は`_tidb_rowid`列インデックスに基づいており、 TiFlashは列ストレージインデックスを使用するため、インデックスの選択はテーブルにアクセスするための演算子の選択となります。

## インデックス選択ルール {#index-selection-rules}

TiDBは、ルールまたはコストに基づいてインデックスを選択します。ルールには、事前ルールとスカイラインプルーニングが含まれます。インデックスを選択する際、TiDBはまず事前ルールを試します。インデックスが事前ルールを満たす場合、TiDBはそのインデックスを直接選択します。そうでない場合は、TiDBはスカイラインプルーニングを使用して不適切なインデックスを除外し、テーブルにアクセスする各オペレータのコスト見積もりに基づいて、コストが最も低いインデックスを選択します。

### ルールに基づく選択 {#rule-based-selection}

#### 事前ルール {#pre-rules}

TiDBは、インデックスを選択するために以下のヒューリスティックな事前ルールを使用します。

-   ルール 1: インデックスが「完全一致の一意インデックス + テーブルから行を取得する必要がない（つまり、インデックスによって生成されるプランが IndexReader オペレーターである）」という条件を満たす場合、TiDB はこのインデックスを直接選択します。

-   ルール 2: インデックスが「完全一致の一意インデックス + テーブルから行を取得する必要性（つまり、インデックスによって生成されるプランが IndexLookupReader オペレーターである）」を満たす場合、TiDB はテーブルから取得する行数が最も少ないインデックスを候補インデックスとして選択します。

-   ルール 3: インデックスが「通常のインデックス + テーブルから行を取得する必要がない + 読み取る行数が特定のしきい値の値より少ない」という条件を満たす場合、TiDB は読み取る行数が最も少ないインデックスを候補インデックスとして選択します。

-   ルール4：ルール2とルール3に基づいて候補インデックスが1つだけ選択された場合は、その候補インデックスを選択します。ルール2とルール3に基づいてそれぞれ2つの候補インデックスが選択された場合は、読み込む行数が少ない方のインデックスを選択します（インデックスを持つ行数＋テーブルから取得する行数）。

上記のルールにおける「完全一致のインデックス」とは、インデックス付けされた各列が等しい条件を満たすことを意味します。 `EXPLAIN FORMAT = 'verbose' ...`ステートメントを実行する際に、事前ルールがインデックスに一致する場合、TiDB はインデックスが事前ルールに一致することを示す NOTE レベルの警告を出力します。

次の例では、インデックス`idx_b`ルール 2 の条件「完全一致の一意インデックス + テーブルから行を取得する必要性」を満たしているため、TiDB はインデックス`idx_b`をアクセス パスとして選択し、 `SHOW WARNING`インデックス`idx_b`が事前ルールに一致することを示すメモを返します。

```sql
mysql> CREATE TABLE t(a INT PRIMARY KEY, b INT, c INT, UNIQUE INDEX idx_b(b));
Query OK, 0 rows affected (0.01 sec)

mysql> EXPLAIN FORMAT = 'verbose' SELECT b, c FROM t WHERE b = 3 OR b = 6;
+-------------------+---------+---------+------+-------------------------+------------------------------+
| id                | estRows | estCost | task | access object           | operator info                |
+-------------------+---------+---------+------+-------------------------+------------------------------+
| Batch_Point_Get_5 | 2.00    | 8.80    | root | table:t, index:idx_b(b) | keep order:false, desc:false |
+-------------------+---------+---------+------+-------------------------+------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+-------+------+-------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                   |
+-------+------+-------------------------------------------------------------------------------------------+
| Note  | 1105 | unique index idx_b of t is selected since the path only has point ranges with double scan |
+-------+------+-------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### スカイライン剪定 {#skyline-pruning}

スカイライン剪定は、インデックスに対するヒューリスティックなフィルタリングルールであり、誤った推定によるインデックス選択の誤りの可能性を低減できます。インデックスを評価するには、以下の次元が必要です。

-   インデックス付き列によってカバーされるアクセス条件の数はいくつでしょうか。「アクセス条件」とは、列範囲に変換できるWHERE句の条件のことです。インデックス付き列セットがカバーするアクセス条件が多いほど、この点において優れています。

-   テーブルにアクセスするためにインデックスを選択した場合に、テーブルから行を取得する必要があるかどうか（つまり、インデックスによって生成されるプランが IndexReader オペレーターまたは IndexLookupReader オペレーターであるかどうか）。テーブルから行を取得しないインデックスは、取得するインデックスよりもこの点で優れています。両方のインデックスが TiDB を使用してテーブルから行を取得する必要がある場合は、インデックス付き列によってカバーされるフィルタリング条件の数を比較します。フィルタリング条件とは、インデックスに基づいて判断できる`where`条件のことです。インデックスの列セットがより多くのアクセス条件をカバーするほど、テーブルから取得される行の数は少なくなり、この点でインデックスの性能が向上します。

-   インデックスが特定の順序を満たすかどうかを選択します。インデックスの読み取りでは特定の列セットの順序が保証されるため、クエリの順序を満たすインデックスは、この次元で満たさないインデックスよりも優れています。

-   インデックスが[グローバルインデックス](/global-indexes.md)かどうか。パーティション テーブルでは、グローバル インデックスにより、通常のインデックスと比較して SQL の cop タスクの数が効果的に削減され、全体的なパフォーマンスが向上します。

上記次元において、インデックス`idx_a`が 3 つの次元すべてにおいてインデックス`idx_b`と同等以上のパフォーマンスを発揮し、かつ 1 つの次元において`idx_b`よりも優れたパフォーマンスを発揮する場合、 `idx_a`が優先されます。 `EXPLAIN FORMAT = 'verbose' ...`ステートメントを実行する際に、スカイラインプルーニングによって一部のインデックスが除外された場合、TiDB は、スカイラインプルーニングによる除外後に残ったインデックスを一覧表示する NOTE レベルの警告を出力します。

次の例では、インデックス`idx_b`と`idx_e`はどちらも`idx_b_c`より劣るため、スカイライン剪定によって除外されます。 `SHOW WARNING`の戻り値には、スカイライン剪定後に残ったインデックスが表示されます。

```sql
mysql> CREATE TABLE t(a INT PRIMARY KEY, b INT, c INT, d INT, e INT, INDEX idx_b(b), INDEX idx_b_c(b, c), INDEX idx_e(e));
Query OK, 0 rows affected (0.01 sec)

mysql> EXPLAIN FORMAT = 'verbose' SELECT * FROM t WHERE b = 2 AND c > 4;
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
| id                            | estRows | estCost | task      | access object                | operator info                                      |
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
| IndexLookUp_10                | 33.33   | 738.29  | root      |                              |                                                    |
| ├─IndexRangeScan_8(Build)     | 33.33   | 2370.00 | cop[tikv] | table:t, index:idx_b_c(b, c) | range:(2 4,2 +inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 33.33   | 2370.00 | cop[tikv] | table:t                      | keep order:false, stats:pseudo                     |
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
3 rows in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+-------+------+------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                  |
+-------+------+------------------------------------------------------------------------------------------+
| Note  | 1105 | [t,idx_b_c] remain after pruning paths for t given Prop{SortItems: [], TaskTp: rootTask} |
+-------+------+------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### コスト見積もりに基づく選定 {#cost-estimation-based-selection}

スカイライン剪定ルールを使用して不適切なインデックスを除外した後、インデックスの選択は完全にコスト見積もりに基づいて行われます。テーブルへのアクセスにかかるコスト見積もりには、以下の点を考慮する必要があります。

-   ストレージエンジン内のインデックス付きデータの各行の平均長。
-   インデックスによって生成されたクエリ範囲内の行数。
-   テーブルから行を取得するのにかかるコスト。
-   クエリ実行中にインデックスによって生成される範囲の数。

これらの要素とコストモデルに基づいて、オプティマイザはテーブルにアクセスするためのコストが最も低いインデックスを選択します。

#### コスト見積もりに基づく選択における一般的なチューニングの問題 {#common-tuning-problems-with-cost-estimation-based-selection}

1.  推定行数は正確ではありませんか？

    これは通常、統計情報が古いか不正確であることが原因です。 `ANALYZE TABLE`ステートメントを再実行するか、 `ANALYZE TABLE`のパラメータを変更してください。

2.  統計は正確で、 TiFlashからの読み取りは高速ですが、なぜオプティマイザはTiKVからの読み取りを選択するのでしょうか？

    現状では、 TiFlashとTiKV [`tidb_opt_seek_factor`](/system-variables.md#tidb_opt_seek_factor)区別するためのコストモデルはまだ粗雑です。tidb_opt_seek_factorパラメータの値を小さくすると、オプティマイザはTiFlashを選択するようになります。

3.  統計情報は正確です。インデックスAはテーブルから行を取得する必要がありますが、実際にはテーブルから行を取得しないインデックスBよりも高速に実行されます。オプティマイザはなぜインデックスBを選択するのでしょうか？

    この場合、テーブルから行を取得する際のコスト見積もりが大きすぎる可能性があります。tidb_opt_network_factor パラメータの値を小さくすることで[`tidb_opt_network_factor`](/system-variables.md#tidb_opt_network_factor)テーブルから行を取得する際のコストを削減できます。

## 制御インデックスの選択 {#control-index-selection}

インデックスの選択は[オプティマイザのヒント](/optimizer-hints.md)を介して単一のクエリで制御できます。

-   `USE_INDEX` / `IGNORE_INDEX`オプティマイザに特定のインデックスを使用/使用しないように強制できます。 `FORCE_INDEX`と`USE_INDEX`は同じ効果があります。

-   `READ_FROM_STORAGE`オプティマイザに特定のテーブルに対してクエリを実行するために TiKV / TiFlashストレージエンジンを選択するように強制できます。

## 複数値インデックスを使用する {#use-multi-valued-indexes}

[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)は通常のインデックスとは異なります。 TiDB は現在、複数値のインデックスにアクセスするために[インデックスマージ](/explain-index-merge.md)のみを使用します。したがって、データ アクセスに複数値インデックスを使用するには、システム変数[`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)の値が`ON`に設定されていることを確認してください。

複数値インデックスの制限事項については、 [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md#limitations)を参照してください。

### サポートされているシナリオ {#supported-scenarios}

現在、TiDB は`json_member_of` 、 `json_contains` E}} 、 `json_overlaps`の条件から自動的に変換される IndexMerge を使用して、複数値インデックスへのアクセスをサポートしています。オプティマイザがコストに基づいて IndexMerge を自動的に選択するようにするか、オプティマイザヒント[`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)または[`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を使用して複数値インデックスの選択を指定できます。以下の例を参照してください。

```sql
mysql> CREATE TABLE t1 (j JSON, INDEX idx((CAST(j->'$.path' AS SIGNED ARRAY)))); -- Uses '$.path' as the path to create a multi-valued index
Query OK, 0 rows affected (0.04 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE (1 MEMBER OF (j->'$.path'));
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                               | operator info                                                          |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
| Selection_5                     | 8000.00 | root      |                                                                             | json_memberof(cast(1, json BINARY), json_extract(test.t1.j, "$.path")) |
| └─IndexMerge_8                  | 10.00   | root      |                                                                             | type: union                                                            |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                            |
|   └─TableRowIDScan_7(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo                                         |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_9                  | 10.00   | root      |                                                                             | type: intersection                          |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[3,3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
5 rows in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                               | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 8000.00 | root      |                                                                             | json_overlaps(json_extract(test.t1.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 10.00   | root      |                                                                             | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                                      |
|   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo                                      |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[3,3], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
6 rows in set, 1 warning (0.00 sec)
```

複合多値インデックスは、IndexMerge を介してアクセスすることもできます。

```sql
CREATE TABLE t2 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j->'$.path' AS SIGNED ARRAY)), b), INDEX idx2(b, (CAST(k->'$.path' AS SIGNED ARRAY))));
EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND (1 MEMBER OF (j->'$.path')) AND b=2;
EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
EXPLAIN SELECT /*+ use_index_merge(t2, idx, idx2) */ * FROM t2 WHERE (a=1 AND 1 member of (j->'$.path')) AND (b=1 AND 2 member of (k->'$.path'));
```

```sql
> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND (1 MEMBER OF (j->'$.path')) AND b=2;
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                       |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| IndexMerge_7                  | 0.00    | root      |                                                                                   | type: union                                         |
| ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1 2,1 1 2], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                      |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                   |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| IndexMerge_9                  | 0.00    | root      |                                                                                   | type: intersection                              |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                                     | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 0.24    | root      |                                                                                   | json_overlaps(json_extract(test.t2.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 0.30    | root      |                                                                                   | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_8(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo                                  |
|   └─TableRowIDScan_9(Probe)     | 0.30    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t2, idx, idx2) */ * FROM t2 WHERE (a=1 AND 1 member of (j->'$.path')) AND (b=1 AND 2 member of (k->'$.path'));
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                       |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| IndexMerge_8                  | 0.00    | root      |                                                                                   | type: intersection                                  |
| ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1 1,1 1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx2(b, cast(json_extract(`k`, _utf8'$.path') as signed array))   | range:[1 2,1 2], keep order:false, stats:pseudo     |
| └─TableRowIDScan_7(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                      |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
```

TiDBはIndexMergeを使用して、複数値インデックスと通常のインデックスの両方にアクセスすることもできます。例：

```sql
CREATE TABLE t3(j1 JSON, j2 JSON, a INT, INDEX k1((CAST(j1->'$.path' AS SIGNED ARRAY))), INDEX k2((CAST(j2->'$.path' AS SIGNED ARRAY))), INDEX ka(a));
EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') OR a = 3;
EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') AND 2 member of (j2->'$.path') AND (a = 3);
```

```sql
> EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') OR a = 3;
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_8                  | 19.99   | root      |                                                                             | type: union                                 |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t3, index:k1(cast(json_extract(`j1`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t3, index:ka(a)                                                       | range:[3,3], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 19.99   | cop[tikv] | table:t3                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') AND 2 member of (j2->'$.path') AND (a = 3);
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_9                  | 0.00    | root      |                                                                             | type: intersection                          |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t3, index:ka(a)                                                       | range:[3,3], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t3, index:k1(cast(json_extract(`j1`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t3, index:k2(cast(json_extract(`j2`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t3                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
```

`json_member_of` 、 `json_contains`または`json_overlaps`の複数の条件が`OR`または`AND`と関連付けられている場合、IndexMergeを使用して複数値インデックスにアクセスするには、以下の要件を満たす必要があります。

```sql
CREATE TABLE t4(a INT, j JSON, INDEX mvi1((CAST(j->'$.a' AS UNSIGNED ARRAY))), INDEX mvi2((CAST(j->'$.b' AS UNSIGNED ARRAY))));
```

-   `OR`に関連する条件については、それぞれ IndexMerge を使用してアクセスできる必要があります。例:

    ```sql
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_overlaps(j->'$.a', '[3, 4]');
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_length(j->'$.a') = 3;
    SHOW WARNINGS;
    ```

    ```sql
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_overlaps(j->'$.a', '[3, 4]');
    +----------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | id                               | estRows | task      | access object                                                               | operator info                                                                                                                                              |
    +----------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Selection_5                      | 31.95   | root      |                                                                             | or(json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1, 2]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.a"), cast("[3, 4]", json BINARY))) |
    | └─IndexMerge_11                  | 39.94   | root      |                                                                             | type: union                                                                                                                                                |
    |   ├─IndexRangeScan_6(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                                |
    |   ├─IndexRangeScan_7(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                                |
    |   ├─IndexRangeScan_8(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                                |
    |   ├─IndexRangeScan_9(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[4,4], keep order:false, stats:pseudo                                                                                                                |
    |   └─TableRowIDScan_10(Probe)     | 39.94   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                             |
    +----------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+

    -- json_length(j->'$.a') = 3 cannot be accessed with IndexMerge directly, so TiDB cannot use IndexMerge for this SQL statement.
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_length(j->'$.a') = 3;
    +-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
    | id                      | estRows  | task      | access object | operator info                                                                                                                      |
    +-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
    | Selection_5             | 8000.00  | root      |               | or(json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1, 2]", json BINARY)), eq(json_length(json_extract(test.t4.j, "$.a")), 3)) |
    | └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                               |
    |   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t4      | keep order:false, stats:pseudo                                                                                                     |
    +-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------+

    > SHOW WARNINGS;
    +---------+------+----------------------------+
    | Level   | Code | Message                    |
    +---------+------+----------------------------+
    | Warning | 1105 | IndexMerge is inapplicable |
    +---------+------+----------------------------+
    ```

-   `AND`に関連する条件については、それぞれ IndexMerge を使用してアクセスできる必要があります。TiDB は、これらの条件を持つマルチ値インデックスへのアクセスに IndexMerge のみを使用できます。例:

    ```sql
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]');
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]') AND json_length(j->'$.a') = 2;
    ```

    ```sql
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]');
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
    | id                            | estRows | task      | access object                                                               | operator info                               |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
    | IndexMerge_10                 | 0.00    | root      |                                                                             | type: intersection                          |
    | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
    | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
    | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
    | ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[4,4], keep order:false, stats:pseudo |
    | └─TableRowIDScan_9(Probe)     | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

    -- json_length(j->'$.a') = 3 cannot be accessed with IndexMerge directly, so TiDB uses IndexMerge to access the other two json_contains conditions, and json_length(j->'$.a') = 3 becomes a Selection operator.
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]') AND json_length(j->'$.a') = 2;
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------+
    | id                            | estRows | task      | access object                                                               | operator info                                      |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------+
    | IndexMerge_11                 | 0.00    | root      |                                                                             | type: intersection                                 |
    | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo        |
    | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo        |
    | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo        |
    | ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[4,4], keep order:false, stats:pseudo        |
    | └─Selection_10(Probe)         | 0.00    | cop[tikv] |                                                                             | eq(json_length(json_extract(test.t4.j, "$.a")), 2) |
    |   └─TableRowIDScan_9          | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                     |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------+
    ```

-   IndexMerge に使用されるすべての条件は、それらを接続している`OR`または`AND`のセマンティクスと一致する必要があります。

    -   `json_contains` `AND`と接続されている場合は、意味的に一致します。例:

        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') AND json_contains(j->'$.b', '[2, 3]');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2, 3]');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') AND json_contains(j->'$.b', '[2, 3]');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_9                  | 0.00    | root      |                                                                             | type: intersection                          |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
        | └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

        -- The conditions do not match the semantics, so TiDB cannot use IndexMerge for this SQL statement as explained above.
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2, 3]');
        +-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                      | estRows  | task      | access object | operator info                                                                                                                                           |
        +-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | TableReader_7           | 10.01    | root      |               | data:Selection_6                                                                                                                                        |
        | └─Selection_6           | 10.01    | cop[tikv] |               | or(json_contains(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_contains(json_extract(test.t4.j, "$.b"), cast("[2, 3]", json BINARY))) |
        |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t4      | keep order:false, stats:pseudo                                                                                                                          |
        +-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        ```

    -   `json_overlaps` `OR`と接続されている場合は、意味的に一致します。例:

        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') OR json_overlaps(j->'$.b', '[2, 3]');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2, 3]');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') OR json_overlaps(j->'$.b', '[2, 3]');
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                              | estRows | task      | access object                                                               | operator info                                                                                                                                           |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | Selection_5                     | 23.98   | root      |                                                                             | or(json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.b"), cast("[2, 3]", json BINARY))) |
        | └─IndexMerge_10                 | 29.97   | root      |                                                                             | type: union                                                                                                                                             |
        |   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                             |
        |   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                             |
        |   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                             |
        |   └─TableRowIDScan_9(Probe)     | 29.97   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                          |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+

        -- The conditions do not match the semantics, so TiDB can only use IndexMerge for part of the conditions of this SQL statement as explained above.
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2, 3]');
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                              | estRows | task      | access object                                                               | operator info                                                                                                                                       |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
        | Selection_5                     | 15.99   | root      |                                                                             | json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.b"), cast("[2, 3]", json BINARY)) |
        | └─IndexMerge_8                  | 10.00   | root      |                                                                             | type: union                                                                                                                                         |
        |   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                         |
        |   └─TableRowIDScan_7(Probe)     | 10.00   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                      |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
        ```

    -   `json_member_of`が`OR`または`AND`に接続されている場合、意味的に一致します。例:

        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND 2 member of (j->'$.b') AND 3 member of (j->'$.a');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR 2 member of (j->'$.b') OR 3 member of (j->'$.a');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND 2 member of (j->'$.b') AND 3 member of (j->'$.a');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_9                  | 0.00    | root      |                                                                             | type: intersection                          |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR 2 member of (j->'$.b') OR 3 member of (j->'$.a');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_9                  | 29.97   | root      |                                                                             | type: union                                 |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
        | └─TableRowIDScan_8(Probe)     | 29.97   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        ```

    -   複数の値を含む`json_contains`条件が`OR`に接続されている場合、または複数の値を含む`json_overlaps`条件が`AND`に接続されている場合、それらは意味論に一致しませんが、値が 1 つだけの場合は意味論に一致します。例:

        ```sql
        -- Refer to the preceding examples for conditions that do not match the semantics. The following only provides examples of conditions that match the semantics.
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2]');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2]');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2]');
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                              | estRows | task      | access object                                                               | operator info                                                                                                                                    |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
        | Selection_5                     | 8.00    | root      |                                                                             | json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.b"), cast("[2]", json BINARY)) |
        | └─IndexMerge_9                  | 0.01    | root      |                                                                             | type: intersection                                                                                                                               |
        |   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                      |
        |   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                      |
        |   └─TableRowIDScan_8(Probe)     | 0.01    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                   |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+

        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2]');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_8                  | 19.99   | root      |                                                                             | type: union                                 |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | └─TableRowIDScan_7(Probe)     | 19.99   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        ```

    -   `OR`と`AND`の両方を使用して条件を接続する場合 (実質的には`OR`と`AND`ネストされている場合)、IndexMerge を構成する条件は`OR`のセマンティクスにすべて一致するか、 `AND`のセマンティクスにすべて一致する必要があります。 `OR`のセマンティクスに部分的に一致し、かつ`AND`のセマンティクスに部分的に一致することはできません。例:

        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND (2 member of (j->'$.b') OR 3 member of (j->'$.a'));
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR (2 member of (j->'$.b') AND 3 member of (j->'$.a'));
        ```

        ```sql
        -- Only 2 member of (j->'$.b') and 3 member of (j->'$.a') that match the semantics of OR constitute the IndexMerge. 1 member of (j->'$.a') that matches the semantics of AND is not included.
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND (2 member of (j->'$.b') OR 3 member of (j->'$.a'));
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                                                                                                                                                                                                     |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | IndexMerge_9                  | 0.00    | root      |                                                                             | type: union                                                                                                                                                                                                       |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                                                                                       |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                                                                                       |
        | └─Selection_8(Probe)          | 0.00    | cop[tikv] |                                                                             | json_memberof(cast(1, json BINARY), json_extract(test.t4.j, "$.a")), or(json_memberof(cast(2, json BINARY), json_extract(test.t4.j, "$.b")), json_memberof(cast(3, json BINARY), json_extract(test.t4.j, "$.a"))) |
        |   └─TableRowIDScan_7          | 19.99   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                                                                                    |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

        -- Only 1 member of (j->'$.a') and 2 member of (j->'$.a') that match the semantics of OR constitute the IndexMerge. 2 member of (j->'$.b') that matches the semantics of AND is not included.
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR (2 member of (j->'$.b') AND 3 member of (j->'$.a'));
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                                                                                                                                                                                                          |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | IndexMerge_9                  | 0.02    | root      |                                                                             | type: union                                                                                                                                                                                                            |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                                                                                            |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                                                                                            |
        | └─Selection_8(Probe)          | 0.02    | cop[tikv] |                                                                             | or(json_memberof(cast(1, json BINARY), json_extract(test.t4.j, "$.a")), and(json_memberof(cast(2, json BINARY), json_extract(test.t4.j, "$.b")), json_memberof(cast(3, json BINARY), json_extract(test.t4.j, "$.a")))) |
        |   └─TableRowIDScan_7          | 19.99   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                                                                                         |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        ```

条件にネストされた`OR` / `AND`が含まれている場合、または条件が展開などの変換後にインデックス付き列のみに対応する場合、TiDB は IndexMerge を使用できないか、すべての条件を十分に活用できない可能性があります。個々のケースの動作を確認することをお勧めします。

以下にいくつかの例を示します。

```sql
CREATE TABLE t5 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY))), INDEX idx2(b, (CAST(k as SIGNED ARRAY))));
CREATE TABLE t6 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY)), b), INDEX idx2(a, (CAST(k as SIGNED ARRAY)), b));
```

`AND`が`OR`で接続された条件の中にネストされており、 `AND`で接続されたサブ条件が複数列インデックスの正確な列に対応している場合、TiDB は通常、これらの条件を最大限に活用できます。例:

```sql
EXPLAIN SELECT /*+ use_index_merge(t5, idx, idx2) */ * FROM t5 WHERE (a=1 AND 1 member of (j)) OR (b=2 AND 2 member of (k));
```

```sql
> EXPLAIN SELECT /*+ use_index_merge(t5, idx, idx2) */ * FROM t5 WHERE (a=1 AND 1 member of (j)) OR (b=2 AND 2 member of (k));
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                      | operator info                                   |
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
| IndexMerge_8                  | 0.20    | root      |                                                    | type: union                                     |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t5, index:idx(a, cast(`j` as signed array))  | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t5, index:idx2(b, cast(`k` as signed array)) | range:[2 2,2 2], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 0.20    | cop[tikv] | table:t5                                           | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
```

`OR`が`AND`で接続された条件の中にネストされており、 `OR`で接続されたサブ条件が展開後にインデックス付き列に対応する場合、TiDB は通常、これらの条件を最大限に活用できます。例:

```sql
EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND (1 member of (j) OR 2 member of (k));
```

```sql
+-------------------------------+---------+-----------+-------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object                                         | operator info                                                                                                           |
+-------------------------------+---------+-----------+-------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| IndexMerge_9                  | 0.20    | root      |                                                       | type: union                                                                                                             |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1,1 1], keep order:false, stats:pseudo                                                                         |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                                                         |
| └─Selection_8(Probe)          | 0.20    | cop[tikv] |                                                       | eq(test2.t6.a, 1), or(json_memberof(cast(1, json BINARY), test2.t6.j), json_memberof(cast(2, json BINARY), test2.t6.k)) |
|   └─TableRowIDScan_7          | 0.20    | cop[tikv] | table:t6                                              | keep order:false, stats:pseudo                                                                                          |
+-------------------------------+---------+-----------+-------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
```

`OR`で接続された条件の中に複数の`AND`がネストされており、 `OR`で接続されたサブ条件をインデックス列に対応するように展開する必要がある場合、TiDB はすべての条件を完全に利用できない可能性があります。例:

```sql
EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND (1 member of (j) OR 2 member of (k)) and (b = 1 OR b = 2);
EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND ((1 member of (j) AND b = 1) OR (1 member of (j) AND b = 2) OR (2 member of (k) AND b = 1) OR (2 member of (k) AND b = 2));
```

```sql
-- Due to current implementation limitations, (b = 1 or b = 2) does not constitute the IndexMerge, but becomes a Selection operator
> EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND (1 member of (j) OR 2 member of (k)) AND (b = 1 OR b = 2);
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object                                         | operator info                                                                                                                                                |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexMerge_9                  | 0.20    | root      |                                                       | type: union                                                                                                                                                  |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1,1 1], keep order:false, stats:pseudo                                                                                                              |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                                                                                              |
| └─Selection_8(Probe)          | 0.20    | cop[tikv] |                                                       | eq(test.t6.a, 1), or(eq(test.t6.b, 1), eq(test.t6.b, 2)), or(json_memberof(cast(1, json BINARY), test.t6.j), json_memberof(cast(2, json BINARY), test.t6.k)) |
|   └─TableRowIDScan_7          | 0.20    | cop[tikv] | table:t6                                              | keep order:false, stats:pseudo                                                                                                                               |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+

-- If you manually expand the two OR conditions connected with AND, TiDB can make full use of these conditions
> EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND ((1 member of (j) AND b = 1) OR (1 member of (j) AND b = 2) OR (2 member of (k) AND b = 1) OR (2 member of (k) AND b = 2));
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object                                         | operator info                                                                                                                                                                                                                                                                                                            |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexMerge_11                 | 0.00    | root      |                                                       | type: union                                                                                                                                                                                                                                                                                                              |
| ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1 1,1 1 1], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| ├─IndexRangeScan_6(Build)     | 0.00    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1 2,1 1 2], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| ├─IndexRangeScan_7(Build)     | 0.00    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2 1,1 2 1], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| ├─IndexRangeScan_8(Build)     | 0.00    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2 2,1 2 2], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| └─Selection_10(Probe)         | 0.00    | cop[tikv] |                                                       | eq(test.t6.a, 1), or(or(and(json_memberof(cast(1, json BINARY), test.t6.j), eq(test.t6.b, 1)), and(json_memberof(cast(1, json BINARY), test.t6.j), eq(test.t6.b, 2))), or(and(json_memberof(cast(2, json BINARY), test.t6.k), eq(test.t6.b, 1)), and(json_memberof(cast(2, json BINARY), test.t6.k), eq(test.t6.b, 2)))) |
|   └─TableRowIDScan_9          | 0.00    | cop[tikv] | table:t6                                              | keep order:false, stats:pseudo                                                                                                                                                                                                                                                                                           |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

現在のマルチバリューインデックスの実装上の制約により、 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を使用すると`Can't find a proper physical plan for this query`エラーが発生する可能性がありますが、 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)使用するとそのようなエラーは発生しません。したがって、マルチバリューインデックスを使用する場合は`use_index_merge`を使用することをお勧めします。

```sql
mysql> EXPLAIN SELECT /*+ use_index(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
ERROR 1815 (HY000): Internal : Cant find a proper physical plan for this query

mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                                                                                                                |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(and(json_memberof(cast(1, json BINARY), test.t3.j), json_memberof(cast(2, json BINARY), test.t3.j)), and(json_memberof(cast(3, json BINARY), test.t3.j), json_memberof(cast(4, json BINARY), test.t3.j))) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                                                                                                         |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                                                                                                               |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 2 warnings (0.00 sec)
```

### 複数値インデックスとプランキャッシュ {#multi-valued-indexes-and-plan-cache}

`member of`を使用して複数値インデックスを選択するクエリプランはキャッシュできます。 `JSON_CONTAINS()`または`JSON_OVERLAPS()`関数を使用して複数値インデックスを選択するクエリプランはキャッシュできません。

クエリプランをキャッシュできる例をいくつか以下に示します。

```sql
mysql> CREATE TABLE t5 (j1 JSON, j2 JSON, INDEX idx1((CAST(j1 AS SIGNED ARRAY))));
Query OK, 0 rows affected (0.04 sec)

mysql> PREPARE st FROM 'SELECT /*+ use_index(t5, idx1) */ * FROM t5 WHERE (? member of (j1))';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @a=1;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE st USING @a;
Empty set (0.01 sec)

mysql> EXECUTE st USING @a;
Empty set (0.00 sec)

mysql> SELECT @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)

mysql> PREPARE st FROM 'SELECT /*+ use_index(t5, idx1) */ * FROM t5 WHERE (? member of (j1)) AND JSON_CONTAINS(j2, ?)';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @a=1, @b='[1,2]';
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE st USING @a, @b;
Empty set (0.00 sec)

mysql> EXECUTE st USING @a, @b;
Empty set (0.00 sec)

mysql> SELECT @@LAST_PLAN_FROM_CACHE; -- can hit plan cache if the JSON_CONTAINS doesn't impact index selection
+------------------------+
| @@LAST_PLAN_FROM_CACHE |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

クエリプランをキャッシュできない例をいくつか示します。

```sql
mysql> PREPARE st2 FROM 'SELECT /*+ use_index(t5, idx1) */ * FROM t5 WHERE JSON_CONTAINS(j1, ?)';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @a='[1,2]';
Query OK, 0 rows affected (0.01 sec)

mysql> EXECUTE st2 USING @a;
Empty set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;  -- cannot hit plan cache since the JSON_CONTAINS predicate might affect index selection
+---------+------+-------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                               |
+---------+------+-------------------------------------------------------------------------------------------------------+
| Warning | 1105 | skip prepared plan-cache: json_contains function with immutable parameters can affect index selection |
+---------+------+-------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB SQL Tuning Lab 1: Clustered and Non-Clustered Indexes" type="lab" link="https://labs.tidb.io/labs/dba_307_lab_ff0" imgSrc="https://lab-static.pingcap.com/quick-demo/307-01.png" duration="90 mins" />
</RelatedResources>

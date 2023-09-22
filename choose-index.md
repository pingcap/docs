---
title: Index Selection
summary: Choose the best indexes for TiDB query optimization.
---

# インデックスの選択 {#index-selection}

storageエンジンからのデータの読み取りは、SQL 実行中に最も時間がかかる手順の 1 つです。現在、TiDB は、さまざまなstorageエンジンおよびさまざまなインデックスからのデータの読み取りをサポートしています。クエリの実行パフォーマンスは、適切なインデックスを選択したかどうかに大きく依存します。

このドキュメントでは、テーブルにアクセスするためのインデックスの選択方法と、インデックスの選択を制御するための関連する方法をいくつか紹介します。

## アクセステーブル {#access-tables}

インデックス選択を導入する前に、TiDB がテーブルにアクセスする方法、各方法のトリガー、各方法の違い、および長所と短所を理解することが重要です。

### テーブルにアクセスするための演算子 {#operators-for-accessing-tables}

| オペレーター               | トリガー条件                                              | 該当するシナリオ                                     | 説明                                                                                                                                                                      |
| :------------------- | :-------------------------------------------------- | :------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ポイントゲット / バッチポイントゲット | 1 つ以上の単一ポイント範囲内のテーブルにアクセスする場合。                      | あらゆるシナリオ                                     | トリガーされると、コプロセッサー・インターフェースを呼び出すのではなく、kvget インターフェースを直接呼び出して計算を実行するため、通常は最も高速なオペレーターとみなされます。                                                                              |
| テーブルリーダー             | なし                                                  | あらゆるシナリオ                                     | この TableReader オペレーターは TiKV 用です。これは一般に、TiKVレイヤーからテーブル データを直接スキャンする最も効率の悪いオペレーターとみなされます。これは、 `_tidb_rowid`列に範囲クエリがある場合、またはテーブルにアクセスするための他の演算子が選択できない場合にのみ選択できます。         |
| テーブルリーダー             | テーブルにはTiFlashノード上にレプリカがあります。                        | 読み取る列は少なくなりますが、評価する行は多くなります。                 | この TableReader オペレーターはTiFlash用です。 TiFlash は列ベースのstorageです。少数の列と多数の行を計算する必要がある場合は、この演算子を選択することをお勧めします。                                                                   |
| インデックスリーダー           | テーブルには 1 つ以上のインデックスがあり、計算に必要な列はインデックスに含まれています。      | インデックスに狭い範囲のクエリがある場合、またはインデックス付き列の順序要件がある場合。 | 複数のインデックスが存在する場合、コスト見積もりに基づいて合理的なインデックスが選択されます。                                                                                                                         |
| IndexLookupReader    | テーブルには 1 つ以上のインデックスがあり、計算に必要な列がインデックスに完全には含まれていません。 | IndexReader と同じです。                           | インデックスは計算列を完全にはカバーしていないため、TiDB はインデックスを読み取った後にテーブルから行を取得する必要があります。 IndexReader オペレーターと比較して追加のコストがかかります。                                                                 |
| インデックスマージ            | テーブルには複数のインデックスまたは複数値のインデックスがあります。                  | 多値インデックスまたは複数のインデックスが使用される場合。                | 演算子を使用するには、 [オプティマイザーのヒント](/optimizer-hints.md)指定するか、コスト見積もりに基づいてオプティマイザにこの演算子を自動的に選択させることができます。詳細は[インデックス マージを使用した Explain ステートメント](/explain-index-merge.md)を参照してください。 |

> **注記：**
>
> TableReader 演算子は`_tidb_rowid`列インデックスに基づいており、 TiFlash は列storageインデックスを使用するため、インデックスの選択はテーブルにアクセスするための演算子の選択となります。

## インデックスの選択ルール {#index-selection-rules}

TiDB はルールまたはコストに基づいてインデックスを選択します。ベースのルールには、事前ルールとスカイライン プルーニングが含まれます。インデックスを選択するとき、TiDB は最初に事前ルールを試行します。インデックスが事前ルールを満たす場合、TiDB はこのインデックスを直接選択します。それ以外の場合、TiDB はスカイライン プルーニングを使用して不適切なインデックスを除外し、テーブルにアクセスする各オペレーターのコスト推定に基づいてコストが最も低いインデックスを選択します。

### ルールベースの選択 {#rule-based-selection}

#### 事前ルール {#pre-rules}

TiDB は、次のヒューリスティック事前ルールを使用してインデックスを選択します。

-   ルール 1: インデックスが「完全一致の一意のインデックス + テーブルから行を取得する必要がない (つまり、インデックスによって生成されたプランが IndexReader 演算子であることを意味します)」を満たす場合、TiDB はこのインデックスを直接選択します。

-   ルール 2: インデックスが「完全一致を持つ一意のインデックス + テーブルから行を取得する必要性 (つまり、インデックスによって生成されたプランが IndexReader 演算子であることを意味します)」を満たしている場合、TiDB は、行数が最も少ないインデックスを選択します。候補インデックスとしてテーブルから取得されます。

-   ルール 3: インデックスが「通常のインデックス + テーブルから行を取得する必要がない + 読み込む行数が一定のしきい値未満」を満たす場合、TiDB は読み込む行数が最も少ないインデックスを選択します。候補インデックスとして読み込まれます。

-   ルール 4: ルール 2 および 3 に基づいて候補インデックスが 1 つだけ選択された場合は、この候補インデックスを選択します。ルール 2 と 3 でそれぞれ 2 つの候補インデクスが選択された場合は、読み込む行数（インデクスのある行数 + 表から取得する行数）が少ない方のインデクスを選択します。

上記のルールの「完全一致のインデックス」とは、インデックス付けされた各列が等しい条件を持つことを意味します。 `EXPLAIN FORMAT = 'verbose' ...`ステートメントの実行時に、事前ルールがインデックスと一致する場合、TiDB はインデックスが事前ルールと一致することを示す NOTE レベルの警告を出力します。

次の例では、インデックス`idx_b`ルール 2 の「完全一致の一意のインデックス + テーブルから行を取得する必要がある」という条件を満たしているため、TiDB はアクセス パスとしてインデックス`idx_b`を選択し、インデックス`SHOW WARNING`は、インデックス`idx_b`事前ルールに一致します。

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

### スカイラインの剪定 {#skyline-pruning}

スカイライン プルーニングはインデックスのヒューリスティック フィルタリング ルールであり、誤った推定によって引き起こされる誤ったインデックスの選択の可能性を減らすことができます。インデックスを判断するには、次の 3 つの側面が必要です。

-   インデックス付き列でカバーされるアクセス条件の数。 「アクセス条件」は、列範囲に変換できる where 条件です。また、インデックス付き列セットがカバーするアクセス条件が多ければ多いほど、このディメンションではより優れたものになります。

-   テーブルにアクセスするインデックスを選択するときに、テーブルから行を取得する必要があるかどうか (つまり、インデックスによって生成されるプランは IndexReader 演算子または IndexLookupReader 演算子です)。このディメンションでは、テーブルから行を取得しないインデックスの方が、テーブルから行を取得するインデックスよりも優れています。両方のインデックスでテーブルから行を取得するために TiDB が必要な場合は、インデックス付き列でカバーされるフィルター条件の数を比較します。絞り込み条件とは、指標に基づいて判断できる`where`条件を指します。インデックスの列セットがより多くのアクセス条件をカバーする場合、テーブルから取得される行の数が少なくなり、このディメンションにおけるインデックスの品質が向上します。

-   インデックスが特定の順序を満たすかどうかを選択します。インデックスの読み取りによって特定の列セットの順序が保証されるため、クエリ順序を満たすインデックスは、このディメンションに関して満たさないインデックスよりも優れています。

上記の 3 つの次元について、インデックス`idx_a`パフォーマンスが 3 つの次元すべてでインデックス`idx_b`より悪くなく、1 つの次元で`idx_b`よりも優れている場合は、 `idx_a`が優先されます。 `EXPLAIN FORMAT = 'verbose' ...`ステートメントの実行時に、スカイライン プルーニングによって一部のインデックスが除外される場合、TiDB は、スカイライン プルーニングの除外後に残りのインデックスをリストした NOTE レベルの警告を出力します。

次の例では、インデックス`idx_b`と`idx_e`は両方とも`idx_b_c`より劣っているため、スカイライン枝刈りによって除外されます。返された結果`SHOW WARNING`には、スカイライン プルーニング後の残りのインデックスが表示されます。

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

### 見積りによる選定 {#cost-estimation-based-selection}

スカイライン プルーニング ルールを使用して不適切なインデックスを除外した後、インデックスの選択は完全にコスト見積もりに基づいて行われます。テーブルへのアクセスのコストを見積もるには、次の考慮事項が必要です。

-   storageエンジン内のインデックス付きデータの各行の平均長。
-   インデックスによって生成されたクエリ範囲内の行数。
-   テーブルから行を取得するためのコスト。
-   クエリの実行中にインデックスによって生成された範囲の数。

これらの要素とコスト モデルに従って、オプティマイザはテーブルにアクセスするためのコストが最も低いインデックスを選択します。

#### コスト見積もりに基づいた選択に伴う一般的なチューニングの問題 {#common-tuning-problems-with-cost-estimation-based-selection}

1.  推定行数は正確ではありませんか?

    これは通常、統計が古いか不正確であることが原因です。 `analyze table`ステートメントを再実行するか、 `analyze table`ステートメントのパラメーターを変更できます。

2.  統計は正確で、 TiFlashからの読み取りの方が高速ですが、オプティマイザはなぜ TiKV からの読み取りを選択するのでしょうか?

    現時点では、 TiFlashと TiKV を区別するコスト モデルはまだ大まかです。 `tidb_opt_seek_factor`パラメータの値を減らすことができ、その場合、オプティマイザはTiFlashを選択することを優先します。

3.  統計は正確です。インデックス A はテーブルから行を取得する必要がありますが、実際にはテーブルから行を取得しないインデックス B よりも高速に実行されます。オプティマイザはなぜインデックス B を選択するのでしょうか?

    この場合、コスト見積もりが大きすぎてテーブルから行を取得できない可能性があります。 `tidb_opt_network_factor`パラメータの値を減らして、テーブルから行を取得するコストを削減できます。

## 制御インデックスの選択 {#control-index-selection}

インデックスの選択は、 [オプティマイザーのヒント](/optimizer-hints.md)を介して単一のクエリによって制御できます。

-   `USE_INDEX` / `IGNORE_INDEX` 、オプティマイザに特定のインデックスを使用または使用しないように強制できます。 `FORCE_INDEX`と`USE_INDEX`同様の効果があります。

-   `READ_FROM_STORAGE`指定すると、オプティマイザがクエリを実行するために特定のテーブルに対して TiKV / TiFlashstorageエンジンを選択するように強制できます。

## 複数値のインデックスを使用する {#use-multi-valued-indexes}

[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)は通常のインデックスとは異なります。 TiDB は現在、複数値インデックスへのアクセスに[インデックスマージ](/explain-index-merge.md)のみを使用します。したがって、データ アクセスに複数値インデックスを使用するには、システム変数`tidb_enable_index_merge`の値が`ON`に設定されていることを確認してください。

複数値インデックスの制限については、 [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md#limitations)を参照してください。

### サポートされているシナリオ {#supported-scenarios}

現在、TiDB は、 `json_member_of` 、 `json_contains` 、および`json_overlaps`条件から自動的に変換される IndexMerge を使用した複数値インデックスへのアクセスをサポートしています。オプティマイザを利用してコストに基づいて IndexMerge を自動的に選択することも、オプティマイザのヒント[`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)または[`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を使用して複数値インデックスの選択を指定することもできます。次の例を参照してください。

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

複合多値インデックスには、IndexMerge を通じてアクセスすることもできます。

```sql
mysql> CREATE TABLE t2 (a INT, j JSON, b INT, INDEX idx(a, (CAST(j->'$.path' AS SIGNED ARRAY)), b));
Query OK, 0 rows affected (0.04 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND (1 MEMBER OF (j->'$.path')) AND b=2;
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                                     | operator info                                                          |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+------------------------------------------------------------------------+
| Selection_5                     | 0.01    | root      |                                                                                   | json_memberof(cast(1, json BINARY), json_extract(test.t2.j, "$.path")) |
| └─IndexMerge_8                  | 0.00    | root      |                                                                                   | type: union                                                            |
|   ├─IndexRangeScan_6(Build)     | 0.00    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1 2,1 1 2], keep order:false, stats:pseudo                    |
|   └─TableRowIDScan_7(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                                         |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+------------------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                   |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| IndexMerge_9                  | 0.10    | root      |                                                                                   | type: intersection                              |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 0.10    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
5 rows in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                                     | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 8.00    | root      |                                                                                   | json_overlaps(json_extract(test.t2.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 0.10    | root      |                                                                                   | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_8(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo                                  |
|   └─TableRowIDScan_9(Probe)     | 0.10    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
6 rows in set, 1 warning (0.00 sec)
```

同じ複数値インデックスにアクセスできる複数の`member of`式で構成される`OR`条件の場合、IndexMerge を使用して複数値インデックスにアクセスできます。

```sql
mysql> CREATE TABLE t3 (a INT, j JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY))));
Query OK, 0 rows affected (0.04 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE ((a=1 AND (1 member of (j)))) OR ((a=2 AND (2 member of (j))));
+---------------------------------+---------+-----------+---------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                     | operator info                                                                                                                                    |
+---------------------------------+---------+-----------+---------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5                     | 0.08    | root      |                                                   | or(and(eq(test.t3.a, 1), json_memberof(cast(1, json BINARY), test.t3.j)), and(eq(test.t3.a, 2), json_memberof(cast(2, json BINARY), test.t3.j))) |
| └─IndexMerge_9                  | 0.10    | root      |                                                   | type: union                                                                                                                                      |
|   ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t3, index:idx(a, cast(`j` as signed array)) | range:[1 1,1 1], keep order:false, stats:pseudo                                                                                                  |
|   ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t3, index:idx(a, cast(`j` as signed array)) | range:[2 2,2 2], keep order:false, stats:pseudo                                                                                                  |
|   └─TableRowIDScan_8(Probe)     | 0.10    | cop[tikv] | table:t3                                          | keep order:false, stats:pseudo                                                                                                                   |
+---------------------------------+---------+-----------+---------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
```

### 部分的にサポートされるシナリオ {#partially-supported-scenarios}

複数の異なるインデックスに対応する複数の式で構成される`AND`条件の場合、アクセスに使用できる複数値インデックスは 1 つだけです。

```sql
mysql> create table t(j1 json, j2 json, a int, INDEX k1((CAST(j1->'$.path' AS SIGNED ARRAY))), INDEX k2((CAST(j2->'$.path' AS SIGNED ARRAY))), INDEX ka(a));
Query OK, 0 rows affected (0.02 sec)

mysql> explain select /*+ use_index_merge(t, k1, k2, ka) */ * from t where (1 member of (j1->'$.path')) and (2 member of (j2->'$.path')) and (a = 3);
+---------------------------------+---------+-----------+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                              | operator info                                                                                                                                  |
+---------------------------------+---------+-----------+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5                     | 8.00    | root      |                                                                            | json_memberof(cast(1, json BINARY), json_extract(test.t.j1, "$.path")), json_memberof(cast(2, json BINARY), json_extract(test.t.j2, "$.path")) |
| └─IndexMerge_9                  | 0.01    | root      |                                                                            | type: union                                                                                                                                    |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t, index:k1(cast(json_extract(`j1`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                    |
|   └─Selection_8(Probe)          | 0.01    | cop[tikv] |                                                                            | eq(test.t.a, 3)                                                                                                                                |
|     └─TableRowIDScan_7          | 10.00   | cop[tikv] | table:t                                                                    | keep order:false, stats:pseudo                                                                                                                 |
+---------------------------------+---------+-----------+----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
5 rows in set, 6 warnings (0.01 sec)
```

現在、TiDB は、複数のインデックスを使用して同時にアクセスする次のプランを生成するのではなく、1 つのインデックスを使用したアクセスのみをサポートしています。

    Selection
    └─IndexMerge
      ├─IndexRangeScan(k1)
      ├─IndexRangeScan(k2)
      ├─IndexRangeScan(ka)
      └─Selection
        └─TableRowIDScan

### サポートされていないシナリオ {#unsupported-scenarios}

複数の異なるインデックスに対応する複数の式で構成される`OR`条件の場合、複数値インデックスは使用できません。

```sql
mysql> create table t(j1 json, j2 json, a int, INDEX k1((CAST(j1->'$.path' AS SIGNED ARRAY))), INDEX k2((CAST(j2->'$.path' AS SIGNED ARRAY))), INDEX ka(a));
Query OK, 0 rows affected (0.03 sec)

mysql> explain select /*+ use_index_merge(t, k1, k2, ka) */ * from t where (1 member of (j1->'$.path')) or (2 member of (j2->'$.path'));
+-------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                                                      |
+-------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(json_memberof(cast(1, json BINARY), json_extract(test.t.j1, "$.path")), json_memberof(cast(2, json BINARY), json_extract(test.t.j2, "$.path"))) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                                               |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                                                                     |
+-------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 3 warnings (0.00 sec)

mysql> explain select /*+ use_index_merge(t, k1, k2, ka) */ * from t where (1 member of (j1->'$.path')) or (a = 3);
+-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                               |
+-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(json_memberof(cast(1, json BINARY), json_extract(test.t.j1, "$.path")), eq(test.t.a, 3)) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                        |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
3 rows in set, 3 warnings (0.00 sec)
```

前述のシナリオの回避策は、 `Union All`を使用してクエリを書き直すことです。

以下は、まだサポートされていない、より複雑なシナリオです。

```sql
mysql> CREATE TABLE t4 (j JSON, INDEX idx((CAST(j AS SIGNED ARRAY))));
Query OK, 0 rows affected (0.04 sec)

-- If a query contains the OR condition composed of multiple json_contains expressions, the index cannot be accessed using IndexMerge.
mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE (json_contains(j, '[1, 2]')) OR (json_contains(j, '[3, 4]'));
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                    |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 9600.00  | root      |               | data:Selection_6                                                                                                 |
| └─Selection_6           | 9600.00  | cop[tikv] |               | or(json_contains(test.t3.j, cast("[1, 2]", json BINARY)), json_contains(test.t3.j, cast("[3, 4]", json BINARY))) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                   |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
3 rows in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------+
| Level   | Code | Message                    |
+---------+------+----------------------------+
| Warning | 1105 | IndexMerge is inapplicable |
+---------+------+----------------------------+
1 row in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE (json_contains(j, '[1, 2]')) OR (json_contains(j, '[3, 4]'));
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                    |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 9600.00  | root      |               | data:Selection_6                                                                                                 |
| └─Selection_6           | 9600.00  | cop[tikv] |               | or(json_contains(test.t3.j, cast("[1, 2]", json BINARY)), json_contains(test.t3.j, cast("[3, 4]", json BINARY))) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                   |
+-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------+
3 rows in set, 1 warning (0.01 sec)

-- If a query contains the more complex expression formed by multi-layer OR/AND nesting, the index cannot be accessed using IndexMerge.
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

複数値インデックスの現在の実装による制限により、 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を使用すると`Can't find a proper physical plan for this query`エラーが返される可能性がありますが、 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)使用するとそのようなエラーは返されません。したがって、複数値のインデックスを使用する場合は`use_index_merge`を使用することをお勧めします。

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

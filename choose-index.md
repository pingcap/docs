---
title: Index Selection
summary: TiDB クエリの最適化に最適なインデックスを選択します。
---

# インデックスの選択 {#index-selection}

storageエンジンからデータを読み取ることは、SQL 実行中に最も時間のかかるステップの 1 つです。現在、TiDB はさまざまなstorageエンジンとさまざまなインデックスからのデータの読み取りをサポートしています。クエリ実行のパフォーマンスは、適切なインデックスを選択したかどうかに大きく依存します。

このドキュメントでは、テーブルにアクセスするためのインデックスの選択方法と、インデックスの選択を制御する関連する方法について説明します。

## アクセステーブル {#access-tables}

インデックス選択を導入する前に、TiDB がテーブルにアクセスする方法、それぞれの方法をトリガーするもの、それぞれの方法の違い、そして長所と短所を理解することが重要です。

### テーブルにアクセスするための演算子 {#operators-for-accessing-tables}

| オペレーター             | トリガー条件                                              | 適用可能なシナリオ                                         | 説明                                                                                                                                                                    |
| :----------------- | :-------------------------------------------------- | :------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ポイント取得 / バッチポイント取得 | 1 つ以上の単一ポイント範囲内のテーブルにアクセスする場合。                      | あらゆるシナリオ                                          | トリガーされると、コプロセッサ インターフェイスを呼び出すのではなく、kvget インターフェイスを直接呼び出して計算を実行するため、通常は最も高速な演算子と見なされます。                                                                                |
| テーブルリーダー           | なし                                                  | あらゆるシナリオ                                          | この TableReader 演算子は TiKV 用です。これは通常、 `_tidb_rowid`レイヤーからテーブル データを直接スキャンする最も効率の悪い演算子であると考えられています。1 列に範囲クエリがある場合、またはテーブルにアクセスするための他の演算子が選択できない場合にのみ選択できます。               |
| テーブルリーダー           | テーブルのレプリカがTiFlashノード上に存在します。                        | 読み取る列は少なくなりますが、評価する行は多くなります。                      | この TableReader 演算子はTiFlash用です。TiFlashは列ベースのstorageです。少数の列と多数の行を計算する必要がある場合は、この演算子を選択することをお勧めします。                                                                      |
| インデックスリーダー         | テーブルには 1 つ以上のインデックスがあり、計算に必要な列がインデックスに含まれています。      | インデックスに対してより狭い範囲のクエリがある場合、またはインデックス付き列に順序要件がある場合。 | 複数のインデックスが存在する場合、コスト見積もりに基づいて適切なインデックスが選択されます。                                                                                                                        |
| インデックスルックアップリーダー   | テーブルには 1 つ以上のインデックスがあり、計算に必要な列がインデックスに完全には含まれていません。 | IndexReader と同じです。                                | インデックスは計算列を完全にはカバーしないため、TiDB はインデックスを読み取った後にテーブルから行を取得する必要があります。IndexReader 演算子と比較して余分なコストがかかります。                                                                     |
| インデックスマージ          | テーブルには複数のインデックスまたは複数値インデックスがあります。                   | 複数値インデックスまたは複数のインデックスが使用される場合。                    | 演算子を使用するには、 [オプティマイザヒント](/optimizer-hints.md)を指定するか、コスト見積もりに基づいてオプティマイザにこの演算子を自動的に選択させることができます。詳細については、 [インデックスマージを使用したステートメントの説明](/explain-index-merge.md)を参照してください。 |

> **注記：**
>
> TableReader 演算子は`_tidb_rowid`列のインデックスに基づいており、 TiFlash は列storageインデックスを使用するため、インデックスの選択はテーブルにアクセスするための演算子の選択になります。

## インデックス選択ルール {#index-selection-rules}

TiDB は、ルールまたはコストに基づいてインデックスを選択します。ベースとなるルールには、事前ルールとスカイライン プルーニングが含まれます。インデックスを選択する際、TiDB はまず事前ルールを試します。インデックスが事前ルールを満たしている場合、TiDB はそのインデックスを直接選択します。そうでない場合、TiDB はスカイライン プルーニングを使用して不適切なインデックスを除外し、テーブルにアクセスする各演算子のコスト推定に基づいてコストが最も低いインデックスを選択します。

### ルールベースの選択 {#rule-based-selection}

#### 事前ルール {#pre-rules}

TiDB は、次のヒューリスティックな事前ルールを使用してインデックスを選択します。

-   ルール 1: インデックスが「完全一致の一意のインデックス + テーブルから行を取得する必要がない (つまり、インデックスによって生成されるプランは IndexReader 演算子である)」という条件を満たす場合、TiDB はこのインデックスを直接選択します。

-   ルール 2: インデックスが「完全一致の一意のインデックス + テーブルから行を取得する必要がある (つまり、インデックスによって生成されるプランは IndexLookupReader 演算子である)」という条件を満たす場合、TiDB はテーブルから取得される行数が最も少ないインデックスを候補インデックスとして選択します。

-   ルール 3: インデックスが「通常のインデックス + テーブルから行を取得する必要がない + 読み取る行数が特定のしきい値未満」の条件を満たす場合、TiDB は読み取る行数が最も少ないインデックスを候補インデックスとして選択します。

-   ルール 4: ルール 2 と 3 に基づいて候補インデックスが 1 つだけ選択された場合は、この候補インデックスを選択します。ルール 2 と 3 に基づいてそれぞれ 2 つの候補インデックスが選択された場合には、読み取る行数 (インデックスを持つ行数 + テーブルから取得する行数) が少ない方のインデックスを選択します。

上記のルールの「完全一致のインデックス」は、インデックスが付けられた各列に等しい条件があることを意味します。 `EXPLAIN FORMAT = 'verbose' ...`ステートメントを実行すると、事前ルールがインデックスに一致する場合、TiDB はインデックスが事前ルールに一致することを示す NOTE レベルの警告を出力します。

次の例では、インデックス`idx_b`ルール 2 の条件「完全一致の一意のインデックス + テーブルから行を取得する必要がある」を満たしているため、TiDB はインデックス`idx_b`をアクセス パスとして選択し、インデックス`idx_b`が事前ルールに一致することを示すメモを`SHOW WARNING`返します。

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

スカイラインプルーニングは、インデックスのヒューリスティックなフィルタリングルールであり、誤った推定によって誤ったインデックスが選択される可能性を減らすことができます。インデックスを判断するには、次の 3 つの次元が必要です。

-   インデックス列によってカバーされるアクセス条件の数。「アクセス条件」は、列範囲に変換できる where 条件です。インデックス列セットがカバーするアクセス条件が多いほど、このディメンションでは優れています。

-   インデックスを選択してテーブルにアクセスする際に、テーブルから行を取得する必要があるかどうか (つまり、インデックスによって生成されたプランが IndexReader 演算子または IndexLookupReader 演算子であるかどうか)。テーブルから行を取得しないインデックスは、取得するインデックスよりもこの次元では優れています。両方のインデックスでテーブルから行を取得するために TiDB が必要な場合は、インデックス列でカバーされるフィルタリング条件の数を比較します。フィルタリング条件とは、インデックスに基づいて判断できる`where`条件を意味します。インデックスの列セットがカバーするアクセス条件が多いほど、テーブルから取得される行数が少なくなり、この次元ではインデックスが優れています。

-   インデックスが特定の順序を満たすかどうかを選択します。インデックスの読み取りによって特定の列セットの順序が保証されるため、クエリ順序を満たすインデックスは、このディメンションで満たさないインデックスよりも優先されます。

上記の 3 つの次元では、インデックス`idx_a`パフォーマンスが 3 `EXPLAIN FORMAT = 'verbose' ...`の次元すべてでインデックス`idx_b`より悪くなく、1 つの次元で`idx_b`より優れている場合、 `idx_a`が推奨されます。9 ステートメントを実行すると、スカイライン プルーニングによって一部のインデックスが除外されると、TiDB はスカイライン プルーニング除外後の残りのインデックスをリストする NOTE レベルの警告を出力します。

次の例では、インデックス`idx_b`と`idx_e`どちらも`idx_b_c`より下位であるため、スカイライン プルーニングによって除外されます。返される結果`SHOW WARNING`は、スカイライン プルーニング後の残りのインデックスを表示します。

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

### コスト見積もりに基づく選択 {#cost-estimation-based-selection}

スカイライン プルーニング ルールを使用して不適切なインデックスを除外した後、インデックスの選択は完全にコスト見積もりに基づいて行われます。テーブルへのアクセスのコスト見積もりでは、次の点を考慮する必要があります。

-   storageエンジン内のインデックス付きデータの各行の平均長。
-   インデックスによって生成されたクエリ範囲内の行数。
-   テーブルから行を取得するためのコスト。
-   クエリ実行中にインデックスによって生成された範囲の数。

これらの要因とコスト モデルに従って、オプティマイザーはテーブルにアクセスするためのコストが最も低いインデックスを選択します。

#### コスト見積もりに基づく選択における一般的なチューニングの問題 {#common-tuning-problems-with-cost-estimation-based-selection}

1.  推定行数が正確ではありませんか?

    これは通常、統計が古いか不正確であることが原因です。 `ANALYZE TABLE`ステートメントを再実行するか、 `ANALYZE TABLE`のステートメントのパラメータを変更できます。

2.  統計は正確で、 TiFlashからの読み取りは高速ですが、なぜオプティマイザーは TiKV からの読み取りを選択するのでしょうか?

    現時点では、 TiFlashと TiKV を区別するコスト モデルはまだ大まかです。 [`tidb_opt_seek_factor`](/system-variables.md#tidb_opt_seek_factor)パラメータの値を減らすと、オプティマイザはTiFlashを選択するようになります。

3.  統計は正確です。インデックス A はテーブルから行を取得する必要がありますが、実際にはテーブルから行を取得しないインデックス B よりも高速に実行されます。なぜオプティマイザーはインデックス B を選択するのでしょうか。

    この場合、テーブルから行を取得するためのコスト見積もりが大きすぎる可能性があります。 [`tidb_opt_network_factor`](/system-variables.md#tidb_opt_network_factor)パラメータの値を減らすと、テーブルから行を取得するコストを削減できます。

## 制御インデックスの選択 {#control-index-selection}

インデックスの選択は、 [オプティマイザのヒント](/optimizer-hints.md)介した単一のクエリによって制御できます。

-   `USE_INDEX` / `IGNORE_INDEX` `FORCE_INDEX`オプティマイザに特定のインデックスの使用/不使用を強制できます。4 と`USE_INDEX`同じ効果があります。

-   `READ_FROM_STORAGE` 、クエリを実行するために、特定のテーブルに対して TiKV / TiFlashstorageエンジンを選択するようにオプティマイザーに強制できます。

## 複数値インデックスを使用する {#use-multi-valued-indexes}

[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)は通常のインデックスとは異なります。TiDB は現在、多値インデックスへのアクセスに[インデックスマージ](/explain-index-merge.md)のみを使用します。したがって、データ アクセスに多値インデックスを使用するには、システム変数[`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40)の値が`ON`に設定されていることを確認してください。

多値インデックスの制限については[`CREATE INDEX`](/sql-statements/sql-statement-create-index.md#limitations)を参照してください。

### サポートされているシナリオ {#supported-scenarios}

現在、TiDB は、 `json_member_of` 、 `json_contains` 、および`json_overlaps`条件から自動的に変換される IndexMerge を使用して、複数値インデックスへのアクセスをサポートしています。コストに基づいて IndexMerge を自動的に選択するようにオプティマイザに頼るか、オプティマイザ ヒント[`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)または[`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)を使用して複数値インデックスの選択を指定できます。次の例を参照してください。

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

複合多値インデックスには IndexMerge を通じてアクセスすることもできます。

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

TiDB は IndexMerge を使用して、複数値インデックスと通常のインデックスの両方にアクセスすることもできます。例:

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

複数の`json_member_of` 、 `json_contains` 、または`json_overlaps`の条件が`OR`または`AND`に接続されている場合、IndexMerge を使用して複数値インデックスにアクセスするには、次の要件を満たす必要があります。

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

-   `AND`に関連する条件のうちいくつかは、それぞれ IndexMerge でアクセスできる必要があります。TiDB は、これらの条件を持つ複数値インデックスにアクセスする場合にのみ IndexMerge を使用できます。例:

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

-   IndexMerge に使用されるすべての条件は、それらを接続する`OR`または`AND`のセマンティクスと一致する必要があります。

    -   `json_contains` `AND`と接続されている場合、意味が一致します。例:

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

    -   `json_overlaps` `OR`と接続されている場合、意味が一致します。例:

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

    -   `json_member_of` `OR`または`AND`と接続されている場合、意味は一致します。例:

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

    -   複数の値を含む`json_contains`条件が`OR`で接続されている場合、または複数の値を含む`json_overlaps`条件が`AND`で接続されている場合、それらは意味と一致しませんが、 1 つの値のみを含む場合は意味と一致します。例:

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

    -   `OR`と`AND`両方を使用して条件を接続する場合 (基本的に`OR`と`AND`がネストされます)、IndexMerge を構成する条件は、 `OR`の意味にすべて一致するか、 `AND`の意味にすべて一致し、 `OR`の意味に部分的に一致せず、 `AND`の意味に部分的に一致する必要があります。例:

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

条件にネストされた`OR` / `AND`が含まれている場合、または条件が拡張などの変換後のインデックス付き列のみに対応している場合、TiDB は IndexMerge を使用できないか、すべての条件を十分に活用できない可能性があります。それぞれの特定のケースの動作を確認することをお勧めします。

以下に例をいくつか示します。

```sql
CREATE TABLE t5 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY))), INDEX idx2(b, (CAST(k as SIGNED ARRAY))));
CREATE TABLE t6 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY)), b), INDEX idx2(a, (CAST(k as SIGNED ARRAY)), b));
```

`AND`が`OR`で接続された条件にネストされ、 `AND`で接続されたサブ条件が複数列インデックスの正確な列に対応する場合、TiDB は通常、条件を最大限に活用できます。例:

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

`AND`で接続された条件に 1 つの`OR`がネストされ、 `OR`で接続されたサブ条件が拡張後のインデックス列に対応する場合、TiDB は通常、条件を最大限に活用できます。例:

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

`AND`で接続された条件に複数の`OR`ネストされ、 `OR`で接続されたサブ条件をインデックス列に対応するように拡張する必要がある場合、TiDB はすべての条件を十分に活用できない可能性があります。例:

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

マルチ値インデックスの現在の実装によって制限されているため、 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-)使用すると`Can't find a proper physical plan for this query`エラーが返される可能性がありますが、 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)を使用するとそのようなエラーは返されません。したがって、マルチ値インデックスを使用する場合は`use_index_merge`使用することをお勧めします。

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

### 多値インデックスとプランキャッシュ {#multi-valued-indexes-and-plan-cache}

`member of`使用して複数値インデックスを選択するクエリ プランはキャッシュできます。3 `JSON_OVERLAPS()` `JSON_CONTAINS()`を使用して複数値インデックスを選択するクエリ プランはキャッシュできません。

クエリ プランをキャッシュできる例をいくつか示します。

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

クエリ プランをキャッシュできない例を次に示します。

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

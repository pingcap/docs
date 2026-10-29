---
title: Vector Search Index
summary: ベクトル検索インデックスを構築して使用し、TiDB で K近傍法 (KNN) クエリを高速化する方法を学びます。
aliases: ['/ja/tidb/stable/vector-search-index/','/ja/tidbcloud/vector-search-index/']
---

# ベクトル検索インデックス {#vector-search-index}

[ベクトル検索](/ai/guides/vector-search-overview.md)文書で説明されているように、ベクトル検索は、与えられたベクトルとデータベースに格納されているすべてのベクトルとの距離を計算することで、与えられたベクトルの上位K近傍（KNN）を特定します。このアプローチは正確な結果をもたらしますが、テーブルに多数のベクトルが含まれている場合、テーブル全体のスキャンが必要となるため、処理速度が低下する可能性があります[^1]

検索効率を向上させるために、TiDBでは近似KNN（ANN）検索用のベクトル検索インデックスを作成できます。ベクトル検索にベクトルインデックスを使用すると、TiDBは精度をわずかに低下させるだけでクエリパフォーマンスを大幅に向上させ、通常90%以上の検索再現率を維持できます。

> **Note:**
>
> - ベクトル検索機能はパブリックプレビューです。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> - ベクトル検索機能は[TiDB Self-Managed](/overview.md)および[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter)で利用可能です。TiDB Self-Managedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

現在、TiDB は[HNSW（階層的ナビゲート可能なスモールワールド）](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)ベクトル検索インデックスアルゴリズムをサポートしています。

## 制限 {#restrictions}

- 事前にTiFlashノードをクラスターにデプロイする必要があります。
- ベクトル検索インデックスは、主キーまたは一意インデックスとして使用できません。
- ベクトル検索インデックスは単一のベクトル列にのみ作成でき、他の列 (整数や文字列など) と組み合わせて複合インデックスを形成できません。
- ベクトル検索インデックスの作成および使用時には、距離関数を指定する必要があります。現在、コサイン距離`VEC_COSINE_DISTANCE()`とL2距離`VEC_L2_DISTANCE()`の関数のみがサポートされています。
- 同じ列に対して、同じ距離関数を使用して複数のベクトル検索インデックスを作成することはサポートされていません。
- ベクトル検索インデックスが設定された列を直接削除することはサポートされていません。このような列を削除するには、まずその列のベクトル検索インデックスを削除し、次に列自体を削除します。
- ベクトルインデックスを持つ列の型の変更はサポートされていません。
- ベクトル検索インデックスを[不可視](/sql-statements/sql-statement-alter-index.md)に設定することはサポートされていません。
- [保存時の暗号化](/encryption-at-rest.md)が有効になっているTiFlashノード上でベクトル検索インデックスを構築することはサポートされていません。

## HNSWベクトルインデックスを作成する {#create-the-hnsw-vector-index}

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)は、最も人気のあるベクトルインデックスアルゴリズムの1つです。HNSWインデックスは、特定のケースでは最大98%という比較的高い精度で優れたパフォーマンスを提供します。

TiDB では、次のいずれかの方法で、 [ベクトルデータ型](/ai/reference/vector-search-data-types.md)列に対して HNSW インデックスを作成できます。

- テーブルを作成するときは、次の構文を使用して HNSW インデックスのベクトル列を指定します。

    ```sql
    CREATE TABLE foo (
        id       INT PRIMARY KEY,
        embedding     VECTOR(5),
        VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
    );
    ```

- ベクトル列がすでに含まれている既存のテーブルの場合は、次の構文を使用してベクトル列の HNSW インデックスを作成します。

    ```sql
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding)));
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)));

    -- You can also explicitly specify "USING HNSW" to build the vector search index.
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ```

> **Note:**
>
> ベクトル検索インデックス機能は、テーブルのTiFlashレプリカに依存します。
>
> - テーブルの作成時にベクトル検索インデックスが定義されている場合、TiDB はテーブルのTiFlashレプリカを自動的に作成します。
> - テーブルの作成時にベクトル検索インデックスが定義されておらず、テーブルに現在TiFlashレプリカが存在しない場合は、テーブルにベクトル検索インデックスを追加する前に、手動でTiFlashレプリカを作成する必要があります。例: `ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;` 。

HNSW ベクトルインデックスを作成するときは、ベクトルの距離関数を指定する必要があります。

- コサイン距離: `((VEC_COSINE_DISTANCE(embedding)))`
- L2距離: `((VEC_L2_DISTANCE(embedding)))`

ベクトルインデックスは、固定次元のベクトル列（例えば、 `VECTOR(3)`と定義された列）に対してのみ作成できます。ベクトル距離は、同じ次元のベクトル間でのみ計算できるため、非固定次元のベクトル列（例えば、 `VECTOR`と定義された列）には作成できません。

ベクトル検索インデックスの制限と制約については、 [制限](#restrictions)を参照してください。

## ベクトルインデックスを使用する {#use-the-vector-index}

ベクトル検索インデックスは、次のように`ORDER BY ... LIMIT`句を使用して K近傍検索クエリで使用できます。

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

ベクトル検索でインデックスを使用するには、 `ORDER BY ... LIMIT`句がベクトルインデックスの作成時に指定したものと同じ距離関数を使用していることを確認します。

## フィルター付きベクトルインデックスを使用する {#use-the-vector-index-with-filters}

`WHERE` フィルターをどこに置くかによって、ベクトル検索でベクトルインデックスを使用できるかどうかが決まります。2 つのパターンがあり、それぞれ精度と速度のトレードオフが逆になります。

### ベクトル検索の前にフィルターする {#filter-before-the-vector-search}

`WHERE` でフィルターしてから距離でソートするクエリは、一致する行の中だけで K 近傍を求めます。ベクトルインデックスはその問いに答えられないため、TiDB はテーブルをスキャンし、フィルターを適用し、一致する各行の距離を計算します。

```sql
-- The WHERE filter is applied before the K-nearest-neighbor search, so the vector index is not used:

SELECT * FROM vec_table
WHERE category = "document"
  AND VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') IS NOT NULL
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

距離が `NULL` の行を除外することで、結果は正確になります。つまり、フィルターに一致し、有効なコサイン距離を持つ最も近い 5 行、またはそのような行が 5 行未満の場合はそのすべてを取得します。`VEC_COSINE_DISTANCE()` は、入力ベクトルが `NULL` の場合や、ゼロベクトルのようにコサイン距離が未定義の場合に `NULL` を返します。この除外を行わないと、`NULL` 値は昇順では非 `NULL` 値より前にソートされ、結果の先頭を占めることがあります。コストはフィルターを通過する行数に応じて増加するため、このパターンは選択性の高いフィルターに適しています。

### ベクトル検索の後にフィルターする {#filter-after-the-vector-search}

ベクトルインデックスを使用するには、まずサブクエリで K 近傍を見つけてから、結果をフィルターします。

```sql
-- The WHERE filter is applied after the K-nearest-neighbor search, so the query can use the vector index:

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";
```

フィルターは近傍が見つかった後でそれらを除外するため、このクエリは 5 行未満、または 0 行を返すことがあります。その可能性を低くするには、サブクエリで必要数より多くの近傍を取得し、最終結果の件数を制限します。

```sql
SELECT * FROM
(
  SELECT *, VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') AS distance
  FROM vec_table
  ORDER BY distance
  LIMIT 50
) t
WHERE category = "document"
ORDER BY distance
LIMIT 5;
```

より多くの近傍を取得すると 5 行を得られる可能性は高まりますが、保証はされません。内側の `LIMIT` は、通常フィルターによって何行除外されるかに基づいて選択してください。

クエリがどちらのパターンを使用しているかを確認するには、そのクエリに対して `EXPLAIN` を実行し、`operator info` カラムに `annIndex:` があるかを確認します。詳細は、[ベクトルインデックスが使用されているかどうかを確認する](#check-whether-the-vector-index-is-used) を参照してください。

> **Note:**
>
> パーティションテーブルにはベクトルインデックスを作成できません。ベクトルインデックス付きの `CREATE TABLE ... PARTITION BY` と、パーティションテーブルに対する `ALTER TABLE ... ADD VECTOR INDEX` は、どちらも `ERROR 8200 (HY000): Unsupported add columnar index: partition table is currently not supported` を返します。たとえばテナントごとにテーブルをパーティション化した場合、そのテーブルに対するベクトル検索では、ベクトルインデックスを使用せずに選択されたパーティションをスキャンします。

## インデックス構築の進行状況を確認する {#view-index-build-progress}

大量のデータを挿入した後、その一部がTiFlashに即座に保存されない場合があります。既に保存されているベクトルデータの場合、ベクトル検索インデックスは同期的に構築されます。まだ保存されていないデータの場合、データが保存された時点でインデックスが構築されます。このプロセスはデータの精度と一貫性に影響を与えません。ベクトル検索はいつでも実行でき、完全な結果を得ることができます。ただし、ベクトルインデックスが完全に構築されるまでは、パフォーマンスは最適ではありません。

インデックス構築の進行状況を表示するには、次のように`INFORMATION_SCHEMA.TIFLASH_INDEXES`テーブルをクエリします。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME    | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | tcff1d827  |      219 | col1fff     | 0a452311      |         7 |        1 | HNSW       |               29646 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      717 | embedding   | idx_embedding |         2 |        1 | HNSW       |                   0 |                       0 |                  0 |                      3 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- インデックス構築の進行状況は、 `ROWS_STABLE_INDEXED`と`ROWS_STABLE_NOT_INDEXED`列で確認できます。`ROWS_STABLE_NOT_INDEXED`が0になると、インデックス構築が完了します。

    参考までに、768次元の500MiBベクトルデータセットのインデックス作成には最大20分かかる場合があります。インデクサーは複数のテーブルに対して並列実行できます。現在、インデクサーの優先度や速度の調整はサポートされていません。

- デルタレイヤーの行数は`ROWS_DELTA_NOT_INDEXED`列で確認できます。TiFlashのストレージレイヤーのデータは、デルタレイヤーとステーブルレイヤーの2つのレイヤーに保存されます。デルタレイヤーには最近挿入または更新された行が保存され、書き込みワークロードに応じて定期的にステーブルレイヤーにマージされます。このマージプロセスはコンパクションと呼ばれます。

    Deltaレイヤーは常にインデックス化されません。最適なパフォーマンスを実現するには、DeltaレイヤーをStableレイヤーに強制的にマージし、すべてのデータがインデックス化されるようにできます。

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    詳細については[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)を参照してください。

さらに、 `ADMIN SHOW DDL JOBS;`を実行して`row count`を確認することで、DDLジョブの実行進捗状況を監視できます。ただし、 `row count`の値は`TIFLASH_INDEXES`の`rows_stable_indexed`フィールドから取得されるため、この方法は完全には正確ではありません。この方法は、インデックス作成の進捗状況を追跡するための参照として使用できます。

## ベクトルインデックスが使用されているかどうかを確認する {#check-whether-the-vector-index-is-used}

クエリがベクトルインデックスを使用しているかどうかを確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを使用します。`TableFullScan`エグゼキュータの`operator info`列に`annIndex:`が表示されている場合、このテーブルスキャンはベクトルインデックスを使用していることを意味します。

**例: ベクトルインデックスが使用される**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;
+-----+-------------------------------------------------------------------------------------+
| ... | operator info                                                                       |
+-----+-------------------------------------------------------------------------------------+
| ... | ...                                                                                 |
| ... | Column#5, offset:0, count:10                                                        |
| ... | ..., vec_cosine_distance(test.vector_table_with_index.embedding, [1,2,3])->Column#5 |
| ... | MppVersion: 1, data:ExchangeSender_16                                               |
| ... | ExchangeType: PassThrough                                                           |
| ... | ...                                                                                 |
| ... | Column#4, offset:0, count:10                                                        |
| ... | ..., vec_cosine_distance(test.vector_table_with_index.embedding, [1,2,3])->Column#4 |
| ... | annIndex:COSINE(test.vector_table_with_index.embedding..[1,2,3], limit:10), ...     |
+-----+-------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

**例: Top Kを指定していないため、ベクトルインデックスは使用されません。**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
     -> ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]');
+--------------------------------+-----+--------------------------------------------------+
| id                             | ... | operator info                                    |
+--------------------------------+-----+--------------------------------------------------+
| Projection_15                  | ... | ...                                              |
| └─Sort_4                       | ... | Column#4                                         |
|   └─Projection_16              | ... | ..., vec_cosine_distance(..., [1,2,3])->Column#4 |
|     └─TableReader_14           | ... | MppVersion: 1, data:ExchangeSender_13            |
|       └─ExchangeSender_13      | ... | ExchangeType: PassThrough                        |
|         └─TableFullScan_12     | ... | keep order:false, stats:pseudo                   |
+--------------------------------+-----+--------------------------------------------------+
6 rows in set, 1 warning (0.01 sec)
```

ベクトルインデックスが使用できない場合、原因の調査に役立つ警告が表示される場合があります。

```sql
-- Using a wrong distance function:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_L2_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- Using a wrong order:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## ベクトル検索のパフォーマンスを分析する {#analyze-vector-search-performance}

ベクトルインデックスの使用方法に関する詳細情報を確認するには、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを実行し、出力の`execution info`列を確認します。

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;
+-----+--------------------------------------------------------+-----+
|     | execution info                                         |     |
+-----+--------------------------------------------------------+-----+
| ... | time:339.1ms, loops:2, RU:0.000000, Concurrency:OFF    | ... |
| ... | time:339ms, loops:2                                    | ... |
| ... | time:339ms, loops:3, Concurrency:OFF                   | ... |
| ... | time:339ms, loops:3, cop_task: {...}                   | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{...}, vector_idx:{                       | ... |
|     |   load:{total:68ms,from_s3:1,from_disk:0,from_cache:0},|     |
|     |   search:{total:0ms,visited_nodes:2,discarded_nodes:0},|     |
|     |   read:{vec_total:0ms,others_total:0ms}},...}          |     |
+-----+--------------------------------------------------------+-----+
```

> **Note:**
>
> 実行情報は内部情報です。フィールドとフォーマットは予告なく変更される場合があります。これらの情報に依存しないでください。

いくつかの重要なフィールドの説明:

- `vector_index.load.total` : インデックスの読み込みにかかる合計時間。複数のベクトルインデックスが並行して読み込まれる可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
- `vector_index.load.from_s3` : S3 からロードされたインデックスの数。
- `vector_index.load.from_disk` : ディスクからロードされたインデックスの数。インデックスは以前にS3からダウンロード済みです。
- `vector_index.load.from_cache` : キャッシュからロードされたインデックスの数。インデックスは以前にS3からダウンロード済みです。
- `vector_index.search.total` : インデックス内の検索にかかる合計時間。レイテンシーが大きい場合、通常、インデックスがコールド状態（一度もアクセスされていない、またはかなり前にアクセスされている状態）であるため、インデックス検索時に大量のI/O操作が発生します。複数のベクトルインデックスが並列で検索される可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
- `vector_index.search.discarded_nodes` : 検索中に訪問されたが破棄されたベクトル行の数。これらの破棄されたベクトルは検索結果には考慮されません。この値が大きい場合、通常、 `UPDATE`または`DELETE`文によって多くの古い行が発生していることを示します。

出力の解釈については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 、および[`EXPLAIN`ウォークスルー](/explain-walkthrough.md)を参照してください。

## 参照 {#see-also}

- [ベクトル検索のパフォーマンスを向上させる](/ai/reference/vector-search-improve-performance.md)
- [ベクトルデータ型](/ai/reference/vector-search-data-types.md)

[^1]: KNN 検索の説明は、ClickHouse ドキュメントの[rschu1ze](https://github.com/rschu1ze)が作成した[近似最近傍検索インデックス](https://github.com/ClickHouse/ClickHouse/pull/50661/files#diff-7ebd9e71df96e74230c9a7e604fa7cb443be69ba5e23bf733fcecd4cc51b7576)ドキュメントに基づいており、Apache License 2.0 に基づいてライセンスされています。

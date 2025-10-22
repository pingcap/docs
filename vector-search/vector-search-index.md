---
title: Vector Search Index
summary: ベクトル検索インデックスを構築して使用し、TiDB で K 近傍法 (KNN) クエリを高速化する方法を学びます。
---

# ベクター検索インデックス {#vector-search-index}

[ベクトル検索](/vector-search/vector-search-overview.md)文書で説明されているように、ベクトル検索は、与えられたベクトルとデータベースに格納されているすべてのベクトルとの距離を計算することで、与えられたベクトルの上位K近傍（KNN）を特定します。このアプローチは正確な結果をもたらしますが、テーブルに多数のベクトルが含まれている場合、テーブル全体のスキャンが必要となるため、処理速度が低下する可能性があります[^1]

検索効率を向上させるために、TiDBでは近似KNN（ANN）検索用のベクトル検索インデックスを作成できます。ベクトル検索にベクトルインデックスを使用すると、TiDBは精度をわずかに低下させるだけでクエリパフォーマンスを大幅に向上させ、通常90%以上の検索再現率を維持できます。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB Self-Managed、 [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)利用できます[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

現在、TiDB は[HNSW（階層的ナビゲート可能なスモールワールド）](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)ベクトル検索インデックス アルゴリズムをサポートしています。

## 制限 {#restrictions}

-   事前にTiFlashノードをクラスターにデプロイする必要があります。
-   ベクトル検索インデックスは、主キーまたは一意のインデックスとして使用することはできません。
-   ベクトル検索インデックスは単一のベクトル列にのみ作成でき、他の列 (整数や文字列など) と組み合わせて複合インデックスを形成することはできません。
-   ベクトル検索インデックスの作成および使用時には、距離関数を指定する必要があります。現在、コサイン距離`VEC_COSINE_DISTANCE()`とL2距離`VEC_L2_DISTANCE()`関数のみがサポートされています。
-   同じ列に対して、同じ距離関数を使用して複数のベクトル検索インデックスを作成することはサポートされていません。
-   ベクトル検索インデックスが設定された列を直接削除することはサポートされていません。このような列を削除するには、まずその列のベクトル検索インデックスを削除し、次に列自体を削除します。
-   ベクトル インデックスを持つ列の型の変更はサポートされていません。
-   ベクトル検索インデックスを[見えない](/sql-statements/sql-statement-alter-index.md)に設定することはサポートされていません。
-   [保存時の暗号化](https://docs.pingcap.com/tidb/stable/encryption-at-rest)有効になっているTiFlashノード上でベクトル検索インデックスを構築することはサポートされていません。

## HNSWベクトルインデックスを作成する {#create-the-hnsw-vector-index}

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)は、最も人気のあるベクトルインデックスアルゴリズムの1つです。HNSWインデックスは、特定のケースでは最大98%という比較的高い精度で優れたパフォーマンスを提供します。

TiDB では、次のいずれかの方法で、 [ベクトルデータ型](/vector-search/vector-search-data-types.md)の列に対して HNSW インデックスを作成できます。

-   テーブルを作成するときは、次の構文を使用して HNSW インデックスのベクトル列を指定します。

    ```sql
    CREATE TABLE foo (
        id       INT PRIMARY KEY,
        embedding     VECTOR(5),
        VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
    );
    ```

-   ベクター列がすでに含まれている既存のテーブルの場合は、次の構文を使用してベクター列の HNSW インデックスを作成します。

    ```sql
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding)));
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)));

    -- You can also explicitly specify "USING HNSW" to build the vector search index.
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ```

> **注記：**
>
> ベクター検索インデックス機能は、テーブルのTiFlashレプリカに依存します。
>
> -   テーブルの作成時にベクトル検索インデックスが定義されている場合、TiDB はテーブルのTiFlashレプリカを自動的に作成します。
> -   テーブルの作成時にベクトル検索インデックスが定義されておらず、テーブルに現在TiFlashレプリカが存在しない場合は、テーブルにベクトル検索インデックスを追加する前に、手動でTiFlashレプリカを作成する必要があります。例: `ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;` 。

HNSW ベクトル インデックスを作成するときは、ベクトルの距離関数を指定する必要があります。

-   コサイン距離: `((VEC_COSINE_DISTANCE(embedding)))`
-   L2距離: `((VEC_L2_DISTANCE(embedding)))`

ベクトルインデックスは、固定次元のベクトル列（例えば、 `VECTOR(3)`と定義された列）に対してのみ作成できます。ベクトル距離は、同じ次元のベクトル間でのみ計算できるため、非固定次元のベクトル列（例えば、 `VECTOR`と定義された列）には作成できません。

ベクター検索インデックスの制限と制約については、 [制限](#restrictions)参照してください。

## ベクトルインデックスを使用する {#use-the-vector-index}

ベクトル検索インデックスは、次のように`ORDER BY ... LIMIT`句を使用して K 近傍検索クエリで使用できます。

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

ベクトル検索でインデックスを使用するには、 `ORDER BY ... LIMIT`句がベクトル インデックスの作成時に指定したものと同じ距離関数を使用していることを確認します。

## フィルター付きベクトルインデックスを使用する {#use-the-vector-index-with-filters}

プレフィルタ（ `WHERE`句を使用）を含むクエリは、SQLセマンティクスに従ってK近傍検索を実行していないため、ベクトルインデックスを利用できません。例：

```sql
-- For the following query, the `WHERE` filter is performed before KNN, so the vector index cannot be used:

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

フィルター付きのベクター インデックスを使用するには、まずベクター検索を使用して K 近傍を照会し、次に不要な結果をフィルター処理します。

```sql
-- For the following query, the `WHERE` filter is performed after KNN, so the vector index cannot be used:

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- Note that this query might return fewer than 5 results if some are filtered out.
```

## インデックス構築の進行状況をビュー {#view-index-build-progress}

大量のデータを挿入した後、その一部がTiFlashに即座に保存されない場合があります。既に保存されているベクターデータの場合、ベクター検索インデックスは同期的に構築されます。まだ保存されていないデータの場合、データが保存された時点でインデックスが構築されます。このプロセスはデータの精度と一貫性に影響を与えません。ベクター検索はいつでも実行でき、完全な結果を得ることができます。ただし、ベクターインデックスが完全に構築されるまでは、パフォーマンスは最適ではありません。

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

-   インデックス構築の進行状況は、 `ROWS_STABLE_INDEXED`と`ROWS_STABLE_NOT_INDEXED`列で確認できます。5が`ROWS_STABLE_NOT_INDEXED`になると、インデックス構築が完了します。

    参考までに、768次元の500MiBベクターデータセットのインデックス作成には最大20分かかる場合があります。インデクサーは複数のテーブルに対して並列実行できます。現在、インデクサーの優先度や速度の調整はサポートされていません。

-   デルタレイヤーの行数は`ROWS_DELTA_NOT_INDEXED`列目で確認できます。TiFlashのstorageレイヤーのデータは、デルタレイヤーとステーブルレイヤーの2つのレイヤーに保存されます。デルタレイヤーには最近挿入または更新された行が保存され、書き込みワークロードに応じて定期的にステーブルレイヤーにマージされます。このマージプロセスはコンパクションと呼ばれます。

    Deltaレイヤーは常にインデックス化されません。最適なパフォーマンスを実現するには、DeltaレイヤーをStableレイヤーに強制的にマージし、すべてのデータがインデックス化されるようにすることができます。

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    詳細については[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)参照してください。

さらに、 `ADMIN SHOW DDL JOBS;`実行して`row count`確認することで、DDLジョブの実行進捗状況を監視できます。ただし、 `row count`値は`TIFLASH_INDEXES`の`rows_stable_indexed`フィールドから取得されるため、この方法は完全に正確ではありません。この方法は、インデックス作成の進捗状況を追跡するための参照として使用できます。

## ベクトルインデックスが使用されているかどうかを確認する {#check-whether-the-vector-index-is-used}

クエリがベクトルインデックスを使用しているかどうかを確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを使用します`TableFullScan`エグゼキュータの`operator info`列に`annIndex:`表示されている場合、このテーブルスキャンはベクトルインデックスを使用していることを意味します。

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

ベクトル インデックスが使用できない場合、原因の調査に役立つ警告が表示される場合があります。

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

ベクトル インデックスの使用方法に関する詳細情報を確認するには、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを実行し、出力の`execution info`列を確認します。

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

> **注記：**
>
> 実行情報は内部情報です。フィールドとフォーマットは予告なく変更される場合があります。これらの情報に依存しないでください。

いくつかの重要なフィールドの説明:

-   `vector_index.load.total` : インデックスの読み込みにかかる合計時間。複数のベクターインデックスが並行して読み込まれる可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
-   `vector_index.load.from_s3` : S3 からロードされたインデックスの数。
-   `vector_index.load.from_disk` : ディスクからロードされたインデックスの数。インデックスは以前にS3からダウンロード済みです。
-   `vector_index.load.from_cache` : キャッシュからロードされたインデックスの数。インデックスは以前にS3からダウンロード済みです。
-   `vector_index.search.total` : インデックス内の検索にかかる合計時間。レイテンシーが大きい場合、通常、インデックスがコールド状態（一度もアクセスされていない、またはかなり前にアクセスされている状態）であるため、インデックス検索時に大量のI/O操作が発生します。複数のベクターインデックスが並列で検索される可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
-   `vector_index.search.discarded_nodes` : 検索中に訪問されたが破棄されたベクトル行の数。これらの破棄されたベクトルは検索結果には考慮されません。この値が大きい場合、通常、 `UPDATE`または`DELETE`ステートメントによって多くの古い行が発生していることを示します。

出力の解釈については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 、および[EXPLAIN コマンド](/explain-walkthrough.md)参照してください。

## 参照 {#see-also}

-   [ベクトル検索のパフォーマンスを向上させる](/vector-search/vector-search-improve-performance.md)
-   [ベクトルデータ型](/vector-search/vector-search-data-types.md)

[^1]: KNN 検索の説明は、ClickHouse ドキュメントの[rschu1ze](https://github.com/rschu1ze)が作成した[近似最近傍検索インデックス](https://github.com/ClickHouse/ClickHouse/pull/50661/files#diff-7ebd9e71df96e74230c9a7e604fa7cb443be69ba5e23bf733fcecd4cc51b7576)ドキュメントに基づいており、Apache License 2.0 に基づいてライセンスされています。

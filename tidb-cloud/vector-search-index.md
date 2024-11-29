---
title: Vector Search Index
summary: ベクトル検索インデックスを構築して使用し、TiDB で K 近傍法 (KNN) クエリを高速化する方法を学びます。
---

# ベクター検索インデックス {#vector-search-index}

K 近傍法 (KNN) 検索は、ベクトル空間内の特定の点に最も近い K 個の点を検索する方法です。KNN 検索を実行する最も簡単な方法は、特定のベクトルと空間内の他のすべてのベクトル間の距離を計算する総当たり検索です。この方法では完全な精度が保証されますが、実用的に使用するには通常は遅すぎます。そのため、KNN 検索では速度と効率を高めるために、近似アルゴリズムが一般的に使用されます。

TiDB では、 [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)の列に対するこのような近似最近傍 (ANN) 検索にベクトル検索インデックスを作成して使用できます。ベクトル検索インデックスを使用すると、ベクトル検索クエリを数ミリ秒で完了できます。

現在、TiDB は[HNSW (階層的にナビゲート可能なスモールワールド)](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)ベクトル検索インデックス アルゴリズムをサポートしています。

## HNSWベクトルインデックスを作成する {#create-the-hnsw-vector-index}

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)は、最も人気のあるベクトル インデックス アルゴリズムの 1 つです。HNSW インデックスは、特定のケースでは最大 98% という比較的高い精度で優れたパフォーマンスを提供します。

TiDB では、次のいずれかの方法で、 [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)列に対して HNSW インデックスを作成できます。

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
> -   テーブルの作成時にベクトル検索インデックスが定義されておらず、テーブルに現在TiFlashレプリカがない場合は、テーブルにベクトル検索インデックスを追加する前に、手動でTiFlashレプリカを作成する必要があります。例: `ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;` 。

HNSW ベクトル インデックスを作成するときは、ベクトルの距離関数を指定する必要があります。

-   コサイン距離: `((VEC_COSINE_DISTANCE(embedding)))`
-   L2距離: `((VEC_L2_DISTANCE(embedding)))`

ベクトル インデックスは、 `VECTOR(3)`として定義された列などの固定次元のベクトル列に対してのみ作成できます。ベクトル距離は同じ次元のベクトル間でのみ計算できるため、固定次元でないベクトル列 ( `VECTOR`として定義された列など) に対しては作成できません。

その他の制限については[ベクトルインデックスの制限](/tidb-cloud/vector-search-limitations.md#vector-index-limitations)参照してください。

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

プレフィルター ( `WHERE`句を使用) を含むクエリは、SQL セマンティクスに従って K 近傍をクエリしていないため、ベクトル インデックスを利用できません。例:

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

大量のデータを挿入した後、その一部がTiFlashに即座に保存されない場合があります。すでに保存されているベクター データの場合、ベクター検索インデックスは同期的に構築されます。まだ保存されていないデータの場合、データが保存されるとインデックスが構築されます。このプロセスは、データの精度と一貫性に影響しません。ベクター検索はいつでも実行でき、完全な結果を得ることができます。ただし、ベクター インデックスが完全に構築されるまで、パフォーマンスは最適ではありません。

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

-   インデックス構築の進行状況は、 `ROWS_STABLE_INDEXED`列と`ROWS_STABLE_NOT_INDEXED`列で確認できます。5 が`ROWS_STABLE_NOT_INDEXED`になると、インデックス構築が完了します。

    参考までに、768 次元の 500 MiB ベクター データセットのインデックス作成には最大 20 分かかる場合があります。インデクサーは複数のテーブルに対して並列実行できます。現在、インデクサーの優先度や速度の調整はサポートされていません。

-   デルタレイヤーの行数は`ROWS_DELTA_NOT_INDEXED`列で確認できます。TiFlash のstorageレイヤーのデータは、デルタレイヤーと安定レイヤーの2 つのレイヤーに保存されます。デルタレイヤーには最近挿入または更新された行が保存され、書き込みワークロードに応じて定期的に安定レイヤーにマージされます。このマージ プロセスは、コンパクションと呼ばれます。

    デルタレイヤーは常にインデックス化されません。最適なパフォーマンスを実現するには、デルタレイヤーを安定レイヤーに強制的にマージして、すべてのデータをインデックス化できるようにします。

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    詳細については[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)参照してください。

さらに、 `ADMIN SHOW DDL JOBS;`実行して`row count`確認することで、 DDL ジョブの実行進行状況を監視できます。ただし、 `row count`値は`TIFLASH_INDEXES`の`rows_stable_indexed`フィールドから取得されるため、この方法は完全に正確ではありません。このアプローチは、インデックス作成の進行状況を追跡するための参照として使用できます。

## ベクトルインデックスが使用されているかどうかを確認する {#check-whether-the-vector-index-is-used}

クエリがベクトル インデックスを使用しているかどうかを確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを使用します。9 `TableFullScan`キュータの`operator info`列に`annIndex:`表示されている場合は、このテーブル スキャンがベクトル インデックスを使用していることを意味します。

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
> 実行情報は内部情報です。フィールドと形式は予告なく変更される可能性があります。これらに依存しないでください。

いくつかの重要なフィールドの説明:

-   `vector_index.load.total` : インデックスのロードにかかる合計時間。複数のベクター インデックスが並行してロードされる可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
-   `vector_index.load.from_s3` : S3 からロードされたインデックスの数。
-   `vector_index.load.from_disk` : ディスクからロードされたインデックスの数。インデックスは以前に S3 からすでにダウンロードされています。
-   `vector_index.load.from_cache` : キャッシュからロードされたインデックスの数。インデックスは以前に S3 からダウンロード済みです。
-   `vector_index.search.total` : インデックスの検索にかかる合計時間。通常、レイテンシーが長いということは、インデックスがコールド状態 (以前に一度もアクセスされていないか、かなり前にアクセスされている) であるため、インデックスを検索するときに I/O 操作が大量に発生することを意味します。複数のベクター インデックスが並行して検索される可能性があるため、このフィールドは実際のクエリ時間よりも長くなる場合があります。
-   `vector_index.search.discarded_nodes` : 検索中に訪問されたが破棄されたベクトル行の数。これらの破棄されたベクトルは検索結果では考慮されません。通常、値が大きい場合は、 `UPDATE`または`DELETE`ステートメントによって古い行が多数あることを示します。

出力の解釈については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 、 [EXPLAIN コマンド](/explain-walkthrough.md)参照してください。

## 制限事項 {#limitations}

[ベクトルインデックスの制限](/tidb-cloud/vector-search-limitations.md#vector-index-limitations)参照。

## 参照 {#see-also}

-   [ベクトル検索のパフォーマンスを向上させる](/tidb-cloud/vector-search-improve-performance.md)
-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)

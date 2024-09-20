---
title: Vector Search Index
summary: ベクトル検索インデックスを構築して使用し、TiDB で K 近傍法 (KNN) クエリを高速化する方法を学びます。
---

# ベクター検索インデックス {#vector-search-index}

K 近傍法 (KNN) 検索は、ベクトル空間内の特定の点に対して K 個の最も近い点を見つける問題です。この問題を解決する最も直接的な方法は、ベクトル空間内のすべての点と参照点の間の距離を計算する総当たり検索です。この方法は完全な精度を保証しますが、実用的に使用するには通常は遅すぎます。そのため、近傍法検索の問題は、多くの場合、近似アルゴリズムで解決されます。

TiDB では、 [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)の列に対する近似最近傍 (ANN) 検索にベクトル検索インデックスを作成して利用できます。ベクトル検索インデックスを使用すると、ベクトル検索クエリを数ミリ秒で完了できます。

TiDB は現在、次のベクトル検索インデックス アルゴリズムをサポートしています。

-   HNSW

> **注記：**
>
> ベクトル検索インデックスは[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対してのみ使用できます。

## HNSWベクトルインデックスを作成する {#create-the-hnsw-vector-index}

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)は、最も人気のあるベクトル インデックス アルゴリズムの 1 つです。HNSW インデックスは、比較的高い精度 (一般的なケースでは 98% 以上) で優れたパフォーマンスを提供します。

HNSW ベクトル インデックスを作成するには、テーブルの作成時に、列のコメントに[ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)インデックス定義を指定します。

```sql
CREATE TABLE vector_table_with_index (
    id INT PRIMARY KEY, doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
);
```

> **注記：**
>
> ベクトル インデックスを作成するための構文は、将来のリリースで変更される可能性があります。

ベクトル インデックスを作成するときは、 `distance=<metric>`構成で距離メトリックを指定する必要があります。

-   コサイン距離: `COMMENT "hnsw(distance=cosine)"`
-   L2距離: `COMMENT "hnsw(distance=l2)"`

ベクトル インデックスは、 `VECTOR(3)`のような固定次元のベクトル列に対してのみ作成できます。ベクトル距離は同じ次元のベクトル間でのみ計算できるため、 `VECTOR`のような混合次元のベクトル列に対しては作成できません。

プログラミング言語 SDK または ORM を使用している場合は、ベクター インデックスの作成について次のドキュメントを参照してください。

-   パイソン: [Python 用 TiDB ベクター SDK](https://github.com/pingcap/tidb-vector-python)
-   パイソン: [SQLアルケミー](/tidb-cloud/vector-search-integrate-with-sqlalchemy.md)
-   パイソン: [ピーウィー](/tidb-cloud/vector-search-integrate-with-peewee.md)
-   パイソン: [ジャンゴ](/tidb-cloud/vector-search-integrate-with-django-orm.md)

ベクトル インデックスを作成するときは、次の制限に注意してください。これらの制限は、将来のリリースで削除される可能性があります。

-   L1 距離と内積は、ベクトル インデックスではまだサポートされていません。

-   ベクトル インデックスは、テーブルの作成時にのみ定義および作成できます。テーブルの作成後に、DDL ステートメントを使用してオンデマンドでベクトル インデックスを作成することはできません。また、DDL ステートメントを使用してベクトル インデックスを削除することもできません。

## ベクトルインデックスを使用する {#use-the-vector-index}

ベクトル検索インデックスは、次のような`ORDER BY ... LIMIT`の形式を使用して、K 近傍検索クエリで使用できます。

```sql
SELECT *
FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
LIMIT 10
```

ベクトル検索でインデックスを利用する場合は、ベクトル インデックスの作成時に定義したのと同じ距離メトリックを使用する必要があります。

## フィルター付きベクトルインデックスを使用する {#use-the-vector-index-with-filters}

プレフィルター ( `WHERE`句を使用) を含むクエリは、SQL セマンティクスに従って K 近傍をクエリしていないため、ベクトル インデックスを利用できません。例:

```sql
-- Filter is performed before kNN, so Vector Index cannot be used:

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

いくつかの回避策は次のとおりです。

**ベクトル検索後のポストフィルタ:**最初に K 近傍をクエリし、次に不要な結果をフィルタリングします。

```sql
-- The filter is performed after kNN for these queries, so Vector Index can be used:

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- Note that this query may return less than 5 results if some are filtered out.
```

**テーブル パーティションの使用**: [テーブルパーティション](/partitioned-table.md)内のクエリはベクトル インデックスを完全に利用できます。等価フィルターを指定されたパーティションへのアクセスに変えることができるため、等価フィルターを実行する場合に役立ちます。

例: 特定の製品バージョンに最も近いドキュメントを見つけたいとします。

```sql
-- Filter is performed before kNN, so Vector Index cannot be used:
SELECT * FROM docs
WHERE ver = "v2.0"
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

`WHERE`句を使用してクエリを記述する代わりに、テーブルをパーティション分割し、 [`PARTITION`キーワード](/partitioned-table.md#partition-selection)使用してパーティション内でクエリを実行できます。

```sql
CREATE TABLE docs (
    id INT,
    ver VARCHAR(10),
    doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
) PARTITION BY LIST COLUMNS (ver) (
    PARTITION p_v1_0 VALUES IN ('v1.0'),
    PARTITION p_v1_1 VALUES IN ('v1.1'),
    PARTITION p_v1_2 VALUES IN ('v1.2'),
    PARTITION p_v2_0 VALUES IN ('v2.0')
);

SELECT * FROM docs
PARTITION (p_v2_0)
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

詳細については[テーブルパーティション](/partitioned-table.md)参照してください。

## インデックス構築の進行状況をビュー {#view-index-build-progress}

他のインデックスとは異なり、ベクター インデックスは非同期的に構築されます。したがって、ベクター インデックスは、一括データ挿入後すぐには利用できない場合があります。これはデータの正確性や一貫性には影響せず、いつでもベクター検索を実行して完全な結果を得ることができます。ただし、ベクター インデックスが完全に構築されるまで、パフォーマンスは最適ではありません。

インデックス構築の進行状況を表示するには、次のように`INFORMATION_SCHEMA.TIFLASH_INDEXES`テーブルをクエリします。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TIDB_PARTITION | TABLE_ID | BELONGING_TABLE_ID | COLUMN_NAME | COLUMN_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | TIFLASH_INSTANCE |
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
| test          | sample     | NULL           |      106 |                 -1 | vec         |         2 | HNSW       |                   0 |                   13000 |                  0 |                   2000 | store-6ba728d2   |
| test          | sample     | NULL           |      106 |                 -1 | vec         |         2 | HNSW       |               10500 |                       0 |                  0 |                   4500 | store-7000164f   |
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
```

-   `ROWS_STABLE_INDEXED`列と`ROWS_STABLE_NOT_INDEXED`列はインデックス構築の進行状況を示します。5 が`ROWS_STABLE_NOT_INDEXED`になると、インデックス構築が完了します。

    参考までに、500 MiB のベクター データセットのインデックス作成には最大 20 分かかる場合があります。インデクサーは複数のテーブルに対して並列実行できます。現在、インデクサーの優先度や速度の調整はサポートされていません。

-   `ROWS_DELTA_NOT_INDEXED`列目は、デルタレイヤーの行数を示します。デルタレイヤーには*最近*挿入または更新された行が格納され、書き込みワークロードに応じて定期的に安定レイヤーにマージされます。このマージ プロセスは、圧縮と呼ばれます。

    デルタレイヤーは常にインデックス化されません。最適なパフォーマンスを実現するには、デルタレイヤーを安定レイヤーに強制的にマージして、すべてのデータをインデックス化できるようにします。

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    詳細については[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)参照してください。

## ベクトルインデックスが使用されているかどうかを確認する {#check-whether-the-vector-index-is-used}

[`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを使用して、このクエリがベクトル インデックスを使用しているかどうかを確認します。9 `TableFullScan`エグゼキュータの`operator info`列に`annIndex:`が表示されている場合は、このテーブル スキャンがベクトル インデックスを利用していることを意味します。

**例: ベクトルインデックスが使用される**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
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
     -> ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]');
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
-- Using a wrong distance metric:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_l2_Distance(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- Using a wrong order:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## ベクトル検索のパフォーマンスを分析する {#analyze-vector-search-performance}

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)文には、 `execution info`列でベクトル インデックスがどのように使用されるかについての詳細情報が含まれています。

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
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

-   `vector_index.load.total` : インデックスのロードにかかる合計時間。複数のベクトル インデックスが並行してロードされる可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
-   `vector_index.load.from_s3` : S3 からロードされたインデックスの数。
-   `vector_index.load.from_disk` : ディスクからロードされたインデックスの数。インデックスは以前に S3 からすでにダウンロードされています。
-   `vector_index.load.from_cache` : キャッシュからロードされたインデックスの数。インデックスは以前に S3 からすでにダウンロードされています。
-   `vector_index.search.total` : インデックスの検索にかかる合計時間。レイテンシーが大きいということは、通常、インデックスがコールド状態 (以前に一度もアクセスされていないか、かなり前にアクセスされている) であるため、インデックスを検索するときに IO が大量に発生することを意味します。複数のベクター インデックスが並行して検索される可能性があるため、このフィールドは実際のクエリ時間よりも長くなる可能性があります。
-   `vector_index.search.discarded_nodes` : 検索中に訪問されたが破棄されたベクター行の数。これらの破棄されたベクターは検索結果では考慮されません。通常、値が大きい場合は、UPDATE または DELETE ステートメントによって古い行が多数あることを示します。

出力の解釈については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 、 [EXPLAIN コマンド](/explain-walkthrough.md)参照してください。

## 参照 {#see-also}

-   [ベクトル検索のパフォーマンスを向上させる](/tidb-cloud/vector-search-improve-performance.md)
-   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)

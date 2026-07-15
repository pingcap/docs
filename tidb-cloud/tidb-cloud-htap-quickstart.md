---
title: TiDB Cloud HTAP Quick Start
summary: TiDB Cloudで HTAP を使い始める方法を学習します。
aliases: ['/ja/tidbcloud/use-htap-cluster']
---

# TiDB Cloud HTAP クイックスタート {#tidb-cloud-htap-quick-start}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) は、ハイブリッドトランザクションおよび分析処理を意味します。TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースストレージエンジン[TiKV](https://tikv.org)と、分析処理用に設計された列指向ストレージエンジン[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されています。アプリケーションデータはまず TiKV に保存され、その後Raftコンセンサスアルゴリズムを介してTiFlashに複製されます。つまり、行ベースストレージから列指向ストレージへのリアルタイムレプリケーションです。

このチュートリアルでは、 TiDB Cloudのハイブリッドトランザクションおよび分析処理（HTAP）機能を簡単に体験する方法をご案内します。TiFlashへのテーブルのレプリケーション方法、 TiFlashを使用したクエリの実行方法、そしてパフォーマンス向上の体験方法などについて説明します。

## 始める前に {#before-you-begin}

HTAP 機能を試す前に、[TiDB Cloudクイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)に従って {{{ .starter }}} インスタンスを作成し、次のようにデータ（このドキュメントでは **Steam Games Dataset 2021-2025** を例として使用します）をインスタンスにインポートします。

1. Kaggle から [Steam Games Dataset 2021-2025](https://www.kaggle.com/datasets/jypenpen54534/steam-games-dataset-2021-2025-65k) をダウンロードします。
2. {{{ .starter }}} インスタンスの **Import** ページを開きます。

    1. [TiDB Cloudコンソール](https://tidbcloud.com/) で [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .starter }}} インスタンス名をクリックして概要ページに移動します。
    2. 概要ページの左側のナビゲーションペインで、**Data** > **Import** をクリックします。

3. ダウンロードした CSV ファイルを {{{ .starter }}} インスタンスにインポートします。

    1. **Import** ページで **Upload a local file** をクリックし、ダウンロードした CSV ファイルを選択してアップロードします。
    2. **Destination** セクションで、**Database** フィールドに `steam`、**Table** フィールドに `games` を入力します。
    3. **Define Table** をクリックし、カラム `categories` のデータ型を `TEXT` に変更してから、カラム `developer` のデータ型を `TEXT` に変更します。
    4. **Start Import** をクリックします。

        **Import Task Detail** ページでインポートの進行状況を確認できます。

## 手順 {#steps}

### ステップ1. サンプルデータを列指向ストレージエンジンに複製する {#step-1-replicate-the-sample-data-to-the-columnar-storage-engine}

{{{ .starter }}} インスタンスを作成した後、TiDB はデフォルトでは TiKV から TiFlash にデータを複製しません。対象のテーブルを TiFlash に複製するには、MySQL クライアントを使用して {{{ .starter }}} インスタンスに接続し、DDL 文を実行します。TiDB はその後、指定されたテーブルのレプリカを TiFlash に作成します。

たとえば、`games` テーブル（**Steam Games Dataset 2021-2025** から）を TiFlash に複製するには、次のステートメントを実行します。

```sql
USE steam;
```

```sql
ALTER TABLE games SET TIFLASH REPLICA 2;
```

レプリケーションの進行状況を確認するには、次のステートメントを実行します。

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ID, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'steam' AND TABLE_NAME = 'games';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| steam        | games      |      227 |             2 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.24 sec)
```

上記のステートメントの結果は次のようになります。

-   `AVAILABLE` 、特定のテーブルのTiFlashレプリカが利用可能かどうかを示します。2 `1`利用可能、 `0`利用不可を意味します。レプリカが利用可能になると、このステータスは変更されません。
-   `PROGRESS`レプリケーションの進行状況を表します。値は`0`から`1`までです。6 `1`少なくとも1つのレプリカがレプリケートされていることを意味します。

### ステップ2. HTAPを使用してデータをクエリする {#step-2-query-data-using-htap}

レプリケーションが完了したら、クエリを実行できます。

たとえば、毎年リリースされるゲームの数、平均価格、および平均推奨数を確認できます。

```sql
SELECT
  `release_year`,
  COUNT(*) AS `games_released`,
  AVG(`price`) AS `average_price`,
  AVG(`recommendations`) AS `average_recommendations`
FROM
  `games`
WHERE
  `release_year` IS NOT NULL
GROUP BY
  `release_year`
ORDER BY
  `release_year` DESC;
```

### ステップ3. 行ベースのストレージと列ベースのストレージのクエリパフォーマンスを比較する {#step-3-compare-the-query-performance-between-row-based-storage-and-columnar-storage}

このステップでは、TiKV (行ベースのストレージ) とTiFlash (列ベースのストレージ) 間の実行統計を比較できます。

-   TiKV を使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[games]) */
      `release_year`,
      `genres`,
      `developer`,
      COUNT(*) AS `games_released`,
      SUM(`recommendations`) AS `total_recommendations`,
      AVG(`recommendations`) AS `average_recommendations`,
      AVG(`price`) AS `average_price`,
      MAX(`recommendations`) AS `max_recommendations`
    FROM
      `games`
    WHERE
      `release_year` IS NOT NULL
      AND `genres` IS NOT NULL
      AND `developer` IS NOT NULL
    GROUP BY
      `release_year`,
      `genres`,
      `developer`
    HAVING
      COUNT(*) >= 2
    ORDER BY
      `total_recommendations` DESC,
      `games_released` DESC
    LIMIT 20;
    ```

    TiFlashレプリカを持つテーブルの場合、TiDBオプティマイザーはコスト見積もりに基づいて、TiKVレプリカとTiFlashレプリカのどちらを使用するかを自動的に決定します。前述の`EXPLAIN ANALYZE`の文では、 `/*+ READ_FROM_STORAGE(TIKV[games]) */`ヒントを使用してオプティマイザーにTiKVを選択させ、TiKVの実行統計を確認できるようにしています。

    > **注記：**
    >
    > MySQL 5.7.7より前のコマンドラインクライアントは、デフォルトでオプティマイザヒントを削除します。これらの以前のバージョンで`Hint`構文を使用している場合は、クライアントの起動時に`--comments`オプションを追加してください。例： `mysql -h 127.0.0.1 -P 4000 -uroot --comments`

    出力では、 `execution info`列から実行時間を取得できます。

    ```sql
    id                                | estRows  | actRows | task      | access object | execution info                              | operator info                              | memory   | disk
    ----------------------------------+----------+---------+-----------+---------------+---------------------------------------------+--------------------------------------------+----------+---------
    Projection_10                     | 20.00    | 20      | root      |               | time:234.4ms, loops:2, RU:241.66, ...       | steam.games.release_year, ...              | 6.03 KB  | N/A
    └─TopN_13                         | 20.00    | 20      | root      |               | time:234.4ms, loops:2                       | Column#13:desc, Column#12:desc, ...        | 12.6 KB  | 0 Bytes
      └─Selection_18                  | 36774.40 | 2458    | root      |               | time:233.9ms, loops:5                       | ge(Column#12, ?)                           | 187.0 KB | N/A
        └─HashAgg_22                  | 45968.00 | 59883   | root      |               | time:228.4ms, loops:62, partial_worker:...  | group by:Column#39, Column#40, ...         | 31.7 MB  | 0 Bytes
          └─Projection_38             | 65521.00 | 65521   | root      |               | time:142.9ms, loops:66, Concurrency:5       | cast(steam.games.recommendations, ...      | 1.16 MB  | N/A
            └─TableReader_32          | 65521.00 | 65521   | root      |               | time:49.5ms, loops:66, cop_task:{num:9...   | data:Selection_31                          | 3.26 MB  | N/A
              └─Selection_31          | 65521.00 | 65521   | cop[tikv] |               | tikv_task:{proc max:20ms, min:0s, ...       | not(isnull(steam.games.developer)), ...    | N/A      | N/A
                └─TableFullScan_30    | 65521.00 | 65521   | cop[tikv] | table:games   | tikv_task:{proc max:10ms, min:0s, ...       | keep order:false                           | N/A      | N/A
    (8 rows)
    ```

-   TiFlashを使用してこのクエリの実行統計を取得するには、`/*+ READ_FROM_STORAGE(TIKV[games]) */` ヒントを付けずに同じステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT
      `release_year`,
      `genres`,
      `developer`,
      COUNT(*) AS `games_released`,
      SUM(`recommendations`) AS `total_recommendations`,
      AVG(`recommendations`) AS `average_recommendations`,
      AVG(`price`) AS `average_price`,
      MAX(`recommendations`) AS `max_recommendations`
    FROM
      `games`
    WHERE
      `release_year` IS NOT NULL
      AND `genres` IS NOT NULL
      AND `developer` IS NOT NULL
    GROUP BY
      `release_year`,
      `genres`,
      `developer`
    HAVING
      COUNT(*) >= 2
    ORDER BY
      `total_recommendations` DESC,
      `games_released` DESC
    LIMIT 20;
    ```

    出力では、 `execution info`列から実行時間を取得できます。

    ```sql
    id                                      | estRows  | actRows | task         | access object | execution info                              | operator info                              | memory  | disk
    ----------------------------------------+----------+---------+--------------+---------------+---------------------------------------------+--------------------------------------------+---------+---------
    Projection_10                           | 20.00    | 20      | root         |               | time:92.5ms, loops:2, RU:120.42, ...        | steam.games.release_year, ...              | 6.03 KB | N/A
    └─TopN_14                               | 20.00    | 20      | root         |               | time:92.4ms, loops:2                        | Column#13:desc, Column#12:desc, ...        | 4.32 KB | 0 Bytes
      └─TableReader_68                      | 20.00    | 20      | root         |               | time:92.4ms, loops:2, cop_task:{num:2...    | MppVersion: 2, data:ExchangeSender_67      | 7.99 KB | N/A
        └─ExchangeSender_67                 | 20.00    | 20      | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | ExchangeType: PassThrough                  | N/A     | N/A
          └─TopN_66                         | 20.00    | 20      | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | Column#13:desc, Column#12:desc, ...        | N/A     | N/A
            └─Selection_65                  | 36774.40 | 2458    | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | ge(Column#12, ?)                           | N/A     | N/A
              └─Projection_58               | 45968.00 | 59883   | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | Column#12, Column#13, div(Column#14, ...   | N/A     | N/A
                └─HashAgg_56                | 45968.00 | 59883   | mpp[tiflash] |               | tiflash_task:{time:71ms, loops:1, ...       | group by:Column#79, Column#80, ...         | N/A     | N/A
                  └─Projection_71           | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31ms, loops:7, ...       | cast(steam.games.recommendations, ...      | N/A     | N/A
                    └─ExchangeReceiver_41   | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31ms, loops:7, ...       |                                            | N/A     | N/A
                      └─ExchangeSender_40   | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31.2ms, loops:7, ...     | ExchangeType: HashPartition, ...           | N/A     | N/A
                        └─Selection_39      | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:21.2ms, loops:7, ...     | not(isnull(steam.games.developer)), ...    | N/A     | N/A
                          └─TableFullScan_38| 65521.00 | 65521   | mpp[tiflash] | table:games   | tiflash_task:{time:21.2ms, loops:7, ...     | pushed down filter:empty, keep order:false | N/A     | N/A
    (13 rows)
    ```

> **注記：**
>
> サンプルデータセットは小さく、このドキュメントのクエリは比較的単純であるため、このクエリに対してオプティマイザーにTiKVを選択させてから同じクエリを再度実行すると、TiKV はキャッシュを再利用するため、クエリは大幅に高速になります。データが頻繁に更新される場合、キャッシュは無効になります。

## もっと詳しく知る {#learn-more}

-   [TiFlashの概要](/tiflash/tiflash-overview.md)
-   [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)
-   [TiFlashからデータを読み取る](/tiflash/use-tidb-to-read-tiflash.md)
-   [MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)
-   [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)

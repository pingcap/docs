---
title: TiDB Cloud HTAP Quick Start
summary: TiDB Cloudで HTAP を使い始める方法を学習します。
aliases: ['/ja/tidbcloud/use-htap-cluster']
---

# TiDB Cloud HTAP クイックスタート {#tidb-cloud-htap-quick-start}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 、ハイブリッドトランザクションおよび分析処理を意味します。TiDB TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースstorageエンジン[TiKV](https://tikv.org)と、分析処理用に設計された列指向storage[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されています。アプリケーションデータはまず TiKV に保存され、その後Raftコンセンサスアルゴリズムを介してTiFlashに複製されます。つまり、行ベースstorageから列指向storageへのリアルタイムレプリケーションです。

このチュートリアルでは、 TiDB Cloudのハイブリッドトランザクションおよび分析処理（HTAP）機能を簡単に体験する方法をご案内します。TiFlashへのテーブルのレプリケーション方法、 TiFlashを使用したクエリの実行方法、そしてパフォーマンス向上の体験方法などについて説明します。

## 始める前に {#before-you-begin}

HTAP 機能を体験する前に、 [TiDB Cloudクイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)に従ってTiDB Cloud Serverless クラスターを作成し、 **Steam Game Stats**サンプル データセットをクラスターにインポートします。

## 手順 {#steps}

### ステップ1. サンプルデータを列指向storageエンジンに複製する {#step-1-replicate-the-sample-data-to-the-columnar-storage-engine}

TiFlashノードを含むクラスターを作成した後、TiKVはデフォルトではTiFlashにデータを複製しません。複製するテーブルを指定するには、TiDBのMySQLクライアントでDDL文を実行する必要があります。その後、TiDBは指定されたテーブルのレプリカをTiFlashに作成します。

たとえば、 `games`テーブル ( **Steam Game Stats**サンプル データセット内) をTiFlashに複製するには、次のステートメントを実行します。

```sql
USE game;
```

```sql
ALTER TABLE games SET TIFLASH REPLICA 2;
```

レプリケーションの進行状況を確認するには、次のステートメントを実行します。

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ID, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'game' and TABLE_NAME = 'games';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| game         | games      |       88 |             2 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.20 sec)
```

上記のステートメントの結果は次のようになります。

-   `AVAILABLE` 、特定のテーブルのTiFlashレプリカが利用可能かどうかを示します。2 `1`利用可能、 `0`利用不可を意味します。レプリカが利用可能になると、このステータスは変更されません。
-   `PROGRESS`レプリケーションの進行状況を表します。値は`0`から`1`までです。6 `1`少なくとも1つのレプリカがレプリケートされていることを意味します。

### ステップ2. HTAPを使用してデータをクエリする {#step-2-query-data-using-htap}

レプリケーションのプロセスが完了したら、いくつかのクエリの実行を開始できます。

たとえば、毎年リリースされるゲームの数、平均価格、平均プレイ時間を確認できます。

```sql
SELECT
  YEAR(`release_date`) AS `release_year`,
  COUNT(*) AS `games_released`,
  AVG(`price`) AS `average_price`,
  AVG(`average_playtime_forever`) AS `average_playtime`
FROM
  `games`
GROUP BY
  `release_year`
ORDER BY
  `release_year` DESC;
```

### ステップ3. 行ベースのstorageと列ベースのstorageのクエリパフォーマンスを比較する {#step-3-compare-the-query-performance-between-row-based-storage-and-columnar-storage}

このステップでは、TiKV (行ベースのstorage) とTiFlash (列ベースのstorage) 間の実行統計を比較できます。

-   TiKV を使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[games]) */
      YEAR(`release_date`) AS `release_year`,
      COUNT(*) AS `games_released`,
      AVG(`price`) AS `average_price`,
      AVG(`average_playtime_forever`) AS `average_playtime`
    FROM
      `games`
    GROUP BY
      `release_year`
    ORDER BY
      `release_year` DESC;
    ```

    TiFlashレプリカを持つテーブルの場合、TiDBオプティマイザーはコスト見積もりに基づいて、TiKVレプリカとTiFlashレプリカのどちらを使用するかを自動的に決定します。前述の`EXPLAIN ANALYZE`の文では、 `/*+ READ_FROM_STORAGE(TIKV[games]) */`ヒントを使用してオプティマイザーにTiKVを選択させ、TiKVの実行統計を確認できるようにしています。

    > **注記：**
    >
    > MySQL 5.7.7より前のコマンドラインクライアントは、デフォルトでオプティマイザヒントを削除します。これらの以前のバージョンで`Hint`構文を使用している場合は、クライアントの起動時に`--comments`オプションを追加してください。例： `mysql -h 127.0.0.1 -P 4000 -uroot --comments`

    出力では、 `execution info`列目から実行時間を取得できます。

    ```sql
    id                         | estRows  | actRows | task      | access object | execution info                             | operator info                                 | memory  | disk    
    ---------------------------+----------+---------+-----------+---------------+--------------------------------------------+-----------------------------------------------+---------+---------
    Sort_5                     | 4019.00  | 28      | root      |               | time:672.7ms, loops:2, RU:1159.679690      | Column#36:desc                                | 18.0 KB | 0 Bytes 
    └─Projection_7             | 4019.00  | 28      | root      |               | time:672.7ms, loops:6, Concurrency:5       | year(game.games.release_date)->Column#36, ... | 35.5 KB | N/A     
      └─HashAgg_15             | 4019.00  | 28      | root      |               | time:672.6ms, loops:6, partial_worker:...  | group by:Column#38, funcs:count(Column#39)... | 56.7 KB | N/A     
        └─TableReader_16       | 4019.00  | 28      | root      |               | time:672.4ms, loops:2, cop_task: {num:...  | data:HashAgg_9                                | 3.60 KB | N/A     
          └─HashAgg_9          | 4019.00  | 28      | cop[tikv] |               | tikv_task:{proc max:300ms, min:0s, avg...  | group by:year(game.games.release_date), ...   | N/A     | N/A     
            └─TableFullScan_14 | 68223.00 | 68223   | cop[tikv] | table:games   | tikv_task:{proc max:290ms, min:0s, avg...  | keep order:false                              | N/A     | N/A     
    (6 rows)
    ```

-   TiFlashを使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT
      YEAR(`release_date`) AS `release_year`,
      COUNT(*) AS `games_released`,
      AVG(`price`) AS `average_price`,
      AVG(`average_playtime_forever`) AS `average_playtime`
    FROM
      `games`
    GROUP BY
      `release_year`
    ORDER BY
      `release_year` DESC;
    ```

    出力では、 `execution info`列目から実行時間を取得できます。

    ```sql
    id                                   | estRows  | actRows | task         | access object | execution info                                        | operator info                              | memory  | disk    
    -------------------------------------+----------+---------+--------------+---------------+-------------------------------------------------------+--------------------------------------------+---------+---------
    Sort_5                               | 4019.00  | 28      | root         |               | time:222.2ms, loops:2, RU:25.609675                   | Column#36:desc                             | 3.77 KB | 0 Bytes 
    └─TableReader_39                     | 4019.00  | 28      | root         |               | time:222.1ms, loops:2, cop_task: {num: 2, max: 0s,... | MppVersion: 1, data:ExchangeSender_38      | 4.64 KB | N/A     
      └─ExchangeSender_38                | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | ExchangeType: PassThrough                  | N/A     | N/A     
        └─Projection_8                   | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | year(game.games.release_date)->Column#3... | N/A     | N/A     
          └─Projection_34                | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | Column#33, div(Column#34, cast(case(eq(... | N/A     | N/A     
            └─HashAgg_35                 | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | group by:Column#63, funcs:sum(Column#64... | N/A     | N/A     
              └─ExchangeReceiver_37      | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:8}       |                                            | N/A     | N/A     
                └─ExchangeSender_36      | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:1, threads:1}       | ExchangeType: HashPartition, Compressio... | N/A     | N/A     
                  └─HashAgg_33           | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:1, threads:1}       | group by:Column#75, funcs:count(1)->Col... | N/A     | N/A     
                    └─Projection_40      | 68223.00 | 68223   | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:2, threads:8}       | game.games.price, game.games.price, gam... | N/A     | N/A     
                      └─TableFullScan_23 | 68223.00 | 68223   | mpp[tiflash] | table:games   | tiflash_task:{time:210.6ms, loops:2, threads:8}, ...  | keep order:false                           | N/A     | N/A     
    (11 rows)
    ```

> **注記：**
>
> サンプルデータのサイズが小さく、このドキュメントのクエリは非常に単純なため、このクエリに対してオプティマイザーにTiKVを選択させ、同じクエリを再度実行すると、TiKVはキャッシュを再利用するため、クエリの速度が大幅に向上する可能性があります。ただし、データが頻繁に更新される場合は、キャッシュが失われる可能性があります。

## もっと詳しく知る {#learn-more}

-   [TiFlashの概要](/tiflash/tiflash-overview.md)
-   [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)
-   [TiFlashからデータを読み取る](/tiflash/use-tidb-to-read-tiflash.md)
-   [MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)
-   [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)

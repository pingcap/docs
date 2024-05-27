---
title: TiDB Cloud HTAP Quick Start
summary: TiDB Cloudで HTAP を使い始める方法を学習します。
---

# TiDB Cloud HTAP クイックスタート {#tidb-cloud-htap-quick-start}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 、ハイブリッド トランザクションおよび分析処理を意味します。TiDB TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースのstorageエンジンである[ティクヴ](https://tikv.org)と、分析処理用に設計された列指向storageである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されています。アプリケーション データは最初に TiKV に保存され、次にRaftコンセンサス アルゴリズムを介してTiFlashに複製されます。つまり、行ベースのstorageから列指向storageへのリアルタイムのレプリケーションです。

このチュートリアルでは、 TiDB Cloudのハイブリッド トランザクションおよび分析処理 (HTAP) 機能を簡単に体験する方法を説明します。内容には、テーブルをTiFlashに複製する方法、 TiFlashを使用してクエリを実行する方法、パフォーマンスの向上を体験する方法などが含まれます。

## あなたが始める前に {#before-you-begin}

HTAP 機能を体験する前に、 [TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md)に従ってTiFlashノードを含むクラスターを作成し、TiDB クラスターに接続し、Capital Bikeshare サンプル データをクラスターにインポートします。

## 手順 {#steps}

### ステップ1. サンプルデータを列指向storageエンジンに複製する {#step-1-replicate-the-sample-data-to-the-columnar-storage-engine}

TiFlashノードを含むクラスターが作成された後、TiKV はデフォルトでデータをTiFlashに複製しません。複製するテーブルを指定するには、TiDB の MySQL クライアントで DDL ステートメントを実行する必要があります。その後、TiDB はそれに応じて指定されたテーブルのレプリカをTiFlashに作成します。

たとえば、 `trips`テーブル (Capital Bikeshare サンプル データ内) をTiFlashに複製するには、次のステートメントを実行します。

```sql
USE bikeshare;
```

```sql
ALTER TABLE trips SET TIFLASH REPLICA 1;
```

レプリケーションの進行状況を確認するには、次のステートメントを実行します。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bikeshare' and TABLE_NAME = 'trips';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+------------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS | TABLE_MODE |
+--------------+------------+----------+---------------+-----------------+-----------+----------+------------+
| bikeshare    | trips      |       88 |             1 |                 |         1 |        1 | NORMAL     |
+--------------+------------+----------+---------------+-----------------+-----------+----------+------------+
1 row in set (0.20 sec)
```

上記のステートメントの結果は次のようになります。

-   `AVAILABLE` 、特定のテーブルのTiFlashレプリカが使用可能かどうかを示します。2 `1`使用可能、 `0`使用不可を意味します。レプリカが使用可能になると、このステータスは変更されなくなります。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は`0`から`1`の間です。6 `1`少なくとも 1 つのレプリカがレプリケートされていることを意味します。

### ステップ2. HTAPを使用してデータをクエリする {#step-2-query-data-using-htap}

レプリケーションのプロセスが完了したら、いくつかのクエリの実行を開始できます。

たとえば、出発駅と到着駅ごとに旅行回数を確認できます。

```sql
SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
GROUP BY start_station_name, end_station_name
ORDER BY count ASC;
```

### ステップ3. 行ベースのstorageと列ベースのstorageのクエリパフォーマンスを比較する {#step-3-compare-the-query-performance-between-row-based-storage-and-columnar-storage}

このステップでは、TiKV (行ベースのstorage) とTiFlash (列ベースのstorage) の実行統計を比較できます。

-   TiKV を使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[trips]) */ start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

    TiFlashレプリカを持つテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいて TiKV レプリカとTiFlashレプリカのどちらを使用するかを自動的に決定します。前の`EXPLAIN ANALYZE`ステートメントでは、 `HINT /*+ READ_FROM_STORAGE(TIKV[trips]) */`を使用してオプティマイザーに TiKV を選択させ、TiKV の実行統計を確認できるようにしています。

    > **注記：**
    >
    > 5.7.7 より前の MySQL コマンドライン クライアントは、デフォルトでオプティマイザ ヒントを削除します。これらの以前のバージョンで`Hint`構文を使用している場合は、クライアントの起動時に`--comments`オプションを追加します。例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

    出力では、 `execution info`列目から実行時間を取得できます。

    ```sql
    id                         | estRows   | actRows | task      | access object | execution info                            | operator info                                | memory  | disk
    ---------------------------+-----------+---------+-----------+---------------+-------------------------------------------+-----------------------------------------------+---------+---------
    Sort_5                     | 633.00    | 73633   | root      |               | time:1.62s, loops:73                      | Column#15                                    | 6.88 MB | 0 Bytes
    └─Projection_7             | 633.00    | 73633   | root      |               | time:1.57s, loops:76, Concurrency:OFF...  | bikeshare.trips.start_station_name...        | 6.20 MB | N/A                                                                                                                                        | 6.20 MB | N/A
      └─HashAgg_15             | 633.00    | 73633   | root      |               | time:1.57s, loops:76, partial_worker:...  | group by:bikeshare.trips.end_station_name... | 58.0 MB | N/A
        └─TableReader_16       | 633.00    | 111679  | root      |               | time:1.34s, loops:3, cop_task: {num: ...  | data:HashAgg_8                               | 7.55 MB | N/A
          └─HashAgg_8          | 633.00    | 111679  | cop[tikv] |               | tikv_task:{proc max:830ms, min:470ms,...  | group by:bikeshare.trips.end_station_name... | N/A     | N/A
            └─TableFullScan_14 | 816090.00 | 816090  | cop[tikv] | table:trips   | tikv_task:{proc max:490ms, min:310ms,...  | keep order:false                             | N/A     | N/A
    (6 rows)
    ```

-   TiFlashを使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

    出力では、 `execution info`列目から実行時間を取得できます。

    ```sql
    id                                 | estRows   | actRows | task         | access object | execution info                            | operator info                      | memory  | disk
    -----------------------------------+-----------+---------+--------------+---------------+-------------------------------------------+------------------------------------+---------+---------
    Sort_5                             | 633.00    | 73633   | root         |               | time:420.2ms, loops:73                    | Column#15                          | 5.61 MB | 0 Bytes
    └─Projection_7                     | 633.00    | 73633   | root         |               | time:368.7ms, loops:73, Concurrency:OFF   | bikeshare.trips.start_station_...  | 4.94 MB | N/A
      └─TableReader_34                 | 633.00    | 73633   | root         |               | time:368.6ms, loops:73, cop_task: {num... | data:ExchangeSender_33             | N/A     | N/A
        └─ExchangeSender_33            | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:360.7ms, loops:1,...   | ExchangeType: PassThrough          | N/A     | N/A
          └─Projection_29              | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:330.7ms, loops:1,...   | Column#15, bikeshare.trips.star... | N/A     | N/A
            └─HashAgg_30               | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:330.7ms, loops:1,...   | group by:bikeshare.trips.end_st... | N/A     | N/A
              └─ExchangeReceiver_32    | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:280.7ms, loops:12,...  |                                    | N/A     | N/A
                └─ExchangeSender_31    | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:272.3ms, loops:256,... | ExchangeType: HashPartition, Ha... | N/A     | N/A
                  └─HashAgg_12         | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:252.3ms, loops:256,... | group by:bikeshare.trips.end_st... | N/A     | N/A
                    └─TableFullScan_28 | 816090.00 | 816090  | mpp[tiflash] | table:trips   | tiflash_task:{time:92.3ms, loops:16,...   | keep order:false                   | N/A     | N/A
    (10 rows)
    ```

> **注記：**
>
> サンプル データのサイズが小さく、このドキュメントのクエリは非常に単純なため、このクエリに対してオプティマイザーに TiKV を選択させてから同じクエリを再度実行すると、TiKV はキャッシュを再利用するため、クエリの速度が大幅に向上する可能性があります。データが頻繁に更新されると、キャッシュが失われます。

## もっと詳しく知る {#learn-more}

-   [TiFlashの概要](/tiflash/tiflash-overview.md)
-   [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)
-   [TiFlashからデータを読み取る](/tiflash/use-tidb-to-read-tiflash.md)
-   [MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)
-   [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)

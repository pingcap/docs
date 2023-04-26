---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with HTAP in TiDB Cloud.
aliases: ['/tidbcloud/use-htap-cluster']
---

# TiDB CloudHTAP クイック スタート {#tidb-cloud-htap-quick-start}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)はハイブリッド トランザクションおよび分析処理を意味します。 TiDB Cloudの HTAP クラスターは、トランザクション処理用に設計された行ベースのstorageエンジン[TiKV](https://tikv.org)と、分析処理用に設計された列型storage[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されます。アプリケーション データはまず TiKV に保存され、次にRaftコンセンサス アルゴリズムを介してTiFlashに複製されます。つまり、行storageから列storageへのリアルタイム レプリケーションです。

このチュートリアルでは、 TiDB Cloudの Hybrid Transactional and Analytical Processing (HTAP) 機能を体験する簡単な方法について説明します。このコンテンツには、テーブルをTiFlashにレプリケートする方法、 TiFlashでクエリを実行する方法、およびパフォーマンスの向上を体験する方法が含まれています。

## あなたが始める前に {#before-you-begin}

HTAP 機能を体験する前に、 [TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md)に従ってTiFlashノードを含むクラスターを作成し、TiDB クラスターに接続して、Capital Bikeshare サンプル データをクラスターにインポートします。

## 手順 {#steps}

### 手順 1. サンプル データを列指向storageエンジンにレプリケートする {#step-1-replicate-the-sample-data-to-the-columnar-storage-engine}

TiFlashノードを持つクラスターが作成された後、TiKV はデフォルトでデータをTiFlashに複製しません。レプリケートするテーブルを指定するには、TiDB の MySQL クライアントで DDL ステートメントを実行する必要があります。その後、TiDB はそれに応じて指定されたテーブルのレプリカをTiFlashに作成します。

たとえば、 `trips`テーブル (Capital Bikeshare サンプル データ内) をTiFlashにレプリケートするには、次のステートメントを実行します。

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

前述のステートメントの結果:

-   `AVAILABLE`特定のテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`利用可能であることを意味し、 `0`利用できないことを意味します。レプリカが使用可能になると、このステータスは変更されなくなります。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は`0` ～ `1`です。 `1`少なくとも 1 つのレプリカが複製されていることを意味します。

### ステップ 2. HTAP を使用してデータを照会する {#step-2-query-data-using-htap}

レプリケーションのプロセスが完了したら、いくつかのクエリの実行を開始できます。

たとえば、さまざまな出発駅と到着駅での乗車数を確認できます。

```sql
SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
GROUP BY start_station_name, end_station_name
ORDER BY count ASC;
```

### ステップ 3. 行ベースのstorageと列指向のstorageのクエリ パフォーマンスを比較する {#step-3-compare-the-query-performance-between-row-based-storage-and-columnar-storage}

このステップでは、TiKV (行ベースのstorage) とTiFlash (列型storage) の実行統計を比較できます。

-   TiKV を使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[trips]) */ start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

    TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザーは、コストの見積もりに基づいて、TiKV またはTiFlashレプリカのどちらを使用するかを自動的に決定します。上記の`EXPLAIN ANALYZE`ステートメントでは、TiKV の実行統計を確認できるように、オプティマイザーに強制的に TiKV を選択させるために`HINT /*+ READ_FROM_STORAGE(TIKV[trips]) */`が使用されています。

    > **ノート：**
    >
    > 5.7.7 より前の MySQL コマンドライン クライアントは、デフォルトでオプティマイザ ヒントを取り除きます。これらの以前のバージョンで`Hint`構文を使用している場合は、クライアントの起動時に`--comments`オプションを追加してください。例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

    出力では、 `execution info`列から実行時間を取得できます。

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

    出力では、 `execution info`列から実行時間を取得できます。

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

> **ノート：**
>
> サンプル データのサイズが小さく、このドキュメントのクエリは非常に単純であるため、オプティマイザがこのクエリに TiKV を選択するように強制し、同じクエリを再度実行した場合、TiKV はそのキャッシュを再利用するため、クエリは非常に多くなる可能性があります。もっと早く。データが頻繁に更新されると、キャッシュが失われます。

## もっと詳しく知る {#learn-more}

-   [TiFlashの概要](/tiflash/tiflash-overview.md)
-   [TiFlashレプリカの作成](/tiflash/create-tiflash-replicas.md)
-   [TiFlashからのデータの読み取り](/tiflash/use-tidb-to-read-tiflash.md)
-   [MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)
-   [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)

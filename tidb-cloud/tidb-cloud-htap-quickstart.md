---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with HTAP in TiDB Cloud.
---

# TiDB CloudHTAPクイックスタート {#tidb-cloud-htap-quick-start}

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)は、ハイブリッドトランザクションおよび分析処理を意味します。 TiDB CloudのHTAPクラスタは、トランザクション処理用に設計された行ベースのストレージエンジンである[TiKV](https://tikv.org)と、分析処理用に設計された列型ストレージである[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)で構成されています。アプリケーションデータは最初にTiKVに保存され、次にRaftコンセンサスアルゴリズムを介してTiFlashに複製されます。つまり、行ストレージから列ストレージへのリアルタイムレプリケーションです。

このチュートリアルでは、 TiDB Cloudのハイブリッドトランザクションおよび分析処理（HTAP）機能を簡単に体験する方法について説明します。コンテンツには、テーブルをTiFlashに複製する方法、TiFlashを使用してクエリを実行する方法、およびパフォーマンスの向上を体験する方法が含まれています。

## あなたが始める前に {#before-you-begin}

HTAP機能を体験する前に、 [TiDB Cloudクイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)に従ってTiFlashノードでクラスタを作成し、TiDBクラスタに接続して、CapitalBikeshareサンプルデータをクラスタにインポートします。

## 手順 {#steps}

### 手順1.サンプルデータを列型ストレージエンジンに複製します {#step-1-replicate-the-sample-data-to-the-columnar-storage-engine}

TiFlashノードを含むクラスタが作成された後、TiKVはデフォルトでデータをTiFlashに複製しません。レプリケートするテーブルを指定するには、TiDBのMySQLクライアントでDDLステートメントを実行する必要があります。その後、TiDBはそれに応じて指定されたテーブルレプリカをTiFlashに作成します。

たとえば、 `trips`のテーブル（Capital Bikeshareサンプルデータ内）をTiFlashに複製するには、次のステートメントを実行します。

```sql
USE bikeshare;
ALTER TABLE trips SET TIFLASH REPLICA 1;
```

レプリケーションの進行状況を確認するには、次のステートメントを実行します。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bikeshare' and TABLE_NAME = 'trips';
```

前のステートメントの結果：

-   `AVAILABLE`は、特定のテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`は利用可能、 `0`は利用不可を意味します。レプリカが使用可能になると、このステータスは変更されなくなります。
-   `PROGRESS`は、レプリケーションの進行状況を意味します。値は`0.0` `1.0` 。 `1.0`は、少なくとも1つのレプリカが複製されることを意味します。

### ステップ2.HTAPを使用してデータをクエリする {#step-2-query-data-using-htap}

レプリケーションのプロセスが完了すると、いくつかのクエリの実行を開始できます。

たとえば、さまざまな開始ステーションと終了ステーションによるトリップ数を確認できます。

```sql
SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
GROUP BY start_station_name, end_station_name
ORDER BY count ASC;
```

### 手順3.行ベースのストレージと列型ストレージのクエリパフォーマンスを比較します {#step-3-compare-the-query-performance-between-row-based-storage-and-columnar-storage}

このステップでは、TiKV（行ベースのストレージ）とTiFlash（列型ストレージ）の実行統計を比較できます。

-   TiKVを使用してこのクエリの実行統計を取得するには、次のステートメントを実行します。

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[trips]) */ start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

    TiFlashレプリカを含むテーブルの場合、TiDBオプティマイザは、コスト見積もりに基づいて、TiKVレプリカとTiFlashレプリカのどちらを使用するかを自動的に決定します。前の`EXPLAIN ANALYZE`のステートメントでは、 `HINT /*+ READ_FROM_STORAGE(TIKV[trips]) */`を使用してオプティマイザーにTiKVを選択させ、TiKVの実行統計を確認できるようにします。

    > **ノート：**
    >
    > 5.7.7より前のMySQLコマンドラインクライアントは、デフォルトでオプティマイザヒントを削除します。これらの以前のバージョンで`Hint`構文を使用している場合は、クライアントの起動時に`--comments`オプションを追加してください。例： `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

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
> サンプルデータのサイズが小さく、このドキュメントのクエリは非常に単純であるため、オプティマイザにこのクエリにTiKVを選択させて同じクエリを再度実行するように強制している場合、TiKVはキャッシュを再利用するため、クエリが多くなる可能性があります。もっと早く。データが頻繁に更新されると、キャッシュが失われます。

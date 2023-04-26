---
title: DM Cluster Performance Test
summary: Learn how to test the performance of DM clusters.
---

# DMクラスタのパフォーマンス テスト {#dm-cluster-performance-test}

このドキュメントでは、DM クラスターでパフォーマンス テストを実行するためのテスト シナリオを構築する方法について説明します。これには、データ移行に関する速度テストとレイテンシーテストが含まれます。

## 移行データ フロー {#migration-data-flow}

MySQL -&gt; DM -&gt; TiDB という単純な移行データ フローを使用して、DM クラスターのデータ移行パフォーマンスをテストできます。

## テスト環境をデプロイ {#deploy-test-environment}

-   すべてのデフォルト構成でTiUPを使用して TiDB テスト クラスターをデプロイ。
-   MySQL サービスをデプロイ。 binlogの`ROW`モードを有効にし、他の構成項目にはデフォルト構成を使用します。
-   DM-worker と DM-master を使用して DM クラスターをデプロイ。

## 性能テスト {#performance-test}

### テーブル スキーマ {#table-schema}

パフォーマンス テストには、次のスキーマを持つテーブルを使用します。

{{< copyable "" >}}

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` char(60) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### 全輸入ベンチマークケース {#full-import-benchmark-case}

#### テストデータの生成 {#generate-test-data}

アップストリームでテスト テーブルを作成し、フル インポート用のテスト データを生成するには、 `sysbench`を使用します。次の`sysbench`コマンドを実行して、テスト データを生成します。

{{< copyable "" >}}

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリームの MySQL ソースを作成し、 `source-id`から`source-1`を設定します。詳細については、 [データ ソース構成の読み込み](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  移行タスクを作成します ( `full`モード)。以下は、タスク構成テンプレートです。

```yaml
---
name: test-full
task-mode: full

# Configure the migration task using the TiDB information of your actual test environment.
target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "source-1"
    block-allow-list:  "instance"
    mydumper-config-name: "global"
    loader-thread: 16

# Configure the name of the database where sysbench generates data.
block-allow-list:
  instance:
    do-dbs: ["dm_benchmark"]

mydumpers:
  global:
    rows: 32000
    threads: 32
```

移行タスクの作成方法の詳細については、 [データ移行タスクの作成](/dm/dm-create-task.md)を参照してください。

> **ノート：**
>
> -   マルチスレッドを使用して単一のテーブルから同時にデータをエクスポートできるようにするには、 `mydumpers`構成項目で`rows`オプションを使用できます。これにより、データのエクスポートが高速化されます。
> -   異なる構成でパフォーマンスをテストするには、構成`mysql-instances`で`loader-thread`調整し、構成`mydumpers`で`rows`と`threads`調整します。

#### テスト結果を取得する {#get-test-results}

DM-worker ログを観察します。 `all data files have been finished`が表示された場合、完全なデータがインポートされたことを意味します。この場合、データのインポートにかかった時間を確認できます。サンプル ログは次のとおりです。

```
 [INFO] [loader.go:604] ["all data files have been finished"] [task=test] [unit=load] ["cost time"=52.439796ms]
```

テスト データのサイズとデータのインポートにかかる時間に応じて、完全なデータの移行速度を計算できます。

### 増分レプリケーションのベンチマーク ケース {#incremental-replication-benchmark-case}

#### テーブルの初期化 {#initialize-tables}

アップストリームでテスト テーブルを作成するには、 `sysbench`を使用します。

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリーム MySQL のソースを作成します。 `source-id` ～ `source-1`を設定します（ [全輸入ベンチマークケース](#full-import-benchmark-case)でソースを作成した場合は、再度作成する必要はありません）。詳細については、 [データ ソース構成のロード](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  DM 移行タスクを作成します ( `all`モードで)。以下は、タスク構成ファイルの例です。

```yaml
---
name: test-all
task-mode: all

# Configure the migration task using the TiDB information of your actual test environment.
target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  -
    source-id: "source-1"
    block-allow-list:  "instance"
    syncer-config-name: "global"

# Configure the name of the database where sysbench generates data.
block-allow-list:
  instance:
    do-dbs: ["dm_benchmark"]

syncers:
  global:
    worker-count: 16
    batch: 100
```

データ移行タスクの作成方法の詳細については、 [データ移行タスクの作成](/dm/dm-create-task.md)を参照してください。

> **ノート：**
>
> 異なる構成でパフォーマンスをテストするには、構成項目`syncers`の`worker-count`と`batch`を調整します。

#### 増分データの生成 {#generate-incremental-data}

アップストリームで増分データを継続的に生成するには、 `sysbench`コマンドを実行します。

{{< copyable "" >}}

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

> **ノート：**
>
> さまざまな`sysbench`ステートメントを使用して、さまざまなシナリオでデータ移行のパフォーマンスをテストできます。

#### テスト結果を取得する {#get-test-results}

DM の移行ステータスを確認するには、 `query-status`コマンドを実行します。 DM のモニタリング メトリックを観察するには、Grafana を使用できます。ここでの監視メトリックは、 `finished sqls jobs` (単位時間あたりに終了したジョブの数) およびその他の関連するメトリックを参照します。詳細については、 [Binlog移行の監視メトリクス](/dm/monitor-a-dm-cluster.md#binlog-replication)を参照してください。

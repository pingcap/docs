---
title: DM Cluster Performance Test
summary: Learn how to test the performance of DM clusters.
---

# DMクラスタのパフォーマンス テスト {#dm-cluster-performance-test}

このドキュメントでは、データ移行に関する速度テストやレイテンシーテストを含む、DM クラスターのパフォーマンス テストを実行するテスト シナリオを構築する方法について説明します。

## 移行データの流れ {#migration-data-flow}

単純な移行データ フロー (MySQL -&gt; DM -&gt; TiDB) を使用して、DM クラスターのデータ移行パフォーマンスをテストできます。

## テスト環境のデプロイ {#deploy-test-environment}

-   TiUPを使用し、すべてのデフォルト構成で TiDB テスト クラスターをデプロイ。
-   MySQL サービスをデプロイ。 binlogの`ROW`モードを有効にし、他の構成項目にはデフォルト構成を使用します。
-   DM ワーカーと DM マスターを備えた DM クラスターをデプロイ。

## 性能テスト {#performance-test}

### テーブルスキーマ {#table-schema}

パフォーマンス テストには、次のスキーマを持つテーブルを使用します。

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

### フルインポートベンチマークケース {#full-import-benchmark-case}

#### テストデータの生成 {#generate-test-data}

アップストリームでテスト テーブルを作成し、完全インポート用のテスト データを生成するには、 `sysbench`を使用します。次の`sysbench`コマンドを実行してテスト データを生成します。

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  上流の MySQL ソースを作成し、 `source-id` ～ `source-1`を設定します。詳細は[データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  移行タスクを作成します ( `full`モード)。以下はタスク構成テンプレートです。

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

> **注記：**
>
> -   マルチスレッドを使用して 1 つのテーブルからデータを同時にエクスポートできるようにするには、 `mydumpers`構成項目の`rows`オプションを使用します。これにより、データのエクスポートが高速化されます。
> -   さまざまな構成でパフォーマンスをテストするには、構成`mysql-instances`の`loader-thread`と、構成`mydumpers`の項目の`rows`および`threads`を調整できます。

#### テスト結果を取得する {#get-test-results}

DM ワーカーのログを確認します。 `all data files have been finished`が表示される場合は、完全なデータがインポートされたことを意味します。この場合、データのインポートにかかる時間を確認できます。サンプルログは次のとおりです。

     [INFO] [loader.go:604] ["all data files have been finished"] [task=test] [unit=load] ["cost time"=52.439796ms]

テスト データのサイズとデータのインポートにかかる時間に応じて、完全なデータの移行速度を計算できます。

### 増分レプリケーションのベンチマークケース {#incremental-replication-benchmark-case}

#### テーブルの初期化 {#initialize-tables}

上流にテスト テーブルを作成するには`sysbench`を使用します。

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  上流の MySQL のソースを作成します。 `source-id` ～ `source-1`を設定します( [フルインポートベンチマークケース](#full-import-benchmark-case)でソースを作成している場合は、再度作成する必要はありません)。詳細は[データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  DM 移行タスクを作成します ( `all`モード)。以下はタスク構成ファイルの例です。

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

> **注記：**
>
> さまざまな構成でパフォーマンスをテストするには、構成項目`syncers`の`worker-count`と`batch`を調整します。

#### 増分データの生成 {#generate-incremental-data}

アップストリームで増分データを継続的に生成するには、次のコマンド`sysbench`を実行します。

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

> **注記：**
>
> さまざまな`sysbench`ステートメントを使用して、さまざまなシナリオでデータ移行のパフォーマンスをテストできます。

#### テスト結果を取得する {#get-test-results}

DM の移行ステータスを確認するには、 `query-status`コマンドを実行します。 DM の監視メトリクスを観察するには、Grafana を使用できます。ここで、監視メトリクスは`finished sqls jobs` (単位時間あたりに完了したジョブの数) およびその他の関連メトリクスを指します。詳細については、 [Binlog移行監視メトリクス](/dm/monitor-a-dm-cluster.md#binlog-replication)を参照してください。

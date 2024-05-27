---
title: DM Cluster Performance Test
summary: DM クラスターのパフォーマンスをテストする方法を学習します。
---

# DMクラスタパフォーマンス テスト {#dm-cluster-performance-test}

このドキュメントでは、データ移行に関する速度テストやレイテンシーテストなど、DM クラスターでパフォーマンス テストを実行するためのテスト シナリオの構築方法について説明します。

## 移行データフロー {#migration-data-flow}

MySQL -&gt; DM -&gt; TiDB という単純な移行データ フローを使用して、DM クラスターのデータ移行パフォーマンスをテストできます。

## テスト環境をデプロイ {#deploy-test-environment}

-   すべてのデフォルト構成で、 TiUPを使用して TiDB テスト クラスターをデプロイ。
-   MySQL サービスをデプロイ。binlogの`ROW`モードを有効にし、他の構成項目にはデフォルト構成を使用します。
-   DM ワーカーと DM マスターを使用して DM クラスターをデプロイ。

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

#### テストデータを生成する {#generate-test-data}

`sysbench`使用して、アップストリームにテスト テーブルを作成し、完全インポート用のテスト データを生成します。テスト データを生成するには、次の`sysbench`コマンドを実行します。

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリーム MySQL ソースを作成し、 `source-id`を`source-1`に設定します。詳細については、 [データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)を参照してください。

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

移行タスクの作成方法の詳細については、 [データ移行タスクを作成する](/dm/dm-create-task.md)を参照してください。

> **注記：**
>
> -   マルチスレッドを使用して単一のテーブルから同時にデータをエクスポートできるようにするには、 `mydumpers`構成項目の`rows`オプションを使用します。これにより、データのエクスポートが高速化されます。
> -   さまざまな構成でパフォーマンスをテストするには、 `mysql-instances`構成の`loader-thread`と、 `mydumpers`構成項目の`rows`と`threads`調整できます。

#### テスト結果を取得する {#get-test-results}

DM-worker ログを確認します。 `all data files have been finished`表示されている場合は、完全なデータがインポートされたことを意味します。この場合、データのインポートにかかった時間を確認できます。サンプル ログは次のとおりです。

     [INFO] [loader.go:604] ["all data files have been finished"] [task=test] [unit=load] ["cost time"=52.439796ms]

テスト データのサイズとデータのインポートにかかる時間に応じて、完全なデータの移行速度を計算できます。

### 増分レプリケーションのベンチマークケース {#incremental-replication-benchmark-case}

#### テーブルを初期化する {#initialize-tables}

`sysbench`使用して、アップストリームにテスト テーブルを作成します。

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリーム MySQL のソースを作成します。1 `source-id` `source-1`に設定します ( [フルインポートベンチマークケース](#full-import-benchmark-case)でソースを作成している場合は、再度作成する必要はありません)。詳細については、 [データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  DM 移行タスクを作成します ( `all`モード)。タスク構成ファイルの例を次に示します。

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

データ移行タスクの作成方法の詳細については、 [データ移行タスクを作成する](/dm/dm-create-task.md)参照してください。

> **注記：**
>
> さまざまな構成でのパフォーマンスをテストするには、構成項目`syncers`の`worker-count`と`batch`を調整できます。

#### 増分データを生成する {#generate-incremental-data}

アップストリームで継続的に増分データを生成するには、 `sysbench`コマンドを実行します。

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

> **注記：**
>
> 異なる`sysbench`つのステートメントを使用して、さまざまなシナリオでのデータ移行パフォーマンスをテストできます。

#### テスト結果を取得する {#get-test-results}

DM の移行ステータスを確認するには、 `query-status`コマンドを実行します。DM の監視メトリックを確認するには、Grafana を使用します。ここでの監視メトリックとは、 `finished sqls jobs` (単位時間あたりに完了したジョブの数) およびその他の関連メトリックを指します。詳細については、 [Binlog移行監視メトリクス](/dm/monitor-a-dm-cluster.md#binlog-replication)を参照してください。

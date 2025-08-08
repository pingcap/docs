---
title: DM Cluster Performance Test
summary: DM クラスターのパフォーマンスをテストする方法を学びます。
---

# DMクラスタパフォーマンステスト {#dm-cluster-performance-test}

このドキュメントでは、データ移行に関する速度テストやレイテンシーテストなど、DM クラスターでパフォーマンス テストを実行するためのテスト シナリオの構築方法について説明します。

## 移行データフロー {#migration-data-flow}

MySQL -&gt; DM -&gt; TiDB という単純な移行データフローを使用して、DM クラスターのデータ移行パフォーマンスをテストできます。

## テスト環境をデプロイ {#deploy-test-environment}

-   すべてのデフォルト構成で、 TiUPを使用して TiDB テスト クラスターをデプロイ。
-   MySQL サービスをデプロイ。binlogの`ROW`モードを有効にし、その他の設定項目はデフォルト設定を使用します。
-   DM ワーカーと DM マスターを使用して DM クラスターをデプロイ。

## パフォーマンステスト {#performance-test}

### テーブルスキーマ {#table-schema}

パフォーマンス テストには、次のスキーマを持つテーブルを使用します。

```sql
CREATE TABLE `sbtest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `k` int NOT NULL DEFAULT '0',
  `c` char(120) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` char(60) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### 完全輸入ベンチマークケース {#full-import-benchmark-case}

#### テストデータを生成する {#generate-test-data}

`sysbench`使用してアップストリームにテストテーブルを作成し、フルインポート用のテストデータを生成します。テストデータを生成するには、以下の`sysbench`コマンドを実行します。

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリームMySQLソースを作成し、 `source-id`を`source-1`に設定します。詳細は[データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)参照してください。

2.  移行タスクを作成します（モード`full` ）。タスク設定テンプレートは次のとおりです。

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

移行タスクの作成方法の詳細については、 [データ移行タスクを作成する](/dm/dm-create-task.md)参照してください。

> **注記：**
>
> -   マルチスレッドを使用して単一のテーブルから同時にデータをエクスポートするには、設定項目`mydumpers`のオプション`rows`使用します。これにより、データのエクスポートが高速化されます。
> -   異なる構成でのパフォーマンスをテストするには、 `mysql-instances`構成の`loader-thread`と、 `mydumpers`構成項目の`rows`と`threads`調整できます。

#### テスト結果を取得する {#get-test-results}

DM-worker のログを確認してください。1 `all data files have been finished`表示されている場合は、すべてのデータがインポートされたことを意味します。この場合、データのインポートにかかった時間を確認できます。サンプルログは次のとおりです。

     [INFO] [loader.go:604] ["all data files have been finished"] [task=test] [unit=load] ["cost time"=52.439796ms]

テスト データのサイズとデータのインポートにかかる時間に応じて、完全なデータの移行速度を計算できます。

### 増分レプリケーションのベンチマークケース {#incremental-replication-benchmark-case}

#### テーブルを初期化する {#initialize-tables}

アップストリームにテスト テーブルを作成するには`sysbench`使用します。

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリームMySQLのソースを作成します。1を`source-id` `source-1`設定します（ [完全輸入ベンチマークケース](#full-import-benchmark-case)でソースを作成済みの場合は、再度作成する必要はありません）。詳細は[データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)参照してください。

2.  DM移行タスク（モード`all` ）を作成します。タスク設定ファイルの例を以下に示します。

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
> さまざまな構成でのパフォーマンスをテストするには、構成項目`syncers`の`worker-count`と`batch`調整できます。

#### 増分データを生成する {#generate-incremental-data}

アップストリームで増分データを継続的に生成するには、 `sysbench`コマンドを実行します。

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

> **注記：**
>
> 異なる`sysbench`のステートメントを使用して、さまざまなシナリオでのデータ移行のパフォーマンスをテストできます。

#### テスト結果を取得する {#get-test-results}

DMの移行ステータスを確認するには、コマンド`query-status`実行してください。DMの監視メトリクスを確認するには、Grafanaを使用してください。ここでの監視メトリクスとは、 `finished sqls jobs` （単位時間あたりに完了したジョブ数）およびその他の関連メトリクスを指します。詳細については、 [Binlog移行監視メトリクス](/dm/monitor-a-dm-cluster.md#binlog-replication)参照してください。

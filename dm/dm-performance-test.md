---
title: DM Cluster Performance Test
summary: Learn how to test the performance of DM clusters.
---

# DMクラスターパフォーマンステスト {#dm-cluster-performance-test}

このドキュメントでは、データ移行に関する速度テストや遅延テストなど、DMクラスタでパフォーマンステストを実行するためのテストシナリオを構築する方法について説明します。

## 移行データフロー {#migration-data-flow}

単純な移行データフロー、つまりMySQL-&gt; DM-&gt; TiDBを使用して、DMクラスタのデータ移行パフォーマンスをテストできます。

## テスト環境をデプロイ {#deploy-test-environment}

-   すべてのデフォルト構成で、TiUPを使用してTiDBテストクラスタをデプロイします。
-   MySQLサービスをデプロイします。 binlogに対して`ROW`モードを有効にし、他の構成アイテムにはデフォルト構成を使用します。
-   DMワーカーとDMマスターを使用してDMクラスタをデプロイします。

## 性能テスト {#performance-test}

### テーブルスキーマ {#table-schema}

パフォーマンステストには、次のスキーマのテーブルを使用します。

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

### 完全なインポートベンチマークケース {#full-import-benchmark-case}

#### テストデータを生成する {#generate-test-data}

`sysbench`を使用して、アップストリームでテストテーブルを作成し、完全にインポートするためのテストデータを生成します。次の`sysbench`のコマンドを実行して、テストデータを生成します。

{{< copyable "" >}}

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリームのMySQLソースを作成し、 `source-id`から`source-1`に設定します。詳細については、 [データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  移行タスクを作成します（ `full`モードで）。以下は、タスク構成テンプレートです。

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

> **ノート：**
>
> -   マルチスレッドを使用して単一のテーブルからデータを同時にエクスポートできるようにするには、 `mydumpers`の構成項目で`rows`オプションを使用できます。これにより、データのエクスポートが高速化されます。
> -   さまざまな構成でパフォーマンスをテストするには、 `mysql-instances`の構成で`loader-thread`を調整し、 `mydumpers`の構成項目で`rows`と`threads`を調整します。

#### テスト結果を取得する {#get-test-results}

DMワーカーのログを確認します。 `all data files have been finished`が表示されている場合は、完全なデータがインポートされていることを意味します。この場合、データのインポートに費やされた時間を確認できます。サンプルログは次のとおりです。

```
 [INFO] [loader.go:604] ["all data files have been finished"] [task=test] [unit=load] ["cost time"=52.439796ms]
```

テストデータのサイズとデータのインポートにかかる時間に応じて、完全なデータの移行速度を計算できます。

### インクリメンタルレプリケーションベンチマークケース {#incremental-replication-benchmark-case}

#### テーブルを初期化します {#initialize-tables}

`sysbench`を使用して、アップストリームにテストテーブルを作成します。

#### データ移行タスクを作成する {#create-a-data-migration-task}

1.  アップストリームMySQLのソースを作成します。 `source-id`から`source-1`に設定します（ソースが[完全なインポートベンチマークケース](#full-import-benchmark-case)で作成されている場合は、再度作成する必要はありません）。詳細については、 [データソース構成をロードする](/dm/dm-manage-source.md#operate-data-source)を参照してください。

2.  DM移行タスクを作成します（ `all`モードで）。以下は、タスク構成ファイルの例です。

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

データ移行タスクの作成方法の詳細については、 [データ移行タスクを作成する](/dm/dm-create-task.md)を参照してください。

> **ノート：**
>
> さまざまな構成でパフォーマンスをテストするために、 `syncers`の構成項目で`worker-count`と`batch`を調整できます。

#### 増分データを生成する {#generate-incremental-data}

アップストリームでインクリメンタルデータを継続的に生成するには、次の`sysbench`コマンドを実行します。

{{< copyable "" >}}

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

> **ノート：**
>
> さまざまな`sysbench`ステートメントを使用して、さまざまなシナリオでデータ移行のパフォーマンスをテストできます。

#### テスト結果を取得する {#get-test-results}

DMの移行ステータスを監視するには、 `query-status`コマンドを実行します。 DMの監視メトリックを監視するには、Grafanaを使用できます。ここで、監視メトリックは`finished sqls jobs` （単位時間あたりに完了したジョブの数）などを参照します。詳細については、 [Binlog移行監視メトリック](/dm/monitor-a-dm-cluster.md#binlog-replication)を参照してください。

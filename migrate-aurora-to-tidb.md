---
title: Migrate Data from Amazon Aurora to TiDB
summary: Learn how to migrate data from Amazon Aurora to TiDB using DB snapshot.
---

# Amazon Auroraから TiDB へのデータの移行 {#migrate-data-from-amazon-aurora-to-tidb}

このドキュメントでは、Amazon Auroraから TiDB にデータを移行する方法について説明します。移行プロセスでは[<a href="https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html">DBスナップショット</a>](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html)使用されるため、スペースと時間が大幅に節約されます。

移行全体には次の 2 つのプロセスがあります。

-   TiDB Lightningを使用して完全なデータを TiDB にインポートする
-   DM を使用して増分データを TiDB に複製する (オプション)

## 前提条件 {#prerequisites}

-   [<a href="/migration-tools.md">DumplingとTiDB Lightningをインストールする</a>](/migration-tools.md)
-   [<a href="/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database">TiDB Lightningに必要なターゲット データベース権限を取得します。</a>](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database) 。

## 完全なデータを TiDB にインポート {#import-full-data-to-tidb}

### ステップ 1. Auroraスナップショットを Amazon S3 にエクスポートする {#step-1-export-an-aurora-snapshot-to-amazon-s3}

1.  Auroraで、次のコマンドを実行して現在のbinlogの位置をクエリします。

    ```sql
    mysql> SHOW MASTER STATUS;
    ```

    出力は次のようになります。後で使用できるように、binlogの名前と位置を記録します。

    ```
    +------------------+----------+--------------+------------------+-------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +------------------+----------+--------------+------------------+-------------------+
    | mysql-bin.000002 |    52806 |              |                  |                   |
    +------------------+----------+--------------+------------------+-------------------+
    1 row in set (0.012 sec)
    ```

2.  Auroraスナップショットをエクスポートします。詳細な手順については、 [<a href="https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html">DB スナップショット データを Amazon S3 にエクスポートする</a>](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)を参照してください。

binlogの位置を取得したら、5 分以内にスナップショットをエクスポートします。そうしないと、記録されたbinlogの位置が古くなり、増分レプリケーション中にデータの競合が発生する可能性があります。

上記の 2 つの手順を完了したら、次の情報が用意されていることを確認してください。

-   スナップショット作成時のAurora binlog の名前と位置。
-   スナップショットが保存される S3 パス、および S3 パスにアクセスできる SecretKey と AccessKey。

### ステップ 2. スキーマのエクスポート {#step-2-export-schema}

Auroraからのスナップショット ファイルには DDL ステートメントが含まれていないため、 Dumplingを使用してスキーマをエクスポートし、 TiDB Lightningを使用してターゲット データベースにスキーマを作成する必要があります。スキーマを手動で作成する場合は、この手順をスキップできます。

次のコマンドを実行して、 Dumplingを使用してスキーマをエクスポートします。このコマンドには、必要なテーブル スキーマのみをエクスポートする`--filter`パラメーターが含まれています。

{{< copyable "" >}}

```shell
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12]' --no-data --output 's3://my-bucket/schema-backup' --filter "mydb.*"
```

上記のコマンドで使用されるパラメータは次のとおりです。その他のパラメータについては、 [<a href="/dumpling-overview.md">Dumplingの概要</a>](/dumpling-overview.md)を参照してください。

| パラメータ                  | 説明                                                                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `-u`または`--user`        | Aurora MySQL ユーザー                                                                                                                          |
| `-p`または`--password`    | MySQLユーザーのパスワード                                                                                                                            |
| `-P`または`--port`        | MySQLポート                                                                                                                                   |
| `-h`または`--host`        | MySQLのIPアドレス                                                                                                                               |
| `-t`または`--thread`      | エクスポートに使用されるスレッドの数                                                                                                                         |
| `-o`または`--output`      | エクスポートされたファイルを保存するディレクトリ。ローカルパスまたは[<a href="/br/backup-and-restore-storages.md">外部storageURI</a>](/br/backup-and-restore-storages.md)をサポート |
| `-r`または`--row`         | 1 つのファイル内の最大行数                                                                                                                             |
| `-F`                   | 単一ファイルの最大サイズ (MiB 単位)。推奨値: 256 MiB。                                                                                                        |
| `-B`または`--database`    | エクスポートするデータベースを指定します                                                                                                                       |
| `-T`または`--tables-list` | 指定されたテーブルをエクスポートします                                                                                                                        |
| `-d`または`--no-data`     | データをエクスポートしません。スキーマのみをエクスポートします。                                                                                                           |
| `-f`または`--filter`      | パターンに一致するテーブルをエクスポートします。 `-f`と`-T`を同時に使用しないでください。構文については[<a href="/table-filter.md">テーブルフィルター</a>](/table-filter.md)を参照してください。             |

### ステップ 3. TiDB Lightning構成ファイルを作成する {#step-3-create-the-tidb-lightning-configuration-file}

次のように`tidb-lightning.toml`構成ファイルを作成します。

{{< copyable "" >}}

```shell
vim tidb-lightning.toml
```

{{< copyable "" >}}

```toml
[tidb]

# The target TiDB cluster information.
host = ${host}                # e.g.: 172.16.32.1
port = ${port}                # e.g.: 4000
user = "${user_name}          # e.g.: "root"
password = "${password}"      # e.g.: "rootroot"
status-port = ${status-port}  # Obtains the table schema information from TiDB status port, e.g.: 10080
pd-addr = "${ip}:${port}"     # The cluster PD address, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.

[tikv-importer]
# "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
# "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally.
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

[mydumper]
# The path that stores the snapshot file.
data-source-dir = "${s3_path}"  # e.g.: s3://my-bucket/sql-backup

[[mydumper.files]]
# The expression that parses the parquet file.
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

TiDB クラスターで TLS を有効にする必要がある場合は、 [<a href="/tidb-lightning/tidb-lightning-configuration.md">TiDB Lightningコンフィグレーション</a>](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

### ステップ 4. TiDB に完全なデータをインポートする {#step-4-import-full-data-to-tidb}

1.  TiDB Lightningを使用してターゲット データベースにテーブルを作成します。

    {{< copyable "" >}}

    ```shell
    tiup tidb-lightning -config tidb-lightning.toml -d 's3://my-bucket/schema-backup'
    ```

2.  `tidb-lightning`を実行してインポートを開始します。コマンド ラインでプログラムを直接起動すると、SIGHUP シグナルの受信後にプロセスが予期せず終了する可能性があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例えば：

    S3storageパスにアクセスできる SecretKey と AccessKey を環境変数としてDumplingノードに渡します。 `~/.aws/credentials`から資格情報を読み取ることもできます。

    {{< copyable "" >}}

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  インポートの開始後、次のいずれかの方法でインポートの進行状況を確認できます。

    -   `grep`ログ内のキーワード`progress` 。デフォルトでは、進行状況は 5 分ごとに更新されます。
    -   [<a href="/tidb-lightning/monitor-tidb-lightning.md">監視ダッシュボード</a>](/tidb-lightning/monitor-tidb-lightning.md)で進行状況を確認します。
    -   [<a href="/tidb-lightning/tidb-lightning-web-interface.md">TiDB Lightning Web インターフェース</a>](/tidb-lightning/tidb-lightning-web-interface.md)で進行状況を確認します。

4.  TiDB Lightning はインポートを完了すると、自動的に終了します。最後の行に`tidb-lightning.log` `the whole procedure completed`含まれているかどうかを確認します。 「はい」の場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処します。

> **ノート：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、インポートが成功したことを必ずしも意味するわけではありません。

インポート中に問題が発生した場合は、 [<a href="/tidb-lightning/tidb-lightning-faq.md">TiDB LightningFAQ</a>](/tidb-lightning/tidb-lightning-faq.md)のトラブルシューティングを参照してください。

## 増分データを TiDB に複製する (オプション) {#replicate-incremental-data-to-tidb-optional}

### 前提条件 {#prerequisites}

-   [<a href="/dm/deploy-a-dm-cluster-using-tiup.md">DMをインストールする</a>](/dm/deploy-a-dm-cluster-using-tiup.md) 。
-   [<a href="/dm/dm-worker-intro.md">DM に必要なソース データベースとターゲット データベースの権限を取得します。</a>](/dm/dm-worker-intro.md) 。

### ステップ 1: データ ソースを作成する {#step-1-create-the-data-source}

1.  次のように`source1.yaml`ファイルを作成します。

    {{< copyable "" >}}

    ```yaml
    # Must be unique.
    source-id: "mysql-01"
    # Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
    enable-gtid: false

    from:
      host: "${host}"         # e.g.: 172.16.10.81
      user: "root"
      password: "${password}" # Supported but not recommended to use plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2.  次のコマンドを実行して、 `tiup dmctl`を使用してデータ ソース構成を DM クラスターにロードします。

    {{< copyable "" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    上記のコマンドで使用されるパラメータは次のように説明されます。

    | パラメータ                   | 説明                                                                      |
    | ----------------------- | ----------------------------------------------------------------------- |
    | `--master-addr`         | `dmctl`が接続されるクラスタ内の任意の DM マスターの`{advertise-addr}` 、例: 172.16.10.71:8261 |
    | `operate-source create` | データ ソースを DM クラスターにロードします。                                               |

### ステップ 2: 移行タスクを作成する {#step-2-create-the-migration-task}

次のように`task1.yaml`ファイルを作成します。

{{< copyable "" >}}

```yaml
# Task name. Multiple tasks that are running at the same time must each have a unique name.
name: "test"
# Task mode. Options are:
# - full: only performs full data migration.
# - incremental: only performs binlog real-time replication.
# - all: full data migration + binlog real-time replication.
task-mode: "incremental"
# The configuration of the target TiDB database.
target-database:
  host: "${host}"                   # e.g.: 172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # Supported but not recommended to use a plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

# Global configuration for block and allow lists. Each instance can reference the configuration by name.
block-allow-list:                     # If the DM version is earlier than v2.0.0-beta.2, use black-white-list.
  listA:                              # Name.
    do-tables:                        # Allow list for the upstream tables to be migrated.
    - db-name: "test_db"              # Name of databases to be migrated.
      tbl-name: "test_table"          # Name of tables to be migrated.

# Configures the data source.
mysql-instances:
  - source-id: "mysql-01"               # Data source ID, i.e., source-id in source1.yaml
    block-allow-list: "listA"           # References the block-allow-list configuration above.
#       syncer-config-name: "global"    # Name of the syncer configuration.
    meta:                               # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.
      binlog-name: "mysql-bin.000004"   # The binlog position recorded in "Step 1. Export an Aurora snapshot to Amazon S3". When the upstream database has source-replica switching, GTID mode is required.
      binlog-pos: 109227
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

# (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
   # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
   # syncers:            # The running configurations of the sync processing unit.
   #   global:            # Configuration name.
   #     safe-mode: true  # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
```

上記の YAML ファイルは、移行タスクに必要な最小構成です。その他の設定項目については、 [<a href="/dm/task-configuration-file-full.md">DM 拡張タスクコンフィグレーションファイル</a>](/dm/task-configuration-file-full.md)を参照してください。

### ステップ 3. 移行タスクを実行する {#step-3-run-the-migration-task}

移行タスクを開始する前に、エラーの可能性を減らすために、 `check-task`コマンドを実行して構成が DM の要件を満たしていることを確認することをお勧めします。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

その後、 `tiup dmctl`を実行して移行タスクを開始します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

上記のコマンドで使用されるパラメータは次のように説明されます。

| パラメータ           | 説明                                                                      |
| --------------- | ----------------------------------------------------------------------- |
| `--master-addr` | `dmctl`が接続されるクラスタ内の任意の DM マスターの`{advertise-addr}` 、例: 172.16.10.71:8261 |
| `start-task`    | 移行タスクを開始します。                                                            |

タスクの開始に失敗した場合は、プロンプト メッセージを確認して構成を修正します。その後、上記のコマンドを再実行してタスクを開始できます。

何か問題が発生した場合は、 [<a href="/dm/dm-error-handling.md">DMエラー処理</a>](/dm/dm-error-handling.md)と[<a href="/dm/dm-faq.md">DMに関するFAQ</a>](/dm/dm-faq.md)を参照してください。

### ステップ 4. 移行タスクのステータスを確認する {#step-4-check-the-migration-task-status}

DM クラスターに進行中の移行タスクがあるかどうかとタスクのステータスを確認するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、 [<a href="/dm/dm-query-status.md">クエリステータス</a>](/dm/dm-query-status.md)を参照してください。

### ステップ 5. タスクを監視し、ログを表示する {#step-5-monitor-the-task-and-view-logs}

移行タスクの履歴ステータスとその他の内部メトリックを表示するには、次の手順を実行します。

TiUPを使用して DM をデプロイしたときに Prometheus、Alertmanager、および Grafana をデプロイしている場合は、デプロイ中に指定された IP アドレスとポートを使用して Grafana にアクセスできます。次に、DM ダッシュボードを選択して、DM 関連の監視メトリックを表示できます。

DM の実行中、DM-worker、DM-master、および dmctl は関連情報をログに出力します。これらのコンポーネントのログ ディレクトリは次のとおりです。

-   DM マスター: DM マスター プロセス パラメーター`--log-file`によって指定されます。 TiUPを使用して DM をデプロイする場合、デフォルトのログ ディレクトリは`/dm-deploy/dm-master-8261/log/`です。
-   DM-worker: DM-worker プロセス パラメーター`--log-file`によって指定されます。 TiUPを使用して DM をデプロイする場合、デフォルトのログ ディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## 次は何ですか {#what-s-next}

-   [<a href="/dm/dm-pause-task.md">移行タスクを一時停止する</a>](/dm/dm-pause-task.md) 。
-   [<a href="/dm/dm-resume-task.md">移行タスクを再開する</a>](/dm/dm-resume-task.md) 。
-   [<a href="/dm/dm-stop-task.md">移行タスクを停止する</a>](/dm/dm-stop-task.md) 。
-   [<a href="/dm/dm-export-import-config.md">クラスターデータソースとタスク構成のエクスポートとインポート</a>](/dm/dm-export-import-config.md) 。
-   [<a href="/dm/handle-failed-ddl-statements.md">失敗した DDL ステートメントを処理する</a>](/dm/handle-failed-ddl-statements.md) 。

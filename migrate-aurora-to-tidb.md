---
title: Migrate Data from Amazon Aurora to TiDB
summary: Learn how to migrate data from Amazon Aurora to TiDB using DB snapshot.
---

# Amazon Auroraから TiDB へのデータの移行 {#migrate-data-from-amazon-aurora-to-tidb}

このドキュメントでは、Amazon Auroraから TiDB にデータを移行する方法について説明します。移行プロセスでは[DBスナップショット](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html)使用されるため、スペースと時間が大幅に節約されます。

移行全体には次の 2 つのプロセスがあります。

-   TiDB Lightningを使用して完全なデータを TiDB にインポートする
-   DM を使用して増分データを TiDB に複製する (オプション)

## 前提条件 {#prerequisites}

-   [DumplingとTiDB Lightningをインストールする](/migration-tools.md) 。ターゲット側で対応するテーブルを手動で作成する場合は、 Dumpling をインストールしないでください。
-   [Dumplingに必要なアップストリーム データベース権限を取得します。](/dumpling-overview.md#required-privileges) 。
-   [TiDB Lightningに必要なターゲット データベース権限を取得します。](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database) 。

## 完全なデータを TiDB にインポート {#import-full-data-to-tidb}

### ステップ 1. スキーマ ファイルをエクスポートおよびインポートする {#step-1-export-and-import-the-schema-file}

このセクションでは、Amazon Auroraからスキーマ ファイルをエクスポートし、TiDB にインポートする方法について説明します。ターゲット データベースにテーブルを手動で作成した場合は、この手順をスキップできます。

#### 1.1 Amazon Auroraからスキーマ ファイルをエクスポートする {#1-1-export-the-schema-file-from-amazon-aurora}

Amazon Auroraのスナップショット ファイルには DDL ステートメントが含まれていないため、 Dumplingを使用してスキーマをエクスポートし、 TiDB Lightningを使用してターゲット データベースにスキーマを作成する必要があります。

次のコマンドを実行して、 Dumplingを使用してスキーマをエクスポートします。このコマンドには、必要なテーブル スキーマのみをエクスポートするための`--filter`パラメータが含まれています。パラメータの詳細については、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12],mydb.*' --consistency none --no-data --output 's3://my-bucket/schema-backup'
```

上記のコマンドでエクスポートされたスキーマの URI (「s3://my-bucket/schema-backup」など) を記録します。これは、後でスキーマ ファイルをインポートするときに使用されます。

Amazon S3 にアクセスするには、この Amazon S3storageパスにアクセスできるアカウントのシークレット アクセス キーとアクセス キーを環境変数としてDumplingまたはTiDB Lightningノードに渡すことができます。 DumplingとTiDB Lightning は、資格情報ファイルの`~/.aws/credentials`からの読み取りもサポートしています。この方法により、 DumplingまたはTiDB Lightningノード上のすべてのタスクに対して秘密アクセス キーとアクセス キーを再度提供する必要がなくなります。

#### 1.2 スキーマファイル用のTiDB Lightning設定ファイルを作成する {#1-2-create-the-tidb-lightning-configuration-file-for-the-schema-file}

新しい`tidb-lightning-schema.toml`ファイルを作成し、次の内容をファイルにコピーし、対応する内容を置き換えます。

```toml
[tidb]

# The target TiDB cluster information.
host = ${host}
port = ${port}
user = "${user_name}
password = "${password}"
status-port = ${status-port}  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"     # The cluster PD address. Usually the port is 2379.

[tikv-importer]
# "local": Use the default Physical Import Mode (the "local" backend).
# During the import, the target TiDB cluster cannot provide any service.
# For more information about import modes, see https://docs.pingcap.com/tidb/stable/tidb-lightning-overview
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files.
# The directory must be empty, and the storage space must be greater than the size of the dataset to be imported.
# For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage,
# which can use I/O exclusively.
sorted-kv-dir = "${path}"

[mydumper]
# Set the directory of the schema file exported from Amazon Aurora
data-source-dir = "s3://my-bucket/schema-backup"
```

TiDB クラスターで TLS を有効にする必要がある場合は、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

#### 1.3 スキーマ ファイルを TiDB にインポートする {#1-3-import-the-schema-file-to-tidb}

TiDB Lightning を使用して、スキーマ ファイルをダウンストリーム TiDB にインポートします。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning-schema.toml > nohup.out 2>&1 &
```

### ステップ 2. Amazon Auroraスナップショットを Amazon S3 にエクスポートおよびインポートする {#step-2-export-and-import-an-amazon-aurora-snapshot-to-amazon-s3}

このセクションでは、Amazon Auroraスナップショットを Amazon S3 にエクスポートし、 TiDB Lightningによって TiDB にインポートする方法について説明します。

#### 2.1 Amazon Auroraスナップショットを Amazon S3 にエクスポートする {#2-1-export-an-amazon-aurora-snapshot-to-amazon-s3}

1.  後続の増分移行のために、Amazon Aurora binlogの名前と場所を取得します。 Amazon Auroraで、 `SHOW MASTER STATUS`コマンドを実行し、現在のbinlogの位置を記録します。

    ```sql
    SHOW MASTER STATUS;
    ```

    出力は次のようになります。後で使用できるように、binlogの名前と位置を記録します。

        +----------------------------+----------+--------------+------------------+-------------------+
        | File                       | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
        +----------------------------+----------+--------------+------------------+-------------------+
        | mysql-bin-changelog.018128 |    52806 |              |                  |                   |
        +----------------------------+----------+--------------+------------------+-------------------+
        1 row in set (0.012 sec)

2.  Amazon Auroraスナップショットをエクスポートします。詳細な手順については、 [DB スナップショット データを Amazon S3 にエクスポートする](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)を参照してください。binlogの位置を取得したら、5 分以内にスナップショットをエクスポートします。そうしないと、記録されたbinlogの位置が古くなり、増分レプリケーション中にデータの競合が発生する可能性があります。

#### 2.2 データファイル用のTiDB Lightning設定ファイルを作成する {#2-2-create-the-tidb-lightning-configuration-file-for-the-data-file}

新しい`tidb-lightning-data.toml`構成ファイルを作成し、次の内容をファイルにコピーし、対応する内容を置き換えます。

```toml
[tidb]

# The target TiDB cluster information.
host = ${host}
port = ${port}
user = "${user_name}
password = "${password}"
status-port = ${status-port}  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"     # The cluster PD address. Usually the port is 2379.

[tikv-importer]
# "local": Use the default Physical Import Mode (the "local" backend).
# During the import, the target TiDB cluster cannot provide any service.
# For more information about import modes, see https://docs.pingcap.com/tidb/stable/tidb-lightning-overview
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files.
# The directory must be empty, and the storage space must be greater than the size of the dataset to be imported.
# For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage,
# which can use I/O exclusively.
sorted-kv-dir = "${path}"

[mydumper]
# Set the directory of the snapshot file exported from Amazon Aurora
data-source-dir = "${s3_path}"  # eg: s3://my-bucket/sql-backup

[[mydumper.files]]
# The expression that parses the parquet file.
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

TiDB クラスターで TLS を有効にする必要がある場合は、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

#### 2.3 TiDB への完全なデータのインポート {#2-3-import-full-data-to-tidb}

1.  TiDB Lightning を使用して、Amazon Auroraスナップショットから TiDB にデータをインポートします。

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning-data.toml > nohup.out 2>&1 &
    ```

2.  インポートの開始後、次のいずれかの方法でインポートの進行状況を確認できます。

    -   `grep`ログ内のキーワード`progress` 。デフォルトでは、進行状況は 5 分ごとに更新されます。
    -   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。
    -   [TiDB Lightning Web インターフェース](/tidb-lightning/tidb-lightning-web-interface.md)で進捗状況を確認します。

3.  TiDB Lightning はインポートを完了すると、自動的に終了します。最後の行に`tidb-lightning.log` `the whole procedure completed`含まれているかどうかを確認します。 「はい」の場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処します。

> **注記：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、インポートが成功したことを必ずしも意味するわけではありません。

インポート中に問題が発生した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)のトラブルシューティングを参照してください。

## 増分データを TiDB に複製する (オプション) {#replicate-incremental-data-to-tidb-optional}

### 前提条件 {#prerequisites}

-   [DMをインストールする](/dm/deploy-a-dm-cluster-using-tiup.md) 。
-   [DM に必要なソース データベースとターゲット データベースの権限を取得します。](/dm/dm-worker-intro.md) 。

### ステップ 1: データ ソースを作成する {#step-1-create-the-data-source}

1.  次のように`source1.yaml`ファイルを作成します。

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
      binlog-name: "mysql-bin.000004"   # The binlog position recorded in "Step 1. Export an Amazon Aurora snapshot to Amazon S3". When the upstream database has source-replica switching, GTID mode is required.
      binlog-pos: 109227
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

# (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
   # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
   # syncers:            # The running configurations of the sync processing unit.
   #   global:            # Configuration name.
   #     safe-mode: true  # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
```

上記の YAML ファイルは、移行タスクに必要な最小構成です。その他の設定項目については、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

### ステップ 3. 移行タスクを実行する {#step-3-run-the-migration-task}

移行タスクを開始する前に、エラーの可能性を減らすために、 `check-task`コマンドを実行して構成が DM の要件を満たしていることを確認することをお勧めします。

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

その後、 `tiup dmctl`を実行して移行タスクを開始します。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

上記のコマンドで使用されるパラメータは次のように説明されます。

| パラメータ           | 説明                                                                      |
| --------------- | ----------------------------------------------------------------------- |
| `--master-addr` | `dmctl`が接続されるクラスタ内の任意の DM マスターの`{advertise-addr}` 、例: 172.16.10.71:8261 |
| `start-task`    | 移行タスクを開始します。                                                            |

タスクの開始に失敗した場合は、プロンプト メッセージを確認して構成を修正します。その後、上記のコマンドを再実行してタスクを開始できます。

問題が発生した場合は、 [DMエラー処理](/dm/dm-error-handling.md)と[DMに関するFAQ](/dm/dm-faq.md)を参照してください。

### ステップ 4. 移行タスクのステータスを確認する {#step-4-check-the-migration-task-status}

DM クラスターに進行中の移行タスクがあるかどうかとタスクのステータスを確認するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、 [クエリステータス](/dm/dm-query-status.md)を参照してください。

### ステップ 5. タスクを監視し、ログを表示する {#step-5-monitor-the-task-and-view-logs}

移行タスクの履歴ステータスとその他の内部メトリックを表示するには、次の手順を実行します。

TiUPを使用して DM をデプロイしたときに Prometheus、Alertmanager、および Grafana をデプロイしている場合は、デプロイ中に指定された IP アドレスとポートを使用して Grafana にアクセスできます。次に、DM ダッシュボードを選択して、DM 関連の監視メトリックを表示できます。

DM の実行中、DM-worker、DM-master、および dmctl は関連情報をログに出力します。これらのコンポーネントのログ ディレクトリは次のとおりです。

-   DM マスター: DM マスター プロセス パラメーター`--log-file`によって指定されます。 TiUPを使用して DM をデプロイする場合、デフォルトのログ ディレクトリは`/dm-deploy/dm-master-8261/log/`です。
-   DM-worker: DM-worker プロセス パラメーター`--log-file`によって指定されます。 TiUPを使用して DM をデプロイする場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-worker-8262/log/`です。

## 次は何ですか {#what-s-next}

-   [移行タスクを一時停止する](/dm/dm-pause-task.md) 。
-   [移行タスクを再開する](/dm/dm-resume-task.md) 。
-   [移行タスクを停止する](/dm/dm-stop-task.md) 。
-   [クラスターデータソースとタスク構成のエクスポートとインポート](/dm/dm-export-import-config.md) 。
-   [失敗した DDL ステートメントを処理する](/dm/handle-failed-ddl-statements.md) 。

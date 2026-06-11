---
title: Migrate Data from Amazon Aurora to TiDB
summary: DBスナップショットを使用して、Amazon AuroraからTiDBへデータを移行する方法を学びましょう。
---

# Amazon AuroraからTiDBへのデータ移行 {#migrate-data-from-amazon-aurora-to-tidb}

このドキュメントでは、Amazon Auroraから TiDB にデータを移行する方法について説明します。移行プロセスでは[DBスナップショット](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html)を使用するため、スペースと時間が大幅に節約されます。

移行全体は2つのプロセスから構成されます。

-   TiDB Lightningを使用してTiDBに完全なデータをインポートします
-   DMを使用して増分データをTiDBに複製する（オプション）

## 前提条件 {#prerequisites}

-   [DumplingとTiDB Lightningをインストールする](/migration-tools.md)。ターゲット側で対応するテーブルを手動で作成する場合は、 Dumplingをインストールしないでください。
-   [Dumplingに必要な上流データベース権限を取得します。](/dumpling-overview.md#required-privileges)
-   [TiDB Lightningに必要なターゲットデータベース権限を取得します。](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)

## TiDBに全データをインポートする {#import-full-data-to-tidb}

### ステップ1. スキーマファイルのエクスポートとインポート {#step-1-export-and-import-the-schema-file}

このセクションでは、Amazon Auroraからスキーマ ファイルをエクスポートし、TiDB にインポートする方法について説明します。対象データベースにテーブルを手動で作成している場合は、この手順をスキップできます。

#### 1.1 Amazon Auroraからスキーマファイルをエクスポートする {#1-1-export-the-schema-file-from-amazon-aurora}

Amazon Auroraのスナップショット ファイルには DDL ステートメントが含まれていないため、 Dumplingを使用してスキーマをエクスポートし、 TiDB Lightningを使用してターゲット データベースにスキーマを作成する必要があります。

次のコマンドを実行して、 Dumplingを使用してスキーマをエクスポートします。このコマンドには`--filter`パラメータが含まれており、目的のテーブルスキーマのみをエクスポートできます。パラメータの詳細については、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)参照してください。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12],mydb.*' --consistency none --no-data --output 's3://my-bucket/schema-backup'
```

上記コマンドでエクスポートされたスキーマのURI（例：「s3://my-bucket/schema-backup」）を記録しておいてください。これは後でスキーマファイルをインポートする際に使用します。

Amazon S3 にアクセスするには、この Amazon S3storageパスへのアクセス権を持つアカウントのシークレット アクセス キーとアクセス キーを環境変数としてDumplingまたはTiDB Lightningノードに渡します。Dumpling とTiDB Lightning は`~/.aws/credentials`からの認証情報ファイルの読み取りもサポートしています。この方法により、そのDumplingまたはTiDB Lightningノード上のすべてのタスクでシークレット アクセス キーとアクセス キーを再度指定する必要がなくなります。

#### 1.2 スキーマファイル用のTiDB Lightning設定ファイルを作成する {#1-2-create-the-tidb-lightning-configuration-file-for-the-schema-file}

新しい`tidb-lightning-schema.toml`ファイルを作成し、以下の内容をファイルにコピーして、対応する内容を置き換えます。

```toml
[tidb]

# The target TiDB cluster information.
host = "${host}"
port = "${port}"
user = "${user_name}"
password = "${password}"
status-port = "${status-port}"  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"       # The cluster PD address. Usually the port is 2379.

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

TiDBクラスターでTLSを有効にする必要がある場合は、 [TiDB Lightningの構成](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

#### 1.3 スキーマファイルをTiDBにインポートする {#1-3-import-the-schema-file-to-tidb}

TiDB Lightningを使用して、スキーマファイルをターゲットのTiDBにインポートします。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning-schema.toml > nohup.out 2>&1 &
```

### ステップ2. Amazon AuroraスナップショットをAmazon S3にエクスポートおよびインポートする {#step-2-export-and-import-an-amazon-aurora-snapshot-to-amazon-s3}

このセクションでは、Amazon Auroraスナップショットを Amazon S3 にエクスポートし、 TiDB Lightningを使用して TiDB にインポートする方法について説明します。

#### 2.1 Amazon AuroraのスナップショットをAmazon S3にエクスポートする {#2-1-export-an-amazon-aurora-snapshot-to-amazon-s3}

1.  後続の増分移行のために、Amazon Auroraのbinlogの名前と場所を取得します。Amazon Auroraで`SHOW MASTER STATUS`コマンドを実行し、現在のbinlogの位置を記録します。

    ```sql
    SHOW MASTER STATUS;
    ```

    出力は以下のようになります。後で使用するために、binlogの名前と位置を記録しておいてください。

        +----------------------------+----------+--------------+------------------+-------------------+
        | File                       | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
        +----------------------------+----------+--------------+------------------+-------------------+
        | mysql-bin-changelog.018128 |    52806 |              |                  |                   |
        +----------------------------+----------+--------------+------------------+-------------------+
        1 row in set (0.012 sec)

2.  Amazon Auroraスナップショットをエクスポートします。詳細な手順については、 [DBスナップショットデータをAmazon S3にエクスポートする](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)参照してください。binlogの位置を取得したら、5 分以内にスナップショットをエクスポートします。そうしないと、記録されたbinlogの位置が古くなり、増分レプリケーション中にデータの競合が発生する可能性があります。

#### 2.2 データファイル用のTiDB Lightning構成ファイルを作成する {#2-2-create-the-tidb-lightning-configuration-file-for-the-data-file}

新しい`tidb-lightning-data.toml`設定ファイルを作成し、以下の内容をファイルにコピーして、対応する内容を置き換えます。

```toml
[tidb]

# The target TiDB cluster information.
host = "${host}"
port = "${port}"
user = "${user_name}"
password = "${password}"
status-port = "${status-port}"  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"       # The cluster PD address. Usually the port is 2379.

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

TiDBクラスターでTLSを有効にする必要がある場合は、 [TiDB Lightningの構成](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

#### 2.3 TiDBへの全データのインポート {#2-3-import-full-data-to-tidb}

1.  TiDB Lightningを使用して、Amazon AuroraのスナップショットからTiDBにデータをインポートします。

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning-data.toml > nohup.out 2>&1 &
    ```

2.  インポートが開始された後、以下のいずれかの方法でインポートの進行状況を確認できます。

    -   ログ内のキーワード`progress`を`grep`することで、インポートの進行状況を確認できます。進行状況は、デフォルトでは 5 分ごとに更新されます。
    -   [モニタリングダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。
    -   [TiDB Lightning Webインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)で進行状況を確認します。

3.  TiDB Lightning はインポートが完了すると自動的に終了します。`tidb-lightning.log`の最後の行に`the whole procedure completed`が含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポート中にエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **注記：**
>
> インポートが成功したかどうかに関わらず、ログの最後の行には`tidb lightning exit`と表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するものではありません。

インポート中に問題が発生した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してトラブルシューティングを行ってください。

## 増分データをTiDBに複製する（オプション） {#replicate-incremental-data-to-tidb-optional}

### 前提条件 {#prerequisites}

-   [DMをインストール](/dm/deploy-a-dm-cluster-using-tiup.md)。
-   [DMに必要なソースデータベースとターゲットデータベースの権限を取得します。](/dm/dm-worker-intro.md)

### ステップ1：データソースを作成する {#step-1-create-the-data-source}

1.  `source1.yaml`ファイルは以下の手順で作成します。

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

2.  次のコマンドを実行して、 `tiup dmctl`を使用してデータソース構成を DM クラスターにロードします。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    上記のコマンドで使用されるパラメータは、以下のように説明されます。

    | パラメータ                   | 説明                                                                          |
    | ----------------------- | --------------------------------------------------------------------------- |
    | `--master-addr`         | `{advertise-addr}`が接続されるクラスタ内の任意の DM-master の`dmctl` (例: 172.16.10.71:8261) |
    | `operate-source create` | データソースをDMクラスターにロードします。                                                      |

### ステップ2：移行タスクを作成する {#step-2-create-the-migration-task}

`task1.yaml`ファイルは以下の手順で作成します。

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

上記の YAML ファイルは、移行タスクに必要な最小構成です。その他の設定項目については、 [DM 高度タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

### ステップ3. マイグレーションタスクを実行する {#step-3-run-the-migration-task}

移行作業を開始する前に、エラーの可能性を減らすため、 `check-task`コマンドを実行して、構成が DM の要件を満たしていることを確認することをお勧めします。

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

その後、 `tiup dmctl`を実行して移行タスクを開始します。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

上記のコマンドで使用されるパラメータは、以下のように説明されます。

| パラメータ           | 説明                                                                          |
| --------------- | --------------------------------------------------------------------------- |
| `--master-addr` | `{advertise-addr}`が接続されるクラスタ内の任意の DM-master の`dmctl` (例: 172.16.10.71:8261) |
| `start-task`    | 移行タスクを開始します。                                                                |

タスクの開始に失敗した場合は、プロンプトメッセージを確認し、設定を修正してください。その後、上記のコマンドを再度実行してタスクを開始できます。

問題が発生した場合は、 [DMエラー処理](/dm/dm-error-handling.md)および[DMに関するFAQ](/dm/dm-faq.md)を参照してください。

### ステップ4．移行タスクのステータスを確認する {#step-4-check-the-migration-task-status}

DM クラスターで進行中の移行タスクがあるかどうか、およびそのタスクの状態を確認するには、 `query-status`を使用して`tiup dmctl`コマンドを実行します。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、[クエリステータス](/dm/dm-query-status.md)を参照してください。

### ステップ5．タスクを監視し、ログを表示する {#step-5-monitor-the-task-and-view-logs}

移行タスクの履歴ステータスやその他の内部指標を確認するには、以下の手順に従ってください。

TiUPを使用してDMをデプロイした際に、Prometheus、Alertmanager、およびGrafanaもデプロイしている場合は、デプロイ時に指定したIPアドレスとポートを使用してGrafanaにアクセスできます。その後、DMダッシュボードを選択して、DM関連の監視メトリクスを表示できます。

DMが実行されている間、DM-worker、DM-master、およびdmctlは関連情報をログに出力します。これらのコンポーネントのログディレクトリは以下のとおりです。

-   DM-master: DM-master プロセス パラメータ`--log-file`で指定されます。TiUPを使用して DM をデプロイする場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-master-8261/log/`になります。
-   DM-worker: DM-worker プロセス パラメータ`--log-file`で指定されます。TiUPを使用して DM をデプロイする場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-worker-8262/log/`になります。

## 次は？ {#what-s-next}

-   [移行タスクを一時停止する](/dm/dm-pause-task.md)。
-   [移行タスクを再開する](/dm/dm-resume-task.md)。
-   [移行タスクを停止します](/dm/dm-stop-task.md)。
-   [クラスタデータソースとタスク構成のエクスポートとインポート](/dm/dm-export-import-config.md)。
-   [失敗したDDLステートメントを処理する](/dm/handle-failed-ddl-statements.md)。

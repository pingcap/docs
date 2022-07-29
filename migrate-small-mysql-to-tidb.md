---
title: Migrate MySQL of Small Datasets to TiDB
summary: Learn how to migrate MySQL of small datasets to TiDB.
---

# 小さなデータセットのMySQLをTiDBに移行する {#migrate-mysql-of-small-datasets-to-tidb}

このドキュメントでは、TiDBデータ移行（DM）を使用して、小さなデータセットのMySQLを完全移行モードと増分レプリケーションモードでTiDBに移行する方法について説明します。このドキュメントの「小さなデータセット」とは、データサイズが1TiB未満であることを意味します。

移行速度は、テーブルスキーマ、ハードウェア、ネットワーク環境のインデックス数などの複数の要因に応じて、30 GB/hから50GB/hまで変化します。<!--The migration process using DM is shown in the figure below.-->

<!--/media/dm/migrate-with-dm.png-->

## 前提条件 {#prerequisites}

-   [TiUPを使用してDMクラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [DMのソースデータベースとターゲットデータベースに必要な権限を付与します](/dm/dm-worker-intro.md)

## 手順1.データソースを作成する {#step-1-create-the-data-source}

まず、次のように`source1.yaml`のファイルを作成します。

{{< copyable "" >}}

```yaml
# The ID must be unique.
source-id: "mysql-01"

# Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable GTID, the upstream MySQL must have enabled GTID. If the upstream MySQL has automatic source-replica switching, the GTID mode is required.
enable-gtid: true

from:
  host: "${host}"         # For example: 172.16.10.81
  user: "root"
  password: "${password}" # Plaintext password is supported but not recommended. It is recommended to use dmctl encrypt to encrypt the plaintext password before using the password.
  port: 3306
```

次に、次のコマンドを実行して、 `tiup dmctl`を使用してデータソース構成をDMクラスタにロードします。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

上記のコマンドで使用されるパラメーターは、次のとおりです。

| パラメータ                   | 説明                                                                    |
| :---------------------- | :-------------------------------------------------------------------- |
| `--master-addr`         | `dmctl`が接続するクラスタのDMマスターノードの{advertise-addr}。たとえば、172.16.10.71：8261です。 |
| `operate-source create` | データソースをDMクラスタにロードします。                                                 |

## 手順2.移行タスクを作成する {#step-2-create-the-migration-task}

次のように`task1.yaml`のファイルを作成します。

{{< copyable "" >}}

```yaml
# Task name. Each of the multiple tasks running at the same time must have a unique name.
name: "test"
# Task mode. Options are:
# full: only performs full data migration.
# incremental: only performs binlog real-time replication.
# all: full data migration + binlog real-time replication.
task-mode: "all"
# The configuration of the target TiDB database.
target-database:
  host: "${host}"                   # For example: 172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # Plaintext password is supported but not recommended. It is recommended to use dmctl encrypt to encrypt the plaintext password before using the password.

# The configuration of all MySQL instances of source database required for the current migration task.
mysql-instances:
-
  # The ID of an upstream instance or a replication group
  source-id: "mysql-01"
  # The names of the block list and allow list configuration of the schema name or table name that is to be migrated. These names are used to reference the global configuration of the block and allowlist. For the global configuration, refer to the `block-allow-list` configuration below.
  block-allow-list: "listA"

# The global configuration of blocklist and allowlist. Each instance is referenced by a configuration item name.
block-allow-list:
  listA:                              # name
    do-tables:                        # The allowlist of upstream tables that need to be migrated.
    - db-name: "test_db"              # The schema name of the table to be migrated.
      tbl-name: "test_table"          # The name of the table to be migrated.

```

上記は、移行を実行するための最小タスク構成です。タスクに関するその他の構成項目については、 [DMタスクの完全な構成ファイルの紹介](/dm/task-configuration-file-full.md)を参照してください。

## 手順3.移行タスクを開始します {#step-3-start-the-migration-task}

エラーを回避するために、移行タスクを開始する前に、 `check-task`コマンドを使用して、構成がDM構成の要件を満たしているかどうかを確認することをお勧めします。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

次のコマンドを`tiup dmctl`で実行して、移行タスクを開始します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

上記のコマンドで使用されるパラメーターは、次のとおりです。

| パラメータ           | 説明                                                               |
| --------------- | ---------------------------------------------------------------- |
| `--master-addr` | `dmctl`が接続するクラスタのDMマスターノードの{advertise-addr}。例：172.16.10.71：8261。 |
| `start-task`    | 移行タスクを開始します                                                      |

タスクの開始に失敗した場合は、返された結果に従って構成を変更した後、 `start-task task.yaml`コマンドを実行してタスクを再開できます。問題が発生した場合は、 [エラーの処理](/dm/dm-error-handling.md)と[FAQ](/dm/dm-faq.md)を参照してください。

## 手順4：移行タスクのステータスを確認する {#step-4-check-the-migration-task-status}

DMクラスタに進行中の移行タスク、タスクステータス、およびその他の情報があるかどうかを確認するには、 `tiup dmctl`を使用して`query-status`コマンドを実行します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、 [クエリステータス](/dm/dm-query-status.md)を参照してください。

## ステップ5.タスクを監視し、ログを表示します（オプション） {#step-5-monitor-the-task-and-view-logs-optional}

移行タスクの履歴ステータスおよびその他の内部メトリックを表示するには、次の手順を実行します。

TiUPを使用してDMをデプロイするときにPrometheus、Alertmanager、およびGrafanaをデプロイした場合、デプロイ中に指定されたIPアドレスとポートを使用してGrafanaにアクセスできます。次に、DMダッシュボードを選択して、DM関連の監視メトリックを表示できます。

-   DM-masterのログディレクトリ：DM-masterプロセスパラメータ`--log-file`で指定されます。 TiUPを使用してDMを展開した場合、ログディレクトリはデフォルトで`/dm-deploy/dm-master-8261/log/`です。
-   DM-workerのログディレクトリ：DM-workerプロセスパラメータ`--log-file`で指定されます。 TiUPを使用してDMを展開した場合、ログディレクトリはデフォルトで`/dm-deploy/dm-worker-8262/log/`です。

## 次は何ですか {#what-s-next}

-   [移行タスクを一時停止します](/dm/dm-pause-task.md)
-   [移行タスクを再開します](/dm/dm-resume-task.md)
-   [移行タスクを停止します](/dm/dm-stop-task.md)
-   [クラスタデータソースとタスク構成をエクスポートおよびインポートします](/dm/dm-export-import-config.md)
-   [失敗したDDLステートメントを処理する](/dm/handle-failed-ddl-statements.md)

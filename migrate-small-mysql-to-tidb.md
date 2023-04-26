---
title: Migrate MySQL of Small Datasets to TiDB
summary: Learn how to migrate MySQL of small datasets to TiDB.
---

# 小さなデータセットの MySQL を TiDB に移行する {#migrate-mysql-of-small-datasets-to-tidb}

このドキュメントでは、TiDB Data Migration (DM) を使用して、小さなデータセットの MySQL を完全移行モードおよび増分レプリケーション モードで TiDB に移行する方法について説明します。このドキュメントの「小さなデータセット」とは、1 TiB 未満のデータ サイズを意味します。

移行速度は、テーブル スキーマのインデックス数、ハードウェア、ネットワーク環境などの複数の要因に応じて、30 GB/h から 50 GB/h までさまざまです。<!--The migration process using DM is shown in the figure below.-->

<!--/media/dm/migrate-with-dm.png-->

## 前提条件 {#prerequisites}

-   [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [DM のソース データベースとターゲット データベースに必要な権限を付与します。](/dm/dm-worker-intro.md)

## 手順 1. データ ソースを作成する {#step-1-create-the-data-source}

まず、次のように`source1.yaml`ファイルを作成します。

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

次に、次のコマンドを実行して、 `tiup dmctl`を使用してデータ ソース構成を DM クラスターに読み込みます。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

上記のコマンドで使用されるパラメーターは、次のとおりです。

| パラメータ                   | 説明                                                                               |
| :---------------------- | :------------------------------------------------------------------------------- |
| `--master-addr`         | `dmctl`が接続するクラスタ内の任意の DM マスター ノードの`{advertise-addr}` 。たとえば、172.16.10.71:8261 です。 |
| `operate-source create` | データ ソースを DM クラスターに読み込みます。                                                        |

## ステップ 2.移行タスクを作成する {#step-2-create-the-migration-task}

次のように`task1.yaml`ファイルを作成します。

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

上記は、移行を実行するための最小タスク構成です。タスクに関するその他の設定項目については、 [DM タスク完了構成ファイルの紹介](/dm/task-configuration-file-full.md)を参照してください。

## ステップ 3. 移行タスクを開始する {#step-3-start-the-migration-task}

エラーを回避するために、移行タスクを開始する前に、 `check-task`コマンドを使用して、構成が DM 構成の要件を満たしているかどうかを確認することをお勧めします。

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

| パラメータ           | 説明                                                                          |
| --------------- | --------------------------------------------------------------------------- |
| `--master-addr` | `dmctl`が接続するクラスタ内の任意の DM マスター ノードの`{advertise-addr}` 。例: 172.16.10.71:8261。 |
| `start-task`    | 移行タスクを開始する                                                                  |

タスクの開始に失敗した場合は、返された結果に従って構成を変更した後、 `start-task task.yaml`コマンドを実行してタスクを再開できます。問題が発生した場合は、 [エラー処理](/dm/dm-error-handling.md)および[FAQ](/dm/dm-faq.md)を参照してください。

## ステップ 4: 移行タスクのステータスを確認する {#step-4-check-the-migration-task-status}

DM クラスターに進行中の移行タスクがあるかどうか、タスクのステータス、およびその他の情報を確認するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、 [クエリのステータス](/dm/dm-query-status.md)を参照してください。

## ステップ 5. タスクの監視とログの表示 (オプション) {#step-5-monitor-the-task-and-view-logs-optional}

移行タスクの履歴ステータスとその他の内部メトリックを表示するには、次の手順を実行します。

TiUPを使用して DM を展開するときに Prometheus、Alertmanager、および Grafana を展開した場合は、展開中に指定された IP アドレスとポートを使用して Grafana にアクセスできます。次に、DM ダッシュボードを選択して、DM 関連のモニタリング メトリックを表示できます。

-   DM-master のログ ディレクトリ: DM-master プロセス パラメータ`--log-file`によって指定されます。 TiUP を使用して DM をデプロイした場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-master-8261/log/`です。
-   DM-worker のログ ディレクトリ: DM-worker プロセス パラメータ`--log-file`で指定されます。 TiUP を使用して DM をデプロイした場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-worker-8262/log/`です。

## 次は何ですか {#what-s-next}

-   [移行タスクを一時停止します](/dm/dm-pause-task.md)
-   [移行タスクを再開します](/dm/dm-resume-task.md)
-   [移行タスクを停止する](/dm/dm-stop-task.md)
-   [クラスター データ ソースとタスク構成のエクスポートとインポート](/dm/dm-export-import-config.md)
-   [失敗した DDL ステートメントを処理する](/dm/handle-failed-ddl-statements.md)

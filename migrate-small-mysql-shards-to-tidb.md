---
title: Migrate and Merge MySQL Shards of Small Datasets to TiDB
summary: シャードの小さなデータセットを MySQL から TiDB に移行およびマージする方法を学びます。
---

# 小さなデータセットの MySQL シャードを TiDB に移行してマージする {#migrate-and-merge-mysql-shards-of-small-datasets-to-tidb}

複数のMySQLデータベースインスタンスを上流から下流の1つのTiDBデータベースに移行・統合し、データ量がそれほど大きくない場合は、DMを使用してMySQLシャードを移行できます。本ドキュメントにおける「小規模データセット」とは、通常、1TiB程度以下のデータを指します。本ドキュメントの例を通して、移行の操作手順、注意事項、トラブルシューティングについて理解を深めることができます。

このドキュメントは、合計1TiB未満のMySQLシャードの移行に適用されます。合計1TiBを超えるデータを持つMySQLシャードを移行する場合、DMのみを使用して移行すると長い時間がかかります。この場合、 [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)で紹介した操作に従って移行を実行することをお勧めします。

このドキュメントでは、簡単な例を用いて移行手順を説明します。例では、2つのデータソースMySQLインスタンスのMySQLシャードが下流のTiDBクラスタに移行されます。

この例では、MySQLインスタンス1とMySQLインスタンス2の両方に以下のスキーマとテーブルが含まれています。この例では、両方のインスタンスでプレフィックスが`sale`あるスキーマ`store_01`と`store_02`テーブルを、スキーマ`store`の下流のテーブル`sale`に移行してマージします。

| スキーマ   | テーブル          |
| :----- | :------------ |
| ストア_01 | セール_01、セール_02 |
| ストア_02 | セール_01、セール_02 |

ターゲット スキーマとテーブル:

| スキーマ | テーブル |
| :--- | :--- |
| 店    | 販売   |

## 前提条件 {#prerequisites}

移行を開始する前に、次のタスクが完了していることを確認してください。

-   [TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [DMワーカーに必要な権限](/dm/dm-worker-intro.md)

### シャードテーブルの競合をチェックする {#check-conflicts-for-the-sharded-tables}

移行に異なるシャーディングされたテーブルからのデータのマージが含まれる場合、マージ中に主キーまたは一意のインデックスの競合が発生する可能性があります。そのため、移行前に、現在のシャーディングスキームをビジネスの観点から詳細に検討し、競合を回避する方法を見つける必要があります。詳細については、 [複数のシャードテーブル間の主キーまたは一意のインデックス間の競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables)参照してください。以下に簡単に説明します。

この例では、 `sale_01`と`sale_02`次の同じテーブル構造を持ちます。

```sql
CREATE TABLE `sale_01` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sid` bigint NOT NULL,
  `pid` bigint NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

`id`列目は主キー、 `sid`列目はシャーディングキーです。5列目`id`自動増分であり、複数のシャーディングテーブル範囲が重複するとデータ競合が発生します。7列`sid`インデックスのグローバル一意性を保証するため、 [自動増分主キーの主キー属性を削除します](/dm/shard-merge-best-practices.md#remove-the-primary-key-attribute-from-the-column)目の手順に従って`id`列目をバイパスできます。

```sql
CREATE TABLE `sale` (
  `id` bigint NOT NULL,
  `sid` bigint NOT NULL,
  `pid` bigint NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

## ステップ1. データソースを読み込む {#step-1-load-data-sources}

`source1.yaml`という新しいデータ ソース ファイルを作成し、DM にアップストリーム データ ソースを構成して、次のコンテンツを追加します。

```yaml
# Configuration.
source-id: "mysql-01" # Must be unique.
# Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
# The prerequisite is that you have already enabled GTID in the upstream MySQL.
# If you have configured the upstream database service to switch master between different nodes automatically, you must enable GTID.
enable-gtid: true
from:
  host: "${host}"           # For example: 172.16.10.81
  user: "root"
  password: "${password}"   # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
  port: ${port}             # For example: 3306
```

ターミナルで次のコマンドを実行します。1 `tiup dmctl`指定して、データソース構成を DM クラスターに読み込みます。

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

パラメータの説明は以下のとおりです。

| パラメータ                   | 説明                                                                 |
| ----------------------- | ------------------------------------------------------------------ |
| `--master-addr`         | dmctlが接続するクラスタ内の任意のDMマスターノードの`{advertise-addr}`例：172.16.10.71:8261 |
| `operate-source create` | データ ソースを DM クラスターにロードします。                                          |

すべてのデータ ソースが DM クラスターに追加されるまで、上記の手順を繰り返します。

## ステップ2. 移行タスクを構成する {#step-2-configure-the-migration-task}

`task1.yaml`という名前のタスク構成ファイルを作成し、次の内容を書き込みます。

```yaml
name: "shard_merge"               # The name of the task. Should be globally unique.
# Task mode. You can set it to the following:
# - full: Performs only full data migration (incremental replication is skipped)
# - incremental: Only performs real-time incremental replication using binlog. (full data migration is skipped)
# - all: Performs both full data migration and incremental replication. For migrating small to medium amount of data here, use this option.
task-mode: all
# Required for the MySQL shards. By default, the "pessimistic" mode is used.
# If you have a deep understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb/dev/feature-shard-merge/)
shard-mode: "pessimistic"
meta-schema: "dm_meta"                        # A schema will be created in the downstream database to store the metadata
ignore-checking-items: ["auto_increment_ID"]  # In this example, there are auto-incremental primary keys upstream, so you do not need to check this item.

target-database:
  host: "${host}"                             # For example: 192.168.0.1
  port: 4000
  user: "root"
  password: "${password}"                     # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.

mysql-instances:
  -
    source-id: "mysql-01"                                    # ID of the data source, which is source-id in source1.yaml
    route-rules: ["sale-route-rule"]                         # Table route rules applied to the data source
    filter-rules: ["store-filter-rule", "sale-filter-rule"]  # Binlog event filter rules applied to the data source
    block-allow-list:  "log-bak-ignored"                     # Block & Allow Lists rules applied to the data source
  -
    source-id: "mysql-02"
    route-rules: ["sale-route-rule"]
    filter-rules: ["store-filter-rule", "sale-filter-rule"]
    block-allow-list:  "log-bak-ignored"

# Configurations for merging MySQL shards
routes:
  sale-route-rule:
    schema-pattern: "store_*"                               # Merge schemas store_01 and store_02 to the store schema in the downstream
    table-pattern: "sale_*"                                 # Merge tables sale_01 and sale_02 of schemas store_01 and store_02 to the sale table in the downstream
    target-schema: "store"
    target-table:  "sale"
    # Optional. Used for extracting the source information of sharded schemas and tables and writing the information to the user-defined columns in the downstream. If these options are configured, you need to manually create a merged table in the downstream. For details, see the following table routing setting.
    # extract-table:                                        # Extracts and writes the table name suffix without the sale_ part to the c-table column of the merged table. For example, 01 is extracted and written to the c-table column for the sharded table sale_01.
    #   table-regexp: "sale_(.*)"
    #   target-column: "c_table"
    # extract-schema:                                       # Extracts and writes the schema name suffix without the store_ part to the c_schema column of the merged table. For example, 02 is extracted and written to the c_schema column for the sharded schema store_02.
    #   schema-regexp: "store_(.*)"
    #   target-column: "c_schema"
    # extract-source:                                       # Extracts and writes the source instance information to the c_source column of the merged table. For example, mysql-01 is extracted and written to the c_source column for the data source mysql-01.
    #   source-regexp: "(.*)"
    #   target-column: "c_source"

# Filters out some DDL events.
filters:
  sale-filter-rule:           # Filter name.
    schema-pattern: "store_*" # The binlog events or DDL SQL statements of upstream MySQL instance schemas that match schema-pattern are filtered by the rules below.
    table-pattern: "sale_*"   # The binlog events or DDL SQL statements of upstream MySQL instance tables that match table-pattern are filtered by the rules below.
    events: ["truncate table", "drop table", "delete"]   # The binlog event array.
    action: Ignore                                       # The string (`Do`/`Ignore`). `Do` is the allow list. `Ignore` is the block list.
  store-filter-rule:
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore

# Block and allow list
block-allow-list:           # filter or only migrate all operations of some databases or some tables.
  log-bak-ignored:          # Rule name.
    do-dbs: ["store_*"]     # The allow list of the schemas to be migrated, similar to replicate-do-db in MySQL.
```

上記の例は、移行タスクを実行するための最小限の構成です。詳細については、 [DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)参照してください。

タスク ファイル内の`routes` 、およびその他`filters`構成の詳細については、次のドキュメントを参照してください。

-   [テーブルルーティング](/dm/dm-table-routing.md)
-   [ブロックと許可のテーブルリスト](/dm/dm-block-allow-table-lists.md)
-   [Binlogイベントフィルター](/filter-binlog-event.md)
-   [SQL 式を使用して特定の行の変更をフィルタリングする](/filter-dml-event.md)

## ステップ3. タスクを開始する {#step-3-start-the-task}

移行タスクを開始する前に、 `tiup dmctl`の`check-task`サブコマンドを実行して、構成が DM の要件を満たしているかどうかを確認し、起こりうるエラーを回避します。

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

移行タスクを開始するには、 `tiup dmctl`で次のコマンドを実行します。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

| パラメータ           | 説明                                                                 |
| --------------- | ------------------------------------------------------------------ |
| `--master-addr` | dmctlが接続するクラスタ内の任意のDMマスターノードの`{advertise-addr}`例：172.16.10.71:8261 |
| `start-task`    | データ移行タスクを開始します。                                                    |

移行タスクの開始に失敗した場合は、エラー情報に従って構成情報を変更し、手順`start-task task.yaml`再度実行して移行タスクを開始してください。問題が発生した場合は、 [エラーの処理](/dm/dm-error-handling.md)と[FAQ](/dm/dm-faq.md)参照してください。

## ステップ4. タスクを確認する {#step-4-check-the-task}

移行タスクを開始した後、 `dmtcl tiup`使用して`query-status`実行し、タスクのステータスを表示できます。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

エラーが発生した場合は、 `query-status ${task-name}`使用して詳細情報を表示してください。3 `query-status`のクエリ結果、タスクステータス、サブタスクステータスの詳細については、 [TiDB データ移行クエリのステータス](/dm/dm-query-status.md)参照してください。

## ステップ5. タスクを監視し、ログを確認する（オプション） {#step-5-monitor-tasks-and-check-logs-optional}

Grafana またはログを通じて、移行タスクの履歴と内部運用メトリックを表示できます。

-   グラファナ経由

    TiUPを使用してDMクラスターをデプロイする際に、Prometheus、Alertmanager、Grafanaが正しくデプロイされていれば、GrafanaでDMの監視メトリクスを確認できます。具体的には、デプロイ時に指定したIPアドレスとポート番号をGrafanaに入力し、DMダッシュボードを選択してください。

-   ログ経由

    DM の実行中、DM-master、DM-worker、dmctl は、移行タスクに関する情報を含むログを出力します。各コンポーネントのログディレクトリは以下のとおりです。

    -   DMマスターログディレクトリ：DMマスタープロセスパラメータ`--log-file`で指定されます。DMがTiUPを使用して展開されている場合、ログディレクトリは`/dm-deploy/dm-master-8261/log/`です。
    -   DMワーカーログディレクトリ：DMワーカープロセスパラメータ`--log-file`で指定します。DMがTiUPを使用してデプロイされている場合、ログディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## 参照 {#see-also}

-   [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md) 。
-   [シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge.md)
-   [シャード統合シナリオにおけるデータ移行のベストプラクティス](/dm/shard-merge-best-practices.md)
-   [エラーの処理](/dm/dm-error-handling.md)
-   [パフォーマンスの問題に対処する](/dm/dm-handle-performance-issues.md)
-   [FAQ](/dm/dm-faq.md)

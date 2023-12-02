---
title: Migrate and Merge MySQL Shards of Small Datasets to TiDB
summary: Learn how to migrate and merge small datasets of shards from MySQL to TiDB.
---

# 小規模なデータセットの MySQL シャードを TiDB に移行およびマージする {#migrate-and-merge-mysql-shards-of-small-datasets-to-tidb}

アップストリームの複数の MySQL データベース インスタンスを 1 つの TiDB データベース ダウンストリームに移行およびマージする必要があり、データ量がそれほど大きくない場合は、DM を使用して MySQL シャードを移行できます。このドキュメントにおける「小規模なデータセット」とは、通常、1 TiB 程度またはそれ未満のデータを意味します。本書の例を通じて、移行の操作手順や注意事項、トラブルシューティングについて学ぶことができます。

このドキュメントは、合計 1 TiB 未満の MySQL シャードの移行に適用されます。合計 1 TiB を超えるデータを持つ MySQL シャードを移行する場合、DM のみを使用して移行するには長い時間がかかります。この場合は、 [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)で紹介した操作に従って移行を行うことをお勧めします。

このドキュメントでは、簡単な例を使用して移行手順を説明します。この例の 2 つのデータ ソース MySQL インスタンスの MySQL シャードは、ダウンストリームの TiDB クラスターに移行されます。

この例では、MySQL インスタンス 1 と MySQL インスタンス 2 の両方に次のスキーマとテーブルが含まれています。この例では、両方のインスタンスで`sale`プレフィックスを持つ`store_01`および`store_02`スキーマのテーブルを、 `store`スキーマの下流の`sale`テーブルに移行およびマージします。

| スキーマ   | テーブル          |
| :----- | :------------ |
| ストア_01 | セール_01、セール_02 |
| ストア_02 | セール_01、セール_02 |

ターゲットのスキーマとテーブル:

| スキーマ | テーブル |
| :--- | :--- |
| 店    | セール  |

## 前提条件 {#prerequisites}

移行を開始する前に、次のタスクが完了していることを確認してください。

-   [TiUPを使用した DMクラスタのデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [DM ワーカーに必要な権限](/dm/dm-worker-intro.md)

### シャードテーブルの競合を確認する {#check-conflicts-for-the-sharded-tables}

移行に異なるシャードテーブルのデータのマージが含まれる場合、マージ中に主キーまたは一意のインデックスの競合が発生する可能性があります。したがって、移行前に、ビジネスの観点から現在のシャーディング スキームを詳しく調べ、競合を回避する方法を見つける必要があります。詳細については、 [複数のシャードテーブルにわたる主キーまたは一意のインデックス間の競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables)を参照してください。以下に簡単に説明します。

この例では、 `sale_01`と`sale_02`次のような同じテーブル構造を持ちます。

```sql
CREATE TABLE `sale_01` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

`id`列が主キー、 `sid`列がシャーディング キーです。 `id`列は自動増分であり、複数のシャードテーブル範囲が重複するとデータの競合が発生します。 `sid`インデックスがグローバルに一意であることが保証されるため、 [自動インクリメント主キーの主キー属性を削除します。](/dm/shard-merge-best-practices.md#remove-the-primary-key-attribute-from-the-column)の手順に従って`id`列をバイパスできます。

```sql
CREATE TABLE `sale` (
  `id` bigint(20) NOT NULL,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

## ステップ 1. データソースをロードする {#step-1-load-data-sources}

DM へのアップストリーム データ ソースを構成する`source1.yaml`という新しいデータ ソース ファイルを作成し、次のコンテンツを追加します。

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

ターミナルで次のコマンドを実行します。データ ソース構成を DM クラスターにロードするには、 `tiup dmctl`を使用します。

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

パラメータは次のように説明されます。

| パラメータ                   | 説明                                                                         |
| ----------------------- | -------------------------------------------------------------------------- |
| `--master-addr`         | dmctl が接続するクラスター内の任意の DM マスター ノードの`{advertise-addr}` 。例: 172.16.10.71:8261 |
| `operate-source create` | データ ソースを DM クラスターにロードします。                                                  |

すべてのデータ ソースが DM クラスターに追加されるまで、上記の手順を繰り返します。

## ステップ 2. 移行タスクを構成する {#step-2-configure-the-migration-task}

`task1.yaml`という名前のタスク構成ファイルを作成し、次の内容をそれに書き込みます。

```yaml
name: "shard_merge"               # The name of the task. Should be globally unique.
# Task mode. You can set it to the following:
# - full: Performs only full data migration (incremental replication is skipped)
# - incremental: Only performs real-time incremental replication using binlog. (full data migration is skipped)
# - all: Performs both full data migration and incremental replication. For migrating small to medium amount of data here, use this option.
task-mode: all
# Required for the MySQL shards. By default, the "pessimistic" mode is used.
# If you have a deep understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb/v7.5/feature-shard-merge/)
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

上記の例は、移行タスクを実行するための最小構成です。詳細については、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

タスク ファイルの`routes` 、 `filters`およびその他の構成の詳細については、次のドキュメントを参照してください。

-   [テーブルルーティング](/dm/dm-table-routing.md)
-   [ブロックおよび許可テーブル リスト](/dm/dm-block-allow-table-lists.md)
-   [Binlogイベントフィルター](/filter-binlog-event.md)
-   [SQL式を使用して特定の行変更をフィルタリングする](/filter-dml-event.md)

## ステップ 3. タスクを開始する {#step-3-start-the-task}

移行タスクを開始する前に、エラーの発生を避けるために、 `tiup dmctl`の`check-task`サブコマンドを実行して、構成が DM の要件を満たしているかどうかを確認してください。

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

`tiup dmctl`で次のコマンドを実行して、移行タスクを開始します。

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

| パラメータ           | 説明                                                                         |
| --------------- | -------------------------------------------------------------------------- |
| `--master-addr` | dmctl が接続するクラスター内の任意の DM マスター ノードの`{advertise-addr}` 。例: 172.16.10.71:8261 |
| `start-task`    | データ移行タスクを開始します。                                                            |

移行タスクの開始に失敗した場合は、エラー情報に従って構成情報を変更し、再度`start-task task.yaml`を実行して移行タスクを開始します。問題が発生した場合は、 [エラーの処理](/dm/dm-error-handling.md)と[FAQ](/dm/dm-faq.md)を参照してください。

## ステップ4. タスクを確認する {#step-4-check-the-task}

移行タスクを開始した後、 `dmtcl tiup`から`query-status`を実行してタスクのステータスを表示できます。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

エラーが発生した場合は、 `query-status ${task-name}`を使用して詳細情報を表示します。 `query-status`コマンドのクエリ結果、タスクステータス、サブタスクステータスの詳細については、 [TiDB データ移行クエリのステータス](/dm/dm-query-status.md)を参照してください。

## ステップ 5. タスクを監視し、ログを確認する (オプション) {#step-5-monitor-tasks-and-check-logs-optional}

Grafana またはログを通じて、移行タスクの履歴と内部運用メトリックを表示できます。

-   グラファナ経由

    TiUPを使用して DM クラスターをデプロイするときに Prometheus、Alertmanager、および Grafana が正しくデプロイされている場合は、Grafana で DM モニタリング メトリックを表示できます。具体的には、Grafana での展開時に指定した IP アドレスとポートを入力し、DM ダッシュボードを選択します。

-   ログ経由

    DM の実行中、DM-master、DM-worker、および dmctl は、移行タスクに関する情報を含むログを出力します。各コンポーネントのログディレクトリは以下のとおりです。

    -   DM マスター ログ ディレクトリ: DM マスター プロセス パラメーター`--log-file`によって指定されます。 DM がTiUPを使用して展開されている場合、ログ ディレクトリは`/dm-deploy/dm-master-8261/log/`です。
    -   DM-worker ログ ディレクトリ: DM-worker プロセス パラメーター`--log-file`によって指定されます。 DM がTiUPを使用して展開されている場合、ログ ディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## こちらも参照 {#see-also}

-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md) 。
-   [シャードテーブルからのデータのマージと移行](/dm/feature-shard-merge.md)
-   [シャード結合シナリオにおけるデータ移行のベスト プラクティス](/dm/shard-merge-best-practices.md)
-   [エラーの処理](/dm/dm-error-handling.md)
-   [パフォーマンスの問題に対処する](/dm/dm-handle-performance-issues.md)
-   [FAQ](/dm/dm-faq.md)

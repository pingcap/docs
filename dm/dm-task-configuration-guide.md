---
title: Data Migration Task Configuration Guide
summary: データ移行 (DM) でデータ移行タスクを構成する方法を学習します。
---

# データ移行タスクコンフィグレーションガイド {#data-migration-task-configuration-guide}

このドキュメントでは、データ移行 (DM) でデータ移行タスクを構成する方法について説明します。

## 移行するデータソースを構成する {#configure-data-sources-to-be-migrated}

タスク用に移行するデータ ソースを構成する前に、まず DM が対応するデータ ソースの構成ファイルをロードしていることを確認する必要があります。次に、操作の参考資料をいくつか示します。

-   データソースを表示するには、 [データソースの構成を確認する](/dm/dm-manage-source.md#check-data-source-configurations)を参照してください。
-   データソースを作成するには、 [データソースを作成する](/dm/migrate-data-using-dm.md#step-3-create-data-source)を参照してください。
-   データ ソース構成ファイルを生成するには、 [ソース構成ファイルの紹介](/dm/dm-source-configuration-file.md)を参照してください。

次の例`mysql-instances`は、データ移行タスクで移行する必要があるデータ ソースを構成する方法を示しています。

```yaml
---

## ********* Basic configuration *********
name: test             # The name of the task. Should be globally unique.

## ******** Data source configuration **********
mysql-instances:
  - source-id: "mysql-replica-01"  # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
  - source-id: "mysql-replica-02"  # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
```

## ダウンストリームTiDBクラスタを構成する {#configure-the-downstream-tidb-cluster}

次の例`target-database`は、データ移行タスクの移行先となるターゲット TiDB クラスターを構成する方法を示しています。

```yaml
---

## ********* Basic configuration *********
name: test             # The name of the task. Should be globally unique.

## ******** Data source configuration **********
mysql-instances:
  - source-id: "mysql-replica-01"  # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
  - source-id: "mysql-replica-02"  # Migrate data from the data source whose `source-id` is `mysql-replica-02`.

## ******** Downstream TiDB database configuration **********
target-database:       # Configuration of target TiDB database.
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # If the password is not null, it is recommended to use a password encrypted with dmctl.
```

## 移行するテーブルを構成する {#configure-tables-to-be-migrated}

> **注記：**
>
> 特定のテーブルをフィルタリングしたり、特定のテーブルを移行したりする必要がない場合は、この構成をスキップします。

データ移行タスクのデータ ソース テーブルのブロック リストと許可リストを構成するには、次の手順を実行します。

1.  タスク構成ファイルで、ブロックおよび許可リストのグローバル フィルター ルール セットを構成します。

    ```yaml
    block-allow-list:
      bw-rule-1:                           # The name of the block and allow list rule.
        do-dbs: ["test.*", "user"]         # The allow list of upstream schemas to be migrated. Wildcard characters (*?) are supported. You only need to configure either `do-dbs` or `ignore-dbs`. If both fields are configured, only `do-dbs` takes effect.
        # ignore-dbs: ["mysql", "account"] # The block list of upstream schemas to be migrated. Wildcard characters (*?) are supported.
        do-tables:                         # The allow list of upstream tables to be migrated. You only need to configure either `do-tables` or `ignore-tables`. If both fields are configured, only `do-tables` takes effect.
        - db-name: "test.*"
          tbl-name: "t.*"
        - db-name: "user"
          tbl-name: "information"
      bw-rule-2:                          # The name of the block allow list rule.
        ignore-tables:                    # The block list of data source tables needs to be migrated.
        - db-name: "user"
          tbl-name: "log"
    ```

    詳細な設定ルールについては[ブロックと許可のテーブルリスト](/dm/dm-block-allow-table-lists.md)参照してください。

2.  データ ソース構成のブロック リスト ルールと許可リスト ルールを参照して、移行するテーブルをフィルター処理します。

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"  # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-1" # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
      - source-id: "mysql-replica-02"  # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
        block-allow-list:  "bw-rule-2" # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
    ```

## 移行するbinlogイベントを構成する {#configure-binlog-events-to-be-migrated}

> **注記：**
>
> 特定のスキーマまたはテーブルの特定のbinlogイベントをフィルターする必要がない場合は、この構成をスキップします。

データ移行タスクのbinlogイベントのフィルターを構成するには、次の手順を実行します。

1.  タスク構成ファイルで、 binlogイベントのグローバル フィルター ルール セットを構成します。

    ```yaml
    filters:                                        # The filter rule set of data source binlog events. You can set multiple rules at the same time.
      filter-rule-1:                                # The name of the filtering rule.
        schema-pattern: "test_*"                    # The pattern of the data source schema name. Wildcard characters (*?) are supported.
        table-pattern: "t_*"                        # The pattern of the data source table name. Wildcard characters (*?) are supported.
        events: ["truncate table", "drop table"]    # The event types to be filtered out in schemas or tables that match the `schema-pattern` or the `table-pattern`.
        action: Ignore                              # Whether to migrate (Do) or ignore (Ignore) the binlog that matches the filtering rule.
      filter-rule-2:
        schema-pattern: "test"
        events: ["all dml"]
        action: Do
    ```

    詳細な設定ルールについては[Binlogイベント フィルター](/dm/dm-binlog-event-filter.md)参照してください。

2.  データ ソース構成のbinlogイベント フィルタリング ルールを参照して、データ ソース内の指定されたテーブルまたはスキーマの指定されたbinlogイベントをフィルタリングします。

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"    # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-1"   # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-1"]  # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
      - source-id: "mysql-replica-02"    # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-2"   # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-2"]  # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    ```

## データソーステーブルから下流のTiDBテーブルへのマッピングを構成する {#configure-the-mapping-of-data-source-tables-to-downstream-tidb-tables}

> **注記：**
>
> -   データ ソースの特定のテーブルをダウンストリーム TiDB インスタンス内の別の名前のテーブルに移行する必要がない場合は、この構成をスキップします。
>
> -   シャードマージタスクの場合は、タスク構成ファイルでマッピングルールを設定する**必要があります**。

データ ソース テーブルを指定されたダウンストリーム TiDB テーブルに移行するためのルーティング マッピング ルールを構成するには、次の手順を実行します。

1.  タスク構成ファイルでグローバル ルーティング マッピング ルール セットを構成します。

    ```yaml
    routes:                           # The routing mapping rule set between the data source tables and downstream TiDB tables. You can set multiple rules at the same time.
      route-rule-1:                   # The name of the routing mapping rule.
        schema-pattern: "test_*"      # The pattern of the upstream schema name. Wildcard characters (*?) are supported.
        table-pattern: "t_*"          # The pattern of the upstream table name. Wildcard characters (*?) are supported.
        target-schema: "test"         # The name of the downstream TiDB schema.
        target-table: "t"             # The name of the downstream TiDB table.
      route-rule-2:
        schema-pattern: "test_*"
        target-schema: "test"
    ```

    詳細な設定ルールについては[テーブルルーティング](/dm/dm-table-routing.md)参照してください。

2.  データ ソース構成のルーティング マッピング ルールを参照して、移行するテーブルをフィルター処理します。

    ```yaml
    mysql-instances:
      - source-id: "mysql-replica-01"                     # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
        block-allow-list:  "bw-rule-1"                    # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-1"]                   # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
        route-rules: ["route-rule-1", "route-rule-2"]     # The name of the routing mapping rule. You can configure multiple rules here.
      - source-id: "mysql-replica-02"                     # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
        block-allow-list:  "bw-rule-2"                    # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
        filter-rules: ["filter-rule-2"]                   # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    ```

## シャードマージタスクを構成する {#configure-a-shard-merge-task}

> **注記：**
>
> -   シャード マージ シナリオでシャーディング DDL ステートメントを移行する必要がある場合は、 `shard-mode`フィールドを明示的に構成する**必要があります**。それ以外の場合は、 `shard-mode`まったく構成**しないでください**。
>
> -   シャーディング DDL ステートメントを移行すると、多くの問題が発生する可能性があります。この機能を使用する前に、DM 移行 DDL ステートメントの原則と制限を理解し、慎重に使用する**必要があります**。

次の例は、タスクをシャードマージタスクとして構成する方法を示しています。

```yaml
---

## ********* Basic information *********
name: test                      # The name of the task. Should be globally unique.
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
```

## その他の構成 {#other-configurations}

以下は、このドキュメントの全体的なタスク構成の例です。完全なタスク構成テンプレートは[DM タスク構成ファイルの完全な紹介](/dm/task-configuration-file-full.md)にあります。

```yaml
---

## ********* Basic configuration *********
name: test                      # The name of the task. Should be globally unique.
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
task-mode: all                  # The task mode. Can be set to `full`(only migrates full data)/`incremental`(replicates binlog synchronously)/`all` (replicates both full and incremental binlogs).
timezone: "UTC"               # The timezone used in SQL Session. By default, DM uses the global timezone setting in the target cluster, which ensures the correctness automatically. A customized timezone does not affect data migration but is unnecessary.

## ******** Data source configuration **********
mysql-instances:
  - source-id: "mysql-replica-01"                   # Migrate data from the data source whose `source-id` is `mysql-replica-01`.
    block-allow-list:  "bw-rule-1"                  # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
    filter-rules: ["filter-rule-1"]                 # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    route-rules: ["route-rule-1", "route-rule-2"]   # The name of the routing mapping rule. You can configure multiple rules here.
  - source-id: "mysql-replica-02"                   # Migrate data from the data source whose `source-id` is `mysql-replica-02`.
    block-allow-list:  "bw-rule-2"                  # The name of the block and allow list rule. If the DM version is earlier than v2.0.0-beta.2, use `black-white-list` instead.
    filter-rules: ["filter-rule-2"]                 # The name of the rule that filters specific binlog events of the data source. You can configure multiple rules here.
    route-rules: ["route-rule-2"]                   # The name of the routing mapping rule. You can configure multiple rules here.

## ******** Downstream TiDB instance configuration **********
target-database:       # Configuration of the downstream database instance.
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # If the password is not null, it is recommended to use a password encrypted with dmctl.

## ******** Feature configuration set **********
# The filter rule set of tables to be migrated from the upstream database instance. You can set multiple rules at the same time.
block-allow-list:                      # Use black-white-list if the DM version is earlier than v2.0.0-beta.2.
  bw-rule-1:                           # The name of the block and allow list rule.
    do-dbs: ["test.*", "user"]         # The allow list of upstream schemas to be migrated. Wildcard characters (*?) are supported. You only need to configure either `do-dbs` or `ignore-dbs`. If both fields are configured, only `do-dbs` takes effect.
    # ignore-dbs: ["mysql", "account"] # The block list of upstream schemas to be migrated. Wildcard characters (*?) are supported.
    do-tables:                         # The allow list of upstream tables to be migrated. You only need to configure either `do-tables` or `ignore-tables`. If both fields are configured, only `do-tables` takes effect.
    - db-name: "test.*"
      tbl-name: "t.*"
    - db-name: "user"
      tbl-name: "information"
  bw-rule-2:                         # The name of the block allow list rule.
    ignore-tables:                   # The block list of data source tables needs to be migrated.
    - db-name: "user"
      tbl-name: "log"

# The filter rule set of data source binlog events.
filters:                                        # You can set multiple rules at the same time.
  filter-rule-1:                                # The name of the filtering rule.
    schema-pattern: "test_*"                    # The pattern of the data source schema name. Wildcard characters (*?) are supported.
    table-pattern: "t_*"                        # The pattern of the data source table name. Wildcard characters (*?) are supported.
    events: ["truncate table", "drop table"]    # The event types to be filtered out in schemas or tables that match the `schema-pattern` or the `table-pattern`.
    action: Ignore                              # Whether to migrate (Do) or ignore (Ignore) the binlog that matches the filtering rule.
  filter-rule-2:
    schema-pattern: "test"
    events: ["all dml"]
    action: Do

# The routing mapping rule set between the data source and target TiDB instance tables.
routes:                           # You can set multiple rules at the same time.
  route-rule-1:                   # The name of the routing mapping rule.
    schema-pattern: "test_*"      # The pattern of the data source schema name. Wildcard characters (*?) are supported.
    table-pattern: "t_*"          # The pattern of the data source table name. Wildcard characters (*?) are supported.
    target-schema: "test"         # The name of the downstream TiDB schema.
    target-table: "t"             # The name of the downstream TiDB table.
  route-rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

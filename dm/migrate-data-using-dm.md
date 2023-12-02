---
title: Migrate Data Using Data Migration
summary: Use the Data Migration tool to migrate the full data and the incremental data.
---

# データ移行を使用してデータを移行する {#migrate-data-using-data-migration}

このガイドでは、データ移行 (DM) ツールを使用してデータを移行する方法を説明します。

## ステップ 1: DM クラスターをデプロイ {#step-1-deploy-the-dm-cluster}

[TiUPを使用して DM クラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)にオススメです。トライアルまたはテスト用に[バイナリを使用して DM クラスターをデプロイする](/dm/deploy-a-dm-cluster-using-binary.md)行うこともできます。

> **注記：**
>
> -   すべての DM 構成ファイルのデータベース パスワードには、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベースのパスワードが空の場合、暗号化する必要はありません。 [dmctlを使用してデータベースのパスワードを暗号化する](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。
> -   アップストリーム データベースとダウンストリーム データベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。

## ステップ 2: クラスター情報を確認する {#step-2-check-the-cluster-information}

TiUPを使用して DM クラスターをデプロイすると、構成情報は以下のようになります。

-   DM クラスター内の関連コンポーネントの構成情報:

    | 成分         | ホスト          | ポート  |
    | ---------- | ------------ | ---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master  | 172.16.10.71 | 8261 |

-   上流および下流のデータベース インスタンスの情報:

    | データベースインスタンス     | ホスト          | ポート  | ユーザー名 | 暗号化されたパスワード                      |
    | ---------------- | ------------ | ---- | ----- | -------------------------------- |
    | アップストリーム MySQL-1 | 172.16.10.81 | 3306 | 根     | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | アップストリーム MySQL-2 | 172.16.10.82 | 3306 | 根     | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | ダウンストリーム TiDB    | 172.16.10.83 | 4000 | 根     |                                  |

MySQL ホストで必要な権限のリストは、 [事前チェック](/dm/dm-precheck.md)ドキュメントに記載されています。

## ステップ 3: データソースを作成する {#step-3-create-data-source}

1.  MySQL-1 関連情報を`conf/source1.yaml`に書き込みます。

    ```yaml
    # MySQL1 Configuration.

    source-id: "mysql-replica-01"
    # This indicates that whether DM-worker uses Global Transaction Identifier (GTID) to pull binlog. Before you use this configuration item, make sure that the GTID mode is enabled in the upstream MySQL.
    enable-gtid: false

    from:
      host: "172.16.10.81"
      user: "root"
      password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="
      port: 3306
    ```

2.  ターミナルで次のコマンドを実行し、 `tiup dmctl`を使用して MySQL-1 データ ソース構成を DM クラスターにロードします。

    ```bash
    tiup dmctl --master-addr 172.16.10.71:8261 operate-source create conf/source1.yaml
    ```

3.  MySQL-2 の場合は、設定ファイル内の関連情報を変更し、 `dmctl`コマンドを実行します。

## ステップ 4: データ移行タスクを構成する {#step-4-configure-the-data-migration-task}

次の例では、上流の MySQL-1 インスタンスと MySQL-2 インスタンスの両方の`test_db`データベースにあるすべての`test_table`テーブル データを、TiDB の`test_db`データベースにあるダウンストリーム`test_table`テーブルに完全データと増分データで移行する必要があることを前提としています。モード。

`task.yaml`タスク構成ファイルを次のように編集します。

```yaml
# The task name. You need to use a different name for each of the multiple tasks that
# run simultaneously.
name: "test"
# The full data plus incremental data (all) migration mode.
task-mode: "all"
# The downstream TiDB configuration information.
target-database:
  host: "172.16.10.83"
  port: 4000
  user: "root"
  password: ""

# Configuration of all the upstream MySQL instances required by the current data migration task.
mysql-instances:
-
  # The ID of upstream instances or the migration group. You can refer to the configuration of `source_id` in the "inventory.ini" file or in the "dm-master.toml" file.
  source-id: "mysql-replica-01"
  # The configuration item name of the block and allow lists of the name of the
  # database/table to be migrated, used to quote the global block and allow
  # lists configuration that is set in the global block-allow-list below.
  block-allow-list: "global"  # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  # The configuration item name of the dump processing unit, used to quote the global configuration of the dump unit.
  mydumper-config-name: "global"

-
  source-id: "mysql-replica-02"
  block-allow-list: "global"  # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  mydumper-config-name: "global"

# The global configuration of block and allow lists. Each instance can quote it by the
# configuration item name.
block-allow-list:                     # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  global:
    do-tables:                        # The allow list of upstream tables to be migrated.
    - db-name: "test_db"              # The database name of the table to be migrated.
      tbl-name: "test_table"          # The name of the table to be migrated.

# The global configuration of the dump unit. Each instance can quote it by the configuration item name.
mydumpers:
  global:
    extra-args: ""
```

## ステップ 5: データ移行タスクを開始する {#step-5-start-the-data-migration-task}

データ移行構成の潜在的なエラーを事前に検出するために、DM は事前チェック機能を提供します。

-   DM は、データ移行タスクの開始時に、対応する権限と構成を自動的にチェックします。
-   `check-task`コマンドを使用して、アップストリームの MySQL インスタンス構成が DM 要件を満たしているかどうかを手動で事前チェ​​ックすることもできます。

事前チェック機能の詳細については、 [アップストリームの MySQL インスタンス構成を事前チェックする](/dm/dm-precheck.md)を参照してください。

> **注記：**
>
> 初めてデータ移行タスクを開始する前に、アップストリームを構成しておく必要があります。それ以外の場合、タスクの開始時にエラーが報告されます。

`tiup dmctl`コマンドを実行してデータ移行タスクを開始します。 `task.yaml`が上記で編集した設定ファイルです。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 start-task ./task.yaml
```

-   上記のコマンドが次の結果を返した場合、タスクが正常に開始されたことを示します。

    ```json
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "172.16.10.72:8262",
                "msg": ""
            },
            {
                "result": true,
                "worker": "172.16.10.73:8262",
                "msg": ""
            }
        ]
    }
    ```

-   データ移行タスクの開始に失敗した場合は、返されたプロンプトに従って構成を変更し、 `start-task task.yaml`コマンドを実行してタスクを再開します。

## ステップ 6: データ移行タスクを確認する {#step-6-check-the-data-migration-task}

タスクの状態、または特定のデータ移行タスクが DM クラスターで実行されているかどうかを確認する必要がある場合は、 `tiup dmctl`で次のコマンドを実行します。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 query-status
```

## ステップ 7: データ移行タスクを停止する {#step-7-stop-the-data-migration-task}

データを移行する必要がなくなった場合は、 `tiup dmctl`で次のコマンドを実行してタスクを停止します。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 stop-task test
```

`test`は`task.yaml`設定ファイルの`name`設定項目に設定したタスク名です。

## ステップ 8: タスクを監視し、ログを確認する {#step-8-monitor-the-task-and-check-logs}

Prometheus、Alertmanager、および Grafana がTiUP を使用した DM クラスターのデプロイメントとともに正常にデプロイされ、Grafana アドレスが`172.16.10.71`であると仮定します。 DM に関連するアラート情報を表示するには、ブラウザで[http://172.16.10.71:9093](http://172.16.10.71:9093)を開き、Alertmanager に入ります。監視メトリックを確認するには、 [http://172.16.10.71:3000](http://172.16.10.71:3000)に進み、DM ダッシュボードを選択します。

DM クラスターの実行中、DM-master、DM-worker、および dmctl はログを通じて監視メトリック情報を出力します。各コンポーネントのログディレクトリは次のとおりです。

-   DM マスター ログ ディレクトリ: `--log-file` DM マスター プロセス パラメーターによって指定されます。 DM がTiUPを使用してデプロイされている場合、ログ ディレクトリは DM マスター ノードの`{log_dir}`です。
-   DM-worker ログ ディレクトリ: `--log-file` DM-worker プロセス パラメーターで指定されます。 TiUPを使用して DM がデプロイされている場合、ログ ディレクトリは DM ワーカー ノードの`{log_dir}`です。

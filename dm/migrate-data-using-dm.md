---
title: Migrate Data Using Data Migration
summary: データ移行ツールを使用して、完全なデータと増分データを移行します。
---

# データ移行を使用してデータを移行する {#migrate-data-using-data-migration}

このガイドでは、データ移行 (DM) ツールを使用してデータを移行する方法を説明します。

## ステップ1: DMクラスターをデプロイ {#step-1-deploy-the-dm-cluster}

[TiUPを使用してDMクラスタを展開する](/dm/deploy-a-dm-cluster-using-tiup.md)を推奨します。試用やテスト用に[バイナリを使用してDMクラスタを展開する](/dm/deploy-a-dm-cluster-using-binary.md)も使用できます。

> **注記：**
>
> -   すべての DM 構成ファイル内のデータベース パスワードについては、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベース パスワードが空の場合は、暗号化する必要はありません。 [dmctlを使用してデータベースパスワードを暗号化する](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。
> -   アップストリーム データベースとダウンストリーム データベースのユーザーには、対応する読み取り権限が必要です。

## ステップ2: クラスター情報を確認する {#step-2-check-the-cluster-information}

TiUPを使用して DM クラスターを展開した後の構成情報は、以下のようになります。

-   DM クラスター内の関連コンポーネントの構成情報:

    | 成分         | ホスト          | ポート  |
    | ---------- | ------------ | ---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_マスター    | 172.16.10.71 | 8261 |

-   アップストリームおよびダウンストリーム データベース インスタンスの情報:

    | データベースインスタンス     | ホスト          | ポート  | ユーザー名 | 暗号化されたパスワード                      |
    | ---------------- | ------------ | ---- | ----- | -------------------------------- |
    | アップストリーム MySQL-1 | 172.16.10.81 | 3306 | 根     | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | アップストリーム MySQL-2 | 172.16.10.82 | 3306 | 根     | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | ダウンストリーム TiDB    | 172.16.10.83 | 4000 | 根     |                                  |

MySQL ホストで必要な権限のリストは、 [事前チェック](/dm/dm-precheck.md)ドキュメントに記載されています。

## ステップ3: データソースを作成する {#step-3-create-data-source}

1.  MySQL-1関連の情報を`conf/source1.yaml`に書き込む:

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

2.  ターミナルで次のコマンドを実行し、 `tiup dmctl`使用して MySQL-1 データ ソース構成を DM クラスターにロードします。

    ```bash
    tiup dmctl --master-addr 172.16.10.71:8261 operate-source create conf/source1.yaml
    ```

3.  MySQL-2 の場合は、設定ファイル内の関連情報を変更し、同じ`dmctl`コマンドを実行します。

## ステップ4: データ移行タスクを構成する {#step-4-configure-the-data-migration-task}

次の例では、アップストリーム MySQL-1 インスタンスと MySQL-2 インスタンスの両方の`test_db`データベースにある`test_table`テーブルのデータすべてを、フル データと増分データ モードで TiDB の`test_db`データベースにあるダウンストリーム`test_table`テーブルに移行する必要があることを前提としています。

`task.yaml`タスク構成ファイルを以下のように編集します。

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

## ステップ5: データ移行タスクを開始する {#step-5-start-the-data-migration-task}

データ移行構成の潜在的なエラーを事前に検出するために、DM は事前チェック機能を提供します。

-   DM は、データ移行タスクを開始するときに、対応する権限と構成を自動的にチェックします。
-   `check-task`コマンドを使用して、アップストリーム MySQL インスタンス構成が DM 要件を満たしているかどうかを手動で事前確認することもできます。

事前チェック機能の詳細については、 [アップストリームのMySQLインスタンス構成を事前に確認する](/dm/dm-precheck.md)参照してください。

> **注記：**
>
> データ移行タスクを初めて開始する前に、アップストリームを構成する必要があります。そうしないと、タスクの開始時にエラーが報告されます。

`tiup dmctl`コマンドを実行してデータ移行タスクを開始します。3 `task.yaml`上記で編集した構成ファイルです。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 start-task ./task.yaml
```

-   上記のコマンドが次の結果を返す場合、タスクが正常に開始されたことを示します。

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

-   データ移行タスクを開始できない場合は、返されたプロンプトに従って構成を変更し、 `start-task task.yaml`コマンドを実行してタスクを再起動します。

## ステップ6: データ移行タスクを確認する {#step-6-check-the-data-migration-task}

タスクの状態を確認する必要がある場合、または特定のデータ移行タスクが DM クラスターで実行されているかどうかを確認する場合は、 `tiup dmctl`で次のコマンドを実行します。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 query-status
```

## ステップ7: データ移行タスクを停止する {#step-7-stop-the-data-migration-task}

データを移行する必要がなくなった場合は、 `tiup dmctl`で次のコマンドを実行してタスクを停止します。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 stop-task test
```

`test`は、 `task.yaml`構成ファイルの`name`構成項目で設定したタスク名です。

## ステップ8: タスクを監視してログを確認する {#step-8-monitor-the-task-and-check-logs}

TiUP を使用して DM クラスターのデプロイメントとともに Prometheus、Alertmanager、および Grafana が正常にデプロイされ、Grafana アドレスが`172.16.10.71`であると仮定します。DM に関連するアラート情報を表示するには、ブラウザーで[http://172.16.10.71:9093](http://172.16.10.71:9093)開いて Alertmanager に入ります。監視メトリックを確認するには、 [http://172.16.10.71:3000](http://172.16.10.71:3000)に移動して DM ダッシュボードを選択します。

DM クラスターの実行中、DM-master、DM-worker、dmctl は監視メトリック情報をログに出力します。各コンポーネントのログ ディレクトリは次のとおりです。

-   DM マスター ログ ディレクトリ: `--log-file` DM マスター プロセス パラメータで指定します。DM がTiUP を使用して展開されている場合、ログ ディレクトリは DM マスター ノードの`{log_dir}`になります。
-   DM-worker ログ ディレクトリ: `--log-file` DM-worker プロセス パラメータで指定します。DM がTiUP を使用してデプロイされている場合、ログ ディレクトリは DM-worker ノードの`{log_dir}`になります。

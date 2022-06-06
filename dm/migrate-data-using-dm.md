---
title: Migrate Data Using Data Migration
summary: Use the Data Migration tool to migrate the full data and the incremental data.
---

# データ移行を使用してデータを移行する {#migrate-data-using-data-migration}

このガイドでは、データ移行（DM）ツールを使用してデータを移行する方法を示します。

## ステップ1：DMクラスタをデプロイ {#step-1-deploy-the-dm-cluster}

[TiUPを使用してDMクラスタをデプロイします](/dm/deploy-a-dm-cluster-using-tiup.md)にすることをお勧めします。トライアルまたはテスト用に[バイナリを使用してDMクラスタをデプロイする](/dm/deploy-a-dm-cluster-using-binary.md)することもできます。

> **ノート：**
>
> -   すべてのDM構成ファイルのデータベースパスワードには、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベースパスワードが空の場合、暗号化する必要はありません。 [dmctlを使用してデータベースパスワードを暗号化します](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。
> -   アップストリームおよびダウンストリームデータベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。

## ステップ2：クラスタ情報を確認する {#step-2-check-the-cluster-information}

TiUPを使用してDMクラスタを展開した後の構成情報は、以下のようになります。

-   DMクラスタの関連コンポーネントの構成情報：

    | 成分         | ホスト          | ポート  |
    | ---------- | ------------ | ---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master  | 172.16.10.71 | 8261 |

-   アップストリームおよびダウンストリームデータベースインスタンスの情報：

    | データベースインスタンス    | ホスト          | ポート  | ユーザー名 | 暗号化されたパスワード                           |
    | --------------- | ------------ | ---- | ----- | ------------------------------------- |
    | アップストリームMySQL-1 | 172.16.10.81 | 3306 | 根     | VjX8cEeTX + qcvZ3bPaO4h0C80pe / 1aU = |
    | アップストリームMySQL-2 | 172.16.10.82 | 3306 | 根     | VjX8cEeTX + qcvZ3bPaO4h0C80pe / 1aU = |
    | ダウンストリームTiDB    | 172.16.10.83 | 4000 | 根     |                                       |

MySQLホストに必要な特権のリストは、 [事前チェック](/dm/dm-precheck.md)のドキュメントに記載されています。

## ステップ3：データソースを作成する {#step-3-create-data-source}

1.  MySQL-1関連情報を`conf/source1.yaml`に書き込みます：

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

2.  ターミナルで次のコマンドを実行し、 `tiup dmctl`を使用してMySQL-1データソース構成をDMクラスタにロードします。

    {{< copyable "" >}}

    ```bash
    tiup dmctl --master-addr 172.16.10.71:8261 operate-source create conf/source1.yaml
    ```

3.  MySQL-2の場合、構成ファイルの関連情報を変更して、同じ`dmctl`コマンドを実行します。

## ステップ4：データ移行タスクを構成する {#step-4-configure-the-data-migration-task}

次の例では、アップストリームMySQL-1インスタンスとMySQL-2インスタンスの両方の`test_db`データベースのすべての`test_table`テーブルデータを、完全データと増分データのTiDBの`test_db`データベースのダウンストリーム`test_table`テーブルに移行する必要があると想定しています。モード。

`task.yaml`のタスク構成ファイルを次のように編集します。

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

## ステップ5：データ移行タスクを開始します {#step-5-start-the-data-migration-task}

データ移行構成で発生する可能性のあるエラーを事前に検出するために、DMは事前チェック機能を提供します。

-   DMは、データ移行タスクの開始時に、対応する特権と構成を自動的にチェックします。
-   `check-task`コマンドを使用して、アップストリームのMySQLインスタンス構成がDM要件を満たしているかどうかを手動で事前チェックすることもできます。

事前チェック機能の詳細については、 [アップストリームのMySQLインスタンス構成を事前に確認します](/dm/dm-precheck.md)を参照してください。

> **ノート：**
>
> データ移行タスクを初めて開始する前に、アップストリームを構成しておく必要があります。それ以外の場合は、タスクの開始中にエラーが報告されます。

`tiup dmctl`コマンドを実行して、データ移行タスクを開始します。 `task.yaml`は、上記で編集した構成ファイルです。

{{< copyable "" >}}

```bash
tiup dmctl --master-addr 172.16.10.71:8261 start-task ./task.yaml
```

-   上記のコマンドが次の結果を返す場合は、タスクが正常に開始されたことを示しています。

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

-   データ移行タスクの開始に失敗した場合は、返されたプロンプトに従って構成を変更してから、 `start-task task.yaml`コマンドを実行してタスクを再開してください。

## 手順6：データ移行タスクを確認する {#step-6-check-the-data-migration-task}

タスクの状態を確認する必要がある場合、または特定のデータ移行タスクがDMクラスタで実行されているかどうかを確認する必要がある場合は、次のコマンドを`tiup dmctl`で実行します。

{{< copyable "" >}}

```bash
tiup dmctl --master-addr 172.16.10.71:8261 query-status
```

## 手順7：データ移行タスクを停止する {#step-7-stop-the-data-migration-task}

データを移行する必要がなくなった場合は、次のコマンドを`tiup dmctl`で実行して、タスクを停止します。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 stop-task test
```

`test`は、 `task.yaml`構成ファイルの`name`構成項目で設定したタスク名です。

## ステップ8：タスクを監視し、ログを確認します {#step-8-monitor-the-task-and-check-logs}

Prometheus、Alertmanager、およびGrafanaが、TiUPを使用したDMクラスタのデプロイとともに正常にデプロイされ、Grafanaアドレスが`172.16.10.71`であると仮定します。 DMに関連するアラート情報を表示するには、ブラウザーで[http://172.16.10.71：9093](http://172.16.10.71:9093)を開き、Alertmanagerに入ります。監視メトリックを確認するには、 [http://172.16.10.71：3000](http://172.16.10.71:3000)に移動し、DMダッシュボードを選択します。

DMクラスタの実行中、DM-master、DM-worker、およびdmctlは、ログを介して監視メトリック情報を出力します。各コンポーネントのログディレクトリは次のとおりです。

-   DM-masterログディレクトリ： `--log-file`のDM-masterプロセスパラメータで指定されます。 DMがTiUPを使用して展開されている場合、ログディレクトリはDMマスターノードで`{log_dir}`です。
-   DM-workerログディレクトリ： `--log-file` -workerプロセスパラメータで指定されます。 DMがTiUPを使用してデプロイされている場合、ログディレクトリはDM-workerノードで`{log_dir}`です。

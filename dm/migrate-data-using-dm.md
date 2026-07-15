---
title: Migrate Data Using Data Migration
summary: データ移行ツールを使用して、全データと増分データを移行します。
---

# データ移行を使用してデータを移行する {#migrate-data-using-data-migration}

このガイドでは、データ移行（DM）ツールを使用してデータを移行する方法を説明します。

## ステップ1：DMクラスターをデプロイ {#step-1-deploy-the-dm-cluster}

[TiUPを使用してDMクラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)のがおすすめです。トライアルやテストのために[バイナリを使用してDMクラスターをデプロイする](/dm/deploy-a-dm-cluster-using-binary.md)もできます。

> **Note:**
>
> -   すべての DM 構成ファイルのデータベース パスワードには、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベースのパスワードが空の場合、暗号化する必要はありません。 [dmctlを使用してデータベースのパスワードを暗号化します](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。
> -   上流および下流データベースのユーザーは、対応する読み取り権限と書き込み権限を持っている必要があります。

## ステップ2：クラスタ情報を確認する {#step-2-check-the-cluster-information}

TiUPを使用してDMクラスタをデプロイした後、構成情報は以下のようになります。

-   DMクラスタ内の関連コンポーネントの構成情報：

    | 成分         | ホスト          | ポート  |
    | ---------- | ------------ | ---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master  | 172.16.10.71 | 8261 |

-   上流および下流のデータベースインスタンスの情報：

    | データベースインスタンス     | ホスト          | ポート  | ユーザー名 | 暗号化されたパスワード                      |
    | ---------------- | ------------ | ---- | ----- | -------------------------------- |
    | アップストリームのMySQL-1 | 172.16.10.81 | 3306 | 根     | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | アップストリームのMySQL-2 | 172.16.10.82 | 3306 | 根     | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | ダウンストリーム TiDB    | 172.16.10.83 | 4000 | 根     |                                  |

MySQL ホストで必要な権限のリストは[事前チェック](/dm/dm-precheck.md)ドキュメントに記載されています。

## ステップ3：データソースを作成する {#step-3-create-data-source}

1.  `conf/source1.yaml`にMySQL-1関連の情報を書き込みます。

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

    ```bash
    tiup dmctl --master-addr 172.16.10.71:8261 operate-source create conf/source1.yaml
    ```

3.  MySQL-2 の場合は、設定ファイル内の関連情報を変更し、同じ`dmctl`コマンドを実行します。

## ステップ4：データ移行タスクの設定 {#step-4-configure-the-data-migration-task}

次の例では、上流の MySQL-1 および MySQL-2 インスタンスの`test_table`データベースにある`test_db`テーブルのすべてのデータを、TiDB の`test_table`データベースにある下流の`test_db`テーブルに、フルデータと増分データの両方のモードで移行する必要があることを想定しています。

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

## ステップ5：データ移行タスクを開始する {#step-5-start-the-data-migration-task}

データ移行設定における潜在的なエラーを事前に検出するために、DMは事前チェック機能を提供します。

-   DMは、データ移行タスクを開始する際に、対応する権限と構成を自動的にチェックします。
-   `check-task`コマンドを使用して、アップストリームの MySQL インスタンス構成が DM の要件を満たしているかどうかを手動で事前確認することもできます。

事前チェック機能の詳細については、[アップストリームのMySQLインスタンス構成を事前に確認する](/dm/dm-precheck.md)を参照してください。

> **Note:**
>
> データ移行タスクを初めて開始する前に、アップストリームの設定を完了しておく必要があります。設定が完了していない場合、タスクの開始時にエラーが発生します。

データ移行タスクを開始するには、 `tiup dmctl`コマンドを実行してください。 `task.yaml`は、上記で編集した構成ファイルです。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 start-task ./task.yaml
```

-   上記のコマンドが以下の結果を返した場合、タスクが正常に開始されたことを示します。

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

-   データ移行タスクの開始に失敗した場合は、表示されたプロンプトに従って設定を変更し、 `start-task task.yaml`コマンドを実行してタスクを再起動してください。

## ステップ6：データ移行タスクを確認する {#step-6-check-the-data-migration-task}

タスクの状態を確認したり、特定のデータ移行タスクが DM クラスターで実行されているかどうかを確認したりする必要がある場合は、 `tiup dmctl`で次のコマンドを実行します。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 query-status
```

## ステップ7：データ移行タスクを停止する {#step-7-stop-the-data-migration-task}

データの移行が不要になった場合は、 `tiup dmctl`で次のコマンドを実行してタスクを停止してください。

```bash
tiup dmctl --master-addr 172.16.10.71:8261 stop-task test
```

`test`は`name`設定ファイルの`task.yaml`設定項目で設定したタスク名です。

## ステップ8：タスクを監視し、ログを確認する {#step-8-monitor-the-task-and-check-logs}

TiUPを使用して DM クラスタのデプロイとともに Prometheus、Alertmanager、および Grafana が正常にデプロイされ、Grafana のアドレスが`172.16.10.71`であると仮定します。DM に関連するアラート情報を表示するには、ブラウザで[http://172.16.10.71:9093](http://172.16.10.71:9093)を開き、Alertmanager にアクセスします。監視メトリックを確認するには、 [http://172.16.10.71:3000](http://172.16.10.71:3000)にアクセスし、DM ダッシュボードを選択します。

DMクラスタの実行中、DMマスター、DMワーカー、およびdmctlは、監視メトリクス情報をログに出力します。各コンポーネントのログディレクトリは以下のとおりです。

-   DMマスターのログディレクトリ：これは`--log-file` DMマスタープロセスパラメータで指定されます。DMがTiUPを使用してデプロイされている場合、ログディレクトリはDMマスターノードの`{log_dir}`になります。
-   DMワーカーのログディレクトリ：これは`--log-file` DMワーカープロセスパラメータで指定されます。DMがTiUPを使用してデプロイされている場合、ログディレクトリはDMワーカーノードの`{log_dir}`になります。

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB Admin Lab 10: Migrating Data Using TiDB Data Migration" type="lab" link="https://labs.tidb.io/labs/dba_303_lab_ff9" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch11_en.png" duration="60 mins" />
</RelatedResources>

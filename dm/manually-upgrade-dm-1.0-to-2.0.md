---
title: Manually Upgrade TiDB Data Migration from v1.0.x to v2.0+
summary: Learn how to manually upgrade TiDB data migration from v1.0.x to v2.0+.
---

# TiDBデータ移行をv1.0.xからv2.0+に手動でアップグレードする {#manually-upgrade-tidb-data-migration-from-v1-0-x-to-v2-0}

このドキュメントでは、TiDBDMツールをv1.0.xからv2.0+に手動でアップグレードする方法を紹介します。主なアイデアは、v1.0.xのグローバルチェックポイント情報を使用して、v2.0+クラスタで新しいデータ移行タスクを開始することです。

TiDBDMツールをv1.0.xからv2.0+に自動的にアップグレードする方法については、 [TiUPを使用して、DM-Ansibleによってデプロイされた1.0クラスタを自動的にインポートします](/dm/maintain-dm-using-tiup.md#import-and-upgrade-a-dm-10-cluster-deployed-using-dm-ansible)を参照してください。

> **ノート：**
>
> -   現在、データ移行タスクが完全エクスポートまたは完全インポートの処理中である場合、DMをv1.0.xからv2.0+にアップグレードすることはサポートされていません。
> -   DMクラスタのコンポーネント間の相互作用に使用されるgRPCプロトコルは大幅に更新されるため、アップグレードの前後でDMコンポーネント（dmctlを含む）が同じバージョンを使用していることを確認する必要があります。
> -   DMクラスタのメタデータストレージ（チェックポイント、シャードDDLロックステータス、オンラインDDLメタデータなど）が大幅に更新されるため、v1.0.xのメタデータをv2.0+で自動的に再利用することはできません。したがって、アップグレード操作を実行する前に、次の要件が満たされていることを確認する必要があります。
>     -   すべてのデータ移行タスクは、シャードDDL調整のプロセスではありません。
>     -   すべてのデータ移行タスクがオンラインDDL調整の過程にあるわけではありません。

手動アップグレードの手順は次のとおりです。

## ステップ1：v2.0+構成ファイルを準備する {#step-1-prepare-v2-0-configuration-file}

v2.0 +の準備された構成ファイルには、アップストリームデータベースの構成ファイルとデータ移行タスクの構成ファイルが含まれています。

### アップストリームデータベース構成ファイル {#upstream-database-configuration-file}

v2.0 +では、 [アップストリームデータベース構成ファイル](/dm/dm-source-configuration-file.md)はDMワーカーのプロセス構成から分離されているため、 [v1.0.xDMワーカー構成](/dm/dm-worker-configuration-file.md)に基づいてソース構成を取得する必要があります。

> **ノート：**
>
> v1.0.xからv2.0+へのアップグレード中にソース構成の`enable-gtid`が有効になっている場合は、binlogまたはリレーログファイルを解析して、binlogの位置に対応するGTIDセットを取得する必要があります。

#### DM-Ansibleによってデプロイされたv1.0.xクラスタをアップグレードします {#upgrade-a-v1-0-x-cluster-deployed-by-dm-ansible}

v1.0.x DMクラスタがDM-Ansibleによってデプロイされ、次の`dm_worker_servers`の構成が`inventory.ini`のファイルにあると想定します。

```ini
[dm_master_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

次に、それを次の2つのソース構成ファイルに変換できます。

```yaml
# The source configuration corresponding to the original dm_worker1. For example, it is named as source1.yaml.
server-id: 101                                   # Corresponds to the original `server_id`.
source-id: "mysql-replica-01"                    # Corresponds to the original `source_id`.
from:
  host: "172.16.10.81"                           # Corresponds to the original `mysql_host`.
  port: 3306                                     # Corresponds to the original `mysql_port`.
  user: "root"                                   # Corresponds to the original `mysql_user`.
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # Corresponds to the original `mysql_password`.
```

```yaml
# The source configuration corresponding to the original dm_worker2. For example, it is named as source2.yaml.
server-id: 102                                   # Corresponds to the original `server_id`.
source-id: "mysql-replica-02"                    # Corresponds to the original `source_id`.
from:
  host: "172.16.10.82"                           # Corresponds to the original `mysql_host`.
  port: 3306                                     # Corresponds to the original `mysql_port`.
  user: "root"                                   # Corresponds to the original `mysql_user`.
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # Corresponds to the original `mysql_password`.
```

#### バイナリによってデプロイされたv1.0.xクラスタをアップグレードします {#upgrade-a-v1-0-x-cluster-deployed-by-binary}

v1.0.x DMクラスタがバイナリーによってデプロイされ、対応するDM-worker構成が次のとおりであると想定します。

```toml
log-level = "info"
log-file = "dm-worker.log"
worker-addr = ":8262"
server-id = 101
source-id = "mysql-replica-01"
flavor = "mysql"
[from]
host = "172.16.10.81"
user = "root"
password = "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="
port = 3306
```

次に、それを次のソース構成ファイルに変換できます。

```yaml
server-id: 101                                   # Corresponds to the original `server-id`.
source-id: "mysql-replica-01"                    # Corresponds to the original `source-id`.
flavor: "mysql"                                  # Corresponds to the original `flavor`.
from:
  host: "172.16.10.81"                           # Corresponds to the original `from.host`.
  port: 3306                                     # Corresponds to the original `from.port`.
  user: "root"                                   # Corresponds to the original `from.user`.
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # Corresponds to the original `from.password`.
```

### データ移行タスク構成ファイル {#data-migration-task-configuration-file}

[データ移行タスク構成ガイド](/dm/dm-task-configuration-guide.md)の場合、v2.0+は基本的にv1.0.xと互換性があります。 v1.0.xの構成を直接コピーできます。

## ステップ2：v2.0+クラスタをデプロイ {#step-2-deploy-the-v2-0-cluster}

> **ノート：**
>
> 他のv2.0+クラスターを使用できる場合は、この手順をスキップしてください。

[TiUPを使用する](/dm/deploy-a-dm-cluster-using-tiup.md)は、必要なノード数に応じて新しいv2.0+クラスタをデプロイします。

## 手順3：v1.0.xクラスタを停止する {#step-3-stop-the-v1-0-x-cluster}

元のv1.0.xクラスタがDM-Ansibleによってデプロイされている場合は、 [DM-v1.0.xクラスタを停止できます](https://docs.pingcap.com/tidb-data-migration/v1.0/cluster-operations#stop-a-cluster)を使用する必要があります。

元のv1.0.xクラスタがバイナリーでデプロイされている場合は、DM-workerおよびDM-masterプロセスを直接停止できます。

## ステップ4：データ移行タスクをアップグレードする {#step-4-upgrade-data-migration-task}

1.  [`operate-source`](/dm/dm-manage-source.md#operate-data-source)コマンドを使用して、アップストリームデータベースソース設定を[ステップ1](#step-1-prepare-v20-configuration-file)からv2.0+クラスタにロードします。

2.  ダウンストリームTiDBクラスタで、v1.0.xデータ移行タスクのインクリメンタルチェックポイントテーブルから対応するグローバルチェックポイント情報を取得します。

    -   v1.0.xデータ移行構成で`meta-schema`が指定されておらず（またはその値がデフォルトの`dm_meta`として指定されて）、対応するタスク名が`task_v1`であるとすると、対応するチェックポイント情報はダウンストリームTiDBの`` `dm_meta`.`task_v1_syncer_checkpoint` ``テーブルにあります。
    -   次のSQLステートメントを使用して、データ移行タスクに対応するすべてのアップストリームデータベースソースのグローバルチェックポイント情報を取得します。

        ```sql
        > SELECT `id`, `binlog_name`, `binlog_pos` FROM `dm_meta`.`task_v1_syncer_checkpoint` WHERE `is_global`=1;
        +------------------+-------------------------+------------+
        | id               | binlog_name             | binlog_pos |
        +------------------+-------------------------+------------+
        | mysql-replica-01 | mysql-bin|000001.000123 | 15847      |
        | mysql-replica-02 | mysql-bin|000001.000456 | 10485      |
        +------------------+-------------------------+------------+
        ```

3.  v1.0.xデータ移行タスク構成ファイルを更新して、新しいv2.0+データ移行タスクを開始します。

    -   v1.0.xのデータ移行タスク構成ファイルが`task_v1.yaml`の場合は、それをコピーして`task_v2.yaml`に名前を変更します。
    -   `task_v2.yaml`に次の変更を加えます。
        -   `name`を`task_v2`などの新しい名前に変更します。
        -   `task-mode`を`incremental`に変更します。
        -   手順2で取得したグローバルチェックポイント情報に従って、各ソースの増分レプリケーションの開始点を設定します。次に例を示します。

            ```yaml
            mysql-instances:
              - source-id: "mysql-replica-01"        # Corresponds to the `id` of the checkpoint information.
                meta:
                  binlog-name: "mysql-bin.000123"    # Corresponds to the `binlog_name` in the checkpoint information, excluding the part of `|000001`.
                  binlog-pos: 15847                  # Corresponds to `binlog_pos` in the checkpoint information.

              - source-id: "mysql-replica-02"
                meta:
                  binlog-name: "mysql-bin.000456"
                  binlog-pos: 10485
            ```

            > **ノート：**
            >
            > ソース構成で`enable-gtid`が有効になっている場合、現在、binlogまたはリレーログファイルを解析して、binlogの位置に対応するGTIDセットを取得し、 `meta`で`binlog-gtid`に設定する必要があります。

4.  [`start-task`](/dm/dm-create-task.md)コマンドを使用して、v2.0+データ移行タスク構成ファイルを介してアップグレードされたデータ移行タスクを開始します。

5.  [`query-status`](/dm/dm-query-status.md)コマンドを使用して、データ移行タスクが正常に実行されているかどうかを確認します。

データ移行タスクが正常に実行されている場合は、v2.0+へのDMアップグレードが成功したことを示しています。

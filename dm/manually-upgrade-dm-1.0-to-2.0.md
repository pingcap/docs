---
title: Manually Upgrade TiDB Data Migration from v1.0.x to v2.0+
summary: TiDB データ移行を v1.0.x から v2.0+ に手動でアップグレードする方法を学習します。
---

# TiDB データ移行を v1.0.x から v2.0+ に手動でアップグレードする {#manually-upgrade-tidb-data-migration-from-v1-0-x-to-v2-0}

このドキュメントでは、TiDB DM ツールを v1.0.x から v2.0+ に手動でアップグレードする方法を紹介します。主な考え方は、v1.0.x のグローバル チェックポイント情報を使用して、v2.0+ クラスターで新しいデータ移行タスクを開始することです。

TiDB DM ツールを v1.0.x から v2.0+ に自動的にアップグレードする方法については、 [TiUPを使用して、DM-Ansible によってデプロイされた 1.0 クラスターを自動的にインポートする](/dm/maintain-dm-using-tiup.md#import-and-upgrade-a-dm-10-cluster-deployed-using-dm-ansible)を参照してください。

> **注記：**
>
> -   現在、データ移行タスクが完全エクスポートまたは完全インポートのプロセス中の場合、DM を v1.0.x から v2.0+ にアップグレードすることはサポートされていません。
> -   DM クラスターのコンポーネント間のやり取りに使用される gRPC プロトコルが大幅に更新されるため、アップグレードの前後で DM コンポーネント (dmctl を含む) が同じバージョンを使用していることを確認する必要があります。
> -   DM クラスターのメタデータstorage(チェックポイント、シャード DDL ロック ステータス、オンライン DDL メタデータなど) が大幅に更新されるため、v1.0.x のメタデータを v2.0+ で自動的に再利用することはできません。そのため、アップグレード操作を実行する前に、次の要件が満たされていることを確認する必要があります。
>     -   すべてのデータ移行タスクがシャード DDL 調整プロセス中ではありません。
>     -   すべてのデータ移行タスクがオンライン DDL 調整のプロセス中にあるわけではありません。

手動アップグレードの手順は次のとおりです。

## ステップ1: v2.0+構成ファイルを準備する {#step-1-prepare-v2-0-configuration-file}

v2.0+ で準備された構成ファイルには、アップストリーム データベースの構成ファイルとデータ移行タスクの構成ファイルが含まれます。

### 上流データベース構成ファイル {#upstream-database-configuration-file}

v2.0 以降では、 [アップストリームデータベース構成ファイル](/dm/dm-source-configuration-file.md)​​ DM ワーカーのプロセス構成から分離されているため、 [v1.0.x DMワーカー構成](/dm/dm-worker-configuration-file.md)に基づいてソース構成を取得する必要があります。

> **注記：**
>
> v1.0.x から v2.0+ へのアップグレード中にソース構成の`enable-gtid`が有効になっている場合は、 binlogまたはリレー ログ ファイルを解析して、 binlog の位置に対応する GTID セットを取得する必要があります。

#### DM-Ansible によってデプロイされた v1.0.x クラスターをアップグレードする {#upgrade-a-v1-0-x-cluster-deployed-by-dm-ansible}

v1.0.x DM クラスターが DM-Ansible によってデプロイされ、次の`dm_worker_servers`構成が`inventory.ini`ファイルにあると仮定します。

```ini
[dm_master_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

次に、次の 2 つのソース構成ファイルに変換できます。

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

#### バイナリでデプロイされたv1.0.xクラスタをアップグレードする {#upgrade-a-v1-0-x-cluster-deployed-by-binary}

v1.0.x DM クラスターがバイナリでデプロイされ、対応する DM ワーカー構成が次のようになっていると仮定します。

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

次に、次のソース構成ファイルに変換できます。

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

[データ移行タスク構成ガイド](/dm/dm-task-configuration-guide.md)については、v2.0+ は基本的に v1.0.x と互換性があります。v1.0.x の設定をそのままコピーできます。

## ステップ2: v2.0+クラスターをデプロイ {#step-2-deploy-the-v2-0-cluster}

> **注記：**
>
> 他の v2.0+ クラスターが利用可能な場合は、この手順をスキップしてください。

[TiUPを使用する](/dm/deploy-a-dm-cluster-using-tiup.md) 、必要なノード数に応じて新しい v2.0+ クラスターをデプロイします。

## ステップ3: v1.0.xクラスターを停止する {#step-3-stop-the-v1-0-x-cluster}

元の v1.0.x クラスターが DM-Ansible によってデプロイされている場合は、 [DM-Ansible で v1.0.x クラスターを停止する](https://docs.pingcap.com/tidb-data-migration/v1.0/cluster-operations#stop-a-cluster)使用する必要があります。

元の v1.0.x クラスターがバイナリでデプロイされている場合は、DM-worker プロセスと DM-master プロセスを直接停止できます。

## ステップ4: データ移行タスクのアップグレード {#step-4-upgrade-data-migration-task}

1.  [`operate-source`](/dm/dm-manage-source.md#operate-data-source)コマンドを使用して、アップストリーム データベース ソース構成を[ステップ1](#step-1-prepare-v20-configuration-file)から v2.0+ クラスターにロードします。

2.  ダウンストリーム TiDB クラスターで、v1.0.x データ移行タスクの増分チェックポイント テーブルから対応するグローバル チェックポイント情報を取得します。

    -   v1.0.x データ移行構成で`meta-schema`指定されておらず（またはその値がデフォルトの`dm_meta`に指定されており）、対応するタスク名が`task_v1`で、対応するチェックポイント情報がダウンストリーム TiDB の`` `dm_meta`.`task_v1_syncer_checkpoint` ``テーブルにあると仮定します。
    -   次の SQL ステートメントを使用して、データ移行タスクに対応するすべての上流データベース ソースのグローバル チェックポイント情報を取得します。

        ```sql
        > SELECT `id`, `binlog_name`, `binlog_pos` FROM `dm_meta`.`task_v1_syncer_checkpoint` WHERE `is_global`=1;
        +------------------+-------------------------+------------+
        | id               | binlog_name             | binlog_pos |
        +------------------+-------------------------+------------+
        | mysql-replica-01 | mysql-bin|000001.000123 | 15847      |
        | mysql-replica-02 | mysql-bin|000001.000456 | 10485      |
        +------------------+-------------------------+------------+
        ```

3.  新しい v2.0+ データ移行タスクを開始するには、v1.0.x データ移行タスク構成ファイルを更新します。

    -   v1.0.x のデータ移行タスク構成ファイルが`task_v1.yaml`の場合は、それをコピーして`task_v2.yaml`に名前を変更します。
    -   `task_v2.yaml`に次の変更を加えます。
        -   `name` `task_v2`などの新しい名前に変更します。
        -   `task-mode` `incremental`に変更します。
        -   手順 2 で取得したグローバル チェックポイント情報に従って、各ソースの増分レプリケーションの開始点を設定します。例:

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

            > **注記：**
            >
            > ソース構成で`enable-gtid`有効になっている場合、現在は、 binlogまたはリレー ログ ファイルを解析して、 binlog の位置に対応する GTID セットを取得し、 `meta`で`binlog-gtid`に設定する必要があります。

4.  [`start-task`](/dm/dm-create-task.md)コマンドを使用して、v2.0+ データ移行タスク構成ファイルを通じてアップグレードされたデータ移行タスクを開始します。

5.  [`query-status`](/dm/dm-query-status.md)コマンドを使用して、データ移行タスクが正常に実行されているかどうかを確認します。

データ移行タスクが正常に実行された場合、DM の v2.0+ へのアップグレードが成功したことを示します。

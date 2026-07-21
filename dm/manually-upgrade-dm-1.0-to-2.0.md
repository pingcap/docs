---
title: Manually Upgrade TiDB Data Migration from v1.0.x to v2.0+
summary: TiDB Data Migrationをv1.0.xからv2.0+へ手動でアップグレードする方法を学びましょう。
---

# TiDB Data Migrationをv1.0.xからv2.0+へ手動でアップグレードする {#manually-upgrade-tidb-data-migration-from-v10x-to-v20}

このドキュメントでは、TiDB DMツールをv1.0.xからv2.0+に手動でアップグレードする方法について説明します。主な手順は、v1.0.xのグローバルチェックポイント情報を使用して、v2.0+クラスタで新しいデータ移行タスクを開始することです。

TiDB DM ツールを v1.0.x から v2.0+ に自動的にアップグレードする方法については、 [TiUPを使用して、DM-Ansibleによってデプロイされた1.0クラスターを自動的にインポートする](/dm/maintain-dm-using-tiup.md#import-and-upgrade-a-dm-10-cluster-deployed-using-dm-ansible)。

> **Note:**
>
> -   現在、データ移行タスクが完全エクスポートまたは完全インポートの処理中の場合、DMをv1.0.xからv2.0+にアップグレードすることはサポートされていません。
> -   DMクラスタのコンポーネント間の通信に使用されるgRPCプロトコルが大幅に更新されるため、アップグレードの前後でDMコンポーネント（dmctlを含む）が同じバージョンを使用していることを確認する必要があります。
> -   DMクラスタのメタデータストレージ（チェックポイント、シャードDDLロックステータス、オンラインDDLメタデータなど）が大幅に更新されるため、v1.0.xのメタデータはv2.0+で自動的に再利用できません。そのため、アップグレード操作を実行する前に、以下の要件を満たしていることを確認する必要があります。
>     -   すべてのデータ移行タスクがシャードDDL調整プロセスに含まれるわけではありません。
>     -   すべてのデータ移行タスクがオンラインDDL調整プロセスに含まれているわけではありません。

手動アップグレードの手順は以下のとおりです。

## ステップ1：v2.0+設定ファイルを準備する {#step-1-prepare-v20-configuration-file}

バージョン2.0以降で準備された構成ファイルには、上流データベースの構成ファイルとデータ移行タスクの構成ファイルが含まれています。

### アップストリームデータベース構成ファイル {#upstream-database-configuration-file}

v2.0以降では、[アップストリームデータベース構成ファイル](/dm/dm-source-configuration-file.md)ファイルがDMワーカーのプロセス構成から分離されているため、 [v1.0.x DMワーカー設定](/dm/dm-worker-configuration-file.md)をベースにしたソース構成を取得する必要があります。

> **Note:**
>
> v1.0.x から v2.0+ へのアップグレード中にソース構成の`enable-gtid`が有効になっている場合、 binlogまたはリレーログファイルを解析して、 binlog の位置に対応する GTID セットを取得する必要があります。

#### DM-Ansibleによってデプロイされたv1.0.xクラスターをアップグレードする {#upgrade-a-v10x-cluster-deployed-by-dm-ansible}

v1.0.x DM クラスターが DM-Ansible によってデプロイされ、 `dm_worker_servers`ファイルに次の`inventory.ini`設定が含まれていると仮定します。

```ini
[dm_master_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

そうすれば、以下の2つのソース設定ファイルに変換できます。

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

#### バイナリによってデプロイされたv1.0.xクラスターをアップグレードする {#upgrade-a-v10x-cluster-deployed-by-binary}

v1.0.x DM クラスターがバイナリによってデプロイされ、対応する DM-worker 構成が以下のようになっていると仮定します。

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

そうすれば、以下のソース設定ファイルに変換できます。

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

[データ移行タスク構成ガイド](/dm/dm-task-configuration-guide.md)については、v2.0+ は基本的に v1.0.x と互換性があります。 v1.0.x の設定を直接コピーできます。

## ステップ2：v2.0+クラスターをデプロイ {#step-2-deploy-the-v20-cluster}

> **Note:**
>
> 他のv2.0以降のクラスターが利用可能な場合は、この手順をスキップしてください。

[TiUPを使用する](/dm/deploy-a-dm-cluster-using-tiup.md)必要なノード数に応じて新しい v2.0+ クラスターをデプロイします。

## ステップ3：v1.0.xクラスタを停止します {#step-3-stop-the-v10x-cluster}

元の v1.0.x クラスターが DM-Ansible によってデプロイされている場合は、 [DM-Ansibleを使用してv1.0.xクラスタを停止します](https://docs-archive.pingcap.com/tidb-data-migration/v1.0/cluster-operations#stop-a-cluster) 。

元のv1.0.xクラスタがバイナリでデプロイされている場合は、DM-workerプロセスとDM-masterプロセスを直接停止できます。

## ステップ4：データ移行タスクのアップグレード {#step-4-upgrade-data-migration-task}

1.  [`operate-source`](/dm/dm-manage-source.md#operate-data-source)コマンドを使用して、アップストリーム データベース ソース構成を[ステップ1](#step-1-prepare-v20-configuration-file)から v2.0+ クラスターにロードします。

2.  下流のTiDBクラスタでは、v1.0.xデータ移行タスクの増分チェックポイントテーブルから、対応するグローバルチェックポイント情報を取得します。

    -   v1.0.x データ移行構成で`meta-schema`が指定されていない（またはデフォルト値`dm_meta`として指定されている）場合、対応するタスク名が`task_v1`であると仮定すると、対応するチェックポイント情報は、ダウンストリーム TiDB の`` `dm_meta`.`task_v1_syncer_checkpoint` ``テーブルにあります。
    -   データ移行タスクに対応するすべての上流データベースソースのグローバルチェックポイント情報を取得するには、以下のSQL文を使用します。

        ```sql
        > SELECT `id`, `binlog_name`, `binlog_pos` FROM `dm_meta`.`task_v1_syncer_checkpoint` WHERE `is_global`=1;
        +------------------+-------------------------+------------+
        | id               | binlog_name             | binlog_pos |
        +------------------+-------------------------+------------+
        | mysql-replica-01 | mysql-bin|000001.000123 | 15847      |
        | mysql-replica-02 | mysql-bin|000001.000456 | 10485      |
        +------------------+-------------------------+------------+
        ```

3.  新しいv2.0以降のデータ移行タスクを開始するには、v1.0.xのデータ移行タスク構成ファイルを更新してください。

    -   v1.0.x のデータ移行タスク構成ファイルが`task_v1.yaml`の場合、それをコピーして`task_v2.yaml`に名前を変更します。
    -   `task_v2.yaml`に対して以下の変更を行ってください。
        -   `name` `task_v2`などの新しい名前に変更します。
        -   `task-mode`を`incremental`に変更します。
        -   ステップ2で取得したグローバルチェックポイント情報に基づいて、各ソースの増分レプリケーションの開始点を設定します。例：

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

            > **Note:**
            >
            > ソース構成で`enable-gtid`が有効になっている場合、現在、binlogまたはリレーログファイルを解析して、binlogの位置に対応する GTID セットを取得し、それを`binlog-gtid`の`meta` } に設定する必要があります。

4.  [`start-task`](/dm/dm-create-task.md)コマンドを使用して、v2.0以降のデータ移行タスク構成ファイルからアップグレードされたデータ移行タスクを開始します。

5.  [`query-status`](/dm/dm-query-status.md)コマンドを使用して、データ移行タスクが正常に実行されているかどうかを確認してください。

データ移行タスクが正常に実行された場合、DMのv2.0+へのアップグレードが成功したことを示します。

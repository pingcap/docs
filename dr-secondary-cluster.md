---
title: DR Solution Based on Primary and Secondary Clusters
summary: Learn how to implement primary-secondary disaster recovery based on TiCDC.
---

# プライマリ クラスタとセカンダリ クラスタに基づく DR ソリューション {#dr-solution-based-on-primary-and-secondary-clusters}

プライマリ データベースとセカンダリ データベースに基づく災害復旧 (DR) は、一般的なソリューションです。このソリューションでは、DR システムにはプライマリ クラスターとセカンダリ クラスターがあります。プライマリ クラスタはユーザーのリクエストを処理し、セカンダリ クラスタはプライマリ クラスタからのデータをバックアップします。プライマリ クラスタに障害が発生した場合、セカンダリ クラスタがサービスを引き継ぎ、バックアップ データを使用してサービスを提供し続けます。これにより、ビジネス システムは障害による中断なしに正常に動作し続けることが保証されます。

プライマリ-セカンダリ DR ソリューションには次の利点があります。

-   高可用性: プライマリ-セカンダリアーキテクチャによりシステムの可用性が向上し、障害からの迅速な回復が保証されます。
-   高速スイッチオーバー: プライマリ クラスタに障害が発生した場合、システムはすぐにセカンダリ クラスタに切り替えてサービスを提供し続けることができます。
-   データの一貫性: セカンダリ クラスタは、プライマリ クラスタからほぼリアルタイムでデータをバックアップします。このようにして、障害によりシステムがセカンダリ クラスターに切り替わっても、データは基本的に最新の状態になります。

この文書には次の内容が含まれています。

-   プライマリ クラスタとセカンダリ クラスタをセットアップします。
-   プライマリ クラスタからセカンダリ クラスタにデータをレプリケートします。
-   クラスターを監視します。
-   DRスイッチオーバーを実行します。

一方、このドキュメントでは、セカンダリ クラスタでビジネス データをクエリする方法と、プライマリ クラスタとセカンダリ クラスタの間で双方向レプリケーションを実行する方法についても説明します。

## TiCDC に基づいてプライマリ クラスタとセカンダリ クラスタをセットアップする {#set-up-primary-and-secondary-clusters-based-on-ticdc}

### アーキテクチャ {#architecture}

![TiCDC secondary cluster architecture](/media/dr/dr-ticdc-secondary-cluster.png)

前述のアーキテクチャには、プライマリ クラスタとセカンダリ クラスタの 2 つの TiDB クラスタが含まれています。

-   プライマリ クラスター: リージョン 1 で実行され、3 つのレプリカを持つアクティブなクラスター。このクラスターは読み取りおよび書き込みリクエストを処理します。
-   セカンダリ クラスター: リージョン 2 で実行され、TiCDC を介してプライマリ クラスターからデータをレプリケートするスタンバイ クラスター。

この DRアーキテクチャはシンプルで使いやすいです。 DR システムは地域的な障害に耐えることができるため、プライマリ クラスタの書き込みパフォーマンスが低下しないことが保証され、セカンダリ クラスタは遅延の影響を受けない一部の読み取り専用ビジネスを処理できます。このソリューションの目標復旧時点 (RPO) は秒単位であり、目標復旧時間 (RTO) は分またはそれより短い場合もあります。これは、多くのデータベース ベンダーが重要な本番システムに対して推奨しているソリューションです。

> **注記：**
>
> -   [TiKVの「リージョン」](/glossary.md#regionpeerraft-group)データの範囲を意味し、「領域」という用語は物理的な位置を意味します。この 2 つの用語は互換性がありません。
> -   セカンダリ クラスターにデータをレプリケートするために複数の変更フィードを実行したり、セカンダリ クラスターがすでに存在する状態で別のセカンダリ クラスターを実行したりしないでください。そうしないと、セカンダリ クラスターのデータ トランザクションの整合性が保証されません。

### プライマリ クラスタとセカンダリ クラスタをセットアップする {#set-up-primary-and-secondary-clusters}

このドキュメントでは、TiDB プライマリ クラスターとセカンダリ クラスターが 2 つの異なるリージョン (リージョン 1 とリージョン 2) にデプロイされています。プライマリ クラスタとセカンダリ クラスタの間には一定のネットワークレイテンシーが存在するため、TiCDC はセカンダリ クラスタと一緒にデプロイされます。 TiCDC をセカンダリ クラスターとともに展開すると、ネットワークレイテンシーの影響を回避でき、最適なレプリケーション パフォーマンスの実現に役立ちます。このドキュメントで提供される例のデプロイメント トポロジは次のとおりです (1 つのコンポーネントノードが 1 つのサーバーにデプロイされます)。

| リージョン  | ホスト                        | クラスタ | 成分                               |
| ------ | -------------------------- | ---- | -------------------------------- |
| リージョン1 | 10.0.1.9                   | 主要な  | Monitor、Grafana、または AlterManager |
| リージョン2 | 10.0.1.11                  | 二次   | Monitor、Grafana、または AlterManager |
| リージョン1 | 10.0.1.1/10.0.1.2/10.0.1.3 | 主要な  | PD                               |
| リージョン2 | 10.1.1.1/10.1.1.2/10.1.1.3 | 二次   | PD                               |
| リージョン2 | 10.1.1.9/10.1.1.10         | 主要な  | TiCDC                            |
| リージョン1 | 10.0.1.4/10.0.1.5          | 主要な  | TiDB                             |
| リージョン2 | 10.1.1.4/10.1.1.5          | 二次   | TiDB                             |
| リージョン1 | 10.0.1.6/10.0.1.7/10.0.1.8 | 主要な  | TiKV                             |
| リージョン2 | 10.1.1.6/10.1.1.7/10.1.1.8 | 二次   | TiKV                             |

サーバー構成については、次のドキュメントを参照してください。

-   [TiDB のソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)
-   [TiCDC のソフトウェアおよびハードウェアの推奨事項](/ticdc/deploy-ticdc.md#software-and-hardware-recommendations)

TiDB プライマリ クラスターとセカンダリ クラスターを展開する方法の詳細については、 [TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。

TiCDC を展開するときは、セカンダリ クラスターと TiCDC を一緒に展開して管理し、それらの間のネットワークを接続する必要があることに注意してください。

-   TiCDC を既存のプライマリ クラスターにデプロイするには、 [TiCDCのデプロイ](/ticdc/deploy-ticdc.md#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup)を参照してください。
-   新しいプライマリ クラスターと TiCDC をデプロイするには、次のデプロイ テンプレートを使用し、必要に応じて構成パラメータを変更します。

    ```yaml
    global:
    user: "tidb"
    ssh_port: 22
    deploy_dir: "/tidb-deploy"
    data_dir: "/tidb-data"
    server_configs: {}
    pd_servers:
    - host: 10.0.1.1
    - host: 10.0.1.2
    - host: 10.0.1.3
    tidb_servers:
    - host: 10.0.1.4
    - host: 10.0.1.5
    tikv_servers:
    - host: 10.0.1.6
    - host: 10.0.1.7
    - host: 10.0.1.8
    monitoring_servers:
    - host: 10.0.1.9
    grafana_servers:
    - host: 10.0.1.9
    alertmanager_servers:
    - host: 10.0.1.9
    cdc_servers:
    - host: 10.1.1.9
        gc-ttl: 86400
        data_dir: "/cdc-data"
        ticdc_cluster_id: "DR_TiCDC"
    - host: 10.1.1.10
        gc-ttl: 86400
        data_dir: "/cdc-data"
        ticdc_cluster_id: "DR_TiCDC"
    ```

### プライマリ クラスタからセカンダリ クラスタにデータをレプリケートする {#replicate-data-from-the-primary-cluster-to-the-secondary-cluster}

TiDB プライマリ クラスターとセカンダリ クラスターをセットアップした後、まずプライマリ クラスターからセカンダリ クラスターにデータを移行し、次にレプリケーション タスクを作成して、リアルタイムの変更データをプライマリ クラスターからセカンダリ クラスターにレプリケートします。

#### 外部storageを選択する {#select-an-external-storage}

外部storageは、データの移行やリアルタイムの変更データのレプリケーション時に使用されます。 Amazon S3 をお勧めします。 TiDB クラスターが自社構築のデータセンターにデプロイされている場合は、次の方法をお勧めします。

-   バックアップstorageシステムとして[MinIO](https://docs.min.io/docs/minio-quickstart-guide.html)を構築し、S3 プロトコルを使用してデータを MinIO にバックアップします。
-   ネットワーク ファイル システム (NAS など) ディスクを br コマンド ライン ツール、TiKV、および TiCDC インスタンスにマウントし、POSIX ファイル システム インターフェイスを使用してバックアップ データを対応する NFS ディレクトリに書き込みます。

次の例では、storageシステムとして MinIO を使用していますが、これは参照のみを目的としています。 MinIO をリージョン 1 またはリージョン 2 にデプロイするには、別のサーバーを準備する必要があることに注意してください。

```shell
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
# Configure access-key and access-secret-id to access MinIO
export HOST_IP='10.0.1.10' # Replace it with the IP address of MinIO
export MINIO_ROOT_USER='minio'
export MINIO_ROOT_PASSWORD='miniostorage'
# Create the redo and backup directories. `backup` and `redo` are bucket names.
mkdir -p data/redo
mkdir -p data/backup
# Start minio at port 6060
nohup ./minio server ./data --address :6060 &
```

前述のコマンドは、1 つのノードで MinIOサーバーを起動し、Amazon S3 サービスをシミュレートします。コマンドのパラメータは次のように構成されます。

-   `endpoint` ： `http://10.0.1.10:6060/`
-   `access-key` ： `minio`
-   `secret-access-key` ： `miniostorage`
-   `bucket` `backup` `redo`

リンクは次のとおりです。

    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true

#### データの移行 {#migrate-data}

プライマリ クラスタからセカンダリ クラスタにデータを移行するには、 [バックアップと復元機能](/br/backup-and-restore-overview.md)を使用します。

1.  GC を無効にします。新しく書き込まれたデータが増分移行中に削除されないようにするには、バックアップ前にアップストリーム クラスターの GC を無効にする必要があります。これにより、履歴データは削除されません。

    次のステートメントを実行して GC を無効にします。

    ```sql
    SET GLOBAL tidb_gc_enable=FALSE;
    ```

    変更が有効であることを確認するには、値`tidb_gc_enable`をクエリします。

    ```sql
    SELECT @@global.tidb_gc_enable;
    ```

    値が`0`の場合、GC が無効になっていることを意味します。

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

    > **注記：**
    >
    > 本番クラスターでは、GC を無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響を与える可能性があります。パフォーマンスの低下を避けるために、オフピーク時間にデータをバックアップし、 `RATE_LIMIT`を適切な値に設定することをお勧めします。

2.  バックアップデータ。アップストリーム クラスターで`BACKUP`ステートメントを実行して、データをバックアップします。

    ```sql
    BACKUP DATABASE * TO '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true`';
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | s3://backup          | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`ステートメントの実行後、TiDB はバックアップ データに関するメタデータを返します。 `BackupTS`バックアップ前にデータが生成されるため注意してください。このドキュメントでは、**増分移行の開始**として`BackupTS`が使用されます。

3.  データを復元します。セカンダリ クラスターで`RESTORE`ステートメントを実行してデータを復元します。

    ```sql
    RESTORE DATABASE * FROM '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true`';
    ```

        +----------------------+----------+----------+---------------------+---------------------+
        | Destination          | Size     | BackupTS | Queue Time          | Execution Time      |
        +----------------------+----------+----------+---------------------+---------------------+
        | s3://backup          | 10315858 | 0        | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
        +----------------------+----------+----------+---------------------+---------------------+
        1 row in set (41.85 sec)

#### 増分データをレプリケートする {#replicate-incremental-data}

前のセクションで説明したようにデータを移行した後、 **BackupTS**から開始して、プライマリ クラスターからセカンダリ クラスターに増分データをレプリケートできます。

1.  チェンジフィードを作成します。

    チェンジフィード構成ファイルを作成します`changefeed.toml` 。

    ```toml
    [consistent]
    # eventual consistency: redo logs are used to ensure eventual consistency in disaster scenarios.
    level = "eventual"
    # The size of a single redo log, in MiB. The default value is 64, and the recommended value is less than 128.
    max-log-size = 64
    # The interval for refreshing or uploading redo logs to Amazon S3, in milliseconds. The default value is 1000, and the recommended value range is 500-2000.
    flush-interval = 2000
    # The path where redo logs are saved.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true"
    ```

    プライマリ クラスターで次のコマンドを実行して、プライマリ クラスターからセカンダリ クラスターへの変更フィードを作成します。

    ```shell
    tiup cdc cli changefeed create --server=http://10.1.1.9:8300 \
    --sink-uri="mysql://{username}:{password}@10.1.1.4:4000" \
    --changefeed-id="dr-primary-to-secondary" --start-ts="431434047157698561"
    ```

    変更フィード構成の詳細については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)を参照してください。

2.  チェンジフィードタスクが適切に実行されるかどうかを確認するには、 `changefeed query`コマンドを実行します。クエリ結果には、タスク情報とタスクの状態が含まれます。 `--simple`または`-s`引数を指定すると、基本的なレプリケーション状態とチェックポイント情報のみを表示できます。この引数を指定しない場合、出力には詳細なタスク構成、レプリケーション状態、およびレプリケーション テーブル情報が含まれます。

    ```shell
    tiup cdc cli changefeed query -s --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"
    ```

    ```shell
    {
    "state": "normal",
    "tso": 431434047157998561,  # The TSO to which the changefeed has been replicated
    "checkpoint": "2020-08-27 10:12:19.579", # The physical time corresponding to the TSO
    "error": null
    }
    ```

3.  GCを有効にします。

    TiCDC は、履歴データがレプリケートされる前にガベージ コレクションが行われないことを保証します。したがって、プライマリ クラスターからセカンダリ クラスターへの変更フィードを作成した後、次のステートメントを実行して GC を再度有効にすることができます。

    次のステートメントを実行して GC を有効にします。

    ```sql
    SET GLOBAL tidb_gc_enable=TRUE;
    ```

    変更が有効であることを確認するには、値`tidb_gc_enable`をクエリします。

    ```sql
    SELECT @@global.tidb_gc_enable;
    ```

    値が`1`の場合、GC が有効であることを意味します。

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

### プライマリクラスタとセカンダリクラスタを監視する {#monitor-the-primary-and-secondary-clusters}

現在、TiDB では DR ダッシュボードを利用できません。次のダッシュボードを使用して TiDB プライマリ クラスターとセカンダリ クラスターのステータスを確認し、DR スイッチオーバーを実行するかどうかを決定できます。

-   [TiDB の主要な指標](/grafana-overview-dashboard.md)
-   [チェンジフィードメトリクス](/ticdc/monitor-ticdc.md#changefeed)

### DRスイッチオーバーを実行する {#perform-dr-switchover}

このセクションでは、計画的な DR スイッチオーバー、災害時の DR スイッチオーバーを実行する方法、およびセカンダリ クラスターを再構築する手順について説明します。

#### 計画されたプライマリおよびセカンダリのスイッチオーバー {#planned-primary-and-secondary-switchover}

重要なビジネス システムに対して定期的に DR 訓練を実施し、その信頼性をテストすることが重要です。 DR ドリルの推奨手順は次のとおりです。シミュレートされたビジネス書き込みとデータベースにアクセスするためのプロキシ サービスの使用は考慮されていないため、手順は実際のアプリケーション シナリオと異なる場合があることに注意してください。必要に応じて構成を変更できます。

1.  プライマリ クラスターでのビジネス書き込みを停止します。

2.  書き込みがなくなったら、TiDB クラスターの最新の TSO ( `Position` ) をクエリします。

    ```sql
    mysql> show master status;
    +-------------+--------------------+--------------+------------------+-------------------+
    | File        | Position           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +-------------+--------------------+--------------+------------------+-------------------+
    | tidb-binlog | 438223974697009153 |              |                  |                   |
    +-------------+--------------------+--------------+------------------+-------------------+
    1 row in set (0.33 sec)
    ```

3.  条件`TSO >= Position`を満たすまで変更フィード`dr-primary-to-secondary`をポーリングします。

    ```shell
    tiup cdc cli changefeed query -s --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"

    {
        "state": "normal",
        "tso": 438224029039198209,  # The TSO to which the changefeed has been replicated
        "checkpoint": "2022-12-22 14:53:25.307", # The physical time corresponding to the TSO
        "error": null
    }
    ```

4.  チェンジフィードを停止します`dr-primary-to-secondary` 。変更フィードを削除すると、変更フィードを一時停止できます。

    ```shell
    tiup cdc cli changefeed remove --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"
    ```

5.  `start-ts`パラメータを指定せずに、チェンジフィード`dr-secondary-to-primary`を作成します。チェンジフィードは現在時刻からデータのレプリケーションを開始します。

6.  ビジネスアプリケーションのデータベースアクセス構成を変更します。ビジネス アプリケーションを再起動して、セカンダリ クラスターにアクセスできるようにします。

7.  業務アプリケーションが正常に動作しているか確認してください。

前述の手順を繰り返すことで、以前のプライマリ クラスタ構成とセカンダリ クラスタ構成を復元できます。

#### 災害時の1次系と2次系の切り替え {#primary-and-secondary-switchover-upon-disasters}

プライマリ クラスタが配置されているリージョンで停電などの災害が発生すると、プライマリ クラスタとセカンダリ クラスタ間のレプリケーションが突然中断される可能性があります。その結果、セカンダリ クラスタのデータはプライマリ クラスタと不整合になります。

1.  セカンダリ クラスタをトランザクション整合性のある状態に復元します。具体的には、リージョン 2 の任意の TiCDC ノードで次のコマンドを実行して、REDO ログをセカンダリ クラスターに適用します。

    ```shell
    tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://{username}:{password}@10.1.1.4:4000"
    ```

    このコマンドのパラメータの説明は次のとおりです。

    -   `--storage` : Amazon S3 内の REDO ログが保存されるパス
    -   `--tmp-dir` : Amazon S3 から REDO ログをダウンロードするためのキャッシュ ディレクトリ
    -   `--sink-uri` : セカンダリクラスタのアドレス

2.  ビジネスアプリケーションのデータベースアクセス構成を変更します。ビジネス アプリケーションを再起動して、セカンダリ クラスターにアクセスできるようにします。

3.  業務アプリケーションが正常に動作しているか確認してください。

#### プライマリ クラスタとセカンダリ クラスタを再構築する {#rebuild-the-primary-and-secondary-clusters}

プライマリ クラスターで発生した災害が解決された後、またはプライマリ クラスターが一時的に回復できなかった後は、セカンダリ クラスターのみがプライマリ クラスターとして機能するため、TiDB クラスターは脆弱になります。システムの信頼性を維持するには、DR クラスターを再構築する必要があります。

TiDB プライマリ クラスタとセカンダリ クラスタを再構築するには、新しいクラスタをデプロイして新しい DR システムを形成します。詳細については、次のドキュメントを参照してください。

-   [プライマリ クラスタとセカンダリ クラスタをセットアップする](#set-up-primary-and-secondary-clusters-based-on-ticdc)
-   [プライマリ クラスタからセカンダリ クラスタにデータをレプリケートする](#replicate-data-from-the-primary-cluster-to-the-secondary-cluster)
-   前述の手順が完了したら、新しいプライマリ クラスターを作成するには、 [プライマリとセカンダリの切り替え](#planned-primary-and-secondary-switchover)を参照してください。

> **注記：**
>
> プライマリ クラスタとセカンダリ クラスタ間のデータの不整合を解決できる場合は、新しいクラスタを展開する代わりに、修復したクラスタを使用して DR システムを再構築できます。

### セカンダリ クラスター上のビジネス データをクエリする {#query-business-data-on-the-secondary-cluster}

プライマリ - セカンダリ DR シナリオでは、待機時間を気にしないクエリを実行するために、セカンダリ クラスターが読み取り専用クラスターとして使用されるのが一般的です。 TiDB は、プライマリ - セカンダリ DR ソリューションによってこの機能も提供します。

変更フィードを作成するときは、構成ファイルで同期ポイント機能を有効にします。次に、変更フィードは、セカンダリ クラスターで`SET GLOBAL tidb_external_ts = @@tidb_current_ts`実行することによって、セカンダリ クラスターにレプリケートされた一貫性のあるスナップショット ポイントを定期的に ( `sync-point-interval`で) 設定します。

セカンダリ クラスターからデータをクエリするには、ビジネス アプリケーションで`SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;`を構成します。これにより、プライマリ クラスターとトランザクション的に一貫性のあるデータを取得できます。

```toml
# Starting from v6.4.0, only the changefeed with the SYSTEM_VARIABLES_ADMIN or SUPER privilege can use the TiCDC Syncpoint feature.
enable-sync-point = true

# Specifies the interval at which Syncpoint aligns the primary and secondary snapshots. It also indicates the maximum latency at which you can read the complete transaction, for example, read the transaction data generated on the primary cluster two minutes ago from the secondary cluster.
# The format is in h m s. For example, "1h30m30s". The default value is "10m" and the minimum value is "30s".
sync-point-interval = "10m"

# Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up.
# The format is in h m s. For example, "24h30m30s". The default value is "24h".
sync-point-retention = "1h"

[consistent]
# eventual consistency: redo logs are used to ensure eventual consistency in disaster scenarios.
level = "eventual"
# The size of a single redo log, in MiB. The default value is 64, and the recommended value is less than 128.
max-log-size = 64
# Interval for refreshing or uploading redo logs to Amazon S3, in milliseconds. The default value is 1000, and the recommended value range is 500-2000.
flush-interval = 2000
# The path where redo logs are saved.
storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true"
```

> **注記：**
>
> プライマリ - セカンダリ DRアーキテクチャでは、セカンダリ クラスタは 1 つの変更フィードからのデータのみをレプリケートできます。そうしないと、セカンダリ クラスターのデータ トランザクションの整合性が保証されません。

### プライマリクラスタとセカンダリクラスタの間で双方向レプリケーションを実行します。 {#perform-bidirectional-replication-between-the-primary-and-secondary-clusters}

この DR シナリオでは、2 つのリージョンの TiDB クラスターが互いの災害復旧クラスターとして機能できます。ビジネス トラフィックはリージョン構成に基づいて対応する TiDB クラスターに書き込まれ、2 つの TiDB クラスターは互いのデータをバックアップします。

![TiCDC bidirectional replication](/media/dr/bdr-ticdc.png)

双方向レプリケーション機能を使用すると、2 つのリージョンにある TiDB クラスターが相互にデータをレプリケートできます。この DR ソリューションは、データのセキュリティと信頼性を保証し、データベースの書き込みパフォーマンスも保証します。計画的な DR スイッチオーバーでは、新しい変更フィードを開始する前に実行中の変更フィードを停止する必要がないため、運用とメンテナンスが簡素化されます。

双方向 DR クラスターを構築するには、 [TiCDC 双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)を参照してください。

## トラブルシューティング {#troubleshooting}

前の手順で問題が発生した場合は、まず[TiDB よくある質問](/faq/faq-overview.md)で問題の解決策を見つけることができます。問題が解決しない場合は、 [バグを報告](/support.md)を実行できます。

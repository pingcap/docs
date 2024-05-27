---
title: DR Solution Based on Primary and Secondary Clusters
summary: TiCDC に基づいてプライマリ/セカンダリ災害復旧を実装する方法を学びます。
---

# プライマリおよびセカンダリ クラスタに基づく DR ソリューション {#dr-solution-based-on-primary-and-secondary-clusters}

プライマリ データベースとセカンダリ データベースに基づく災害復旧 (DR) は、一般的なソリューションです。このソリューションでは、DR システムにプライマリ クラスターとセカンダリ クラスターがあります。プライマリ クラスターはユーザー要求を処理し、セカンダリ クラスターはプライマリ クラスターからデータをバックアップします。プライマリ クラスターに障害が発生すると、セカンダリ クラスターがサービスを引き継ぎ、バックアップ データを使用してサービスの提供を継続します。これにより、障害による中断がなく、ビジネス システムが正常に稼働し続けることが保証されます。

プライマリ/セカンダリ DR ソリューションには、次の利点があります。

-   高可用性: プライマリ/セカンダリアーキテクチャによりシステムの可用性が向上し、あらゆる障害からの迅速な回復が保証されます。
-   高速切り替え: プライマリ クラスターに障害が発生した場合、システムはセカンダリ クラスターにすばやく切り替えて、サービスの提供を継続できます。
-   データの一貫性: セカンダリ クラスターは、プライマリ クラスターのデータをほぼリアルタイムでバックアップします。これにより、障害によりシステムがセカンダリ クラスターに切り替わった場合でも、データは基本的に最新の状態になります。

このドキュメントには次の内容が含まれています。

-   プライマリ クラスターとセカンダリ クラスターをセットアップします。
-   プライマリ クラスターからセカンダリ クラスターにデータを複製します。
-   クラスターを監視します。
-   DR スイッチオーバーを実行します。

また、このドキュメントでは、セカンダリ クラスターでビジネス データをクエリする方法と、プライマリ クラスターとセカンダリ クラスター間で双方向レプリケーションを実行する方法についても説明します。

## TiCDC に基づいてプライマリ クラスターとセカンダリ クラスターを設定する {#set-up-primary-and-secondary-clusters-based-on-ticdc}

### アーキテクチャ {#architecture}

![TiCDC secondary cluster architecture](/media/dr/dr-ticdc-secondary-cluster.png)

上記のアーキテクチャには、プライマリ クラスターとセカンダリ クラスターの 2 つの TiDB クラスターが含まれています。

-   プライマリ クラスター: リージョン 1 で実行され、3 つのレプリカを持つアクティブ クラスター。このクラスターは読み取りおよび書き込み要求を処理します。
-   セカンダリ クラスター: リージョン 2 で実行され、TiCDC を介してプライマリ クラスターからデータを複製するスタンバイ クラスター。

この DRアーキテクチャはシンプルで使いやすいです。地域的な障害に耐えられるため、DR システムはプライマリ クラスターの書き込みパフォーマンスが低下しないことを保証し、セカンダリ クラスターは遅延の影響を受けない読み取り専用業務を処理できます。このソリューションのリカバリ ポイント目標 (RPO) は数秒で、リカバリ時間目標 (RTO) は数分またはそれ以下です。これは、多くのデータベース ベンダーが重要な本番システム向けに推奨するソリューションです。

> **注記：**
>
> -   [TiKV の「リージョン」](/glossary.md#regionpeerraft-group)データの範囲を意味し、「リージョン」という用語は物理的な場所を意味します。この 2 つの用語は互換性がありません。
> -   セカンダリ クラスターにデータをレプリケートするために複数の変更フィードを実行しないでください。また、セカンダリ クラスターがすでに存在する状態で別のセカンダリ クラスターを実行しないでください。そうしないと、セカンダリ クラスターのデータ トランザクションの整合性が保証されません。

### プライマリクラスタとセカンダリクラスタを設定する {#set-up-primary-and-secondary-clusters}

このドキュメントでは、TiDB プライマリ クラスターとセカンダリ クラスターが 2 つの異なるリージョン (リージョン 1 とリージョン 2) にデプロイされています。プライマリ クラスターとセカンダリ クラスターの間には一定のネットワークレイテンシーがあるため、TiCDC はセカンダリ クラスターと一緒にデプロイされています。セカンダリ クラスターと一緒に TiCDC をデプロイすると、ネットワークレイテンシーの影響を回避でき、最適なレプリケーション パフォーマンスを実現できます。このドキュメントで提供される例のデプロイ トポロジは次のとおりです (1 つのコンポーネントノードが 1 つのサーバーにデプロイされています)。

| リージョン  | ホスト                        | クラスタ | 成分                           |
| ------ | -------------------------- | ---- | ---------------------------- |
| リージョン1 | 10.0.1.9                   | 主要な  | モニター、Grafana、またはAlterManager |
| リージョン2 | 10.0.1.11                  | 二次   | モニター、Grafana、またはAlterManager |
| リージョン1 | 10.0.1.1/10.0.1.2/10.0.1.3 | 主要な  | PD                           |
| リージョン2 | 10.1.1.1/10.1.1.2/10.1.1.3 | 二次   | PD                           |
| リージョン2 | 10.1.1.9/10.1.1.10         | 主要な  | ティCDC                        |
| リージョン1 | 10.0.1.4/10.0.1.5          | 主要な  | ティビ                          |
| リージョン2 | 10.1.1.4/10.1.1.5          | 二次   | ティビ                          |
| リージョン1 | 10.0.1.6/10.0.1.7/10.0.1.8 | 主要な  | ティクヴ                         |
| リージョン2 | 10.1.1.6/10.1.1.7/10.1.1.8 | 二次   | ティクヴ                         |

サーバー構成については、次のドキュメントを参照してください。

-   [TiDB のソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)
-   [TiCDC のソフトウェアとハ​​ードウェアの推奨事項](/ticdc/deploy-ticdc.md#software-and-hardware-recommendations)

TiDB プライマリ クラスターとセカンダリ クラスターをデプロイする方法の詳細については、 [TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

TiCDC をデプロイする場合、セカンダリ クラスターと TiCDC を一緒にデプロイして管理する必要があり、それらの間のネットワークが接続されている必要があることに注意してください。

-   既存のプライマリ クラスターに TiCDC をデプロイするには、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup)参照してください。
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

### プライマリクラスタからセカンダリクラスタにデータを複製する {#replicate-data-from-the-primary-cluster-to-the-secondary-cluster}

TiDB プライマリ クラスターとセカンダリ クラスターを設定したら、まずプライマリ クラスターからセカンダリ クラスターにデータを移行し、次にレプリケーション タスクを作成して、リアルタイムの変更データをプライマリ クラスターからセカンダリ クラスターに複製します。

#### 外部storageを選択 {#select-an-external-storage}

データの移行やリアルタイムの変更データの複製には外部storageが使用されます。Amazon S3 が推奨されます。TiDB クラスターを自社構築のデータセンターにデプロイする場合は、次の方法が推奨されます。

-   バックアップstorageシステムとして[ミニオ](https://docs.min.io/docs/minio-quickstart-guide.html)を構築し、S3 プロトコルを使用してデータを MinIO にバックアップします。
-   ネットワーク ファイル システム (NAS などの NFS) ディスクを br コマンドライン ツール、TiKV、および TiCDC インスタンスにマウントし、POSIX ファイル システム インターフェイスを使用して、対応する NFS ディレクトリにバックアップ データを書き込みます。

以下の例では、storageシステムとして MinIO を使用していますが、参考用です。リージョン 1 またはリージョン 2 に MinIO を展開するには、別のサーバーを用意する必要があることに注意してください。

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

上記のコマンドは、1 つのノードで MinIOサーバーを起動し、Amazon S3 サービスをシミュレートします。コマンドのパラメータは次のように構成されます。

-   `endpoint` : `http://10.0.1.10:6060/`
-   `access-key` : `minio`
-   `secret-access-key` : `miniostorage`
-   `bucket` : `redo` / `backup`

リンクは次のとおりです。

    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true

#### データの移行 {#migrate-data}

[バックアップと復元機能](/br/backup-and-restore-overview.md)を使用して、プライマリ クラスターからセカンダリ クラスターにデータを移行します。

1.  GC を無効にします。増分移行中に新しく書き込まれたデータが削除されないようにするには、バックアップの前にアップストリーム クラスターの GC を無効にする必要があります。この方法では、履歴データは削除されません。

    GC を無効にするには、次のステートメントを実行します。

    ```sql
    SET GLOBAL tidb_gc_enable=FALSE;
    ```

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    SELECT @@global.tidb_gc_enable;
    ```

    値が`0`の場合、GC は無効であることを意味します。

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

    > **注記：**
    >
    > 本番クラスターでは、GC を無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響する可能性があります。パフォーマンスの低下を避けるために、オフピーク時にデータをバックアップし、 `RATE_LIMIT`適切な値に設定することをお勧めします。

2.  データをバックアップします。アップストリーム クラスターで`BACKUP`ステートメントを実行してデータをバックアップします。

    ```sql
    BACKUP DATABASE * TO '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true`';
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | s3://backup          | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`文が実行されると、TiDB はバックアップ データに関するメタデータを返します。3 `BackupTS`バックアップされる前に生成されたデータなので注意してください。このドキュメントでは、 `BackupTS`**増分移行の開始**として使用されます。

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

#### 増分データを複製する {#replicate-incremental-data}

前のセクションで説明したようにデータを移行した後、 **BackupTS**から開始して、プライマリ クラスターからセカンダリ クラスターに増分データを複製できます。

1.  変更フィードを作成します。

    changefeed 構成ファイル`changefeed.toml`を作成します。

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

    changefeed 構成の詳細については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)参照してください。

2.  changefeed タスクが適切に実行されているかどうか`-s`確認するには、 `changefeed query`コマンドを実行します。クエリ結果には、タスク情報とタスク状態が含まれます。3 または`--simple`引数を指定して、基本的なレプリケーション状態とチェックポイント情報のみを表示できます。この引数を指定しない場合は、詳細なタスク構成、レプリケーション状態、およびレプリケーション テーブル情報が出力に含まれます。

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

3.  GC を有効にします。

    TiCDC は、履歴データがレプリケートされる前にガベージ コレクションされないようにします。したがって、プライマリ クラスターからセカンダリ クラスターへの変更フィードを作成した後、次のステートメントを実行して GC を再度有効にすることができます。

    GC を有効にするには、次のステートメントを実行します。

    ```sql
    SET GLOBAL tidb_gc_enable=TRUE;
    ```

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    SELECT @@global.tidb_gc_enable;
    ```

    値が`1`の場合、GC が有効になっていることを意味します。

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

### プライマリクラスタとセカンダリクラスタを監視する {#monitor-the-primary-and-secondary-clusters}

現在、TiDB では DR ダッシュボードは利用できません。次のダッシュボードを使用して TiDB プライマリ クラスターとセカンダリ クラスターのステータスを確認し、DR スイッチオーバーを実行するかどうかを決定できます。

-   [TiDB 主要指標](/grafana-overview-dashboard.md)
-   [チェンジフィードメトリクス](/ticdc/monitor-ticdc.md#changefeed)

### DRスイッチオーバーを実行する {#perform-dr-switchover}

このセクションでは、計画された DR スイッチオーバー、災害発生時の DR スイッチオーバーを実行する方法、およびセカンダリ クラスターを再構築する手順について説明します。

#### 計画的なプライマリおよびセカンダリの切り替え {#planned-primary-and-secondary-switchover}

重要なビジネス システムの信頼性をテストするために、定期的に DR ドリルを実施することが重要です。以下は、DR ドリルの推奨手順です。シミュレートされたビジネス書き込みや、データベースにアクセスするためのプロキシ サービスの使用は考慮されていないため、手順は実際のアプリケーション シナリオと異なる場合があります。必要に応じて構成を変更できます。

1.  プライマリ クラスターでのビジネス書き込みを停止します。

2.  書き込みがなくなったら、TiDBクラスタの最新のTSO（ `Position` ）をクエリします。

    ```sql
    mysql> show master status;
    +-------------+--------------------+--------------+------------------+-------------------+
    | File        | Position           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +-------------+--------------------+--------------+------------------+-------------------+
    | tidb-binlog | 438223974697009153 |              |                  |                   |
    +-------------+--------------------+--------------+------------------+-------------------+
    1 row in set (0.33 sec)
    ```

3.  条件`TSO >= Position`を満たすまで、変更フィード`dr-primary-to-secondary`をポーリングします。

    ```shell
    tiup cdc cli changefeed query -s --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"

    {
        "state": "normal",
        "tso": 438224029039198209,  # The TSO to which the changefeed has been replicated
        "checkpoint": "2022-12-22 14:53:25.307", # The physical time corresponding to the TSO
        "error": null
    }
    ```

4.  変更フィードを停止します`dr-primary-to-secondary` 。変更フィードを削除することで一時停止できます。

    ```shell
    tiup cdc cli changefeed remove --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"
    ```

5.  `start-ts`パラメータを指定せずに changefeed `dr-secondary-to-primary`を作成します。changefeed は現在の時刻からデータの複製を開始します。

6.  ビジネス アプリケーションのデータベース アクセス構成を変更します。ビジネス アプリケーションを再起動して、セカンダリ クラスターにアクセスできるようにします。

7.  ビジネスアプリケーションが正常に実行されているかどうかを確認します。

上記の手順を繰り返すことで、以前のプライマリ クラスターとセカンダリ クラスターの構成を復元できます。

#### 災害時のプライマリとセカンダリの切り替え {#primary-and-secondary-switchover-upon-disasters}

プライマリ クラスターが配置されている地域で停電などの災害が発生すると、プライマリ クラスターとセカンダリ クラスター間のレプリケーションが突然中断される可能性があります。その結果、セカンダリ クラスターのデータがプライマリ クラスターと一致しなくなります。

1.  セカンダリ クラスターをトランザクション整合性のある状態に復元します。具体的には、リージョン 2 の任意の TiCDC ノードで次のコマンドを実行して、REDO ログをセカンダリ クラスターに適用します。

    ```shell
    tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://{username}:{password}@10.1.1.4:4000"
    ```

    このコマンドのパラメータの説明は次のとおりです。

    -   `--storage` : Amazon S3 で REDO ログが保存されるパス
    -   `--tmp-dir` : Amazon S3 から REDO ログをダウンロードするためのキャッシュ ディレクトリ
    -   `--sink-uri` : セカンダリクラスタのアドレス

2.  ビジネス アプリケーションのデータベース アクセス構成を変更します。ビジネス アプリケーションを再起動して、セカンダリ クラスターにアクセスできるようにします。

3.  ビジネスアプリケーションが正常に実行されているかどうかを確認します。

#### プライマリクラスタとセカンダリクラスタを再構築する {#rebuild-the-primary-and-secondary-clusters}

プライマリ クラスターで発生した災害が解決された後、またはプライマリ クラスターが一時的に復旧できない場合、セカンダリ クラスターのみがプライマリ クラスターとして稼働しているため、TiDB クラスターは脆弱です。システムの信頼性を維持するには、DR クラスターを再構築する必要があります。

TiDB プライマリ クラスターとセカンダリ クラスターを再構築するには、新しいクラスターをデプロイして新しい DR システムを形成します。詳細については、次のドキュメントを参照してください。

-   [プライマリクラスタとセカンダリクラスタを設定する](#set-up-primary-and-secondary-clusters-based-on-ticdc)
-   [プライマリクラスタからセカンダリクラスタにデータを複製する](#replicate-data-from-the-primary-cluster-to-the-secondary-cluster)
-   上記の手順が完了したら、新しいプライマリ クラスターを作成するには、 [プライマリとセカンダリの切り替え](#planned-primary-and-secondary-switchover)参照してください。

> **注記：**
>
> プライマリ クラスターとセカンダリ クラスター間のデータの不整合を解決できる場合は、新しいクラスターを展開する代わりに、修復されたクラスターを使用して DR システムを再構築できます。

### セカンダリ クラスターでビジネス データをクエリする {#query-business-data-on-the-secondary-cluster}

プライマリ/セカンダリ DR シナリオでは、セカンダリ クラスターを読み取り専用クラスターとして使用し、レイテンシの影響を受けないクエリを実行するのが一般的です。TiDB も、プライマリ/セカンダリ DR ソリューションによってこの機能を提供します。

changefeed を作成するときは、構成ファイルで Syncpoint 機能を有効にします。その後、changefeed は定期的に ( `sync-point-interval`で) セカンダリ クラスターで`SET GLOBAL tidb_external_ts = @@tidb_current_ts`を実行して、セカンダリ クラスターに複製された一貫性のあるスナップショット ポイントを設定します。

セカンダリ クラスターからデータをクエリするには、ビジネス アプリケーションで`SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;`構成します。これにより、プライマリ クラスターとトランザクション的に一貫性のあるデータを取得できます。

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
> プライマリ/セカンダリ DRアーキテクチャでは、セカンダリ クラスターは 1 つの変更フィードからのみデータを複製できます。そうしないと、セカンダリ クラスターのデータ トランザクションの整合性が保証されません。

### プライマリクラスタとセカンダリクラスタ間の双方向レプリケーションを実行する {#perform-bidirectional-replication-between-the-primary-and-secondary-clusters}

この DR シナリオでは、2 つのリージョンの TiDB クラスターが互いの災害復旧クラスターとして機能できます。ビジネス トラフィックはリージョン構成に基づいて対応する TiDB クラスターに書き込まれ、2 つの TiDB クラスターは互いのデータをバックアップします。

![TiCDC bidirectional replication](/media/dr/bdr-ticdc.png)

双方向レプリケーション機能により、2 つのリージョンの TiDB クラスターは互いのデータを複製できます。この DR ソリューションは、データのセキュリティと信頼性を保証し、データベースの書き込みパフォーマンスも確保します。計画された DR スイッチオーバーでは、新しい変更フィードを開始する前に実行中の変更フィードを停止する必要がないため、操作とメンテナンスが簡素化されます。

双方向 DR クラスターを構築するには、 [TiCDC 双方向レプリケーション](/ticdc/ticdc-bidirectional-replication.md)参照してください。

## トラブルシューティング {#troubleshooting}

前の手順で問題が発生した場合は、まず[TiDB に関するよくある質問](/faq/faq-overview.md)で問題の解決策を見つけてください。問題が解決しない場合は[バグを報告](/support.md)実行してください。

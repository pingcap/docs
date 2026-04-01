---
title: DR Solution Based on Primary and Secondary Clusters
summary: TiCDCに基づいたプライマリ・セカンダリディザスタリカバリの実装方法を学びましょう。
---

# プライマリクラスタとセカンダリクラスタに基づく災害復旧ソリューション {#dr-solution-based-on-primary-and-secondary-clusters}

プライマリデータベースとセカンダリデータベースに基づく災害リカバリ（DR）は、一般的なソリューションです。このソリューションでは、DRシステムはプライマリクラスタとセカンダリクラスタで構成されます。プライマリクラスタはユーザーからのリクエストを処理し、セカンダリクラスタはプライマリクラスタからデータをバックアップします。プライマリクラスタに障害が発生した場合、セカンダリクラスタがサービスを引き継ぎ、バックアップデータを使用してサービスの提供を継続します。これにより、障害による中断なく、ビジネスシステムが正常に稼働し続けることが保証されます。

プライマリ・セカンダリ型災害復旧ソリューションには、以下の利点があります。

-   高可用性：プライマリ・セカンダリアーキテクチャによりシステムの可用性が向上し、あらゆる障害からの迅速なリカバリが保証されます。
-   高速切り替え：プライマリクラスタに障害が発生した場合、システムはセカンダリクラスタに迅速に切り替えてサービスの提供を継続できます。
-   データの一貫性：セカンダリクラスタは、プライマリクラスタのデータをほぼリアルタイムでバックアップします。これにより、システムが障害発生時にセカンダリクラスタに切り替わった場合でも、データは基本的に最新の状態に保たれます。

この文書には以下の内容が含まれています。

-   プライマリクラスタとセカンダリクラスタを設定します。
-   プライマリクラスタからセカンダリクラスタへデータを複製します。
-   クラスターを監視する。
-   DR（災害復旧）システムの切り替えを実行します。

一方、このドキュメントでは、セカンダリクラスタ上のビジネスデータを照会する方法、およびプライマリクラスタとセカンダリクラスタ間で双方向レプリケーションを実行する方法についても説明します。

## TiCDCに基づいてプライマリおよびセカンダリクラスタをセットアップする {#set-up-primary-and-secondary-clusters-based-on-ticdc}

### アーキテクチャ {#architecture}

![TiCDC secondary cluster architecture](/media/dr/dr-ticdc-secondary-cluster.png)

前述のアーキテクチャは、プライマリクラスタとセカンダリクラスタという2つのTiDBクラスタで構成されています。

-   プライマリークラスター：リージョン1で稼働するアクティブなクラスターで、3つのレプリカを持ちます。このクラスターは読み取りおよび書き込みリクエストを処理します。
-   セカンダリークラスター：リージョン2で稼働し、TiCDCを介してプライマリークラスターからデータを複製するスタンバイクラスター。

このDRアーキテクチャはシンプルで使いやすい。リージョン障害に対応できるため、プライマリクラスタの書き込みパフォーマンスが低下しないことが保証され、セカンダリクラスタはレイテンシに影響されない読み取り専用処理を処理できる。このソリューションのリカバリポイント目標（RPO）は秒単位、リカバリ時間目標（RTO）は数分、あるいはそれ以下となる。多くのデータベースベンダーが重要な本番システム向けに推奨しているソリューションである。

> **注記：**
>
> -   [TiKVの「リージョン」](/glossary.md#regionpeerraft-group)はデータの範囲を意味し、「領域」という用語は物理的な場所を意味します。この2つの用語は互換性がありません。
> -   セカンダリクラスタへのデータ複製のために複数のチェンジフィードを実行したり、既にセカンダリクラスタが存在する状態で別のセカンダリクラスタを実行したりしないでください。そうしないと、セカンダリクラスタのデータトランザクションの整合性が保証されません。

### プライマリクラスターとセカンダリクラスターを設定する {#set-up-primary-and-secondary-clusters}

このドキュメントでは、TiDBのプライマリクラスタとセカンダリクラスタは2つの異なるリージョン（リージョン1とリージョン2）にデプロイされています。プライマリクラスタとセカンダリクラスタの間には一定のネットワークレイテンシーがあるため、TiCDCはセカンダリクラスタと共にデプロイされます。TiCDCをセカンダリクラスタと共にデプロイすることで、ネットワークレイテンシーの影響を回避し、最適なレプリケーションパフォーマンスを実現できます。このドキュメントで提供する例のデプロイトポロジーは以下のとおりです（1つのコンポーネントノードが1つのサーバーにデプロイされます）。

| リージョン  | ホスト                        | クラスタ | 成分                              |
| ------ | -------------------------- | ---- | ------------------------------- |
| リージョン1 | 10.0.1.9                   | 主要な  | Monitor、Grafana、またはAlterManager |
| リージョン2 | 10.0.1.11                  | 二次   | Monitor、Grafana、またはAlterManager |
| リージョン1 | 10.0.1.1/10.0.1.2/10.0.1.3 | 主要な  | PD                              |
| リージョン2 | 10.1.1.1/10.1.1.2/10.1.1.3 | 二次   | PD                              |
| リージョン2 | 10.1.1.9/10.1.1.10         | 主要な  | TiCDC                           |
| リージョン1 | 10.0.1.4/10.0.1.5          | 主要な  | TiDB                            |
| リージョン2 | 10.1.1.4/10.1.1.5          | 二次   | TiDB                            |
| リージョン1 | 10.0.1.6/10.0.1.7/10.0.1.8 | 主要な  | ティクヴ                            |
| リージョン2 | 10.1.1.6/10.1.1.7/10.1.1.8 | 二次   | ティクヴ                            |

サーバーの設定については、以下のドキュメントを参照してください。

-   [TiDB向けのソフトウェアおよびハードウェアに関する推奨事項](/hardware-and-software-requirements.md)
-   [TiCDC向けのソフトウェアおよびハードウェアに関する推奨事項](/ticdc/deploy-ticdc.md#software-and-hardware-recommendations)

TiDBプライマリクラスタとセカンダリクラスタのデプロイ方法の詳細については、 [TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

TiCDCを導入する際は、セカンダリクラスタとTiCDCを一緒に導入・管理する必要があり、両者間のネットワークが接続されている必要があることに注意してください。

-   既存のプライマリ クラスターに TiCDC をデプロイするには、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup)参照してください。
-   新しいプライマリクラスタとTiCDCをデプロイするには、以下のデプロイテンプレートを使用し、必要に応じて構成パラメータを変更してください。

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

### プライマリークラスターからセカンダリークラスターへデータを複製する {#replicate-data-from-the-primary-cluster-to-the-secondary-cluster}

TiDBのプライマリクラスタとセカンダリクラスタを設定した後、まずプライマリクラスタからセカンダリクラスタへデータを移行し、次にプライマリクラスタからセカンダリクラスタへリアルタイムの変更データを複製するためのレプリケーションタスクを作成します。

#### 外部storageを選択してください {#select-an-external-storage}

データの移行やリアルタイム変更データの複製には、外部storageを使用します。Amazon S3 が推奨されます。TiDB クラスターを自社構築のデータセンターにデプロイする場合は、以下の方法が推奨されます。

-   バックアップstorageシステムとして構築[ミニオ](https://docs.min.io/docs/minio-quickstart-guide.html)使用し、S3プロトコルを使用してデータをMinIOにバックアップします。
-   ネットワークファイルシステム（NFS、NASなど）ディスクをbrコマンドラインツール、TiKV、およびTiCDCインスタンスにマウントし、POSIXファイルシステムインターフェースを使用してバックアップデータを対応するNFSディレクトリに書き込みます。

以下の例では、storageシステムとしてMinIOを使用していますが、これはあくまで参考例です。リージョン1またはリージョン2にMinIOをデプロイするには、別途サーバーを用意する必要があることに注意してください。

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

上記のコマンドは、Amazon S3サービスをシミュレートするために、1つのノード上でMinIOサーバーを起動します。コマンドのパラメータは次のように設定されます。

-   `endpoint` : `http://10.0.1.10:6060/`
-   `access-key` : `minio`
-   `secret-access-key` : `miniostorage`
-   `bucket` : `redo` / `backup`

リンクは以下のとおりです。

    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true

#### データの移行 {#migrate-data}

[バックアップと復元機能](/br/backup-and-restore-overview.md)を使用して、プライマリ クラスターからセカンダリ クラスターにデータを移行します。

1.  GCを無効にします。増分移行中に新しく書き込まれたデータが削除されないようにするには、バックアップ前にアップストリームクラスタのGCを無効にする必要があります。こうすることで、履歴データが削除されるのを防ぐことができます。

    GCを無効にするには、次のステートメントを実行してください。

    ```sql
    SET GLOBAL tidb_gc_enable=FALSE;
    ```

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    SELECT @@global.tidb_gc_enable;
    ```

    値が`0`場合は、GCが無効になっていることを意味します。

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

    > **注記：**
    >
    > 本番のクラスタでは、GCを無効にした状態でバックアップを実行すると、クラスタのパフォーマンスに影響が出る可能性があります。パフォーマンスの低下を避けるため、データのバックアップはピーク時以外の時間帯に行い、 `RATE_LIMIT`適切な値に設定することをお勧めします。

2.  データのバックアップ。アップストリームクラスタで以下のステートメント`BACKUP`を実行してデータをバックアップします。

    ```sql
    BACKUP DATABASE * TO '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true`';
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | s3://backup          | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`のステートメントが実行されると、TiDBはバックアップデータに関するメタデータを返します。3 `BackupTS`のステートメントには注意してください。これは、バックアップ前に生成されたデータが含まれているためです。このドキュメントでは、 `BackupTS`**を増分マイグレーションの開始**として使用します。

3.  データの復元。セカンダリクラスタで以下のステートメント`RESTORE`を実行してデータを復元します。

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

前のセクションで説明したようにデータを移行した後、 **BackupTS**からプライマリ クラスターからセカンダリ クラスターに増分データを複製できます。

1.  変更フィードを作成します。

    変更フィード設定ファイル`changefeed.toml`を作成します。

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

    プライマリクラスタで、次のコマンドを実行して、プライマリクラスタからセカンダリクラスタへの変更フィードを作成します。

    ```shell
    tiup cdc cli changefeed create --server=http://10.1.1.9:8300 --sink-uri="mysql://{username}:{password}@10.1.1.4:4000" --changefeed-id="dr-primary-to-secondary" --start-ts="431434047157698561" --config changefeed.toml
    ```

    変更フィードの設定の詳細については、 [TiCDC Changefeedフィード構成](/ticdc/ticdc-changefeed-config.md)参照してください。

2.  変更フィードタスクが正しく実行されているかどうかを確認するには、コマンド`changefeed query`を実行します。クエリ結果には、タスク情報とタスクの状態が含まれます。引数`--simple`または`-s`を指定すると、基本的なレプリケーション状態とチェックポイント情報のみが表示されます。この引数を指定しない場合、出力には詳細なタスク構成、レプリケーション状態、およびレプリケーションテーブル情報が含まれます。

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

3.  GCを有効にする。

    TiCDCは、履歴データがレプリケートされる前にガベージコレクションされないようにします。そのため、プライマリクラスタからセカンダリクラスタに変更フィードを作成した後、次のステートメントを実行してGCを再度有効にすることができます。

    GCを有効にするには、次のステートメントを実行してください。

    ```sql
    SET GLOBAL tidb_gc_enable=TRUE;
    ```

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    SELECT @@global.tidb_gc_enable;
    ```

    値が`1`場合は、GCが有効になっていることを意味します。

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

### プライマリークラスターとセカンダリークラスターを監視する {#monitor-the-primary-and-secondary-clusters}

現在、TiDBにはDRダッシュボードは用意されていません。以下のダッシュボードを使用してTiDBのプライマリクラスタとセカンダリクラスタの状態を確認し、DR切り替えを実行するかどうかを判断してください。

-   [TiDBの主要指標](/grafana-overview-dashboard.md)
-   [変更フィード指標](/ticdc/monitor-ticdc.md#changefeed)

### DR切り替えを実行する {#perform-dr-switchover}

このセクションでは、計画的な災害復旧（DR）切り替え、災害発生時のDR切り替え、およびセカンダリクラスタを再構築する手順について説明します。

#### 計画されたプライマリおよびセカンダリ切り替え {#planned-primary-and-secondary-switchover}

重要な業務システムの信頼性をテストするためには、定期的な災害復旧（DR）訓練を実施することが重要です。以下に、DR訓練の推奨手順を示します。なお、シミュレーションによる業務データの書き込みや、データベースへのアクセスにプロキシサービスを使用することは考慮されていないため、実際のアプリケーションシナリオとは手順が異なる場合があります。必要に応じて設定を変更してください。

1.  プライマリークラスターへの業務書き込みを停止します。

2.  書き込みがなくなったら、TiDBクラスタの最新のTSO（ `Position` ）を照会します。

    ```sql
    BEGIN; SELECT TIDB_CURRENT_TSO(); ROLLBACK;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)

    +--------------------+
    | TIDB_CURRENT_TSO() |
    +--------------------+
    | 452654700157468673 |
    +--------------------+
    1 row in set (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)
    ```

3.  条件`TSO >= Position`満たすまで、changefeed `dr-primary-to-secondary`をポーリングします。

    ```shell
    tiup cdc cli changefeed query -s --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"

    {
        "state": "normal",
        "tso": 438224029039198209,  # The TSO to which the changefeed has been replicated
        "checkpoint": "2022-12-22 14:53:25.307", # The physical time corresponding to the TSO
        "error": null
    }
    ```

4.  変更フィード`dr-primary-to-secondary`を停止します。変更フィードを削除すると、一時停止できます。

    ```shell
    tiup cdc cli changefeed remove --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"
    ```

5.  パラメータ`start-ts`を指定せずにチェンジフィード`dr-secondary-to-primary`を作成します。このチェンジフィードは現在時刻からデータの複製を開始します。

6.  ビジネスアプリケーションのデータベースアクセス設定を変更します。セカンダリクラスタにアクセスできるように、ビジネスアプリケーションを再起動します。

7.  業務アプリケーションが正常に動作しているかどうかを確認してください。

上記の手順を繰り返すことで、以前のプライマリおよびセカンダリクラスタ構成を復元できます。

#### 災害発生時の一次および二次切り替え {#primary-and-secondary-switchover-upon-disasters}

例えば、プライマリクラスタが設置されている地域で停電などの災害が発生した場合、プライマリクラスタとセカンダリクラスタ間のレプリケーションが突然中断される可能性があります。その結果、セカンダリクラスタ内のデータがプライマリクラスタ内のデータと矛盾することになります。

1.  セカンダリクラスタをトランザクション整合性のある状態に復元します。具体的には、リージョン2内の任意のTiCDCノードで次のコマンドを実行して、リドゥログをセカンダリクラスタに適用します。

    ```shell
    tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://{username}:{password}@10.1.1.4:4000"
    ```

    このコマンドにおけるパラメータの説明は以下のとおりです。

    -   `--storage` ：Amazon S3にリドゥログが保存されるパス
    -   `--tmp-dir` : Amazon S3 からリドゥログをダウンロードするためのキャッシュディレクトリ
    -   `--sink-uri` ：セカンダリクラスタのアドレス

2.  ビジネスアプリケーションのデータベースアクセス設定を変更します。セカンダリクラスタにアクセスできるように、ビジネスアプリケーションを再起動します。

3.  業務アプリケーションが正常に動作しているかどうかを確認してください。

#### プライマリクラスターとセカンダリクラスターを再構築する {#rebuild-the-primary-and-secondary-clusters}

プライマリクラスタで発生した障害が解決した場合、またはプライマリクラスタが一時的に復旧できない場合、セカンダリクラスタのみがプライマリクラスタとして稼働するため、TiDBクラスタは脆弱な状態になります。システムの信頼性を維持するには、DRクラスタを再構築する必要があります。

TiDBのプライマリクラスタとセカンダリクラスタを再構築するには、新しいクラスタをデプロイして新しいDRシステムを構築できます。詳細については、以下のドキュメントを参照してください。

-   [プライマリクラスターとセカンダリクラスターを設定する](#set-up-primary-and-secondary-clusters-based-on-ticdc)
-   [プライマリークラスターからセカンダリークラスターへデータを複製する](#replicate-data-from-the-primary-cluster-to-the-secondary-cluster)
-   上記の手順が完了したら、新しいプライマリー クラスターを作成するには、 [プライマリおよびセカンダリの切り替え](#planned-primary-and-secondary-switchover)参照してください。

> **注記：**
>
> プライマリクラスタとセカンダリクラスタ間のデータ不整合が解消できる場合は、新しいクラスタをデプロイする代わりに、修復されたクラスタを使用してDRシステムを再構築できます。

### セカンダリクラスタでビジネスデータを照会する {#query-business-data-on-the-secondary-cluster}

プライマリ/セカンダリDRシナリオでは、セカンダリクラスタを読み取り専用クラスタとして使用し、レイテンシに影響されないクエリを実行するのが一般的です。TiDBも、プライマリ/セカンダリDRソリューションにおいてこの機能を提供しています。

変更フィードを作成する際に、構成ファイルで同期ポイント機能を有効にします。すると、変更フィードは定期的に（ `sync-point-interval`タイミングで）、セカンダリクラスタ上で`SET GLOBAL tidb_external_ts = @@tidb_current_ts`実行することにより、セカンダリクラスタに複製された一貫性のあるスナップショットポイントを設定します。

セカンダリクラスタからデータを照会するには、ビジネスアプリケーションで`SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;`設定します。そうすることで、プライマリクラスタとトランザクション的に整合性のあるデータを取得できます。

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
> プライマリ・セカンダリ型の災害復旧アーキテクチャでは、セカンダリクラスタは1つのチェンジフィードからのデータしか複製できません。そうでない場合、セカンダリクラスタのデータトランザクションの整合性は保証されません。

### プライマリクラスターとセカンダリクラスター間で双方向レプリケーションを実行する {#perform-bidirectional-replication-between-the-primary-and-secondary-clusters}

このDRシナリオでは、2つのリージョンにあるTiDBクラスタが互いのディザスタリカバリクラスタとして機能します。リージョン構成に基づいて、ビジネストラフィックは対応するTiDBクラスタに書き込まれ、2つのTiDBクラスタは互いのデータをバックアップします。

![TiCDC bidirectional replication](/media/dr/bdr-ticdc.png)

双方向レプリケーション機能により、2つのリージョンにあるTiDBクラスタ間でデータのレプリケーションが可能になります。このDRソリューションは、データのセキュリティと信頼性を保証するとともに、データベースの書き込みパフォーマンスも確保します。計画的なDR切り替えでは、新しいチェンジフィードを開始する前に実行中のチェンジフィードを停止する必要がないため、運用とメンテナンスが簡素化されます。

双方向DRクラスタを構築するには、 [TiCDCの双方向複製](/ticdc/ticdc-bidirectional-replication.md)参照してください。

## トラブルシューティング {#troubleshooting}

前の手順で問題が発生した場合は、まず[TiDBに関するよくある質問](/faq/faq-overview.md)で問題の解決策を見つけてください。問題が解決しない場合は、 [バグを報告する](/support.md)実行してください。

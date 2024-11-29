---
title: Migrate from one TiDB cluster to another TiDB cluster
summary: ある TiDB クラスターから別の TiDB クラスターにデータを移行する方法を学習します。
---

# ある TiDBクラスタから別の TiDBクラスタに移行する {#migrate-from-one-tidb-cluster-to-another-tidb-cluster}

このドキュメントでは、ある TiDB クラスターから別の TiDB クラスターにデータを移行する方法について説明します。この機能は、次のシナリオに適用されます。

-   データベースの分割: TiDB クラスターが大きすぎる場合、またはクラスターのサービス間への影響を避けたい場合は、データベースを分割できます。
-   データベースの再配置: データ センターの変更など、データベースを物理的に再配置します。
-   新しいバージョンの TiDB クラスターにデータを移行する: データのセキュリティと精度の要件を満たすために、新しいバージョンの TiDB クラスターにデータを移行します。

このドキュメントでは、移行プロセス全体を例示しており、次の手順が含まれています。

1.  環境を設定します。

2.  全データを移行します。

3.  増分データを移行します。

4.  サービスを新しい TiDB クラスターに移行します。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1.  TiDB クラスターをデプロイ。

    TiUP Playground を使用して、アップストリームとダウンストリームの 2 つの TiDB クラスターをデプロイ。詳細については、 [TiUP を使用してオンライン TiDBクラスタをデプロイおよび管理](/tiup/tiup-cluster.md)を参照してください。

    ```shell
    # Create an upstream cluster
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、新しくデプロイされたクラスターにテスト データベースが作成されます。したがって、 [システムベンチ](https://github.com/akopytov/sysbench#linux)使用してテスト データを生成し、実際のシナリオでデータをシミュレートできます。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbench を使用して`oltp_write_only`スクリプトを実行します。このスクリプトは、テスト データベースに 10,000 行のテーブルを 10 個生成します。tidb-config は次のとおりです。

    ```shell
    mysql-host=172.16.6.122 # Replace the value with the IP address of your upstream cluster
    mysql-port=4000
    mysql-user=root
    mysql-password=
    db-driver=mysql         # Set database driver to MySQL
    mysql-db=test           # Set the database as a test database
    report-interval=10      # Set data collection period to 10s
    threads=10              # Set the number of worker threads to 10
    time=0                  # Set the time required for executing the script. O indicates time unlimited
    rate=100                # Set average TPS to 100
    ```

3.  サービスのワークロードをシミュレートします。

    実際のシナリオでは、サービス データはアップストリーム クラスターに継続的に書き込まれます。このドキュメントでは、sysbench を使用してこのワークロードをシミュレートします。具体的には、次のコマンドを実行して、10 人のワーカーが sbtest1、sbtest2、sbtest3 の 3 つのテーブルにデータを継続的に書き込むようにします。TPS の合計は 100 を超えません。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部storageを準備します。

    フルデータバックアップでは、上流クラスターと下流クラスターの両方がバックアップファイルにアクセスする必要があります。バックアップファイルの保存には[外部storage](/br/backup-and-restore-storages.md)使用することをお勧めします。このドキュメントでは、Minio を使用して S3 互換のstorageサービスをシミュレートします。

    ```shell
    wget https://dl.min.io/server/minio/release/linux-amd64/minio
    chmod +x minio
    # Configure access-key access-screct-id to access minio
    export HOST_IP='172.16.6.122' # Replace the value with the IP address of your upstream cluster
    export MINIO_ROOT_USER='minio'
    export MINIO_ROOT_PASSWORD='miniostorage'
    # Create the database directory. backup is the bucket name.
    mkdir -p data/backup
    # Start minio at port 6060
    ./minio server ./data --address :6060 &
    ```

    上記のコマンドは、1 つのノードで minioサーバーを起動し、S3 サービスをシミュレートします。コマンドのパラメータは次のように設定されます。

    -   エンドポイント: `http://${HOST_IP}:6060/`
    -   アクセスキー: `minio`
    -   シークレットアクセスキー: `miniostorage`
    -   バケット: `backup`

    アクセスリンクは以下の通りです。

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ2. 全データを移行する {#step-2-migrate-full-data}

環境設定後、 [BR](https://github.com/pingcap/tidb/tree/release-8.1/br)のバックアップと復元関数を使用して全データを移行できます。 [3つの方法](/br/br-use-overview.md#deploy-and-use-br)でBR を起動できます。 このドキュメントでは、SQL 文`BACKUP`と`RESTORE`使用します。

> **注記：**
>
> -   `BACKUP`と`RESTORE` SQL ステートメントは実験的です。本番環境での使用は推奨されません。予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。
> -   本番クラスターでは、GC を無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響する可能性があります。パフォーマンスの低下を避けるために、オフピーク時にデータをバックアップし、 `RATE_LIMIT`を適切な値に設定することをお勧めします。
> -   アップストリーム クラスタとダウンストリーム クラスタのバージョンが異なる場合は、 [BR互換性](/br/backup-and-restore-overview.md#before-you-use)確認する必要があります。このドキュメントでは、アップストリーム クラスタとダウンストリーム クラスタは同じバージョンであると想定しています。

1.  GC を無効にします。

    増分移行中に新しく書き込まれたデータが削除されないようにするには、バックアップの前にアップストリーム クラスターの GC を無効にする必要があります。この方法では、履歴データは削除されません。

    GC を無効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+:
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

    > **注記：**
    >
    > TiCDC `gc-ttl`デフォルトで 24 時間です。バックアップと復元に長い時間がかかる場合、デフォルトの`gc-ttl`不十分な可能性があり、後続の[増分レプリケーションタスク](#step-3-migrate-incremental-data)失敗する可能性があります。この状況を回避するには、TiCDCサーバーを起動するときに、特定のニーズに応じて`gc-ttl`値を調整します。詳細については、 [TiCDC の`gc-ttl`とは何ですか?](/ticdc/ticdc-faq.md#what-is-gc-ttl-in-ticdc)参照してください。

2.  データをバックアップします。

    データをバックアップするには、アップストリーム クラスターで`BACKUP`ステートメントを実行します。

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    ```

        +---------------+----------+--------------------+---------------------+---------------------+
        | Destination   | Size     | BackupTS           | Queue Time          | Execution Time      |
        +---------------+----------+--------------------+---------------------+---------------------+
        | s3://backup   | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +---------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`コマンドが実行されると、 TiDB はバックアップ データに関するメタデータを返します。 `BackupTS`はバックアップされる前に生成されたデータなので注意してください。 このドキュメントでは、 `BackupTS`**データ チェックの終了**と**TiCDC による増分移行スキャンの開始**として使用します。

3.  データを復元します。

    データを復元するには、ダウンストリーム クラスターで`RESTORE`コマンドを実行します。

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    ```

        +--------------+-----------+--------------------+---------------------+---------------------+
        | Destination  | Size      | BackupTS           | Queue Time          | Execution Time      |
        +--------------+-----------+--------------------+---------------------+---------------------+
        | s3://backup  | 10315858  | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
        +--------------+-----------+--------------------+---------------------+---------------------+
        1 row in set (41.85 sec)

4.  (オプション) データを検証します。

    [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用すると、特定の時点でのアップストリームとダウンストリーム間のデータの一貫性を確認できます。前の`BACKUP`出力は、アップストリーム クラスターが 431434047157698561 にバックアップを完了したことを示しています。前の`RESTORE`出力は、ダウンストリームが 431434141450371074 に復元を完了したことを示しています。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の設定方法の詳細については、 [コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)参照してください。このドキュメントでは、設定は次のようになります。

    ```shell
    # Diff Configuration.
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
        host = "172.16.6.122" # Replace the value with the IP address of your upstream cluster
        port = 4000
        user = "root"
        password = ""
        snapshot = "431434047157698561" # Set snapshot to the actual backup time (BackupTS in the "Back up data" section in [Step 2. Migrate full data](#step-2-migrate-full-data))
    [data-sources.downstream]
        host = "172.16.6.125" # Replace the value with the IP address of your downstream cluster
        port = 4000
        user = "root"
        password = ""

    ######################### Task config #########################
    [task]
        output-dir = "./output"
        source-instances = ["upstream"]
        target-instance = "downstream"
        target-check-tables = ["*.*"]
    ```

## ステップ3. 増分データを移行する {#step-3-migrate-incremental-data}

1.  TiCDCをデプロイ。

    完全なデータ移行が完了したら、増分データをレプリケートするために TiCDC をデプロイして構成します。本番環境では、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md)の手順に従って TiCDC をデプロイします。このドキュメントでは、テスト クラスターの作成時に TiCDC ノードが起動されています。したがって、TiCDC をデプロイする手順をスキップして、changefeed 構成に進むことができます。

2.  変更フィードを作成します。

    アップストリーム クラスターで次のコマンドを実行して、アップストリーム クラスターからダウンストリーム クラスターへの変更フィードを作成します。

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="upstream-to-downstream" --start-ts="431434047157698561"
    ```

    このコマンドのパラメータは次のとおりです。

    -   `--server` : TiCDC クラスター内の任意のノードの IP アドレス
    -   `--sink-uri` : ダウンストリーム クラスターの URI
    -   `--changefeed-id` : チェンジフィード ID。正規表現の形式である必要があります。^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$
    -   `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時間 (または[ステップ2. 全データを移行する](#step-2-migrate-full-data)の「データのバックアップ」セクションの BackupTS) である必要があります。

    changefeed 構成の詳細については、 [タスク設定ファイル](/ticdc/ticdc-changefeed-config.md)参照してください。

3.  GC を有効にします。

    TiCDC を使用した増分移行では、GC はレプリケートされた履歴データのみを削除します。そのため、チェンジフィードを作成した後、以下のコマンドを実行して GC を有効にする必要があります。詳細については、 [TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか?](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)参照してください。

    GC を有効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

## ステップ4. 新しいTiDBクラスタにサービスを移行する {#step-4-migrate-services-to-the-new-tidb-cluster}

変更フィードを作成すると、アップストリーム クラスターに書き込まれたデータは、低レイテンシーでダウンストリーム クラスターに複製されます。読み取りトラフィックをダウンストリーム クラスターに徐々に移行できます。一定期間観察します。ダウンストリーム クラスターが安定している場合は、次の手順を実行して、書き込みトラフィックをダウンストリーム クラスターに移行できます。

1.  アップストリーム クラスターの書き込みサービスを停止します。変更フィードを停止する前に、すべてのアップストリーム データがダウンストリームに複製されていることを確認してください。

    ```shell
    # Stop the changefeed from the upstream cluster to the downstream cluster
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --server=http://172.16.6.122:8300

    # View the changefeed status
    tiup cdc cli changefeed list
    ```

        [
          {
            "id": "upstream-to-downstream",
            "summary": {
            "state": "stopped",  # Ensure that the status is stopped
            "tso": 431747241184329729,
            "checkpoint": "2022-03-11 15:50:20.387", # This time must be later than the time of stopping writing
            "error": null
            }
          }
        ]

2.  ダウンストリームからアップストリームへの変更フィードを作成します。アップストリームとダウンストリームのデータは一貫しており、クラスターに書き込まれる新しいデータはないため、デフォルト設定を使用するために`start-ts`指定しないままにすることができます。

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.125:8300 --sink-uri="mysql://root:@172.16.6.122:4000" --changefeed-id="downstream -to-upstream"
    ```

3.  書き込みサービスをダウンストリーム クラスターに移行した後、しばらく観察します。ダウンストリーム クラスターが安定している場合は、アップストリーム クラスターを破棄できます。

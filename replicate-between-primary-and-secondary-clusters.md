---
title: Replicate data between primary and secondary clusters
summary: プライマリ クラスターからセカンダリ クラスターにデータを複製する方法を学習します。
---

# プライマリクラスタとセカンダリクラスタ間でデータを複製する {#replicate-data-between-primary-and-secondary-clusters}

このドキュメントでは、TiDBプライマリ（上流）クラスタとTiDBまたはMySQLセカンダリ（下流）クラスタを設定し、プライマリクラスタからセカンダリクラスタに増分データをレプリケートする方法について説明します。このプロセスは、以下の手順で構成されます。

1.  TiDB プライマリ クラスターと TiDB または MySQL セカンダリ クラスターを構成します。
2.  プライマリ クラスターからセカンダリ クラスターに増分データを複製します。
3.  プライマリ クラスターがダウンしている場合は、Redo ログを使用してデータを一貫して回復します。

実行中の TiDB クラスターからセカンダリ クラスターに増分データを複製するには、バックアップと復元[BR](/br/backup-and-restore-overview.md)と[TiCDC](/ticdc/ticdc-overview.md)使用できます。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1.  TiDB クラスターをデプロイ。

    TiUP Playgroundを使用して、アップストリームとダウンストリームにそれぞれ1つずつTiDBクラスターを2つデプロイ。本番環境では、 [TiUPを使用してオンライン TiDBクラスタをデプロイおよび管理](/tiup/tiup-cluster.md)を参照してクラスターをデプロイしてください。

    このドキュメントでは、2 つのクラスターを 2 台のマシンにデプロイします。

    -   ノードA: 172.16.6.123、上流TiDBクラスタのデプロイ用

    -   ノードB: 172.16.6.124、下流TiDBクラスタのデプロイ用

    ```shell
    # Create an upstream cluster on Node A
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster on Node B
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、新しくデプロイされたクラスターにテストデータベースが作成されます。そのため、 [システムベンチ](https://github.com/akopytov/sysbench#linux)使用してテストデータを生成し、実際のシナリオでデータをシミュレートできます。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbenchを使用してスクリプト`oltp_write_only`実行します。このスクリプトは、上流データベースにそれぞれ10,000行のテーブルを10個生成します。tidb-configは以下のとおりです。

    ```shell
    mysql-host=172.16.6.122 # Replace it with the IP address of your upstream cluster
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

    実際のシナリオでは、サービスデータは上流クラスターに継続的に書き込まれます。このドキュメントでは、sysbenchを使用してこのワークロードをシミュレートします。具体的には、以下のコマンドを実行して、10人のワーカーが3つのテーブル（sbtest1、sbtest2、sbtest3）に継続的にデータを書き込むようにし、合計TPSが100を超えないようにします。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部storageを準備します。

    フルデータバックアップでは、上流クラスターと下流クラスターの両方がバックアップファイルにアクセスする必要があります。バックアップファイルの保存には[外部storage](/br/backup-and-restore-storages.md)使用することをお勧めします。この例では、Minioを使用してS3互換storageサービスをシミュレートしています。

    ```shell
    wget https://dl.min.io/server/minio/release/linux-amd64/minio
    chmod +x minio
    # Configure access-key access-screct-id to access minio
    export HOST_IP='172.16.6.123' # Replace it with the IP address of your upstream cluster
    export MINIO_ROOT_USER='minio'
    export MINIO_ROOT_PASSWORD='miniostorage'
    # Create the redo and backup directories. `backup` and `redo` are bucket names.
    mkdir -p data/redo
    mkdir -p data/backup
    # Start minio at port 6060
    nohup ./minio server ./data --address :6060 &
    ```

    上記のコマンドは、S3サービスをシミュレートするために、1つのノードでminioサーバーを起動します。コマンドのパラメータは以下のように設定されています。

    -   エンドポイント: `http://${HOST_IP}:6060/`
    -   アクセスキー: `minio`
    -   シークレットアクセスキー: `miniostorage`
    -   バケット: `redo`

    リンクは次のとおりです。

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ2. 全データの移行 {#step-2-migrate-full-data}

環境構築後、 [BR](https://github.com/pingcap/tidb/tree/release-8.5/br)のバックアップ・リストア関数を使用して全データを移行できます。BRは[3つの方法](/br/br-use-overview.md#deploy-and-use-br)で起動できます。本稿では、SQL文`BACKUP`と`RESTORE`使用します。

> **注記：**
>
> -   `BACKUP`と`RESTORE` SQL 文は実験的です。本番環境での使用は推奨されません。予告なく変更または削除される可能性があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告してください。
> -   本番のクラスタでは、GCを無効にしてバックアップを実行すると、クラスタのパフォーマンスに影響する可能性があります。パフォーマンスの低下を防ぐため、データのバックアップはオフピーク時間帯に行い、RATE_LIMITを適切な値に設定することをお勧めします。
> -   アップストリームクラスタとダウンストリームクラスタのバージョンが異なる場合は、 [BR互換性](/br/backup-and-restore-overview.md#some-tips)確認する必要があります。このドキュメントでは、アップストリームクラスタとダウンストリームクラスタは同じバージョンであると想定しています。

1.  GC を無効にします。

    増分マイグレーション中に新しく書き込まれたデータが削除されないようにするには、バックアップ前に上流クラスターのGCを無効にする必要があります。これにより、履歴データが削除されなくなります。

    GC を無効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

2.  データをバックアップします。

    データをバックアップするには、アップストリーム クラスターで`BACKUP`ステートメントを実行します。

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | local:///tmp/backup/ | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`コマンドの実行後、TiDB はバックアップデータに関するメタデータを返します。3 はバックアップ前に生成されたデータなので、ご注意ください。このドキュメントでは、 `BackupTS` `BackupTS`**データチェックの終了**と**TiCDC による増分移行スキャンの開始**として使用します。

3.  データを復元します。

    ダウンストリーム クラスターで`RESTORE`コマンドを実行してデータを復元します。

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | local:///tmp/backup/ | 10315858 | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (41.85 sec)

4.  (オプション) データを検証します。

    [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) 、特定の時刻における上流と下流のデータの整合性を確認するために使用します。上記の`BACKUP`出力は、上流クラスターが 431434047157698561 にバックアップを完了したことを示しています。上記の`RESTORE`出力は、下流クラスターが 431434141450371074 に復元を完了したことを示しています。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の設定方法の詳細については[コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)参照してください。このドキュメントでは、設定は以下のとおりです。

    ```shell
    # Diff Configuration.
    ######################### Global config #########################
    check-thread-count = 4
    export-fix-sql = true
    check-struct-only = false

    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
            host = "172.16.6.123" # Replace it with the IP address of your upstream cluster
            port = 4000
            user = "root"
            password = ""
            snapshot = "431434047157698561" # Set snapshot to the actual backup time
    [data-sources.downstream]
            host = "172.16.6.124" # Replace the value with the IP address of your downstream cluster
            port = 4000
            user = "root"
            password = ""
            snapshot = "431434141450371074" # Set snapshot to the actual restore time

    ######################### Task config #########################
    [task]
            output-dir = "./output"
            source-instances = ["upstream"]
            target-instance = "downstream"
            target-check-tables = ["*.*"]
    ```

## ステップ3. 増分データの移行 {#step-3-migrate-incremental-data}

1.  TiCDCをデプロイ。

    完全なデータ移行が完了したら、増分データをレプリケーションするためのTiCDCをデプロイして設定します。本番環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)の手順に従ってTiCDCをデプロイしてください。このドキュメントでは、テストクラスターの作成時にTiCDCノードが起動済みであるため、TiCDCのデプロイ手順は省略し、変更フィードの設定に進みます。

2.  変更フィードを作成します。

    changefeed 構成ファイル`changefeed.toml`を作成します。

    ```shell
    [consistent]
    # Consistency level, eventual means enabling consistent replication
    level = "eventual"
    # Use S3 to store redo logs. Other options are local and nfs.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.125:6060&force-path-style=true"
    ```

    アップストリーム クラスターで次のコマンドを実行して、アップストリーム クラスターからダウンストリーム クラスターへの変更フィードを作成します。

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary" --start-ts="431434047157698561"
    ```

    このコマンドのパラメータは次のとおりです。

    -   `--server` : TiCDC クラスター内の任意のノードの IP アドレス
    -   `--sink-uri` : 下流クラスタのURI
    -   `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時刻（または[ステップ2. 全データの移行](#step-2-migrate-full-data)で説明した BackupTS）である必要があります。

    changefeed 構成の詳細については、 [TiCDC Changefeedフィード構成](/ticdc/ticdc-changefeed-config.md)参照してください。

3.  GC を有効にします。

    TiCDCを用いた増分移行では、GCは複製された履歴データのみを削除します。そのため、変更フィードを作成した後、以下のコマンドを実行してGCを有効にする必要があります。詳細は[TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか?](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)参照してください。

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

## ステップ4.上流クラスターで災害をシミュレートする {#step-4-simulate-a-disaster-in-the-upstream-cluster}

上流クラスターの実行中に、そのクラスターで致命的なイベントを発生させます。例えば、Ctrl+C を押すことで、tiup プレイグラウンドプロセスを終了できます。

## ステップ5. REDOログを使用してデータの一貫性を確保する {#step-5-use-redo-log-to-ensure-data-consistency}

通常、TiCDCはスループットを向上させるために、下流へのトランザクションの同時書き込みを行います。変更フィードが予期せず中断された場合、下流のデータが上流のデータと異なる可能性があります。この不整合に対処するには、以下のコマンドを実行して、下流のデータと上流のデータの整合性を確保してください。

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

-   `--storage` : S3内のREDOログの場所と認証情報
-   `--tmp-dir` : S3からダウンロードしたREDOログのキャッシュディレクトリ
-   `--sink-uri` : 下流クラスタのURI

## ステップ6. プライマリクラスタとそのサービスを回復する {#step-6-recover-the-primary-cluster-and-its-services}

前の手順の後、下流（セカンダリ）クラスターには、特定の時点における上流（プライマリ）クラスターと整合性のあるデータが格納されます。データの信頼性を確保するには、新しいプライマリクラスターとセカンダリクラスターをセットアップする必要があります。

1.  新しいプライマリ クラスターとして、ノード A に新しい TiDB クラスターをデプロイ。

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2.  BRを使用して、セカンダリ クラスターからプライマリ クラスターにデータを完全にバックアップおよび復元します。

    ```shell
    # Back up full data of the secondary cluster
    tiup br --pd http://172.16.6.124:2379 backup full --storage ./backup
    # Restore full data of the secondary cluster
    tiup br --pd http://172.16.6.123:2379 restore full --storage ./backup
    ```

3.  プライマリ クラスターからセカンダリ クラスターにデータをバックアップするための新しい変更フィードを作成します。

    ```shell
    # Create a changefeed
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary"
    ```

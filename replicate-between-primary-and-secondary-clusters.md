---
title: Replicate data between primary and secondary clusters
summary: プライマリ クラスターからセカンダリ クラスターにデータを複製する方法を学習します。
---

# プライマリクラスタとセカンダリクラスタ間でデータを複製する {#replicate-data-between-primary-and-secondary-clusters}

このドキュメントでは、TiDB プライマリ (アップストリーム) クラスターと TiDB または MySQL セカンダリ (ダウンストリーム) クラスターを構成し、プライマリ クラスターからセカンダリ クラスターに増分データをレプリケートする方法について説明します。プロセスには、次の手順が含まれます。

1.  TiDB プライマリ クラスターと TiDB または MySQL セカンダリ クラスターを構成します。
2.  プライマリ クラスターからセカンダリ クラスターに増分データを複製します。
3.  プライマリ クラスターがダウンしたときに、REDO ログを使用してデータを一貫して回復します。

実行中の TiDB クラスターからセカンダリ クラスターに増分データを複製するには、バックアップと復元[BR](/br/backup-and-restore-overview.md)および[ティCDC](/ticdc/ticdc-overview.md)使用できます。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1.  TiDB クラスターをデプロイ。

    TiUP Playground を使用して、アップストリームとダウンストリームの 2 つの TiDB クラスターをデプロイ。本番環境では、 [TiUP を使用してオンライン TiDBクラスタをデプロイおよび管理](/tiup/tiup-cluster.md)を参照してクラスターをデプロイします。

    このドキュメントでは、2 つのクラスターを 2 台のマシンにデプロイします。

    -   ノードA: 172.16.6.123、上流TiDBクラスタのデプロイ用

    -   ノード B: 172.16.6.124、下流 TiDB クラスターのデプロイ用

    ```shell
    # Create an upstream cluster on Node A
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster on Node B
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、新しくデプロイされたクラスターにテスト データベースが作成されます。したがって、 [システムベンチ](https://github.com/akopytov/sysbench#linux)使用してテスト データを生成し、実際のシナリオでデータをシミュレートできます。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbench を使用して`oltp_write_only`スクリプトを実行します。このスクリプトは、アップストリーム データベースに 10,000 行のテーブルを 10 個生成します。tidb-config は次のとおりです。

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

    実際のシナリオでは、サービス データはアップストリーム クラスターに継続的に書き込まれます。このドキュメントでは、sysbench を使用してこのワークロードをシミュレートします。具体的には、次のコマンドを実行して、10 人のワーカーが sbtest1、sbtest2、sbtest3 の 3 つのテーブルにデータを継続的に書き込むようにします。TPS の合計は 100 を超えません。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部storageを準備します。

    フルデータバックアップでは、上流クラスターと下流クラスターの両方がバックアップファイルにアクセスする必要があります。バックアップファイルの保存には[外部storage](/br/backup-and-restore-storages.md)使用することをお勧めします。この例では、Minio を使用して S3 互換のstorageサービスをシミュレートします。

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

    上記のコマンドは、1 つのノードで minioサーバーを起動し、S3 サービスをシミュレートします。コマンドのパラメータは次のように設定されます。

    -   エンドポイント: `http://${HOST_IP}:6060/`
    -   アクセスキー: `minio`
    -   シークレットアクセスキー: `miniostorage`
    -   バケット: `redo`

    リンクは次のとおりです。

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ2. 全データを移行する {#step-2-migrate-full-data}

環境設定後、 [BR](https://github.com/pingcap/tidb/tree/release-8.5/br)のバックアップと復元関数を使用して全データを移行できます。 [3つの方法](/br/br-use-overview.md#deploy-and-use-br)でBR を起動できます。 このドキュメントでは、SQL 文`BACKUP`と`RESTORE`使用します。

> **注記：**
>
> -   `BACKUP`と`RESTORE` SQL ステートメントは実験的です。本番環境での使用は推奨されません。予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。
> -   本番クラスターでは、GC を無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響する可能性があります。パフォーマンスの低下を避けるために、オフピーク時にデータをバックアップし、RATE_LIMIT を適切な値に設定することをお勧めします。
> -   アップストリーム クラスタとダウンストリーム クラスタのバージョンが異なる場合は、 [BR互換性](/br/backup-and-restore-overview.md#some-tips)確認する必要があります。このドキュメントでは、アップストリーム クラスタとダウンストリーム クラスタは同じバージョンであると想定しています。

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

    `BACKUP`コマンドが実行されると、 TiDB はバックアップ データに関するメタデータを返します。 `BackupTS`はバックアップされる前に生成されたデータなので注意してください。 このドキュメントでは、 `BackupTS`**データ チェックの終了**と**TiCDC による増分移行スキャンの開始**として使用します。

3.  データを復元します。

    データを復元するには、ダウンストリーム クラスターで`RESTORE`コマンドを実行します。

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

    [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用して、特定の時間におけるアップストリームとダウンストリーム間のデータの整合性を確認します。前の`BACKUP`の出力は、アップストリーム クラスターが 431434047157698561 にバックアップを完了したことを示しています。前の`RESTORE`出力は、ダウンストリームが 431434141450371074 に復元を完了したことを示しています。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の設定方法の詳細については、 [コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)参照してください。このドキュメントでは、設定は次のとおりです。

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

## ステップ3. 増分データを移行する {#step-3-migrate-incremental-data}

1.  TiCDCをデプロイ。

    完全なデータ移行が完了したら、増分データをレプリケートするために TiCDC をデプロイして構成します。本番環境では、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md)の手順に従って TiCDC をデプロイします。このドキュメントでは、テスト クラスターの作成時に TiCDC ノードが起動されています。そのため、TiCDC をデプロイする手順をスキップし、changefeed 構成に進みます。

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
    -   `--sink-uri` : ダウンストリーム クラスターの URI
    -   `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時間（または[ステップ2. 全データを移行する](#step-2-migrate-full-data)で説明した BackupTS）である必要があります。

    changefeed 構成の詳細については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)参照してください。

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

## ステップ4. 上流クラスターで災害をシミュレートする {#step-4-simulate-a-disaster-in-the-upstream-cluster}

アップストリーム クラスターの実行中に、そのクラスターで致命的なイベントを作成します。たとえば、Ctrl + C を押すと、tiup プレイグラウンド プロセスを終了できます。

## ステップ5. REDOログを使用してデータの一貫性を確保する {#step-5-use-redo-log-to-ensure-data-consistency}

通常、TiCDC はスループットを向上させるために、ダウンストリームにトランザクションを同時に書き込みます。変更フィードが予期せず中断されると、ダウンストリームにはアップストリームと同じ最新のデータがない可能性があります。不整合を解決するには、次のコマンドを実行して、ダウンストリーム データがアップストリーム データと整合していることを確認します。

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

-   `--storage` : S3 内の REDO ログの場所と認証情報
-   `--tmp-dir` : S3からダウンロードしたREDOログのキャッシュディレクトリ
-   `--sink-uri` : ダウンストリーム クラスターの URI

## ステップ6. プライマリクラスタとそのサービスを回復する {#step-6-recover-the-primary-cluster-and-its-services}

前の手順を実行すると、ダウンストリーム (セカンダリ) クラスターには、特定の時点でアップストリーム (プライマリ) クラスターと一致するデータが格納されます。データの信頼性を確保するには、新しいプライマリ クラスターとセカンダリ クラスターをセットアップする必要があります。

1.  新しいプライマリ クラスターとして、ノード A に新しい TiDB クラスターをデプロイ。

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2.  BR を使用して、セカンダリ クラスターからプライマリ クラスターにデータを完全にバックアップおよび復元します。

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

---
title: Replicate data between primary and secondary clusters
summary: プライマリクラスタからセカンダリクラスタへデータを複製する方法を学びましょう。
---

# プライマリクラスタとセカンダリクラスタ間でデータを複製する {#replicate-data-between-primary-and-secondary-clusters}

このドキュメントでは、TiDBプライマリ（アップストリーム）クラスタとTiDBまたはMySQLセカンダリ（ダウンストリーム）クラスタを構成し、プライマリクラスタからセカンダリクラスタへ増分データをレプリケートする方法について説明します。プロセスには以下の手順が含まれます。

1.  TiDBプライマリクラスタと、TiDBまたはMySQLセカンダリクラスタを設定します。
2.  プライマリクラスタからセカンダリクラスタへ、増分データを複製する。
3.  プライマリクラスタがダウンした場合でも、リドゥログを使用してデータの確実な復旧を実現します。

実行中の TiDB クラスタからセカンダリ クラスタに増分データを複製するには、Backup &amp; Restore [BR](/br/backup-and-restore-overview.md)と[TiCDC](/ticdc/ticdc-overview.md)を使用できます。

## ステップ1. 環境をセットアップする {#step-1-set-up-the-environment}

1.  TiDBクラスタをデプロイ。

    TiUP Playground を使用して、2 つの TiDB クラスター (1 つはアップストリーム、もう 1 つはダウンストリーム)をデプロイ。本番環境の場合は、 [TiUPを使用してオンラインTiDBクラスタをデプロイおよび管理](/tiup/tiup-cluster.md)を参照してクラスターをデプロイします。

    このドキュメントでは、2台のマシンに2つのクラスターをデプロイします。

    -   ノードA：172.16.6.123、上流のTiDBクラスタをデプロイするため

    -   ノードB：172.16.6.124、下流のTiDBクラスタをデプロイするため

    ```shell
    # Create an upstream cluster on Node A
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster on Node B
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、新しくデプロイされたクラスタにテストデータベースが作成されます。そのため、 [sysbench](https://github.com/akopytov/sysbench#linux)を使用してテストデータを生成し、実際のシナリオでデータをシミュレートできます。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbench を使用して`oltp_write_only`スクリプトを実行します。このスクリプトは、アップストリームデータベースに 10 個のテーブルを生成し、各テーブルには 10,000 行のデータが含まれます。tidb-config は以下のとおりです。

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

3.  サービス負荷をシミュレーションします。

    実際のシナリオでは、サービスデータはアップストリームクラスタに継続的に書き込まれます。このドキュメントでは、sysbenchを使用してこのワークロードをシミュレートします。具体的には、以下のコマンドを実行して、10個のワーカーがsbtest1、sbtest2、sbtest3の3つのテーブルにデータを継続的に書き込むようにし、合計TPSが100を超えないようにします。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部storageを準備してください。

    フルデータバックアップでは、アップストリームクラスタとダウンストリームクラスタの両方がバックアップファイルにアクセスする必要があります。バックアップファイルの保存には[外部storage](/br/backup-and-restore-storages.md)を使用することをお勧めします。この例では、Minioを使用してS3互換のstorageサービスをシミュレートしています。

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

    上記のコマンドは、S3サービスをシミュレートするために、1つのノード上でMinIOサーバーを起動します。コマンドのパラメータは次のように設定されます。

    -   エンドポイント: `http://${HOST_IP}:6060/`
    -   アクセスキー: `minio`
    -   秘密アクセスキー: `miniostorage`
    -   バケット: `redo`

    リンクは以下のとおりです。

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ2. 全データを移行する {#step-2-migrate-full-data}

環境設定後、 [BR](https://github.com/pingcap/tidb/tree/release-8.5/br)のバックアップおよび復元関数を使用して、データ全体を移行できます。BRは[3つの方法](/br/br-use-overview.md#deploy-and-use-br)で起動できます。このドキュメントでは、SQL ステートメント`BACKUP`および`RESTORE`を使用します。

> **注記：**
>
> -   `BACKUP`および`RESTORE` SQL ステートメントは実験的です。本番環境での使用は推奨されません。予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   本番のクラスタでは、GCを無効にした状態でバックアップを実行すると、クラスタのパフォーマンスに影響を与える可能性があります。パフォーマンスの低下を避けるため、データのバックアップはピーク時以外の時間帯に行い、RATE_LIMITを適切な値に設定することをお勧めします。
> -   アップストリームとダウンストリームのクラスタのバージョンが異なる場合は、 [BR互換性](/br/backup-and-restore-overview.md#some-tips)確認してください。このドキュメントでは、アップストリームとダウンストリームのクラスタのバージョンが同じであることを前提としています。

1.  GCを無効にする。

    増分移行中に新しく書き込まれたデータが削除されないようにするには、バックアップ前にアップストリームクラスタのガベージコレクション（GC）を無効にする必要があります。こうすることで、履歴データが削除されるのを防ぐことができます。

    GCを無効にするには、以下のコマンドを実行してください。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会してください。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

2.  データをバックアップしてください。

    上流クラスターで`BACKUP`ステートメントを実行してデータをバックアップします。

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | local:///tmp/backup/ | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`コマンドが実行されると、TiDB はバックアップ データに関するメタデータを返します。 `BackupTS`には、それ以前に生成されたデータがバックアップされるため、注意してください。このドキュメントでは、 `BackupTS`**データ チェックの終了**と**TiCDC による増分移行スキャンの開始**として使用します。

3.  データを復元します。

    ダウンストリームクラスタで`RESTORE`コマンドを実行してデータを復元します。

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | local:///tmp/backup/ | 10315858 | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (41.85 sec)

4.  （オプション）データの検証。

    [同期差分検査ツール](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して、特定の時刻におけるアップストリームとダウンストリーム間のデータの一貫性を確認します。前述の`BACKUP`出力は、アップストリーム クラスタが 431434047157698561 にバックアップを完了したことを示しています。前述の`RESTORE`出力は、ダウンストリームが 431434141450371074 にリストアを完了したことを示しています。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の設定方法の詳細については、 [コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)参照してください。このドキュメントでは、構成は次のようになります。

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

    データの完全移行が完了したら、増分データを複製するために TiCDC をデプロイして構成します。本番環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)デプロイしてください。このドキュメントでは、テスト クラスターの作成時に TiCDC ノードが起動されているため、TiCDC のデプロイ手順は省略し、changefeed の構成に進みます。

2.  変更フィードを作成します。

    変更フィード設定ファイル`changefeed.toml`を作成します。

    ```shell
    [consistent]
    # Consistency level, eventual means enabling consistent replication
    level = "eventual"
    # Use S3 to store redo logs. Other options are local and nfs.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.125:6060&force-path-style=true"
    ```

    アップストリームクラスターで、次のコマンドを実行して、アップストリームクラスターからダウンストリームクラスターへの変更フィードを作成します。

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary" --start-ts="431434047157698561" --config=./changefeed.toml
    ```

    このコマンドにおけるパラメータは以下のとおりです。

    -   `--server` : TiCDCクラスタ内の任意のノードのIPアドレス
    -   `--sink-uri` : ダウンストリームクラスタのURI
    -   `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時間 (または[ステップ2. 全データを移行する](#step-2-migrate-full-data))

    チェンジフィード構成の詳細については、 [TiCDC Changefeedフィード構成](/ticdc/ticdc-changefeed-config.md)参照してください。

3.  GCを有効にする。

    TiCDC を使用した増分移行では、GC はレプリケートされた履歴データのみを削除します。したがって、変更フィードを作成した後、次のコマンドを実行して GC を有効にする必要があります。詳細については、 [TiCDCのガベージコレクション（GC）セーフポイントの完全な動作とはどのようなものですか？](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)参照してください。

    GCを有効にするには、次のコマンドを実行してください。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会してください。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

## ステップ4．上流クラスターで災害をシミュレーションする {#step-4-simulate-a-disaster-in-the-upstream-cluster}

上流クラスタが実行中に、致命的な障害を発生させます。たとえば、Ctrl+C を押して tiup プレイグラウンド プロセスを終了させることができます。

## ステップ5．リドゥログを使用してデータの一貫性を確保する {#step-5-use-redo-log-to-ensure-data-consistency}

通常、TiCDCはスループットを向上させるために、トランザクションをダウンストリームに同時に書き込みます。変更フィードが予期せず中断された場合、ダウンストリームにはアップストリームと同じ最新データが存在しない可能性があります。この不整合に対処するには、次のコマンドを実行して、ダウンストリームのデータがアップストリームのデータと整合していることを確認してください。

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

-   `--storage` : S3 内のリドゥログの場所と認証情報
-   `--tmp-dir` : S3からダウンロードしたリドゥログのキャッシュディレクトリ
-   `--sink-uri` : ダウンストリームクラスタのURI

## ステップ6．プライマリクラスタとそのサービスを復旧する {#step-6-recover-the-primary-cluster-and-its-services}

前の手順の後、下流（セカンダリ）クラスターには、特定の時点において上流（プライマリ）クラスターと整合性のあるデータが格納されます。データの信頼性を確保するためには、新しいプライマリクラスターとセカンダリクラスターを設定する必要があります。

1.  新しいプライマリクラスタとして、ノードA上に新しいTiDBクラスタをデプロイ。

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2.  BRを使用して、セカンダリクラスタからプライマリクラスタへデータを完全にバックアップおよび復元します。

    ```shell
    # Back up full data of the secondary cluster
    tiup br --pd http://172.16.6.124:2379 backup full --storage ./backup
    # Restore full data of the secondary cluster
    tiup br --pd http://172.16.6.123:2379 restore full --storage ./backup
    ```

3.  プライマリクラスタからセカンダリクラスタへデータをバックアップするための新しい変更フィードを作成します。

    ```shell
    # Create a changefeed
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary"
    ```

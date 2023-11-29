---
title: Replicate data between primary and secondary clusters
summary: Learn how to replicate data from a primary cluster to a secondary cluster.
---

# プライマリクラスタとセカンダリクラスタの間でデータをレプリケートする {#replicate-data-between-primary-and-secondary-clusters}

このドキュメントでは、TiDB プライマリ (アップストリーム) クラスターと TiDB または MySQL セカンダリ (ダウンストリーム) クラスターを構成し、プライマリ クラスターからセカンダリ クラスターに増分データをレプリケートする方法について説明します。このプロセスには次の手順が含まれます。

1.  TiDB プライマリ クラスターと TiDB または MySQL セカンダリ クラスターを構成します。
2.  増分データをプライマリ クラスタからセカンダリ クラスタにレプリケートします。
3.  プライマリ クラスターがダウンしたときに、REDO ログを使用してデータを一貫して復元します。

実行中の TiDB クラスターからそのセカンダリ クラスターに増分データをレプリケートするには、バックアップ &amp; リストア[BR](/br/backup-and-restore-overview.md)および[TiCDC](/ticdc/ticdc-overview.md)を使用できます。

## ステップ 1. 環境をセットアップする {#step-1-set-up-the-environment}

1.  TiDB クラスターをデプロイ。

    TiUP Playground を使用して、2 つの TiDB クラスター (1 つはアップストリーム、もう 1 つはダウンストリーム)をデプロイ。本番環境の場合は、 [TiUPを使用したオンライン TiDBクラスタのデプロイと管理](/tiup/tiup-cluster.md)を参照してクラスターをデプロイします。

    このドキュメントでは、2 つのクラスターを 2 台のマシンにデプロイします。

    -   ノード A: 172.16.6.123、アップストリーム TiDB クラスターの展開用

    -   ノード B: 172.16.6.124、ダウンストリーム TiDB クラスターの展開用

    ```shell
    # Create an upstream cluster on Node A
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster on Node B
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、新しくデプロイされたクラスターにテスト データベースが作成されます。したがって、 [システムベンチ](https://github.com/akopytov/sysbench#linux)を使用してテスト データを生成し、実際のシナリオでデータをシミュレートできます。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbench を使用して`oltp_write_only`スクリプトを実行します。このスクリプトは、それぞれ 10,000 行を含む 10 個のテーブルをアップストリーム データベースに生成します。 tidb-config は次のとおりです。

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

    実際のシナリオでは、サービス データは上流クラスターに継続的に書き込まれます。このドキュメントでは、sysbench を使用してこのワークロードをシミュレートします。具体的には、次のコマンドを実行して、10 人のワーカーが 3 つのテーブル sbtest1、sbtest2、および sbtest3 にデータを連続的に書き込みできるようにします。合計 TPS は 100 を超えません。

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部storageを準備します。

    フルデータバックアップでは、アップストリームクラスタとダウンストリームクラスタの両方がバックアップファイルにアクセスする必要があります。バックアップ ファイルを保存するには[外部storage](/br/backup-and-restore-storages.md)を使用することをお勧めします。この例では、Minio を使用して S3 互換storageサービスをシミュレートします。

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

    前述のコマンドは、S3 サービスをシミュレートするために 1 つのノード上で minioサーバーを起動します。コマンドのパラメータは次のように構成されます。

    -   エンドポイント: `http://${HOST_IP}:6060/`
    -   アクセスキー: `minio`
    -   シークレットアクセスキー: `miniostorage`
    -   バケツ: `redo`

    リンクは次のとおりです。

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ 2. 全データを移行する {#step-2-migrate-full-data}

環境をセットアップしたら、 [BR](https://github.com/pingcap/tidb/tree/master/br)のバックアップおよびリストア関数を使用して、完全なデータを移行できます。 BRは[三つの方法](/br/br-use-overview.md#deploy-and-use-br)で起動可能です。このドキュメントでは、SQL ステートメント`BACKUP`と`RESTORE`を使用します。

> **注記：**
>
> -   `BACKUP`と`RESTORE` SQL ステートメントは実験的ものです。本番環境でこれらを使用することはお勧めできません。予告なく変更または削除される場合がございます。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。
> -   本番クラスターでは、GC を無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響を与える可能性があります。パフォーマンスの低下を避けるために、オフピーク時間にデータをバックアップし、RATE_LIMIT を適切な値に設定することをお勧めします。
> -   上流クラスターと下流クラスターのバージョンが異なる場合は、 [BR互換性](/br/backup-and-restore-overview.md#some-tips)をチェックする必要があります。このドキュメントでは、アップストリーム クラスターとダウンストリーム クラスターが同じバージョンであると仮定します。

1.  GC を無効にします。

    新しく書き込まれたデータが増分移行中に削除されないようにするには、バックアップ前にアップストリーム クラスターの GC を無効にする必要があります。これにより、履歴データは削除されません。

    次のコマンドを実行して GC を無効にします。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効であることを確認するには、値`tidb_gc_enable`をクエリします。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

2.  バックアップデータ。

    アップストリーム クラスターで`BACKUP`ステートメントを実行してデータをバックアップします。

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    ```

        +----------------------+----------+--------------------+---------------------+---------------------+
        | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
        +----------------------+----------+--------------------+---------------------+---------------------+
        | local:///tmp/backup/ | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
        +----------------------+----------+--------------------+---------------------+---------------------+
        1 row in set (2.11 sec)

    `BACKUP`コマンドが実行されると、TiDB はバックアップ データに関するメタデータを返します。 `BackupTS`バックアップ前にデータが生成されるため注意してください。このドキュメントでは、**データ チェックの終了**および**TiCDC による増分移行スキャンの開始**として`BackupTS`を使用します。

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

    特定の時点で上流と下流の間のデータの整合性をチェックするには、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用します。前の`BACKUP`出力は、アップストリーム クラスターが 431434047157698561 でバックアップを終了したことを示しています。前の`RESTORE`の出力は、ダウンストリーム クラスターが 431434141450371074 で復元を終了したことを示しています。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の構成方法の詳細については、 [コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)を参照してください。このドキュメントでは、構成は次のようになります。

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

## ステップ 3. 増分データを移行する {#step-3-migrate-incremental-data}

1.  TiCDCをデプロイ。

    完全なデータ移行が完了したら、増分データを複製するように TiCDC を展開および構成します。本番環境では、 [TiCDCのデプロイ](/ticdc/deploy-ticdc.md)の指示に従って TiCDC をデプロイします。このドキュメントでは、テスト クラスターの作成時に TiCDC ノードが開始されています。したがって、TiCDC をデプロイするステップをスキップして、変更フィード構成に進みます。

2.  チェンジフィードを作成します。

    チェンジフィード構成ファイルを作成します`changefeed.toml` 。

    ```shell
    [consistent]
    # Consistency level, eventual means enabling consistent replication
    level = "eventual"
    # Use S3 to store redo logs. Other options are local and nfs.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.125:6060&force-path-style=true"
    ```

    上流クラスターで次のコマンドを実行して、上流クラスターから下流クラスターへの変更フィードを作成します。

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary" --start-ts="431434047157698561"
    ```

    このコマンドのパラメータは次のとおりです。

    -   `--server` : TiCDC クラスター内の任意のノードの IP アドレス
    -   `--sink-uri` : ダウンストリームクラスターのURI
    -   `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時間 (または[ステップ 2. 全データを移行する](#step-2-migrate-full-data)で説明した BackupTS) である必要があります。

    変更フィード構成の詳細については、 [TiCDC Changefeed構成](/ticdc/ticdc-changefeed-config.md)を参照してください。

3.  GC を有効にします。

    TiCDC を使用した増分移行では、GC はレプリケートされた履歴データのみを削除します。したがって、変更フィードを作成した後、次のコマンドを実行して GC を有効にする必要があります。詳細は[TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか?](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)を参照してください。

    GC を有効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効であることを確認するには、値`tidb_gc_enable`をクエリします。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

## ステップ 4. 上流クラスターでの災害のシミュレーション {#step-4-simulate-a-disaster-in-the-upstream-cluster}

アップストリーム クラスターの実行中に、そのクラスターで悲惨なイベントを作成します。たとえば、Ctrl+C を押すと、tiup プレイグラウンド プロセスを終了できます。

## ステップ 5. REDO ログを使用してデータの一貫性を確保する {#step-5-use-redo-log-to-ensure-data-consistency}

通常、TiCDC はトランザクションをダウンストリームに同時に書き込み、全体的に増加します。チェンジフィードが予期せず中断された場合、ダウンストリームにはアップストリームにあるような最新データが存在しない可能性があります。不一致に対処するには、次のコマンドを実行して、ダウンストリーム データがアップストリーム データと一貫していることを確認します。

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

-   `--storage` : S3 の REDO ログの場所と認証情報
-   `--tmp-dir` : S3からダウンロードしたREDOログのキャッシュディレクトリ
-   `--sink-uri` : ダウンストリームクラスターのURI

## ステップ 6. プライマリクラスターとそのサービスを回復する {#step-6-recover-the-primary-cluster-and-its-services}

前のステップの後、ダウンストリーム (セカンダリ) クラスターには、特定の時点でアップストリーム (プライマリ) クラスターと一致するデータが含まれます。データの信頼性を確保するには、新しいプライマリ クラスタとセカンダリ クラスタをセットアップする必要があります。

1.  新しい TiDB クラスターを新しいプライマリ クラスターとしてノード A にデプロイ。

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2.  BRを使用して、セカンダリ クラスタからプライマリ クラスタにデータを完全にバックアップおよび復元します。

    ```shell
    # Back up full data of the secondary cluster
    tiup br --pd http://172.16.6.124:2379 backup full --storage ./backup
    # Restore full data of the secondary cluster
    tiup br --pd http://172.16.6.123:2379 restore full --storage ./backup
    ```

3.  新しい変更フィードを作成して、プライマリ クラスターからセカンダリ クラスターにデータをバックアップします。

    ```shell
    # Create a changefeed
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary"
    ```

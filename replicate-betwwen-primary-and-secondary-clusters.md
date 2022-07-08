---
title: Replicate data between primary and secondary clusters
summary: Learn how to replicate data from a primary cluster to a secondary cluster.
---

# プライマリクラスターとセカンダリクラスター間でデータを複製する {#replicate-data-between-primary-and-secondary-clusters}

このドキュメントでは、TiDBプライマリ（アップストリーム）クラスタとTiDBまたはMySQLセカンダリ（ダウンストリーム）クラスタを構成し、プライマリクラスタからセカンダリクラスタに増分データをレプリケートする方法について説明します。このプロセスには、次の手順が含まれます。

1.  TiDBプライマリクラスタとTiDBまたはMySQLセカンダリクラスタを構成します。
2.  プライマリクラスタからセカンダリクラスタに増分データを複製します。
3.  プライマリクラスタがダウンしているときにREDOログを使用して、データを一貫して回復します。

実行中のTiDBクラスタからそのセカンダリクラスタに増分データを複製するには、バックアップと復元[BR](/br/backup-and-restore-overview.md)および[TiCDC](/ticdc/ticdc-overview.md)を使用できます。

## ステップ1.環境をセットアップします {#step-1-set-up-the-environment}

1.  TiDBクラスターをデプロイします。

    デプロイプレイグラウンドを使用して、2つのTiDBクラスターを1つはアップストリームに、もう1つはダウンストリームにデプロイします。実稼働環境の場合は、 [TiUPを使用したオンラインTiDBクラスターのデプロイと管理](/tiup/tiup-cluster.md)を参照してクラスターをデプロイします。

    このドキュメントでは、2つのクラスターを2つのマシンにデプロイします。

    -   ノードA：172.16.6.123、アップストリームTiDBクラスタをデプロイするため

    -   ノードB：172.16.6.124、ダウンストリームTiDBクラスタをデプロイするため

    {{< copyable "" >}}

    ```shell
    # Create an upstream cluster on Node A
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster on Node B
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、テストデータベースは新しくデプロイされたクラスターに作成されます。したがって、 [sysbench](https://github.com/akopytov/sysbench#linux)を使用してテストデータを生成し、実際のシナリオでデータをシミュレートできます。

    {{< copyable "" >}}

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbenchを使用して`oltp_write_only`のスクリプトを実行します。このスクリプトは、アップストリームデータベースにそれぞれ10,000行の10個のテーブルを生成します。 tidb-configは次のとおりです。

    {{< copyable "" >}}

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

    実際のシナリオでは、サービスデータはアップストリームクラスタに継続的に書き込まれます。このドキュメントでは、sysbenchを使用してこのワークロードをシミュレートします。具体的には、次のコマンドを実行して、10人のワーカーがsbtest1、sbtest2、およびsbtest3の3つのテーブルに、合計TPSが100を超えないようにデータを継続的に書き込むことができるようにします。

    {{< copyable "" >}}

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部ストレージを準備します。

    フルデータバックアップでは、アップストリームクラスターとダウンストリームクラスターの両方がバックアップファイルにアクセスする必要があります。バックアップファイルの保存には[外部記憶装置](/br/backup-and-restore-storages.md#external-storages)を使用することをお勧めします。この例では、Minioを使用してS3互換のストレージサービスをシミュレートしています。

    {{< copyable "" >}}

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

    上記のコマンドは、S3サービスをシミュレートするために1つのノードでminioサーバーを起動します。コマンドのパラメーターは次のように構成されます。

    -   エンドポイント： `http://${HOST_IP}:6060/`
    -   アクセスキー： `minio`
    -   シークレットアクセスキー： `miniostorage`
    -   バケット： `redo`

    リンクは次のとおりです。

    {{< copyable "" >}}

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ2.完全なデータを移行する {#step-2-migrate-full-data}

環境を設定した後、 [BR](https://github.com/pingcap/tidb/tree/master/br) ）のバックアップおよび復元機能を使用して完全なデータを移行できます。 BRは[3つの方法](/br/br-deployment.md#use-br)で開始できます。このドキュメントでは、SQLステートメント`BACKUP`および`RESTORE`を使用します。

> **ノート：**
>
> アップストリームクラスターとダウンストリームクラスターのバージョンが異なる場合は、 [BRの互換性](/br/backup-and-restore-overview.md#before-you-use-br)を確認する必要があります。このドキュメントでは、アップストリームクラスターとダウンストリームクラスターが同じバージョンであると想定しています。

1.  GCを無効にします。

    増分移行中に新しく書き込まれたデータが削除されないようにするには、バックアップの前にアップストリームクラスタのGCを無効にする必要があります。このように、履歴データは削除されません。

    {{< copyable "" >}}

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    Query OK, 0 rows affected (0.01 sec)
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

    > **ノート：**
    >
    > 本番クラスターでは、GCを無効にしてバックアップを実行すると、クラスタのパフォーマンスに影響を与える可能性があります。オフピーク時にデータをバックアップし、パフォーマンスの低下を防ぐためにRATE_LIMITを適切な値に設定することをお勧めします。

2.  バックアップデータ。

    アップストリームクラスタで`BACKUP`ステートメントを実行して、データをバックアップします。

    {{< copyable "" >}}

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | local:///tmp/backup/ | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
    +----------------------+----------+--------------------+---------------------+---------------------+
    1 row in set (2.11 sec)
    ```

    `BACKUP`コマンドが実行された後、TiDBはバックアップデータに関するメタデータを返します。データはバックアップされる前に生成されるため、 `BackupTS`に注意してください。このドキュメントでは**、データチェックの終了と**<strong>TiCDCによる増分移行スキャンの開始</strong>として`BackupTS`を使用します。

3.  データを復元します。

    ダウンストリームクラスタで`RESTORE`コマンドを実行して、データを復元します。

    {{< copyable "" >}}

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | local:///tmp/backup/ | 10315858 | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +----------------------+----------+--------------------+---------------------+---------------------+
    1 row in set (41.85 sec)
    ```

4.  （オプション）データを確認します。

    [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して、特定の時間におけるアップストリームとダウンストリーム間のデータの整合性を確認します。前の`BACKUP`の出力は、アップストリームクラスタが431434047157698561でバックアップを終了することを示しています。前の`RESTORE`の出力は、ダウンストリームが431434141450371074で復元を終了することを示しています。

    {{< copyable "" >}}

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspectorの構成方法の詳細については、 [Configuration / コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)を参照してください。このドキュメントでは、構成は次のとおりです。

    {{< copyable "" >}}

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

## ステップ3.増分データを移行する {#step-3-migrate-incremental-data}

1.  TiCDCをデプロイします。

    完全なデータ移行が完了したら、増分データを複製するようにTiCDCを展開および構成します。実稼働環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)の指示に従ってTiCDCをデプロイします。このドキュメントでは、テストクラスターの作成時にTiCDCノードが開始されています。したがって、TiCDCをデプロイするステップをスキップして、チェンジフィード構成に進みます。

2.  チェンジフィードを作成します。

    チェンジフィード構成ファイルを作成します`changefeed.toml` 。

    {{< copyable "" >}}

    ```shell
    [consistent]
    # Consistency level, eventual means enabling consistent replication
    level = "eventual"
    # Use S3 to store redo logs. Other options are local and nfs.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.125:6060&force-path-style=true"
    ```

    アップストリームクラスタで、次のコマンドを実行して、アップストリームクラスターからダウンストリームクラスターへのチェンジフィードを作成します。

    {{< copyable "" >}}

    ```shell
    tiup cdc cli changefeed create --pd=http://172.16.6.122:2379 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary" --start-ts="431434047157698561"
    ```

    このコマンドのパラメーターは次のとおりです。

    -   --pd：アップストリームクラスタのPDアドレス
    -   --sink-uri：ダウンストリームクラスタのURI
    -   --start-ts：チェンジフィードの開始タイムスタンプ。バックアップ時間（または[ステップ2.完全なデータを移行する](#step-2-migrate-full-data)で説明したBackupTS）である必要があります。

    チェンジフィード構成の詳細については、 [タスク構成ファイル](/ticdc/manage-ticdc.md#task-configuration-file)を参照してください。

3.  GCを有効にします。

    TiCDCを使用した増分移行では、GCは複製された履歴データのみを削除します。したがって、チェンジフィードを作成した後、次のコマンドを実行してGCを有効にする必要があります。詳細については、 [TiCDCガベージコレクション（GC）セーフポイントの完全な動作は何ですか？](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)を参照してください。

    {{< copyable "" >}}

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    Query OK, 0 rows affected (0.01 sec)
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

## ステップ4.アップストリームクラスタで災害をシミュレートする {#step-4-simulate-a-disaster-in-the-upstream-cluster}

実行中に、アップストリームクラスタに悲惨なイベントを作成します。たとえば、Ctrl + Cを押すと、tiupプレイグラウンドプロセスを終了できます。

## ステップ5.REDOログを使用して、データの整合性を確保します {#step-5-use-redo-log-to-ensure-data-consistency}

通常、TiCDCはトランザクションをダウンストリームに同時に書き込み、全体を増やします。チェンジフィードが予期せず中断された場合、ダウンストリームはアップストリームにあるため、最新のデータを持っていない可能性があります。不整合に対処するには、次のコマンドを実行して、ダウンストリームデータがアップストリームデータと整合していることを確認します。

{{< copyable "" >}}

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

-   --storage：S3のREDOログの場所とクレデンシャル
-   --tmp-dir：S3からダウンロードしたREDOログのキャッシュディレクトリ
-   --sink-uri：ダウンストリームクラスタのURI

## ステップ6.プライマリクラスタとそのサービスを回復する {#step-6-recover-the-primary-cluster-and-its-services}

前のステップの後、ダウンストリーム（セカンダリ）クラスタには、特定の時間にアップストリーム（プライマリ）クラスタと整合性のあるデータがあります。データの信頼性を確保するには、新しいプライマリクラスターとセカンダリクラスターを設定する必要があります。

1.  新しいプライマリクラスタとして、ノードAに新しいTiDBクラスタをデプロイします。

    {{< copyable "" >}}

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2.  BRを使用して、セカンダリクラスタからプライマリクラスタにデータを完全にバックアップおよび復元します。

    {{< copyable "" >}}

    ```shell
    # Back up full data of the secondary cluster
    tiup br --pd http://172.16.6.124:2379 backup full --storage ./backup
    # Restore full data of the secondary cluster
    tiup br --pd http://172.16.6.123:2379 restore full --storage ./backup
    ```

3.  新しいチェンジフィードを作成して、プライマリクラスタからセカンダリクラスタにデータをバックアップします。

    {{< copyable "" >}}

    ```shell
    # Create a changefeed
    tiup cdc cli changefeed create --pd=http://172.16.6.122:2379 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary"
    ```

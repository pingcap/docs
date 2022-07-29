---
title: Migrate from one TiDB cluster to another TiDB cluster
summary: Learn how to migrate data from one TiDB cluster to another TiDB cluster.
aliases: ['/tidb/v6.1/incremental-replication-between-clusters/']
---

# 1つのTiDBクラスターから別のTiDBクラスターに移行する {#migrate-from-one-tidb-cluster-to-another-tidb-cluster}

このドキュメントでは、あるTiDBクラスタから別のTiDBクラスタにデータを移行する方法について説明します。この機能は、次のシナリオに適用されます。

-   データベースの分割：TiDBクラスタが大きすぎる場合、またはクラスタのサービス間の影響を回避したい場合は、データベースを分割できます。
-   データベースの再配置：データセンターの変更など、データベースを物理的に再配置します。
-   新しいバージョンのTiDBクラスタへのデータの移行：データのセキュリティと精度の要件を満たすために、新しいバージョンのTiDBクラスタにデータを移行します。

このドキュメントは、移行プロセス全体の例であり、次の手順が含まれています。

1.  環境を設定します。

2.  完全なデータを移行します。

3.  増分データを移行します。

4.  サービスを新しいTiDBクラスタに切り替えます。

## ステップ1.環境をセットアップします {#step-1-set-up-the-environment}

1.  TiDBクラスターをデプロイします。

    デプロイプレイグラウンドを使用して、2つのTiDBクラスターを1つはアップストリームに、もう1つはダウンストリームにデプロイします。詳細については、 [TiUPを使用してオンラインTiDBクラスターをデプロイおよび管理する](/tiup/tiup-cluster.md)を参照してください。

    {{< copyable "" >}}

    ```shell
    # Create an upstream cluster
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

2.  データを初期化します。

    デフォルトでは、テストデータベースは新しくデプロイされたクラスターに作成されます。したがって、 [sysbench](https://github.com/akopytov/sysbench#linux)を使用してテストデータを生成し、実際のシナリオでデータをシミュレートできます。

    {{< copyable "" >}}

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    このドキュメントでは、sysbenchを使用して`oltp_write_only`のスクリプトを実行します。このスクリプトは、テストデータベースにそれぞれ10,000行の10個のテーブルを生成します。 tidb-configは次のとおりです。

    {{< copyable "" >}}

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

    実際のシナリオでは、サービスデータは継続的にアップストリームクラスタに書き込まれます。このドキュメントでは、sysbenchを使用してこのワークロードをシミュレートします。具体的には、次のコマンドを実行して、10人のワーカーがsbtest1、sbtest2、およびsbtest3の3つのテーブルに、合計TPSが100を超えないようにデータを継続的に書き込むことができるようにします。

    {{< copyable "" >}}

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4.  外部ストレージを準備します。

    フルデータバックアップでは、アップストリームクラスターとダウンストリームクラスターの両方がバックアップファイルにアクセスする必要があります。バックアップファイルの保存には[外部記憶装置](/br/backup-and-restore-storages.md)を使用することをお勧めします。このドキュメントでは、Minioを使用してS3互換のストレージサービスをシミュレートします。

    {{< copyable "" >}}

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

    上記のコマンドは、S3サービスをシミュレートするために1つのノードでminioサーバーを起動します。コマンドのパラメーターは次のように構成されます。

    -   エンドポイント： `http://${HOST_IP}:6060/`
    -   アクセスキー： `minio`
    -   シークレットアクセスキー： `miniostorage`
    -   バケット： `backup`

    アクセスリンクは次のとおりです。

    {{< copyable "" >}}

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## ステップ2.完全なデータを移行する {#step-2-migrate-full-data}

環境をセットアップした後、 [BR](https://github.com/pingcap/tidb/tree/master/br)のバックアップおよび復元関数を使用して、完全なデータを移行できます。 BRは[3つの方法](/br/br-deployment.md#use-br)で開始できます。このドキュメントでは、SQLステートメント`BACKUP`および`RESTORE`を使用します。

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
    +-------------------------+:
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
    +---------------+----------+--------------------+---------------------+---------------------+
    | Destination   | Size     | BackupTS           | Queue Time          | Execution Time      |
    +---------------+----------+--------------------+---------------------+---------------------+
    | s3://backup   | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
    +---------------+----------+--------------------+---------------------+---------------------+
    1 row in set (2.11 sec)
    ```

    `BACKUP`コマンドが実行された後、TiDBはバックアップデータに関するメタデータを返します。データはバックアップされる前に生成されるため、 `BackupTS`に注意してください。このドキュメントでは**、データチェックの終了と**<strong>TiCDCによる増分移行スキャンの開始</strong>として`BackupTS`を使用します。

3.  データを復元します。

    ダウンストリームクラスタで`RESTORE`コマンドを実行して、データを復元します。

    {{< copyable "" >}}

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    +--------------+-----------+--------------------+---------------------+---------------------+
    | Destination  | Size      | BackupTS           | Queue Time          | Execution Time      |
    +--------------+-----------+--------------------+---------------------+---------------------+
    | s3://backup  | 10315858  | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +--------------+-----------+--------------------+---------------------+---------------------+
    1 row in set (41.85 sec)
    ```

4.  （オプション）データを確認します。

    [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して、特定の時間におけるアップストリームとダウンストリーム間のデータの整合性を確認できます。前の`BACKUP`の出力は、アップストリームクラスタが431434047157698561でバックアップを終了することを示しています。前の`RESTORE`の出力は、ダウンストリームが431434141450371074で復元を終了することを示しています。

    {{< copyable "" >}}

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspectorの構成方法の詳細については、 [Configuration / コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)を参照してください。このドキュメントでは、構成は次のとおりです。

    {{< copyable "" >}}

    ```shell
    # Diff Configuration.
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
        host = "172.16.6.122" # Replace the value with the IP address of your upstream cluster
        port = 4000
        user = "root"
        password = ""
        snapshot = "431434047157698561" # Set snapshot to the actual backup time (see BackupTS in the previous step)
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

## ステップ3.増分データを移行する {#step-3-migrate-incremental-data}

1.  TiCDCをデプロイします。

    完全なデータ移行が完了したら、増分データを複製するようにTiCDCを展開および構成します。実稼働環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)の指示に従ってTiCDCをデプロイします。このドキュメントでは、テストクラスターの作成時にTiCDCノードが開始されています。したがって、TiCDCをデプロイするステップをスキップして、チェンジフィード構成に進むことができます。

2.  チェンジフィードを作成します。

    アップストリームクラスタで、次のコマンドを実行して、アップストリームクラスターからダウンストリームクラスターへのチェンジフィードを作成します。

    {{< copyable "" >}}

    ```shell
    tiup cdc cli changefeed create --pd=http://172.16.6.122:2379 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="upstream-to-downstream" --start-ts="431434047157698561"
    ```

    このコマンドのパラメーターは次のとおりです。

    -   --pd：アップストリームクラスタのPDアドレス
    -   --sink-uri：ダウンストリームクラスタのURI
    -   --changefeed-id：changefeed ID、正規表現の形式である必要があります^ [a-zA-Z0-9] +（-[a-zA-Z0-9] +）* $
    -   --start-ts：チェンジフィードの開始タイムスタンプ。バックアップ時間（または前の手順で説明したBackupTS）である必要があります。

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

## ステップ4.サービスを新しいTiDBクラスタに切り替えます {#step-4-switch-services-to-the-new-tidb-cluster}

チェンジフィードを作成した後、アップストリームクラスターに書き込まれたデータは、低レイテンシでダウンストリームクラスタに複製されクラスタ。読み取りストリームをダウンストリームクラスタに段階的に移行できます。期間を守ってください。ダウンストリームクラスタが安定している場合は、書き込みストリームをダウンストリームクラスタに切り替えることもできます。これには次の3つの手順が含まれる場合があります。

1.  アップストリームクラスタで書き込みサービスを停止します。チェンジフィードを停止する前に、すべてのアップストリームデータがダウンストリームに複製されていることを確認してください。

    {{< copyable "" >}}

    ```shell
    # Stop the changefeed from the upstream cluster to the downstream cluster
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --pd=http://172.16.6.122:2379

    # View the changefeed status
    tiup cdc cli changefeed list
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
    ```

2.  ダウンストリームからアップストリームへのチェンジフィードを作成します。アップストリームとダウンストリームのデータは一貫しており、クラスタに新しいデータが書き込まれないため、デフォルト設定を使用するために`start-ts`を未指定のままにしておくことができます。

    {{< copyable "" >}}

    ```shell
    tiup cdc cli changefeed create --pd=http://172.16.6.125:2379 --sink-uri="mysql://root:@172.16.6.122:4000" --changefeed-id="downstream -to-upstream"
    ```

3.  書き込みサービスをダウンストリームクラスタに移行した後、しばらく観察します。ダウンストリームクラスタが安定している場合は、アップストリームクラスタを終了できます。

---
title: Migrate Large Datasets from MySQL to TiDB
summary: MySQLからTiDBへ大規模データセットを移行する方法を学びましょう。
---

# MySQLからTiDBへの大規模データセットの移行 {#migrate-large-datasets-from-mysql-to-tidb}

移行するデータ量が少ない場合は、完全移行と増分レプリケーションの両方で、 [DMを使用してデータを移行する](/migrate-small-mysql-to-tidb.md)簡単にできます。ただし、DM はデータのインポート速度が遅い (30 ～ 50 GiB/h) ため、データ量が多い場合、移行に時間がかかることがあります。このドキュメントにおける「大規模なデータセット」とは、通常、約 1 TiB 以上のデータを意味します。

このドキュメントでは、 DumplingとTiDB Lightningを使用してフルマイグレーションを実行する方法について説明します。TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)では、最大500 GiB/hの速度でデータをインポートできます。ただし、この速度はハードウェア構成、テーブルスキーマ、インデックス数など、さまざまな要因によって影響を受けることに注意してください。フルマイグレーションが完了したら、DMを使用して増分データをレプリケートできます。

## 前提条件 {#prerequisites}

-   [DMをインストール](/dm/deploy-a-dm-cluster-using-tiup.md)。
-   [DumplingとTiDB Lightningをインストールする](/migration-tools.md)。
-   [DMに必要なソースデータベースとターゲットデータベースの権限を付与します](/dm/dm-worker-intro.md)
-   [TiDB Lightningに必要なターゲットデータベース権限を付与します](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)
-   [Dumplingに必要なソースデータベース権限を付与する](/dumpling-overview.md#export-data-from-tidb-or-mysql)。

## リソース要件 {#resource-requirements}

**オペレーティングシステム**: このドキュメントの例では、新規の CentOS 7 インスタンスを使用しています。仮想マシンは、ローカル ホストまたはクラウドにデプロイできます。TiDB Lightning はデフォルトで必要なだけの CPU リソースを消費するため、専用サーバーにデプロイすることをお勧めします。それが不可能な場合は、他の TiDB コンポーネント (たとえば`tikv-server` ) と一緒に単一のサーバーにデプロイし、 `region-concurrency`を構成して、 TiDB Lightningの CPU 使用率を制限できます。通常、論理 CPU の 75% にサイズを設定できます。

**メモリとCPU** ： TiDB Lightningは多くのリソースを消費するため、64 GiB以上のメモリと32以上のCPUコアを割り当てることを推奨します。最高のパフォーマンスを得るには、CPUコアとメモリ（GiB）の比率が1:2以上であることを確認してください。

**ディスク容量**：

-   Dumplingには、データソース全体を保存できる（またはエクスポートされるすべての上流テーブルを保存できる）ディスク容量が必要です。SSD推奨です。必要なスペースを計算するには、 [ターゲットデータベースのストレージ要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)を参照してください。
-   インポート処理中、 TiDB Lightningはソート済みのキーと値のペアを保存するための一時的な領域を必要とします。ディスク容量は、データソースの最大の単一テーブルを格納できるのに十分な量が必要です。
-   データ総量が大きい場合は、上流側のbinlogの保存期間を延長することができます。これは、増分レプリケーション中にバイナリログが失われないようにするためです。

**注**： DumplingによってMySQLからエクスポートされる正確なデータ量を計算することは困難ですが、次のSQLステートメントを使用して`information_schema.tables`テーブルの`DATA_LENGTH`フィールドを要約することで、データ量を推定できます。

```sql
-- Calculate the size of all schemas
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- Calculate the 5 largest tables
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```

### ターゲットとなるTiKVクラスターのディスク容量 {#disk-space-for-the-target-tikv-cluster}

ターゲットの TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。[標準ハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲットの TiKV クラスターのストレージ容量は**、データソースのサイズ × <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカ数</a>× 2**よりも大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲットの TiKV クラスターは、データソースのサイズの 6 倍よりも大きなストレージ容量が必要です。この式に`x 2`が含まれている理由は次のとおりです。

-   インデックスには余分な容量が必要になる場合があります。
-   RocksDBには空間増幅がある。

## ステップ1. MySQLからすべてのデータをエクスポートする {#step-1-export-all-data-from-mysql}

1.  以下のコマンドを実行して、MySQLからすべてのデータをエクスポートします。

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup'
    ```

    DumplingはデフォルトでデータをSQLファイルにエクスポートします。 `--filetype`オプションを追加することで、別のファイル形式を指定できます。

    上記で使用したパラメータは以下のとおりです。 Dumplingパラメータの詳細については、 [Dumplingの概要](/dumpling-overview.md)を参照してください。

    | パラメータ                | 説明                                                                                  |
    | -------------------- | ----------------------------------------------------------------------------------- |
    | `-u`または`--user`      | MySQLユーザー                                                                           |
    | `-p`または`--password`  | MySQLユーザーのパスワード                                                                     |
    | `-P`または`--port`      | MySQLポート                                                                            |
    | `-h`または`--host`      | MySQLのIPアドレス                                                                        |
    | `-t`または`--thread`    | エクスポートに使用されるスレッド数                                                                   |
    | `-o`または`--output`    | エクスポートされたファイルを保存するディレクトリ。ローカルパスまたは[外部ストレージURI](/external-storage-uri.md)をサポートします。 |
    | `-r`または`--row`       | 単一ファイル内の最大行数                                                                        |
    | `-F`                 | 単一ファイルの最大サイズ（MiB単位）。推奨値：256 MiB。                                                    |
    | - `B`または`--database` | エクスポートするデータベースを指定します。                                                               |
    | `-f`または`--filter`    | パターンに一致するテーブルをエクスポートします。構文については[テーブルフィルター](/table-filter.md)を参照してください。              |

    `${data-path}`には、エクスポートされたすべての上流テーブルを保存するのに十分な空き容量があることを確認してください。必要な容量を計算するには、 [ターゲットデータベースのストレージ要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)を参照してください。大きなテーブルがすべてのスペースを消費してエクスポートが中断されるのを防ぐため、 `-F`オプションを使用して単一ファイルのサイズを制限することを強くお勧めします。

2.  `${data-path}`ディレクトリにある`metadata`ファイルを確認します。これは、Dumpling によって生成されたメタデータ ファイルです。ステップ 3 の増分レプリケーションに必要なbinlogの位置情報を記録します。

        SHOW MASTER STATUS:
        Log: mysql-bin.000004
        Pos: 109227
        GTID:

## ステップ2. TiDBに全データをインポートする {#step-2-import-full-data-to-tidb}

1.  `tidb-lightning.toml`設定ファイルを作成します。

    ```toml
    [lightning]
    # log.
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
    # "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally. For more information on the backends, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.
    backend = "local"
    # Sets the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # The data source directory. The same directory where Dumpling exports data in "Step 1. Export all data from MySQL".
    data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup'.

    [tidb]
    # The target TiDB cluster information.
    host = "${host}"              # e.g.: 172.16.32.1
    port = "${port}"                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = "${status-port}"  # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
    pd-addr = "${ip}:${port}"     # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    TiDB Lightning構成の詳細については、 [TiDB Lightning のコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

2.  `tidb-lightning`を実行してインポートを開始します。コマンドラインでプログラムを直接起動すると、SIGHUP シグナルを受信した後にプロセスが予期せず終了する可能性があります。 `nohup`を使用してコマンドラインからプロセスを直接起動することは推奨されません。代わりに、次のスクリプトの内容を編集してください。例:

    S3 からデータをインポートする場合は、S3ストレージパスにアクセスできる SecretKey と AccessKey を環境変数としてTiDB Lightningノードに渡してください。また、 `~/.aws/credentials`から認証情報を読み取ることもできます。

    ```shell
    #!/bin/bash
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

    次に、スクリプトを使用してTiDB Lightning を起動します。

3.  インポートが開始された後、以下のいずれかの方法でインポートの進行状況を確認できます。

    -   ログ内のキーワード`progress`を`grep`することで、インポートの進行状況を確認できます。進行状況は、デフォルトでは 5 分ごとに更新されます。
    -   [モニタリングダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。

4.  TiDB Lightning はインポートが完了すると自動的に終了します。`tidb-lightning.log`の最後の行に`the whole procedure completed`が含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポート中にエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **Note:**
>
> インポートが成功したかどうかに関わらず、ログの最後の行には`tidb lightning exit`と表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するものではありません。

インポートが失敗した場合は、トラブルシューティングのために[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## ステップ3. 増分データをTiDBに複製する {#step-3-replicate-incremental-data-to-tidb}

### データソースを追加する {#add-the-data-source}

1.  `source1.yaml`ファイルを作成します。

    ```yaml
    # Must be unique.
    source-id: "mysql-01"

    # Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
    enable-gtid: true

    from:
      host: "${host}"           # e.g.: 172.16.10.81
      user: "root"
      password: "${password}"   # Supported but not recommended to use a plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2.  次のコマンドを実行して、 `tiup dmctl`を使用してデータソース構成を DM クラスターにロードします。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    上記のコマンドで使用されるパラメータは、以下のように説明されます。

    | パラメータ                   | 説明                                                                          |
    | ----------------------- | --------------------------------------------------------------------------- |
    | `--master-addr`         | `{advertise-addr}`が接続されるクラスタ内の任意の DM-master の`dmctl` (例: 172.16.10.71:8261) |
    | `operate-source create` | データソースをDMクラスターにロードします。                                                      |

### レプリケーションタスクを追加する {#add-a-replication-task}

1.  `task.yaml`ファイルを編集します。増分レプリケーションモードと各データソースの開始点を設定します。

    ```yaml
    name: task-test                      # Task name. Must be globally unique.
    task-mode: incremental               # Task mode. The "incremental" mode only performs incremental data replication.

    # Configures the target TiDB database.
    target-database:                     # The target database instance.
      host: "${host}"                    # e.g.: 127.0.0.1
      port: 4000
      user: "root"
      password: "${password}"            # It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

    # Use block and allow lists to specify the tables to be replicated.
    block-allow-list:                    # The collection of filtering rules that matches the tables in the source database instance. If the DM version is earlier than v2.0.0-beta.2, use black-white-list.
      bw-rule-1:                         # The block-allow-list configuration item ID.
        do-dbs: ["${db-name}"]           # Name of databases to be replicated.

    # Configures the data source.
    mysql-instances:
      - source-id: "mysql-01"            # Data source ID, i.e., source-id in source1.yaml
        block-allow-list: "bw-rule-1"    # You can use the block-allow-list configuration above.
        # syncer-config-name: "global"    # You can use the syncers incremental data configuration below.
        meta:                            # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.
          # binlog-name: "mysql-bin.000004"  # The binlog position recorded in "Step 1. Export all data from MySQL". If the upstream database service is configured to switch master between different nodes automatically, GTID mode is required.
          # binlog-pos: 109227
          binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

    # (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
    # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    # syncers:            # The running configurations of the sync processing unit.
    #   global:           # Configuration name.
    #     safe-mode: true # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
    ```

    上記の YAML は、移行タスクに必要な最小構成です。その他の設定項目については、 [DM 高度タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

    移行作業を開始する前に、エラーの可能性を減らすため、 `check-task`コマンドを実行して、構成が DM の要件を満たしていることを確認することをお勧めします。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
    ```

2.  以下のコマンドを実行して、移行タスクを開始します。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
    ```

    上記のコマンドで使用されるパラメータは、以下のように説明されます。

    | パラメータ           | 説明                                                                       |
    | --------------- | ------------------------------------------------------------------------ |
    | `--master-addr` | `dmctl`が接続されるクラスタ内の任意の DM-master の {advertise-addr}。例: 172.16.10.71:8261 |
    | `start-task`    | 移行タスクを開始します。                                                             |

    タスクの開始に失敗した場合は、プロンプトメッセージを確認し、設定を修正してください。その後、上記のコマンドを再度実行してタスクを開始できます。

    問題が発生した場合は、 [DMエラー処理](/dm/dm-error-handling.md)および[DMに関するFAQ](/dm/dm-faq.md)を参照してください。

### 移行タスクのステータスを確認します {#check-the-migration-task-status}

DM クラスターで進行中の移行タスクがあるかどうかを確認し、タスクの状態を表示するには、 `query-status`を使用して`tiup dmctl`コマンドを実行します。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、[クエリステータス](/dm/dm-query-status.md)を参照してください。

### タスクを監視し、ログを表示する {#monitor-the-task-and-view-logs}

移行タスクの履歴ステータスやその他の内部指標を確認するには、以下の手順に従ってください。

TiUPを使用してDMをデプロイした際に、Prometheus、Alertmanager、およびGrafanaもデプロイしている場合は、デプロイ時に指定したIPアドレスとポートを使用してGrafanaにアクセスできます。その後、DMダッシュボードを選択して、DM関連の監視メトリクスを表示できます。

DMが実行されている間、DM-worker、DM-master、およびdmctlは関連情報をログに出力します。これらのコンポーネントのログディレクトリは以下のとおりです。

-   DM-master: DM-master プロセス パラメータ`--log-file`で指定されます。TiUPを使用して DM をデプロイする場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-master-8261/log/`になります。
-   DM-worker: DM-worker プロセス パラメータ`--log-file`で指定されます。TiUPを使用して DM をデプロイする場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-worker-8262/log/`になります。

## 次は？ {#what-s-next}

-   [データ移行タスクを一時停止する](/dm/dm-pause-task.md)
-   [データ移行タスクを再開する](/dm/dm-resume-task.md)
-   [データ移行タスクを停止する](/dm/dm-stop-task.md)
-   [クラスターのデータソースのエクスポートとインポート、およびタスクコンフィグレーション](/dm/dm-export-import-config.md)
-   [失敗したDDLステートメントを処理する](/dm/handle-failed-ddl-statements.md)

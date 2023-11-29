---
title: Migrate Large Datasets from MySQL to TiDB
summary: Learn how to migrate large datasets from MySQL to TiDB.
---

# 大規模なデータセットを MySQL から TiDB に移行する {#migrate-large-datasets-from-mysql-to-tidb}

移行するデータのボリュームが小さい場合は、完全な移行と増分レプリケーションの[DM を使用してデータを移行する](/migrate-small-mysql-to-tidb.md)を簡単に行うことができます。ただし、DM はデータのインポート速度が遅い (30 ～ 50 GiB/h) ため、データ量が多い場合、移行に時間がかかることがあります。このドキュメントにおける「大規模なデータセット」とは、通常、約 1 TiB 以上のデータを意味します。

このドキュメントでは、 DumplingとTiDB Lightningを使用して完全な移行を実行する方法について説明します。 TiDB Lightning [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)最大 500 GiB/h の速度でデータをインポートできます。この速度は、ハードウェア構成、テーブル スキーマ、インデックスの数などのさまざまな要因の影響を受けることに注意してください。完全な移行が完了したら、DM を使用して増分データをレプリケートできます。

## 前提条件 {#prerequisites}

-   [DMをインストールする](/dm/deploy-a-dm-cluster-using-tiup.md) 。
-   [DumplingとTiDB Lightningをインストールする](/migration-tools.md) 。
-   [DMに必要なソース・データベースとターゲット・データベースの権限を付与します。](/dm/dm-worker-intro.md) 。
-   [TiDB Lightningに必要なターゲット データベース権限を付与します。](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database) 。
-   [Dumplingに必要なソース データベース権限を付与します。](/dumpling-overview.md#export-data-from-tidb-or-mysql) 。

## リソース要件 {#resource-requirements}

**オペレーティング システム**: このドキュメントの例では、新しい CentOS 7 インスタンスを使用しています。仮想マシンはローカル ホストまたはクラウドにデプロイできます。 TiDB Lightning はデフォルトで必要なだけの CPU リソースを消費するため、専用サーバーに展開することをお勧めします。これが不可能な場合は、他の TiDB コンポーネント (たとえば`tikv-server` ) とともに単一サーバーにデプロイし、 TiDB Lightningからの CPU 使用率を制限するように`region-concurrency`を構成できます。通常、サイズは論理 CPU の 75% に構成できます。

**メモリと CPU** : TiDB Lightning は大量のリソースを消費するため、64 GiB 以上のメモリと 32 以上の CPU コアを割り当てることをお勧めします。最高のパフォーマンスを得るには、CPU コアとメモリ(GiB) の比率が 1:2 より大きいことを確認してください。

**ディスクスペース**：

-   Dumplingには、データ ソース全体を保存できる (またはエクスポートされるすべてのアップストリーム テーブルを保存できる) ディスク容量が必要です。 SSD推奨です。必要なスペースを計算するには、 [ダウンストリームのstorageスペース要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)を参照してください。
-   インポート中、 TiDB Lightning はソートされたキーと値のペアを保存するための一時スペースを必要とします。ディスク容量は、データ ソースからの最大の単一テーブルを保持するのに十分である必要があります。
-   全データのボリュームが大きい場合は、アップストリームでのbinlogのstorage時間を増やすことができます。これは、増分レプリケーション中にバイナリログが失われないようにするためです。

**注**: Dumplingによって MySQL からエクスポートされる正確なデータ量を計算することは困難ですが、次の SQL ステートメントを使用してテーブル`information_schema.tables`の`DATA_LENGTH`フィールドを要約することで、データ量を見積もることができます。

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

### ターゲット TiKV クラスターのディスク容量 {#disk-space-for-the-target-tikv-cluster}

ターゲット TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。ターゲット TiKV クラスターのstorage容量は、 [標準的なハードウェア要件](/hardware-and-software-requirements.md)に加えて、**データ ソースのサイズ x <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカの数</a>x 2**より大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターにはデータ ソースのサイズの 6 倍を超えるstorageスペースが必要です。この式に`x 2`含まれるのは、次の理由からです。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDB には空間増幅効果があります。

## ステップ 1. MySQL からすべてのデータをエクスポートする {#step-1-export-all-data-from-mysql}

1.  次のコマンドを実行して、MySQL からすべてのデータをエクスポートします。

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup'
    ```

    Dumpling は、デフォルトでデータを SQL ファイルにエクスポートします。 `--filetype`オプションを追加すると、別のファイル形式を指定できます。

    上記で使用したパラメータは以下のとおりです。 Dumplingパラメータの詳細については、 [Dumplingの概要](/dumpling-overview.md)を参照してください。

    | パラメーター               | 説明                                                                                  |
    | -------------------- | ----------------------------------------------------------------------------------- |
    | `-u`または`--user`      | MySQLユーザー                                                                           |
    | `-p`または`--password`  | MySQLユーザーのパスワード                                                                     |
    | `-P`または`--port`      | MySQLポート                                                                            |
    | `-h`または`--host`      | MySQLのIPアドレス                                                                        |
    | `-t`または`--thread`    | エクスポートに使用されるスレッドの数                                                                  |
    | `-o`または`--output`    | エクスポートされたファイルを保存するディレクトリ。ローカル パスまたは[外部storageURI](/external-storage-uri.md)をサポートします |
    | `-r`または`--row`       | 1 つのファイル内の最大行数                                                                      |
    | `-F`                 | 単一ファイルの最大サイズ (MiB 単位)。推奨値: 256 MiB。                                                 |
    | - `B`または`--database` | エクスポートするデータベースを指定します                                                                |
    | `-f`または`--filter`    | パターンに一致するテーブルをエクスポートします。構文については[テーブルフィルター](/table-filter.md)を参照してください。              |

    `${data-path}`エクスポートされたすべてのアップストリーム テーブルを保存するためのスペースがあることを確認してください。必要なスペースを計算するには、 [ダウンストリームのstorageスペース要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)を参照してください。大きなテーブルがすべてのスペースを消費してエクスポートが中断されないようにするには、 `-F`オプションを使用して 1 つのファイルのサイズを制限することを強くお勧めします。

2.  `${data-path}`ディレクトリ内の`metadata`ファイルをビュー。これは、Dumpling によって生成されたメタデータ ファイルです。ステップ 3 の増分レプリケーションに必要なbinlogの位置情報を記録します。

        SHOW MASTER STATUS:
        Log: mysql-bin.000004
        Pos: 109227
        GTID:

## ステップ 2. 完全なデータを TiDB にインポートする {#step-2-import-full-data-to-tidb}

1.  `tidb-lightning.toml`構成ファイルを作成します。

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
    host = ${host}                # e.g.: 172.16.32.1
    port = ${port}                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = ${status-port}  # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
    pd-addr = "${ip}:${port}"     # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    TiDB Lightning構成の詳細については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

2.  `tidb-lightning`を実行してインポートを開始します。コマンド ラインでプログラムを直接起動すると、SIGHUP シグナルの受信後にプロセスが予期せず終了する可能性があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例えば：

    S3 からデータをインポートする場合は、S3storageパスにアクセスできる SecretKey と AccessKey を環境変数としてTiDB Lightningノードに渡します。 `~/.aws/credentials`から資格情報を読み取ることもできます。

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  インポートの開始後、次のいずれかの方法でインポートの進行状況を確認できます。

    -   `grep`ログ内のキーワード`progress` 。デフォルトでは、進行状況は 5 分ごとに更新されます。
    -   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。
    -   [TiDB Lightning Web インターフェース](/tidb-lightning/tidb-lightning-web-interface.md)で進捗状況を確認します。

4.  TiDB Lightning はインポートを完了すると、自動的に終了します。最後の行に`tidb-lightning.log` `the whole procedure completed`含まれているかどうかを確認します。 「はい」の場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処します。

> **注記：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、インポートが成功したことを必ずしも意味するわけではありません。

インポートが失敗した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)のトラブルシューティングを参照してください。

## ステップ 3. 増分データを TiDB にレプリケートする {#step-3-replicate-incremental-data-to-tidb}

### データソースを追加する {#add-the-data-source}

1.  次のように`source1.yaml`ファイルを作成します。

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

2.  次のコマンドを実行して、 `tiup dmctl`を使用してデータ ソース構成を DM クラスターにロードします。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    上記のコマンドで使用されるパラメータは次のように説明されます。

    | パラメータ                   | 説明                                                                      |
    | ----------------------- | ----------------------------------------------------------------------- |
    | `--master-addr`         | `dmctl`が接続されるクラスタ内の任意の DM マスターの`{advertise-addr}` 、例: 172.16.10.71:8261 |
    | `operate-source create` | データ ソースを DM クラスターにロードします。                                               |

### レプリケーションタスクを追加する {#add-a-replication-task}

1.  `task.yaml`ファイルを編集します。増分レプリケーション モードと各データ ソースの開始点を構成します。

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

    上記の YAML は、移行タスクに必要な最小構成です。その他の設定項目については、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

    移行タスクを開始する前に、エラーの可能性を減らすために、 `check-task`コマンドを実行して構成が DM の要件を満たしていることを確認することをお勧めします。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
    ```

2.  次のコマンドを実行して、移行タスクを開始します。

    ```shell
    tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
    ```

    上記のコマンドで使用されるパラメータは次のように説明されます。

    | パラメータ           | 説明                                                                    |
    | --------------- | --------------------------------------------------------------------- |
    | `--master-addr` | `dmctl`が接続されるクラスタ内の任意の DM マスターの {advertise-addr}、例: 172.16.10.71:8261 |
    | `start-task`    | 移行タスクを開始します。                                                          |

    タスクの開始に失敗した場合は、プロンプト メッセージを確認して構成を修正します。その後、上記のコマンドを再実行してタスクを開始できます。

    問題が発生した場合は、 [DMエラー処理](/dm/dm-error-handling.md)と[DMに関するFAQ](/dm/dm-faq.md)を参照してください。

### 移行タスクのステータスを確認する {#check-the-migration-task-status}

DM クラスターに進行中の移行タスクがあるかどうかを確認し、タスクのステータスを表示するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、 [クエリステータス](/dm/dm-query-status.md)を参照してください。

### タスクを監視し、ログを表示する {#monitor-the-task-and-view-logs}

移行タスクの履歴ステータスとその他の内部メトリックを表示するには、次の手順を実行します。

TiUPを使用して DM をデプロイしたときに Prometheus、Alertmanager、および Grafana をデプロイしている場合は、デプロイ中に指定された IP アドレスとポートを使用して Grafana にアクセスできます。次に、DM ダッシュボードを選択して、DM 関連の監視メトリックを表示できます。

DM の実行中、DM-worker、DM-master、および dmctl は関連情報をログに出力します。これらのコンポーネントのログ ディレクトリは次のとおりです。

-   DM マスター: DM マスター プロセス パラメーター`--log-file`によって指定されます。 TiUPを使用して DM をデプロイする場合、ログ ディレクトリはデフォルトで`/dm-deploy/dm-master-8261/log/`です。
-   DM-worker: DM-worker プロセス パラメーター`--log-file`によって指定されます。 TiUPを使用して DM をデプロイする場合、デフォルトのログ ディレクトリは`/dm-deploy/dm-worker-8262/log/`です。

## 次は何ですか {#what-s-next}

-   [データ移行タスクを一時停止する](/dm/dm-pause-task.md)
-   [データ移行タスクを再開する](/dm/dm-resume-task.md)
-   [データ移行タスクの停止](/dm/dm-stop-task.md)
-   [データソースのエクスポートとインポート、およびクラスターのタスクコンフィグレーション](/dm/dm-export-import-config.md)
-   [失敗した DDL ステートメントの処理](/dm/handle-failed-ddl-statements.md)

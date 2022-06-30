---
title: Migrate MySQL of Large Datasets to TiDB
summary: Learn how to migrate MySQL of large datasets to TiDB.
---

# 大規模なデータセットのMySQLをTiDBに移行する {#migrate-mysql-of-large-datasets-to-tidb}

移行するデータ量が少ない場合は、完全移行とインクリメンタルレプリケーションの両方で簡単に[DMを使用してデータを移行する](/migrate-small-mysql-to-tidb.md)を実行できます。ただし、DMは低速（30〜50 GiB / h）でデータをインポートするため、データ量が多い場合は移行に時間がかかる場合があります。このドキュメントの「大規模なデータセット」とは、通常、1TiB以上のデータを意味します。

このドキュメントでは、大規模なデータセットをMySQLからTiDBに移行する方法について説明します。移行全体には2つのプロセスがあります。

1.  *完全な移行*。 DumplingとTiDBLightningを使用して、完全な移行を実行します。 TiDB Lightningの**ローカルバックエンド**モードでは、最大500 GiB/hの速度でデータをインポートできます。
2.  *インクリメンタルレプリケーション*。完全な移行が完了したら、DMを使用して増分データを複製できます。

## 前提条件 {#prerequisites}

-   [DMをインストールする](/dm/deploy-a-dm-cluster-using-tiup.md) 。
-   [DumplingとTiDBLightningをインストールします](/migration-tools.md) 。
-   [DMに必要なソースデータベースとターゲットデータベースの権限を付与します](/dm/dm-worker-intro.md) 。
-   [TiDBLightningに必要なターゲットデータベース権限を付与します](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database) 。
-   [Dumplingに必要なソースデータベース権限を付与します](/dumpling-overview.md#export-data-from-tidbmysql) 。

## リソース要件 {#resource-requirements}

**オペレーティングシステム**：このドキュメントの例では、新しいCentOS7インスタンスを使用しています。仮想マシンは、ローカルホストまたはクラウドのいずれかにデプロイできます。 TiDB Lightningはデフォルトで必要なだけのCPUリソースを消費するため、専用サーバーにデプロイすることをお勧めします。これが不可能な場合は、他のTiDBコンポーネント（たとえば`tikv-server` ）と一緒に単一のサーバーにデプロイしてから、TiDBLightningからのCPU使用率を制限するように`region-concurrency`を構成できます。通常、サイズは論理CPUの75％に設定できます。

**メモリとCPU** ：TiDB Lightningは大量のリソースを消費するため、64GiBを超えるメモリと32を超えるCPUコアを割り当てることをお勧めします。最高のパフォーマンスを得るには、CPUコアとメモリ（GiB）の比率が1：2より大きいことを確認してください。

**ディスク容量**：

-   Dumplingには、データソース全体を格納できる（またはエクスポートするすべてのアップストリームテーブルを格納できる）ディスクスペースが必要です。 SSDをお勧めします。
-   インポート中、TiDB Lightningには、ソートされたキーと値のペアを格納するための一時的なスペースが必要です。ディスク容量は、データソースからの最大の単一テーブルを保持するのに十分である必要があります。
-   フルデータボリュームが大きい場合は、アップストリームでのbinlogストレージ時間を増やすことができます。これは、インクリメンタルレプリケーション中にbinlogが失われないようにするためです。

**注**：MySQLからDumplingによってエクスポートされた正確なデータ量を計算することは困難ですが、次のSQLステートメントを使用して`information_schema.tables`テーブルの`data-length`フィールドを要約することにより、データ量を見積もることができます。

{{< copyable "" >}}

```sql
/* Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;

/* Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_name,table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM from information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY SUM DESC LIMIT 5;
```

### ターゲットTiKVクラスタのディスク容量 {#disk-space-for-the-target-tikv-cluster}

ターゲットTiKVクラスタには、インポートされたデータを格納するのに十分なディスク容量が必要です。 [標準のハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲットTiKVクラスタのストレージスペースは**、データソースのサイズx <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカの数</a>x2**よりも大きくする必要があります。たとえば、クラスタがデフォルトで3つのレプリカを使用する場合、ターゲットTiKVクラスタには、データソースのサイズの6倍を超えるストレージスペースが必要です。数式には`x 2`あります。理由は次のとおりです。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDBにはスペース増幅効果があります。

## ステップ1.MySQLからすべてのデータをエクスポートする {#step-1-export-all-data-from-mysql}

1.  次のコマンドを実行して、MySQLからすべてのデータをエクスポートします。

    {{< copyable "" >}}

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup?region=us-west-2'
    ```

    DumplingはデフォルトでSQLファイルのデータをエクスポートします。 `--filetype`オプションを追加することにより、別のファイル形式を指定できます。

    上記で使用したパラメータは次のとおりです。その他のDumplingパラメータについては、 [Dumplingの概要](/dumpling-overview.md)を参照してください。

    | パラメーター              | 説明                                                                                         |
    | ------------------- | ------------------------------------------------------------------------------------------ |
    | `-u`または`--user`     | MySQLユーザー                                                                                  |
    | `-p`または`--password` | MySQLユーザーパスワード                                                                             |
    | `-P`または`--port`     | MySQLポート                                                                                   |
    | `-h`または`--host`     | MySQLIPアドレス                                                                                |
    | `-t`または`--thread`   | エクスポートに使用されるスレッドの数                                                                         |
    | `-o`または`--output`   | エクスポートされたファイルを保存するディレクトリ。ローカルパスまたは[外部ストレージURL](/br/backup-and-restore-storages.md)をサポートします |
    | `-r`または`--row`      | 1つのファイルの最大行数                                                                               |
    | `-F`                | MiBでの単一ファイルの最大サイズ。推奨値：256MiB。                                                              |
    | `B`または`--database`  | エクスポートするデータベースを指定します                                                                       |
    | `-f`または`--filter`   | パターンに一致するテーブルをエクスポートします。構文については[テーブルフィルター](/table-filter.md)を参照してください。                     |

    `${data-path}`に、エクスポートされたすべてのアップストリームテーブルを格納するスペースがあることを確認してください。すべてのスペースを消費する大きなテーブルによってエクスポートが中断されないようにするには、 `-F`オプションを使用して単一ファイルのサイズを制限することを強くお勧めします。

2.  `${data-path}`ディレクトリの`metadata`ファイルを表示します。これは、餃子で生成されたメタデータファイルです。手順3の増分レプリケーションに必要なbinlog位置情報を記録します。

    ```
    SHOW MASTER STATUS:
    Log: mysql-bin.000004
    Pos: 109227
    GTID:
    ```

## ステップ2.完全なデータをTiDBにインポートします {#step-2-import-full-data-to-tidb}

1.  `tidb-lightning.toml`の構成ファイルを作成します。

    {{< copyable "" >}}

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
    data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup?region=us-west-2'.

    [tidb]
    # The target TiDB cluster information.
    host = ${host}                # e.g.: 172.16.32.1
    port = ${port}                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = ${status-port}  # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
    pd-addr = "${ip}:${port}"     # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    TiDB Lightning構成の詳細については、 [TiDBLightningConfiguration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

2.  `tidb-lightning`を実行してインポートを開始します。コマンドラインで直接プログラムを起動すると、SIGHUP信号を受信した後、プロセスが予期せず終了する場合があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例えば：

    S3からデータをインポートする場合は、S3ストレージパスにアクセスできるSecretKeyとAccessKeyを環境変数としてTiDBLightningノードに渡します。 `~/.aws/credentials`からクレデンシャルを読み取ることもできます。

    {{< copyable "" >}}

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  インポートの開始後、次のいずれかの方法でインポートの進行状況を確認できます。

    -   `grep`ログのキーワード`progress` 。進行状況は、デフォルトで5分ごとに更新されます。
    -   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。
    -   [TiDBLightningWebインターフェイス](/tidb-lightning/tidb-lightning-web-interface.md)で進捗状況を確認します。

4.  TiDB Lightningがインポートを完了すると、自動的に終了します。ログ印刷`the whole procedure completed`の最後の5行が見つかった場合、インポートは成功しています。

> **ノート：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、TiDB Lightningが正常に終了することを意味しますが、必ずしもインポートが成功したことを意味するわけではありません。

インポートが失敗した場合、トラブルシューティングについては[TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## ステップ3.インクリメンタルデータをTiDBに複製する {#step-3-replicate-incremental-data-to-tidb}

### データソースを追加する {#add-the-data-source}

1.  次のように`source1.yaml`のファイルを作成します。

    {{< copyable "" >}}

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

2.  次のコマンドを実行して、 `tiup dmctl`を使用してデータソース構成をDMクラスタにロードします。

    {{< copyable "" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    上記のコマンドで使用されるパラメーターは、次のとおりです。

    | パラメータ                   | 説明                                                                |
    | ----------------------- | ----------------------------------------------------------------- |
    | `--master-addr`         | `dmctl`が接続されるクラスタの任意のDMマスターの`{advertise-addr}`例：172.16.10.71：8261 |
    | `operate-source create` | データソースをDMクラスタにロードします。                                             |

### レプリケーションタスクを追加する {#add-a-replication-task}

1.  `task.yaml`のファイルを編集します。インクリメンタルレプリケーションモードと各データソースの開始点を構成します。

    {{< copyable "" >}}

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
      - source-id: "mysql-01"            # Data source ID，i.e., source-id in source1.yaml
        block-allow-list: "bw-rule-1"    # You can use the block-allow-list configuration above.
        # syncer-config-name: "global"    # You can use the syncers incremental data configuration below.
        meta:                            # When task-mode is "incremental" and the target database does not have a checkpoint, DM uses the binlog position as the starting point. If the target database has a checkpoint, DM uses the checkpoint as the starting point.
          # binlog-name: "mysql-bin.000004"  # The binlog position recorded in "Step 1. Export all data from MySQL". If the upstream database service is configured to switch master between different nodes automatically, GTID mode is required.
          # binlog-pos: 109227
          binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

    # (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
    # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    # syncers:            # The running configurations of the sync processing unit.
    #   global:           # Configuration name.
    #     safe-mode: true # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
    ```

    上記のYAMLは、移行タスクに必要な最小構成です。その他の設定項目については、 [DM高度なタスクConfiguration / コンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

    移行タスクを開始する前に、エラーの可能性を減らすために、次の`check-task`コマンドを実行して、構成がDMの要件を満たしていることを確認することをお勧めします。

    {{< copyable "" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
    ```

2.  次のコマンドを実行して、移行タスクを開始します。

    {{< copyable "" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
    ```

    上記のコマンドで使用されるパラメーターは、次のとおりです。

    | パラメータ           | 説明                                                           |
    | --------------- | ------------------------------------------------------------ |
    | `--master-addr` | `dmctl`が接続されるクラスタのDMマスターの{advertise-addr}例：172.16.10.71：8261 |
    | `start-task`    | 移行タスクを開始します。                                                 |

    タスクの開始に失敗した場合は、プロンプトメッセージを確認し、構成を修正してください。その後、上記のコマンドを再実行してタスクを開始できます。

    問題が発生した場合は、 [DMエラー処理](/dm/dm-error-handling.md)と[DM FAQ](/dm/dm-faq.md)を参照してください。

### 移行タスクのステータスを確認する {#check-the-migration-task-status}

DMクラスタに進行中の移行タスクがあるかどうかを確認し、タスクステータスを表示するには、 `tiup dmctl`を使用して`query-status`コマンドを実行します。

{{< copyable "" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

結果の詳細な解釈については、 [クエリステータス](/dm/dm-query-status.md)を参照してください。

### タスクを監視し、ログを表示します {#monitor-the-task-and-view-logs}

移行タスクの履歴ステータスおよびその他の内部メトリックを表示するには、次の手順を実行します。

TiUPを使用してDMをデプロイしたときにPrometheus、Alertmanager、およびGrafanaをデプロイした場合は、デプロイメント中に指定したIPアドレスとポートを使用してGrafanaにアクセスできます。次に、DMダッシュボードを選択して、DM関連の監視メトリックを表示できます。

DMの実行中、DM-worker、DM-master、およびdmctlは、関連情報をログに出力します。これらのコンポーネントのログディレクトリは次のとおりです。

-   DM-master：DM-masterプロセスパラメーター`--log-file`で指定されます。 TiUPを使用してDMを展開する場合、ログディレクトリはデフォルトで`/dm-deploy/dm-master-8261/log/`です。
-   DM-worker：DM-workerプロセスパラメーター`--log-file`で指定されます。 TiUPを使用してDMを展開する場合、ログディレクトリはデフォルトで`/dm-deploy/dm-worker-8262/log/`です。

## 次は何ですか {#what-s-next}

-   [データ移行タスクを一時停止します](/dm/dm-pause-task.md)
-   [データ移行タスクを再開します](/dm/dm-resume-task.md)
-   [データ移行タスクを停止する](/dm/dm-stop-task.md)
-   [データソースのエクスポートとインポート、およびクラスターのタスクConfiguration / コンフィグレーション](/dm/dm-export-import-config.md)
-   [失敗したDDLステートメントの処理](/dm/handle-failed-ddl-statements.md)

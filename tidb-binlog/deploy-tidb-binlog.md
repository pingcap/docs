---
title: TiDB Binlog Cluster Deployment
summary: Learn how to deploy TiDB Binlog cluster.
---

# TiDBBinlogクラスタの展開 {#tidb-binlog-cluster-deployment}

このドキュメントでは、 [バイナリ パッケージを使用して TiDB Binlogをデプロイする](#deploy-tidb-binlog-using-a-binary-package)方法について説明します。

## ハードウェア要件 {#hardware-requirements}

PumpとDrainer は、 Intel x86-64アーキテクチャを備えた 64 ビット ユニバーサル ハードウェアサーバープラットフォーム上に展開され、動作します。

開発、テスト、本番の環境では、サーバーハードウェアの要件は次のとおりです。

| サービス    | サーバーの数 | CPU   | ディスク                                                                         | メモリ |
| :------ | :----- | :---- | :--------------------------------------------------------------------------- | :-- |
| Pump    | 3      | 8コア以上 | SSD、200GB以上                                                                  | 16G |
| Drainer | 1      | 8コア以上 | SAS、100 GB+ (バイナリログがローカル ファイルとして出力される場合、ディスク サイズはこれらのファイルが保持される期間によって異なります。) | 16G |

## TiUP を使用して TiDB Binlogをデプロイ {#deploy-tidb-binlog-using-tiup}

TiUP を使用して TiDB Binlogを展開することをお勧めします。そのためには、 TiUPを使用して TiDB をデプロイするときに、 [TiDBBinlog展開トポロジ](/tidb-binlog-deployment-topology.md)に TiDB Binlogの`drainer`と`pump`のノード情報を追加する必要があります。導入の詳細については、 [TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)を参照してください。

## バイナリ パッケージを使用して TiDB Binlogをデプロイ {#deploy-tidb-binlog-using-a-binary-package}

### 公式バイナリパッケージをダウンロードする {#download-the-official-binary-package}

TiDB Binlogのバイナリ パッケージはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

### 使用例 {#the-usage-example}

3 つの PD ノード、1 つの TiDB ノード、2 つのPumpノード、および 1 つのDrainerノードがあると仮定すると、各ノードの情報は次のとおりです。

| ノード     | IP           |
| :------ | :----------- |
| TiDB    | 192.168.0.10 |
| PD1     | 192.168.0.16 |
| PD2     | 192.168.0.15 |
| PD3     | 192.168.0.14 |
| Pump    | 192.168.0.11 |
| Pump    | 192.168.0.12 |
| Drainer | 192.168.0.13 |

次のパートでは、上記のノードに基づいてPumpとDrainerを使用する方法を示します。

1.  バイナリを使用してPumpをデプロイ。

    -   Pumpのコマンド ライン パラメータを表示するには、 `./pump -help`を実行します。

        ```bash
        Usage of Pump:
        -L string
            the output information level of logs: debug, info, warn, error, fatal ("info" by default)
        -V
            the print version information
        -addr string
            the RPC address through which Pump provides the service (-addr="192.168.0.11:8250")
        -advertise-addr string
            the RPC address through which Pump provides the external service (-advertise-addr="192.168.0.11:8250")
        -config string
            the path of the configuration file. If you specify the configuration file, Pump reads the configuration in the configuration file first. If the corresponding configuration also exits in the command line parameters, Pump uses the configuration of the command line parameters to cover that of the configuration file.
        -data-dir string
            the path where the Pump data is stored
        -gc int
            the number of days to retain the data in Pump ("7" by default)
        -heartbeat-interval int
            the interval of the heartbeats Pump sends to PD (in seconds)
        -log-file string
            the file path of logs
        -log-rotate string
            the switch frequency of logs (hour/day)
        -metrics-addr string
            the Prometheus Pushgateway address. If not set, it is forbidden to report the monitoring metrics.
        -metrics-interval int
            the report frequency of the monitoring metrics ("15" by default, in seconds)
        -node-id string
            the unique ID of a Pump node. If you do not specify this ID, the system automatically generates an ID based on the host name and listening port.
        -pd-urls string
            the address of the PD cluster nodes (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -fake-binlog-interval int
            the frequency at which a Pump node generates fake binlog ("3" by default, in seconds)
        ```

    -   例として「192.168.0.11」にPumpを展開すると、Pump設定ファイルは次のようになります。

        ```toml
        # Pump Configuration

        # the bound address of Pump
        addr = "192.168.0.11:8250"

        # the address through which Pump provides the service
        advertise-addr = "192.168.0.11:8250"

        # the number of days to retain the data in Pump ("7" by default)
        gc = 7

        # the directory where the Pump data is stored
        data-dir = "data.pump"

        # the interval of the heartbeats Pump sends to PD (in seconds)
        heartbeat-interval = 2

        # the address of the PD cluster nodes (each separated by a comma with no whitespace)
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # [security]
        # This section is generally commented out if no special security settings are required.
        # The file path containing a list of trusted SSL CAs connected to the cluster.
        # ssl-ca = "/path/to/ca.pem"
        # The path to the X509 certificate in PEM format that is connected to the cluster.
        # ssl-cert = "/path/to/drainer.pem"
        # The path to the X509 key in PEM format that is connected to the cluster.
        # ssl-key = "/path/to/drainer-key.pem"

        # [storage]
        # Set to true (by default) to guarantee reliability by ensuring binlog data is flushed to the disk
        # sync-log = true

        # When the available disk capacity is less than the set value, Pump stops writing data.
        # 42 MB -> 42000000, 42 mib -> 44040192
        # default: 10 gib
        # stop-write-at-available-space = "10 gib"
        # The LSM DB settings embedded in Pump. Unless you know this part well, it is usually commented out.
        # [storage.kv]
        # block-cache-capacity = 8388608
        # block-restart-interval = 16
        # block-size = 4096
        # compaction-L0-trigger = 8
        # compaction-table-size = 67108864
        # compaction-total-size = 536870912
        # compaction-total-size-multiplier = 8.0
        # write-buffer = 67108864
        # write-L0-pause-trigger = 24
        # write-L0-slowdown-trigger = 17
        ```

    -   Pumpを起動する例:

        ```bash
        ./pump -config pump.toml
        ```

        コマンド ライン パラメータが構成ファイルのパラメータと同じ場合は、コマンド ライン パラメータの値が使用されます。

2.  バイナリを使用してDrainerをデプロイ。

    -   Drainerのコマンド ライン パラメータを表示するには、 `./drainer -help`を実行します。

        ```bash
        Usage of Drainer:
        -L string
            the output information level of logs: debug, info, warn, error, fatal ("info" by default)
        -V
            the print version information
        -addr string
            the address through which Drainer provides the service (-addr="192.168.0.13:8249")
        -c int
            the number of the concurrency of the downstream for replication. The bigger the value, the better throughput performance of the concurrency ("1" by default).
        -cache-binlog-count int
            the limit on the number of binlog items in the cache ("8" by default)
            If a large single binlog item in the upstream causes OOM in Drainer, try to lower the value of this parameter to reduce memory usage.
        -config string
            the directory of the configuration file. Drainer reads the configuration file first.
            If the corresponding configuration exists in the command line parameters, Drainer uses the configuration of the command line parameters to cover that of the configuration file.
        -data-dir string
            the directory where the Drainer data is stored ("data.drainer" by default)
        -dest-db-type string
            the downstream service type of Drainer
            The value can be "mysql", "tidb", "kafka", and "file". ("mysql" by default)
        -detect-interval int
            the interval of checking the online Pump in PD ("10" by default, in seconds)
        -disable-detect
            whether to disable the conflict monitoring
        -disable-dispatch
            whether to disable the SQL feature of splitting a single binlog file. If it is set to "true", each binlog file is restored to a single transaction for replication based on the order of binlogs.
            It is set to "False", when the downstream is MySQL.
        -ignore-schemas string
            the db filter list ("INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test" by default)
            It does not support the Rename DDL operation on tables of `ignore schemas`.
        -initial-commit-ts
            If Drainer does not have the related breakpoint information, you can configure the related breakpoint information using this parameter. ("-1" by default)
            If the value of this parameter is `-1`, Drainer automatically obtains the latest timestamp from PD.
        -log-file string
            the path of the log file
        -log-rotate string
            the switch frequency of log files, hour/day
        -metrics-addr string
            the Prometheus Pushgateway address
            It it is not set, the monitoring metrics are not reported.
        -metrics-interval int
            the report frequency of the monitoring metrics ("15" by default, in seconds)
        -node-id string
            the unique ID of a Drainer node. If you do not specify this ID, the system automatically generates an ID based on the host name and listening port.
        -pd-urls string
            the address of the PD cluster nodes (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -safe-mode
            Whether to enable safe mode so that data can be written into the downstream MySQL/TiDB repeatedly.
            This mode replaces the `INSERT` statement with the `REPLACE` statement and splits the `UPDATE` statement into `DELETE` plus `REPLACE`.
        -txn-batch int
            the number of SQL statements of a transaction which are output to the downstream database ("1" by default)
        ```

    -   例として「192.168.0.13」にDrainerをデプロイする場合、 Drainer設定ファイルは次のとおりです。

        ```toml
        # Drainer Configuration.

        # the address through which Drainer provides the service ("192.168.0.13:8249")
        addr = "192.168.0.13:8249"

        # the address through which Drainer provides the external service
        advertise-addr = "192.168.0.13:8249"

        # the interval of checking the online Pump in PD ("10" by default, in seconds)
        detect-interval = 10

        # the directory where the Drainer data is stored "data.drainer" by default)
        data-dir = "data.drainer"

        # the address of the PD cluster nodes (each separated by a comma with no whitespace)
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # the directory of the log file
        log-file = "drainer.log"

        # Drainer compresses the data when it gets the binlog from Pump. The value can be "gzip". If it is not configured, it will not be compressed
        # compressor = "gzip"

        # [security]
        # This section is generally commented out if no special security settings are required.
        # The file path containing a list of trusted SSL CAs connected to the cluster.
        # ssl-ca = "/path/to/ca.pem"
        # The path to the X509 certificate in PEM format that is connected to the cluster.
        # ssl-cert = "/path/to/pump.pem"
        # The path to the X509 key in PEM format that is connected to the cluster.
        # ssl-key = "/path/to/pump-key.pem"

        # Syncer Configuration
        [syncer]
        # If the item is set, the sql-mode will be used to parse the DDL statement.
        # If the downstream database is MySQL or TiDB, then the downstream sql-mode
        # is also set to this value.
        # sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

        # the number of SQL statements of a transaction that are output to the downstream database ("20" by default)
        txn-batch = 20

        # the number of the concurrency of the downstream for replication. The bigger the value,
        # the better throughput performance of the concurrency ("16" by default)
        worker-count = 16

        # whether to disable the SQL feature of splitting a single binlog file. If it is set to "true",
        # each binlog file is restored to a single transaction for replication based on the order of binlogs.
        # If the downstream service is MySQL, set it to "False".
        disable-dispatch = false

        # In safe mode, data can be written into the downstream MySQL/TiDB repeatedly.
        # This mode replaces the `INSERT` statement with the `REPLACE` statement and replaces the `UPDATE` statement with `DELETE` plus `REPLACE` statements.
        safe-mode = false

        # the downstream service type of Drainer ("mysql" by default)
        # Valid value: "mysql", "tidb", "file", and "kafka".
        db-type = "mysql"

        # If `commit ts` of the transaction is in the list, the transaction is filtered and not replicated to the downstream.
        ignore-txn-commit-ts = []

        # the db filter list ("INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test" by default)
        # Does not support the Rename DDL operation on tables of `ignore schemas`.
        ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

        # `replicate-do-db` has priority over `replicate-do-table`. When they have the same `db` name,
        # regular expressions are supported for configuration.
        # The regular expression should start with "~".

        # replicate-do-db = ["~^b.*","s1"]

        # [syncer.relay]
        # It saves the directory of the relay log. The relay log is not enabled if the value is empty.
        # The configuration only comes to effect if the downstream is TiDB or MySQL.
        # log-dir = ""
        # the maximum size of each file
        # max-file-size = 10485760

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "log"

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "~^a.*"

        # Ignore the replication of some tables
        # [[syncer.ignore-table]]
        # db-name = "test"
        # tbl-name = "log"

        # the server parameters of the downstream database when `db-type` is set to "mysql"
        [syncer.to]
        host = "192.168.0.13"
        user = "root"
        # If you do not want to set a cleartext `password` in the configuration file, you can create `encrypted_password` using `./binlogctl -cmd encrypt -text string`.
        # When you have created an `encrypted_password` that is not empty, the `password` above will be ignored, because `encrypted_password` and `password` cannot take effect at the same time.
        password = ""
        encrypted_password = ""
        port = 3306

        [syncer.to.checkpoint]
        # When the checkpoint type is "mysql" or "tidb", this option can be
        # enabled to change the database that saves the checkpoint
        # schema = "tidb_binlog"
        # Currently only the "mysql" and "tidb" checkpoint types are supported
        # You can remove the comment tag to control where to save the checkpoint
        # The default method of saving the checkpoint for the downstream db-type:
        # mysql/tidb -> in the downstream MySQL or TiDB database
        # file/kafka -> file in `data-dir`
        # type = "mysql"
        # host = "127.0.0.1"
        # user = "root"
        # password = ""
        # `encrypted_password` is encrypted using `./binlogctl -cmd encrypt -text string`.
        # When `encrypted_password` is not empty, the `password` above will be ignored.
        # encrypted_password = ""
        # port = 3306

        # the directory where the binlog file is stored when `db-type` is set to `file`
        # [syncer.to]
        # dir = "data.drainer"

        # the Kafka configuration when `db-type` is set to "kafka"
        # [syncer.to]
        # only one of kafka-addrs and zookeeper-addrs is needed. If both are present, the program gives priority
        # to the kafka address in zookeeper
        # zookeeper-addrs = "127.0.0.1:2181"
        # kafka-addrs = "127.0.0.1:9092"
        # kafka-version = "0.8.2.0"
        # The maximum number of messages (number of binlogs) in a broker request. If it is left blank or a value smaller than 0 is configured, the default value 1024 is used.
        # kafka-max-messages = 1024
        # The maximum size of a broker request (unit: byte). The default value is 1 GiB and the maximum value is 2 GiB.
        # kafka-max-message-size = 1073741824

        # the topic name of the Kafka cluster that saves the binlog data. The default value is <cluster-id>_obinlog.
        # To run multiple Drainers to replicate data to the same Kafka cluster, you need to set different `topic-name`s for each Drainer.
        # topic-name = ""
        ```

    -   開始時のDrainer:

        > **注記：**
        >
        > ダウンストリームが MySQL/TiDB の場合、データの整合性を保証するには、 Drainerの最初の起動前に、値`initial-commit-ts`を取得してデータの完全バックアップを作成し、データを復元する必要があります。

        Drainerを初めて起動するときは、パラメータ`initial-commit-ts`を使用します。

        ```bash
        ./drainer -config drainer.toml -initial-commit-ts {initial-commit-ts}
        ```

        コマンドラインパラメータと構成ファイルパラメータが同じ場合、コマンドラインのパラメータ値が使用されます。

3.  TiDBサーバーを開始します:

    -   PumpとDrainerを起動した後、TiDBサーバーの構成ファイルに次のセクションを追加して、 binlog を有効にして TiDBサーバーを起動します。

            [binlog]
            enable=true

    -   TiDBサーバーは、登録されたポンプのアドレスを PD から取得し、すべてのポンプにデータをストリーミングします。登録されたPumpインスタンスがない場合、TiDBサーバーは起動を拒否するか、Pumpインスタンスがオンラインになるまで起動をブロックします。

> **注記：**
>
> -   TiDB の実行中は、少なくとも 1 つのPumpが正常に実行されていることを保証する必要があります。
> -   TiDBサーバーで TiDB Binlogサービスを有効にするには、TiDB で`-enable-binlog`起動パラメーターを使用するか、TiDBサーバー構成ファイルの [ binlog ] セクションにenable=true を追加します。
> -   同じクラスター内のすべての TiDB インスタンスで TiDB Binlogサービスが有効になっていることを確認してください。有効になっていないと、データ レプリケーション中に上流と下流のデータの不整合が発生する可能性があります。 TiDB Binlogサービスが有効になっていない TiDB インスタンスを一時的に実行する場合は、TiDB 構成ファイルで`run_ddl=false`を設定します。
> -   Drainer は、 `ignore schemas`のテーブル (フィルター リスト内のスキーマ) に対する`rename` DDL 操作をサポートしていません。
> -   既存の TiDB クラスターでDrainerを開始する場合は、通常、クラスター データの完全バックアップを作成し、スナップショットの**タイムスタンプを**取得し、データをターゲット データベースにインポートしてから、 Drainerを開始して、対応する**スナップショット**から増分データをレプリケートする必要があります。**タイムスタンプ**。
> -   ダウンストリーム データベースが TiDB または MySQL の場合、アップストリーム データベースとダウンストリーム データベースの`sql_mode`が一致していることを確認してください。つまり、各 SQL ステートメントがアップストリームで実行され、ダウンストリームにレプリケートされるとき、 `sql_mode`は同じである必要があります。アップストリームとダウンストリームでそれぞれ`select @@sql_mode;`ステートメントを実行して、 `sql_mode`を比較できます。
> -   DDL ステートメントがアップストリームでサポートされているが、ダウンストリームと互換性がない場合、 Drainer はデータのレプリケートに失敗します。例としては、ダウンストリーム データベース MySQL が InnoDB エンジンを使用する場合に`CREATE TABLE t1(a INT) ROW_FORMAT=FIXED;`ステートメントを複製することが挙げられます。この場合、 Drainerで[トランザクションをスキップする](/tidb-binlog/tidb-binlog-faq.md#what-can-i-do-when-some-ddl-statements-supported-by-the-upstream-database-cause-error-when-executed-in-the-downstream-database)構成し、ダウンストリーム データベースで互換性のあるステートメントを手動で実行できます。

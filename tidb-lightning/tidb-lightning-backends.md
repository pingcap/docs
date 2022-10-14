---
title: TiDB Lightning Backends
summary: Learn the backends of TiDB Lightning.
---

# TiDB Lightningバックエンド {#tidb-lightning-backends}

バックエンドは、 TiDB Lightningがターゲット クラスタにデータをインポートする方法を決定します。

TiDB Lightningは次の[バックエンド](/tidb-lightning/tidb-lightning-glossary.md#back-end)をサポートしています。

-   [ローカル バックエンド](#tidb-lightning-local-backend)
-   [インポーターバックエンド](#tidb-lightning-importer-backend)
-   [TiDB バックエンド](#tidb-lightning-tidb-backend)

**Local-backend** : `tidb-lightning`は、最初にデータをキーと値のペアにエンコードし、並べ替えてローカルの一時ディレクトリに保存し、これらのキーと値のペアを*SST ファイルとして*各 TiKV ノードに<em>アップロード</em>します。次に、TiKV はこれらの<em>SST ファイル</em>をクラスターに取り込みます。 Local-backend の実装は Importer-backend の実装と同じですが、外部の`tikv-importer`コンポーネントには依存しません。

**Importer-backend** : `tidb-lightning`は、最初に SQL または CSV データを KV ペアにエンコードし、外部プログラムに依存してこれらの KV ペアをソートし、 `tikv-importer`ノードに直接取り込みます。

**TiDB バックエンド**: `tidb-lightning`は、最初にこれらのデータを SQL `INSERT`ステートメントにエンコードし、これらのステートメントを TiDB ノードで直接実行します。

| バックエンド                | ローカル バックエンド    | インポーターバックエンド    | TiDB バックエンド   |
| :-------------------- | :------------- | :-------------- | :------------ |
| スピード                  | 高速 (~500 GB/時) | 高速 (~300 GB/時)  | 遅い (~50 GB/時) |
| リソース使用量               | 高い             | 高い              | 低い            |
| ネットワーク帯域幅の使用          | 高い             | 中くらい            | 低い            |
| インポート中に考慮されるACID      | いいえ            | いいえ             | はい            |
| 対象テーブル                | 空である必要があります    | 空である必要があります     | 移入可能          |
| 追加コンポーネントが必要          | いいえ            | `tikv-importer` | いいえ           |
| サポートされている TiDB のバージョン | = v4.0.0       | 全て              | 全て            |
| 影響を受ける TiDB サービス      | はい             | はい              | いいえ           |

> **ノート：**
>
> -   複数のTiDB Lightningインスタンスを使用して同じターゲットにデータをインポートする場合は、一度に 1 つのバックエンドのみを適用します。たとえば、ローカル バックエンド モードと TiDB バックエンド モードの両方で同時に同じ TiDB クラスターにデータをインポートすることはできません。
>
> -   デフォルトでは、複数のTiDB Lightningインスタンスを開始して、同じ TiDB クラスターにデータをインポートすることはできません。代わりに、 [並行輸入品](/tidb-lightning/tidb-lightning-distributed-import.md)機能を使用できます。

## バックエンド モードの選択方法 {#how-to-choose-the-backend-modes}

-   データ インポートのターゲット クラスターが v4.0 以降のバージョンである場合は、他の 2 つのモードよりも使いやすく、パフォーマンスが高い Local-backend モードを最初に使用することを検討してください。
-   データ インポートのターゲット クラスターが v3.x 以前のバージョンである場合は、Importer-backend モードを使用することをお勧めします。
-   データ インポートのターゲット クラスターがオンラインの運用環境にある場合、またはデータ インポートのターゲット テーブルに既にデータがある場合は、TiDB バックエンド モードを使用することをお勧めします。

## TiDB Lightningローカルバックエンド {#tidb-lightning-local-backend}

TiDB v4.0.3 以降、ローカル バックエンド機能がTiDB Lightningに導入されました。この機能を使用して、v4.0.0 以降の TiDB クラスターにデータをインポートできます。

### ローカル バックエンドの展開 {#deployment-for-local-backend}

ローカル バックエンド モードでTiDB Lightningをデプロイするには、 [TiDB Lightningの導入](/tidb-lightning/deploy-tidb-lightning.md)を参照してください。

## TiDB Lightning TiDB バックエンド {#tidb-lightning-tidb-backend}

> **ノート：**
>
> TiDB v4.0 以降、PingCAP は[ローダ](https://docs.pingcap.com/tidb/v4.0/loader-overview)ツールを維持しなくなりました。 v5.0 以降、ローダーのドキュメントは利用できなくなりました。ローダーの機能はTiDB Lightningに切り替えることを強くお勧めします。

### TiDB バックエンドのデプロイ {#deployment-for-tidb-backend}

TiDB バックエンドを使用する場合、 `tikv-importer`をデプロイする必要はありません。 [標準展開手順](/tidb-lightning/deploy-tidb-lightning.md)と比較すると、TiDB バックエンドのデプロイには次の 2 つの違いがあります。

-   `tikv-importer`を含むすべてのステップをスキップできます。
-   TiDB バックエンドを使用することを宣言するには、構成を変更する必要があります。

#### ハードウェア要件 {#hardware-requirements}

TiDB バックエンドを使用したTiDB Lightningの速度は、TiDB の SQL 処理速度によって制限されます。したがって、ローエンドのマシンでも可能なパフォーマンスを最大限に引き出すことができます。推奨されるハードウェア構成は次のとおりです。

-   16個の論理コアCPU
-   データ ソース全体を格納するのに十分な大きさの SSD、より高速な読み取り速度を優先する
-   1 ギガビット ネットワーク カード

#### 手動展開 {#manual-deployment}

`tikv-importer`をダウンロードして構成する必要はありません。 TiDB Lightningは[ここ](/download-ecosystem-tools.md#tidb-lightning)からダウンロードできます。

`tidb-lightning`を実行する前に、構成ファイルに次の行を追加します。

```toml
[tikv-importer]
backend = "tidb"
```

または`tidb-lightning`を実行するときに`--backend tidb`引数を指定します。

#### Configuration / コンフィグレーションの説明とサンプル {#configuration-description-and-samples}

このセクションでは、 TiDB Lightningでのタスク設定のサンプルを提供します。

```toml
# tidb-lightning task configuration

[lightning]
# Checks whether the cluster satisfies the minimum requirement before starting.
check-requirements = true

# Each table is split into one "index engine" to store indices, and multiple
# "data engines" to store row data. These settings control the maximum
# concurrent number for each type of engines.
# Controls the maximum number of tables that can be imported in parallel. For TiDB-backend, the default value is the number of CPU cores.
index-concurrency = 40

# Controls the maximum number of "data engines" allowed to be imported in parallel. The default value is the number of CPU cores. The value should be no less than the value of index-concurrency.
table-concurrency = 40

# The number of concurrent SQL statements executed. It is set to the number of logical CPU cores by default. The bottleneck of TiDB-backend is usually not the CPU. You can increase this value based on the actual load of the downstream cluster to optimize the write speed. At the same time, when adjusting this configuration, it is recommended to adjust the index-concurrency and table-concurrency to the same value.
region-concurrency = 40

# Logging
level = "info"
# The directory to which the log is output. If it is empty (default), the file is saved to /tmp/lightning.log.{timestamp}. If you want the logs to be written to the system standard output, set it to "-".
file = "tidb-lightning.log"

[checkpoint]
# Whether to enable checkpoints.
# While importing data, TiDB Lightning records which tables have been imported, so
# even if TiDB Lightning or some other component crashes, you can start from a known
# good state instead of restarting from scratch.
enable = true

# Where to store the checkpoints.
#  - file (default): store as a local file (requires v2.1.1 or later)
#  - mysql: store into a remote MySQL-compatible database
driver = "file"

# The schema name (database name) to store the checkpoints
# Enabled only when `driver = "mysql"`.
# schema = "tidb_lightning_checkpoint"

# The data source name (DSN) indicating the location of the checkpoint storage.
#
# For the "file" driver, the DSN is a path. If the path is not specified, Lightning would
# default to "/tmp/CHECKPOINT_SCHEMA.pb".
#
# For the "mysql" driver, the DSN is a URL in the form of "USER:PASS@tcp(HOST:PORT)/".
# If the URL is not specified, the TiDB server from the [tidb] section is used to
# store the checkpoints. You should specify a different MySQL-compatible
# database server to reduce the load of the target TiDB cluster.
#dsn = "/tmp/tidb_lightning_checkpoint.pb"

# Whether to keep the checkpoints after all data are imported. If false, the
# checkpoints are deleted. Keeping the checkpoints can aid debugging but
# might leak metadata about the data source.
# keep-after-success = false

[tikv-importer]
# use the TiDB-backend.
backend = "tidb"

# Action to do when trying to insert a duplicated entry in the "tidb" backend.
#  - replace: use new entry to replace the existing entry
#  - ignore: keep the existing entry, and ignore the new entry
#  - error: report error and quit the program
# on-duplicate = "replace"

[mydumper]
# Block size for file reading. Keep it longer than the longest string of
# the data source.
# read-block-size = "64KiB" 

# Minimum size (in terms of source data file) of each batch of import.
# TiDB Lightning splits a large table into multiple data engine files according to this size.
# batch-size = 107_374_182_400 # Byte (default = 100 GB)

# Local source data directory or the URL of the external storage.
data-source-dir = "/data/my_database"

# the input data in a "strict" format speeds up processing.
# "strict-format = true" requires that:
# in CSV, every value cannot contain literal new lines (U+000A and U+000D, or \r and \n) even
# when quoted, which means new lines are strictly used to separate rows.
# "Strict" format allows TiDB Lightning to quickly locate split positions of a large file for parallel processing.
# However, if the input data is not "strict", it may split a valid data in half and
# corrupt the result.
# The default value is false for safety instead of speed.
strict-format = false

# If strict-format is true, TiDB Lightning splits large CSV files into multiple chunks to process in
# parallel. max-region-size is the maximum size of each chunk after splitting.
# max-region-size = 268_435_456 # Byte (default = 256 MB)

# Only import tables if these wildcard rules are matched. See the corresponding section for details.
filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

# Configures how CSV files are parsed.
[mydumper.csv]
# Separator between fields, should be an ASCII character.
separator = ','
# Quoting delimiter, can either be an ASCII character or empty string.
delimiter = '"'
# Whether the CSV files contain a header.
# If `header` is true, the first line will be skipped.
header = true
# Whether the CSV contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to interpret backslash escapes inside fields.
backslash-escape = true
# If a line ends with a separator, remove it.
trim-last-separator = false

[tidb]
# Configuration of any TiDB server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
password = ""

# The default SQL mode used to parse and execute the SQL statements.
sql-mode = "ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION"

# Whether to use TLS for SQL connections. Valid values are:
#  * ""            - force TLS (same as "cluster") if [tidb.security] section is populated, otherwise same as "false"
#  * "false"       - disable TLS
#  * "cluster"     - force TLS and verify the server's certificate with the CA specified in the [tidb.security] section
#  * "skip-verify" - force TLS but do not verify the server's certificate (insecure!)
#  * "preferred"   - same as "skip-verify", but if the server does not support TLS, fallback to unencrypted connection
# tls = ""

# Specifies certificates and keys for TLS-enabled MySQL connections.
# [tidb.security]

# Public certificate of the CA. Set to empty string to disable TLS for SQL.
# ca-path = "/path/to/ca.pem"

# Public certificate of this service. Default to copy of `security.cert-path`
# cert-path = "/path/to/lightning.pem"

# Private key of this service. Default to copy of `security.key-path`
# key-path = "/path/to/lightning.key"

# Configures the background periodic actions.
# Supported units: h (hour), m (minute), s (second).
[cron]

# Duration between which an import progress is printed to the log.
log-progress = "5m"
```

構成項目の詳細な説明については、 [TiDB LightningConfiguration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

### 紛争解決 {#conflict-resolution}

TiDB バックエンドは、既に入力されているテーブルへのインポートをサポートしています。ただし、新しいデータは、古いデータとの一意キーの競合を引き起こす可能性があります。このタスク構成を使用して、競合を解決する方法を制御できます。

```toml
[tikv-importer]
backend = "tidb"
on-duplicate = "replace" # or "error" or "ignore"
```

| 設定  | コンフリクト時の振る舞い            | 同等の SQL ステートメント          |
| :-- | :---------------------- | :----------------------- |
| 交換  | 新しいエントリが古いエントリに置き換わる    | `REPLACE INTO ...`       |
| 無視  | 古いエントリを保持し、新しいエントリを無視する | `INSERT IGNORE INTO ...` |
| エラー | インポートを中止                | `INSERT INTO ...`        |

### Loader からTiDB Lightningへの移行 TiDB バックエンド {#migrating-from-loader-to-tidb-lightning-tidb-backend}

データを TiDB クラスターにインポートする必要がある場合、TiDB バックエンドを使用するTiDB Lightningは[ローダ](https://docs.pingcap.com/tidb/v4.0/loader-overview)の機能を完全に置き換えることができます。次のリストは、ローダー構成を[TiDB Lightning構成](/tidb-lightning/tidb-lightning-configuration.md)に変換する方法を示しています。

<table><thead><tr><th>ローダ</th><th>TiDB Lightning</th></tr></thead><tbody><tr><td>

```toml

# log level
log-level = "info"

# The directory to which the log is output
log-file = "loader.log"

# Prometheus
status-addr = ":8272"

# concurrency
pool-size = 16
```

</td><td>

```toml
[lightning]
# log level
level = "info"

# The directory to which the log is output. If this directory is not specified, it defaults to the directory where the command is executed.
file = "tidb-lightning.log"

# Prometheus
pprof-port = 8289

# concurrency (better left as default)
#region-concurrency = 16
```

</td></tr>
<tr><td>

```toml
# checkpoint database
checkpoint-schema = "tidb_loader"
```

</td><td>

```toml
[checkpoint]
# checkpoint storage
enable = true
schema = "tidb_lightning_checkpoint"
# by default the checkpoint is stored in
# a local file, which is more efficient.
# but you could still choose to store the
# checkpoints in the target database with
# this setting:
#driver = "mysql"
```

</td></tr>
<tr><td>

```toml
```

</td><td>

```toml
[tikv-importer]
# use the TiDB-backend
backend = "tidb"
```

</td></tr>
<tr><td>

```toml

# data source directory
dir = "/data/export/"
```

</td><td>

```toml
[mydumper]
# data source directory
data-source-dir = "/data/export"
```

</td></tr>

<tr><td>

```toml
[db]
# TiDB connection parameters
host = "127.0.0.1"
port = 4000

user = "root"
password = ""

#sql-mode = ""
```

</td><td>

```toml
[tidb]
# TiDB connection parameters
host = "127.0.0.1"
port = 4000

# In the TiDB-backend mode, this parameter is optional.
# status-port = 10080
user = "root"
password = ""

#sql-mode = ""
```

</td></tr>
<tr><td>

```toml
# [[route-rules]]
# Table routes
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td><td>

```toml
# [[routes]]
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td></tr>
</tbody>
</table>

## TiDB Lightning Importer バックエンド {#tidb-lightning-importer-backend}

### インポーター バックエンド モードのデプロイ {#deployment-for-importer-backend-mode}

このセクションでは、インポーター バックエンド モードで[TiDB Lightningを手動でデプロイする](#deploy-tidb-lightning-manually)を実行する方法について説明します。

#### ハードウェア要件 {#hardware-requirements}

`tidb-lightning`と`tikv-importer`は、どちらもリソースを大量に消費するプログラムです。それらを 2 台の別々のマシンにデプロイすることをお勧めします。

最高のパフォーマンスを実現するには、次のハードウェア構成を使用することをお勧めします。

-   `tidb-lightning` :

    -   32 以上の論理コア CPU
    -   データ ソース全体を格納するのに十分な大きさの SSD、より高速な読み取り速度を優先する
    -   10 ギガビット ネットワーク カード (300 MB/秒以上で転送可能)
    -   `tidb-lightning`は、実行時にすべての CPU コアを完全に消費するため、専用のマシンにデプロイすることを強くお勧めします。不可能な場合は、 `tidb-lightning`を`tidb-server`などの他のコンポーネントと一緒にデプロイし、CPU 使用率を`region-concurrency`設定で制限することができます。

-   `tikv-importer` :

    -   32 以上の論理コア CPU
    -   40 GB 以上のメモリ
    -   1 TB+ SSD、より高い IOPS を優先 (≥ 8000 を推奨)
        -   ディスクは、上位 N 個のテーブルの合計サイズ ( `N` = `max(index-concurrency, table-concurrency)` ) より大きくする必要があります。
    -   10 ギガビット ネットワーク カード (300 MB/秒以上で転送可能)
    -   `tikv-importer`は、実行時にすべての CPU、ディスク I/O、およびネットワーク帯域幅を完全に消費するため、専用のマシンにデプロイすることを強くお勧めします。

十分な数のマシンがある場合は、複数の`tidb lightning` + `tikv importer`サーバーを展開し、それぞれが個別のテーブル セットで動作して、データを並行してインポートできます。

#### TiDB Lightningを手動でデプロイ {#deploy-tidb-lightning-manually}

##### ステップ 1: TiDB クラスターをデプロイする {#step-1-deploy-a-tidb-cluster}

データをインポートする前に、クラスター バージョン 2.0.9 以降の TiDB クラスターをデプロイする必要があります。最新バージョンを使用することを強くお勧めします。

導入手順は[TiDB クイック スタート ガイド](/quick-start-with-tidb.md)にあります。

#### ステップ 2: TiDB Lightningインストール パッケージをダウンロードする {#step-2-download-the-tidb-lightning-installation-package}

[TiDB エンタープライズ ツールのダウンロード ページ](/download-ecosystem-tools.md#tidb-lightning)を参照して、 TiDB Lightningパッケージをダウンロードします (TiDB クラスターと同じバージョンを選択してください)。

#### ステップ 3: <code>tikv-importer</code>開始する {#step-3-start-code-tikv-importer-code}

1.  インストール パッケージから`bin/tikv-importer`をアップロードします。

2.  構成する`tikv-importer.toml` .

    ```toml
    # TiKV Importer configuration file template

    # Log file
    log-file = "tikv-importer.log"
    # Log level: trace, debug, info, warn, error, off.
    log-level = "info"

    # Listening address of the status server.
    status-server-address = "0.0.0.0:8286"

    [server]
    # The listening address of tikv-importer. tidb-lightning needs to connect to
    # this address to write data.
    addr = "0.0.0.0:8287"

    [import]
    # The directory to store engine files.
    import-dir = "/mnt/ssd/data.import/"
    ```

    上記は重要な設定のみを示しています。設定の完全なリストについては、セクション[Configuration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer)を参照してください。

3.  `tikv-importer`を実行します。

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### ステップ 4: <code>tidb-lightning</code>を開始する {#step-4-start-code-tidb-lightning-code}

1.  ツール セットから`bin/tidb-lightning`と`bin/tidb-lightning-ctl`をアップロードします。

2.  データ ソースを同じマシンにマウントします。

3.  構成する`tidb-lightning.toml` .以下のテンプレートに表示されない構成の場合、 TiDB Lightningは構成エラーをログ ファイルに書き込み、終了します。

    ```toml
    [lightning]
    # The concurrency number of data. It is set to the number of logical CPU
    # cores by default. When deploying together with other components, you can
    # set it to 75% of the size of logical CPU cores to limit the CPU usage.
    # region-concurrency =

    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # The listening address of tikv-importer. Change it to the actual address.
    addr = "172.16.31.10:8287"

    [mydumper]
    # mydumper local source data directory
    data-source-dir = "/data/my_database"

    [tidb]
    # Configuration of any TiDB server from the cluster
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    ```

    上記は重要な設定のみを示しています。設定の完全なリストについては、セクション[Configuration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)を参照してください。

4.  `tidb-lightning`を実行します。コマンドラインでコマンドを直接実行すると、SIGHUP シグナルを受信したためにプロセスが終了する場合があります。代わりに、 `nohup`コマンドを含む bash スクリプトを実行することをお勧めします。

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

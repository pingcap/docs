---
title: Reparo User Guide
summary: Reparoの使い方を学びます。
---

# Reparoユーザーガイド {#reparo-user-guide}

Reparo は、増分データを回復するために使用される TiDB Binlogツールです。増分データをバックアップするには、TiDB BinlogのDrainer を使用して、binlogデータを protobuf 形式でファイルに出力します。増分データを復元するには、 Reparo を使用してファイル内のbinlogデータを解析し、TiDB/MySQL にbinlogを適用します。

Reparoインストールパッケージ( `reparo` )はTiDB Toolkitに含まれています。TiDBTiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

## Reparoの使用 {#reparo-usage}

### コマンドラインパラメータの説明 {#description-of-command-line-parameters}

    Usage of Reparo:
    -L string
        The level of the output information of logs
        Value: "debug"/"info"/"warn"/"error"/"fatal" ("info" by default)
    -V Prints the version.
    -c int
        The number of concurrencies in the downstream for the replication process (`16` by default). A higher value indicates a better throughput for the replication.
    -config string
        The path of the configuration file
        If the configuration file is specified, Reparo reads the configuration data in this file.
        If the configuration data also exists in the command line parameters, Reparo uses the configuration data in the command line parameters to cover that in the configuration file.
    -data-dir string
        The storage directory for the binlog file in the protobuf format that Drainer outputs ("data.drainer" by default)
    -dest-type string
        The downstream service type
        Value: "print"/"mysql" ("print" by default)
        If it is set to "print", the data is parsed and printed to standard output while the SQL statement is not executed.
        If it is set to "mysql", you need to configure the "host", "port", "user" and "password" information in the configuration file.
    -log-file string
        The path of the log file
    -log-rotate string
        The switch frequency of log files
        Value: "hour"/"day"
    -start-datetime string
        Specifies the time point for starting recovery.
        Format: "2006-01-02 15:04:05"
        If it is not set, the recovery process starts from the earliest binlog file.
    -stop-datetime string
        Specifies the time point of finishing the recovery process.
        Format: "2006-01-02 15:04:05"
        If it is not set, the recovery process ends up with the last binlog file.
    -safe-mode bool
        Specifies whether to enable safe mode. When enabled, it supports repeated replication.
    -txn-batch int
        The number of SQL statements in a transaction that is output to the downstream database (`20` by default).

### 設定ファイルの説明 {#description-of-the-configuration-file}

```toml
# The storage directory for the binlog file in the protobuf format that Drainer outputs
data-dir = "./data.drainer"

# The level of the output information of logs
# Value: "debug"/"info"/"warn"/"error"/"fatal" ("info" by default)
log-level = "info"

# Uses `start-datetime` and `stop-datetime` to specify the time range in which
# the binlog files are to be recovered.
# Format: "2006-01-02 15:04:05"
# start-datetime = ""
# stop-datetime = ""

# Correspond to `start-datetime` and `stop-datetime` respectively.
# They are used to specify the time range in which the binlog files are to be recovered.
# If `start-datetime` and `stop-datetime` are set, there is no need to set `start-tso` and `stop-tso`.
# When you perform a full recovery or resume an incremental recovery, set start-tso to tso + 1 or stop-tso + 1, respectively.
# start-tso = 0
# stop-tso = 0

# The downstream service type
# Value: "print"/"mysql" ("print" by default)
# If it is set to "print", the data is parsed and printed to standard output
# while the SQL statement is not executed.
# If it is set to "mysql", you need to configure `host`, `port`, `user` and `password` in [dest-db].
dest-type = "mysql"

# The number of SQL statements in a transaction that is output to the downstream database (`20` by default).
txn-batch = 20

# The number of concurrencies in the downstream for the replication process (`16` by default). A higher value indicates a better throughput for the replication.
worker-count = 16

# Safe-mode configuration
# Value: "true"/"false" ("false" by default)
# If it is set to "true", Reparo splits the `UPDATE` statement into a `DELETE` statement plus a `REPLACE` statement.
safe-mode = false

# `replicate-do-db` and `replicate-do-table` specify the database and table to be recovered.
# `replicate-do-db` has priority over `replicate-do-table`.
# You can use a regular expression for configuration. The regular expression should start with "~".
# The configuration method for `replicate-do-db` and `replicate-do-table` is
# the same with that for `replicate-do-db` and `replicate-do-table` of Drainer.
# replicate-do-db = ["~^b.*","s1"]
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "log"
# [[replicate-do-table]]
# db-name ="test"
# tbl-name = "~^a.*"

# If `dest-type` is set to `mysql`, `dest-db` needs to be configured.
[dest-db]
host = "127.0.0.1"
port = 3309
user = "root"
password = ""
```

### 例を開始 {#start-example}

    ./reparo -config reparo.toml

> **注記：**
>
> -   `data-dir` Drainer が出力するbinlogファイルのディレクトリを指定します。
> -   `start-datatime`と`start-tso`どちらもリカバリを開始する時点を指定するために使用されますが、時間形式が異なります。設定されていない場合、リカバリプロセスはデフォルトで最も古いbinlogファイルから開始されます。
> -   `stop-datetime`と`stop-tso`どちらもリカバリを終了する時点を指定するために使用されますが、時間形式が異なります。設定されていない場合、リカバリ プロセスはデフォルトで最後のbinlogファイルで終了します。
> -   `dest-type`宛先タイプを指定します。その値は「mysql」と「print」になります。
>
>     -   `mysql`に設定すると、MySQL プロトコルを使用するか互換性のある MySQL または TiDB にデータを復旧できます。この場合、構成情報の`[dest-db]`でデータベース情報を指定する必要があります。
>     -   `print`に設定すると、binlog情報のみが出力されます。通常は、デバッグやbinlog情報の確認に使用します。この場合、 `[dest-db]`指定する必要はありません。
> -   `replicate-do-db`リカバリするデータベースを指定します。設定されていない場合は、すべてのデータベースがリカバリされます。
> -   `replicate-do-table`リカバリするテーブルを指定します。設定されていない場合は、すべてのテーブルがリカバリされます。

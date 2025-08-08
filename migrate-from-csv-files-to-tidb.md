---
title: Migrate Data from CSV Files to TiDB
summary: CSV ファイルから TiDB にデータを移行する方法を学びます。
---

# CSV ファイルから TiDB へのデータの移行 {#migrate-data-from-csv-files-to-tidb}

このドキュメントでは、CSV ファイルから TiDB にデータを移行する方法について説明します。

TiDB Lightningは、CSVファイルやタブ区切り値（TSV）などの他の区切り形式からデータを読み取ることができます。その他のフラットファイルデータソースについては、こちらのドキュメントを参照してTiDBにデータを移行してください。

## 前提条件 {#prerequisites}

-   [TiDB Lightningをインストールする](/migration-tools.md) 。
-   [TiDB Lightningに必要なターゲットデータベース権限を取得する](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database) 。

## ステップ1.CSVファイルを準備する {#step-1-prepare-the-csv-files}

すべてのCSVファイルを同じディレクトリに置いてください。TiDB TiDB LightningですべてのCSVファイルを認識させるには、ファイル名が以下の要件を満たす必要があります。

-   CSV ファイルにテーブル全体のデータが含まれている場合は、ファイルに`${db_name}.${table_name}.csv`名前を付けます。
-   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加してください。例： `${db_name}.${table_name}.003.csv` 。数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さを揃えるため、数値の前にゼロを追加する必要があります。

TiDB Lightning は、このディレクトリとそのサブディレクトリ内のすべての`.csv`ファイルを再帰的に検索します。

## ステップ2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schema}

CSVファイルにはスキーマ情報が含まれていないため、CSVファイルからTiDBにデータをインポートする前に、ターゲットテーブルスキーマを作成する必要があります。ターゲットテーブルスキーマは、以下の2つの方法のいずれかで作成できます。

-   **方法 1** : TiDB Lightningを使用してターゲット テーブル スキーマを作成します。

    必要な DDL ステートメントを含む SQL ファイルを作成します。

    -   `${db_name}-schema-create.sql`ファイルに`CREATE DATABASE`ステートメントを追加します。
    -   `${db_name}.${table_name}-schema.sql`ファイルに`CREATE TABLE`ステートメントを追加します。

-   **方法 2** : ターゲット テーブル スキーマを手動で作成します。

## ステップ3. 構成ファイルを作成する {#step-3-create-the-configuration-file}

次の内容のファイルを`tidb-lightning.toml`作成します。

```toml
[lightning]
# Log
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
# "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally.
# For more information on import mode, refer to <https://docs.pingcap.com/tidb/stable/tidb-lightning-overview#tidb-lightning-architecture>
backend = "local"
# Set the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

[mydumper]
# Directory of the data source.
data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup'.

# Defines CSV format.
[mydumper.csv]
# Field separator of the CSV file. Must not be empty. If the source file contains fields that are not string or numeric, such as binary, blob, or bit, it is recommended not to usesimple delimiters such as ",", and use an uncommon character combination like "|+|" instead.
separator = ','
# Delimiter. Can be zero or multiple characters.
delimiter = '"'
# Line terminator. By default, \r, \n, and \r\n are all treated as line terminators.
# terminator = "\r\n"
# Configures whether the CSV file has a table header.
# If this item is set to true, TiDB Lightning uses the first line of the CSV file to parse the corresponding relationship of fields.
header = true
# Configures whether the CSV file contains NULL.
# If this item is set to true, any column of the CSV file cannot be parsed as NULL.
not-null = false
# If `not-null` is set to false (CSV contains NULL),
# The following value is parsed as NULL.
null = '\N'
# Whether to treat the backslash ('\') in the string as an escape character.
backslash-escape = true
# Whether to trim the last separator at the end of each line.
trim-last-separator = false

[tidb]
# The target cluster.
host = ${host}            # e.g.: 172.16.32.1
port = ${port}            # e.g.: 4000
user = "${user_name}"     # e.g.: "root"
password = "${password}"  # e.g.: "rootroot"
status-port = ${status-port} # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
pd-addr = "${ip}:${port}" # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
```

設定ファイルの詳細については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ4. インポートパフォーマンスの調整（オプション） {#step-4-tune-the-import-performance-optional}

約256MiBの均一サイズのCSVファイルからデータをインポートする場合、 TiDB Lightningは最高のパフォーマンスを発揮します。ただし、単一の大きなCSVファイルからデータをインポートする場合、 TiDB Lightningはデフォルトで1つのスレッドしか使用できないため、インポート速度が低下する可能性があります。

インポートを高速化するために、大きなCSVファイルを小さなファイルに分割することができます。一般的な形式のCSVファイルの場合、 TiDB Lightningがファイル全体を読み込む前に、各行の開始位置と終了位置を素早く特定することは困難です。そのため、 TiDB LightningはデフォルトではCSVファイルを自動的に分割しません。ただし、インポートするCSVファイルが特定の形式要件を満たしている場合は、モード`strict-format`有効にすることができます。このモードでは、 TiDB Lightningは1つの大きなCSVファイルを約256MiBの複数のファイルに自動的に分割し、それらを並列処理します。

> **注記：**
>
> CSVファイルが厳密なフォーマットではないにもかかわらず、誤ってモード`strict-format`を`true`に設定した場合、複数行にまたがるフィールドが2つのフィールドに分割されます。その結果、解析に失敗し、 TiDB Lightningはエラーを報告せずに破損したデータをインポートする可能性があります。

厳密な形式のCSVファイルでは、各フィールドは1行のみで記述されます。以下の要件を満たす必要があります。

-   区切り文字が空です。
-   各フィールドにはCR（ `\r` ）またはLF（ `\n` ）が含まれません。

`strict-format` CSV ファイルの場合は、行末文字`terminator`明示的に指定する必要があります。

CSV ファイルが上記の要件を満たしている場合は、次のように`strict-format`モードを有効にすることでインポートを高速化できます。

```toml
[mydumper]
strict-format = true
```

## ステップ5. データをインポートする {#step-5-import-the-data}

インポートを開始するには、 `tidb-lightning`実行してください。コマンドラインでプログラムを起動すると、SIGHUP シグナルを受信した後にプロセスが予期せず終了する可能性があります。その場合は、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例:

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

インポートが開始されたら、次のいずれかの方法でインポートの進行状況を確認できます。

-   ログにキーワード`progress` `grep`します。デフォルトでは、進行状況は5分ごとに更新されます。
-   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)の進捗状況を確認します。
-   [TiDB Lightningウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)の進捗状況を確認します。

TiDB Lightningはインポートを完了すると自動的に終了します。最後の行の`tidb-lightning.log`に`the whole procedure completed`含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポートでエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **注記：**
>
> インポートが成功したかどうかにかかわらず、ログの最後の行には`tidb lightning exit`表示されます。これはTiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するわけではありません。

インポートに失敗した場合は、トラブルシューティングについては[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## その他のファイル形式 {#other-file-formats}

データソースが他の形式の場合、データソースからデータを移行するには、ファイル名の末尾に`.csv`を追加し、 `tidb-lightning.toml`の設定ファイルの`[mydumper.csv]`番目のセクションに該当する変更を加える必要があります。一般的な形式での変更例を以下に示します。

**TSV:**

```toml
# Format example
# ID    Region    Count
# 1     East      32
# 2     South     NULL
# 3     West      10
# 4     North     39

# Format configuration
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
trim-last-separator = false
```

**TPC-H DBGEN:**

```toml
# Format example
# 1|East|32|
# 2|South|0|
# 3|West|10|
# 4|North|39|

# Format configuration
[mydumper.csv]
separator = '|'
delimiter = ''
header = false
not-null = true
backslash-escape = false
trim-last-separator = true
```

## 次は何？ {#what-s-next}

-   [CSVのサポートと制限](/tidb-lightning/tidb-lightning-data-source.md#csv) 。

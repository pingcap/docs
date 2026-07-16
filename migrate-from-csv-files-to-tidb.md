---
title: Migrate Data from CSV Files to TiDB
summary: CSVファイルからTiDBへのデータ移行方法を学びましょう。
---

# CSVファイルからTiDBへのデータ移行 {#migrate-data-from-csv-files-to-tidb}

このドキュメントでは、CSVファイルからTiDBへデータを移行する方法について説明します。

TiDB Lightningは、CSVファイルやタブ区切り値（TSV）などの他の区切り文字形式のデータを読み取ることができます。その他のフラットファイルデータソースについても、このドキュメントを参照してTiDBへのデータ移行を行うことができます。

## 前提条件 {#prerequisites}

-   [TiDB Lightningをインストールする](/migration-tools.md)。
-   [TiDB Lightningに必要なターゲットデータベース権限を取得します](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database)

## ステップ1. CSVファイルを準備する {#step-1-prepare-the-csv-files}

すべてのCSVファイルを同じディレクトリに配置してください。TiDB LightningがすべてのCSVファイルを認識する必要がある場合は、ファイル名が以下の要件を満たす必要があります。

-   CSV ファイルにテーブル全体のデータが含まれている場合は、ファイル名を`${db_name}.${table_name}.csv`とします。
-   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値サフィックスを追加してください。例： `${db_name}.${table_name}.003.csv` 。数値サフィックスは連続していなくても構いませんが、昇順である必要があります。また、すべてのサフィックスの長さが同じになるように、数値の前にゼロを追加する必要があります。

TiDB Lightning は、このディレクトリとそのサブディレクトリ内のすべての`.csv`ファイルを再帰的に検索します。

## ステップ2. 対象テーブルのスキーマを作成する {#step-2-create-the-target-table-schema}

CSVファイルにはスキーマ情報が含まれていないため、CSVファイルからTiDBにデータをインポートする前に、対象テーブルのスキーマを作成する必要があります。対象テーブルのスキーマは、以下の2つの方法のいずれかで作成できます。

-   **方法 1** : TiDB Lightningを使用してターゲット テーブル スキーマを作成します。

    必要なDDLステートメントを含むSQLファイルを作成します。

    -   `CREATE DATABASE`ファイルに`${db_name}-schema-create.sql` } ステートメントを追加します。
    -   `CREATE TABLE`ファイルに`${db_name}.${table_name}-schema.sql` } ステートメントを追加します。

-   **方法2** ：対象テーブルのスキーマを手動で作成する。

## ステップ3．設定ファイルを作成する {#step-3-create-the-configuration-file}

以下の内容で`tidb-lightning.toml`ファイルを作成してください。

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
host = "${host}"            # e.g.: 172.16.32.1
port = "${port}"            # e.g.: 4000
user = "${user_name}"     # e.g.: "root"
password = "${password}"  # e.g.: "rootroot"
status-port = "${status-port}" # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
pd-addr = "${ip}:${port}" # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
```

設定ファイルの詳細については、 [TiDB Lightning のコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ4．インポートパフォーマンスの調整（オプション） {#step-4-tune-the-import-performance-optional}

TiDB Lightningは、サイズが約256MiBの均一なCSVファイルからデータをインポートする場合、最高のパフォーマンスを発揮します。しかし、単一の大きなCSVファイルからデータをインポートする場合、 TiDB Lightningはデフォルトでは1つのスレッドしか使用できないため、インポート速度が低下する可能性があります。

インポートを高速化するために、大きな CSV ファイルを小さなファイルに分割することができます。一般的な形式の CSV ファイルの場合、 TiDB Lightning がファイル全体を読み込む前に、各行の開始位置と終了位置を素早く特定するのは困難です。そのため、 TiDB Lightning はデフォルトでは CSV ファイルを自動的に分割しません。ただし、インポートする CSV ファイルが特定の形式要件を満たしている場合は、 `strict-format`モードを有効にすることができます。このモードでは、 TiDB Lightning は1 つの大きな CSV ファイルを約 256 MiB の複数のファイルに自動的に分割し、並列処理します。

> **Note:**
>
> CSVファイルが厳密なフォーマットに準拠していないにもかかわらず、 `strict-format`モードが誤って`true`に設定されている場合、複数行にわたるフィールドが2つのフィールドに分割されます。これにより解析が失敗し、 TiDB Lightningはエラーを報告せずに破損したデータをインポートしてしまう可能性があります。

厳密な形式のCSVファイルでは、各フィールドは1行のみを占めます。以下の要件を満たす必要があります。

-   区切り文字が空です。
-   各フィールドには CR ( `\r` ) または LF ( `\n` ) は含まれていません。

`terminator` `strict-format` } を明示的に指定する必要があります。

CSVファイルが上記の要件を満たしている場合は、次のように`strict-format`モードを有効にすることでインポートを高速化できます。

```toml
[mydumper]
strict-format = true
```

## ステップ5．データのインポート {#step-5-import-the-data}

インポートを開始するには、 `tidb-lightning`を実行します。コマンドラインでプログラムを起動すると、SIGHUP シグナルを受信した後にプロセスが予期せず終了する可能性があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例:

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

インポートが開始された後、以下のいずれかの方法でインポートの進行状況を確認できます。

-   ログ内のキーワード`progress`を`grep`することで、インポートの進行状況を確認できます。進行状況は、デフォルトでは 5 分ごとに更新されます。
-   [モニタリングダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進行状況を確認します。

TiDB Lightning はインポートが完了すると自動的に終了します。`tidb-lightning.log`の最後の行に`the whole procedure completed`が含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポート中にエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **Note:**
>
> インポートが成功したかどうかに関わらず、ログの最後の行には`tidb lightning exit`と表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するものではありません。

インポートが失敗した場合は、トラブルシューティングのために[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## その他のファイル形式 {#other-file-formats}

データソースが他の形式の場合、データソースからデータを移行するには、ファイル名の末尾に`.csv`を追加し、 `[mydumper.csv]`設定ファイルの`tidb-lightning.toml`セクションに適切な変更を加える必要があります。一般的な形式の場合の変更例を以下に示します。

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

## 次は？ {#what-s-next}

-   [CSVのサポートと制限事項](/tidb-lightning/tidb-lightning-data-source.md#csv)。

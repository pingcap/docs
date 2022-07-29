---
title: Migrate Data from CSV Files to TiDB
summary: Learn how to migrate data from CSV files to TiDB.
---

# CSVファイルからTiDBへのデータの移行 {#migrate-data-from-csv-files-to-tidb}

このドキュメントでは、CSVファイルからTiDBにデータを移行する方法について説明します。

TiDB Lightningは、CSVファイルおよびタブ区切り値（TSV）などの他の区切り文字形式からデータを読み取ることができます。その他のフラットファイルデータソースについては、このドキュメントを参照してデータをTiDBに移行することもできます。

## 前提条件 {#prerequisites}

-   [TiDB Lightningをインストールします](/migration-tools.md) 。
-   [TiDB Lightningに必要なターゲットデータベース権限を取得します](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database) 。

## 手順1.CSVファイルを準備します {#step-1-prepare-the-csv-files}

すべてのCSVファイルを同じディレクトリに配置します。すべてのCSVファイルを認識するためにTiDB Lightningが必要な場合、ファイル名は次の要件を満たしている必要があります。

-   CSVファイルにテーブル全体のデータが含まれている場合は、ファイルに`${db_name}.${table_name}.csv`という名前を付けます。
-   1つのテーブルのデータが複数のCSVファイルに分割されている場合は、これらのCSVファイルに数値のサフィックスを追加します。たとえば、 `${db_name}.${table_name}.003.csv` 。数字の接尾辞は連続していない場合がありますが、昇順である必要があります。また、すべてのサフィックスが同じ長さになるように、数値の前にゼロを追加する必要があります。

## 手順2.ターゲットテーブルスキーマを作成します {#step-2-create-the-target-table-schema}

CSVファイルにはスキーマ情報が含まれていないため、CSVファイルからTiDBにデータをインポートする前に、ターゲットテーブルスキーマを作成する必要があります。次の2つの方法のいずれかによって、ターゲットテーブルスキーマを作成できます。

-   **方法1** ： TiDB Lightningを使用してターゲットテーブルスキーマを作成します。

    必要なDDLステートメントを含むSQLファイルを作成します。

    -   `${db_name}-schema-create.sql`のファイルに`CREATE DATABASE`のステートメントを追加します。
    -   `${db_name}.${table_name}-schema.sql`のファイルに`CREATE TABLE`のステートメントを追加します。

-   **方法2** ：ターゲットテーブルスキーマを手動で作成します。

## ステップ3.構成ファイルを作成します {#step-3-create-the-configuration-file}

次の内容で`tidb-lightning.toml`のファイルを作成します。

{{< copyable "" >}}

```toml
[lightning]
# Log
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
# "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally.
backend = "local"
# Set the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

[mydumper]
# Directory of the data source.
data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup?region=us-west-2'.

# Defines CSV format.
[mydumper.csv]
# Field separator of the CSV file. Must not be empty. If the source file contains fields that are not string or numeric, such as binary, blob, or bit, it is recommended not to usesimple delimiters such as ",", and use an uncommon character combination like "|+|" instead.
separator = ','
# Delimiter. Can be zero or multiple characters.
delimiter = '"'
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

構成ファイルの詳細については、 [TiDB LightningConfiguration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 手順4.インポートパフォーマンスを調整します（オプション） {#step-4-tune-the-import-performance-optional}

約256MiBの均一サイズのCSVファイルからデータをインポートすると、 TiDB Lightningが最高のパフォーマンスで動作します。ただし、単一の大きなCSVファイルからデータをインポートする場合、 TiDB Lightningはデフォルトでインポートを処理するために1つのスレッドしか使用できないため、インポート速度が低下する可能性があります。

インポートを高速化するために、大きなCSVファイルを小さなファイルに分割できます。一般的な形式のCSVファイルの場合、 TiDB Lightningがファイル全体を読み取る前に、各行の開始位置と終了位置をすばやく見つけることは困難です。したがって、 TiDB LightningはデフォルトでCSVファイルを自動的に分割しません。ただし、インポートするCSVファイルが特定の形式の要件を満たしている場合は、 `strict-format`モードを有効にできます。このモードでは、 TiDB Lightningは1つの大きなCSVファイルをそれぞれ約256MiBの複数のファイルに自動的に分割し、それらを並行して処理します。

> **ノート：**
>
> CSVファイルが厳密な形式ではないが、誤って`strict-format`モードが`true`に設定されている場合、複数行にまたがるフィールドは2つのフィールドに分割されます。これにより、解析が失敗し、 TiDB Lightningがエラーを報告せずに破損したデータをインポートする可能性があります。

厳密な形式のCSVファイルでは、各フィールドは1行しか使用しません。次の要件を満たしている必要があります。

-   区切り文字は空です。
-   各フィールドには、CR（ `\r` ）またはLF（ `\n` ）は含まれていません。

CSVファイルが上記の要件を満たしている場合は、次のように`strict-format`モードを有効にすることでインポートを高速化できます。

```toml
[mydumper]
strict-format = true
```

## ステップ5.データをインポートします {#step-5-import-the-data}

インポートを開始するには、 `tidb-lightning`を実行します。コマンドラインでプログラムを起動すると、SIGHUPシグナルを受信した後、プロセスが予期せず終了する場合があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例えば：

{{< copyable "" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

インポートの開始後、次のいずれかの方法でインポートの進行状況を確認できます。

-   `grep`ログのキーワード`progress` 。デフォルトでは、進行状況は5分ごとに更新されます。
-   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。
-   [TiDB Lightningインターフェイス](/tidb-lightning/tidb-lightning-web-interface.md)で進捗状況を確認します。

TiDB Lightningがインポートを完了すると、自動的に終了します。ログ印刷`the whole procedure completed`の最後の5行が見つかった場合、インポートは成功しています。

> **ノート：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightningが正常に終了することを意味しますが、必ずしもインポートが成功したことを意味するわけではありません。

インポートが失敗した場合、トラブルシューティングについては[TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## その他のファイル形式 {#other-file-formats}

データソースが他の形式の場合、データソースからデータを移行するには、ファイル名を`.csv`で終了し、 `tidb-lightning.toml`の構成ファイルの`[mydumper.csv]`セクションで対応する変更を加える必要があります。一般的な形式の変更例は次のとおりです。

**TSV：**

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

**TPC-H DBGEN：**

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

## 次は何ですか {#what-s-next}

-   [CSVのサポートと制限](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md) 。

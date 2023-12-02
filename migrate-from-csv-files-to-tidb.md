---
title: Migrate Data from CSV Files to TiDB
summary: Learn how to migrate data from CSV files to TiDB.
---

# CSV ファイルから TiDB へのデータの移行 {#migrate-data-from-csv-files-to-tidb}

このドキュメントでは、CSV ファイルから TiDB にデータを移行する方法について説明します。

TiDB Lightning は、CSV ファイルおよびタブ区切り値 (TSV) などの他の区切り文字形式からデータを読み取ることができます。他のフラット ファイル データ ソースについては、このドキュメントを参照してデータを TiDB に移行することもできます。

## 前提条件 {#prerequisites}

-   [TiDB Lightningをインストールする](/migration-tools.md) 。
-   [TiDB Lightningに必要なターゲット データベース権限を取得します。](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database) 。

## ステップ 1. CSV ファイルを準備する {#step-1-prepare-the-csv-files}

すべての CSV ファイルを同じディレクトリに置きます。 TiDB Lightning がすべての CSV ファイルを認識する必要がある場合、ファイル名は次の要件を満たしている必要があります。

-   CSV ファイルにテーブル全体のデータが含まれている場合は、ファイルに`${db_name}.${table_name}.csv`という名前を付けます。
-   1 つのテーブルのデータが複数の CSV ファイルに分割されている場合は、これらの CSV ファイルに数字のサフィックスを追加します。たとえば、 `${db_name}.${table_name}.003.csv` 。数値接尾辞は連続していなくてもかまいませんが、昇順である必要があります。また、すべての接尾辞が同じ長さになるように、数値の前にゼロを追加する必要があります。

## ステップ 2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schema}

CSV ファイルにはスキーマ情報が含まれていないため、CSV ファイルから TiDB にデータをインポートする前に、ターゲット テーブル スキーマを作成する必要があります。次の 2 つの方法のいずれかでターゲット テーブル スキーマを作成できます。

-   **方法 1** : TiDB Lightningを使用してターゲット テーブル スキーマを作成します。

    必要な DDL ステートメントを含む SQL ファイルを作成します。

    -   `${db_name}-schema-create.sql`ファイルに`CREATE DATABASE`ステートメントを追加します。
    -   `${db_name}.${table_name}-schema.sql`ファイルに`CREATE TABLE`ステートメントを追加します。

-   **方法 2** : ターゲット テーブル スキーマを手動で作成します。

## ステップ 3. 構成ファイルを作成する {#step-3-create-the-configuration-file}

次の内容を含む`tidb-lightning.toml`ファイルを作成します。

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

## ステップ 4. インポートのパフォーマンスを調整する (オプション) {#step-4-tune-the-import-performance-optional}

約 256 MiB の均一サイズの CSV ファイルからデータをインポートすると、 TiDB Lightning は最高のパフォーマンスで動作します。ただし、単一の大きな CSV ファイルからデータをインポートする場合、 TiDB Lightning はデフォルトでインポートの処理に 1 つのスレッドしか使用できないため、インポート速度が遅くなる可能性があります。

インポートを高速化するために、大きな CSV ファイルを小さな CSV ファイルに分割できます。一般的な形式の CSV ファイルの場合、 TiDB Lightning がファイル全体を読み取る前に、各行の開始位置と終了位置をすばやく見つけるのは困難です。したがって、 TiDB Lightning はデフォルトでは CSV ファイルを自動的に分割しません。ただし、インポートする CSV ファイルが特定の形式要件を満たしている場合は、 `strict-format`モードを有効にすることができます。このモードでは、 TiDB Lightning は1 つの大きな CSV ファイルを自動的に複数のファイル (それぞれ約 256 MiB) に分割し、それらを並列処理します。

> **注記：**
>
> CSV ファイルが厳密な形式ではなく、誤って`strict-format`モードを`true`に設定すると、複数行にまたがるフィールドが 2 つのフィールドに分割されます。これにより解析が失敗し、 TiDB Lightning がエラーを報告せずに破損したデータをインポートする可能性があります。

厳密形式の CSV ファイルでは、各フィールドは 1 行のみを占めます。次の要件を満たしている必要があります。

-   区切り文字が空です。
-   各フィールドには CR ( `\r` ) または LF ( `\n` ) は含まれません。

CSV ファイルが上記の要件を満たしている場合は、次のように`strict-format`モードを有効にすることでインポートを高速化できます。

```toml
[mydumper]
strict-format = true
```

## ステップ 5. データをインポートする {#step-5-import-the-data}

インポートを開始するには、 `tidb-lightning`を実行します。コマンド ラインでプログラムを起動すると、SIGHUP シグナルの受信後にプロセスが予期せず終了する可能性があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例えば：

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

インポートの開始後、次のいずれかの方法でインポートの進行状況を確認できます。

-   `grep`ログ内のキーワード`progress` 。デフォルトでは、進行状況は 5 分ごとに更新されます。
-   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認します。
-   [TiDB Lightning Web インターフェース](/tidb-lightning/tidb-lightning-web-interface.md)で進捗状況を確認します。

TiDB Lightning はインポートを完了すると、自動的に終了します。最後の行に`tidb-lightning.log` `the whole procedure completed`含まれているかどうかを確認します。 「はい」の場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処します。

> **注記：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、インポートが成功したことを必ずしも意味するわけではありません。

インポートが失敗した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)のトラブルシューティングを参照してください。

## 他のファイル形式 {#other-file-formats}

データ ソースが他の形式である場合、データ ソースからデータを移行するには、ファイル名の末尾を`.csv`にし、構成ファイル`tidb-lightning.toml`の`[mydumper.csv]`セクションで対応する変更を行う必要があります。一般的な形式の変更例を次に示します。

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

## 次は何ですか {#what-s-next}

-   [CSV のサポートと制限](/tidb-lightning/tidb-lightning-data-source.md#csv) 。

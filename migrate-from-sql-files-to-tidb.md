---
title: Migrate Data from SQL Files to TiDB
summary: SQLファイルからTiDBへのデータ移行方法を学びましょう。
---

# SQLファイルからTiDBへのデータ移行 {#migrate-data-from-sql-files-to-tidb}

このドキュメントでは、TiDB Lightningを使用して MySQL SQL ファイルから TiDB にデータを移行する方法について説明します。 MySQL SQL ファイルを生成する方法については、 [Dumplingを使用してSQLファイルにエクスポートする](/dumpling-overview.md#export-to-sql-files)にエクスポートするを参照してください。

## 前提条件 {#prerequisites}

-   [TiUPを使用してTiDB Lightningをインストールする](/migration-tools.md)
-   [TiDB Lightningの対象データベースに必要な権限を付与します](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)

## ステップ1. SQLファイルを準備する {#step-1-prepare-sql-files}

すべての SQL ファイルを`/data/my_datasource/`や`s3://my-bucket/sql-backup`のように同じディレクトリに配置してください。TiDB Lightning は、このディレクトリとそのサブディレクトリ内のすべての`.sql`ファイルを再帰的に検索します。

## ステップ2. 対象テーブルのスキーマを定義する {#step-2-define-the-target-table-schema}

TiDBにデータをインポートするには、対象データベースのテーブルスキーマを作成する必要があります。

Dumplingを使用してデータをエクスポートする場合、テーブルスキーマファイルは自動的にエクスポートされます。その他の方法でエクスポートされたデータについては、以下のいずれかの方法でテーブルスキーマを作成できます。

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
# "local": Default. The local backend is used to import large volumes of data (around or more than 1 TiB). During the import, the target TiDB cluster cannot provide any service.
# "tidb": The "tidb" backend can also be used to import small volumes of data (less than 1 TiB). During the import, the target TiDB cluster can provide service normally. For the information about backend mode, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.

backend = "local"
# Sets the temporary storage directory for the sorted key-value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# Directory of the data source
data-source-dir = "${data-path}" # Local or S3 path, such as 's3://my-bucket/sql-backup'

[tidb]
# The information of target cluster
host = "${host}"              # For example, 172.16.32.1
port = "${port}"              # For example, 4000
user = "${user_name}"         # For example, "root"
password = "${password}"      # For example, "rootroot"
status-port = "${status-port}"  # During the import process, TiDB Lightning needs to obtain table schema information from the "Status Port" of TiDB, such as 10080.
pd-addr = "${ip}:${port}"     # The address of the cluster's PD. TiDB Lightning obtains some information through PD, such as 172.16.31.3:2379. When backend = "local", you must correctly specify status-port and pd-addr. Otherwise, the import will encounter errors.
```

設定ファイルの詳細については、 [TiDB Lightning のコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ4．データのインポート {#step-4-import-the-data}

インポートを開始するには、 `tidb-lightning`を実行してください。コマンドラインでプログラムを起動すると、 `SIGHUP`シグナルによってプログラムが終了する場合があります。この場合は、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。

S3からデータをインポートする場合は、アカウントの`SecretKey`と`AccessKey`を環境変数として渡す必要があります。このアカウントには、S3バックエンドストレージへのアクセス権限が付与されています。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

TiDB Lightning は`~/.aws/credentials`からの認証情報ファイルの読み取りもサポートしています。

インポートが開始された後、以下のいずれかの方法で進行状況を確認できます。

-   ログ内のキーワード`progress`を`grep`することで、インポートの進行状況を確認できます。このログはデフォルトで 5 分ごとに更新されます。
-   Grafana ダッシュボードを使用します。詳細については、 [TiDB Lightningモニタリング](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。

インポートが完了すると、 TiDB Lightning は自動的に終了します。`tidb-lightning.log`の最後の行に`the whole procedure completed`が含まれているかどうかを確認してください。含まれている場合は、インポートは成功です。含まれていない場合は、インポート中にエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **注記：**
>
> インポートが成功したかどうかに関わらず、最後の行には`tidb lightning exit`と表示されます。これは、 TiDB Lightning が正常に終了したことを意味するだけで、タスクが完了したことを意味するものではありません。インポート処理中に問題が発生した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してトラブルシューティングを行ってください。

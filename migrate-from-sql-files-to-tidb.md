---
title: Migrate Data from SQL Files to TiDB
summary: Learn how to migrate data from SQL files to TiDB.
---

# SQL ファイルから TiDB へのデータの移行 {#migrate-data-from-sql-files-to-tidb}

このドキュメントでは、 TiDB Lightningを使用して MySQL SQL ファイルから TiDB にデータを移行する方法について説明します。 MySQL SQL ファイルの生成方法については、 [Dumplingを使用して SQL ファイルにエクスポートする](/dumpling-overview.md#export-to-sql-files)を参照してください。

## 前提条件 {#prerequisites}

-   [TiUPを使用してTiDB Lightningをインストールする](/migration-tools.md)
-   [TiDB Lightningのターゲット データベースに必要な権限を付与します。](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)

## ステップ 1. SQL ファイルを準備する {#step-1-prepare-sql-files}

すべての SQL ファイルを同じディレクトリ ( `/data/my_datasource/`や`s3://my-bucket/sql-backup`など) に置きます。 TiDB Lightning は、このディレクトリとそのサブディレクトリ内の`.sql`ファイルすべてを再帰的に検索します。

## ステップ 2. ターゲットテーブルスキーマを定義する {#step-2-define-the-target-table-schema}

TiDB にデータをインポートするには、ターゲット データベースのテーブル スキーマを作成する必要があります。

Dumplingを使用してデータをエクスポートすると、テーブル スキーマ ファイルが自動的にエクスポートされます。他の方法でエクスポートされたデータの場合は、次のいずれかの方法でテーブル スキーマを作成できます。

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
host = ${host}                # For example, 172.16.32.1
port = ${port}                # For example, 4000
user = "${user_name}"         # For example, "root"
password = "${password}"      # For example, "rootroot"
status-port = ${status-port}  # During the import process, TiDB Lightning needs to obtain table schema information from the "Status Port" of TiDB, such as 10080.
pd-addr = "${ip}:${port}"     # The address of the cluster's PD. TiDB Lightning obtains some information through PD, such as 172.16.31.3:2379. When backend = "local", you must correctly specify status-port and pd-addr. Otherwise, the import will encounter errors.
```

構成ファイルの詳細については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ 4. データをインポートする {#step-4-import-the-data}

インポートを開始するには、 `tidb-lightning`を実行します。コマンド ラインでプログラムを起動すると、 `SIGHUP`シグナルが原因でプログラムが終了する可能性があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。

S3 からデータをインポートする場合は、アカウントの`SecretKey`と`AccessKey`を環境変数として渡す必要があります。このアカウントには、S3 バックエンドstorageにアクセスする権限があります。

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

TiDB Lightning は、 `~/.aws/credentials`からの認証情報ファイルの読み取りもサポートしています。

インポートが開始されたら、次のいずれかの方法で進行状況を確認できます。

-   デフォルトでは 5 分ごとに更新される`grep`ログで`progress`キーワードを検索します。
-   Grafana ダッシュボードを使用します。詳細は[TiDB Lightning監視](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。
-   Webインターフェイスを使用します。詳細は[TiDB LightningWeb インターフェイス](/tidb-lightning/tidb-lightning-web-interface.md)を参照してください。

インポートが完了すると、 TiDB Lightning は自動的に終了します。最後の行に`tidb-lightning.log` `the whole procedure completed`含まれているかどうかを確認します。 「はい」の場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処します。

> **注記：**
>
> インポートが成功したかどうかに関係なく、最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味するだけで、タスクが完了したことを意味するわけではありません。インポート プロセス中に問題が発生した場合は、トラブルシューティングについて[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

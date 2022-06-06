---
title: Migrate Data from SQL Files to TiDB
summary: Learn how to migrate data from SQL files to TiDB.
---

# SQLファイルからTiDBへのデータの移行 {#migrate-data-from-sql-files-to-tidb}

このドキュメントでは、TiDBLightningを使用してMySQLSQLファイルからTiDBにデータを移行する方法について説明します。 MySQL SQLファイルの生成方法については、 [Dumplingを使用してSQLファイルにエクスポート](/dumpling-overview.md#export-to-sql-files)を参照してください。

## 前提条件 {#prerequisites}

-   [TiUPを使用してTiDBLightningをインストールする](/migration-tools.md)
-   [TiDBLightningのターゲットデータベースに必要な権限を付与します](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)

## ステップ1.SQLファイルを準備します {#step-1-prepare-sql-files}

すべてのSQLファイルを`/data/my_datasource/`や`s3://my-bucket/sql-backup?region=us-west-2`などの同じディレクトリに配置します。 TiDB Lightingは、このディレクトリとそのサブディレクトリ内の`.sql`のファイルすべてを再帰的に検索します。

## 手順2.ターゲットテーブルスキーマを定義する {#step-2-define-the-target-table-schema}

データをTiDBにインポートするには、ターゲットデータベースのテーブルスキーマを作成する必要があります。

Dumplingを使用してデータをエクスポートする場合、テーブルスキーマファイルは自動的にエクスポートされます。他の方法でエクスポートされたデータの場合、次のいずれかの方法でテーブルスキーマを作成できます。

-   **方法1** ：TiDBLightningを使用してターゲットテーブルスキーマを作成します。

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
# "local"：Default. The local backend is used to import large volumes of data (around or more than 1 TiB). During the import, the target TiDB cluster cannot provide any service.
# "tidb"：The "tidb" backend can also be used to import small volumes of data (less than 1 TiB). During the import, the target TiDB cluster can provide service normally. For the information about backend mode, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.

backend = "local"
# Sets the temporary storage directory for the sorted key-value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# Directory of the data source
data-source-dir = "${data-path}" # Local or S3 path, such as 's3://my-bucket/sql-backup?region=us-west-2'

[tidb]
# The information of target cluster
host = ${host}                # For example, 172.16.32.1
port = ${port}                # For example, 4000
user = "${user_name}"         # For example, "root"
password = "${password}"      # For example, "rootroot"
status-port = ${status-port}  # During the import process, TiDB Lightning needs to obtain table schema information from the "Status Port" of TiDB, such as 10080.
pd-addr = "${ip}:${port}"     # The address of the cluster's PD. TiDB Lightning obtains some information through PD, such as 172.16.31.3:2379. When backend = "local", you must correctly specify status-port and pd-addr. Otherwise, the import will encounter errors.
```

構成ファイルの詳細については、 [TiDBLightningConfiguration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ4.データをインポートします {#step-4-import-the-data}

インポートを開始するには、 `tidb-lightning`を実行します。コマンドラインでプログラムを起動すると、 `SIGHUP`信号のためにプログラムが終了する場合があります。この場合、 `nohup`または`screen`のツールを使用してプログラムを実行することをお勧めします。

S3からデータをインポートする場合は、アカウントの`SecretKey`と`AccessKey`を環境変数として渡す必要があります。アカウントには、S3バックエンドストレージにアクセスするためのアクセス許可があります。

{{< copyable "" >}}

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
```

TiDB Lightningは、 `~/.aws/credentials`からのクレデンシャルファイルの読み取りもサポートしています。

インポートが開始されたら、次のいずれかの方法で進行状況を確認できます。

-   デフォルトで5分ごとに更新される`grep`ログで`progress`キーワードを検索します。
-   Grafanaダッシュボードを使用します。詳細については、 [TiDB Lightning Monitoring](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。
-   Webインターフェイスを使用します。詳細については、 [TiDBLightningWebインターフェイス](/tidb-lightning/tidb-lightning-web-interface.md)を参照してください。

インポートが完了すると、TiDBLightningは自動的に終了します。ログの最後の5行に`the whole procedure completed`が含まれている場合は、インポートが正常に完了したことを意味します。

> **ノート：**
>
> インポートが成功したかどうかに関係なく、最後の行には`tidb lightning exit`が表示されます。これは、TiDB Lightningが正常に終了したことを意味するだけであり、タスクの完了ではありません。インポートプロセス中に問題が発生した場合は、トラブルシューティングについて[TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

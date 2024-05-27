---
title: Migrate Data from Parquet Files to TiDB
summary: parquet ファイルから TiDB にデータを移行する方法を学びます。
---

# Parquet ファイルから TiDB へのデータの移行 {#migrate-data-from-parquet-files-to-tidb}

このドキュメントでは、Apache Hive から parquet ファイルを生成する方法と、 TiDB Lightningを使用して parquet ファイルから TiDB にデータを移行する方法について説明します。

Amazon Auroraから parquet ファイルをエクスポートする場合は、 [Amazon Auroraから TiDB にデータを移行する](/migrate-aurora-to-tidb.md)を参照してください。

## 前提条件 {#prerequisites}

-   [TiUPを使用してTiDB Lightningをインストールする](/migration-tools.md) 。
-   [TiDB Lightningに必要なターゲットデータベース権限を取得する](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database) 。

## ステップ1. parquetファイルを準備する {#step-1-prepare-the-parquet-files}

このセクションでは、 TiDB Lightningで読み取ることができる parquet ファイルを Hive からエクスポートする方法について説明します。

Hive 内の各テーブルは、 `STORED AS PARQUET LOCATION '/path/in/hdfs'`注釈することで parquet ファイルにエクスポートできます。したがって、 `test`という名前のテーブルをエクスポートする必要がある場合は、次の手順を実行します。

1.  Hive で次の SQL ステートメントを実行します。

    ```sql
    CREATE TABLE temp STORED AS PARQUET LOCATION '/path/in/hdfs'
    AS SELECT * FROM test;
    ```

    上記のステートメントを実行すると、テーブル データが HDFS システムに正常にエクスポートされます。

2.  `hdfs dfs -get`コマンドを使用して、parquet ファイルをローカル ファイル システムにエクスポートします。

    ```shell
    hdfs dfs -get /path/in/hdfs /path/in/local
    ```

    エクスポートが完了したら、HDFS 内のエクスポートされた parquet ファイルを削除する必要がある場合は、一時テーブル ( `temp` ) を直接削除できます。

    ```sql
    DROP TABLE temp;
    ```

3.  Hive からエクスポートされた parquet ファイルには`.parquet`サフィックスが付いておらず、 TiDB Lightningで正しく識別できない可能性があります。したがって、ファイルをインポートする前に、エクスポートしたファイルの名前を変更し、 `.parquet`サフィックスを追加して、完全なファイル名をTiDB Lightningが認識できる形式 (例: `${db_name}. ${table_name}.parquet` ) に変更する必要があります。ファイルの種類とパターンの詳細については、 [TiDB Lightningデータソース](/tidb-lightning/tidb-lightning-data-source.md)を参照してください。また、正しい[カスタマイズされた表現](/tidb-lightning/tidb-lightning-data-source.md#match-customized-files)を設定することで、データ ファイルを一致させることもできます。

4.  すべての parquet ファイルを`/data/my_datasource/`または`s3://my-bucket/sql-backup`などの統合ディレクトリに配置します。TiDB TiDB Lightning は、このディレクトリとそのサブディレクトリ内の`.parquet`つのファイルすべてを再帰的に検索します。

## ステップ2. ターゲットテーブルスキーマを作成する {#step-2-create-the-target-table-schema}

parquet ファイルから TiDB にデータをインポートする前に、ターゲット テーブル スキーマを作成する必要があります。ターゲット テーブル スキーマは、次の 2 つの方法のいずれかで作成できます。

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
backend = "local"
# "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally.
# For more information on import mode, refer to <https://docs.pingcap.com/tidb/stable/tidb-lightning-overview#tidb-lightning-architecture>
# Set the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# Directory of the data source.
data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup'.

[tidb]
# The target cluster.
host = ${host}            # e.g.: 172.16.32.1
port = ${port}            # e.g.: 4000
user = "${user_name}"     # e.g.: "root"
password = "${password}"  # e.g.: "rootroot"
status-port = ${status-port} # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
pd-addr = "${ip}:${port}" # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
```

設定ファイルの詳細については、 [TiDB Lightning構成](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ4. データをインポートする {#step-4-import-the-data}

1.  `tidb-lightning`実行します。

    -   Amazon S3 からデータをインポートする場合は、 TiDB Lightning を実行する前に、S3 バックエンドstorageにアクセスする権限を持つアカウントの SecretKey と AccessKey を環境変数として設定する必要があります。

        ```shell
        export AWS_ACCESS_KEY_ID=${access_key}
        export AWS_SECRET_ACCESS_KEY=${secret_key}
        ```

        前述の方法に加えて、 TiDB Lightning は`~/.aws/credentials`からの資格情報ファイルの読み取りもサポートしています。

    -   プログラムをコマンドラインで起動すると、 `SIGHUP`シグナルを受信した後にプロセスが予期せず終了することがあります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例:

        ```shell
        nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
        ```

2.  インポートが開始されたら、次のいずれかの方法でインポートの進行状況を確認できます。

    -   `grep`使用してログ内でキーワード`progress`を検索します。デフォルトでは、進行状況は 5 分ごとに更新されます。
    -   [監視ダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)の進捗状況を確認します。
    -   [TiDB Lightningウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)の進捗状況を確認します。

    TiDB Lightning はインポートを完了すると自動的に終了します。

3.  インポートが成功したかどうかを確認します。

    最後の行の`tidb-lightning.log`に`the whole procedure completed`含まれているかどうかを確認します。含まれている場合は、インポートは成功です。含まれていない場合は、インポートでエラーが発生します。エラー メッセージの指示に従ってエラーに対処してください。

    > **注記：**
    >
    > インポートが成功したかどうかに関係なく、ログの最後の行には`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するわけではありません。

インポートに失敗した場合は、トラブルシューティングについては[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

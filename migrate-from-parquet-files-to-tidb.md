---
title: Migrate Data from Parquet Files to TiDB
summary: ParquetファイルからTiDBへのデータ移行方法を学びましょう。
---

# ParquetファイルからTiDBへのデータ移行 {#migrate-data-from-parquet-files-to-tidb}

このドキュメントでは、Apache Hive から Parquet ファイルを生成する方法と、 TiDB Lightningを使用して Parquet ファイルから TiDB にデータを移行する方法について説明します。

Amazon AuroraからParquetファイルをエクスポートする場合は、 [Amazon AuroraからTiDBへデータを移行する](/migrate-aurora-to-tidb.md)を参照してください。

## 前提条件 {#prerequisites}

-   [TiUPを使用してTiDB Lightningをインストールする](/migration-tools.md)。
-   [TiDB Lightningに必要なターゲットデータベース権限を取得します。](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)

## ステップ1. Parquetファイルを用意する {#step-1-prepare-the-parquet-files}

このセクションでは、 TiDB Lightningで読み取れる Parquet ファイルを Hive からエクスポートする方法について説明します。

Hive の各テーブルは`STORED AS PARQUET LOCATION '/path/in/hdfs'`という注釈を付けることで、Parquet ファイルにエクスポートできます。したがって、 `test`という名前のテーブルをエクスポートする必要がある場合は、次の手順を実行します。

1.  Hiveで以下のSQL文を実行してください。

    ```sql
    CREATE TABLE temp STORED AS PARQUET LOCATION '/path/in/hdfs'
    AS SELECT * FROM test;
    ```

    上記のステートメントを実行すると、テーブルデータはHDFSシステムに正常にエクスポートされます。

2.  `hdfs dfs -get`コマンドを使用して、Parquet ファイルをローカルファイルシステムにエクスポートします。

    ```shell
    hdfs dfs -get /path/in/hdfs /path/in/local
    ```

    エクスポートが完了した後、HDFS 内のエクスポートされた Parquet ファイルを削除する必要がある場合は、一時テーブル ( `temp` ) を直接削除できます。

    ```sql
    DROP TABLE temp;
    ```

3.  Hive からエクスポートされた Parquet ファイルには`.parquet`サフィックスが付いていない場合があり、 TiDB Lightningで正しく識別できない可能性があります。そのため、ファイルをインポートする前に、エクスポートされたファイルの名前を変更し、 `.parquet`サフィックスを追加して、ファイル名全体をTiDB Lightning が認識する形式（例: `${db_name}. ${table_name}.parquet`に変更する必要があります。ファイルの種類とパターンに関する詳細については、 [TiDB Lightningデータソース](/tidb-lightning/tidb-lightning-data-source.md)を参照してください。また、正しい[カスタマイズされた表現](/tidb-lightning/tidb-lightning-data-source.md#match-customized-files)を設定することでデータ ファイルを一致させることもできます。

4.  すべての Parquet ファイルを、例えば`/data/my_datasource/`や`s3://my-bucket/sql-backup`のような単一のディレクトリに配置してください。TiDB Lightning は、このディレクトリとそのサブディレクトリ内のすべての`.parquet`ファイルを再帰的に検索します。

## ステップ2. 対象テーブルのスキーマを作成する {#step-2-create-the-target-table-schema}

ParquetファイルからTiDBにデータをインポートする前に、ターゲットテーブルスキーマを作成する必要があります。ターゲットテーブルスキーマは、以下の2つの方法のいずれかで作成できます。

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
host = "${host}"            # e.g.: 172.16.32.1
port = "${port}"            # e.g.: 4000
user = "${user_name}"     # e.g.: "root"
password = "${password}"  # e.g.: "rootroot"
status-port = "${status-port}" # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
pd-addr = "${ip}:${port}" # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
```

設定ファイルの詳細については、 [TiDB Lightning の構成](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## ステップ4．データのインポート {#step-4-import-the-data}

1.  `tidb-lightning`を実行します。

    -   Amazon S3 からデータをインポートする場合は、 TiDB Lightning を実行する前に、S3 バックエンドstorageへのアクセス権限を持つアカウントの SecretKey と AccessKey を環境変数として設定する必要があります。

        ```shell
        export AWS_ACCESS_KEY_ID=${access_key}
        export AWS_SECRET_ACCESS_KEY=${secret_key}
        ```

        前述の方法に加えて、 TiDB Lightning は`~/.aws/credentials`から認証情報ファイルを読み取ることもサポートしています。

    -   コマンドラインでプログラムを起動すると、 `SIGHUP`シグナルを受信した後にプロセスが予期せず終了する可能性があります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例:

        ```shell
        nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
        ```

2.  インポートが開始された後、以下のいずれかの方法でインポートの進行状況を確認できます。

    -   ログ内のキーワード`progress`を`grep`することで、インポートの進行状況を確認できます。進行状況は、デフォルトでは 5 分ごとに更新されます。
    -   [モニタリングダッシュボード](/tidb-lightning/monitor-tidb-lightning.md)で進捗状況を確認してください。
    -   [TiDB Lightning Webインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)で進行状況を確認します。

    TiDB Lightningはインポートが完了すると自動的に終了します。

3.  インポートが成功したかどうか確認してください。

    最終行に`tidb-lightning.log`に`the whole procedure completed`が含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポート中にエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

    > **注記：**
    >
    > インポートが成功したかどうかに関わらず、ログの最後の行には`tidb lightning exit`と表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するものではありません。

インポートが失敗した場合は、トラブルシューティングのために[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

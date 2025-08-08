---
title: Back up and Restore Data Using Dumpling and TiDB Lightning
summary: DumplingとTiDB Lightningを使用して TiDB の完全なデータをバックアップおよび復元する方法を学びます。
---

# DumplingとTiDB Lightning を使用してデータをバックアップおよび復元する {#back-up-and-restore-data-using-dumpling-and-tidb-lightning}

このドキュメントでは、 DumplingとTiDB Lightning を使用して TiDB の完全なデータをバックアップおよび復元する方法を紹介します。

少量のデータ（たとえば、50 GiB 未満）をバックアップする必要があり、高いバックアップ速度を必要としない場合は、 [Dumpling](/dumpling-overview.md)使用して TiDB データベースからデータをエクスポートし、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータを別の TiDB データベースに復元できます。

より大きなデータベースをバックアップする必要がある場合は、 [BR](/br/backup-and-restore-overview.md)使用することをお勧めします。Dumplingを使用して大きなデータベースをエクスポートすることもできますが、 BRの方がより適したツールです。

## 要件 {#requirements}

-   Dumplingをインストール:

    ```shell
    tiup install dumpling
    ```

-   TiDB Lightningをインストールします:

    ```shell
    tiup install tidb-lightning
    ```

-   [Dumplingに必要なソースデータベース権限を付与します](/dumpling-overview.md#export-data-from-tidb-or-mysql)

-   [TiDB Lightningに必要なターゲットデータベース権限を付与します](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database)

## リソース要件 {#resource-requirements}

**オペレーティングシステム**：このドキュメントの例では、新規のCentOS 7インスタンスを使用しています。仮想マシンはローカルホストまたはクラウドにデプロイできます。TiDB TiDB Lightningはデフォルトで必要なCPUリソースを消費するため、専用サーバーにデプロイすることをお勧めします。これが不可能な場合は、他のTiDBコンポーネント（例えば`tikv-server` ）と共に単一のサーバーにデプロイし、 TiDB LightningからのCPU使用量を制限するために`region-concurrency`を設定することができます。通常、サイズは論理CPUの75%に設定できます。

**メモリとCPU** ： TiDB Lightningは多くのリソースを消費するため、64GiB以上のメモリと32個以上のCPUコアを割り当てることをお勧めします。最高のパフォーマンスを得るには、CPUコアとメモリ（GiB）の比率が1:2以上であることを確認してください。

**ディスク容量**:

外部storageとしては、Amazon S3、Google Cloud Storage（GCS）、またはAzure Blob Storageの使用をお勧めします。これらのクラウドstorageを使用すれば、ディスク容量に制限されることなく、バックアップファイルを迅速に保存できます。

1 つのバックアップ タスクのデータをローカル ディスクに保存する必要がある場合は、次の制限に注意してください。

-   Dumpling には、データソース全体（またはエクスポートする上流テーブルすべて）を保存できるディスク容量が必要です。必要な容量を計算するには、 [下流のstorageスペース要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)参照してください。
-   インポート中、 TiDB Lightning はソートされたキーと値のペアを保存するために一時的なスペースを必要とします。ディスク容量は、データソースの最大の単一テーブルを保存できる十分な量である必要があります。

**注意**: MySQL からDumplingによってエクスポートされる正確なデータ量を計算することは困難ですが、次の SQL 文を使用して`information_schema.tables`テーブルの`DATA_LENGTH`フィールドを要約することで、データ量を見積もることができます。

```sql
-- Calculate the size of all schemas
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- Calculate the 5 largest tables
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```

### ターゲット TiKV クラスターのディスク容量 {#disk-space-for-the-target-tikv-cluster}

ターゲットTiKVクラスターには、インポートしたデータを保存するための十分なディスク容量が必要です。1 [標準的なハードウェア要件](/hardware-and-software-requirements.md)加えて、ターゲットTiKVクラスターのstorage容量**は、データソースのサイズ × <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカ数</a>× 2**よりも大きくなければなりません。例えば、クラスターがデフォルトで3つのレプリカを使用する場合、ターゲットTiKVクラスターには、データソースのサイズの6倍よりも大きなstorage容量が必要です。式に x 2 が含まれているのは、以下の理由によるものです。

-   インデックスは追加のスペースを占める可能性があります。
-   RocksDB には空間増幅効果があります。

## Dumplingを使用して完全なデータをバックアップする {#use-dumpling-to-back-up-full-data}

1.  次のコマンドを実行して、TiDB から Amazon S3 の`s3://my-bucket/sql-backup`に完全なデータをエクスポートします。

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup'
    ```

    DumplingはデフォルトでSQLファイルにデータをエクスポートします。1オプションを追加することで、 `--filetype`のファイル形式を指定できます。

    Dumplingのその他の構成については、 [Dumplingのオプションリスト](/dumpling-overview.md#option-list-of-dumpling)参照してください。

2.  エクスポートが完了すると、ディレクトリ`s3://my-bucket/sql-backup`内のバックアップ ファイルを表示できます。

## TiDB Lightningを使用して完全なデータを復元する {#use-tidb-lightning-to-restore-full-data}

1.  `tidb-lightning.toml`ファイルを編集して、 Dumplingを使用して`s3://my-bucket/sql-backup`からバックアップされた完全なデータをターゲットの TiDB クラスターにインポートします。

    ```toml
    [lightning]
    # log
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
    # "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally. For more information on the backends, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.
    backend = "local"
    # Sets the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # The data source directory. The same directory where Dumpling exports data in "Use Dumpling to back up full data".
    data-source-dir = "${data-path}" #  A local path or S3 path. For example, 's3://my-bucket/sql-backup'

    [tidb]
    # The target TiDB cluster information.
    host = ${host}                # e.g.: 172.16.32.1
    port = ${port}                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = ${status-port}  # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
    pd-addr = "${ip}:${port}"     # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    TiDB Lightning構成の詳細については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

2.  `tidb-lightning`実行してインポートを開始します。コマンドラインでプログラムを直接起動すると、 `SIGHUP`シグナルを受け取った後にプロセスが予期せず終了する可能性があります。その場合は、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例:

    S3からデータをインポートする場合は、S3storageパスへのアクセス権を持つSecretKeyとAccessKeyを環境変数としてTiDB Lightningノードに渡します。また、 `~/.aws/credentials`から認証情報を読み取ることもできます。

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  インポート開始後、ログでキーワード`progress` `grep` 、インポートの進行状況を確認できます。デフォルトでは、進行状況は5分ごとに更新されます。

4.  TiDB Lightningはインポートを完了すると自動的に終了します。最後の行の`tidb-lightning.log`に`the whole procedure completed`含まれているかどうかを確認してください。含まれている場合はインポートが成功しています。含まれていない場合は、インポートでエラーが発生しました。エラーメッセージの指示に従ってエラーに対処してください。

> **注記：**
>
> インポートが成功したかどうかにかかわらず、ログの最後の行には`tidb lightning exit`表示されます。これはTiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するわけではありません。

インポートに失敗した場合は、トラブルシューティングについては[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

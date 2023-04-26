---
title: Back up and Restore Data Using Dumpling and TiDB Lightning
summary: Learn how to use Dumpling and TiDB Lightning to back up and restore full data of TiDB.
---

# DumplingとTiDB Lightningを使用したデータのバックアップと復元 {#back-up-and-restore-data-using-dumpling-and-tidb-lightning}

このドキュメントでは、 DumplingとTiDB Lightning を使用して TiDB の全データをバックアップおよび復元する方法を紹介します。

少量のデータ (たとえば、50 GB 未満) をバックアップする必要があり、高速なバックアップ速度を必要としない場合は、 [Dumpling](/dumpling-overview.md)を使用して TiDB データベースからデータをエクスポートし、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してそのデータを別の TiDB にインポートできます。データベース。バックアップと復元の詳細については、 [TiDB のバックアップと復元の概要](/br/backup-and-restore-overview.md)を参照してください。

## 要件 {#requirements}

-   Dumpling をインストールして起動します。

    ```shell
    tiup install dumpling && tiup dumpling
    ```

-   TiDB Lightning をインストールして起動します。

    ```shell
    tiup install tidb lightning && tiup tidb lightning
    ```

-   [Dumplingに必要なソース データベース権限を付与する](/dumpling-overview.md#export-data-from-tidb-or-mysql)

-   [TiDB Lightningに必要なターゲット データベース権限を付与する](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database)

## リソース要件 {#resource-requirements}

**オペレーティング システム**: このドキュメントの例では、新しい CentOS 7 インスタンスを使用しています。仮想マシンは、ローカル ホストまたはクラウドにデプロイできます。 TiDB Lightning はデフォルトで必要なだけ多くの CPU リソースを消費するため、専用サーバーにデプロイすることをお勧めします。これが不可能な場合は、他の TiDB コンポーネント (たとえば`tikv-server` ) と一緒に単一のサーバーにデプロイし、 `region-concurrency`を構成してTiDB Lightningからの CPU 使用を制限できます。通常、サイズは論理 CPU の 75% に設定できます。

**メモリと CPU** : TiDB Lightning は大量のリソースを消費するため、64 GiB を超えるメモリと 32 を超える CPU コアを割り当てることをお勧めします。最高のパフォーマンスを得るには、CPU コアとメモリ(GiB) の比率が 1:2 を超えていることを確認してください。

**ディスク容量**:

外部storageとして、Amazon S3、Google Cloud Storage (GCS)、または Azure Blob Storage を使用することをお勧めします。このようなクラウドstorageを使用すると、ディスク容量に制限されることなく、バックアップ ファイルをすばやく保存できます。

1 つのバックアップ タスクのデータをローカル ディスクに保存する必要がある場合は、次の制限事項に注意してください。

-   Dumpling には、データ ソース全体を格納できる (またはエクスポートするすべてのアップストリーム テーブルを格納できる) ディスク領域が必要です。必要なスペースを計算するには、 [ダウンストリームのstorage容量要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)を参照してください。
-   インポート中、 TiDB Lightning はソートされたキーと値のペアを保存するための一時的なスペースを必要とします。ディスク領域は、データ ソースから最大の単一テーブルを保持するのに十分なはずです。

**注**: Dumplingによって MySQL からエクスポートされた正確なデータ ボリュームを計算することは困難ですが、次の SQL ステートメントを使用して`information_schema.tables`テーブルの`data-length`フィールドを要約することにより、データ ボリュームを見積もることができます。

```sql
/* Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;

/* Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_name,table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM from information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY SUM DESC LIMIT 5;
```

### ターゲット TiKV クラスターのディスク容量 {#disk-space-for-the-target-tikv-cluster}

ターゲットの TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。 [標準のハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲット TiKV クラスターのstorage容量は**、データ ソースのサイズ x <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカの数</a>x 2**より大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターには、データ ソースのサイズの 6 倍を超えるstorageスペースが必要です。次の理由により、式には x 2 があります。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDB には空間増幅効果があります。

## Dumpling を使用して完全なデータをバックアップする {#use-dumpling-to-back-up-full-data}

1.  次のコマンドを実行して、TiDB から Amazon S3 の`s3://my-bucket/sql-backup`に完全なデータをエクスポートします。

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup'
    ```

    Dumpling は、デフォルトで SQL ファイルにデータをエクスポートします。 `--filetype`オプションを追加すると、別のファイル形式を指定できます。

    Dumplingのその他の構成については、 [Dumplingのオプション一覧](/dumpling-overview.md#option-list-of-dumpling)を参照してください。

2.  エクスポートが完了すると、ディレクトリ内のバックアップ ファイルを表示できます`s3://my-bucket/sql-backup` 。

## TiDB Lightning を使用して完全なデータを復元する {#use-tidb-lightning-to-restore-full-data}

1.  `tidb-lightning.toml`ファイルを編集して、 `s3://my-bucket/sql-backup`からDumplingを使用してバックアップされた完全なデータをターゲット TiDB クラスターにインポートします。

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

2.  `tidb-lightning`を実行してインポートを開始します。コマンド ラインでプログラムを直接起動すると、プロセスが`SIGHUP`シグナルを受信した後に予期せず終了することがあります。この場合、 `nohup`または`screen`ツールを使用してプログラムを実行することをお勧めします。例えば：

    S3 からデータをインポートする場合は、S3storageパスにアクセスできる SecretKey と AccessKey を環境変数としてTiDB Lightningノードに渡します。 `~/.aws/credentials`から資格情報を読み取ることもできます。

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3.  インポートの開始後、ログでキーワード`progress` `grep`実行して、インポートの進行状況を確認できます。デフォルトでは、進行状況は 5 分ごとに更新されます。

4.  TiDB Lightning がインポートを完了すると、自動的に終了します。 `tidb-lightning.log`最後の行に`the whole procedure completed`含まれているかどうかを確認します。はいの場合、インポートは成功です。 「いいえ」の場合、インポートでエラーが発生します。エラー メッセージの指示に従って、エラーに対処します。

> **ノート：**
>
> インポートが成功したかどうかに関係なく、ログの最後の行に`tidb lightning exit`が表示されます。これは、 TiDB Lightning が正常に終了したことを意味しますが、必ずしもインポートが成功したことを意味するものではありません。

インポートに失敗した場合は、トラブルシューティングについて[TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

---
title: Migrate from MySQL-Compatible Databases
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using the Dumpling and TiDB Lightning tools.
---

# MySQL 互換データベースからのデータの移行 {#migrate-data-from-mysql-compatible-databases}

> **ノート：**
>
> MySQL 互換データベースを移行するには、データ移行機能を使用することをお勧めします。 [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

TiDB は MySQL と高い互換性があります。データがセルフホスト型 MySQL インスタンスからのものであっても、パブリック クラウドによって提供される RDS サービスからのものであっても、MySQL 互換データベースから TiDB にスムーズにデータを移行できます。

このドキュメントでは[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)使用して MySQL 互換データベースからデータをエクスポートし、 [<a href="https://docs.pingcap.com/tidb/stable/tidb-lightning-overview">TiDB Lightning</a>](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)論理インポート モードを使用してデータをTiDB Cloudにインポートする方法について説明します。

> **ノート：**
>
> アップストリーム データベースが Amazon Aurora MySQL の場合は、このドキュメントを参照する代わりに、 [<a href="/tidb-cloud/migrate-from-aurora-bulk-import.md">Amazon Aurora MySQL からTiDB Cloudへ一括移行</a>](/tidb-cloud/migrate-from-aurora-bulk-import.md)の手順に従ってください。

## 前提条件 {#prerequisites}

MySQL 互換データベースから TiDB にデータを移行する前に、 TiDB Cloudでサポートされている照合順序が要件を満たしていることを確認してください。

デフォルトでは、 TiDB Cloud は次の CI 照合順序をサポートします。

-   ascii_bin
-   バイナリ
-   latin1_bin
-   utf8_bin
-   utf8_general_ci
-   utf8_unicode_ci
-   utf8mb4_bin
-   utf8mb4_general_ci
-   utf8mb4_unicode_ci

## ステップ 1. TiUPをインストールする {#step-1-install-tiup}

TiUPは TiDB エコシステムのパッケージ マネージャーであり、たった 1 行のコマンドであらゆる TiDB クラスターコンポーネントを実行できるようにします。このドキュメントでは、 TiUP は、 DumplingおよびTiDB Lightningのインストールと実行を支援するために使用されます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、 TiUP は対応する`profile`ファイルの絶対パスを表示します。次のコマンドでは、 `.bash_profile` `profile`ファイルのパスに変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source .bash_profile
    ```

## ステップ 2. MySQL 互換データベースからデータをエクスポートする {#step-2-export-data-from-mysql-compatible-databases}

MySQL からデータをダンプするには、 `mysqldump`や`mydumper`などのいくつかの方法を使用できます。より高いパフォーマンスと、PingCAP によって作成されたオープン ソース ツールの 1 つである TiDB との互換性を確保するには、 [<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)を使用することをお勧めします。

1.  Dumplingをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install dumpling
    ```

2.  Dumplingを使用して MySQL データベースをエクスポートします。

    -   データを Amazon S3 クラウドstorageにエクスポートするには、 [<a href="/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage">データを Amazon S3 クラウドstorageにエクスポートする</a>](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage)を参照してください。
    -   データをローカル データ ファイルにエクスポートするには、次のコマンドを使用します。

        {{< copyable "" >}}

        ```shell
        tiup dumpling -h <mysql-host> -P 3306 -u <user> -F 64MiB -t 8 -o /path/to/export/dir
        ```

        指定した一部のデータベースのみをエクスポートする場合は、 `-B`を使用してデータベース名のカンマ区切りリストを指定します。

        最低限必要な権限は次のとおりです。

        -   `SELECT`
        -   `RELOAD`
        -   `LOCK TABLES`
        -   `REPLICATION CLIENT`

## ステップ 3. データをTiDB Cloudにインポートする {#step-3-import-data-to-tidb-cloud}

ソース データの場所とサイズに応じて、インポート方法は異なります。

-   ソース データが Amazon S3 クラウドstorageにある場合は、次の手順を実行します。

    1.  Amazon S3 アクセスを設定して、TiDB クラウドが Amazon S3 バケット内のソース データにアクセスできるようにします。詳細については、 [<a href="/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access">Amazon S3 アクセスを設定する</a>](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。

    2.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインし、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、 **「クラスター」**ページの左側のナビゲーション・ペインでターゲット・プロジェクトに切り替えることができます。

    3.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート]**をクリックします。

    4.  **[インポート]**ページで、右上隅にある**[データのインポート]**をクリックし、 **[S3 から]**を選択して、インポート関連情報を入力します。

-   ソース データがローカル ファイルにある場合は、次のいずれかを実行します。

    -   データが 1 TB を超える場合は、データをTiDB Cloudにインポートまたは移行するためのステージング領域として Amazon S3 または GCS を使用することをお勧めします。詳細については、 [<a href="/tidb-cloud/migrate-from-amazon-s3-or-gcs.md">Amazon S3 または GCS からTiDB Cloudにインポートまたは移行する</a>](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)を参照してください。
    -   データが 1 TB 未満の場合は、本書の次の手順に従ってTiDB Lightningの論理インポート モードを使用できます。

次の手順では、 TiDB Lightningの論理インポート モードを使用してローカル データをTiDB Cloudにインポートする方法を示します。

1.  TiDB Lightningをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install tidb-lightning
    ```

2.  TiDB Lightning設定ファイルを作成し、インポート情報を設定します。

    1.  TiDB Lightning構成ファイルを作成します。

        {{< copyable "" >}}

        ```shell
        vim tidb-lightning.toml
        ```

    2.  インポート情報を設定します。

        {{< copyable "" >}}

        ```toml
        [lightning]
        # The address and port to check TiDB Lightning metrics.
        status-addr = '127.0.0.1:8289'

        [tidb]
        # The target cluster information. Fill in one address of tidb-server.
        # For example: 172.16.128.1
        host = "${host}"
        # The port number of the target cluster. For example: 4000
        port = ${port number}
        # The target database username. For example: root
        user = "${user_name}"
        # The target database password.
        password = "${password}"

        [tikv-importer]
        # The logical import mode to be used for data importing.
        backend = "tidb"

        [mydumper]
        # The data source directory, supporting local path and s3.
        # For example: `/data` for local path or `s3://bucket-name/data-path` for s3
        data-source-dir = "${data_path}"

        # When Dumpling is used to export data, the corresponding table schemas are exported too by default.
        # If you want TiDB Lightning to automatically create table schemas in TiDB Cloud according to the exported schemas, set no-schema to false.
        no-schema = false
        ```

        ターゲット TiDB クラスターで TLS を構成する場合、またはさらに多くの構成を実行する場合は、 [<a href="https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration">TiDB Lightningコンフィグレーション</a>](https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration)を参照してください。

3.  TiDB Lightningを使用してデータを TiDB にインポートします。

    {{< copyable "" >}}

    ```shell
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

    インポートタスクが開始された後、次のいずれかの方法でインポートの進行状況を確認できます。

    -   コマンド ラインを使用して進行状況を取得するには、 `grep`ログにキーワード`progress`入力します。ログはデフォルトで 5 分ごとに更新されます。
    -   TiDB モニタリング フレームワークを使用してさらに多くのモニタリング メトリクスを取得するには、 [<a href="https://docs.pingcap.com/tidb/stable/monitor-tidb-lightning">TiDB Lightning監視</a>](https://docs.pingcap.com/tidb/stable/monitor-tidb-lightning)を参照してください。

## こちらも参照 {#see-also}

-   [<a href="/tidb-cloud/migrate-incremental-data-from-mysql.md">MySQL 互換データベースからの増分データの移行</a>](/tidb-cloud/migrate-incremental-data-from-mysql.md)

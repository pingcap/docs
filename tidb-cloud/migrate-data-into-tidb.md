---
title: Migrate from MySQL-Compatible Databases
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using the Dumpling and TiDB Lightning tools.
---

# MySQL 互換データベースからデータを移行する {#migrate-data-from-mysql-compatible-databases}

TiDB は MySQL との互換性が高いです。データが自己ホスト型の MySQL インスタンスからのものであろうと、パブリック クラウドによって提供される RDS サービスからのものであろうと、MySQL 互換データベースから TiDB にデータをスムーズに移行できます。

このドキュメントでは、 [Dumpling](/dumpling-overview.md)を使用して MySQL 互換データベースからデータをエクスポートし、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)論理インポート モードを使用してデータをTiDB Cloudにインポートする方法について説明します。

> **ノート：**
>
> アップストリーム データベースが Amazon Aurora MySQL の場合は、このドキュメントを参照する代わりに、 [Amazon Aurora MySQL からTiDB Cloudに一括移行する](/tidb-cloud/migrate-from-aurora-bulk-import.md)の手順に従ってください。

## 前提条件 {#prerequisites}

MySQL 互換データベースから TiDB にデータを移行する前に、サポートされているTiDB Cloudの照合順序が要件を満たしていることを確認してください。

デフォルトでは、 TiDB Cloudは次の CI 照合をサポートしています。

-   ascii_bin
-   バイナリ
-   latin1_bin
-   utf8_bin
-   utf8_general_ci
-   utf8_unicode_ci
-   utf8mb4_bin
-   utf8mb4_general_ci
-   utf8mb4_unicode_ci

## ステップ 1. TiUP をインストールする {#step-1-install-tiup}

TiUP は TiDB エコシステムのパッケージ マネージャーであり、たった 1 行のコマンドで任意の TiDBクラスタコンポーネントを実行するのに役立ちます。このドキュメントでは、TiUP を使用してDumplingとTiDB Lightningをインストールして実行します。

1.  TiUP をダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、TiUP は対応する`profile`ファイルの絶対パスを表示します。次のコマンドでは、 `.bash_profile`を`profile`ファイルのパスに変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source .bash_profile
    ```

## ステップ 2. MySQL 互換データベースからデータをエクスポートする {#step-2-export-data-from-mysql-compatible-databases}

`mysqldump`または`mydumper`を使用するなど、MySQL からデータをダンプするいくつかの方法を使用できます。より高いパフォーマンスと、PingCAP によって作成されたオープン ソース ツールの 1 つである TiDB との互換性のために、 [Dumpling](/dumpling-overview.md)を使用することをお勧めします。

1.  Dumplingをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install dumpling
    ```

2.  Dumplingを使用して MySQL データベースをエクスポートします。

    -   データを Amazon S3 クラウド ストレージにエクスポートするには、 [データを Amazon S3 クラウド ストレージにエクスポートする](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage)を参照してください。
    -   データをローカル データ ファイルにエクスポートするには、次のコマンドを使用します。

        {{< copyable "" >}}

        ```shell
        tiup dumpling -h <mysql-host> -P 3306 -u <user> -F 64MiB -t 8 -o /path/to/export/dir
        ```

        指定した一部のデータベースのみをエクスポートする場合は、 `-B`を使用して、データベース名のコンマ区切りリストを指定します。

        最低限必要な権限は次のとおりです。

        -   `SELECT`
        -   `RELOAD`
        -   `LOCK TABLES`
        -   `REPLICATION CLIENT`

## ステップ 3. データをTiDB Cloudにインポートする {#step-3-import-data-to-tidb-cloud}

ソース データの場所とサイズによって、インポート方法が異なります。

-   ソース データが Amazon S3 クラウド ストレージにある場合は、次の手順を実行します。

    1.  Amazon S3 アクセスを構成して、TiDB クラウドが Amazon S3 バケット内のソース データにアクセスできるようにします。詳細については、 [Amazon S3 アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を参照してください。
    2.  TiDB Cloudコンソールから TiDB クラスター ページに移動し、ターゲットクラスタの名前をクリックして、独自の概要ページに移動します。右上隅にある [**データのインポート**] をクリックし、[<strong>データのインポート タスク</strong>] ページでインポート関連の情報を入力します。

-   ソース データがローカル ファイルにある場合は、次のいずれかを実行します。

    -   データが 1 TB を超える場合は、Amazon S3 または GCS をステージング領域として使用して、データをTiDB Cloudにインポートまたは移行することをお勧めします。詳細については、 [Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)を参照してください。
    -   データが 1 TB 未満の場合は、このドキュメントの次の手順に従って、 TiDB Lightningの論理インポート モードを使用できます。

次の手順は、 TiDB Lightningの論理インポート モードを使用してローカル データをTiDB Cloudにインポートする方法を示しています。

1.  TiDB Lightningをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install tidb-lightning
    ```

2.  TiDB Lightning構成ファイルを作成し、インポート情報を構成します。

    1.  TiDB Lightning構成ファイルを作成します。

        {{< copyable "" >}}

        ```shell
        vim tidb-lighting.toml
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
        # The TiDB backend to be used for data importing. 
        backend = "tidb"

        [mydumper]
        # The data source directory, supporting local path and s3.
        # For example: `/data` for local path or `s3://bucket-name/data-path` for s3
        data-source-dir = "${data_path}"  

        # When Dumpling is used to export data, the corresponding table schemas are exported too by default. 
        # If you want TiDB Lightning to automatically create table schemas in TiDB Cloud according to the exported schemas, set no-schema to false. 
        no-schema = false
        ```

        ターゲットの TiDBクラスタで TLS を構成する場合、またはさらに構成を行う場合は、 [TiDB LightningConfiguration / コンフィグレーション](https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration)を参照してください。

3.  TiDB Lightningを使用して TiDB にデータをインポートします。

    {{< copyable "" >}}

    ```shell
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

    インポート タスクが開始されたら、次のいずれかの方法でインポートの進行状況を表示できます。

    -   コマンド ラインを使用して進行状況を取得するには、ログにキーワード`grep`を入力します。これは、デフォルトで`progress`分ごとに更新されます。
    -   TiDB モニタリング フレームワークを使用してその他のモニタリング メトリックを取得するには、 [TiDB Lightningモニタリング](https://docs.pingcap.com/tidb/stable/monitor-tidb-lightning)を参照してください。
